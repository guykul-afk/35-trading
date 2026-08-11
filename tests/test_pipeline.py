import unittest
from datetime import UTC, date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from ta35_dashboard.connectors import (
    DailyBar,
    DemoEodProvider,
    MarketDataType,
    MarketSnapshot,
)
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

    def test_cboe_only_refresh_recomputes_metrics_for_new_run(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            collect_history(
                DemoEodProvider(days=300, end=date(2026, 8, 9)), repository
            )
            bars = tuple(
                DailyBar(
                    symbol=symbol,
                    session_date=date(2026, 8, 10),
                    close=value,
                    source="Cboe",
                )
                for symbol, value in (("VIX9D", 12.77), ("VIX", 15.46), ("VIX3M", 18.98))
            )
            snapshot = MarketSnapshot(
                run_id="cboe-only-2026-08-10",
                source="Cboe",
                source_timestamp=datetime(2026, 8, 10, tzinfo=UTC),
                received_timestamp=datetime(2026, 8, 11, tzinfo=UTC),
                market_data_type=MarketDataType.EOD,
                bars=bars,
            )

            class CboeOnlyProvider:
                def fetch_history(self, *, start=None, end=None):
                    return [snapshot]

            collect_history(CboeOnlyProvider(), repository)
            metrics = repository.latest_metrics()

            self.assertGreater(len(metrics), 0)
            self.assertEqual({metric.run_id for metric in metrics}, {snapshot.run_id})
            self.assertIn("rv_20", {metric.metric_name for metric in metrics})

    def test_failed_analytics_does_not_activate_partial_refresh(self):
        with TemporaryDirectory() as directory:
            database = Path(directory) / "lite.sqlite3"
            repository = SQLiteRepository(database)
            collect_history(DemoEodProvider(days=30), repository)
            before = database.read_bytes()

            with patch(
                "ta35_dashboard.jobs.pipeline.compute_latest_metrics",
                side_effect=RuntimeError("analytics failed"),
            ):
                with self.assertRaisesRegex(RuntimeError, "analytics failed"):
                    collect_history(DemoEodProvider(days=31), repository)

            self.assertEqual(database.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
