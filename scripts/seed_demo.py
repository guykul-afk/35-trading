"""Seed clearly-labelled synthetic EOD data for a first-run preview."""

from __future__ import annotations

import argparse
from pathlib import Path

from ta35_dashboard.config import SETTINGS
from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.storage import SQLiteRepository


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=SETTINGS.database_path)
    parser.add_argument("--days", type=int, default=800)
    args = parser.parse_args()
    repository = SQLiteRepository(args.db)
    runs = collect_history(DemoEodProvider(days=args.days), repository)
    print(f"Seeded {len(runs)} DEMO EOD sessions into {args.db}")


if __name__ == "__main__":
    main()
