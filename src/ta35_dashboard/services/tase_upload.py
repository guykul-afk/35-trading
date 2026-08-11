"""Validated, atomic imports for manually downloaded TASE CSV files."""

from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

from ta35_dashboard.connectors import CsvSeriesSpec, PublicCsvEodProvider, read_series
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.storage import SQLiteRepository


@dataclass(frozen=True, slots=True)
class TaseUploadResult:
    """Outcome of a manual import; counts include newly stored days only."""

    observations: Mapping[str, int]
    latest_dates: Mapping[str, date]


def _validate_upload(symbol: str, raw: bytes, existing: list) -> tuple[Path, tuple]:
    if not raw:
        raise ValueError(f"הקובץ של {symbol} ריק.")
    if len(raw) > 20 * 1024 * 1024:
        raise ValueError(f"הקובץ של {symbol} גדול מ־20MB.")

    with tempfile.NamedTemporaryFile(suffix=".csv", delete=False) as handle:
        path = Path(handle.name)
        handle.write(raw)
    try:
        bars = read_series(CsvSeriesSpec(symbol, path, "TASE", True, True))
    except Exception:
        path.unlink(missing_ok=True)
        raise

    if len(bars) < 20:
        path.unlink(missing_ok=True)
        raise ValueError(
            f"בקובץ {symbol} נמצאו רק {len(bars)} רשומות תקינות; "
            "יש לבחור טווח של 3 שנים באתר הבורסה."
        )
    if symbol == "TA35" and any(None in (bar.open, bar.high, bar.low) for bar in bars):
        path.unlink(missing_ok=True)
        raise ValueError("קובץ ת״א־35 חייב לכלול עמודות פתיחה, גבוה, נמוך ונעילה.")
    if bars[-1].session_date > datetime.now(UTC).date():
        path.unlink(missing_ok=True)
        raise ValueError(f"קובץ {symbol} כולל תאריך עתידי ואינו תקין.")
    return path, bars


def _delta_path(symbol: str, bars: tuple) -> Path:
    """Create a temporary CSV containing only observations absent from the DB."""

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", encoding="utf-8", newline="", delete=False
    ) as handle:
        path = Path(handle.name)
        handle.write("Date,Open,High,Low,Close\n")
        for bar in bars:
            values = (bar.open, bar.high, bar.low, bar.close)
            handle.write(
                f"{bar.session_date.isoformat()},"
                f"{'' if values[0] is None else values[0]},"
                f"{'' if values[1] is None else values[1]},"
                f"{'' if values[2] is None else values[2]},{values[3]}\n"
            )
    return path


def import_tase_uploads(
    database_path: Path,
    downloads_dir: Path,
    uploads: Mapping[str, bytes],
) -> TaseUploadResult:
    """Validate uploads, import into a staged DB, then atomically activate it."""

    unknown = set(uploads) - {"TA35", "VTA35"}
    if unknown:
        raise ValueError(f"סדרות לא נתמכות: {', '.join(sorted(unknown))}")
    payloads = {symbol: raw for symbol, raw in uploads.items() if raw}
    if "TA35" not in payloads:
        raise ValueError("יש להעלות קובץ ת״א־35.")

    database_path = Path(database_path)
    downloads_dir = Path(downloads_dir)
    current = SQLiteRepository(database_path)
    validated: dict[str, tuple[Path, tuple]] = {}
    deltas: dict[str, tuple[Path, tuple]] = {}
    staged_path: Path | None = None
    try:
        for symbol, raw in payloads.items():
            validated[symbol] = _validate_upload(
                symbol, raw, current.bar_history(symbol, 10_000)
            )

        for symbol, (_, bars) in validated.items():
            existing_dates = {
                bar.session_date for bar in current.bar_history(symbol, 10_000)
            }
            new_bars = tuple(
                bar for bar in bars if bar.session_date not in existing_dates
            )
            if new_bars:
                deltas[symbol] = (_delta_path(symbol, new_bars), new_bars)

        if not deltas:
            return TaseUploadResult(
                observations={symbol: 0 for symbol in validated},
                latest_dates={
                    symbol: bars[-1].session_date
                    for symbol, (_, bars) in validated.items()
                },
            )

        database_path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, staged_name = tempfile.mkstemp(
            prefix="ta35-upload-", suffix=".sqlite3", dir=database_path.parent
        )
        os.close(descriptor)
        staged_path = Path(staged_name)
        if database_path.exists():
            shutil.copy2(database_path, staged_path)

        specs = tuple(
            CsvSeriesSpec(symbol, path, "TASE", True, True)
            for symbol, (path, _) in deltas.items()
        )
        staged_repository = SQLiteRepository(staged_path)
        collect_history(PublicCsvEodProvider(specs), staged_repository)

        for symbol, (_, bars) in deltas.items():
            imported = staged_repository.bar_history(symbol, 10_000)
            if not imported or imported[-1].session_date != bars[-1].session_date:
                raise RuntimeError(f"אימות הייבוא של {symbol} נכשל.")

        if database_path.exists():
            backup_dir = database_path.parent / "backups"
            backup_dir.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
            backup_path = backup_dir / f"before-tase-upload-{stamp}.sqlite3"
            shutil.copy2(database_path, backup_path)
        os.replace(staged_path, database_path)
        staged_path = None

        downloads_dir.mkdir(parents=True, exist_ok=True)
        for symbol, raw in payloads.items():
            target = downloads_dir / f"{symbol.lower()}.csv"
            descriptor, staged_csv_name = tempfile.mkstemp(
                prefix=f".{target.stem}-", suffix=".csv", dir=downloads_dir
            )
            with os.fdopen(descriptor, "wb") as stream:
                stream.write(raw)
            os.replace(staged_csv_name, target)

        return TaseUploadResult(
            observations={
                symbol: len(deltas[symbol][1]) if symbol in deltas else 0
                for symbol in validated
            },
            latest_dates={
                symbol: bars[-1].session_date for symbol, (_, bars) in validated.items()
            },
        )
    finally:
        if staged_path is not None:
            staged_path.unlink(missing_ok=True)
        for path, _ in validated.values():
            path.unlink(missing_ok=True)
        for path, _ in deltas.values():
            path.unlink(missing_ok=True)
