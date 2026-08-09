"""Import official public CSV exports into the Lite database."""

from __future__ import annotations

import argparse
from pathlib import Path

from ta35_dashboard.config import SETTINGS
from ta35_dashboard.connectors import (
    CsvSeriesSpec,
    PublicCsvEodProvider,
    official_cboe_specs,
)
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.storage import SQLiteRepository


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=SETTINGS.database_path)
    parser.add_argument("--ta35", type=Path, help="TASE TA35 historical CSV export")
    parser.add_argument("--vta35", type=Path, help="TASE VTA35 historical CSV export")
    parser.add_argument("--usdils", type=Path, help="Bank of Israel USD/ILS CSV export")
    parser.add_argument("--vix9d", type=Path, help="local Cboe VIX9D CSV export")
    parser.add_argument("--vix", type=Path, help="local Cboe VIX CSV export")
    parser.add_argument("--vix3m", type=Path, help="local Cboe VIX3M CSV export")
    parser.add_argument(
        "--cboe",
        action="store_true",
        help="download VIX9D, VIX and VIX3M official CSVs",
    )
    args = parser.parse_args()
    specs: list[CsvSeriesSpec] = []
    for symbol, path, source, dayfirst in (
        ("TA35", args.ta35, "TASE", True),
        ("VTA35", args.vta35, "TASE", True),
        ("USDILS", args.usdils, "Bank of Israel", False),
        ("VIX9D", args.vix9d, "Cboe", False),
        ("VIX", args.vix, "Cboe", False),
        ("VIX3M", args.vix3m, "Cboe", False),
    ):
        if path:
            specs.append(
                CsvSeriesSpec(symbol, path, source, manual=True, dayfirst=dayfirst)
            )
    if args.cboe:
        specs.extend(official_cboe_specs())
    if not specs:
        parser.error("provide at least one CSV path or --cboe")
    repository = SQLiteRepository(args.db)
    runs = collect_history(PublicCsvEodProvider(tuple(specs)), repository)
    print(f"Imported {len(runs)} EOD sessions into {args.db}")


if __name__ == "__main__":
    main()
