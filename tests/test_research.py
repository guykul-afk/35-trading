import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.services import (
    render_research_markdown,
    run_research_backtest,
    write_research_report,
)
from ta35_dashboard.storage import SQLiteRepository


class ResearchBacktestTests(unittest.TestCase):
    def test_report_covers_requested_horizons_and_robustness_tables(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            collect_history(DemoEodProvider(days=420), repository)
            report = run_research_backtest(
                repository,
                indicator_keys=("rv_acceleration", "vta35_change_5d"),
            )

            self.assertEqual(report.observations, 420)
            expected = {3, 7, 14, 30}
            self.assertEqual(
                set(report.tables["indicator_aggregate"]["horizon"]), expected
            )
            self.assertEqual(
                set(report.tables["strategy_summary"]["horizon"]), expected
            )
            self.assertIn("indicator_by_regime", report.tables)
            self.assertIn("indicator_intensity", report.tables)
            self.assertIn("strategy_sensitivity", report.tables)
            self.assertIn("forecast_calibration", report.tables)
            self.assertIn("har_rv_benchmark", report.tables)
            self.assertIn("knowledge_ranking", report.tables)
            self.assertIn("context_ablation_oos", report.tables)
            ablation = report.tables["context_ablation_oos"]
            self.assertEqual(
                set(ablation["feature"]),
                {"fx_equity_state", "ta35_vta35_corr_60"},
            )
            self.assertTrue(
                {"n_eff", "lift", "fdr_q", "eligible", "status"}
                <= set(ablation.columns)
            )
            self.assertEqual(
                set(report.tables["knowledge_ranking"]["tier"]),
                {"C — context only (validation freeze)"},
            )
            aggregate = report.tables["indicator_aggregate"]
            self.assertTrue(
                {
                    "n_eff",
                    "nonoverlap_accuracy_min",
                    "nonoverlap_accuracy",
                    "nonoverlap_accuracy_max",
                }
                <= set(aggregate.columns)
            )

    def test_markdown_contains_all_results_in_one_document(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            repository = SQLiteRepository(root / "lite.sqlite3")
            collect_history(DemoEodProvider(days=320), repository)
            report = run_research_backtest(
                repository, indicator_keys=("rv_acceleration",)
            )
            markdown = render_research_markdown(report)
            self.assertIn("comprehensive backtest research", markdown)
            self.assertIn("Every strategy family", markdown)
            self.assertIn("Indicator robustness by market regime", markdown)
            self.assertIn("Calendar / Diagonal", markdown)
            destination = write_research_report(report, root / "report.md")
            self.assertEqual(destination.read_text(encoding="utf-8"), markdown)


if __name__ == "__main__":
    unittest.main()
