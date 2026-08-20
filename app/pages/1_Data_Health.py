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
frame = pd.DataFrame(
    [
        {
            "סדרה": item.symbol,
            "תאריך אחרון": item.last_date,
            "מספר תצפיות": item.observations,
            "מקור": item.source or "—",
            "מצב": item.status,
        }
        for item in data.health
    ]
)
st.dataframe(frame, width="stretch", hide_index=True)
st.info(
    "סדרות TASE נקלטות מייצוא CSV רשמי. Cboe ניתנת לרענון אוטומטי. נתון חסר נשאר חסר ואינו מוחלף בערך ישן ללא סימון."
)
