from __future__ import annotations

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
