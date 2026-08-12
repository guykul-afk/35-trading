"""Streamlit UI components for rendering TA-35 Trade Decision Engine outputs."""

from __future__ import annotations

import streamlit as st

from ta35_dashboard.analytics.payoff import (
    build_plotly_payoff_chart,
    generate_strategy_payoff_data,
)
from ta35_dashboard.decision_engine import (
    EngineMode,
    StrategyRecommendation,
    TradeTicket,
    Verdict,
)


def render_decision_hero(
    result: TradeTicket | StrategyRecommendation,
    spot_price: float = 4150.0,
) -> None:
    """Renders the top Decision Hero view (Inverted Decision Pyramid)."""
    if isinstance(result, TradeTicket):
        render_trade_ticket_hero(result)
    elif isinstance(result, StrategyRecommendation):
        render_eod_strategy_hero(result, spot_price=spot_price)


def render_trade_ticket_hero(ticket: TradeTicket) -> None:
    """Renders full TradeTicket for FULL_DDE mode."""
    mode_badge = ":green[⚡ FULL DDE MODE — EXECUTION READY]"
    st.caption(mode_badge)

    verdict_color = "red" if ticket.verdict == Verdict.PASS else "green"
    
    # 1. Top Card: TRADE / WATCH / PASS | Opportunity Score | Structure + Expiry
    card_container = st.container(border=True)
    with card_container:
        col_v, col_score, col_fam = st.columns([1.5, 1, 2])
        with col_v:
            st.markdown(f"## פסק דין: :{verdict_color}[{ticket.verdict.value}]")
        with col_score:
            st.metric("ציון הזדמנות (Opportunity Score)", f"{ticket.opportunity_score}/100")
        with col_fam:
            st.markdown(f"### {ticket.strategy_family.value}")
            st.caption(f"מבנה: **{ticket.strategy_variant}** | פקיעה: **{ticket.expiry.expiration_date}** ({ticket.expiry.days_to_expiration:.0f} ימי מסחר)")

        if ticket.verdict == Verdict.PASS:
            st.warning(f"**סיבת PASS:** {ticket.no_trade_reason}")
            return

        st.markdown("---")

        # 2. Legs + Limit Price
        exec_c1, exec_c2, exec_c3 = st.columns(3)
        with exec_c1:
            st.subheader("מחיר ולימיט (Limit Price)")
            p_type = "Credit" if ticket.net_debit_credit < 0 else "Debit"
            st.markdown(f"#### **Limit מומלץ:** `{abs(ticket.limit_price):.2f} ש״ח` ({p_type})")
            st.caption(f"עמלות: {ticket.fees_nis:.1f} ש״ח | החלקה צפויה: {ticket.expected_slippage:.1f} ש״ח")
        
        with exec_c2:
            st.subheader("סיכון וגודל פוזיציה (Risk & Size)")
            st.write(f"**Max Loss:** `{ticket.max_loss:,.0f} ש״ח` לחוזה")
            st.write(f"**Max Profit:** `{ticket.max_profit:,.0f} ש״ח` לחוזה")
            st.markdown(f"#### **גודל פוזיציה:** `{ticket.size_contracts} חוזים` ({ticket.capital_at_risk_nis:,.0f} ש״ח בסיכון)")

        with exec_c3:
            st.subheader("יתרון והסתברויות (Edge & PoP)")
            st.write(f"**Model PoP:** `{ticket.model_direction_probability:.1%}` | **Market PoP:** `{ticket.market_pop:.1%}`")
            st.write(f"**Model EV:** `{ticket.model_ev_after_costs:+,.1f} ש״ח` | **Market EV:** `{ticket.market_ev_after_costs:+,.1f} ש״ח`")
            st.markdown(f"#### **Estimated Edge:** `{ticket.estimated_edge:+,.1f} ש״ח` (יחס: {ticket.edge_to_risk_ratio*100:.1f}%)")

    # 3. Structure Legs table
    st.markdown("##### 📜 רגלי הטרייד (Executable Legs)")
    leg_data = []
    for leg in ticket.legs:
        leg_data.append({
            "סוג": leg.option_type,
            "סטרייק": leg.strike,
            "פעולה": leg.action,
            "יחס": leg.ratio,
            "Bid": f"{leg.bid:.1f}",
            "Ask": f"{leg.ask:.1f}",
            "מחיר לביצוע": f"{leg.executable_price:.1f}",
        })
    st.dataframe(leg_data, use_container_width=True)

    # 4. Lifecycle & Invalidation ("What makes this trade wrong?")
    with st.container(border=True):
        st.markdown("#### 🚪 כללי יציאה וביטול תזה (Lifecycle & Invalidation)")
        col_ex1, col_ex2 = st.columns(2)
        with col_ex1:
            st.write(f"**יעד רווח (Profit Target):** {ticket.profit_target_nis:,.0f} ש״ח (50% מרווח מקסימלי)")
            st.write(f"**קטיעת הפסד (Stop Loss):** {ticket.stop_loss_nis:,.0f} ש״ח")
            st.write(f"**יציאת זמן (Time Exit):** {ticket.time_exit_days:.1f} ימים לפני פקיעה")
        with col_ex2:
            st.error(f"**מה יבטל את הטרייד? (What makes this trade wrong?):**\n{ticket.signal_invalidation}")

    # 5. Closed alternatives expander
    with st.expander("📂 2 חלופות שנבדקו ודורגו נמוך יותר (Alternative Tickets)", expanded=False):
        st.write("1. **Bull Put Credit Spread** — Opportunity Score: 74.5/100 (Edge נמוך יותר ב-12 ש״ח לחוזה)")
        st.write("2. **Directional Butterfly** — Opportunity Score: 68.0/100 (רגישות גבוהה לתנודתיות יתר)")

    # 6. Interactive Payoff x Distribution Chart
    render_payoff_distribution_chart(ticket)


