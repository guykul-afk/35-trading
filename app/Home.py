from __future__ import annotations

import math
import sqlite3
import time

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from ui import bundle, page_header

from decision_ui import render_decision_hero
from ta35_dashboard.analytics import probability_band, recommend_strategy
from ta35_dashboard.analytics.payoff import build_plotly_payoff_chart, generate_strategy_payoff_data
from ta35_dashboard.config import PROJECT_ROOT, SETTINGS
from ta35_dashboard.decision_engine import StrategyRecommendation, TradeTicket
from ta35_dashboard.decision_engine.engine import run_trade_decision_engine
from ta35_dashboard.services import import_tase_uploads
from ta35_dashboard.services.dde_service import analyze_dde_options_data

from ta35_dashboard.analytics.shortterm_strategies import (
    build_shortterm_payoff_fan_chart,
    get_shortterm_recommendation,
)

data = bundle()

# Extract rise probability and spot for DDE initialization
prob_rows_init = [
    row for row in data.family_probabilities if int(row.get("horizon", 0)) in {3, 7, 14}
]
latest_prob_init = 0.50
if prob_rows_init:
    latest_prob_init = float(prob_rows_init[0]["latest_probability"])

last_close_val_init = float(data.ta35_closes[-1]) if data.ta35_closes else 4150.0

dde_result = analyze_dde_options_data(
    uploaded_files=st.session_state.get("dde_file_uploader"),
    spot_override=last_close_val_init,
    prob_rise=latest_prob_init,
)

# Run Trade Decision Engine
decision_result = run_trade_decision_engine(
    spot_price=last_close_val_init,
    prob_up=latest_prob_init,
    forecast_rv=float(data.forecast_volatility) if data.forecast_volatility is not None else 0.15,
    current_rv=float(data.realized_volatility_20d) if getattr(data, "realized_volatility_20d", None) is not None else 0.14,
    regime=getattr(data, "regime", "NORMAL"),
    volatility_state=data.regime_matrix.volatility_state,
    market_state=data.regime_matrix.market_state,
    parsed_chains=dde_result.chains if dde_result and dde_result.chains else None,
)

page_header("מנוע החלטת מסחר ת״א־35 — Trade Decision Engine", data)

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
# TAB 1: THE TRADE — מנוע החלטת המסחר
# -----------------------------------------------------------------------------
with tab_trade:
    render_decision_hero(decision_result, spot_price=last_close_val_init)

# -----------------------------------------------------------------------------
# TAB 2: TRACKING — מעקב
# -----------------------------------------------------------------------------
with tab_track:
    st.subheader("📈 מעקב המלצות וביצועי Shadow Log")
    st.info("כאן נרשמות כל ההמלצות שיוצרו על ידי מנוע ההחלטה למעקב Mark-to-Market ואימות Forward OOS.")

