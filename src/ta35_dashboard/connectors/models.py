"""Validated end-of-day data contracts for the Lite dashboard."""

from __future__ import annotations

from datetime import UTC, date, datetime
from enum import StrEnum
from hashlib import sha256
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

PositiveFloat = Annotated[float, Field(gt=0)]
NonNegativeFloat = Annotated[float, Field(ge=0)]


class MarketDataType(StrEnum):
    EOD = "eod"
    DEMO = "demo"


class QualityFlag(StrEnum):
    MISSING_OHLC = "missing_ohlc"
    STALE = "stale"
    MANUAL_IMPORT = "manual_import"
    PUBLIC_SOURCE = "public_source"
    DEMO = "demo"


class DailyBar(BaseModel):
    """One public end-of-day observation.

    OHLC is optional for external stress series. TA35 needs OHLC for range and
    gap estimators; the pipeline degrades to close-to-close RV when unavailable.
    """

    model_config = ConfigDict(extra="forbid", frozen=True)

    symbol: str = Field(min_length=1)
    session_date: date
    close: PositiveFloat
    open: PositiveFloat | None = None
    high: PositiveFloat | None = None
    low: PositiveFloat | None = None
    source: str = Field(min_length=1)
    quality_flags: tuple[str, ...] = ()

    @model_validator(mode="after")
    def validate_range(self) -> DailyBar:
        supplied = (self.open, self.high, self.low)
        if any(value is not None for value in supplied) and not all(
            value is not None for value in supplied
        ):
            raise ValueError("open, high and low must be supplied together")
        if self.high is not None and self.low is not None and self.open is not None:
            if self.low > self.high:
                raise ValueError("low must not exceed high")
            if self.high < max(self.open, self.close) or self.low > min(
                self.open, self.close
            ):
                raise ValueError("high/low must contain open and close")
        return self


class MarketSnapshot(BaseModel):
    """A replay-safe batch of public EOD bars for one session date."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal["2.0"] = "2.0"
    run_id: str = Field(min_length=1)
    source: str = Field(min_length=1)
    source_timestamp: datetime
    received_timestamp: datetime
    market_data_type: MarketDataType = MarketDataType.EOD
    bars: tuple[DailyBar, ...]

    @field_validator("source_timestamp", "received_timestamp")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("timestamps must be timezone-aware UTC")
        if value.utcoffset().total_seconds() != 0:
            raise ValueError("timestamps must be stored in UTC")
        return value.astimezone(UTC)

    @model_validator(mode="after")
    def validate_snapshot(self) -> MarketSnapshot:
        if self.received_timestamp < self.source_timestamp:
            raise ValueError("received_timestamp cannot precede source_timestamp")
        if not self.bars:
            raise ValueError("snapshot must contain at least one bar")
        dates = {bar.session_date for bar in self.bars}
        if len(dates) != 1:
            raise ValueError("all bars in a snapshot must share one session date")
        symbols = [bar.symbol for bar in self.bars]
        if len(symbols) != len(set(symbols)):
            raise ValueError("symbol must be unique within a snapshot")
        return self

    @property
    def session_date(self) -> date:
        return self.bars[0].session_date

    def bar(self, symbol: str) -> DailyBar | None:
        return next((bar for bar in self.bars if bar.symbol == symbol), None)


def snapshot_id(session_date: date, bars: tuple[DailyBar, ...]) -> str:
    values = "|".join(
        f"{bar.symbol}:{bar.close:.10g}:{bar.open}:{bar.high}:{bar.low}"
        for bar in sorted(bars, key=lambda item: item.symbol)
    )
    return (
        "eod-"
        + sha256(f"{session_date.isoformat()}|{values}".encode()).hexdigest()[:20]
    )
