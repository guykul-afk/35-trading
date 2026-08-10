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

colors = {"רגוע": "green", "רגיל": "blue", "זהירות": "orange", "לחץ גבוה": "red"}
st.markdown(f"### משטר שוק: :{colors.get(data.regime, 'gray')}[{data.regime}]")
st.caption(
    f"מטריצת משטר 3×3: **{data.regime_matrix.market_state} × "
    f"{data.regime_matrix.volatility_state}**"
)
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
with st.expander("מטריצת המשטר המלאה", expanded=False):
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
state_left.metric(
    "כיוון התנודתיות",
    data.volatility_direction,
    delta=vol_score,
    help=(
        "סיכום שווה־משקל של ששת מדדי התנודתיות החדשים. הטווח הוא ‎−100% "
        "(רוב המדדים מצביעים על התכווצות) עד ‎+100% (התרחבות). זהו מדד מצב, "
        "לא תחזית ודאית."
    ),
)
state_right.metric(
    "מצב מגמת ת״א־35",
    data.market_trend,
    delta=trend_score,
    help=(
        "סיכום שווה־משקל של המחיר מול ממוצעי 20/60 יום, תשואות 5/20 יום "
        "והמיקום בטווח 20 יום. הטווח ‎−100% עד ‎+100%; זהו תיאור מגמה ולא "
        "אות קנייה או מכירה."
    ),
)

