from __future__ import annotations

import math
from pathlib import Path
import sqlite3
import sys
import time

# Ensure app directory and src directory are at the beginning of sys.path
_APP_DIR = Path(__file__).resolve().parent
_PROJECT_ROOT = _APP_DIR.parent
_SRC_DIR = _PROJECT_ROOT / "src"

for _p in (_APP_DIR, _SRC_DIR):
    _p_str = str(_p)
    if _p_str in sys.path:
        sys.path.remove(_p_str)
    sys.path.insert(0, _p_str)

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from ui import bundle, page_header, repository

from decision_ui import render_decision_hero
from ta35_dashboard.analytics import probability_band
from ta35_dashboard.analytics.forecasting import predict_live_direction
from ta35_dashboard.config import PROJECT_ROOT, SETTINGS
from ta35_dashboard.decision_engine.engine import run_trade_decision_engine
from ta35_dashboard.services import import_tase_uploads

# Load centralized EOD data bundle
data = bundle()
card_map = {card.key: card for card in data.cards}
repo = repository()

# Extract rise probability and spot for decision engine
range_pos_card = card_map.get("range_position_20")
safety_card = card_map.get("flight_to_safety")
banks_rs_card = card_map.get("banks_rs_spread")

latest_prob_init, prob_confidence = predict_live_direction(
    horizon_days=7,
    market_trend_score=data.market_trend_score,
    range_position=range_pos_card.value if range_pos_card else None,
    flight_to_safety=safety_card.value if safety_card else None,
    banks_rs=banks_rs_card.value if banks_rs_card else None,
)
last_close_val_init = float(data.ta35_closes[-1]) if data.ta35_closes else 4150.0

vta35_card = card_map.get("vta35")
vta35_val = vta35_card.value if vta35_card and vta35_card.value is not None else (data.implied_volatility * 100 if data.implied_volatility else (data.vta35_values[-1] if data.vta35_values else None))

rv20_card = card_map.get("realized_volatility_20") or card_map.get("rv_20")
rv20_val = rv20_card.value if rv20_card and rv20_card.value is not None else (float(data.forecast_volatility) if data.forecast_volatility is not None else 0.14)

vrp_card = card_map.get("vrp_spread")
vrp_val = vrp_card.value if vrp_card and vrp_card.value is not None else None

# Run 100% EOD Trade Decision Engine
decision_result = run_trade_decision_engine(
    spot_price=last_close_val_init,
    prob_up=latest_prob_init,
    forecast_rv=float(data.forecast_volatility) if data.forecast_volatility is not None else 0.15,
    current_rv=float(rv20_val),
    regime=getattr(data, "regime", "NORMAL"),
    volatility_state=data.regime_matrix.volatility_state,
    market_state=data.regime_matrix.market_state,
    horizon_days=7,
)

page_header("מנוע החלטת מסחר ת״א־35 — EOD Trade Decision Engine", data)

# יצירת חלוקת הטאבים המרכזית (פירמידה הפוכה)
tab_trade, tab_track, tab_market, tab_research, tab_data = st.tabs(
    [
        "🎯 הטרייד",
        "📈 מעקב",
        "🌍 שוק ומניפה",
        "🔬 מחקר",
        "⚙️ נתונים",
    ]
)

# -----------------------------------------------------------------------------
# TAB 1: THE TRADE — מנוע החלטת המסחר (100% EOD)
# -----------------------------------------------------------------------------
with tab_trade:
    render_decision_hero(decision_result, spot_price=last_close_val_init)

