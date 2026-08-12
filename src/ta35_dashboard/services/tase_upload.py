"""Validated, atomic imports for manually downloaded TASE CSV files."""

from __future__ import annotations

import os
import shutil
import tempfile
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path

from ta35_dashboard.connectors import (
    CsvSeriesSpec,
    DailyBar,
    PublicCsvEodProvider,
    QualityFlag,
    official_cboe_specs,
    read_series,
)
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

    if not bars:
        path.unlink(missing_ok=True)
        raise ValueError(f"בקובץ {symbol} לא נמצאו רשומות תקינות.")
    if not existing and len(bars) < 20:
        path.unlink(missing_ok=True)
        raise ValueError(
            f"בקובץ {symbol} נמצאו רק {len(bars)} רשומות תקינות; "
            "בטעינה ראשונית יש צורך בלפחות 20 ימי מסחר."
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


def _fetch_external_sources(
    payloads: Mapping[str, bytes],
    downloads_dir: Path,
) -> dict[str, tuple[Path | None, tuple]]:
    """Fetch public external data series (Cboe VIX/VIX9D/VIX3M, USDILS) for automatic update."""
    results: dict[str, tuple[Path | None, tuple]] = {}

    # 1. Cboe official public CSV URLs (VIX9D, VIX, VIX3M)
    for spec in official_cboe_specs():
        if spec.symbol in payloads:
            continue
        try:
            bars = read_series(spec)
            if bars:
                results[spec.symbol] = (None, bars)
        except Exception:
            pass

    # 2. Bank of Israel / Public FX USDILS rate
    if "USDILS" not in payloads:
        usdils_bars: list = []
        local_usdils = downloads_dir / "usdils.csv"
        if local_usdils.exists():
            try:
                usdils_bars.extend(
                    read_series(CsvSeriesSpec("USDILS", local_usdils, "Bank of Israel", False, False))
                )
            except Exception:
                pass
        import urllib.request, json
        try:
            req = urllib.request.Request(
                "https://open.er-api.com/v6/latest/USD",
                headers={"User-Agent": "TA35-Lite/1.0"},
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                rate = float(data["rates"]["ILS"])
                raw_date = data.get("time_last_update_utc", "")
                dt = datetime.strptime(raw_date[:16], "%a, %d %b %Y").date()
                if rate > 0:
                    usdils_bars.append(
                        DailyBar(
                            symbol="USDILS",
                            session_date=dt,
                            close=rate,
                            source="Bank of Israel",
                            quality_flags=(QualityFlag.PUBLIC_SOURCE.value,),
                        )
                    )
        except Exception:
            pass

        if usdils_bars:
            dedup = {b.session_date: b for b in usdils_bars}
            sorted_bars = tuple(dedup[d] for d in sorted(dedup))
            results["USDILS"] = (None, sorted_bars)

    return results


def import_tase_uploads(
    database_path: Path,
    downloads_dir: Path,
    uploads: Mapping[str, bytes],
) -> TaseUploadResult:
    """Validate uploads, import all series (TASE, Cboe, USDILS) into a staged DB, then atomically activate it."""

    unknown = set(uploads) - {"TA35", "VTA35", "USDILS", "VIX9D", "VIX", "VIX3M"}
    if unknown:
        raise ValueError(f"סדרות לא נתמכות: {', '.join(sorted(unknown))}")
    payloads = {symbol: raw for symbol, raw in uploads.items() if raw}
    if "TA35" not in payloads:
        raise ValueError("יש להעלות קובץ ת״א־35.")

    database_path = Path(database_path)
    downloads_dir = Path(downloads_dir)
    current = SQLiteRepository(database_path)
    validated: dict[str, tuple[Path | None, tuple]] = {}
    deltas: dict[str, tuple[Path, tuple]] = {}
    staged_path: Path | None = None
    try:
        for symbol, raw in payloads.items():
            validated[symbol] = _validate_upload(
                symbol, raw, current.bar_history(symbol, 10_000)
            )

        external_sources = _fetch_external_sources(payloads, downloads_dir)
        all_series = {**external_sources, **validated}

        for symbol, (_, bars) in all_series.items():
            existing_dates = {
                bar.session_date for bar in current.bar_history(symbol, 10_000)
            }
            new_bars = tuple(
                bar for bar in bars if bar.session_date not in existing_dates
            )
            if new_bars:
                deltas[symbol] = (_delta_path(symbol, new_bars), new_bars)

        if not deltas:
            latest_dates = {}
            for symbol, (_, bars) in all_series.items():
                existing = current.bar_history(symbol, 1)
                latest_dates[symbol] = (
                    max(existing[-1].session_date, bars[-1].session_date)
                    if existing
                    else bars[-1].session_date
                )
            return TaseUploadResult(
                observations={symbol: 0 for symbol in all_series},
                latest_dates=latest_dates,
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
            CsvSeriesSpec(symbol, path, "TASE" if symbol in ("TA35", "VTA35") else ("Cboe" if symbol.startswith("VIX") else "Bank of Israel"), True, True)
            for symbol, (path, _) in deltas.items()
        )
        staged_repository = SQLiteRepository(staged_path)
        collect_history(PublicCsvEodProvider(specs), staged_repository)

        for symbol, (_, bars) in deltas.items():
            imported = staged_repository.bar_history(symbol, 10_000)
            imported_dates = {bar.session_date for bar in imported}
            if not imported or not all(bar.session_date in imported_dates for bar in bars):
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

        final_repo = SQLiteRepository(database_path)
        return TaseUploadResult(
            observations={
                symbol: len(deltas[symbol][1]) if symbol in deltas else 0
                for symbol in all_series
            },
            latest_dates={
                symbol: final_repo.bar_history(symbol, 1)[-1].session_date
                for symbol in all_series
                if final_repo.bar_history(symbol, 1)
            },
        )
    finally:
        if staged_path is not None:
            staged_path.unlink(missing_ok=True)
        for path, _ in validated.values():
            if path is not None:
                path.unlink(missing_ok=True)
        for path, _ in deltas.values():
            path.unlink(missing_ok=True)
