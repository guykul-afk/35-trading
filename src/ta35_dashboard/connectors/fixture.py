"""Deterministic EOD demo provider used only by tests and first-run preview."""

from __future__ import annotations

import math
from datetime import UTC, date, datetime, timedelta

from .models import DailyBar, MarketDataType, MarketSnapshot, QualityFlag, snapshot_id


class DemoEodProvider:
    source = "deterministic-demo"

    def __init__(self, days: int = 800, end: date = date(2026, 8, 7)) -> None:
        self.days = days
        self.end = end

    def fetch_history(
        self, start: date | None = None, end: date | None = None
    ) -> tuple[MarketSnapshot, ...]:
        sessions: list[date] = []
        cursor = self.end
        while len(sessions) < self.days:
            if cursor.weekday() < 5:
                sessions.append(cursor)
            cursor -= timedelta(days=1)
        sessions.reverse()
        snapshots: list[MarketSnapshot] = []
        ta35_close = 2250.0
        usdils = 3.55
        for index, session in enumerate(sessions):
            if start and session < start:
                continue
            if end and session > end:
                continue
            daily_return = (
                0.00035 + 0.006 * math.sin(index / 17) + 0.003 * math.sin(index / 5)
            )
            previous = ta35_close
            ta35_close *= math.exp(daily_return)
            opening = previous * math.exp(0.0025 * math.sin(index / 11))
            spread = 0.007 + 0.004 * abs(math.sin(index / 13))
            high = max(opening, ta35_close) * (1 + spread / 2)
            low = min(opening, ta35_close) * (1 - spread / 2)
            realized_proxy = 14 + 5 * abs(math.sin(index / 19))
            vta35 = realized_proxy + 3 + 2 * math.sin(index / 23)
            usdils *= math.exp(
                -0.0001 - 0.0012 * daily_return + 0.0015 * math.sin(index / 29)
            )
            vix = 15 + 5 * abs(math.sin(index / 31))
            bars = tuple(
                sorted(
                    (
                        DailyBar(
                            symbol="TA35",
                            session_date=session,
                            open=opening,
                            high=high,
                            low=low,
                            close=ta35_close,
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                        DailyBar(
                            symbol="VTA35",
                            session_date=session,
                            close=vta35,
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                        DailyBar(
                            symbol="USDILS",
                            session_date=session,
                            close=usdils,
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                        DailyBar(
                            symbol="VIX9D",
                            session_date=session,
                            close=vix * (0.92 + 0.12 * math.sin(index / 9)),
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                        DailyBar(
                            symbol="VIX",
                            session_date=session,
                            close=vix,
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                        DailyBar(
                            symbol="VIX3M",
                            session_date=session,
                            close=vix * 1.08,
                            source=self.source,
                            quality_flags=(QualityFlag.DEMO.value,),
                        ),
                    ),
                    key=lambda bar: bar.symbol,
                )
            )
            timestamp = datetime.combine(session, datetime.min.time(), tzinfo=UTC)
            snapshots.append(
                MarketSnapshot(
                    run_id=snapshot_id(session, bars),
                    source=self.source,
                    source_timestamp=timestamp,
                    received_timestamp=timestamp,
                    market_data_type=MarketDataType.DEMO,
                    bars=bars,
                )
            )
        return tuple(snapshots)

    def fetch_snapshot(self, as_of: datetime | None = None) -> MarketSnapshot:
        end = as_of.date() if as_of else None
        history = self.fetch_history(end=end)
        if not history:
            raise LookupError("no demo EOD data for requested date")
        return history[-1]


FixtureSnapshotProvider = DemoEodProvider
FixtureConnector = DemoEodProvider
