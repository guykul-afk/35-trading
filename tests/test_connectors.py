import unittest
from datetime import UTC, date, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import ValidationError

from ta35_dashboard.connectors import (
    CsvSeriesSpec,
    DailyBar,
    DemoEodProvider,
    PublicCsvEodProvider,
)


class ConnectorTests(unittest.TestCase):
    def test_demo_is_deterministic_and_eod_only(self):
        provider = DemoEodProvider(days=10)
        first, second = provider.fetch_history(), provider.fetch_history()
        self.assertEqual(first, second)
        self.assertEqual(len(first), 10)
        self.assertEqual(
            {bar.symbol for bar in first[-1].bars},
            {"TA35", "VTA35", "USDILS", "VIX9D", "VIX", "VIX3M"},
        )
        self.assertTrue(all("demo" in bar.quality_flags for bar in first[-1].bars))

    def test_public_csv_supports_english_and_hebrew_columns(self):
        with TemporaryDirectory() as directory:
            ta = Path(directory) / "ta.csv"
            ta.write_text(
                "Date,Open,High,Low,Close\n2026-08-06,2500,2530,2490,2520\n",
                encoding="utf-8",
            )
            vta = Path(directory) / "vta.csv"
            vta.write_text("תאריך,נעילה\n2026-08-06,18.5\n", encoding="utf-8")
            provider = PublicCsvEodProvider(
                (
                    CsvSeriesSpec("TA35", ta, "TASE", True),
                    CsvSeriesSpec("VTA35", vta, "TASE", True),
                )
            )
            snapshot = provider.fetch_snapshot()
            self.assertEqual(snapshot.bar("TA35").high, 2530)
            self.assertEqual(snapshot.bar("VTA35").close, 18.5)
            self.assertEqual(snapshot.session_date, date(2026, 8, 6))
            self.assertIn("manual_import", snapshot.bar("TA35").quality_flags)

    def test_public_csv_skips_tase_information_rows(self):
        with TemporaryDirectory() as directory:
            ta = Path(directory) / "ta.csv"
            ta.write_text(
                "שם המדד,תא 35\nטווח,3 שנים\n"
                "תאריך,פתיחה,גבוה,נמוך,נעילה\n"
                "06/08/2026,2500,2530,2490,2520\n",
                encoding="utf-8",
            )
            snapshot = PublicCsvEodProvider(
                (CsvSeriesSpec("TA35", ta, "TASE", True, True),)
            ).fetch_snapshot()
            self.assertEqual(snapshot.bar("TA35").close, 2520)

    def test_bar_rejects_partial_or_impossible_ohlc(self):
        with self.assertRaises(ValidationError):
            DailyBar(
                symbol="TA35",
                session_date=date(2026, 8, 9),
                open=1,
                close=1,
                source="x",
            )
        with self.assertRaises(ValidationError):
            DailyBar(
                symbol="TA35",
                session_date=date(2026, 8, 9),
                open=2,
                high=1,
                low=0.5,
                close=2,
                source="x",
            )

    def test_as_of_filters_demo(self):
        provider = DemoEodProvider(days=10)
        snapshot = provider.fetch_snapshot(datetime(2026, 8, 5, tzinfo=UTC))
        self.assertLessEqual(snapshot.session_date, date(2026, 8, 5))


if __name__ == "__main__":
    unittest.main()
