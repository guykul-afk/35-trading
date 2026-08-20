import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.services import DashboardBundle, load_dashboard_bundle
from ta35_dashboard.services.dashboard import CARD_DEFINITIONS
from ta35_dashboard.storage import SQLiteRepository


class ServiceTests(unittest.TestCase):
    def test_bundle_is_consistent_and_marks_demo(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            collect_history(DemoEodProvider(days=300), repository)
            bundle = load_dashboard_bundle(
                repository, now=datetime(2026, 8, 9, tzinfo=UTC)
            )
            self.assertIsInstance(bundle, DashboardBundle)
            self.assertEqual(bundle.meta.market_data_type, "demo")
            self.assertEqual(len(bundle.cards), len(CARD_DEFINITIONS))

            self.assertEqual(len(bundle.health), 6)
            self.assertTrue(bundle.ta35_closes)
            self.assertIsNotNone(bundle.forecast_volatility)
            self.assertIsNotNone(bundle.implied_volatility)
            self.assertIn(bundle.volatility_direction, {"התרחבות", "התכווצות", "מעורב"})
            self.assertIn(
                bundle.market_trend,
                {"מגמה חיובית", "מגמה שלילית", "מצב מעורב"},
            )
            self.assertGreaterEqual(bundle.volatility_direction_score, -1)
            self.assertLessEqual(bundle.volatility_direction_score, 1)
            self.assertGreaterEqual(bundle.market_trend_score, -1)
            self.assertLessEqual(bundle.market_trend_score, 1)
            for card in bundle.cards:
                self.assertIn(card.volatility_arrow, {"↑", "↓", "↔", "—"})
                self.assertGreaterEqual(card.volatility_strength, 1)
                self.assertLessEqual(card.volatility_strength, 10)
                self.assertIn(card.market_arrow, {"↑", "↓", "↔", "—"})
                self.assertGreaterEqual(card.market_strength, 1)
                self.assertLessEqual(card.market_strength, 10)
                self.assertTrue(card.signal_note)
            self.assertEqual(bundle.backtest.ta35_observations, 300)
            self.assertTrue(bundle.backtest.indicator_results)
            self.assertTrue(bundle.backtest.strategy_results)
            self.assertIn(bundle.regime_matrix.market_state, {"עולה", "ניטרלי", "יורד"})
            self.assertIn(
                bundle.regime_matrix.volatility_state,
                {"מתרחבת", "מעורבת", "מתכווצת"},
            )
            self.assertFalse(bundle.premium_evidence.eligible)
            self.assertTrue(bundle.context_ablation)

            cards = {card.key: card for card in bundle.cards}
            self.assertEqual(cards["rv_acceleration"].market_arrow, "↔")
            self.assertEqual(cards["rv_acceleration"].market_strength, 1)
            self.assertEqual(cards["atr_5_20_ratio"].market_arrow, "↔")
            self.assertEqual(cards["atr_5_20_ratio"].market_strength, 1)
            self.assertNotEqual(cards["vta35_change_5d"].market_arrow, "↔")

    def test_empty_repository_raises(self):
        with (
            TemporaryDirectory() as directory,
            self.assertRaisesRegex(LookupError, "no Lite EOD data"),
        ):
            load_dashboard_bundle(SQLiteRepository(Path(directory) / "empty.sqlite3"))

    def test_every_metric_card_has_expanded_explanation(self):
        self.assertGreaterEqual(len(CARD_DEFINITIONS), 23)

        for key, _label, _format, help_text in CARD_DEFINITIONS:
            with self.subTest(key=key):
                self.assertIn("**מהו המדד?**", help_text)
                self.assertIn("**איך הוא בנוי?**", help_text)
                self.assertIn("**איך מפרשים?**", help_text)
                self.assertIn("**חשוב לדעת:**", help_text)

    def test_streamlit_entrypoints_compile(self):
        paths = [Path("app/Home.py"), *Path("app/pages").glob("*.py")]
        self.assertEqual(len(paths), 2)
        for path in paths:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")

    def test_probability_fan_has_an_independent_horizon_control(self):
        source = Path("app/Home.py").read_text(encoding="utf-8")
        self.assertTrue('key="backtest_horizon"' in source or 'key="strategy_horizon"' in source)
        self.assertIn('key="probability_fan_horizon"', source)
        self.assertIn("periods=fan_horizon", source)


if __name__ == "__main__":
    unittest.main()
