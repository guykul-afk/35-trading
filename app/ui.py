from __future__ import annotations

import streamlit as st

from ta35_dashboard.config import SETTINGS
from ta35_dashboard.services import load_dashboard_bundle
from ta35_dashboard.storage import SQLiteRepository


def repository() -> SQLiteRepository:
    return SQLiteRepository(SETTINGS.database_path)


@st.cache_data(show_spinner=False)
def _cached_bundle(database_path: str, modified_ns: int):
    del modified_ns  # cache-key only; the repository reads the path below.
    return load_dashboard_bundle(SQLiteRepository(database_path))


def bundle():
    try:
        database_path = SETTINGS.database_path
        modified_ns = database_path.stat().st_mtime_ns if database_path.exists() else 0
        return _cached_bundle(str(database_path), modified_ns)
    except LookupError:
        st.error(
            "אין נתוני Lite. הרץ `python scripts/seed_demo.py` לתצוגה או ייבא CSV ציבורי."
        )
        st.stop()


def page_header(title: str, data) -> None:
    st.set_page_config(page_title=title, page_icon="📉", layout="wide")
    st.title(title)
    status = "⚠️ נתונים ישנים" if data.meta.stale else "🟢 נתוני סוף יום"
    st.caption(
        f"{status} · נכון ל־{data.meta.as_of:%d/%m/%Y} · מקור: {data.meta.source} · [מאגר קוד (GitHub)]({SETTINGS.repository_url})"
    )
    if data.meta.market_data_type == "demo":
        st.warning("נתוני הדגמה סינתטיים — אינם מיועדים לקבלת החלטות מסחר.")