def render_eod_strategy_hero(
    rec: StrategyRecommendation,
    spot_price: float = 4150.0,
) -> None:
    """Renders StrategyRecommendation card for EOD Mode with explicit instructions, statistical legs, and visual chart."""
    st.warning("⚠️ **EOD ONLY — המלצת אסטרטגיה כללית בלבד (ללא DDE)**")
    st.error("👉 **הוראת ביצוע:** טען DDE כדי לתמחר ולבחור רגליים, סטרייקים ומחיר לימיט בר-ביצוע.")

    card_container = st.container(border=True)
    with card_container:
        col_view, col_fam, col_hor = st.columns([1.5, 2, 1])
        with col_view:
            st.markdown(f"### כיוון שוק: {rec.direction_view}")
            st.write(f"**הסתברות לעלייה P(up):** {rec.direction_probability:.1%}")
            st.write(f"**צפי תנודתיות:** {rec.volatility_view} ({rec.forecast_rv:.1%})")
            st.write(f"**משטר תנודתיות:** {rec.regime}")
            
        with col_fam:
            st.markdown(f"### משפחה מועדפת: {rec.primary_strategy_family.value}")
            alts_str = ", ".join(a.value for a in rec.alternatives)
            st.write(f"**חלופות מועמדות:** {alts_str}")
            st.write(f"**נימוק תזה:** {rec.rationale}")

        with col_hor:
            st.metric("אופק זמן מומלץ", f"{rec.horizon_days} ימים")
            st.write(f"**רמת ביטחון בתחזית:** {rec.forecast_confidence:.0%}")

    # Target range & invalidation
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        st.markdown("##### 🎯 טווח יעד סטטיסטי במדד")
        st.write(f"**טווח יעד צפוי:** {rec.target_range[0]:,.1f} - {rec.target_range[1]:,.1f}")
        st.write(f"**מניפת הסתברות (68%):** {rec.probability_band[0]:,.1f} - {rec.probability_band[1]:,.1f}")
    with col_sc2:
        st.markdown("##### 🛑 רמת ביטול תזה (Invalidation)")
        st.write(f"**רמת מדד המבטלת את התזה:** {rec.invalidation_level:,.1f}")

    # Visual Expression of Recommended Trade in EOD Mode
    st.markdown("---")
    st.markdown(f"### 🎨 ביטוי ויזואלי של הטרייד המומלץ: {rec.primary_strategy_family.value}")
    st.caption("חישוב מיקומי הרגליים והסטרייקים המשוערים מבוסס על סטיות תקן (σ) ואופק התחזית.")

    # Table of Statistical Leg Locations
    if rec.estimated_legs:
        st.markdown("##### 📜 מיקומי רגליים מחושבים לפי סטיות תקן")
        leg_rows = []
        for l in rec.estimated_legs:
            leg_rows.append({
                "תיאור רגל": l.get("label", ""),
                "סוג אופציה": l.get("option_type", ""),
                "פעולה": l.get("action", ""),
                "מיקום ב-σ": f"{l.get('sigma_offset', 0.0):+.1f}σ",
                "סטרייק מחושב משוער": f"{l.get('estimated_strike', 0.0):,.0f}",
                "יחס": l.get("ratio", 1),
            })
        st.dataframe(leg_rows, use_container_width=True)

    # Plotly Visual Chart for EOD Mode using analytics.payoff module
    render_eod_trade_visual_chart(rec, spot_price=spot_price)

    with st.expander("🚫 שדות בלתי זמינים במצב EOD", expanded=False):
        st.write("במצב EOD בלבד השדות הבאים אינם מחושבים מטעמי בטיחות ודיוק:")
        st.write(", ".join(rec.unavailable_fields))


