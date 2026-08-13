"""SQLite persistence for replay-safe public EOD observations and metrics."""

from __future__ import annotations

import json
import sqlite3
from contextlib import contextmanager
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Generator

from ta35_dashboard.connectors import DailyBar, MarketDataType, MarketSnapshot


@dataclass(frozen=True, slots=True)
class MetricValue:
    metric_name: str
    value: float | None
    as_of: datetime
    model_version: str
    run_id: str
    quality_flags: tuple[str, ...] = ()
    dimensions: dict[str, Any] = field(default_factory=dict)


class SQLiteRepository:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)

    @contextmanager
    def _connect(self) -> Generator[sqlite3.Connection, None, None]:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()


    def initialize(self) -> None:
        migrations_dir = Path(__file__).resolve().parents[3] / "migrations"
        migration_files = sorted(migrations_dir.glob("*.sql"))
        with self._connect() as connection:
            for sql_file in migration_files:
                connection.executescript(sql_file.read_text(encoding="utf-8"))


    def insert_snapshot(self, snapshot: MarketSnapshot) -> str:
        self.initialize()
        with self._connect() as connection:
            connection.execute(
                "INSERT OR IGNORE INTO lite_runs VALUES (?, ?, ?, ?, ?, ?)",
                (
                    snapshot.run_id,
                    snapshot.schema_version,
                    snapshot.source,
                    snapshot.source_timestamp.isoformat(),
                    snapshot.received_timestamp.isoformat(),
                    snapshot.market_data_type.value,
                ),
            )
            connection.executemany(
                """INSERT OR REPLACE INTO eod_bars
                   (run_id, symbol, session_date, open, high, low, close, source, quality_flags_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        snapshot.run_id,
                        bar.symbol,
                        bar.session_date.isoformat(),
                        bar.open,
                        bar.high,
                        bar.low,
                        bar.close,
                        bar.source,
                        json.dumps(bar.quality_flags),
                    )
                    for bar in snapshot.bars
                ],
            )
        return snapshot.run_id

    def _snapshot(self, run: sqlite3.Row, bars: list[sqlite3.Row]) -> MarketSnapshot:
        return MarketSnapshot(
            run_id=run["run_id"],
            schema_version=run["schema_version"],
            source=run["source"],
            source_timestamp=datetime.fromisoformat(run["source_timestamp"]),
            received_timestamp=datetime.fromisoformat(run["received_timestamp"]),
            market_data_type=MarketDataType(run["market_data_type"]),
            bars=tuple(
                DailyBar(
                    symbol=row["symbol"],
                    session_date=row["session_date"],
                    open=row["open"],
                    high=row["high"],
                    low=row["low"],
                    close=row["close"],
                    source=row["source"],
                    quality_flags=tuple(json.loads(row["quality_flags_json"])),
                )
                for row in bars
            ),
        )

    def get_snapshot(self, run_id: str) -> MarketSnapshot | None:
        self.initialize()
        with self._connect() as connection:
            run = connection.execute(
                "SELECT * FROM lite_runs WHERE run_id = ?", (run_id,)
            ).fetchone()
            if run is None:
                return None
            bars = connection.execute(
                "SELECT * FROM eod_bars WHERE run_id = ? ORDER BY symbol", (run_id,)
            ).fetchall()
        return self._snapshot(run, bars)

    def latest_snapshot(self) -> MarketSnapshot | None:
        self.initialize()
        with self._connect() as connection:
            run = connection.execute(
                """SELECT * FROM lite_runs
                   ORDER BY source_timestamp DESC, received_timestamp DESC
                   LIMIT 1"""
            ).fetchone()
        return self.get_snapshot(run["run_id"]) if run else None

    def list_snapshots(self, limit: int = 100) -> list[MarketSnapshot]:
        self.initialize()
        with self._connect() as connection:
            ids = [
                row[0]
                for row in connection.execute(
                    "SELECT run_id FROM lite_runs ORDER BY source_timestamp DESC LIMIT ?",
                    (limit,),
                ).fetchall()
            ]
        return [snapshot for run_id in ids if (snapshot := self.get_snapshot(run_id))]

    def bar_history(self, symbol: str, limit: int = 756) -> list[DailyBar]:
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """WITH ranked AS (
                       SELECT eod_bars.*,
                              ROW_NUMBER() OVER (
                                  PARTITION BY session_date
                                  ORDER BY received_timestamp DESC
                              ) AS recency_rank
                       FROM eod_bars JOIN lite_runs USING (run_id)
                       WHERE symbol = ?
                   )
                   SELECT * FROM ranked WHERE recency_rank = 1
                   ORDER BY session_date DESC LIMIT ?""",
                (symbol, limit),
            ).fetchall()
        rows.reverse()
        return [
            DailyBar(
                symbol=row["symbol"],
                session_date=row["session_date"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                source=row["source"],
                quality_flags=tuple(json.loads(row["quality_flags_json"])),
            )
            for row in rows
        ]

    def insert_metrics(self, metrics: list[MetricValue]) -> None:
        if not metrics:
            return
        self.initialize()
        with self._connect() as connection:
            connection.executemany(
                """INSERT OR REPLACE INTO lite_metrics
                   (run_id, metric_name, value, as_of, model_version, quality_flags_json, dimensions_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                [
                    (
                        metric.run_id,
                        metric.metric_name,
                        metric.value,
                        metric.as_of.astimezone(UTC).isoformat(),
                        metric.model_version,
                        json.dumps(metric.quality_flags),
                        json.dumps(metric.dimensions, sort_keys=True),
                    )
                    for metric in metrics
                ],
            )

    def latest_metrics(self, metric_name: str | None = None) -> list[MetricValue]:
        self.initialize()
        # A source-specific refresh (for example Cboe after the TASE close) can
        # create the newest run before its analytics are available.  Keep the
        # dashboard usable by selecting the newest *completed* metric set.
        # Metrics are deliberately kept on one run_id so cards never mix model
        # states from different refreshes.
        with self._connect() as connection:
            run = connection.execute(
                """SELECT lite_runs.run_id
                   FROM lite_runs
                   WHERE EXISTS (
                       SELECT 1 FROM lite_metrics
                       WHERE lite_metrics.run_id = lite_runs.run_id
                   )
                   ORDER BY source_timestamp DESC, received_timestamp DESC
                   LIMIT 1"""
            ).fetchone()
        if run is None:
            return []
        query = "SELECT * FROM lite_metrics WHERE run_id = ?"
        params: tuple[Any, ...] = (run["run_id"],)
        if metric_name:
            query += " AND metric_name = ?"
            params += (metric_name,)
        query += " ORDER BY metric_name, dimensions_json"
        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()
        return [
            MetricValue(
                metric_name=row["metric_name"],
                value=row["value"],
                as_of=datetime.fromisoformat(row["as_of"]),
                model_version=row["model_version"],
                run_id=row["run_id"],
                quality_flags=tuple(json.loads(row["quality_flags_json"])),
                dimensions=json.loads(row["dimensions_json"]),
            )
            for row in rows
        ]

    def insert_chain_snapshots(
        self,
        chain: Any,  # ParsedOptionChain
        source_file: str,
        timestamp: datetime | None = None,
    ) -> None:
        """Insert option chain snapshot quotes into SQLite DB for historical persistence."""
        if not hasattr(chain, "quotes") or not chain.quotes:
            return
        self.initialize()
        ts_str = (timestamp or datetime.now(UTC)).isoformat()
            records = [
                (
                    ts_str,
                    source_file,
                    chain.expiration_label,
                    chain.days_to_expiration,
                    chain.synthetic_spot,
                    q.strike,
                    q.call_bid,
                    q.call_ask,
                    q.call_last,
                    q.call_bid_size,
                    q.call_ask_size,
                    q.call_iv,
                    q.put_bid,
                    q.put_ask,
                    q.put_last,
                    q.put_bid_size,
                    q.put_ask_size,
                    q.put_iv,
                    q.call_contract_id,
                    q.put_contract_id,
                    getattr(chain, "content_hash", None),
                )
                for q in chain.quotes
            ]
            with self._connect() as connection:
                connection.executemany(
                    """INSERT OR IGNORE INTO chain_snapshots
                       (timestamp, source_file, expiration_label, days_to_expiration, synthetic_spot, strike,
                        call_bid, call_ask, call_last, call_bid_size, call_ask_size, call_iv,
                        put_bid, put_ask, put_last, put_bid_size, put_ask_size, put_iv,
                        call_contract_id, put_contract_id, content_hash)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    records,
                )

    def get_chain_snapshot_count(self) -> int:
        """Return total stored historical DDE quote rows."""
        self.initialize()
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) FROM chain_snapshots").fetchone()
            return row[0] if row else 0

    def get_chain_snapshot_summary(self, limit: int = 10) -> list[dict[str, Any]]:
        """Return recent snapshot runs summary."""
        self.initialize()
        with self._connect() as connection:
            rows = connection.execute(
                """SELECT timestamp, source_file, expiration_label, COUNT(*) as quotes_count,
                          MIN(strike) as min_strike, MAX(strike) as max_strike, synthetic_spot
                   FROM chain_snapshots
                   GROUP BY timestamp, source_file, expiration_label
                   ORDER BY timestamp DESC
                   LIMIT ?""",
                (limit,),
            ).fetchall()
            return [dict(r) for r in rows]

