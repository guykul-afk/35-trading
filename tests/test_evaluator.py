"""Unit tests for RecommendationEvaluator."""

from pathlib import Path
import sqlite3
import pytest

from ta35_dashboard.decision_engine.evaluator import (
    DIRECTION_DEADBANDS,
    calculate_realized_volatility,
    enqueue_recommendation_evaluations,
    evaluate_direction,
    evaluate_strategy_and_range,
    evaluate_volatility,
    init_evaluation_schema,
    resolve_pending_evaluations,
)


def test_evaluate_direction_bullish():
    # Horizon 7 deadband is 0.70%
    deadband = DIRECTION_DEADBANDS[7]
    
    # Positive move above deadband -> HIT
    outcome, score = evaluate_direction("שורי (Bullish)", 0.70, deadband + 0.005, 7)
    assert outcome == "HIT"
    assert score == 1.0

    # Negative move below -deadband -> MISS
    outcome, score = evaluate_direction("שורי (Bullish)", 0.70, -(deadband + 0.005), 7)
    assert outcome == "MISS"
    assert score == -1.0

    # Small movement inside deadband -> FLAT
    outcome, score = evaluate_direction("שורי (Bullish)", 0.70, 0.001, 7)
    assert outcome == "FLAT"
    assert score == 0.0


def test_evaluate_direction_bearish():
    deadband = DIRECTION_DEADBANDS[3]
    # Downward move -> HIT
    outcome, score = evaluate_direction("דובי (Bearish)", 0.30, -0.01, 3)
    assert outcome == "HIT"
    assert score == 1.0

    # Upward move -> MISS
    outcome, score = evaluate_direction("דובי (Bearish)", 0.30, 0.01, 3)
    assert outcome == "MISS"
    assert score == -1.0


def test_evaluate_direction_neutral():
    deadband = DIRECTION_DEADBANDS[14]
    # Tight range movement -> HIT
    outcome, score = evaluate_direction("נייטרלי (Neutral)", 0.50, 0.002, 14)
    assert outcome == "HIT"
    assert score == 1.0

    # Large breakout -> MISS
    outcome, score = evaluate_direction("נייטרלי (Neutral)", 0.50, 0.03, 14)
    assert outcome == "MISS"
    assert score == -1.0


def test_evaluate_volatility():
    # Expect rise
    out = evaluate_volatility("ציפייה לעליית תנודתיות", 0.15, 0.20, 14.0, 16.5)
    assert out == "HIT"

    out_miss = evaluate_volatility("ציפייה לעליית תנודתיות", 0.15, 0.10, 14.0, 13.0)
    assert out_miss == "MISS"

    # Expect fall
    out_calm = evaluate_volatility("ציפייה לירידת תנודתיות", 0.20, 0.14, 18.0, 15.0)
    assert out_calm == "HIT"


def test_evaluate_strategy_and_range():
    rec_dict = {
        "probability_band": [4000.0, 4200.0],
        "target_range": [4120.0, 4180.0],
        "invalidation_level": 3950.0,
        "direction_view": "שורי",
    }
    
    # Spot inside target range and probability band, invalidation not breached
    in_band, in_target, inv_breached, outcome = evaluate_strategy_and_range(
        primary_family="Bull Put Spread",
        rec_dict=rec_dict,
        spot_t0=4100.0,
        spot_tk=4150.0,
        max_high=4160.0,
        min_low=4080.0,
    )
    assert in_band == 1
    assert in_target == 1
    assert inv_breached == 0
    assert outcome == "MAX_PROFIT"

    # Invalidation breached
    in_band2, in_target2, inv_breached2, outcome2 = evaluate_strategy_and_range(
        primary_family="Bull Put Spread",
        rec_dict=rec_dict,
        spot_t0=4100.0,
        spot_tk=3900.0,
        max_high=4105.0,
        min_low=3920.0,  # Below invalidation 3950
    )
    assert in_band2 == 0
    assert in_target2 == 0
    assert inv_breached2 == 1
    assert outcome2 == "MAX_LOSS"


def test_evaluator_db_workflow(tmp_path: Path):
    db_path = tmp_path / "test_eval.db"
    conn = sqlite3.connect(str(db_path))
    
    # Set up minimal schema
    init_evaluation_schema(conn)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE shadow_eod_recommendations (
            id INTEGER PRIMARY KEY,
            as_of_date TEXT,
            rec_json TEXT
        )
        """
    )
    cursor.execute(
        """
        CREATE TABLE eod_bars (
            symbol TEXT,
            session_date TEXT,
            high REAL,
            low REAL,
            close REAL
        )
        """
    )

    # Insert fake shadow recommendation
    cursor.execute(
        """
        INSERT INTO shadow_eod_recommendations (id, as_of_date, rec_json)
        VALUES (1, '2026-01-01', '{"probability_band": [100, 120], "target_range": [105, 115]}')
        """
    )

    # Insert baseline bar and 5 future bars
    bars = [
        ('TA35', '2026-01-01', 101, 99, 100),
        ('TA35', '2026-01-02', 103, 100, 102),
        ('TA35', '2026-01-03', 105, 101, 104),
        ('TA35', '2026-01-04', 108, 103, 107), # Day 3 (T+3)
        ('TA35', '2026-01-05', 110, 106, 109),
    ]
    cursor.executemany("INSERT INTO eod_bars VALUES (?, ?, ?, ?, ?)", bars)
    conn.commit()

    # Enqueue recommendation
    enqueue_recommendation_evaluations(
        rec_id=1,
        as_of_date='2026-01-01',
        direction_view="שורי",
        direction_prob=0.75,
        volatility_view="רגוע",
        forecast_rv=0.15,
        primary_family="Bull Put Spread",
        spot_t0=100.0,
        conn=conn,
    )
    conn.close()

    # Resolve pending evaluations
    resolved = resolve_pending_evaluations(db_path)
    # T+3 has 3 sessions, so T+3 must be resolved! T+7, T+14, T+30 remain PENDING.
    assert resolved == 1

    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    cursor.execute("SELECT horizon_days, status, spot_tk, direction_outcome FROM recommendation_evaluations")
    rows = cursor.fetchall()
    conn.close()

    t3_row = [r for r in rows if r[0] == 3][0]
    assert t3_row[1] == "RESOLVED"
    assert t3_row[2] == 107.0
    assert t3_row[3] == "HIT"


def test_evaluator_deduplicates_same_day(tmp_path: Path):
    db_path = tmp_path / "test_dedup.db"
    conn = sqlite3.connect(str(db_path))
    init_evaluation_schema(conn)

    # Enqueue multiple times for the exact same as_of_date
    for fake_rec_id in (1, 2, 3):
        enqueue_recommendation_evaluations(
            rec_id=fake_rec_id,
            as_of_date='2026-08-20',
            direction_view="שורי",
            direction_prob=0.60,
            volatility_view="רגוע",
            forecast_rv=0.14,
            primary_family="Bull Put Spread",
            spot_t0=4150.0,
            conn=conn,
        )

    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM recommendation_evaluations WHERE as_of_date = '2026-08-20'")
    count = cursor.fetchone()[0]
    conn.close()

    # There should be exactly 4 rows (1 for each horizon: 3, 7, 14, 30), NOT 12!
    assert count == 4
