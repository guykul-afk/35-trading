"""Public CSV ingestion with no credentials, account access or order APIs."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import UTC, date, datetime
from io import StringIO
from pathlib import Path
from urllib.request import Request, urlopen

import pandas as pd

from .models import DailyBar, MarketDataType, MarketSnapshot, QualityFlag, snapshot_id

CBOE_URLS = {
    "VIX9D": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX9D_History.csv",
    "VIX": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
    "VIX3M": "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv",
}


@dataclass(frozen=True)
class CsvSeriesSpec:
    symbol: str
    location: str | Path
    source: str
    manual: bool = False
    dayfirst: bool = False


def _key(value: object) -> str:
    return re.sub(r"[^a-z0-9א-ת]", "", str(value).strip().lower())


ALIASES = {
    "date": {"date", "tradedate", "sessiondate", "timeperiod", "תאריך", "תאריךמסחר"},
    "open": {"open", "opening", "openingrate", "שערפתיחה", "פתיחה"},
    "high": {"high", "highrate", "שערגבוה", "גבוה"},
    "low": {"low", "lowrate", "שערנמוך", "נמוך"},
    "close": {
        "close",
        "closing",
        "closingrate",
        "last",
        "value",
        "obsvalue",
        "שערנעילה",
        "נעילה",
        "שער",
    },
}


def _csv_table(text: str) -> str:
    """Strip informational rows that TASE places before the CSV header."""

    lines = text.splitlines()
    date_keys = {_key(value) for value in ALIASES["date"]}
    close_keys = {_key(value) for value in ALIASES["close"]}
    for index, line in enumerate(lines[:25]):
        columns = next(csv.reader([line]), [])
        keys = {_key(column) for column in columns}
        if keys & date_keys and keys & close_keys:
            return "\n".join(lines[index:])
    return text


def _column(frame: pd.DataFrame, name: str, required: bool = True) -> str | None:
    normalized = {_key(column): str(column) for column in frame.columns}
    for alias in ALIASES[name]:
        if _key(alias) in normalized:
            return normalized[_key(alias)]
    if required:
        raise ValueError(f"CSV is missing a recognizable {name} column")
    return None


def _read_bytes(location: str | Path) -> bytes:
    if isinstance(location, Path) or not str(location).startswith(
        ("http://", "https://")
    ):
        return Path(location).read_bytes()
    request = Request(str(location), headers={"User-Agent": "TA35-Lite/1.0"})
    with urlopen(request, timeout=30) as response:
        return response.read()


def _parse_date(value: object, *, dayfirst: bool) -> pd.Timestamp:
    cleaned = str(value).strip()
    if re.fullmatch(r"\d{4}[-/]\d{1,2}[-/]\d{1,2}", cleaned):
        return pd.to_datetime(
            cleaned.replace("/", "-"), format="%Y-%m-%d", errors="coerce"
        )
    return pd.to_datetime(cleaned, dayfirst=dayfirst, errors="coerce")


def read_series(spec: CsvSeriesSpec) -> tuple[DailyBar, ...]:
    raw = _read_bytes(spec.location)
    try:
        text = raw.decode("utf-8-sig")
    except UnicodeDecodeError:
        text = raw.decode("cp1255")
    frame = pd.read_csv(StringIO(_csv_table(text)))
    date_col = _column(frame, "date")
    close_col = _column(frame, "close")
    open_col = _column(frame, "open", required=False)
    high_col = _column(frame, "high", required=False)
    low_col = _column(frame, "low", required=False)
    has_ohlc = all((open_col, high_col, low_col))
    bars: list[DailyBar] = []
    for _, row in frame.iterrows():
        parsed_date = _parse_date(row[date_col], dayfirst=spec.dayfirst)
        close = pd.to_numeric(
            str(row[close_col]).replace(",", "").replace("%", ""), errors="coerce"
        )
        if pd.isna(parsed_date) or pd.isna(close) or float(close) <= 0:
            continue
        values = {}
        if has_ohlc:
            parsed = [
                pd.to_numeric(str(row[column]).replace(",", ""), errors="coerce")
                for column in (open_col, high_col, low_col)
            ]
            if not any(pd.isna(value) for value in parsed):
                values = dict(
                    zip(("open", "high", "low"), map(float, parsed), strict=True)
                )
        flags = [QualityFlag.PUBLIC_SOURCE.value]
        if spec.manual:
            flags.append(QualityFlag.MANUAL_IMPORT.value)
        if spec.symbol == "TA35" and not values:
            flags.append(QualityFlag.MISSING_OHLC.value)
        bar_values = {
            "symbol": spec.symbol,
            "session_date": parsed_date.date(),
            "close": float(close),
            "source": spec.source,
            "quality_flags": tuple(flags),
            **values,
        }
        try:
            bars.append(DailyBar(**bar_values))
        except ValueError:
            # Some historical Cboe rows contain internally inconsistent OHLC
            # values. The Lite analytics use only the close for stress series,
            # so retain that official observation instead of dropping the day.
            if spec.symbol == "TA35" or not values:
                raise
            for name in ("open", "high", "low"):
                bar_values.pop(name, None)
            bars.append(DailyBar(**bar_values))
    if not bars:
        raise ValueError(f"no valid observations found for {spec.symbol}")
    deduplicated = {bar.session_date: bar for bar in bars}
    return tuple(deduplicated[session] for session in sorted(deduplicated))


class PublicCsvEodProvider:
    """Merge independent public CSV series into daily snapshots."""

    source = "public-csv-eod"

    def __init__(self, specs: tuple[CsvSeriesSpec, ...]) -> None:
        if not specs:
            raise ValueError("at least one CSV series is required")
        if len({spec.symbol for spec in specs}) != len(specs):
            raise ValueError("CSV symbols must be unique")
        self.specs = specs

    def fetch_history(
        self, start: date | None = None, end: date | None = None
    ) -> tuple[MarketSnapshot, ...]:
        by_date: dict[date, list[DailyBar]] = {}
        for spec in self.specs:
            for bar in read_series(spec):
                if (start and bar.session_date < start) or (
                    end and bar.session_date > end
                ):
                    continue
                by_date.setdefault(bar.session_date, []).append(bar)
        received = datetime.now(UTC)
        snapshots: list[MarketSnapshot] = []
        for session in sorted(by_date):
            bars = tuple(sorted(by_date[session], key=lambda bar: bar.symbol))
            source_timestamp = datetime.combine(
                session, datetime.min.time(), tzinfo=UTC
            )
            snapshots.append(
                MarketSnapshot(
                    run_id=snapshot_id(session, bars),
                    source=self.source,
                    source_timestamp=source_timestamp,
                    received_timestamp=max(received, source_timestamp),
                    market_data_type=MarketDataType.EOD,
                    bars=bars,
                )
            )
        return tuple(snapshots)

    def fetch_snapshot(self, as_of: datetime | None = None) -> MarketSnapshot:
        snapshots = self.fetch_history(end=as_of.date() if as_of else None)
        if not snapshots:
            raise LookupError("no public EOD observations for requested date")
        return snapshots[-1]


def official_cboe_specs() -> tuple[CsvSeriesSpec, ...]:
    return tuple(
        CsvSeriesSpec(symbol=symbol, location=url, source="Cboe")
        for symbol, url in CBOE_URLS.items()
    )