# -----------------------------------------------------------------------------
# TAB 2: TRACK & VOLATILITY — מעקב תנודתיות ועקומים
# -----------------------------------------------------------------------------
with tab_track:
    st.subheader("📈 מעקב תנודתיות ועקום מבנה שוק (Volatility Term Structure)")

    # 1. מדדי תנודתיות מרכזיים
    col_v1, col_v2, col_v3, col_v4 = st.columns(4)
    with col_v1:
        st.metric(
            "VTA35 (תנודתיות גלומה)",
            f"{vta35_val:.2f}%" if vta35_val is not None else "—",
            help="מדד התנודתיות הגלומה הרשמי של בורסת ת״א לאופציות מעוף 30 יום.",
        )
    with col_v2:
        st.metric(
            "תחזית תנודתיות מודל (HAR/GJR)",
            f"{data.forecast_volatility * 100:.2f}%" if data.forecast_volatility is not None else "—",
            help="תחזית תנודתיות שנתית משוקללת סוף-יום (OOS).",
        )
    with col_v3:
        st.metric(
            "RV-20 (תנודתיות בפועל 20 יום)",
            f"{rv20_val * 100:.2f}%" if rv20_val is not None else "—",
            help="תנודתיות מימוש היסטורית ב-20 ימי המסחר האחרונים.",
        )
    with col_v4:
        st.metric(
            "פרמיית תנודתיות (VRP Spread)",
            f"{vrp_val:+.2f}%" if vrp_val is not None else "—",
            help="מרווח בין VTA35 לבין Realized Volatility 20d (חיובי = פרמיה יקרה / Contango).",
        )

    st.markdown("---")

    # 2. עקום תנודתיות גלובלי (CBOE VIX Curve)
    st.subheader("🌐 עקום תנודתיות גלובלי (Cboe VIX Curve: 9D / 30D / 3M)")
    st.caption("ניתוח מבנה עקום התנודתיות הבינלאומי (Contango vs Backwardation) המשפיע ישירות על ת״א־35.")

    vix9d_history = repo.bar_history("VIX9D", 1)
    vix_history = repo.bar_history("VIX", 1)
    vix3m_history = repo.bar_history("VIX3M", 1)
    vix9d_val = vix9d_history[-1].close if vix9d_history else None
    vix_val = vix_history[-1].close if vix_history else None
    vix3m_val = vix3m_history[-1].close if vix3m_history else None

    vix_vals = []
    vix_labels = []
    if vix9d_val is not None:
        vix_labels.append("VIX 9D (קצר)")
        vix_vals.append(vix9d_val)
    if vix_val is not None:
        vix_labels.append("VIX 30D (סטנדרטי)")
        vix_vals.append(vix_val)
    if vix3m_val is not None:
        vix_labels.append("VIX 3M (רבעוני)")
        vix_vals.append(vix3m_val)

    if vix_vals:
        fig_vix = go.Figure()
        fig_vix.add_trace(
            go.Scatter(
                x=vix_labels,
                y=vix_vals,
                mode="lines+markers+text",
                name="מדדי VIX (%)",
                text=[f"{v:.2f}%" for v in vix_vals],
                textposition="top center",
                line={"color": "#00d4b1", "width": 3},
                marker={"size": 10, "color": "#00ffd0"},
            )
        )
        fig_vix.update_layout(
            height=300,
            margin={"l": 10, "r": 10, "t": 20, "b": 10},
            yaxis_title="רמת תנודתיות (%)",
        )
        st.plotly_chart(fig_vix, use_container_width=True)
    else:
        st.info("נתוני עקום VIX אינם זמינים כעת.")

    st.markdown("---")

    # 3. מבנה אסטרטגיה וסיכום מנהלים
    st.subheader("💡 תמצית המלצת האסטרטגיה המרכזית")
    strat1, strat2, strat3, strat4 = st.columns(4)
    strat1.metric("מבנה נבחר", decision_result.primary_strategy_family.value)
    strat2.metric("אופק מומלץ", f"{decision_result.horizon_days} ימי מסחר")
    strat3.metric("כיוון שוק", decision_result.direction_view)
    strat4.metric("צפי תנודתיות", decision_result.volatility_view)
    st.info(f"**נימוק אסטרטגיה מועדפת:** {decision_result.rationale}")

