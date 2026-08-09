import math
import unittest

from ta35_dashboard.analytics import (
    ewma_volatility_forecast,
    expected_move,
    gap_variance_share,
    parkinson_volatility,
    percentile_rank,
    probability_band,
    realized_volatility,
    volatility_ratio,
    volatility_spread,
    yang_zhang_volatility,
    zscore,
)


class LiteAnalyticsTests(unittest.TestCase):
    def test_close_to_close_and_expected_move_use_252_sessions(self):
        prices = [
            100,
            100 * math.exp(0.01),
            100 * math.exp(-0.01),
            100 * math.exp(0.02),
        ]
        self.assertAlmostEqual(
            realized_volatility(prices).value, 0.025166114784235832 * math.sqrt(252)
        )
        self.assertAlmostEqual(
            expected_move(2500, 0.16, 3).value, 2500 * 0.16 * math.sqrt(3 / 252)
        )
        lower, upper = probability_band(2500, 0.16, 3, 1.5)
        width = 1.5 * 2500 * 0.16 * math.sqrt(3 / 252)
        self.assertAlmostEqual(lower, 2500 - width)
        self.assertAlmostEqual(upper, 2500 + width)
        half_lower, half_upper = probability_band(2500, 0.16, 3, 0.5)
        self.assertAlmostEqual(half_lower, 2500 - width / 3)
        self.assertAlmostEqual(half_upper, 2500 + width / 3)

    def test_ohlc_estimators_and_gap_share(self):
        opens = [100, 102, 101, 104]
        closes = [101, 101, 103, 105]
        highs = [102, 103, 104, 106]
        lows = [99, 100, 100, 103]
        self.assertGreater(parkinson_volatility(highs, lows).value, 0)
        self.assertGreater(yang_zhang_volatility(opens, highs, lows, closes).value, 0)
        self.assertTrue(0 <= gap_variance_share(opens, closes).value <= 1)

    def test_ewma_percentile_zscore_and_vrp(self):
        self.assertGreater(ewma_volatility_forecast([0.01, -0.02, 0.005]).value, 0)
        self.assertEqual(percentile_rank([10, 20, 30, 40], 30).value, 0.75)
        self.assertAlmostEqual(zscore([1, 2, 3]).value, 1.0)
        self.assertAlmostEqual(volatility_spread(20, 0.15).value, 0.05)
        self.assertAlmostEqual(volatility_ratio(20, 0.16).value, 1.25)

    def test_bad_inputs_remain_null(self):
        self.assertIsNone(realized_volatility([100, 101]).value)
        self.assertIsNone(parkinson_volatility([1], [1]).value)
        self.assertIsNone(volatility_ratio(20, 0).value)
        self.assertIsNone(probability_band(2500, 0.16, 3, -1))


if __name__ == "__main__":
    unittest.main()
