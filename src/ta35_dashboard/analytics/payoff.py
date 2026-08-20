"""Option strategy payoff profile and probability distribution visualizer."""

from __future__ import annotations

import math
from typing import Any

import numpy as np


from ..config import TRADING_DAYS_PER_YEAR


def generate_strategy_payoff_data(
    spot: float,
    forecast_volatility: float,
    horizon_days: int,
    legs: list[dict[str, Any]],
    points: int = 150,
) -> dict[str, Any]:
    """Generate index price levels, payoff profile at expiry, and probability density values for any set of legs."""
    if spot <= 0 or forecast_volatility <= 0 or horizon_days <= 0:
        return {"index_levels": [], "payoff": [], "pdf_scaled": [], "spot": spot, "one_sigma": 0, "legs": legs}

    one_sigma = spot * forecast_volatility * math.sqrt(horizon_days / TRADING_DAYS_PER_YEAR)
    sigma_bound = max(3.0 * one_sigma, spot * 0.10)

    min_price = max(10.0, spot - sigma_bound)
    max_price = spot + sigma_bound

    index_levels = np.linspace(min_price, max_price, points)
    payoff = np.zeros_like(index_levels)

    T_years = max(1.0, float(horizon_days)) / 365.0
    r_rate = 0.04
    
    for leg in legs:
        action = str(leg.get("action", "")).lower()
        opt_type = str(leg.get("option_type", "")).lower()
        strike = leg.get("strike") or leg.get("estimated_strike")
        qty = int(leg.get("quantity") or leg.get("ratio", 1))

        if strike is None or strike <= 0:
            continue

        direction = 1.0 if action in ("buy", "קנייה", "long") else -1.0

        # Theoretical Black-Scholes entry premium estimation
        if opt_type in ("call", "קול"):
            d1 = (math.log(spot / strike) + (r_rate + 0.5 * forecast_volatility**2) * T_years) / (forecast_volatility * math.sqrt(T_years))
            d2 = d1 - forecast_volatility * math.sqrt(T_years)
            prem = spot * (0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))) - strike * math.exp(-r_rate * T_years) * (0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0))))
            leg_payoff = np.maximum(index_levels - strike, 0.0) - prem
        elif opt_type in ("put", "פוט"):
            d1 = (math.log(spot / strike) + (r_rate + 0.5 * forecast_volatility**2) * T_years) / (forecast_volatility * math.sqrt(T_years))
            d2 = d1 - forecast_volatility * math.sqrt(T_years)
            prem = strike * math.exp(-r_rate * T_years) * (0.5 * (1.0 + math.erf(-d2 / math.sqrt(2.0)))) - spot * (0.5 * (1.0 + math.erf(-d1 / math.sqrt(2.0))))
            leg_payoff = np.maximum(strike - index_levels, 0.0) - prem
        else:
            leg_payoff = np.zeros_like(index_levels)

        payoff += direction * qty * leg_payoff

    # Normal distribution probability density over index levels
    sigma_p = one_sigma
    if sigma_p > 0:
        pdf = (1.0 / (sigma_p * math.sqrt(2 * math.pi))) * np.exp(
            -0.5 * ((index_levels - spot) / sigma_p) ** 2
        )
    else:
        pdf = np.zeros_like(index_levels)

    # Normalize PDF scale for visual overlay
    max_payoff_abs = float(np.max(np.abs(payoff))) if np.max(np.abs(payoff)) > 0 else 50.0
    pdf_max = float(np.max(pdf))
    pdf_normalized = (pdf / pdf_max) * max_payoff_abs if pdf_max > 0 else pdf

    return {
        "index_levels": index_levels.tolist(),
        "payoff": payoff.tolist(),
        "pdf_raw": pdf.tolist(),
        "pdf_scaled": pdf_normalized.tolist(),
        "spot": spot,
        "one_sigma": one_sigma,
        "legs": legs,
    }


def build_plotly_payoff_chart(payoff_data: dict[str, Any], title: str = 'פרופיל רווח/הפסד בפקיעה והתפלגות הסתברות'):
    """Build a Plotly Figure visualizing Payoff curve, Probability Density, Spot level, and Leg Strike markers."""
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots

    if not payoff_data or not payoff_data.get("index_levels"):
        fig = go.Figure()
        fig.update_layout(title="אין נתונים חוקיים להצגת גרף Payoff")
        return fig

    levels = payoff_data["index_levels"]
    payoff = payoff_data["payoff"]
    pdf_scaled = payoff_data["pdf_scaled"]
    spot = payoff_data["spot"]
    legs = payoff_data.get("legs", [])
    one_sigma = payoff_data["one_sigma"]

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # 1. Add Payoff Curve
    fig.add_trace(
        go.Scatter(
            x=levels,
            y=payoff,
            mode="lines",
            name="פרופיל P&L בפקיעה (נק')",
            line=dict(color="#00D26A", width=3),
        ),
        secondary_y=False,
    )

    # 2. Add Probability Density Area
    fig.add_trace(
        go.Scatter(
            x=levels,
            y=pdf_scaled,
            mode="lines",
            name="התפלגות צפויה (N(μ,σ))",
            line=dict(color="rgba(0, 191, 255, 0.5)", width=1.5, dash="dot"),
            fill="tozeroy",
            fillcolor="rgba(0, 191, 255, 0.12)",
        ),
        secondary_y=False,
    )

    # 3. Add Zero Line
    fig.add_hline(y=0, line_width=1, line_dash="solid", line_color="gray", secondary_y=False)

    # 4. Add Spot Level Marker
    fig.add_vline(
        x=spot,
        line_width=2,
        line_dash="dash",
        line_color="#FFD700",
        annotation_text=f"Spot ({int(round(spot))})",
        annotation_position="top left",
    )

    # 5. Add ±1σ vertical markers
    fig.add_vline(
        x=spot - one_sigma,
        line_width=1,
        line_dash="dot",
        line_color="rgba(255,255,255,0.4)",
        annotation_text="-1σ",
    )
    fig.add_vline(
        x=spot + one_sigma,
        line_width=1,
        line_dash="dot",
        line_color="rgba(255,255,255,0.4)",
        annotation_text="+1σ",
    )

    # 6. Add Leg Strike Lines
    color_map = {
        ("buy", "call"): "#38EF7D",
        ("sell", "call"): "#FF4D4D",
        ("buy", "put"): "#FFA500",
        ("sell", "put"): "#FF6B6B",
    }

    for leg in legs:
        strike_val = leg.get("strike")
        if strike_val is not None:
            action = str(leg.get("action", "")).lower()
            opt_type = str(leg.get("option_type", "")).lower()
            qty = leg.get("quantity", 1)
            lbl = leg.get("label", f"{action.capitalize()} {opt_type.capitalize()}")

            color = color_map.get((action, opt_type), "#FFFFFF")

            fig.add_vline(
                x=strike_val,
                line_width=2,
                line_dash="dot",
                line_color=color,
                annotation_text=f"{lbl} {strike_val} ({qty}x)" if qty > 1 else f"{lbl} {strike_val}",
                annotation_position="bottom right",
            )

    fig.update_layout(
        title=dict(text=title, font=dict(size=16)),
        xaxis_title="רמת מדד ת\"א 35",
        yaxis_title="רווח / הפסד סינתטי (נקודות מדד)",
        hovermode="x unified",
        template="plotly_dark",
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    )

    return fig
