import unittest

from ta35_dashboard.analytics import recommend_strategy


class StrategyRecommendationTests(unittest.TestCase):
    def recommend(self, **overrides):
        inputs = {
            "spot": 4_000.0,
            "forecast_volatility": 0.18,
            "implied_volatility": 0.19,
            "trend_score": 0.6,
            "volatility_score": -1.0,
            "regime": "רגיל",
            "horizon_days": 14,
        }
        inputs.update(overrides)
        return recommend_strategy(**inputs)

    def test_positive_contraction_selects_bullish_butterfly_and_ranges(self):
        result = self.recommend()
        self.assertEqual(result.status, "מועמד כללי")
        self.assertIn("פרפר", result.primary.name)
        self.assertEqual(result.market_view, "חיובי")
        self.assertEqual(result.volatility_view, "מתכווצת")
        self.assertEqual(result.focus_range[0], 4_000.0)
        self.assertGreater(result.target_level, 4_000.0)
        self.assertGreater(result.base_range[1], result.core_range[1])

    def test_strong_breakout_selects_ratio_backspread(self):
        result = self.recommend(trend_score=1.0, volatility_score=1.0)
        self.assertIn("Ratio Backspread", result.primary.name)
        self.assertIn("+1σ", result.focus_label)

    def test_rich_neutral_contraction_selects_iron_condor(self):
        result = self.recommend(
            trend_score=0.0,
            volatility_score=-0.8,
            implied_volatility=0.23,
            premium_sale_eligible=True,
        )
        self.assertEqual(result.primary.name, "Iron Condor")
        self.assertEqual(result.focus_range, result.base_range)

    def test_rich_premium_is_blocked_without_evidence_gate(self):
        result = self.recommend(
            trend_score=0.0,
            volatility_score=-0.8,
            implied_volatility=0.23,
        )
        self.assertFalse(result.premium_sale_eligible)
        self.assertNotIn(
            result.primary.name if result.primary else None,
            {"Iron Condor", "Iron Butterfly", "Bull Put Spread", "Bear Call Spread"},
        )
        self.assertTrue(any("חסומה" in warning for warning in result.warnings))

    def test_scenario_fit_is_not_a_payoff(self):
        result = self.recommend()
        self.assertTrue(result.scenario_fit)
        self.assertTrue(all(len(row) == 3 for row in result.scenario_fit))

    def test_negative_contraction_selects_bearish_butterfly(self):
        result = self.recommend(trend_score=-0.6)
        self.assertIn("פרפר", result.primary.name)
        self.assertEqual(result.market_view, "שלילי")
        self.assertLess(result.target_level, 4_000.0)

    def test_stress_regime_avoids_short_premium_preference(self):
        result = self.recommend(
            trend_score=0.0,
            volatility_score=-0.8,
            implied_volatility=0.25,
            regime="לחץ גבוה",
            premium_sale_eligible=True,
        )
        self.assertNotIn(result.primary.name, {"Iron Condor", "Iron Butterfly"})

    def test_mixed_state_can_return_no_preferred_trade(self):
        result = self.recommend(
            trend_score=0.2,
            volatility_score=0.0,
        )
        self.assertEqual(result.status, "אין עסקה מועדפת")
        self.assertIsNone(result.primary)

    def test_missing_inputs_return_no_recommendation(self):
        result = self.recommend(spot=None, forecast_volatility=None)
        self.assertEqual(result.status, "אין המלצה")
        self.assertIsNone(result.primary)
        self.assertTrue(result.warnings)

    def test_invalid_horizon_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "horizon_days"):
            self.recommend(horizon_days=10)

    def test_seven_day_horizon_is_supported(self):
        self.assertEqual(self.recommend(horizon_days=7).horizon_days, 7)


if __name__ == "__main__":
    unittest.main()