st.subheader("המלצת אסטרטגיה כללית")
st.caption(
    "בחירת משפחת אסטרטגיה לפי מצב המגמה, התנודתיות והתמחור היחסי. "
    "המערכת אינה בוחרת סטרייקים, פרמיות או הוראת ביצוע."
)
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
strategy_left, strategy_middle, strategy_right, strategy_test = st.columns(4)
strategy_left.metric(
    "מבנה עיקרי",
    recommendation.primary.name if recommendation.primary else recommendation.status,
)
strategy_middle.metric("אופק מוצע", f"{recommendation.horizon_days} ימי מסחר")
strategy_right.metric("תמחור תנודתיות", recommendation.pricing_view)
strategy_test.metric(
    "עוצמת תרחיש ב־backtest",
    f"{strategy_history.strength}/10" if strategy_history else "לא זמין",
    delta=(
        f"{strategy_history.observations} מקרים"
        if strategy_history and strategy_history.observations
        else "אין מדגם"
    ),
    help=(
        "מדד מכווץ של הצלחת תרחיש השוק שהמבנה מחפש. "
        "זהו proxy ולא תשואת אופציות, משום שאין במסד שרשרת אופציות היסטורית."
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
st.caption(
    "המפה מתארת התאמה איכותית של משפחת אסטרטגיה למצב השוק. "
    "היא אינה כוללת פרמיות, Greeks, נקודות איזון או P&L."
)

evidence = data.premium_evidence
with st.expander("כרטיס ראיות ושער זכאות למכירת פרמיה", expanded=True):
    e1, e2, e3, e4 = st.columns(4)
    e1.metric("סטטוס", evidence.status)
    e2.metric("n אפקטיבי", evidence.n_eff)
    e3.metric("Lift OOS", "—" if evidence.lift is None else f"{evidence.lift:+.1%}")
    e4.metric("FDR q", "—" if evidence.fdr_q is None else f"{evidence.fdr_q:.3f}")
    st.caption(
        f"Non-overlap: "
        f"{'—' if evidence.nonoverlap_rate is None else f'{evidence.nonoverlap_rate:.1%}'} · "
        f"משטרים חיוביים: {evidence.positive_regimes}/{evidence.tested_regimes}. "
        "נדרשים יחד n_eff≥20, לפחות 80 בחירות, lift חיובי, FDR≤5%, "
        "יתרון במדגם non-overlap ויציבות בשני משטרים."
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

with st.expander("עדכון נתוני ת״א־35 מהבורסה", expanded=False):
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
    st.markdown(
        "**הורדה ידנית:** באתר הבורסה בחר `3 Years`, החל את הסינון ולחץ `CSV`. "
        "אין צורך לערוך את הקובץ או לשנות את שמו."
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
                    f"{symbol}: {result.observations[symbol]:,} רשומות עד "
                    f"{result.latest_dates[symbol]:%d/%m/%Y}"
                    for symbol in result.observations
                )
                st.success(f"הנתונים עודכנו בהצלחה. {details}")
                st.rerun()

st.subheader("אינדיקטורים ועוצמת הסיגנל")
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
st.caption(
    "ציוני העוצמה מתעדכנים לפי ביצועי האות בעבר באופק שנבחר. "
    "הציון מנכה את שיעור הבסיס ומעניש מדגם קטן."
)

for start in range(0, len(data.cards), 4):
    columns = st.columns(4)
    for column, card in zip(columns, data.cards[start : start + 4], strict=False):
        display = "לא זמין" if card.value is None else format(card.value, card.format)
        vol_result = data.backtest.indicator(
            card.key, strength_horizon, "volatility", card.volatility_arrow
        )
        market_result = data.backtest.indicator(
            card.key, strength_horizon, "market", card.market_arrow
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
            f"תנודתיות {card.volatility_arrow} "
            f"עוצמה {vol_result.strength if vol_result else 1}/10 · "
            f"ת״א־35 {card.market_arrow} עוצמה "
            f"{market_result.strength if market_result else 1}/10"
        )

with st.expander("תוצאות backtest — כל האינדיקטורים והאסטרטגיות", expanded=False):
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
                "עוצמת תנודתיות": (
                    f"{vol_result.strength}/10" if vol_result else "—"
                ),
                "דיוק תנודתיות": (
                    f"{vol_result.hit_rate:.1%}"
                    if vol_result and vol_result.hit_rate is not None
                    else "—"
                ),
                "בסיס תנודתיות": (
                    f"{vol_result.baseline_rate:.1%}"
                    if vol_result and vol_result.baseline_rate is not None
                    else "—"
                ),
                "n תנודתיות": vol_result.observations if vol_result else 0,
                "חץ ת״א־35": card.market_arrow,
                "עוצמת ת״א־35": (
                    f"{market_result.strength}/10" if market_result else "—"
                ),
                "דיוק ת״א־35": (
                    f"{market_result.hit_rate:.1%}"
                    if market_result and market_result.hit_rate is not None
                    else "—"
                ),
                "בסיס ת״א־35": (
                    f"{market_result.baseline_rate:.1%}"
                    if market_result and market_result.baseline_rate is not None
                    else "—"
                ),
                "n ת״א־35": market_result.observations if market_result else 0,
            }
        )
    st.markdown("**אינדיקטורים — ביצועי הכיוון המוצג כעת**")
    st.dataframe(pd.DataFrame(indicator_rows), hide_index=True, width="stretch")

    strategy_rows = []
    for result in report.strategy_results:
        if result.horizon_days != tested_horizon:
            continue
        strategy_rows.append(
            {
                "אסטרטגיה": result.strategy_name,
                "מספר המלצות": result.observations,
                "הצלחת תרחיש": (
                    f"{result.success_rate:.1%}"
                    if result.success_rate is not None
                    else "—"
                ),
                "בסיס סטטיסטי": (
                    f"{result.baseline_rate:.1%}"
                    if result.baseline_rate is not None
                    else "—"
                ),
                "עוצמה": f"{result.strength}/10",
                "איכות מדגם": result.sample_quality,
            }
        )
    st.markdown("**אסטרטגיות — proxy להצלחת תרחיש השוק**")
    st.dataframe(pd.DataFrame(strategy_rows), hide_index=True, width="stretch")
    for warning in report.warnings:
        st.caption(f"• {warning}")

with st.expander("Ablation OOS — מט״ח–מניות ומתאם TA35–VTA35", expanded=False):
    if data.context_ablation:
        st.dataframe(pd.DataFrame(data.context_ablation), hide_index=True, width="stretch")
        st.caption(
            "הבדיקות משתמשות במדגמים לא־חופפים וב־FDR. שני המשתנים נשארים "
            "context-only ואינם משנים חץ פעיל ללא מעבר כל השערים."
        )
    else:
        st.info("אין מדגם מספיק לבדיקת התרומה השולית.")

left, right = st.columns(2)
with left:
    st.subheader("ת״א־35 — 252 ימי נתונים")
    if data.ta35_dates:
        st.line_chart(pd.DataFrame({"ת״א־35": data.ta35_closes}, index=data.ta35_dates))
with right:
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
st.caption(
    "אופק המניפה עצמאי מאופק האסטרטגיה. "
    "החצים בכרטיסים מתארים סיגנל היוריסטי; ↔ מציין שאין כיוון אמין."
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
        height=500,
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
    st.caption(
        f"החישוב מבוסס על תנודתיות שנתית משולבת של {data.forecast_volatility:.1%}, "
        "252 ימי מסחר וללא הנחת כיוון. התאריכים העתידיים משוערים ואינם כוללים חגי בורסה."
    )
else:
    st.info("אין מספיק נתוני ת״א־35 או תחזית תנודתיות להצגת המניפה.")

st.caption(
    "כל המדדים הם כלי תמיכה בלבד. אין במערכת הוראות מסחר, חיבור לחשבון או נתוני זמן אמת."
)
