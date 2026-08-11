from __future__ import annotations

import sqlite3

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from ui import bundle, page_header

from ta35_dashboard.analytics import probability_band, recommend_strategy
from ta35_dashboard.config import PROJECT_ROOT, SETTINGS
from ta35_dashboard.services import import_tase_uploads

data = bundle()
page_header("דשבורד תנודתיות ת״א־35 — Lite", data)

# יצירת חלוקת הטאבים המרכזית
tab_hero, tab_indicators, tab_research, tab_data = st.tabs(
    [
        "🎯 תחזית, מניפה ואסטרטגיה",
        "📊 אינדיקטורים מורחבים",
        "🔬 מחקר ו-Backtest",
        "⚙️ עדכון נתונים",
    ]
)

# -----------------------------------------------------------------------------
# TAB 1: HERO VIEW — תחזית, מניפה ואסטרטגיה
# -----------------------------------------------------------------------------
with tab_hero:
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

    colors = {"רגוע": "green", "רגיל": "blue", "זהירות": "orange", "לחץ גבוה": "red"}
    regime_color = colors.get(data.regime, "gray")
    kpi3.metric(
        "משטר שוק",
        data.regime,
        delta=f"{data.regime_matrix.market_state} × {data.regime_matrix.volatility_state}",
        delta_color="normal",
        help="מטריצת משטר שוק ומגמה נוכחית",
    )

    prob_rows = [
        row for row in data.family_probabilities if int(row.get("horizon", 0)) in {3, 7, 14}
    ]
    if prob_rows:
        latest_prob = float(prob_rows[0]["latest_probability"])
        prob_axis = "RV יעלה" if prob_rows[0]["axis"] == "volatility" else "ת״א־35 יעלה"
        kpi4.metric(
            f"P({prob_axis}) · {int(prob_rows[0]['horizon'])}d",
            f"{latest_prob:.1%}",
            delta=f"Brier {float(prob_rows[0]['brier']):.3f}",
            help="תחזית מודל הסתברותי Ridge לאחור",
        )
    else:
        kpi4.metric("P(תחזית הסתברותית)", "Context Only")

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

    # 3. המלצת אסטרטגיה
    st.subheader("💡 המלצת אסטרטגיה כללית")
    horizon = int(
        st.radio(
            "אופק האסטרטגיה (ימי מסחר)",
            options=[3, 7, 14, 30],
            horizontal=True,
            index=2,
            format_func=lambda value: f"{value} ימים",
            key="strategy_horizon",
        )
    )
    recommendation = recommend_strategy(
        spot=float(data.ta35_closes[-1]) if data.ta35_closes else None,
        forecast_volatility=data.forecast_volatility,
        implied_volatility=data.implied_volatility,
        trend_score=data.market_trend_score,
        volatility_score=data.volatility_direction_score,
        regime=data.regime,
        horizon_days=horizon,
        premium_sale_eligible=data.premium_evidence.eligible,
    )

    strategy_history = (
        data.backtest.strategy(recommendation.primary.name, horizon)
        if recommendation.primary
        else None
    )
    strat1, strat2, strat3, strat4 = st.columns(4)
    strat1.metric(
        "מבנה עיקרי",
        recommendation.primary.name if recommendation.primary else recommendation.status,
    )
    strat2.metric("אופק מוצע", f"{recommendation.horizon_days} ימי מסחר")
    strat3.metric("תמחור תנודתיות", recommendation.pricing_view)
    strat4.metric(
        "סטטוס ולידציה",
        "Context only",
        delta=(
            f"{strategy_history.observations} מקרים"
            if strategy_history and strategy_history.observations
            else "אין מדגם"
        ),
    )
    if recommendation.primary:
        st.info(f"**{recommendation.status}:** {recommendation.explanation}")
    else:
        st.warning(f"**{recommendation.status}:** {recommendation.explanation}")

    st.markdown("**מפת התאמת תרחיש — אינה payoff או תחזית רווח/הפסד**")
    st.dataframe(

        pd.DataFrame(
            recommendation.scenario_fit,
            columns=["ממד", "מצב נוכחי", "התאמה"],
        ),
        hide_index=True,
        width="stretch",
    )

    with st.expander("למה האסטרטגיה מתאימה ומהן החלופות", expanded=False):
        st.markdown(
            f"**מצב שוק:** {recommendation.market_view} · "
            f"**תנודתיות:** {recommendation.volatility_view} · "
            f"**תמחור:** {recommendation.pricing_view}"
        )
        if recommendation.primary:
            st.markdown(f"**מבנה עיקרי — {recommendation.primary.name}**")
            st.write(recommendation.primary.rationale)
            st.warning(recommendation.primary.risk_note)
        if recommendation.alternatives:
            st.markdown("**חלופות אפשריות**")
            for candidate in recommendation.alternatives:
                st.markdown(f"- **{candidate.name}:** {candidate.rationale}")
        st.markdown("**מגבלות**")
        for warning in recommendation.warnings:
            st.markdown(f"- {warning}")

    st.markdown("---")

    # 4. גרפי היסטוריית TA-35 ו-VTA35
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
# TAB 2: INDICATORS — אינדיקטורים מורחבים
# -----------------------------------------------------------------------------
with tab_indicators:
    st.subheader("📊 אינדיקטורים טכניים ומדדי תנודתיות")
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
                display = (
                    "לא זמין" if card.value is None else format(card.value, card.format)
                )
                vol_result = data.backtest.indicator(
                    card.key, strength_horizon, "volatility", card.volatility_arrow
                )
                column.metric(
                    card.label,
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

# -----------------------------------------------------------------------------
# TAB 3: RESEARCH & BACKTEST — מחקר ו-Backtest
# -----------------------------------------------------------------------------
with tab_research:
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
            indicator_rows.append(
                {
                    "אינדיקטור": card.label,
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
    st.subheader("⚙️ עדכון נתונים מבורסת תל אביב")
    st.write(
        "הורד מהבורסה קובץ סוף־יום לטווח של 3 שנים, ולאחר מכן העלה אותו כאן. "
        "VTA35 אופציונלי אך מומלץ למדדי התנודתיות הגלומה."
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
            "בדיקה ועדכון הנתונים", type="primary", width="stretch"
        )
    if submitted:
        if ta35_file is None:
            st.error("יש לבחור קובץ ת״א־35 לפני העדכון.")
        else:
            payloads = {"TA35": ta35_file.getvalue()}
            if vta35_file is not None:
                payloads["VTA35"] = vta35_file.getvalue()
            try:
                with st.spinner("בודק את הקבצים ומעדכן את מסד הנתונים…"):
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
                st.success(f"הנתונים עודכנו בהצלחה. {details}")
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
