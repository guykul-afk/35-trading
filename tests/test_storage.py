import sqlite3
import unittest
from datetime import UTC, datetime
from pathlib import Path
from tempfile import TemporaryDirectory

from ta35_dashboard.connectors import DemoEodProvider
from ta35_dashboard.storage import MetricValue, SQLiteRepository


class StorageTests(unittest.TestCase):
    def test_replay_safe_roundtrip_and_history(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "lite.sqlite3"
            repository = SQLiteRepository(path)
            snapshot = DemoEodProvider(days=3).fetch_snapshot()
            repository.insert_snapshot(snapshot)
            repository.insert_snapshot(snapshot)
            self.assertEqual(repository.latest_snapshot(), snapshot)
            self.assertEqual(len(repository.bar_history("TA35")), 1)
            with sqlite3.connect(path) as connection:
                self.assertEqual(
                    connection.execute("select count(*) from lite_runs").fetchone()[0],
                    1,
                )
                self.assertEqual(
                    connection.execute("select count(*) from eod_bars").fetchone()[0], 6
                )

    def test_metric_upsert(self):
        with TemporaryDirectory() as directory:
            repository = SQLiteRepository(Path(directory) / "lite.sqlite3")
            snapshot = DemoEodProvider(days=1).fetch_snapshot()
            repository.insert_snapshot(snapshot)
            base = {
                "metric_name": "rv_20",
                "as_of": datetime.now(UTC),
                "model_version": "x",
                "run_id": snapshot.run_id,
            }
            repository.insert_metrics([MetricValue(value=0.15, **base)])
            repository.insert_metrics([MetricValue(value=0.16, **base)])
            self.assertEqual(repository.latest_metrics("rv_20")[0].value, 0.16)


if __name__ == "__main__":
    unittest.main()
