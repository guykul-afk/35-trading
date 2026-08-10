import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.storage import SQLiteRepository


class PipelineTests(unittest.TestCase):
    def test_history_computes_lite_metrics_and_is_replay_safe(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            provider = DemoEodProvider(days=300)
            first = collect_history(provider, repository)
            second = collect_history(provider, repository)
            self.assertEqual(first, second)
            self.assertEqual(len(repository.list_snapshots(limit=500)), 300)
            metrics = {
                metric.metric_name: metric for metric in repository.latest_metrics()
            }
            expected = {
                "rv_5",
                "rv_20",
                "rv_60",
                "rv_20_60_ratio",
                "atr_5_20_ratio",
                "rv_yang_zhang_20",
                "gap_share_20",
                "vta35",
                "vta35_percentile_252",
                "vta35_change_5d",
                "vta35_zscore_60",
                "vrp_spread",
                "local_iv_family_score",
                "forecast_rv_3d",
                "expected_move_3d_points",
                "vix_curve_ratio",
                "vix9d_vix_ratio",
                "vix_vix3m_ratio",
                "stress_score",
                "volatility_direction_score",
                "market_trend_state",
            }
            self.assertTrue(expected <= metrics.keys())
            self.assertTrue(all(metrics[name].value is not None for name in expected))
            self.assertIn(
                metrics["stress_score"].dimensions["regime"],
                {"רגוע", "רגיל", "זהירות", "לחץ גבוה"},
            )
            self.assertTrue(-1 <= metrics["volatility_direction_score"].value <= 1)
            self.assertEqual(
                metrics["volatility_direction_score"].dimensions["available_inputs"],
                5,
            )
            self.assertEqual(
                metrics["local_iv_family_score"].dimensions["family"],
                "local_iv_no_double_count",
            )
            self.assertTrue(-1 <= metrics["market_trend_state"].value <= 1)
            self.assertEqual(
                metrics["market_trend_state"].dimensions["available_inputs"], 5
            )


if __name__ == "__main__":
    unittest.main()
