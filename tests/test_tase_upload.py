import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.connectors import CsvSeriesSpec, read_series
from ta35_dashboard.jobs import collect_history
from ta35_dashboard.services import import_tase_uploads
from ta35_dashboard.storage import SQLiteRepository


def ta35_csv(end_day: int = 30, *, preamble: bool = True) -> bytes:
    rows = ["Date,Open,High,Low,Close"]
    for day in range(1, end_day + 1):
        close = 2500 + day
        rows.append(f"2026-07-{day:02d},{close - 2},{close + 5},{close - 5},{close}")
    prefix = "Index,TA-35\nRange,3 Years\n" if preamble else ""
    return (prefix + "\n".join(rows) + "\n").encode()


class TaseUploadTests(unittest.TestCase):
    def test_reader_accepts_tase_trade_date_with_semicolon_separator(self):
        with TemporaryDirectory() as directory:
            source = Path(directory) / "ta35.csv"
            source.write_text(
                "מדד;תאריך המסחר;שער פתיחה;גבוה;נמוך;שער נעילה\n"
                "תא-35;01/07/2026;2500;2510;2490;2505\n",
                encoding="utf-8",
            )

            bars = read_series(CsvSeriesSpec("TA35", source, "TASE", True, True))

            self.assertEqual(len(bars), 1)
            self.assertEqual(bars[0].session_date, date(2026, 7, 1))
            self.assertEqual(bars[0].close, 2505)

    def test_upload_replaces_database_only_after_validation(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "data" / "lite.sqlite3"
            downloads = root / "downloads"
            collect_history(
                DemoEodProvider(days=30, end=date(2026, 6, 30)),
                SQLiteRepository(database),
            )

            result = import_tase_uploads(database, downloads, {"TA35": ta35_csv()})

            self.assertEqual(result.observations["TA35"], 30)
            self.assertEqual(result.latest_dates["TA35"], date(2026, 7, 30))
            latest = SQLiteRepository(database).bar_history("TA35")[-1]
            self.assertEqual(latest.close, 2530)
            self.assertTrue((downloads / "ta35.csv").exists())
            backups = list((database.parent / "backups").glob("*.sqlite3"))
            self.assertEqual(len(backups), 1)

    def test_invalid_upload_leaves_database_unchanged(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "data" / "lite.sqlite3"
            repository = SQLiteRepository(database)
            collect_history(DemoEodProvider(days=30, end=date(2026, 6, 30)), repository)
            before = database.read_bytes()

            with self.assertRaises(ValueError):
                import_tase_uploads(database, root / "downloads", {"TA35": b"bad"})

            self.assertEqual(database.read_bytes(), before)

    def test_reupload_skips_days_that_already_exist(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "data" / "lite.sqlite3"
            downloads = root / "downloads"

            first = import_tase_uploads(database, downloads, {"TA35": ta35_csv()})
            second = import_tase_uploads(database, downloads, {"TA35": ta35_csv()})

            self.assertEqual(first.observations["TA35"], 30)
            self.assertEqual(second.observations["TA35"], 0)
            self.assertEqual(len(SQLiteRepository(database).bar_history("TA35")), 30)
            backups = list((database.parent / "backups").glob("*.sqlite3"))
            # The initial import creates one backup; a no-op re-upload does not.
            self.assertEqual(len(backups), 1)

    def test_import_adds_only_missing_dates_from_an_overlapping_file(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "data" / "lite.sqlite3"
            downloads = root / "downloads"
            first = ta35_csv(end_day=25)

            import_tase_uploads(database, downloads, {"TA35": first})
            result = import_tase_uploads(database, downloads, {"TA35": ta35_csv()})

            self.assertEqual(result.observations["TA35"], 5)
            history = SQLiteRepository(database).bar_history("TA35")
            self.assertEqual(len(history), 30)
            self.assertEqual(history[-1].session_date, date(2026, 7, 30))

    def test_incremental_upload_accepts_small_files_when_database_exists(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            database = root / "data" / "lite.sqlite3"
            downloads = root / "downloads"
            first = ta35_csv(end_day=25)
            import_tase_uploads(database, downloads, {"TA35": first})

            # Small 3-day update file
            small_update = (
                "שם המדד;תא 35\n"
                "תאריך המסחר;שער פתיחה;גבוה;נמוך;שער נעילה\n"
                "26/07/2026;2524;2531;2521;2526\n"
                "27/07/2026;2525;2532;2522;2527\n"
                "28/07/2026;2526;2533;2523;2528\n"
            ).encode("utf-8")

            result = import_tase_uploads(database, downloads, {"TA35": small_update})

            self.assertEqual(result.observations["TA35"], 3)
            self.assertEqual(result.latest_dates["TA35"], date(2026, 7, 28))
            history = SQLiteRepository(database).bar_history("TA35")
            self.assertEqual(len(history), 28)
            self.assertEqual(history[-1].close, 2528)


if __name__ == "__main__":
    unittest.main()
