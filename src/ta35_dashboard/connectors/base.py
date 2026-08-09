"""Read-only public EOD provider interfaces."""

from __future__ import annotations

from datetime import date, datetime
from typing import Protocol, runtime_checkable

from .models import MarketSnapshot


@runtime_checkable
class SnapshotProvider(Protocol):
    def fetch_snapshot(self, as_of: datetime | None = None) -> MarketSnapshot:
        """Return the latest normalized EOD snapshot."""

    def fetch_history(
        self, start: date | None = None, end: date | None = None
    ) -> tuple[MarketSnapshot, ...]:
        """Return normalized snapshots in ascending session order."""


MarketDataConnector = SnapshotProvider