# -----------------------------------------------------------------------------
# TAB 3: MARKET — שוק ומניפה
# -----------------------------------------------------------------------------
with tab_market:
    # 1. מדדי KPI מרכזיים בראש העמוד
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    last_close_val = float(data.ta35_closes[-1]) if data.ta35_closes else None

    kpi1.metric(
        "מדד ת״א־35",
        f"{last_close_val:,.1f}" if last_close_val else "לא זמין",
        help="מחירי סגירה אחרונים של מדד תל אביב 35",
    )

    forecast_val = (
        f"{data.forecast_volatility:.1%}" if data.forecast_volatility is not None else "לא זמין"
    )
    kpi2.metric(
        "תחזית תנודתיות (שנתית)",
        forecast_val,
        help="חציון אומדני התנודתיות הממומשת המשולבים לחישוב מניפת ההסתברות",
    )

    vol_state = data.regime_matrix.volatility_state
    vol_delta = f"{data.regime_matrix.market_state} × {data.regime_matrix.volatility_state}"
    kpi3.metric(
        "צפי תנודתיות משוקלל",
        vol_state,
        delta=f"משטר {data.regime} · {vol_delta}",
        delta_color="normal",
        help="שקלול אינדיקטורי התנודתיות והמשטר (VTA35, Cboe VIX, VRP, אחוזון תנודתיות)",
    )

    prob_rows = [
        row for row in data.family_probabilities if int(row.get("horizon", 0)) in {3, 7, 14}
    ]
    market_state = data.regime_matrix.market_state
    if prob_rows:
        latest_prob = float(prob_rows[0]["latest_probability"])
        prob_axis = "ת״א־35 יעלה"
        market_delta = f"P({prob_axis}) {latest_prob:.1%} · Brier {float(prob_rows[0]['brier']):.3f}"
    elif data.market_trend_score is not None:
        market_delta = f"ניקוד מגמה {data.market_trend_score:+.2f}"
    else:
        market_delta = "Context Only"

    kpi4.metric(
        "צפי מדד משוקלל",
        market_state,
        delta=market_delta,
        delta_color="normal",
        help="שקלול אינדיקטורי המגמה והתחזית ההסתברותית למדד ת״א־35",
    )

    st.markdown("---")

    # 2. המרכז הוויזואלי: מניפת הסתברות מדד ת״א־35
    st.subheader("ת״א־35 — מניפת הסתברות")

    fan_horizon = int(
        st.radio(
            "אופק המניפה (ימי מסחר)",
            options=[3, 7, 14, 30],
            horizontal=True,
            index=2,
            format_func=lambda value: f"{value} ימים",
            key="probability_fan_horizon",
        )
    )

    if data.ta35_dates and data.forecast_volatility is not None:
        last_date = pd.Timestamp(data.ta35_dates[-1])
        last_close = float(data.ta35_closes[-1])
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

        figure = go.Figure()
        history_points = min(90, len(data.ta35_dates))
        figure.add_trace(
            go.Scatter(
                x=data.ta35_dates[-history_points:],
                y=data.ta35_closes[-history_points:],
                mode="lines",
                name="ת״א־35 בפועל",
                line={"color": "#55b5ff", "width": 2},
                hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f}<extra></extra>",
            )
        )
        band_styles = (
            (2.0, "95.4% (±2σ)", "rgba(82, 132, 190, 0.13)"),
            (1.5, "86.6% (±1.5σ)", "rgba(82, 132, 190, 0.22)"),
            (1.0, "68.3% (±1σ)", "rgba(82, 132, 190, 0.36)"),
            (0.5, "38.3% (±0.5σ)", "rgba(82, 132, 190, 0.54)"),
        )
        for sigma, label, fill_color in band_styles:
            figure.add_trace(
                go.Scatter(
                    x=fan["date"],
                    y=fan[f"lower_{sigma}"],
                    mode="lines",
                    line={"width": 0},
                    hoverinfo="skip",
                    showlegend=False,
                )
            )
            figure.add_trace(
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
                        f"{label}<br>%{{x|%d/%m/%Y}}<br>טווח: %{{customdata:,.0f}}–%{{y:,.0f}}"
                        "<extra></extra>"
                    ),
                )
            )
        figure.add_trace(
            go.Scatter(
                x=fan["date"],
                y=fan["center"],
                mode="lines",
                name="מרכז התחזית",
                line={"color": "#f3f6fb", "width": 2, "dash": "dash"},
                hovertemplate="%{x|%d/%m/%Y}<br>%{y:,.0f}<extra></extra>",
            )
        )
        figure.add_vline(
            x=last_date.timestamp() * 1000,
            line_dash="dot",
            line_color="#8b98aa",
        )
        figure.update_layout(
            height=450,
            margin={"l": 10, "r": 10, "t": 20, "b": 10},
            hovermode="x unified",
            legend={"orientation": "h", "y": 1.08, "x": 0},
            xaxis_title="תאריך",
            yaxis_title="נקודות מדד",
        )
        st.plotly_chart(figure, width="stretch")

        summary_rows = []
        for days in (3, 7, 14, 30):
            row = {"טווח": f"{days} ימים"}
            for sigma, label in (
                (0.5, "±0.5σ"),
                (1.0, "±1σ"),
                (1.5, "±1.5σ"),
                (2.0, "±2σ"),
            ):
                band = probability_band(last_close, data.forecast_volatility, days, sigma)
                if band is not None:
                    row[label] = f"{band[0]:,.0f}–{band[1]:,.0f}"
            summary_rows.append(row)
        st.dataframe(pd.DataFrame(summary_rows), hide_index=True, width="stretch")
    else:
        st.info("אין מספיק נתוני ת״א־35 או תחזית תנודתיות להצגת המניפה.")

    st.markdown("---")

    # 3. המלצת אסטרטגיה מרכזית (Single Source of Truth מתוך Trade Decision Engine)
    st.subheader("💡 המלצת אסטרטגיה כללית (מנוע ההחלטה המרכזי)")

    if isinstance(decision_result, StrategyRecommendation):
        primary_name = decision_result.primary_strategy_family.value
        alts_names = [a.value for a in decision_result.alternatives]
        dir_view_str = decision_result.direction_view
        vol_view_str = decision_result.volatility_view
        rationale_str = decision_result.rationale
        h_days = decision_result.horizon_days
        confidence_str = f"{decision_result.forecast_confidence:.0%}"
        est_legs = decision_result.estimated_legs
    elif isinstance(decision_result, TradeTicket):
        primary_name = decision_result.strategy_family.value
        alts_names = []
        dir_view_str = f"שורי (P_up: {decision_result.model_direction_probability:.1%})"
        vol_view_str = f"צפי RV: {decision_result.forecast_rv:.1%}"
        rationale_str = f"מבנה נבחר עם ציון הזדמנות {decision_result.opportunity_score}/100"
        h_days = decision_result.horizon_days
        confidence_str = f"{decision_result.forecast_confidence:.0%}"
        est_legs = tuple({"option_type": l.option_type, "action": l.action, "estimated_strike": l.strike, "ratio": l.ratio, "label": f"{l.action} {l.option_type}"} for l in decision_result.legs)
    else:
        primary_name = "Bull Put Spread"
        alts_names = []
        dir_view_str = "שורי"
        vol_view_str = "מתכווצת"
        rationale_str = "תזת שוק שורית עם ציפייה לירידת תנודתיות"
        h_days = 7
        confidence_str = "80%"
        est_legs = ()

    strat1, strat2, strat3, strat4 = st.columns(4)
    strat1.metric("מבנה עיקרי", primary_name)
    strat2.metric("אופק מוצע", f"{h_days} ימי מסחר")
    strat3.metric("כיוון שוק", dir_view_str)
    strat4.metric("צפי תנודתיות", vol_view_str)

    st.info(f"**נימוק אסטרטגיה מועדפת (Trade Decision Engine):** {rationale_str}")
    if alts_names:
        st.caption(f"**חלופות מועמדות:** {', '.join(alts_names)}")

    with st.expander("🎯 מפת סטרייקים מומלצת ופרופיל Payoff בפקיעה (Trade Decision Engine)", expanded=True):
        if est_legs:
            spot_val = last_close_val_init
            leg_rows = []
            payoff_legs = []
            for leg in est_legs:
                strike_val = leg.get("estimated_strike", spot_val)
                dist_pct = (strike_val - spot_val) / spot_val if spot_val and strike_val else 0.0
                act = leg.get("action", "BUY")
                opt = leg.get("option_type", "CALL")
                leg_rows.append({
                    "תיאור רגל": leg.get("label", f"{act} {opt}"),
                    "פעולה": "קנייה (Buy)" if act in ("BUY", "Buy") else "מכירה (Sell)",
                    "סוג אופציה": opt,
                    "סטרייק": strike_val,
                    "כמות": f"{leg.get('ratio', 1)}x",
                    "מרחק מהמדד": f"{dist_pct:+.1%}" if spot_val else "—",
                })
                payoff_legs.append({
                    "action": act,
                    "option_type": opt,
                    "strike": strike_val,
                    "quantity": leg.get("ratio", 1),
                    "label": leg.get("label", f"{act} {opt}"),
                })

            st.dataframe(pd.DataFrame(leg_rows), hide_index=True, width="stretch")

            vol_val = float(data.forecast_volatility) if data.forecast_volatility is not None else 0.15
            payoff_data = generate_strategy_payoff_data(
                spot=spot_val,
                forecast_volatility=vol_val,
                horizon_days=h_days,
                legs=payoff_legs,
            )
            fig = build_plotly_payoff_chart(
                payoff_data,
                title=f"פרופיל Payoff בפקיעה — {primary_name}",
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("אין נתונים מספיקים לגזירת מפת סטרייקים מוצעת.")

    st.markdown("---")

    # 4. נתוני אופציות DDE בזמן אמת, צפי 1/3/7/14 ימים והמלצות אסטרטגיה
    st.subheader("⚡ נתוני אופציות DDE בזמן אמת — צפי 1 / 3 / 7 / 14 ימים והמלצות בלייב")

    col_up, col_ref = st.columns([1.5, 1.0])
    with col_up:
        uploaded_dde = st.file_uploader(
            "העלאת קבצי DDE/אופציות מעודכנים (UTF-16LE / TSV)",
            type=["txt", "csv", "tsv"],
            accept_multiple_files=True,
            help="ניתן להעלות קבצים מעודכנים או לשמור קבצי DDE בתיקיית הפרויקט. המערכת מזהה אותם אוטומטית.",
            key="dde_file_uploader",
        )
    with col_ref:
        st.markdown("<br>", unsafe_allow_html=True)
        auto_refresh = st.checkbox("🔄 רענון אוטומטי בלייב (כל 30 שניות)", value=False, key="dde_auto_refresh")

    # Track active scan time
    current_time_str = time.strftime("%H:%M:%S")
    st.session_state["last_scan_time"] = current_time_str

    # dde_result is already computed globally at the top of the script

    # Detect if file changed since last script run
    if "prev_mtime" not in st.session_state:
        st.session_state["prev_mtime"] = dde_result.last_modified_str
        st.session_state["update_count"] = 0
    elif st.session_state["prev_mtime"] != dde_result.last_modified_str:
        st.session_state["prev_mtime"] = dde_result.last_modified_str
        st.session_state["update_count"] += 1
        st.toast(f"🔔 קובץ DDE עודכן! (עדכון מס' {st.session_state['update_count']})")

    if dde_result.source_files:
        # Check if file has changed in the last 1 minute
        import datetime as dt_module
        is_recent = False
        try:
            mtime_part = dde_result.last_modified_str.split()[0]
            m_h, m_m, m_s = map(int, mtime_part.split(':'))
            now_dt = dt_module.datetime.now()
            file_dt = now_dt.replace(hour=m_h, minute=m_m, second=m_s)
            time_diff = (now_dt - file_dt).total_seconds()
            if time_diff < 0:
                time_diff += 86400
            is_recent = time_diff < 30
        except Exception:
            pass

        if is_recent:
            st.success(f"🟢 **הסורק פעיל:** הנתונים השתנו ועודכנו בהצלחה! · **עדכון אחרון בקובץ:** {dde_result.last_modified_str} · **סריקה אחרונה:** {current_time_str}")
        else:
            st.warning(f"🟡 **הסורק פעיל ומחפש שינויים...** · **סריקה אחרונה:** {current_time_str} · קובץ ה-DDE בדיסק לא השתנה מאז **{dde_result.last_modified_str}** · ⚪ לא זוהה שינוי בנתונים בסריקה האחרונה (הנתונים זהים לציטוט הקודם).")

        col_dde1, col_dde2 = st.columns([1.2, 0.8])
        with col_dde1:
            st.markdown("##### 📈 צפי תנודתיות משתמעת וטווחים (IV Term Structure)")
            exp_table = []
            for h, exp in dde_result.expectations.items():
                exp_table.append({
                    "אופק צפי": f"{h} ימי מסחר",
                    "תנודתיות משתמעת (IV)": f"{exp.implied_volatility:.2%}",
                    "תנודה צפויה (±1σ)": f"±{exp.one_sigma_move:.1f} נק'",
                    "טווח מדד צפוי (68%)": f"{exp.lower_1s:,.0f} – {exp.upper_1s:,.0f}",
                    "טווח מדד רחב (95%)": f"{exp.lower_2s:,.0f} – {exp.upper_2s:,.0f}",
                })
            st.dataframe(pd.DataFrame(exp_table), hide_index=True, width="stretch")

        with col_dde2:
            st.markdown("##### 🎯 נתוני אופציות גלומים")
            st.metric("מחיר מדד/נכס בסיס בשימוש", f"{dde_result.spot_price:,.1f}")
            if dde_result.synthetic_spot:
                st.metric("חוזה סינטטי גלום (Synthetics)", f"{dde_result.synthetic_spot:,.1f}")
            
            st.markdown("##### 📅 פקיעות פעילות שזוהו:")
            for chain in dde_result.chains:
                st.caption(f"· **{chain.expiration_label}** — {chain.days_to_expiration:.1f} ימים לפקיעה ({len(chain.quotes)} סטרייקים)")

        st.markdown("##### 💡 הצעות אסטרטגיה בזמן אמת (תמחור ציטוטי שוק חים - Bid/Ask)")
        if dde_result.realtime_proposals:
            for prop in dde_result.realtime_proposals:
                with st.expander(f"📌 {prop.strategy_name} — תוחלת רווח: {prop.expected_value_nis:+.0f} ש״ח", expanded=True):
                    pcol1, pcol2, pcol3, pcol4 = st.columns(4)
                    pcol1.metric("זיכוי/חיוב נטו", f"{prop.net_credit_debit_nis:+.0f} ש״ח", help="חיובי = זיכוי נטו (Net Credit), שלילי = חיוב נטו (Net Debit)")
                    pcol2.metric("רווח מרבי", f"{prop.max_profit_nis:,.0f} ש״ח" if prop.max_profit_nis != float('inf') else "בלתי מוגבל")
                    pcol3.metric("הפסד מרבי", f"{prop.max_loss_nis:,.0f} ש״ח")
                    pcol4.metric("סיכוי הצלחה (PoP)", f"{prop.probability_of_profit:.1%}")

                    st.write(f"**הסבר:** {prop.rationale}")
                    st.caption(f"נקודות איזון (Breakeven): {', '.join([f'{be:,.1f}' for be in prop.breakeven_points])} נקודות | סטטוס: {prop.quality_label}")

                    st.markdown("**פירוט רגלי העסקה בזמן אמת:**")
                    leg_data = []
                    for leg in prop.legs:
                        leg_data.append({
                            "פעולה": "קנייה (Buy)" if leg.action == "Buy" else "מכירה (Sell)",
                            "סוג": leg.option_type,
                            "מחיר מימוש": leg.strike,
                            "מחיר ביצוע (ש״ח)": f"{leg.exec_price * 100:,.0f} ש״ח",
                            "מחיר בנקודות": f"{leg.exec_price:.2f} נק'",
                            "תיאור רגל": leg.label,
                        })
                    st.dataframe(pd.DataFrame(leg_data), hide_index=True, width="stretch")
        if dde_result.calendar_proposals:
            with st.expander("⏳ אסטרטגיות מרווחי זמן בין פקיעות (Calendar Spreads & Time Skew Arbitrage)", expanded=True):
                st.caption("בדיקת תמחור מרווחי זמן בזמן אמת: מכירת אופציה שבועית לפקיעה קרובה כנגד קניית אופציה חודשית בסטרייק זהה לניצול שחיקת זמן מואצת (Theta Decay) והפרשי תנודתיות גלומה (IV Skew).")
                cal_rows = []
                for cal in dde_result.calendar_proposals[:8]:
                    cal_rows.append({
                        "אסטרטגיה": cal.strategy_name,
                        "סטרייק": f"{cal.strike:,.0f}",
                        "סוג אופציה": cal.option_type,
                        "עלות נטו (ש״ח)": f"{cal.net_debit_nis:,.0f} ש״ח",
                        "עלות בנקודות": f"{cal.net_debit_pts:.2f} נק'",
                        "רווח מרבי משוער (ש״ח)": f"{cal.estimated_max_profit_nis:,.0f} ש״ח",
                        "יתרון שחיקת זמן (Theta)": f"{cal.time_decay_ratio:.1f}x",
                        "נימוק תמחור בלייב": cal.rationale,
                    })
                st.dataframe(pd.DataFrame(cal_rows), hide_index=True, width="stretch")
        else:
            st.info("לא נמצאו מרווחי זמן זמינים בין הפקיעות השונות בנתוני ה-DDE.")
            
        st.markdown("---")
        st.subheader("⚖️ ארביטראז' תנודתיות (Volatility Arbitrage) מול ציפיות מודל")
        st.caption("השוואה בין עלות אוכף/פרפר בפועל (Bid/Ask ביצועי) לבין תוחלת התנודתיות המשוקללת של המערכת, לאיתור תמחור חסר/יתר בשוק.")
        
        if dde_result.chains and data.forecast_volatility:
            from ta35_dashboard.analytics.realtime_strategies import analyze_volatility_arbitrage
            
            all_vol_proposals = []
            for c in dde_result.chains:
                proposals = analyze_volatility_arbitrage(
                    chain=c,
                    spot_price=dde_result.spot_price,
                    expected_vol=data.forecast_volatility,
                )
                all_vol_proposals.extend(proposals)
                
            if all_vol_proposals:
                vol_rows = []
                for vp in all_vol_proposals:
                    vol_rows.append({
                        "אסטרטגיה (סטרייקים)": vp.strategy_name,
                        "ימים לפקיעה": f"{vp.expiration_days:.0f} ימים",
                        "מחיר ביצוע (שוק)": f"{vp.market_price_pts:.2f} נק'",
                        "מחיר הוגן (מודל)": f"{vp.theoretical_price_pts:.2f} נק'",
                        "פער (Edge)": f"{vp.gap_pct:+.1%}",
                        "המלצה": "🟢 Buy (זול)" if vp.recommendation == "Buy" else "🔴 Sell (יקר)"
                    })
                st.dataframe(pd.DataFrame(vol_rows), hide_index=True, width="stretch")
            else:
                st.info("לא אותרו פערי ארביטראז' משמעותיים (>5%) מול תנודתיות המודל.")
        else:
            st.info("חסרים נתוני שרשראות אופציות או תחזית תנודתיות לביצוע אנליזת Vol-Arb.")
            
    else:
        st.info(dde_result.status_message)

    if auto_refresh:
        time.sleep(30)
        st.rerun()

    st.markdown("---")

    # 5. גרפי היסטוריית TA-35 ו-VTA35
    hist_left, hist_right = st.columns(2)
    with hist_left:
        st.subheader("ת״א־35 — 252 ימי נתונים")
        if data.ta35_dates:
            st.line_chart(pd.DataFrame({"ת״א־35": data.ta35_closes}, index=data.ta35_dates))
    with hist_right:
        st.subheader("VTA35 — תנודתיות גלומה")
        if data.vta35_dates:
            figure = go.Figure(
                go.Scatter(x=data.vta35_dates, y=data.vta35_values, name="VTA35")
            )
            figure.update_layout(
                height=350,
                margin={"l": 10, "r": 10, "t": 10, "b": 10},
                yaxis_title="אחוזים",
            )
            st.plotly_chart(figure, width="stretch")
        else:
            st.info("VTA35 חסר; מדדי VRP ואחוזון לא יחושבו.")

# -----------------------------------------------------------------------------
# TAB 4: RESEARCH — מחקר, אינדיקטורים ו-EOD
# -----------------------------------------------------------------------------
with tab_research:
    st.subheader("⚡ טריידים קצרי טווח (1 ו-3 ימי מסחר)")
    st.subheader("⚡ המלצות לטריידים קצרי טווח (1 ו-3 ימי מסחר) לאור נתוני ה-DDE")
    st.caption("תצוגת מנהלים נקייה: ניתוח מילולי מפורט ונימוקי מסחר, ללא שרשרת אופציות עמוסה, בתוספת גרף Payoff משולב מניפת הסתברות.")

    st_horizon = int(
        st.radio(
            "בחירת אופק הטרייד הקצר:",
            options=[1, 3],
            horizontal=True,
            index=0,
            format_func=lambda v: f"{v} יום מסחר ({'פקיעה שבועית / יום קדימה' if v==1 else '3 ימים קדימה'})",
            key="shortterm_horizon_choice",
        )
    )

    st_dde_res = analyze_dde_options_data(
        spot_override=last_close_val,
        prob_rise=latest_prob if 'latest_prob' in locals() else 0.50,
    )

    if st_dde_res.weekly_chain or st_dde_res.monthly_chain:
        exp_h = st_dde_res.expectations.get(st_horizon)
        iv_val = exp_h.implied_volatility if exp_h else 0.15

        proposal, rationale = get_shortterm_recommendation(
            weekly_chain=st_dde_res.weekly_chain,
            monthly_chain=st_dde_res.monthly_chain,
            spot_price=st_dde_res.spot_price,
            horizon_days=st_horizon,
            prob_rise=latest_prob if 'latest_prob' in locals() else 0.50,
            implied_vol=iv_val,
        )

        if proposal and exp_h:
            st.markdown(f"### 📌 הטרייד המומלץ: **{proposal.strategy_name}**")

            # כרטיסי תמצית מנהלים
            sc1, sc2, sc3, sc4, sc5 = st.columns(5)
            sc1.metric("זיכוי/חיוב נטו", f"{proposal.net_credit_debit_nis:+.0f} ש״ח", help="חיובי = Net Credit, שלילי = Net Debit")
            sc2.metric("רווח מרבי", f"{proposal.max_profit_nis:,.0f} ש״ח" if proposal.max_profit_nis != float('inf') else "בלתי מוגבל")
            sc3.metric("הפסד מרבי", f"{proposal.max_loss_nis:,.0f} ש״ח")
            sc4.metric("סיכוי הצלחה (PoP)", f"{proposal.probability_of_profit:.1%}")
            sc5.metric("תוחלת רווח ($EV$)", f"{proposal.expected_value_nis:+.0f} ש״ח", help="תוחלת מתמטית משוקללת סיכון")

            st.markdown("---")

            # מלל ניתוח ונימוקי מסחר מפורטים
            col_info1, col_info2 = st.columns([1.1, 0.9])
            with col_info1:
                st.markdown("##### 📝 ניתוח מילולי וסיבות להמלצה")
                st.markdown(rationale)
                st.caption(f"נקודות איזון בפקיעה (Breakeven): **{', '.join([f'{be:,.1f}' for be in proposal.breakeven_points])}** נקודות")

            with col_info2:
                st.markdown("##### 🛒 רגלי הטרייד לביצוע")
                leg_rows = []
                for leg in proposal.legs:
                    leg_rows.append({
                        "פעולה": "קנייה (Buy)" if leg.action == "Buy" else "מכירה (Sell)",
                        "סוג אופציה": leg.option_type,
                        "סטרייק": f"{leg.strike:,.0f}",
                        "מחיר ביצוע (ש״ח)": f"{leg.exec_price * 50:,.0f} ש״ח",
                        "מחיר בנקודות": f"{leg.exec_price:.2f} נק'",
                    })
                st.dataframe(pd.DataFrame(leg_rows), hide_index=True, use_container_width=True)

            st.markdown("---")

            # הגרף המשולב: Payoff + מניפת הסתברות
            st.markdown("##### 📊 תרשים Payoff בפקיעה משולב מניפת הסתברות (Live DDE Volatility)")
            fig_st = build_shortterm_payoff_fan_chart(
                proposal=proposal,
                horizon_exp=exp_h,
                spot_price=st_dde_res.spot_price,
                multiplier=50.0,
            )
            st.plotly_chart(fig_st, use_container_width=True)

            if st_dde_res.calendar_proposals:
                with st.expander("⏳ הזדמנויות תמחור במרווחי זמן (Calendar Spreads — שבועית מול חודשית)", expanded=False):
                    st.caption("מכירת אופציות שבועיות (שחיקת Theta מואצת) כנגד קניית אופציות חודשיות בסטרייק זהה.")
                    st_cal_rows = []
                    for cal in st_dde_res.calendar_proposals[:6]:
                        st_cal_rows.append({
                            "אסטרטגיה": cal.strategy_name,
                            "סטרייק": f"{cal.strike:,.0f}",
                            "סוג אופציה": cal.option_type,
                            "עלות נטו (ש״ח)": f"{cal.net_debit_nis:,.0f} ש״ח",
                            "עלות בנקודות": f"{cal.net_debit_pts:.2f} נק'",
                            "יתרון שחיקה (Theta)": f"{cal.time_decay_ratio:.1f}x",
                        })
                    st.dataframe(pd.DataFrame(st_cal_rows), hide_index=True, use_container_width=True)
        else:
            st.warning(rationale)
    else:
        st.info("אין נתוני אופציות DDE זמינים. אנא ודא כי קבצי ה-DDE קיימים בתיקיית הפרויקט.")

    st.markdown("---")
    st.subheader("📊 אינדיקטורים טכניים ומדדי תנודתיות (סוף-יום)")
    strength_horizon = int(
        st.radio(
            "אופק מדדי העוצמה (ימי מסחר)",
            options=[3, 7, 14, 30],
            horizontal=True,
            index=2,
            format_func=lambda value: f"{value} ימים",
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

                if card.key == "forecast_rv_3d":
                    card_label = f"תחזית RV ל־{strength_horizon} ימים"
                elif card.key == "expected_move_3d_points":
                    card_label = f"טווח {strength_horizon} ימים"
                    if last_close_val is not None and data.forecast_volatility is not None:
                        card_val = last_close_val * data.forecast_volatility * math.sqrt(strength_horizon / 252.0)
                elif card.key == "har_rv_3d":
                    card_label = f"HAR-EOD ל־{strength_horizon} ימים"
                elif card.key == "matched_vrp_3d":
                    card_label = f"VRP מותאם ({strength_horizon} ימים)"

                display = (
                    "לא זמין" if card_val is None else format(card_val, card.format)
                )
                vol_result = data.backtest.indicator(
                    card.key, strength_horizon, "volatility", card.volatility_arrow
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

    st.markdown("---")
    st.subheader("🔬 מחקר, כיווניות ודוחות OOS")

    # מטריצת משטר ומדדי כיוון
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

    with st.expander("מטריצת המשטר המלאה (3×3)", expanded=True):
        st.dataframe(pd.DataFrame(matrix_rows), hide_index=True, width="stretch")

    state_left, state_right = st.columns(2)
    vol_score = (
        "לא זמין"
        if data.volatility_direction_score is None
        else f"{data.volatility_direction_score:+.0%}"
    )
    trend_score = (
        "לא זמין" if data.market_trend_score is None else f"{data.market_trend_score:+.0%}"
    )
    state_left.metric("כיוון התנודתיות", data.volatility_direction, delta=vol_score)
    state_right.metric("מצב מגמת ת״א־35", data.market_trend, delta=trend_score)

    evidence = data.premium_evidence
    with st.expander("כרטיס ראיות ושער זכאות למכירת פרמיה", expanded=True):
        e1, e2, e3, e4 = st.columns(4)
        e1.metric("סטטוס", evidence.status)
        e2.metric("n אפקטיבי", evidence.n_eff)
        e3.metric("Lift OOS", "—" if evidence.lift is None else f"{evidence.lift:+.1%}")
        e4.metric("FDR q", "—" if evidence.fdr_q is None else f"{evidence.fdr_q:.3f}")

    with st.expander("תוצאות Backtest — כל האינדיקטורים והאסטרטגיות", expanded=True):
        report = data.backtest
        tested_range = (
            f"{report.start_date:%d/%m/%Y}–{report.end_date:%d/%m/%Y}"
            if report.start_date and report.end_date
            else "לא זמין"
        )
        st.caption(
            f"בדיקה walk-forward ללא שימוש בנתונים עתידיים · "
            f"{report.ta35_observations:,} ימי ת״א־35 · {tested_range}."
        )
        tested_horizon = strength_horizon
        indicator_rows = []
        for card in data.cards:
            vol_result = report.indicator(
                card.key, tested_horizon, "volatility", card.volatility_arrow
            )
            market_result = report.indicator(
                card.key, tested_horizon, "market", card.market_arrow
            )
            card_label = card.label
            if card.key == "forecast_rv_3d":
                card_label = f"תחזית RV ל־{tested_horizon} ימים"
            elif card.key == "expected_move_3d_points":
                card_label = f"טווח {tested_horizon} ימים"
            elif card.key == "har_rv_3d":
                card_label = f"HAR-EOD ל־{tested_horizon} ימים"
            elif card.key == "matched_vrp_3d":
                card_label = f"VRP מותאם ({tested_horizon} ימים)"

            indicator_rows.append(
                {
                    "אינדיקטור": card_label,
                    "חץ תנודתיות": card.volatility_arrow,
                    "דיוק תנודתיות": (
                        f"{vol_result.hit_rate:.1%}"
                        if vol_result and vol_result.hit_rate is not None
                        else "—"
                    ),
                    "n תנודתיות": vol_result.observations if vol_result else 0,
                    "חץ ת״א־35": card.market_arrow,
                    "דיוק ת״א־35": (
                        f"{market_result.hit_rate:.1%}"
                        if market_result and market_result.hit_rate is not None
                        else "—"
                    ),
                    "n ת״א־35": market_result.observations if market_result else 0,
                }
            )
        st.dataframe(pd.DataFrame(indicator_rows), hide_index=True, width="stretch")

    with st.expander("Ablation OOS — מט״ח–מניות ומתאם TA35–VTA35", expanded=False):
        if data.context_ablation:
            st.dataframe(pd.DataFrame(data.context_ablation), hide_index=True, width="stretch")
        else:
            st.info("אין מדגם מספיק לבדיקת התרומה השולית.")

    with st.expander("השוואת מודלי תנודתיות OOS — QLIKE ו־MSE", expanded=False):
        if data.volatility_model_comparison:
            model_frame = pd.DataFrame(data.volatility_model_comparison)
            selected_columns = [
                "horizon",
                "model",
                "n_eff",
                "qlike",
                "mse_variance",
                "qlike_improvement_vs_naive",
                "block_bootstrap_p",
            ]
            st.dataframe(model_frame[selected_columns], hide_index=True, width="stretch")

# -----------------------------------------------------------------------------
# TAB 4: DATA & HEALTH — עדכון נתונים ובריאות המערכת
# -----------------------------------------------------------------------------
with tab_data:
    st.subheader("⚙️ עדכון נתונים וסנכרון כל סדרות המערכת")
    st.write(
        "העלאת קובץ ת״א־35 מעדכנת את נתוני הבורסה בת״א ומסנכרנת אוטומטית את כל מקורות המידע במערכת: "
        "ת״א־35, VTA35, מדדי VIX מארה״ב (Cboe) ושער דולר (USD/ILS)."
    )
    link_left, link_right = st.columns(2)
    link_left.link_button(
        "הורדת ת״א־35 מאתר הבורסה",
        "https://market.tase.co.il/en/market_data/index/142/historical_data/eod",
        width="stretch",
    )
    link_right.link_button(
        "הורדת VTA35 מאתר הבורסה",
        "https://market.tase.co.il/en/market_data/index/598/historical_data/eod",
        width="stretch",
    )

    with st.form("tase_csv_upload", clear_on_submit=True):
        upload_left, upload_right = st.columns(2)
        ta35_file = upload_left.file_uploader(
            "קובץ ת״א־35 (חובה)", type=("csv",), key="ta35_csv"
        )
        vta35_file = upload_right.file_uploader(
            "קובץ VTA35 (רשות)", type=("csv",), key="vta35_csv"
        )
        submitted = st.form_submit_button(
            "בדיקה ועדכון כל מקורות הנתונים", type="primary", width="stretch"
        )
    if submitted:
        if ta35_file is None:
            st.error("יש לבחור קובץ ת״א־35 לפני העדכון.")
        else:
            payloads = {"TA35": ta35_file.getvalue()}
            if vta35_file is not None:
                payloads["VTA35"] = vta35_file.getvalue()
            try:
                with st.spinner("בודק את הקבצים ומסנכרן את כל סדרות הנתונים במערכת…"):
                    result = import_tase_uploads(
                        SETTINGS.database_path, PROJECT_ROOT / "downloads", payloads
                    )
            except (OSError, RuntimeError, ValueError, sqlite3.Error) as error:
                st.error(f"העדכון לא בוצע: {error}")
            else:
                details = " · ".join(
                    f"{symbol}: {result.observations[symbol]:,} ימים חדשים יובאו עד "
                    f"{result.latest_dates[symbol]:%d/%m/%Y}"
                    for symbol in result.observations
                )
                st.success(f"הנתונים עודכנו בהצלחה עבור כל המקורות! {details}")
                st.rerun()

    st.markdown("---")
    st.subheader("בריאות סדרות הנתונים במערכת")
    health_rows = [
        {
            "סדרה": item.symbol,
            "תאריך אחרון": f"{item.last_date:%d/%m/%Y}" if item.last_date else "חסר",
            "מספר תצפיות": item.observations,
            "מקור": item.source or "—",
            "סטטוס": item.status,
        }
        for item in data.health
    ]
    st.dataframe(pd.DataFrame(health_rows), hide_index=True, width="stretch")

st.caption(
    "כל המדדים הם כלי תמיכה בלבד. אין במערכת הוראות מסחר, חיבור לחשבון או נתוני זמן אמת."
)
