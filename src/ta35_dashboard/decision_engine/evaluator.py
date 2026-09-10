"""Recommendation Track Record & Historical Validation Engine.

Evaluates past recommendations produced by the Decision Engine across
4 forward horizons: 3, 7, 14, and 30 trading days.
Separates evaluation into 3 distinct axes:
1. Directional Prediction (Hit / Miss / Flat)
2. Volatility Prediction (Forecast vs Actual RV and VTA35)
3. Strategy & Spatial Accuracy (In Band, Target Range, Invalidation, Payoff)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
import logging
import math
from pathlib import Path
import sqlite3
from typing import Any, Sequence

logger = logging.getLogger(__name__)

HORIZONS = (3, 7, 14, 30)

# Deadbands for directional noise filtering by horizon (percentage)
DIRECTION_DEADBANDS = {
    3: 0.0040,   # ±0.40%
    7: 0.0070,   # ±0.70%
    14: 0.0100,  # ±1.00%
    30: 0.0150,  # ±1.50%
}


def init_evaluation_schema(conn_or_path: str | Path | sqlite3.Connection) -> None:
    """Creates the recommendation_evaluations table and associated indices."""
    is_conn = isinstance(conn_or_path, sqlite3.Connection)
    conn = conn_or_path if is_conn else sqlite3.connect(str(conn_or_path))
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS recommendation_evaluations (
                eval_id                 INTEGER PRIMARY KEY AUTOINCREMENT,
                rec_id                  INTEGER NOT NULL,
                as_of_date              TEXT NOT NULL,
                horizon_days            INTEGER NOT NULL,
                target_date             TEXT NOT NULL,
                actual_session_date     TEXT,
                status                  TEXT NOT NULL, -- 'PENDING' | 'RESOLVED' | 'NO_DATA'
                
                spot_t0                 REAL NOT NULL,
                spot_tk                 REAL,
                pct_change              REAL,
                max_high_during         REAL,
                min_low_during          REAL,
                
                direction_view          TEXT NOT NULL,
                direction_prob          REAL NOT NULL,
                direction_outcome       TEXT, -- 'HIT' | 'MISS' | 'FLAT'
                direction_score         REAL, -- +1.0, 0.0, -1.0
                
                volatility_view         TEXT NOT NULL,
                forecast_rv             REAL NOT NULL,
                actual_rv               REAL,
                vta35_t0                REAL,
                vta35_tk                REAL,
                volatility_outcome      TEXT, -- 'HIT' | 'MISS' | 'FLAT'
                
                primary_family          TEXT NOT NULL,
                in_probability_band     INTEGER, -- 1 or 0
                in_target_range         INTEGER, -- 1 or 0
                invalidation_breached   INTEGER, -- 1 or 0
                strategy_outcome        TEXT, -- 'MAX_PROFIT' | 'PARTIAL_PROFIT' | 'BREAKEVEN' | 'LOSS' | 'MAX_LOSS'
                
                resolved_at_utc         TEXT,
                notes                   TEXT,
                UNIQUE(as_of_date, horizon_days)
            )
            """
        )
        # Deduplicate if table previously existed with duplicate dates
        cursor.execute(
            """
            DELETE FROM recommendation_evaluations 
            WHERE eval_id NOT IN (
                SELECT MAX(eval_id) FROM recommendation_evaluations GROUP BY as_of_date, horizon_days
            )
            """
        )
        cursor.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS idx_eval_date_horizon ON recommendation_evaluations(as_of_date, horizon_days);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_eval_status ON recommendation_evaluations(status, as_of_date);"
        )
        cursor.execute(
            "CREATE INDEX IF NOT EXISTS idx_eval_horizon ON recommendation_evaluations(horizon_days, as_of_date);"
        )
        conn.commit()
    finally:
        if not is_conn:
            conn.close()


def _get_trading_sessions_after(
    conn: sqlite3.Connection,
    as_of_date: str,
    limit: int = 40,
) -> list[tuple[str, float, float, float]]:
    """Returns future TA-35 trading sessions (session_date, open, high, low, close)."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT session_date, high, low, close
        FROM eod_bars
        WHERE symbol = 'TA35' AND session_date > ?
        ORDER BY session_date ASC
        LIMIT ?
        """,
        (as_of_date, limit),
    )
    return cursor.fetchall()


