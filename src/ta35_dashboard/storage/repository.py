"""SQLite persistence for replay-safe public EOD observations and metrics."""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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

    def _connect(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def initialize(self) -> None:
        migration = (
            Path(__file__).resolve().parents[3] / "migrations" / "001_initial.sql"
        )
        with self._connect() as connection:
            connection.executescript(migration.read_text(encoding="utf-8"))

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
                """SELECT eod_bars.* FROM eod_bars
                   JOIN lite_runs USING (run_id)
                   WHERE symbol = ?
                   ORDER BY session_date DESC, received_timestamp DESC""",
                (symbol,),
            ).fetchall()
        unique = {}
        for row in rows:
            unique.setdefault(row["session_date"], row)
        rows = list(unique.values())[:limit]
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
        snapshot = self.latest_snapshot()
        if snapshot is None:
            return []
        query = "SELECT * FROM lite_metrics WHERE run_id = ?"
        params: tuple[Any, ...] = (snapshot.run_id,)
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
