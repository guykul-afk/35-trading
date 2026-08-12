import unittest

from ta35_dashboard.analytics import recommend_strategy
from ta35_dashboard.analytics.payoff import generate_strategy_payoff_data
from ta35_dashboard.analytics.strategies import calculate_strategy_strikes


class StrikeSelectionTests(unittest.TestCase):
    def test_calculate_strategy_strikes_bull_put(self):
        strikes = calculate_strategy_strikes(
            spot=2000.0,
            forecast_volatility=0.15,
            horizon_days=14,
            strategy_name="Bull Put Spread",
            regime="רגיל",
            step=10,
        )
        self.assertIn("balanced", strikes)
        self.assertIn("conservative", strikes)
        self.assertIn("aggressive", strikes)

        legs = strikes["balanced"]["legs"]
        self.assertEqual(len(legs), 2)
        
        buy_put = next(l for l in legs if l["action"] == "Buy")
        sell_put = next(l for l in legs if l["action"] == "Sell")

        # Check rounding to 10 points
        self.assertEqual(buy_put["strike"] % 10, 0)
        self.assertEqual(sell_put["strike"] % 10, 0)

        # Long put should be further OTM (lower strike) than short put
        self.assertLess(buy_put["strike"], sell_put["strike"])

    def test_calculate_strategy_strikes_butterfly(self):
        strikes = calculate_strategy_strikes(
            spot=4150.0,
            forecast_volatility=0.15,
            horizon_days=14,
            strategy_name="פרפר Call שורי / Broken-Wing Butterfly",
            regime="רגיל",
            step=10,
        )
        legs = strikes["aggressive"]["legs"]
        self.assertEqual(len(legs), 3)

        # 1x Buy Call lower, 2x Sell Call middle, 1x Buy Call upper
        sell_leg = next(l for l in legs if l["action"] == "Sell")
        self.assertEqual(sell_leg["quantity"], 2)
        self.assertEqual(sell_leg["option_type"], "Call")

        buy_legs = [l for l in legs if l["action"] == "Buy"]
        self.assertEqual(len(buy_legs), 2)
        self.assertLess(buy_legs[0]["strike"], sell_leg["strike"])
        self.assertGreater(buy_legs[1]["strike"], sell_leg["strike"])

        # Test Payoff generation produces a peak (tent shape)
        payoff_data = generate_strategy_payoff_data(
            spot=4150.0,
            forecast_volatility=0.15,
            horizon_days=14,
            legs=legs,
        )
        payoff = payoff_data["payoff"]
        max_idx = payoff.index(max(payoff))
        # Max payoff must occur near the middle short strike
        self.assertGreater(payoff[max_idx], 0)
        self.assertLess(payoff[0], payoff[max_idx])
        self.assertLess(payoff[-1], payoff[max_idx])

    def test_strike_selection_stress_regime_buffer(self):
        normal_strikes = calculate_strategy_strikes(
            spot=2000.0,
            forecast_volatility=0.20,
            horizon_days=14,
            strategy_name="Bull Put Spread",
            regime="רגיל",
        )
        stress_strikes = calculate_strategy_strikes(
            spot=2000.0,
            forecast_volatility=0.20,
            horizon_days=14,
            strategy_name="Bull Put Spread",
            regime="לחץ גבוה",
        )

        normal_short_put = next(l["strike"] for l in normal_strikes["balanced"]["legs"] if l["action"] == "Sell")
        stress_short_put = next(l["strike"] for l in stress_strikes["balanced"]["legs"] if l["action"] == "Sell")

        # Under stress, short put is pushed further OTM (lower strike)
        self.assertLessEqual(stress_short_put, normal_short_put)

    def test_recommendation_includes_suggested_strikes(self):
        rec = recommend_strategy(
            spot=2000.0,
            forecast_volatility=0.15,
            implied_volatility=0.22,
            trend_score=0.0,
            volatility_score=-0.8,
            regime="רגיל",
            horizon_days=14,
            premium_sale_eligible=True,
        )
        self.assertTrue(hasattr(rec, "suggested_strikes"))
        self.assertIn("balanced", rec.suggested_strikes)
        self.assertEqual(rec.primary.name, "Iron Condor")
        self.assertTrue(rec.suggested_strikes["balanced"]["legs"])

    def test_payoff_data_generation(self):
        legs = [
            {"action": "Buy", "option_type": "Put", "strike": 1900, "quantity": 1},
            {"action": "Sell", "option_type": "Put", "strike": 1950, "quantity": 1},
            {"action": "Sell", "option_type": "Call", "strike": 2050, "quantity": 1},
            {"action": "Buy", "option_type": "Call", "strike": 2100, "quantity": 1},
        ]
        payoff_data = generate_strategy_payoff_data(
            spot=2000.0,
            forecast_volatility=0.15,
            horizon_days=14,
            legs=legs,
        )
        self.assertIn("index_levels", payoff_data)
        self.assertIn("payoff", payoff_data)
        self.assertIn("pdf_scaled", payoff_data)
        self.assertEqual(len(payoff_data["index_levels"]), 150)
        self.assertEqual(len(payoff_data["payoff"]), 150)


if __name__ == "__main__":
    unittest.main()
