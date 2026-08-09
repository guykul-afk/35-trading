import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.services import run_backtest
from ta35_dashboard.services.dashboard import CARD_DEFINITIONS
from ta35_dashboard.storage import SQLiteRepository


class BacktestTests(unittest.TestCase):
    def test_walk_forward_report_covers_indicators_horizons_and_strategies(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            collect_history(DemoEodProvider(days=400), repository)
            keys = tuple(definition[0] for definition in CARD_DEFINITIONS)
            report = run_backtest(repository, indicator_keys=keys)

            self.assertEqual(report.ta35_observations, 400)
            self.assertEqual(report.start_date.year, 2025)
            self.assertEqual(report.end_date.year, 2026)
            for key in keys:
                results = [
                    result
                    for result in report.indicator_results
                    if result.indicator_key == key and result.axis == "volatility"
                ]
                self.assertEqual({result.horizon_days for result in results}, {3, 7, 14, 30})
                self.assertTrue(all(1 <= result.strength <= 10 for result in results))
            self.assertEqual(
                {result.horizon_days for result in report.strategy_results},
                {3, 7, 14, 30},
            )
            self.assertTrue(any(result.observations for result in report.strategy_results))

    def test_future_tail_is_excluded_from_every_horizon(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            collect_history(DemoEodProvider(days=180), repository)
            report = run_backtest(repository, indicator_keys=("rv_acceleration",))
            for horizon in (3, 7, 14, 30):
                results = [
                    result
                    for result in report.indicator_results
                    if result.indicator_key == "rv_acceleration"
                    and result.horizon_days == horizon
                    and result.axis == "volatility"
                ]
                self.assertLessEqual(sum(result.observations for result in results), 180 - horizon)


if __name__ == "__main__":
    unittest.main()