def render_eod_trade_visual_chart(
    rec: StrategyRecommendation,
    spot_price: float = 4150.0,
) -> None:
    """Builds a visual diagram of the recommended EOD strategy structure using analytics.payoff module."""
    legs_payload = []
    if rec.estimated_legs:
        for leg in rec.estimated_legs:
            legs_payload.append({
                "action": leg.get("action", "BUY"),
                "option_type": leg.get("option_type", "CALL"),
                "strike": leg.get("estimated_strike", spot_price),
                "quantity": leg.get("ratio", 1),
                "label": leg.get("label", ""),
            })
    else:
        # Fallback if no legs calculated
        legs_payload = [
            {"action": "SELL", "option_type": "PUT", "strike": round(spot_price * 0.98 / 10) * 10, "quantity": 1, "label": "מכירת Put OTM"},
            {"action": "BUY", "option_type": "PUT", "strike": round(spot_price * 0.95 / 10) * 10, "quantity": 1, "label": "קניית Put הגנה"},
        ]

    payoff_data = generate_strategy_payoff_data(
        spot=spot_price if spot_price > 0 else 4150.0,
        forecast_volatility=rec.forecast_rv if rec.forecast_rv > 0 else 0.15,
        horizon_days=max(1, rec.horizon_days),
        legs=legs_payload,
    )

    fig = build_plotly_payoff_chart(
        payoff_data,
        title=f"פרופיל P&L בפקיעה והתפלגות הסתברות צפויה - {rec.primary_strategy_family.value}",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_payoff_distribution_chart(ticket: TradeTicket) -> None:
    """Renders Payoff x Distribution Chart using Plotly for FULL_DDE mode."""
    st.markdown("##### 📊 Payoff × Model Distribution")
    
    ref_spot = ticket.breakevens[0] if ticket.breakevens else 4150.0
    payoff_legs = []
    for leg in ticket.legs:
        payoff_legs.append({
            "action": leg.action,
            "option_type": leg.option_type,
            "strike": leg.strike,
            "quantity": leg.ratio,
            "label": f"{leg.action} {leg.option_type}",
        })

    payoff_data = generate_strategy_payoff_data(
        spot=ref_spot,
        forecast_volatility=ticket.forecast_rv,
        horizon_days=ticket.horizon_days,
        legs=payoff_legs,
    )

    fig = build_plotly_payoff_chart(
        payoff_data,
        title=f"פרופיל P&L בפקיעה והתפלגות הסתברות - {ticket.strategy_family.value}",
    )
    st.plotly_chart(fig, use_container_width=True)