def _get_spot_at_or_before(conn: sqlite3.Connection, date_str: str) -> float | None:
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT close FROM eod_bars
            WHERE symbol = 'TA35' AND session_date <= ?
            ORDER BY session_date DESC LIMIT 1
            """,
            (date_str,),
        )
        row = cursor.fetchone()
        return float(row[0]) if row else None
    except sqlite3.OperationalError:
        return None


def _get_vta35_at_or_before(conn: sqlite3.Connection, date_str: str) -> float | None:
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT close FROM eod_bars
            WHERE symbol = 'VTA35' AND session_date <= ?
            ORDER BY session_date DESC LIMIT 1
            """,
            (date_str,),
        )
        row = cursor.fetchone()
        return float(row[0]) if row else None
    except sqlite3.OperationalError:
        return None


def calculate_realized_volatility(closes: Sequence[float]) -> float:
    """Annualized Close-to-Close Realized Volatility assuming 250 trading days."""
    if len(closes) < 2:
        return 0.15
    log_returns = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    var = sum(r * r for r in log_returns) / len(log_returns)
    return math.sqrt(var * 250.0)


def evaluate_direction(
    direction_view: str,
    direction_prob: float,
    pct_change: float,
    horizon_days: int,
) -> tuple[str, float]:
    """Evaluates whether directional recommendation was HIT, MISS, or FLAT.
    
    If the prediction was Neutral/Rangebound and the market chopped within range,
    it is considered a successful prediction (HIT).
    """
    deadband = DIRECTION_DEADBANDS.get(horizon_days, 0.0070)
    view_lower = (direction_view or "").lower()

    if "שורי" in view_lower or "bull" in view_lower:
        stance = "BULLISH"
    elif "דובי" in view_lower or "bear" in view_lower:
        stance = "BEARISH"
    elif "נייטרלי" in view_lower or "neutral" in view_lower or "range" in view_lower or "דשדוש" in view_lower:
        stance = "NEUTRAL"
    else:
        if direction_prob >= 0.55:
            stance = "BULLISH"
        elif direction_prob <= 0.45:
            stance = "BEARISH"
        else:
            stance = "NEUTRAL"

    if stance == "BULLISH":
        if pct_change > deadband:
            return "HIT", 1.0
        elif pct_change < -deadband:
            return "MISS", -1.0
        else:
            return "FLAT", 0.0

    elif stance == "BEARISH":
        if pct_change < -deadband:
            return "HIT", 1.0
        elif pct_change > deadband:
            return "MISS", -1.0
        else:
            return "FLAT", 0.0

    else:  # NEUTRAL / RANGEBOUND
        # אם החיזוי היה נייטרלי והשוק דשדש - זו הצלחה מלאה (HIT)
        neutral_range_limit = 2.0 * deadband
        if abs(pct_change) <= neutral_range_limit:
            return "HIT", 1.0
        else:
            return "MISS", -1.0


def evaluate_volatility(
    volatility_view: str,
    forecast_rv: float,
    actual_rv: float,
    vta35_t0: float | None,
    vta35_tk: float | None,
) -> str:
    """Evaluates whether volatility expectation was HIT, MISS, or FLAT."""
    vol_view = (volatility_view or "").lower()
    delta_vta = (vta35_tk - vta35_t0) if (vta35_t0 is not None and vta35_tk is not None) else None

    expects_rise = ("עלי" in vol_view or "stress" in vol_view or "מתח" in vol_view or "גבוה" in vol_view)
    expects_fall = ("יריד" in vol_view or "רגיעה" in vol_view or "דעיכ" in vol_view or "רגוע" in vol_view)

    if expects_rise:
        if actual_rv >= forecast_rv * 1.04 or (delta_vta is not None and delta_vta > 0.4):
            return "HIT"
        elif actual_rv <= forecast_rv * 0.94 and (delta_vta is None or delta_vta < 0):
            return "MISS"
        return "FLAT"

    if expects_fall:
        if actual_rv <= forecast_rv * 0.98 or (delta_vta is not None and delta_vta < -0.3):
            return "HIT"
        elif actual_rv >= forecast_rv * 1.08 or (delta_vta is not None and delta_vta > 0.8):
            return "MISS"
        return "FLAT"

    # Steady / Neutral
    if abs(actual_rv - forecast_rv) / max(0.01, forecast_rv) <= 0.20:
        return "HIT"
    return "MISS"


