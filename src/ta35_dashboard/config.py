from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    database_path: Path = PROJECT_ROOT / "data" / "ta35_lite.sqlite3"
    timezone: str = "Asia/Jerusalem"
    stale_after_days: int = 3
    model_version: str = "1.5.0"
    repository_url: str = "https://github.com/guykul-afk/35-trading"
    trading_days_per_year: float = 245.0


SETTINGS = Settings()
TRADING_DAYS_PER_YEAR = SETTINGS.trading_days_per_year