# -----------------------------------------------------------------------------
# TAB 3: MARKET & FAN — שוק ומניפת הסתברות
# -----------------------------------------------------------------------------
with tab_market:
    st.subheader("🌍 שוק, משטרים ומניפת הסתברות סטטיסטית")

    last_close = data.ta35_closes[-1] if data.ta35_closes else None

    # 1. פאנל תחזית תנודתיות וטווח סטטיסטי ליום 1 קדימה
    if data.forecast_volatility is not None and last_close is not None:
        sigma_1d_pct = data.forecast_volatility / math.sqrt(252.0)
        sigma_1d_pts = last_close * sigma_1d_pct
        band_1s = (last_close - sigma_1d_pts, last_close + sigma_1d_pts)
        band_2s = (last_close - 2.0 * sigma_1d_pts, last_close + 2.0 * sigma_1d_pts)

        st.markdown("##### ⚡ תחזית תנודתיות ליום המסחר הבא (1-Day Ahead Forecast)")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(
                "תנודה יומית צפויה (1D Expected Move)",
                f"±{sigma_1d_pct * 100:.2f}%",
                f"±{sigma_1d_pts:.1f} נקודות",
                help="סטיית תקן יומית צפויה במדד ת״א-35 על בסיס תחזית התנודתיות המשוקללת.",
            )
        with c2:
            st.metric(
                "טווח צפוי ליום הבא (68.3% ±1.0σ)",
                f"{band_1s[0]:,.1f} – {band_1s[1]:,.1f}",
                help="הטווח הסטטיסטי שבו המדד צפוי להיסחר ביום המסחר הבא בהסתברות נורמלית של 68.3%.",
            )
        with c3:
            st.metric(
                "טווח קיצון ליום הבא (95.4% ±2.0σ)",
                f"{band_2s[0]:,.1f} – {band_2s[1]:,.1f}",
                help="גבולות קיצון יומיים בהסתברות של 95.4% (חריגה מטווח זה מעידה על אירוע חריג).",
            )

    st.markdown("---")

    # 2. מניפת הסתברות למדד
    st.markdown("##### 🎯 מניפת הסתברות סטטיסטית לת״א־35 (סביב שער הספוט)")
    fan_horizon = int(
        st.radio(
            "אופק מניפת הסתברות (ימי מסחר)",
            options=[1, 3, 7, 14, 30],
            horizontal=True,
            index=1,
            format_func=lambda value: "יום 1 (יום המסחר הבא)" if value == 1 else f"{value} ימים",
            key="probability_fan_horizon",
        )
    )

    if data.ta35_dates and data.forecast_volatility is not None and last_close is not None:
        last_date = pd.Timestamp(data.ta35_dates[-1])
        trading_day = pd.offsets.CustomBusinessDay(weekmask="Sun Mon Tue Wed Thu")
        future_dates = pd.DatetimeIndex(
            [
                last_date,
                *pd.date_range(
                    start=last_date + trading_day,
                    periods=fan_horizon,
                    freq=trading_day,
                ),
            ]
        )
        fan = pd.DataFrame({"date": future_dates, "center": last_close})
        for sigma in (0.5, 1.0, 1.5, 2.0):
            bands = [
                probability_band(last_close, data.forecast_volatility, day, sigma)
                for day in range(fan_horizon + 1)
            ]
            fan[f"lower_{sigma}"] = [band[0] for band in bands if band is not None]
            fan[f"upper_{sigma}"] = [band[1] for band in bands if band is not None]

        fig_fan = go.Figure()
        history_points = min(90, len(data.ta35_dates))
        fig_fan.add_trace(
            go.Scatter(
                x=data.ta35_dates[-history_points:],
                y=data.ta35_closes[-history_points:],
                mode="lines",
                name="ת״א־35 בפועל",
                line={"color": "#00d4b1", "width": 2.5},
                hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f} נק׳<extra></extra>",
            )
        )
        band_styles = (
            (2.0, "95.4% (±2.0σ)", "rgba(82, 132, 190, 0.13)"),
            (1.5, "86.6% (±1.5σ)", "rgba(82, 132, 190, 0.22)"),
            (1.0, "68.3% (±1.0σ)", "rgba(82, 132, 190, 0.36)"),
            (0.5, "38.3% (±0.5σ)", "rgba(82, 132, 190, 0.54)"),
        )
        for sigma, label, fill_color in band_styles:
            fig_fan.add_trace(
                go.Scatter(
                    x=fan["date"],
                    y=fan[f"lower_{sigma}"],
                    mode="lines",
                    line={"width": 0},
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            fig_fan.add_trace(
                go.Scatter(
                    x=fan["date"],
                    y=fan[f"upper_{sigma}"],
                    mode="lines",
                    line={"width": 0},
                    fill="tonexty",
                    fillcolor=fill_color,
                    name=label,
                    customdata=fan[f"lower_{sigma}"],
                    hovertemplate=(
                        f"{label}<br>%{{x|%d/%m/%Y}}<br>טווח: %{{customdata:,.0f}} – %{{y:,.0f}}"
                        "<extra></extra>"
                    ),
                )
            )
        fig_fan.add_trace(
            go.Scatter(
                x=fan["date"],
                y=fan["center"],
                mode="lines",
                name="מרכז התחזית (Spot)",
                line={"color": "#f3f6fb", "width": 2, "dash": "dash"},
                hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f} (ספוט)<extra></extra>",
            )
        )
        fig_fan.add_vline(
            x=last_date.timestamp() * 1000,
            line_dash="dot",
            line_color="#8b98aa",
        )
        fig_fan.update_layout(
            height=480,
            margin={"l": 10, "r": 10, "t": 20, "b": 10},
            hovermode="x unified",
            legend={"orientation": "h", "y": 1.08, "x": 0},
            xaxis_title="תאריך",
            yaxis_title="נקודות מדד ת״א־35",
        )
        st.plotly_chart(fig_fan, use_container_width=True)

        summary_rows = []
        for days in (1, 3, 7, 14, 30):
            row = {"אופק (ימי מסחר)": "יום 1 (הבא)" if days == 1 else f"{days} ימים"}
            for sigma, label in ((0.5, "±0.5σ (38%)"), (1.0, "±1.0σ (68%)"), (1.5, "±1.5σ (87%)"), (2.0, "±2.0σ (95%)")):
                band = probability_band(last_close, data.forecast_volatility, days, sigma)
                if band is not None:
                    row[label] = f"{band[0]:,.0f} – {band[1]:,.0f}"
            summary_rows.append(row)
        st.dataframe(pd.DataFrame(summary_rows), hide_index=True, use_container_width=True)

        st.caption(
            f"החישוב מבוסס על תחזית תנודתיות שנתית משולבת של {data.forecast_volatility:.1%}, "
            "252 ימי מסחר לשנה, ושער ספוט של "
            f"{last_close:,.2f} נקודות. התאריכים העתידיים מחושבים לפי ימי מסחר בורסאיים (א׳–ה׳)."
        )
    else:
        st.info("אין מספיק נתוני ת״א־35 או תחזית תנודתיות להצגת המניפה.")

    st.markdown("---")

    # 2. גרפי היסטוריית TA-35 ו-VTA35
    hist_left, hist_right = st.columns(2)
    with hist_left:
        st.subheader("ת״א־35 — 252 ימי נתונים")
        if data.ta35_dates:
            st.line_chart(pd.DataFrame({"ת״א־35": data.ta35_closes}, index=data.ta35_dates))
    with hist_right:
        st.subheader("VTA35 — תנודתיות גלומה היסטורית")
        if data.vta35_dates:
            figure = go.Figure(
                go.Scatter(x=data.vta35_dates, y=data.vta35_values, name="VTA35", line={"color": "#ff9900"})
            )
            figure.update_layout(
                height=350,
                margin={"l": 10, "r": 10, "t": 10, "b": 10},
                yaxis_title="אחוזים",
            )
            st.plotly_chart(figure, use_container_width=True)
        else:
            st.info("VTA35 חסר; מדדי VRP ואחוזון לא יחושבו.")

# -----------------------------------------------------------------------------
# TAB 4: RESEARCH — מחקר, אינדיקטורים ו-EOD
# -----------------------------------------------------------------------------
with tab_research:
    st.subheader("📊 אינדיקטורים טכניים ומדדי תנודתיות (סוף-יום)")
    strength_horizon = int(
        st.radio(
            "אופק מדדי העוצמה (ימי מסחר)",
            options=[1, 3, 7, 14, 30],
            horizontal=True,
            index=1,
            format_func=lambda value: "יום 1" if value == 1 else f"{value} ימים",
            key="backtest_horizon",
        )
    )

    card_map = {card.key: card for card in data.cards}

    def render_card_grid(keys: tuple[str, ...]):
        selected_cards = [card_map[k] for k in keys if k in card_map]
        for start in range(0, len(selected_cards), 4):
            columns = st.columns(4)
            for column, card in zip(
                columns, selected_cards[start : start + 4], strict=False
            ):
                card_label = card.label
                card_val = card.value
                query_key = card.key
                
                if query_key.endswith("_3d") or query_key == "expected_move_3d_points":
                    if query_key == "expected_move_3d_points":
                        query_key = f"expected_move_{strength_horizon}d_points"
                        card_label = f"טווח {strength_horizon} ימים"
                        if last_close_val_init is not None and data.forecast_volatility is not None:
                            card_val = last_close_val_init * data.forecast_volatility * math.sqrt(strength_horizon / 252.0)
                    else:
                        query_key = query_key.replace("_3d", f"_{strength_horizon}d")
                        if "forecast_rv" in query_key:
                            card_label = f"תחזית RV ל־{strength_horizon} ימים"
                        elif "har_rv" in query_key:
                            card_label = f"HAR-EOD ל־{strength_horizon} ימים"
                        elif "matched_vrp" in query_key:
                            card_label = f"VRP מותאם ({strength_horizon} ימים)"

                display = "לא זמין" if card_val is None else format(card_val, card.format)
                vol_result = data.backtest.indicator(
                    query_key, strength_horizon, "volatility", card.volatility_arrow
                )
                column.metric(
                    card_label,
                    display,
                    help=(
                        f"{card.help}\n\n**פירוש הסימול:** {card.signal_note}\n\n"
                        f"**Backtest תנודתיות ({strength_horizon} ימים):** "
                        + (
                            f"{vol_result.hit_rate:.1%} הצלחה ב־"
                            f"{vol_result.observations} מקרים."
                            if vol_result and vol_result.hit_rate is not None
                            else "אין מדגם מספיק."
                        )
                    ),
                )
                column.caption(
                    f"תנודתיות {card.volatility_arrow} · ת״א־35 {card.market_arrow}"
                )

    with st.expander("תנודתיות מימוש (Realized Volatility)", expanded=True):
        render_card_grid(
            (
                "forecast_rv_3d",
                "expected_move_3d_points",
                "rv_20_60_ratio",
                "downside_share_20",
                "rs_range_5_20",
                "har_rv_3d",
            )
        )

    with st.expander("תנודתיות גלומה ופרמיה (IV & Premium)", expanded=True):
        render_card_grid(
            (
                "vta35",
                "vrp_spread",
                "vta35_momentum_5d",
                "vta35_zscore_60d",
                "vta_vol_of_vol_20",
                "matched_vrp_3d",
            )
        )

    with st.expander("תנופת מחיר וטווחים (Price & Range Momentum)", expanded=True):
        render_card_grid(
            (
                "rv_acceleration",
                "gap_share_20",
                "atr_5_20_ratio",
                "trend_efficiency_20",
                "range_position_20",
                "reversal_5_vol_scaled",
            )
        )

    with st.expander("לחץ גלובלי ומט״ח (Global Stress & FX)", expanded=True):
        render_card_grid(
            (
                "vix_curve_ratio",
                "vix9d_vix_ratio",
                "vix_vix3m_ratio",
                "usdils_change_5d",
                "local_global_stress_spread",
            )
        )

    with st.expander("🏦 סקטור הבנקים והובלת שוק (Banks & Sector Leadership)", expanded=True):
        render_card_grid(
            (
                "banks_rs_spread",
                "banks_momentum_5d",
                "banks_ta35_corr_20",
            )
        )

    with st.expander("🏛️ אג״ח ממשלתי, מאקרו ואשראי קונצרני (Gov Bonds, Credit & Macro)", expanded=True):
        render_card_grid(
            (
                "flight_to_safety",
                "gov_bond_momentum_5d",
                "stock_bond_corr_20",
                "credit_spread_stress",
                "credit_bond_momentum_5d",
            )
        )

    st.markdown("---")
    st.subheader("🔬 מטריצת משטר מלאה (3×3)")

    matrix_rows = []
    for market_state in ("עולה", "ניטרלי", "יורד"):
        row = {"כיוון שוק": market_state}
        for volatility_state in ("מתרחבת", "מעורבת", "מתכווצת"):
            row[volatility_state] = (
                "● מצב נוכחי"
                if market_state == data.regime_matrix.market_state
                and volatility_state == data.regime_matrix.volatility_state
                else "○"
            )
        matrix_rows.append(row)

    st.dataframe(pd.DataFrame(matrix_rows), hide_index=True, use_container_width=True)

# -----------------------------------------------------------------------------
# TAB 5: DATA & HEALTH — עדכון נתונים ובריאות המערכת (EOD Only)
# -----------------------------------------------------------------------------
with tab_data:
    col_head_title, col_head_reset = st.columns([2.5, 1.0])
    with col_head_title:
        st.subheader("⚙️ עדכון נתונים וסנכרון סדרות EOD")
        st.write(
            "העלאת קובץ ת״א־35 מעדכנת את נתוני הבורסה בת״א ומסנכרנת אוטומטית את כל מקורות המידע הרשמיים: "
            "ת״א־35, VTA35, מדדי VIX מארה״ב (Cboe) ושער דולר (USD/ILS)."
        )
    with col_head_reset:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🗑️ איפוס מטמון ורענון", type="secondary", use_container_width=True, help="איפוס זיכרון מטמון לצורך חישוב מחדש של כל המודלים"):
            st.cache_data.clear()
            st.toast("✅ זיכרון המטמון אופס בהצלחה!")
            time.sleep(0.3)
            st.rerun()

    st.markdown("##### 🔗 מרכז קישורי הורדה ישירים מאתר הבורסה (TASE)")
    col_l1, col_l2, col_l3 = st.columns(3)
    with col_l1:
        st.markdown("**📈 מניות ותנודתיות**")
        st.link_button(
            "מדד ת״א־35 (142)",
            "https://www.tase.co.il/he/market_data/index/142/historical_data",
            use_container_width=True,
        )
        st.link_button(
            "מדד VTA35 (598)",
            "https://www.tase.co.il/he/market_data/index/598/historical_data",
            use_container_width=True,
        )
        st.link_button(
            "מדד ת״א בנקים-5 (164)",
            "https://www.tase.co.il/he/market_data/index/164/historical_data",
            use_container_width=True,
        )
    with col_l2:
        st.markdown("**🏛️ אג״ח ממשלתי וקונצרני**")
        st.link_button(
            "תל גוב-כללי (601)",
            "https://www.tase.co.il/he/market_data/index/601/historical_data",
            use_container_width=True,
        )
        st.link_button(
            "תל-בונד 60 (709)",
            "https://www.tase.co.il/he/market_data/index/709/historical_data",
            use_container_width=True,
        )
    with col_l3:
        st.markdown("**⚡ נגזרים ופוזיציות פתוחות**")
        st.link_button(
            "דף שוק הנגזרים הראשי",
            "https://www.tase.co.il/he/market_data/derivatives",
            use_container_width=True,
        )
        st.link_button(
            "פוזיציות פתוחות ומחזורים",
            "https://www.tase.co.il/he/market_data/derivatives/open_positions",
            use_container_width=True,
        )
        st.link_button(
            "נתונים היסטוריים נגזרים",
            "https://www.tase.co.il/he/market_data/derivatives/historical_data",
            use_container_width=True,
        )

    st.markdown("---")
    with st.form("tase_csv_upload", clear_on_submit=True):
        st.markdown("##### 📥 העלאת קבצי CSV יומיים (זיהוי תוכן אוטומטי 🤖)")
        st.caption("אין חשיבות לשם הקובץ או לשדה שבו הוא הועלה — המערכת מנתחת את הטקסט שבתוך הקובץ ומשייכת אותו אוטומטית למדד הנכון.")
        
        multi_files = st.file_uploader(
            "📁 גרירת כל הקבצים ביחד (העלאה מרובה מהירה)",
            type=("csv",),
            accept_multiple_files=True,
            key="multi_csv",
            help="ניתן לסמן את כל קובצי ה-CSV שהורדתם ולגרור אותם לכאן בבת אחת!",
        )
        
        st.markdown("או בחירה בשדות נפרדים:")
        u_col1, u_col2 = st.columns(2)
        ta35_file = u_col1.file_uploader(
            "קובץ ת״א־35", type=("csv",), key="ta35_csv"
        )
        vta35_file = u_col2.file_uploader(
            "קובץ VTA35", type=("csv",), key="vta35_csv"
        )
        
        u_col3, u_col4 = st.columns(2)
        banks_file = u_col3.file_uploader(
            "קובץ ת״א בנקים-5", type=("csv",), key="banks_csv"
        )
        tel_gov_all_file = u_col4.file_uploader(
            "קובץ תל גוב-כללי", type=("csv",), key="tel_gov_all_csv"
        )

        u_col5, _ = st.columns(2)
        tel_bond60_file = u_col5.file_uploader(
            "קובץ תל-בונד 60", type=("csv",), key="tel_bond60_csv"
        )

        submitted = st.form_submit_button(
            "🚀 בדיקה, זיהוי אוטומטי ועדכון כל המקורות", type="primary", use_container_width=True
        )
    def _identify_series(raw: bytes, filename: str = "", default_hint: str = "TA35") -> str:
        sample = ""
        for enc in ("utf-8-sig", "utf-8", "windows-1255", "iso-8859-8", "utf-16"):
            try:
                sample = raw[:4096].decode(enc)
                break
            except UnicodeDecodeError:
                continue

        lines = sample.splitlines()[:10]
        header_text = " ".join(lines).lower().replace("-", " ").replace("_", " ").replace("״", '"')
        full_text = (header_text + " " + filename).lower().replace("-", " ").replace("_", " ").replace("״", '"')

        # Check explicit index codes and keywords
        if any(k in full_text for k in ("vta35", "vta 35", " 598 ", "598", "תנודתיות", "volatility")):
            return "VTA35"
        if any(k in full_text for k in ("banks", "בנקים 5", "בנקים", " 164 ", "164")):
            return "TA_BANKS5"
        if any(k in full_text for k in ("bond 60", "bond60", "בונד 60", "בונד60", " 709 ", "709")):
            return "TEL_BOND60"
        if any(k in full_text for k in ("gov all", "govall", "תל גוב כללי", "גוב כללי", " 601 ", "601")):
            return "TEL_GOV_ALL"
        if any(k in full_text for k in ("usd/ils", "usdils", "שער דולר", "דולר")):
            return "USDILS"
        if any(k in full_text for k in ("ta 35", "ta35", 'ת"א 35', "תל אביב 35", " 142 ", "142")):
            return "TA35"

        # Price heuristic fallback from numeric values in CSV
        try:
            for line in lines[3:]:
                parts = line.split(",")
                if len(parts) >= 2:
                    for p in parts[1:]:
                        try:
                            val = float(p.strip())
                            if 2000.0 <= val <= 6500.0:
                                return "TA35"
                            elif 5000.0 <= val <= 18000.0:
                                return "TA_BANKS5"
                            elif 450.0 <= val <= 550.0:
                                return "TEL_GOV_ALL"
                            elif 380.0 <= val <= 450.0:
                                return "TEL_BOND60"
                            elif 8.0 <= val <= 60.0:
                                return "VTA35"
                        except ValueError:
                            continue
        except Exception:
            pass

        return default_hint

    if submitted:
        uploaded_items = []
        if multi_files:
            for f in multi_files:
                uploaded_items.append((f, None))
        if ta35_file is not None:
            uploaded_items.append((ta35_file, "TA35"))
        if vta35_file is not None:
            uploaded_items.append((vta35_file, "VTA35"))
        if banks_file is not None:
            uploaded_items.append((banks_file, "TA_BANKS5"))
        if tel_gov_all_file is not None:
            uploaded_items.append((tel_gov_all_file, "TEL_GOV_ALL"))
        if tel_bond60_file is not None:
            uploaded_items.append((tel_bond60_file, "TEL_BOND60"))

        if not uploaded_items:
            st.error("יש לבחור לפחות קובץ נתונים אחד לפני העדכון.")
        else:
            payloads = {}
            detected_summary = []
            symbol_names = {
                "TA35": "ת״א־35",
                "VTA35": "VTA35",
                "TA_BANKS5": "ת״א בנקים-5",
                "TEL_GOV_ALL": "תל גוב-כללי",
                "TEL_BOND60": "תל-בונד 60",
            }
            for f, hint in uploaded_items:
                b = f.getvalue()
                sym = _identify_series(b, f.name, default_hint=hint or "TA35")
                payloads[sym] = b
                detected_summary.append(f"`{f.name}` ➔ **{symbol_names.get(sym, sym)}**")

            try:
                import importlib
                import ta35_dashboard.services.tase_upload as tase_upload_mod
                importlib.reload(tase_upload_mod)
                
                with st.spinner("מנתח את תוכן הקבצים, מזהה את הסדרות ומסנכרן את המערכת…"):
                    result = tase_upload_mod.import_tase_uploads(
                        SETTINGS.database_path, PROJECT_ROOT / "downloads", payloads
                    )
            except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
                st.error(f"העדכון לא בוצע: {error}")
            else:
                details = " · ".join(
                    f"{symbol_names.get(symbol, symbol)}: {result.observations[symbol]:,} ימים חדשים"
                    for symbol in result.observations
                )
                st.cache_data.clear()
                st.cache_resource.clear()
                st.success(f"הנתונים זוהו ועודכנו בהצלחה! {details}")
                st.info("🎯 זיהוי קבצים שבוצע: " + " | ".join(detected_summary))
                time.sleep(0.5)
                st.rerun()

    with st.expander("🛠️ ניהול ושחזור נתונים (Rollback / ביטול עדכון שגוי)"):
        st.markdown("אם הועלה קובץ שגוי או שברצונך לבטל את העדכון האחרון:")
        if st.button("⏪ שחזר / בטל עדכון אחרון", type="secondary"):
            try:
                conn = sqlite3.connect(SETTINGS.database_path)
                cur = conn.cursor()
                cur.execute("SELECT run_id, source_timestamp FROM lite_runs ORDER BY rowid DESC LIMIT 2")
                runs = cur.fetchall()
                if len(runs) > 1:
                    last_run_id = runs[0][0]
                    cur.execute("DELETE FROM eod_bars WHERE run_id = ?", (last_run_id,))
                    cur.execute("DELETE FROM lite_metrics WHERE run_id = ?", (last_run_id,))
                    cur.execute("DELETE FROM lite_runs WHERE run_id = ?", (last_run_id,))
                    conn.commit()
                    conn.close()
                    
                    repo_fresh = SQLiteRepository(SETTINGS.database_path)
                    snap_fresh = repo_fresh.latest_snapshot()
                    if snap_fresh:
                        from ta35_dashboard.jobs.pipeline import compute_latest_metrics
                        fresh_metrics = compute_latest_metrics(repo_fresh, snap_fresh)
                        repo_fresh.insert_metrics(fresh_metrics)
                        
                    st.cache_data.clear()
                    st.cache_resource.clear()
                    st.success(f"העדכון האחרון ({last_run_id}) בוטל והמערכת שוחזרה!")
                    time.sleep(0.5)
                    st.rerun()
                else:
                    conn.close()
                    st.warning("אין עדכונים נוספים לביטול.")
            except Exception as e:
                st.error(f"שגיאה בשחזור: {e}")

    st.markdown("---")
    st.subheader("📊 חיווי סטטוס סדרות נתונים במערכת")
    
    EXPECTED_SERIES = [
        ("TA35", "מדד ת״א־35", "📈 מניות", "קובץ TASE", True),
        ("VTA35", "מדד תנודתיות VTA35", "⚡ תנודתיות", "קובץ TASE", False),
        ("TA_BANKS5", "מדד ת״א בנקים-5", "🏦 מגזרי", "קובץ TASE", False),
        ("TEL_GOV_ALL", "מדד תל גוב-כללי", "🏛️ אג״ח ממשלתי", "קובץ TASE", False),
        ("TEL_BOND60", "מדד תל-בונד 60", "📊 אשראי קונצרני", "קובץ TASE", False),
        ("USDILS", "שער דולר/שקל", "💵 מט״ח", "בנק ישראל (אוטומטי)", False),
        ("VIX", "Cboe VIX", "🇺🇸 מאקרו ארה״ב", "Cboe (אוטומטי)", False),
        ("VIX9D", "Cboe VIX 9-Day", "🇺🇸 מאקרו ארה״ב", "Cboe (אוטומטי)", False),
        ("VIX3M", "Cboe VIX 3-Month", "🇺🇸 מאקרו ארה״ב", "Cboe (אוטומטי)", False),
    ]
    
    health_map = {}
    for sym, _, _, _, _ in EXPECTED_SERIES:
        history = repo.bar_history(sym)
        last = history[-1] if history else None
        health_map[sym] = {
            "observations": len(history),
            "last_date": last.session_date if last else None,
            "source": last.source if last else None,
        }
    
    status_cols = st.columns(3)
    for idx, (sym, name, cat, src_type, is_mandatory) in enumerate(EXPECTED_SERIES):
        h = health_map.get(sym)
        obs_count = h["observations"] if h else 0
        last_date = h["last_date"] if h else None
        is_loaded = obs_count > 0
        last_date_str = f"{last_date:%d/%m/%Y}" if last_date else "טרם נטען"
        obs_count_str = f"{obs_count:,} ימים" if is_loaded else "0 ימים"
        
        with status_cols[idx % 3]:
            if is_loaded:
                badge = "🟢 נטען ופעיל"
                box_bg = "#e8f5e9"
                border_color = "#4caf50"
            else:
                badge = "🔴 חסר (חובה לטרייד)" if is_mandatory else "⚪ טרם הועלה (רשות)"
                box_bg = "#fbe9e7" if is_mandatory else "#f8f9fa"
                border_color = "#f44336" if is_mandatory else "#cfd8dc"
                
            st.markdown(
                f"""
                <div style="background-color: {box_bg}; border: 1.5px solid {border_color}; border-radius: 8px; padding: 12px; margin-bottom: 12px;">
                    <div style="font-weight: bold; font-size: 1.05em; color: #1a237e;">{name} ({sym})</div>
                    <div style="font-size: 0.85em; color: #555;">{cat} · {src_type}</div>
                    <div style="margin-top: 6px; font-size: 0.95em;">סטטוס: <b>{badge}</b></div>
                    <div style="font-size: 0.85em; color: #333; margin-top: 2px;">תאריך אחרון: <b>{last_date_str}</b> ({obs_count_str})</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with st.expander("📋 פירוט טבלת בריאות נתונים מלאה"):
        health_rows = [
            {
                "סדרה": sym,
                "תאריך אחרון": f"{health_map[sym]['last_date']:%d/%m/%Y}" if health_map[sym]["last_date"] else "חסר",
                "מספר תצפיות": health_map[sym]["observations"],
                "מקור": health_map[sym]["source"] or "—",
                "סטטוס": "תקין" if health_map[sym]["observations"] > 0 else "חסר",
            }
            for sym, _, _, _, _ in EXPECTED_SERIES
        ]
        st.dataframe(pd.DataFrame(health_rows), hide_index=True, use_container_width=True)

st.caption(
    "כל המדדים הם כלי תמיכה בלבד. אין במערכת הוראות מסחר, חיבור לחשבון או נתוני זמן אמת."
)
