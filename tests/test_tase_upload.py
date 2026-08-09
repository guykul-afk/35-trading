import unittest
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
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


if __name__ == "__main__":
    unittest.main()
