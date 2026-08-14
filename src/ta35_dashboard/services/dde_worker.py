"""Standalone DDE Background Worker.

Continuously monitors DDE input files and updates the pre-calculated analytics cache.
"""
from __future__ import annotations

import logging
from pathlib import Path
import sys
import time

# Ensure project root is in sys.path
PROJECT_DIR = Path(__file__).resolve().parents[3]
if str(PROJECT_DIR / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR / "src"))

from ta35_dashboard.config import PROJECT_ROOT
from ta35_dashboard.services.dde_service import _background_worker_loop

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger("dde_worker")


def main() -> None:
    logger.info("Starting Standalone DDE Background Worker for %s...", PROJECT_ROOT)
    _background_worker_loop(project_root=PROJECT_ROOT, poll_interval_sec=3.0)


if __name__ == "__main__":
    main()
