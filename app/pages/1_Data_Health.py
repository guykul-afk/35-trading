from __future__ import annotations

from pathlib import Path
import sys

# Ensure app directory and src directory are at the beginning of sys.path
_APP_DIR = Path(__file__).resolve().parent.parent
_PROJECT_ROOT = _APP_DIR.parent
_SRC_DIR = _PROJECT_ROOT / "src"

for _p in (_APP_DIR, _SRC_DIR):
    _p_str = str(_p)
    if _p_str in sys.path:
        sys.path.remove(_p_str)
    sys.path.insert(0, _p_str)

import pandas as pd
import streamlit as st
from ui import bundle, page_header

data = bundle()
page_header("בריאות נתונים — Lite", data)
from ta35_dashboard.analytics.putcall_service import load_latest_putcall_snapshot
from ta35_dashboard.config import SETTINGS

health_rows = [
    {
        "סדרה": item.symbol,
        "תאריך אחרון": item.last_date,
        "מספר תצפיות": item.observations,
        "מקור": item.source or "—",
        "מצב": item.status,
    }
    for item in data.health
]

pc_snap = load_latest_putcall_snapshot(SETTINGS.database_path)
if pc_snap:
    health_rows.append({
        "סדרה": "PUTCALL_CHART (פוזיציות פתוחות ומחזורים)",
        "תאריך אחרון": pc_snap.as_of_date,
        "מספר תצפיות": len(pc_snap.strikes),
        "מקור": "TASE (נגזרים)",
        "מצב": "תקין",
    })
else:
    health_rows.append({
        "סדרה": "PUTCALL_CHART (פוזיציות פתוחות ומחזורים)",
        "תאריך אחרון": None,
        "מספר תצפיות": 0,
        "מקור": "TASE (נגזרים)",
        "מצב": "חסר",
    })

frame = pd.DataFrame(health_rows)
st.dataframe(frame, width="stretch", hide_index=True)

st.info(
    "סדרות TASE נקלטות מייצוא CSV רשמי. Cboe ניתנת לרענון אוטומטי. נתון חסר נשאר חסר ואינו מוחלף בערך ישן ללא סימון."
)
st.link_button(
    "📊 דף תרשים פוט/קול ומחזורים בבורסה (Put/Call Chart)",
    "https://market.tase.co.il/he/market_data/derivatives/01/putcallchart",
    type="primary",
    use_container_width=True,
)

