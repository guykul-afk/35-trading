"""Loader script for TASE official trading calendar and contract expiry metadata."""

from __future__ import annotations

from datetime import date, timedelta
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "ta35_dashboard.db"


def seed_trading_calendar(db_path: Path = DB_PATH) -> None:
    """Generate and insert TASE trading calendar for current and upcoming years."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    
    # Run migrations first
    migrations_dir = PROJECT_ROOT / "migrations"
    for sql_file in sorted(migrations_dir.glob("*.sql")):
        conn.executescript(sql_file.read_text(encoding="utf-8"))

    start_date = date(2025, 1, 1)
    end_date = date(2027, 12, 31)

    curr = start_date
    trading_day_idx = 1
    records = []

    while curr <= end_date:
        # TASE trades Sunday (weekday 6) to Thursday (weekday 3)
        # Friday (4) and Saturday (5) are closed
        weekday = curr.weekday()
        
        if weekday in (4, 5):
            is_trading = 0
            session_type = "closed"
            eq_open = eq_close = maof_open = maof_close = None
            prior_us = 0
            gap_days = 1.0
        else:
            is_trading = 1
            if weekday == 6:  # Sunday
                session_type = "sunday_short"
                eq_open, eq_close = "10:00", "15:50"
                maof_open, maof_close = "09:45", "16:00"
                prior_us = 2  # Friday and Saturday US gap
                gap_days = 3.0
            else:  # Monday - Thursday
                session_type = "full"
                eq_open, eq_close = "10:00", "17:20"
                maof_open, maof_close = "09:45", "17:30"
                prior_us = 1
                gap_days = 1.0

        records.append(
            (
                curr.isoformat(),
                "TASE",
                is_trading,
                session_type,
                eq_open,
                eq_close,
                maof_open,
                maof_close,
                "17:24" if session_type == "full" else "15:54",
                trading_day_idx if is_trading else None,
                prior_us,
                gap_days,
                "TASE_OFFICIAL_CALENDAR",
                "Seeded TASE trading session",
            )
        )
        if is_trading:
            trading_day_idx += 1
        curr += timedelta(days=1)

    conn.executemany(
        """INSERT OR REPLACE INTO trading_session
           (session_date, venue, is_trading, session_type, equity_open_local, equity_close_local,
            maof_open_local, maof_close_local, closing_auction_local, trading_day_index,
            prior_us_sessions, calendar_gap_days, source, note)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        records,
    )
    conn.commit()
    conn.close()
    print(f"Successfully loaded {len(records)} trading sessions into {db_path}")


if __name__ == "__main__":
    seed_trading_calendar()