def evaluate_strategy_and_range(
    primary_family: str,
    rec_dict: dict[str, Any],
    spot_t0: float,
    spot_tk: float,
    max_high: float,
    min_low: float,
) -> tuple[int, int, int, str]:
    """Returns (in_probability_band, in_target_range, invalidation_breached, strategy_outcome)."""
    # 1. Probability Band
    prob_band = rec_dict.get("probability_band")
    in_band = 1
    if isinstance(prob_band, (list, tuple)) and len(prob_band) == 2:
        low_b, high_b = float(prob_band[0]), float(prob_band[1])
        in_band = 1 if (low_b <= spot_tk <= high_b) else 0

    # 2. Target Range
    target_range = rec_dict.get("target_range")
    in_target = 0
    if isinstance(target_range, (list, tuple)) and len(target_range) == 2:
        low_t, high_t = float(target_range[0]), float(target_range[1])
        in_target = 1 if (low_t <= spot_tk <= high_t) else 0

    # 3. Invalidation level
    inv_level = rec_dict.get("invalidation_level")
    inv_breached = 0
    if inv_level is not None:
        try:
            inv_val = float(inv_level)
            direction = (rec_dict.get("direction_view") or "").lower()
            if "שורי" in direction or "bull" in direction:
                if min_low <= inv_val:
                    inv_breached = 1
            elif "דובי" in direction or "bear" in direction:
                if max_high >= inv_val:
                    inv_breached = 1
        except Exception:
            pass

    # 4. Strategy Outcome
    family_lower = (primary_family or "").lower()

    if "bull put" in family_lower or "bull call" in family_lower:
        if spot_tk >= spot_t0 * 1.008:
            outcome = "MAX_PROFIT"
        elif spot_tk >= spot_t0:
            outcome = "PARTIAL_PROFIT"
        elif inv_breached or spot_tk < spot_t0 * 0.985:
            outcome = "MAX_LOSS"
        else:
            outcome = "LOSS"

    elif "bear put" in family_lower or "bear call" in family_lower:
        if spot_tk <= spot_t0 * 0.992:
            outcome = "MAX_PROFIT"
        elif spot_tk <= spot_t0:
            outcome = "PARTIAL_PROFIT"
        elif inv_breached or spot_tk > spot_t0 * 1.015:
            outcome = "MAX_LOSS"
        else:
            outcome = "LOSS"

    elif "iron condor" in family_lower or "butterfly" in family_lower:
        if in_target:
            outcome = "MAX_PROFIT"
        elif in_band:
            outcome = "PARTIAL_PROFIT"
        elif inv_breached:
            outcome = "MAX_LOSS"
        else:
            outcome = "LOSS"

    else:
        if in_target:
            outcome = "MAX_PROFIT"
        elif in_band:
            outcome = "PARTIAL_PROFIT"
        elif inv_breached:
            outcome = "MAX_LOSS"
        else:
            outcome = "BREAKEVEN"

    return in_band, in_target, inv_breached, outcome


