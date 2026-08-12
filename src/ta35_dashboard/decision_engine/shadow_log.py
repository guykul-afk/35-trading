"""Layer 9: Shadow Log & Track Record Service.

Persists every TradeTicket and StrategyRecommendation output to SQLite
for out-of-sample forward evaluation and auditability.
"""

from __future__ import annotations

from dataclasses import asdict
import json
import logging
from pathlib import Path
import sqlite3
from typing import Any

from ta35_dashboard.decision_engine.models import StrategyRecommendation, TradeTicket

logger = logging.getLogger(__name__)


def init_shadow_log_db(db_path: str | Path) -> None:
    """Ensures shadow log tables exist in SQLite."""
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shadow_trade_tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                snapshot_id TEXT NOT NULL,
                verdict TEXT NOT NULL,
                opportunity_score REAL NOT NULL,
                strategy_family TEXT NOT NULL,
                strategy_variant TEXT NOT NULL,
                limit_price REAL NOT NULL,
                net_debit_credit REAL NOT NULL,
                max_profit REAL NOT NULL,
                max_loss REAL NOT NULL,
                model_ev REAL NOT NULL,
                market_ev REAL NOT NULL,
                estimated_edge REAL NOT NULL,
                size_contracts INTEGER NOT NULL,
                ticket_json TEXT NOT NULL
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS shadow_eod_recommendations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                as_of_date TEXT NOT NULL,
                snapshot_id TEXT NOT NULL,
                verdict TEXT NOT NULL,
                primary_family TEXT NOT NULL,
                direction_view TEXT NOT NULL,
                direction_prob REAL NOT NULL,
                forecast_rv REAL NOT NULL,
                rec_json TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()


def log_trade_ticket(ticket: TradeTicket, db_path: str | Path) -> None:
    """Logs a TradeTicket recommendation to SQLite."""
    init_shadow_log_db(db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO shadow_trade_tickets (
                timestamp, snapshot_id, verdict, opportunity_score,
                strategy_family, strategy_variant, limit_price, net_debit_credit,
                max_profit, max_loss, model_ev, market_ev, estimated_edge,
                size_contracts, ticket_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                ticket.timestamp,
                ticket.snapshot_id,
                ticket.verdict.value,
                ticket.opportunity_score,
                ticket.strategy_family.value,
                ticket.strategy_variant,
                ticket.limit_price,
                ticket.net_debit_credit,
                ticket.max_profit,
                ticket.max_loss,
                ticket.model_ev_after_costs,
                ticket.market_ev_after_costs,
                ticket.estimated_edge,
                ticket.size_contracts,
                json.dumps(asdict(ticket), default=str),
            ),
        )
        conn.commit()
    except Exception as e:
        logger.error("Failed writing shadow TradeTicket to log: %s", e)
    finally:
        conn.close()


def log_eod_recommendation(rec: StrategyRecommendation, db_path: str | Path) -> None:
    """Logs a StrategyRecommendation (EOD Mode) to SQLite."""
    init_shadow_log_db(db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO shadow_eod_recommendations (
                as_of_date, snapshot_id, verdict, primary_family,
                direction_view, direction_prob, forecast_rv, rec_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rec.as_of_date,
                rec.snapshot_id,
                rec.verdict.value,
                rec.primary_strategy_family.value,
                rec.direction_view,
                rec.direction_probability,
                rec.forecast_rv,
                json.dumps(asdict(rec), default=str),
            ),
        )
        conn.commit()
    except Exception as e:
        logger.error("Failed writing shadow EOD recommendation to log: %s", e)
    finally:
        conn.close()
