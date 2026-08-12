"""Short-Term Trade Recommendation Engine & Combined Payoff-Fan Chart Builder.

Specializes in 1-day and 3-day short-term option trades derived from live DDE option chains.
Provides clear Hebrew trade rationales and builds combined Payoff + Probability Fan Plotly charts.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import pandas as pd
import plotly.graph_objects as go

from ta35_dashboard.analytics.implied_vol import HorizonExpectation
from ta35_dashboard.analytics.realtime_strategies import (
    RealtimeLeg,
    RealtimeStrategyProposal,
    price_realtime_strategies,
)
from ta35_dashboard.connectors.dde_parser import ParsedOptionChain


def get_shortterm_recommendation(
    weekly_chain: ParsedOptionChain | None,
    monthly_chain: ParsedOptionChain | None,
    spot_price: float,
    horizon_days: int = 1,
    prob_rise: float = 0.55,
    implied_vol: float = 0.15,
) -> tuple[RealtimeStrategyProposal | None, str]:
    """Get the top short-term trade recommendation for 1 or 3 days.

    Returns:
        (proposal, rationale_text)
    """
    chain = weekly_chain if (horizon_days == 1 and weekly_chain) else (monthly_chain or weekly_chain)

    if not chain or not chain.quotes or spot_price <= 0:
        return None, "אין נתוני אופציות DDE זמינים עבור אופק זה."

    proposals = price_realtime_strategies(
        chain=chain,
        spot_price=spot_price,
        prob_rise=prob_rise,
        implied_vol=implied_vol,
        contract_multiplier=50.0,
    )

    if not proposals:
        return None, "לא נמצאו אסטרטגיות עומדות במבחן תוחלת הרווח ומרווחי המסחר במחירי ה-DDE הנוכחיים."

    top = proposals[0]

    # Build rich Hebrew rationale text
    direction_str = "חיובי (אופטימי)" if prob_rise >= 0.52 else ("שלילי (זהיר)" if prob_rise <= 0.48 else "ניטרלי")
    ev_sign = "+" if top.expected_value_nis >= 0 else ""

    rationale_parts = [
        f"**אופק הטרייד:** {horizon_days} ימי מסחר (פקיעה קרובה מתוך נתוני ה-DDE).",
        f"**צפי כיווני משוקלל:** {direction_str} (הסתברות לעלייה: {prob_rise:.1%}).",
        f"**תנודתיות גלומה לאופק (IV):** {implied_vol:.2%}, מגלמת תנודה יומית צפויה של ±{spot_price * implied_vol * math.sqrt(horizon_days/252.0):.1f} נקודות.",
        f"**נימוק מסחר:** {top.rationale}",
        f"**תוחלת רווח מתמטית ($EV$):** {ev_sign}{top.expected_value_nis:,.0f} ש״ח לעסקה (סיכוי הצלחה מוערך של {top.probability_of_profit:.1%}).",
    ]

    return top, "\n\n".join(rationale_parts)


def build_shortterm_payoff_fan_chart(
    proposal: RealtimeStrategyProposal,
    horizon_exp: HorizonExpectation,
    spot_price: float,
    multiplier: float = 50.0,
) -> go.Figure:
    """Build a combined Plotly chart showing Trade Payoff curve overlaid with Probability Fan bands."""
    one_sigma = horizon_exp.one_sigma_move
    
    # Generate range of index prices around spot
    min_x = max(1000.0, spot_price - 3.0 * one_sigma)
    max_x = spot_price + 3.0 * one_sigma
    x_vals = [min_x + i * (max_x - min_x) / 300.0 for i in range(301)]

    # Compute Payoff curve at expiration (in NIS)
    payoff_nis = []
    for x in x_vals:
        net_leg_payoff_pts = 0.0
        for leg in proposal.legs:
            if leg.option_type.lower() == "call":
                intrinsic = max(0.0, x - leg.strike)
            else:
                intrinsic = max(0.0, leg.strike - x)

            if leg.action == "Buy":
                net_leg_payoff_pts += intrinsic - leg.exec_price
            else:
                net_leg_payoff_pts += leg.exec_price - intrinsic
        
        payoff_nis.append(net_leg_payoff_pts * multiplier)

    fig = go.Figure()

    # 1. Add Probability Fan Shading Bands
    band_styles = [
        (2.0, f"95.4% (±2σ: {horizon_exp.lower_2s:,.0f}–{horizon_exp.upper_2s:,.0f})", "rgba(59, 130, 246, 0.12)"),
        (1.5, f"86.6% (±1.5σ: {spot_price - 1.5*one_sigma:,.0f}–{spot_price + 1.5*one_sigma:,.0f})", "rgba(59, 130, 246, 0.22)"),
        (1.0, f"68.3% (±1σ: {horizon_exp.lower_1s:,.0f}–{horizon_exp.upper_1s:,.0f})", "rgba(59, 130, 246, 0.38)"),
        (0.5, f"38.3% (±0.5σ: {spot_price - 0.5*one_sigma:,.0f}–{spot_price + 0.5*one_sigma:,.0f})", "rgba(59, 130, 246, 0.55)"),
    ]

    min_payoff = min(payoff_nis)
    max_payoff = max([p for p in payoff_nis if p != float("inf")] or [1000.0])
    y_min_fill = min(-500.0, min_payoff * 1.1)
    y_max_fill = max(500.0, max_payoff * 1.1)

    for sigma, label, fill_color in band_styles:
        x_low = max(min_x, spot_price - sigma * one_sigma)
        x_high = min(max_x, spot_price + sigma * one_sigma)
        
        fig.add_trace(
            go.Scatter(
                x=[x_low, x_high, x_high, x_low],
                y=[y_min_fill, y_min_fill, y_max_fill, y_max_fill],
                fill="toself",
                fillcolor=fill_color,
                line={"width": 0},
                name=f"מניפה {label}",
                hoverinfo="skip",
            )
        )

    # 2. Zero Profit Line
    fig.add_hline(y=0, line_dash="dash", line_color="#8b98aa", annotation_text="קו איזון 0 ש״ח")

    # 3. Spot Price Vertical Line
    fig.add_vline(
        x=spot_price,
        line_dash="dot",
        line_color="#eab308",
        line_width=2,
        annotation_text=f"מדד נוכחי: {spot_price:,.1f}",
        annotation_position="top left",
    )

    # 4. Breakeven Vertical Lines
    for be in proposal.breakeven_points:
        fig.add_vline(
            x=be,
            line_dash="dashdot",
            line_color="#10b981" if proposal.is_credit else "#3b82f6",
            line_width=1.5,
            annotation_text=f"נקודת איזון: {be:,.1f}",
            annotation_position="bottom right",
        )

    # 5. Options Payoff Curve
    fig.add_trace(
        go.Scatter(
            x=x_vals,
            y=payoff_nis,
            mode="lines",
            name="רווח / הפסד בפקיעה (ש״ח)",
            line={"color": "#10b981", "width": 3},
            hovertemplate="מדד בפקיעה: %{x:,.1f}<br>רווח/הפסד: %{y:,.0f} ש״ח<extra></extra>",
        )
    )

    fig.update_layout(
        title=f"גרף Payoff ומניפת הסתברות — {proposal.strategy_name} ({proposal.horizon_days} ימי מסחר)",
        height=480,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        hovermode="x unified",
        xaxis_title="רמת מדד תל אביב 35 בפקיעה",
        yaxis_title="רווח / הפסד כספי (ש״ח)",
        legend={"orientation": "h", "y": 1.12, "x": 0},
    )

    return fig
