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

    # Plausibility / Sanity Price Checks per Index
    expected_ranges = {
        "TA35": (1500.0, 10000.0, "טווח צפוי: 2,000–8,000 נקודות"),
        "TA_BANKS5": (3000.0, 25000.0, "טווח צפוי: 5,000–18,000 נקודות"),
        "TEL_GOV_ALL": (100.0, 1500.0, "טווח צפוי: 200–800 נקודות"),
        "TEL_BOND60": (100.0, 1500.0, "טווח צפוי: 200–800 נקודות"),
        "VTA35": (3.0, 150.0, "טווח צפוי: 5.0–80.0 אחוזים"),
    }
    if symbol in expected_ranges:
        min_p, max_p, hint_msg = expected_ranges[symbol]
        last_price = bars[-1].close
        if last_price is not None and not (min_p <= last_price <= max_p):
            path.unlink(missing_ok=True)
            raise ValueError(
                f"שגיאת אימות תוכן ב-{symbol}: שער הנעילה ({last_price:,.2f}) חורג מהטווח ההגיוני לסדרה זו ({hint_msg})."
            )

    # Sanity check against existing historical close (single-day jump check)
    if existing and len(bars) < 20:  # only for small incremental deltas, not full history reloads
        last_existing_close = existing[-1].close
        # Skip jump check if transitioning from demo data scale to real market scale
        if last_existing_close is not None and last_existing_close > 0:
            is_demo_transition = (symbol == "TA_BANKS5" and last_existing_close < 3000.0 and bars[-1].close > 5000.0)
            if not is_demo_transition:
                for bar in bars:
                    if bar.close is not None and bar.session_date >= existing[-1].session_date:
                        ratio = abs(bar.close / last_existing_close - 1.0)
                        if ratio > 0.35:  # Single day jump > 35%
                            path.unlink(missing_ok=True)
                            raise ValueError(
                                f"שגיאת אימות ב-{symbol}: שינוי יומי חריג של {ratio:.1%} (משער {last_existing_close:,.2f} לשער {bar.close:,.2f}). נראה שקובץ הנתונים שייך למדד אחר."
                            )
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


def auto_detect_series(raw: bytes, filename: str = "") -> str:
    """Automatically detect the financial series/symbol from CSV content and filename."""
    sample = ""
    for enc in ("utf-8-sig", "utf-8", "windows-1255", "iso-8859-8", "utf-16"):
        try:
            sample = raw[:2048].decode(enc)
            break
        except UnicodeDecodeError:
            continue

    # Look only at the first 3 lines to avoid matching numbers in the data rows (like market cap)
    lines = sample.splitlines()[:3]
    header_text = " ".join(lines).lower()
    full_text = (header_text + " " + filename).lower()

    # 1. VTA35 (Implied volatility index)
    if any(k in full_text for k in ("vta35", "vta-35", "vta 35", "598", "תנודתיות", "volatility")):
        return "VTA35"

    # 2. TA-Banks 5
    if any(k in full_text for k in ("banks", "בנקים", "164", "147")):
        return "TA_BANKS5"

    # 3. Tel-Gov 10Y+
    if any(k in full_text for k in ("gov 10", "gov-10", "gov10", "10y", "10+", "שקלי 10", "607")):
        return "TEL_GOV_10Y"

    # 4. Tel-Gov 0-2
    if any(k in full_text for k in ("gov 0-2", "gov 2", "0-2", "2y", "שקלי 0-2", "603")):
        return "TEL_GOV_2Y"

    # 5. Tel-Bond 60
    if any(k in full_text for k in ("bond 60", "bond-60", "bond60", "בונד 60", "בונד-60", "703")):
        return "TEL_BOND60"

    # 6. Tel-Gov All
    if any(k in full_text for k in ("gov all", "gov-all", "govall", "תל גוב-כללי", "תל גוב כללי", "תל-גוב כללי", "גוב כללי", "תל גוב", "601")):
        return "TEL_GOV_ALL"

    # 7. USD/ILS
    if any(k in full_text for k in ("usd/ils", "usdils", "שער דולר", "דולר")):
        return "USDILS"

    # 8. TA-35
    if any(k in full_text for k in ("ta-35", "ta 35", "ta35", "ת\"א-35", "ת״א-35", "ת\"א 35", "ת״א 35", "תל אביב 35", "142")):
        return "TA35"

    return "TA35"


def import_tase_uploads(
    database_path: Path,
    downloads_dir: Path,
    uploads: Mapping[str, bytes],
) -> TaseUploadResult:
    """Validate uploads, auto-detect series from content, import into staged DB, then activate it."""

    SUPPORTED = {
        "TA35",
        "VTA35",
        "USDILS",
        "VIX9D",
        "VIX",
        "VIX3M",
        "TA_BANKS5",
        "TEL_GOV_ALL",
        "TEL_GOV_10Y",
        "TEL_GOV_2Y",
        "TEL_BOND60",
    }
    
    raw_payloads = {key: raw for key, raw in uploads.items() if raw}
    if not raw_payloads:
        raise ValueError("לא נבחרו קבצים לעדכון.")

    # Automatically analyze content of each uploaded file and map to the true series symbol
    payloads: dict[str, bytes] = {}
    for key, raw in raw_payloads.items():
        detected = auto_detect_series(raw, filename=key)
        symbol = detected if detected in SUPPORTED else (key if key in SUPPORTED else "TA35")
        payloads[symbol] = raw

    database_path = Path(database_path)
    downloads_dir = Path(downloads_dir)
    current = SQLiteRepository(database_path)

    existing_ta35 = current.bar_history("TA35", 1)
    if "TA35" not in payloads and not existing_ta35:
        raise ValueError("בטעינה ראשונית של המערכת יש צורך בקובץ ת״א־35.")

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

        def _source_for(s: str) -> str:
            if s.startswith("VIX"):
                return "Cboe"
            if s == "USDILS":
                return "Bank of Israel"
            return "TASE"

        specs = tuple(
            CsvSeriesSpec(symbol, path, _source_for(symbol), True, True)
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