def enqueue_recommendation_evaluations(
    rec_id: int,
    as_of_date: str,
    direction_view: str,
    direction_prob: float,
    volatility_view: str,
    forecast_rv: float,
    primary_family: str,
    spot_t0: float,
    conn: sqlite3.Connection,
) -> None:
    """Inserts PENDING rows for 3, 7, 14, and 30-day evaluation horizons."""
    cursor = conn.cursor()
    vta35_t0 = _get_vta35_at_or_before(conn, as_of_date)

    for h in HORIZONS:
        cursor.execute(
            """
            INSERT OR IGNORE INTO recommendation_evaluations (
                rec_id, as_of_date, horizon_days, target_date, status,
                spot_t0, direction_view, direction_prob, volatility_view,
                forecast_rv, vta35_t0, primary_family
            ) VALUES (?, ?, ?, ?, 'PENDING', ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rec_id,
                as_of_date,
                h,
                f"T+{h}",
                spot_t0,
                direction_view,
                direction_prob,
                volatility_view,
                forecast_rv,
                vta35_t0,
                primary_family,
            ),
        )
    conn.commit()


def resolve_pending_evaluations(db_path: str | Path) -> int:
    """Scans and resolves any PENDING evaluations whose horizon has elapsed."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    resolved_count = 0

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT e.eval_id, e.rec_id, e.as_of_date, e.horizon_days, e.spot_t0,
                   e.direction_view, e.direction_prob, e.volatility_view, e.forecast_rv,
                   e.vta35_t0, e.primary_family, r.rec_json
            FROM recommendation_evaluations e
            JOIN shadow_eod_recommendations r ON e.rec_id = r.id
            WHERE e.status = 'PENDING'
            ORDER BY e.as_of_date ASC
            """
        )
        pending_rows = cursor.fetchall()

        now_utc = datetime.now(timezone.utc).isoformat()

        for row in pending_rows:
            (
                eval_id,
                rec_id,
                as_of_date,
                horizon_days,
                spot_t0,
                direction_view,
                direction_prob,
                volatility_view,
                forecast_rv,
                vta35_t0,
                primary_family,
                rec_json_str,
            ) = row

            future_bars = _get_trading_sessions_after(conn, as_of_date, limit=horizon_days)
            if len(future_bars) < horizon_days:
                # Not enough trading sessions have elapsed yet
                continue

            # The horizon has arrived
            target_bar = future_bars[horizon_days - 1]
            actual_session_date, _, _, spot_tk = target_bar
            spot_tk = float(spot_tk)

            # High/Low and closes across the horizon
            highs = [float(b[1]) for b in future_bars]
            lows = [float(b[2]) for b in future_bars]
            closes = [spot_t0] + [float(b[3]) for b in future_bars]

            max_high = max(highs)
            min_low = min(lows)
            pct_change = (spot_tk - spot_t0) / spot_t0
            actual_rv = calculate_realized_volatility(closes)

            vta35_tk = _get_vta35_at_or_before(conn, actual_session_date)

            rec_dict = {}
            try:
                rec_dict = json.loads(rec_json_str) if rec_json_str else {}
            except Exception:
                pass

            # 1. Evaluate Direction
            dir_outcome, dir_score = evaluate_direction(
                direction_view=direction_view,
                direction_prob=direction_prob,
                pct_change=pct_change,
                horizon_days=horizon_days,
            )

            # 2. Evaluate Volatility
            vol_outcome = evaluate_volatility(
                volatility_view=volatility_view,
                forecast_rv=forecast_rv,
                actual_rv=actual_rv,
                vta35_t0=vta35_t0,
                vta35_tk=vta35_tk,
            )

            # 3. Evaluate Strategy & Range
            in_band, in_target, inv_breached, strat_outcome = evaluate_strategy_and_range(
                primary_family=primary_family,
                rec_dict=rec_dict,
                spot_t0=spot_t0,
                spot_tk=spot_tk,
                max_high=max_high,
                min_low=min_low,
            )

            view_lower = (direction_view or "").lower()
            if "שורי" in view_lower or "bull" in view_lower:
                stance = "BULLISH"
            elif "דובי" in view_lower or "bear" in view_lower:
                stance = "BEARISH"
            elif "נייטרלי" in view_lower or "neutral" in view_lower or "range" in view_lower or "דשדוש" in view_lower:
                stance = "NEUTRAL"
            else:
                stance = "BULLISH" if direction_prob >= 0.55 else ("BEARISH" if direction_prob <= 0.45 else "NEUTRAL")

            if stance == "NEUTRAL":
                if dir_outcome == "HIT":
                    notes = (
                        f"תחזית ניטרלית: השוק דשדש בטווח מרוסן כמצופה מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) - פגיעה ביעד הדשדוש."
                    )
                else:
                    notes = (
                        f"תחזית ניטרלית: התרחשה פריצה חדה מעבר לטווח הדשדוש מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) - שגיאה."
                    )
            elif stance == "BULLISH":
                if dir_outcome == "HIT":
                    notes = f"תחזית שורית: המדד עלה מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) מעל סף הרעש - פגיעה בכיוון."
                elif dir_outcome == "MISS":
                    notes = f"תחזית שורית: המדד ירד מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) - שגיאה."
                else:
                    notes = f"תחזית שורית: תנועה זניחה מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) בתוך סף הרעש."
            else:  # BEARISH
                if dir_outcome == "HIT":
                    notes = f"תחזית דובית: המדד ירד מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) - פגיעה בכיוון."
                elif dir_outcome == "MISS":
                    notes = f"תחזית דובית: המדד עלה מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) - שגיאה."
                else:
                    notes = f"תחזית דובית: תנועה זניחה מ-{spot_t0:,.1f} ל-{spot_tk:,.1f} ({pct_change:+.2%}) בתוך סף הרעש."

            cursor.execute(
                """
                UPDATE recommendation_evaluations
                SET actual_session_date = ?,
                    status = 'RESOLVED',
                    spot_tk = ?,
                    pct_change = ?,
                    max_high_during = ?,
                    min_low_during = ?,
                    direction_outcome = ?,
                    direction_score = ?,
                    actual_rv = ?,
                    vta35_tk = ?,
                    volatility_outcome = ?,
                    in_probability_band = ?,
                    in_target_range = ?,
                    invalidation_breached = ?,
                    strategy_outcome = ?,
                    resolved_at_utc = ?,
                    notes = ?
                WHERE eval_id = ?
                """,
                (
                    actual_session_date,
                    spot_tk,
                    pct_change,
                    max_high,
                    min_low,
                    dir_outcome,
                    dir_score,
                    actual_rv,
                    vta35_tk,
                    vol_outcome,
                    in_band,
                    in_target,
                    inv_breached,
                    strat_outcome,
                    now_utc,
                    notes,
                    eval_id,
                ),
            )
            resolved_count += 1

        conn.commit()
    finally:
        conn.close()

    return resolved_count


def backfill_all_history(db_path: str | Path) -> tuple[int, int]:
    """Backfills all existing records in shadow_eod_recommendations into evaluations."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    enqueued_count = 0

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT id, as_of_date, direction_view, direction_prob,
                   primary_family, forecast_rv, rec_json
            FROM shadow_eod_recommendations
            WHERE id IN (
                SELECT MAX(id) FROM shadow_eod_recommendations GROUP BY as_of_date
            )
            ORDER BY as_of_date ASC
            """
        )
        recs = cursor.fetchall()

        for rec in recs:
            rec_id, as_of_date, dir_view, dir_prob, primary_family, forecast_rv, rec_json = rec
            spot_t0 = _get_spot_at_or_before(conn, as_of_date)
            if spot_t0 is None:
                continue

            # Extract volatility view from rec_json
            vol_view = "רגוע"
            try:
                d = json.loads(rec_json)
                vol_view = d.get("volatility_view", vol_view)
            except Exception:
                pass

            enqueue_recommendation_evaluations(
                rec_id=rec_id,
                as_of_date=as_of_date,
                direction_view=dir_view,
                direction_prob=float(dir_prob),
                volatility_view=vol_view,
                forecast_rv=float(forecast_rv),
                primary_family=primary_family,
                spot_t0=float(spot_t0),
                conn=conn,
            )
            enqueued_count += 1

        conn.commit()
    finally:
        conn.close()

    resolved_count = resolve_pending_evaluations(db_path)
    return enqueued_count, resolved_count


# ---------------------------------------------------------------------------
# Aggregation Functions for Analytics & UI
# ---------------------------------------------------------------------------

def get_direction_performance(db_path: str | Path) -> dict[int, dict[str, Any]]:
    """Calculates Directional Hit-Rate and distribution per horizon."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    stats = {}

    try:
        cursor = conn.cursor()
        for h in HORIZONS:
            cursor.execute(
                """
                SELECT direction_outcome, COUNT(*)
                FROM recommendation_evaluations
                WHERE horizon_days = ? AND status = 'RESOLVED'
                GROUP BY direction_outcome
                """,
                (h,),
            )
            counts = dict(cursor.fetchall())
            hits = counts.get("HIT", 0)
            misses = counts.get("MISS", 0)
            flats = counts.get("FLAT", 0)
            total_decisive = hits + misses
            total = hits + misses + flats

            hit_rate = (hits / total_decisive * 100.0) if total_decisive > 0 else 0.0

            # Bullish vs Bearish breakdown
            cursor.execute(
                """
                SELECT 
                    CASE 
                        WHEN direction_view LIKE '%שורי%' OR direction_view LIKE '%bull%' THEN 'שורי (Bullish)'
                        WHEN direction_view LIKE '%דובי%' OR direction_view LIKE '%bear%' THEN 'דובי (Bearish)'
                        ELSE 'נייטרלי (Neutral)'
                    END as stance,
                    direction_outcome,
                    COUNT(*)
                FROM recommendation_evaluations
                WHERE horizon_days = ? AND status = 'RESOLVED'
                GROUP BY stance, direction_outcome
                """,
                (h,),
            )
            stance_rows = cursor.fetchall()
            stance_breakdown = {}
            for stance, outcome, cnt in stance_rows:
                stance_breakdown.setdefault(stance, {})[outcome] = cnt

            stats[h] = {
                "hits": hits,
                "misses": misses,
                "flats": flats,
                "total": total,
                "hit_rate": hit_rate,
                "stance_breakdown": stance_breakdown,
            }
    finally:
        conn.close()

    return stats


def get_volatility_performance(db_path: str | Path) -> dict[int, dict[str, Any]]:
    """Calculates Volatility Hit-Rate, Mean Absolute Error (MAE) per horizon."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    stats = {}

    try:
        cursor = conn.cursor()
        for h in HORIZONS:
            cursor.execute(
                """
                SELECT volatility_outcome, COUNT(*)
                FROM recommendation_evaluations
                WHERE horizon_days = ? AND status = 'RESOLVED'
                GROUP BY volatility_outcome
                """,
                (h,),
            )
            counts = dict(cursor.fetchall())
            hits = counts.get("HIT", 0)
            misses = counts.get("MISS", 0)
            flats = counts.get("FLAT", 0)
            total = hits + misses + flats
            hit_rate = (hits / max(1, hits + misses) * 100.0) if (hits + misses) > 0 else 0.0

            cursor.execute(
                """
                SELECT AVG(ABS(actual_rv - forecast_rv)), AVG(forecast_rv), AVG(actual_rv)
                FROM recommendation_evaluations
                WHERE horizon_days = ? AND status = 'RESOLVED' AND actual_rv IS NOT NULL
                """,
                (h,),
            )
            mae_row = cursor.fetchone()
            mae = (mae_row[0] * 100.0) if (mae_row and mae_row[0] is not None) else 0.0
            avg_forecast = (mae_row[1] * 100.0) if (mae_row and mae_row[1] is not None) else 0.0
            avg_actual = (mae_row[2] * 100.0) if (mae_row and mae_row[2] is not None) else 0.0

            stats[h] = {
                "hits": hits,
                "misses": misses,
                "flats": flats,
                "total": total,
                "hit_rate": hit_rate,
                "mae_rv_pct": mae,
                "avg_forecast_rv": avg_forecast,
                "avg_actual_rv": avg_actual,
            }
    finally:
        conn.close()

    return stats


def get_strategy_performance(db_path: str | Path) -> dict[str, Any]:
    """Calculates Spatial and Strategy outcome statistics."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    stats = {}

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total,
                SUM(in_probability_band) as in_band,
                SUM(in_target_range) as in_target,
                SUM(invalidation_breached) as inv_breached
            FROM recommendation_evaluations
            WHERE status = 'RESOLVED'
            """
        )
        row = cursor.fetchone()
        tot = row[0] or 0
        in_band = row[1] or 0
        in_target = row[2] or 0
        inv_breached = row[3] or 0

        stats["spatial"] = {
            "total": tot,
            "in_band_pct": (in_band / tot * 100.0) if tot > 0 else 0.0,
            "in_target_pct": (in_target / tot * 100.0) if tot > 0 else 0.0,
            "invalidation_pct": (inv_breached / tot * 100.0) if tot > 0 else 0.0,
        }

        cursor.execute(
            """
            SELECT primary_family, strategy_outcome, COUNT(*)
            FROM recommendation_evaluations
            WHERE status = 'RESOLVED'
            GROUP BY primary_family, strategy_outcome
            """
        )
        family_outcomes = {}
        for fam, outcome, cnt in cursor.fetchall():
            family_outcomes.setdefault(fam, {})[outcome] = cnt
        stats["family_outcomes"] = family_outcomes

    finally:
        conn.close()

    return stats


def fetch_evaluation_records(
    db_path: str | Path,
    horizon_days: int | None = None,
    limit: int = 150,
) -> list[dict[str, Any]]:
    """Fetches resolved and pending evaluation rows for UI tabular display."""
    init_evaluation_schema(db_path)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.cursor()
        if horizon_days is not None:
            cursor.execute(
                """
                SELECT * FROM recommendation_evaluations
                WHERE horizon_days = ?
                ORDER BY as_of_date DESC, eval_id DESC
                LIMIT ?
                """,
                (horizon_days, limit),
            )
        else:
            cursor.execute(
                """
                SELECT * FROM recommendation_evaluations
                ORDER BY as_of_date DESC, horizon_days ASC
                LIMIT ?
                """,
                (limit,),
            )
        rows = [dict(r) for r in cursor.fetchall()]
        return rows
    finally:
        conn.close()
