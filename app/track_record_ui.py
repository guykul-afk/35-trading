"""Track Record & Recommendation Evaluation Dashboard UI.

Strictly separates Directional Prediction Verification from Volatility Prediction
Verification, with an additional tab for Strategy and Range Spatial Outcomes.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from ta35_dashboard.config import PROJECT_ROOT
from ta35_dashboard.decision_engine.evaluator import (
    HORIZONS,
    fetch_evaluation_records,
    get_direction_performance,
    get_strategy_performance,
    get_volatility_performance,
    resolve_pending_evaluations,
)


def render_track_record_dashboard(db_path: str | Path | None = None) -> None:
    """Renders the comprehensive Recommendation Track Record dashboard."""
    if db_path is None:
        db_path = PROJECT_ROOT / "data" / "ta35_dashboard.db"

    # Automatically resolve any newly eligible pending evaluations
    try:
        resolve_pending_evaluations(db_path)
    except Exception:
        pass

    st.markdown(
        """
        <div style="background: linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(31, 41, 55, 0.85)); 
                    border: 1px solid rgba(75, 85, 99, 0.4); border-radius: 12px; padding: 20px; margin-bottom: 25px;">
            <h2 style="margin: 0; color: #f3f4f6; font-size: 1.6rem; font-weight: 700;">
                📊 יומן ביצועים ואימות המלצות עבר (Recommendation Track Record)
            </h2>
            <p style="margin: 6px 0 0 0; color: #9ca3af; font-size: 0.95rem;">
                מעקב אובייקטיבי וממוחשב (Walk-Forward Verification) על כל המלצה שהופקה ע״י מנוע ההחלטות.
                האימות נמדד על נתוני סגירה אמיתיים ב-4 אופקי זמן: <b>3, 7, 14, ו-30 ימי מסחר</b>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    dir_stats = get_direction_performance(db_path)
    vol_stats = get_volatility_performance(db_path)
    strat_stats = get_strategy_performance(db_path)
    all_rows = fetch_evaluation_records(db_path, limit=250)

    # 3 Distinct Sub-Tabs separating Direction, Volatility, and Strategy
    tab_dir, tab_vol, tab_strat = st.tabs(
        [
            "🧭 1. אימות חיזוי כיוון (Direction)",
            "⚡ 2. אימות חיזוי תנודתיות (Volatility)",
            "🎯 3. אסטרטגיות וטווחי מסחר (Strategy & Range)",
        ]
    )

    # =========================================================================
    # SUB-TAB 1: DIRECTIONAL PREDICTION
    # =========================================================================
    with tab_dir:
        st.subheader("🧭 אימות תחזיות כיוון המדד (Directional Accuracy)")
        st.caption(
            "בדיקה האם המדד נע בהתאם לכיוון שנחזה (שורי / דובי / נייטרלי) לאחר סינון רעש שוק (Deadband תואם-אופק)."
        )

        # 1. KPI Cards by Horizon
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]

        for i, h in enumerate(HORIZONS):
            stat = dir_stats.get(h, {})
            hits = stat.get("hits", 0)
            misses = stat.get("misses", 0)
            flats = stat.get("flats", 0)
            hit_rate = stat.get("hit_rate", 0.0)
            total = stat.get("total", 0)

            with cols[i]:
                rate_color = "#10b981" if hit_rate >= 55.0 else ("#f59e0b" if hit_rate >= 45.0 else "#ef4444")
                st.markdown(
                    f"""
                    <div style="background: rgba(31, 41, 55, 0.7); border: 1px solid rgba(75, 85, 99, 0.4); 
                                border-radius: 10px; padding: 14px; text-align: center;">
                        <div style="color: #9ca3af; font-size: 0.85rem; font-weight: 600;">אופק {h} ימי מסחר</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {rate_color}; margin: 6px 0;">
                            {hit_rate:.1f}%
                        </div>
                        <div style="color: #d1d5db; font-size: 0.8rem;">
                            <span style="color: #10b981;">✅ {hits}</span> &nbsp;|&nbsp; 
                            <span style="color: #ef4444;">❌ {misses}</span> &nbsp;|&nbsp; 
                            <span style="color: #9ca3af;">⚪ {flats}</span>
                        </div>
                        <div style="color: #6b7280; font-size: 0.75rem; margin-top: 4px;">
                            סה״כ: {total} החלטות
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Directional Breakdown Chart & Stance Comparison
        c_chart, c_stance = st.columns([3, 2])

        with c_chart:
            st.markdown("##### 📊 שיעור הצלחה כיווני לפי אופק זמן")
            horiz_labels = [f"T+{h}d" for h in HORIZONS]
            rates = [dir_stats.get(h, {}).get("hit_rate", 0.0) for h in HORIZONS]
            hit_counts = [dir_stats.get(h, {}).get("hits", 0) for h in HORIZONS]
            miss_counts = [dir_stats.get(h, {}).get("misses", 0) for h in HORIZONS]
            flat_counts = [dir_stats.get(h, {}).get("flats", 0) for h in HORIZONS]

            fig_dir = go.Figure()
            fig_dir.add_trace(
                go.Bar(
                    name="פגיעה (Hit)",
                    x=horiz_labels,
                    y=hit_counts,
                    marker_color="#10b981",
                )
            )
            fig_dir.add_trace(
                go.Bar(
                    name="שגיאה (Miss)",
                    x=horiz_labels,
                    y=miss_counts,
                    marker_color="#ef4444",
                )
            )
            fig_dir.add_trace(
                go.Bar(
                    name="דשדוש (Flat)",
                    x=horiz_labels,
                    y=flat_counts,
                    marker_color="#6b7280",
                )
            )
            fig_dir.update_layout(
                barmode="stack",
                height=280,
                margin={"l": 20, "r": 20, "t": 20, "b": 20},
                legend={"orientation": "h", "y": -0.2},
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "#e5e7eb"},
            )
            st.plotly_chart(fig_dir, use_container_width=True)

        with c_stance:
            st.markdown("##### 🎯 פילוח לפי עמדת מודל (Stance Breakdown)")
            stance_data = []
            for h in (3, 7, 14):
                bd = dir_stats.get(h, {}).get("stance_breakdown", {})
                for stance, outcomes in bd.items():
                    h_cnt = outcomes.get("HIT", 0)
                    m_cnt = outcomes.get("MISS", 0)
                    f_cnt = outcomes.get("FLAT", 0)
                    tot_s = h_cnt + m_cnt
                    pct = (h_cnt / tot_s * 100) if tot_s > 0 else 0.0
                    stance_data.append(
                        {
                            "אופק": f"T+{h}",
                            "עמדה": stance,
                            "פגיעות": h_cnt,
                            "שגיאות": m_cnt,
                            "הצלחה": f"{pct:.1f}%",
                        }
                    )
            if stance_data:
                st.dataframe(pd.DataFrame(stance_data), hide_index=True, use_container_width=True)
            else:
                st.info("אין מספיק נתונים לפילוח עמדות כיוון.")

        st.markdown("---")

        # 3. Directional Audit Table
        st.markdown("##### 📋 יומן אימות כיוון היסטורי")
        h_filter = st.selectbox("סנן לפי אופק זמן:", [3, 7, 14, 30], index=0, key="dir_h_filter")
        
        filtered_rows = [r for r in all_rows if r.get("horizon_days") == h_filter]
        if filtered_rows:
            display_data = []
            for r in filtered_rows:
                status = r.get("status")
                outcome = r.get("direction_outcome") or ("ממתין ⏳" if status == "PENDING" else "—")
                dir_view_str = (r.get("direction_view") or "").lower()
                is_neutral_rec = "נייטרלי" in dir_view_str or "neutral" in dir_view_str or "דשדוש" in dir_view_str
                if outcome == "HIT":
                    icon = "✅ פגיעה (דשדוש)" if is_neutral_rec else "✅ פגיעה"
                elif outcome == "MISS":
                    icon = "❌ שגיאה (פריצה)" if is_neutral_rec else "❌ שגיאה"
                elif outcome == "FLAT":
                    icon = "⚪ תנועה זניחה"
                else:
                    icon = outcome
                
                pct = r.get("pct_change")
                pct_str = f"{pct:+.2%}" if pct is not None else "—"
                spot_t0 = r.get("spot_t0")
                spot_tk = r.get("spot_tk")

                display_data.append(
                    {
                        "תאריך המלצה": r.get("as_of_date"),
                        "תאריך בדיקה": r.get("actual_session_date") or r.get("target_date"),
                        "כיוון חזוי": r.get("direction_view"),
                        "הסתברות מודל": f"{r.get('direction_prob', 0):.1%}",
                        "מדד כניסה (S₀)": f"{spot_t0:,.1f}" if spot_t0 else "—",
                        "מדד סיום (Sₖ)": f"{spot_tk:,.1f}" if spot_tk else "—",
                        "שינוי מדד": pct_str,
                        "תוצאת כיוון": icon,
                        "הסבר": r.get("notes") or "—",
                    }
                )
            st.dataframe(pd.DataFrame(display_data), hide_index=True, use_container_width=True)
        else:
            st.info(f"לא נמצאו רשומות לאופק {h_filter} ימי מסחר.")

    # =========================================================================
    # SUB-TAB 2: VOLATILITY PREDICTION
    # =========================================================================
    with tab_vol:
        st.subheader("⚡ אימות תחזיות תנודתיות (Volatility Accuracy)")
        st.caption(
            "בדיקה עצמאית האם השוק התנהג בהתאם לצפי התנודתיות (עלייה / ירידה / רגיעה), והשוואת ה-RV בפועל מול תחזית המודל ו-VTA35."
        )

        # 1. KPI Cards for Volatility
        col_v1, col_v2, col_v3, col_v4 = st.columns(4)
        cols_v = [col_v1, col_v2, col_v3, col_v4]

        for i, h in enumerate(HORIZONS):
            v_stat = vol_stats.get(h, {})
            v_hits = v_stat.get("hits", 0)
            v_misses = v_stat.get("misses", 0)
            v_hit_rate = v_stat.get("hit_rate", 0.0)
            v_mae = v_stat.get("mae_rv_pct", 0.0)
            v_total = v_stat.get("total", 0)

            with cols_v[i]:
                rate_color = "#10b981" if v_hit_rate >= 55.0 else ("#f59e0b" if v_hit_rate >= 45.0 else "#ef4444")
                st.markdown(
                    f"""
                    <div style="background: rgba(31, 41, 55, 0.7); border: 1px solid rgba(75, 85, 99, 0.4); 
                                border-radius: 10px; padding: 14px; text-align: center;">
                        <div style="color: #9ca3af; font-size: 0.85rem; font-weight: 600;">תנודתיות {h} ימי מסחר</div>
                        <div style="font-size: 1.8rem; font-weight: 800; color: {rate_color}; margin: 6px 0;">
                            {v_hit_rate:.1f}%
                        </div>
                        <div style="color: #d1d5db; font-size: 0.8rem;">
                            <span style="color: #10b981;">✅ {v_hits}</span> &nbsp;|&nbsp; 
                            <span style="color: #ef4444;">❌ {v_misses}</span>
                        </div>
                        <div style="color: #38bdf8; font-size: 0.75rem; margin-top: 4px;">
                            שגיאה ממוצעת (MAE): {v_mae:.1f}% RV
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)

        # 2. Time-series comparison: Forecast RV vs Actual RV vs VTA35
        st.markdown("##### 📈 השוואת תחזית תנודתיות מול תנודתיות בפועל (Forecast vs Actual Realized Volatility)")
        
        resolved_vol_rows = [r for r in all_rows if r.get("status") == "RESOLVED" and r.get("actual_rv") is not None]
        if resolved_vol_rows:
            # Sort by date
            sorted_vol = sorted(resolved_vol_rows, key=lambda x: (x.get("as_of_date") or "", x.get("horizon_days") or 0))
            
            dates_list = [f"{r['as_of_date']} (T+{r['horizon_days']})" for r in sorted_vol]
            forecast_rvs = [(r.get("forecast_rv") or 0) * 100 for r in sorted_vol]
            actual_rvs = [(r.get("actual_rv") or 0) * 100 for r in sorted_vol]
            vta35_vals = [(r.get("vta35_tk") or r.get("vta35_t0") or 0) for r in sorted_vol]

            fig_vol = go.Figure()
            fig_vol.add_trace(
                go.Scatter(
                    x=dates_list,
                    y=forecast_rvs,
                    mode="lines+markers",
                    name="תחזית RV מודל (%)",
                    line={"color": "#38bdf8", "width": 2},
                )
            )
            fig_vol.add_trace(
                go.Scatter(
                    x=dates_list,
                    y=actual_rvs,
                    mode="lines+markers",
                    name="תנודתיות בפועל Realized RV (%)",
                    line={"color": "#f59e0b", "width": 2},
                )
            )
            if any(v > 0 for v in vta35_vals):
                fig_vol.add_trace(
                    go.Scatter(
                        x=dates_list,
                        y=vta35_vals,
                        mode="lines",
                        name="VTA35 מדד התנודתיות הגלומה (%)",
                        line={"color": "#a855f7", "width": 1.5, "dash": "dot"},
                    )
                )

            fig_vol.update_layout(
                height=320,
                margin={"l": 20, "r": 20, "t": 20, "b": 20},
                legend={"orientation": "h", "y": -0.25},
                yaxis_title="תנודתיות שנתית (%)",
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font={"color": "#e5e7eb"},
            )
            st.plotly_chart(fig_vol, use_container_width=True)
        else:
            st.info("עדיין אין מספיק נתוני תנודתיות שנפתרו להצגת הגרף.")

        st.markdown("---")

        # 3. Volatility Audit Table
        st.markdown("##### 📋 יומן אימות תנודתיות היסטורי")
        h_vol_filter = st.selectbox("סנן לפי אופק זמן:", [3, 7, 14, 30], index=1, key="vol_h_filter")
        
        filtered_vol_rows = [r for r in all_rows if r.get("horizon_days") == h_vol_filter]
        if filtered_vol_rows:
            vol_display_data = []
            for r in filtered_vol_rows:
                status = r.get("status")
                outcome = r.get("volatility_outcome") or ("ממתין ⏳" if status == "PENDING" else "—")
                icon = "✅ פגיעה" if outcome == "HIT" else ("❌ שגיאה" if outcome == "MISS" else outcome)

                f_rv = r.get("forecast_rv")
                a_rv = r.get("actual_rv")
                v_t0 = r.get("vta35_t0")
                v_tk = r.get("vta35_tk")

                vol_display_data.append(
                    {
                        "תאריך המלצה": r.get("as_of_date"),
                        "תאריך סיום": r.get("actual_session_date") or r.get("target_date"),
                        "צפי תנודתיות": r.get("volatility_view"),
                        "תחזית RV מודל": f"{f_rv * 100:.2f}%" if f_rv is not None else "—",
                        "תנודתיות בפועל (RV)": f"{a_rv * 100:.2f}%" if a_rv is not None else "—",
                        "VTA35 בסיס": f"{v_t0:.2f}%" if v_t0 is not None else "—",
                        "VTA35 סיום": f"{v_tk:.2f}%" if v_tk is not None else "—",
                        "תוצאת תנודתיות": icon,
                    }
                )
            st.dataframe(pd.DataFrame(vol_display_data), hide_index=True, use_container_width=True)
        else:
            st.info(f"לא נמצאו רשומות תנודתיות לאופק {h_vol_filter} ימי מסחר.")

    # =========================================================================
    # SUB-TAB 3: OPTIONS STRATEGIES & SPATIAL RANGE
    # =========================================================================
    with tab_strat:
        st.subheader("🎯 אימות אסטרטגיות אופציות ומיקום המדד ביחס לצפי")
        st.caption(
            "בדיקה האם מדד ת״א־35 נותר בתוך מעטפת ההסתברות (Probability Band), הגיע לטווח היעד (Target Range), או שבר את רמת הכשלון (Invalidation Level)."
        )

        spatial = strat_stats.get("spatial", {})
        in_band_pct = spatial.get("in_band_pct", 0.0)
        in_target_pct = spatial.get("in_target_pct", 0.0)
        inv_pct = spatial.get("invalidation_pct", 0.0)

        # Spatial KPI Cards
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            st.metric(
                "הישארות במעטפת ההסתברות (In Probability Band)",
                f"{in_band_pct:.1f}%",
                help="אחוז המקרים שבהם המדד לא חרג ממעטפת התנודתיות הסטטיסטית (1.0σ - 1.5σ).",
            )
        with sc2:
            st.metric(
                "פגיעה בטווח היעד (Hit Target Range)",
                f"{in_target_pct:.1f}%",
                help="אחוז המקרים שבהם המדד שהה בתוך טווח הרווח המרבי שהוגדר לאסטרטגיה.",
            )
        with sc3:
            st.metric(
                "שבירת רמת כשלון (Thesis Invalidation Breached)",
                f"{inv_pct:.1f}%",
                delta=f"-{inv_pct:.1f}%",
                delta_color="inverse",
                help="אחוז המקרים שבהם נשברה רמת הסטופ/כשלון התזה עוד לפני תום החלון (רצוי שיהיה נמוך ככל האפשר).",
            )

        st.markdown("---")

        # Strategy Family Outcomes
        c_fam_chart, c_fam_table = st.columns([3, 2])

        with c_fam_chart:
            st.markdown("##### 📊 התפלגות תוצאות לפי משפחת אסטרטגיה")
            fam_outcomes = strat_stats.get("family_outcomes", {})
            families = list(fam_outcomes.keys())

            if families:
                max_profit_list = [fam_outcomes[f].get("MAX_PROFIT", 0) for f in families]
                partial_profit_list = [fam_outcomes[f].get("PARTIAL_PROFIT", 0) for f in families]
                breakeven_list = [fam_outcomes[f].get("BREAKEVEN", 0) for f in families]
                loss_list = [fam_outcomes[f].get("LOSS", 0) for f in families]
                max_loss_list = [fam_outcomes[f].get("MAX_LOSS", 0) for f in families]

                fig_fam = go.Figure()
                fig_fam.add_trace(go.Bar(name="רווח מקסימלי (Max Profit)", x=families, y=max_profit_list, marker_color="#10b981"))
                fig_fam.add_trace(go.Bar(name="רווח חלקי (Partial)", x=families, y=partial_profit_list, marker_color="#34d399"))
                fig_fam.add_trace(go.Bar(name="איזון (Breakeven)", x=families, y=breakeven_list, marker_color="#9ca3af"))
                fig_fam.add_trace(go.Bar(name="הפסד (Loss)", x=families, y=loss_list, marker_color="#f87171"))
                fig_fam.add_trace(go.Bar(name="הפסד מלא/חריגה (Max Loss)", x=families, y=max_loss_list, marker_color="#ef4444"))

                fig_fam.update_layout(
                    barmode="stack",
                    height=300,
                    margin={"l": 20, "r": 20, "t": 20, "b": 20},
                    legend={"orientation": "h", "y": -0.25},
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font={"color": "#e5e7eb"},
                )
                st.plotly_chart(fig_fam, use_container_width=True)
            else:
                st.info("אין עדיין נתוני אסטרטגיות שנפתרו.")

        with c_fam_table:
            st.markdown("##### 📌 סיכום הצלחת אסטרטגיות")
            fam_rows = []
            for fam, outs in fam_outcomes.items():
                win = outs.get("MAX_PROFIT", 0) + outs.get("PARTIAL_PROFIT", 0)
                tot = sum(outs.values())
                fam_rows.append(
                    {
                        "אסטרטגיה": fam,
                        "סה״כ": tot,
                        "רווחיות": f"{(win / tot * 100):.1f}%" if tot > 0 else "0%",
                    }
                )
            if fam_rows:
                st.dataframe(pd.DataFrame(fam_rows), hide_index=True, use_container_width=True)

        st.markdown("---")

        # Full Strategy Log Table
        st.markdown("##### 📋 יומן אימות אסטרטגיות ומיקום מדד")
        strat_display = []
        for r in all_rows:
            if r.get("status") == "RESOLVED":
                outcome = r.get("strategy_outcome") or "—"
                icon = (
                    "🟢 רווח מלא" if outcome == "MAX_PROFIT"
                    else ("🟢 רווח חלקי" if outcome == "PARTIAL_PROFIT"
                    else ("⚪ איזון" if outcome == "BREAKEVEN"
                    else ("🔴 הפסד מלא" if outcome == "MAX_LOSS" else "🟠 הפסד")))
                )
                strat_display.append(
                    {
                        "תאריך המלצה": r.get("as_of_date"),
                        "אופק": f"T+{r.get('horizon_days')}d",
                        "אסטרטגיה מומלצת": r.get("primary_family"),
                        "מדד כניסה": f"{r.get('spot_t0', 0):,.1f}",
                        "מדד סיום": f"{r.get('spot_tk', 0):,.1f}",
                        "במעטפת הסתברות": "✅ כן" if r.get("in_probability_band") else "❌ חריגה",
                        "ביעד רווח": "🎯 כן" if r.get("in_target_range") else "לא",
                        "שבירת כשלון": "⚠️ נשבר" if r.get("invalidation_breached") else "שמור",
                        "תוצאת אסטרטגיה": icon,
                    }
                )
        if strat_display:
            st.dataframe(pd.DataFrame(strat_display), hide_index=True, use_container_width=True)
        else:
            st.info("אין עדיין נתוני אסטרטגיות להצגה ביומן.")
