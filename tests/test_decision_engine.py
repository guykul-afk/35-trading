"""Unit tests for TA-35 Trade Decision Engine (100% EOD Architecture)."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ta35_dashboard.decision_engine import (
    EngineMode,
    StrategyFamily,
    StrategyRecommendation,
    Verdict,
)
from ta35_dashboard.decision_engine.engine import run_trade_decision_engine
from ta35_dashboard.decision_engine.generators import (
    compute_eod_statistical_legs,
    map_eod_strategy_families,
)
from ta35_dashboard.decision_engine.router import determine_engine_mode


class DecisionEngineEODTests(unittest.TestCase):
    def test_eod_bullish_recommendation(self):
        """Verify that a bullish market state generates an appropriate Bullish strategy recommendation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_db.sqlite3"
            result = run_trade_decision_engine(
                spot_price=4150.0,
                prob_up=0.60,
                forecast_rv=0.15,
                current_rv=0.14,
                regime="NORMAL",
                volatility_state="מתכווצת",
                market_state="עולה",
                horizon_days=7,
                db_path=db_path,
            )

            self.assertIsInstance(result, StrategyRecommendation)
            self.assertEqual(result.mode, EngineMode.EOD_GENERAL)
            self.assertEqual(result.verdict, Verdict.GENERAL_STRATEGY)
            self.assertIn(result.primary_strategy_family, (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.BULL_CALL_DEBIT))
            self.assertGreater(len(result.estimated_legs), 0)
            self.assertGreater(result.target_range[1], result.target_range[0])
            self.assertLess(result.invalidation_level, 4150.0)

    def test_eod_bearish_recommendation(self):
        """Verify that a bearish market state generates an appropriate Bearish strategy recommendation."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_db.sqlite3"
            result = run_trade_decision_engine(
                spot_price=4150.0,
                prob_up=0.40,
                forecast_rv=0.18,
                current_rv=0.16,
                regime="NORMAL",
                volatility_state="מתכווצת",
                market_state="יורד",
                horizon_days=7,
                db_path=db_path,
            )

            self.assertIsInstance(result, StrategyRecommendation)
            self.assertIn(result.primary_strategy_family, (StrategyFamily.BEAR_CALL_CREDIT, StrategyFamily.BEAR_PUT_DEBIT))
            self.assertGreater(result.invalidation_level, 4150.0)

    def test_eod_neutral_expanding_vol_recommendation(self):
        """Verify that neutral direction with expanding volatility recommends Long Straddle."""
        primary, alts, dir_view, vol_view = map_eod_strategy_families(
            prob_up=0.50,
            forecast_rv=0.20,
            current_rv=0.15,
            regime="NORMAL",
            volatility_state="מתרחבת",
            market_state="ניטרלי",
        )
        self.assertEqual(primary, StrategyFamily.LONG_STRADDLE)
        self.assertIn("מתרחבת", vol_view)

    def test_eod_statistical_legs_computation(self):
        """Verify that compute_eod_statistical_legs produces valid strikes and sigma offsets."""
        legs = compute_eod_statistical_legs(
            spot_price=4150.0,
            forecast_rv=0.15,
            horizon_days=7,
            family=StrategyFamily.BULL_CALL_DEBIT,
        )
        self.assertEqual(len(legs), 2)
        self.assertEqual(legs[0]["option_type"], "CALL")
        self.assertEqual(legs[0]["action"], "BUY")
        self.assertEqual(legs[1]["action"], "SELL")
        self.assertGreater(legs[1]["estimated_strike"], legs[0]["estimated_strike"])

    def test_eod_router_validation(self):
        """Verify determine_engine_mode checks required EOD inputs."""
        # 1. Valid inputs
        mode, warnings = determine_engine_mode(spot_price=4150.0, prob_up=0.55, forecast_rv=0.15)
        self.assertEqual(mode, EngineMode.EOD_GENERAL)
        self.assertEqual(len(warnings), 0)

        # 2. Missing spot
        mode_bad, warnings_bad = determine_engine_mode(spot_price=0.0, prob_up=0.55, forecast_rv=0.15)
        self.assertEqual(mode_bad, EngineMode.RESEARCH_ONLY)
        self.assertGreater(len(warnings_bad), 0)


if __name__ == "__main__":
    unittest.main()
