"""Generate the comprehensive TA-35 backtest knowledge-base document."""

from __future__ import annotations

import argparse
from pathlib import Path

from ta35_dashboard.config import PROJECT_ROOT, SETTINGS
from ta35_dashboard.services import run_research_backtest, write_research_report
from ta35_dashboard.services.dashboard import CARD_DEFINITIONS
from ta35_dashboard.storage import SQLiteRepository


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--database", type=Path, default=SETTINGS.database_path)
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_ROOT / "docs" / "backtest-research-report.md",
    )
    args = parser.parse_args()
    repository = SQLiteRepository(args.database)
    keys = tuple(definition[0] for definition in CARD_DEFINITIONS)
    report = run_research_backtest(repository, indicator_keys=keys)
    destination = write_research_report(report, args.output)
    print(
        f"Wrote {destination} with {report.observations:,} TA-35 sessions "
        f"and {len(report.tables)} result tables."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
