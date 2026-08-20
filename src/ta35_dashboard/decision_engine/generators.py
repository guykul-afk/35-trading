"""Strategy Candidate and Leg Generator for EOD Quantitative Architecture.

Maps central regime matrix states to optimal strategy families and calculates
theoretical strike locations and statistical leg bounds based on volatility and horizon.
"""

from __future__ import annotations

import logging
import math
from typing import Any

from ta35_dashboard.decision_engine.models import CandidateTrade, StrategyFamily

logger = logging.getLogger(__name__)


def generate_candidate_trades(
    chain: Any, spot_price: float, model_dist: Any
) -> list[CandidateTrade]:
    """Generates candidate trades from option chain (for Full DDE live execution)."""
    return []


def map_eod_strategy_families(
    prob_up: float,
    forecast_rv: float,
    current_rv: float,
    regime: str,
    volatility_state: str = "מתכווצת",
    market_state: str = "ניטרלי",
    is_premium_eligible: bool = True,
) -> tuple[StrategyFamily, tuple[StrategyFamily, ...], str, str]:
    """Maps EOD market state (P_up, forecast_rv, regime, volatility_state, market_state) to primary and alternative strategy families.
    
    Uses the unified central regime matrix market_state and volatility_state to guarantee 100% consistency across all tabs.
    
    Returns:
        tuple[StrategyFamily, tuple[StrategyFamily, ...], str, str]:
            (primary_family, alternatives, direction_view, vol_view)
    """
    mkt_state_clean = str(market_state).strip().lower()
    if "עולה" in mkt_state_clean or "חיובי" in mkt_state_clean or "bullish" in mkt_state_clean or prob_up >= 0.55:
        is_bullish = True
        is_bearish = False
        is_neutral = False
    elif "יורד" in mkt_state_clean or "שלילי" in mkt_state_clean or "bearish" in mkt_state_clean or prob_up <= 0.45:
        is_bearish = True
        is_bullish = False
        is_neutral = False
    else:
        is_neutral = True
        is_bullish = False
        is_bearish = False

    # Standardize volatility state label from regime matrix
    vol_state_clean = str(volatility_state).strip()
    is_vol_expanding = "מתרחבת" in vol_state_clean or "expanding" in vol_state_clean.lower() or "עלייה" in vol_state_clean
    is_vol_contracting = "מתכווצת" in vol_state_clean or "contracting" in vol_state_clean.lower() or "ירידה" in vol_state_clean
    is_vol_rich = forecast_rv > 0.22 or regime == "STRESS" or regime == "לחץ גבוה"

    if is_vol_expanding:
        vol_view = "עלייה בתנודתיות"
    elif is_vol_contracting:
        vol_view = "ירידה בתנודתיות"
    else:
        vol_view = "יציבות בתנודתיות"

    if is_bullish:
        direction_view = "שורי (Bullish)"
        if (is_vol_rich or is_vol_contracting) and is_premium_eligible:
            primary = StrategyFamily.BULL_PUT_CREDIT
            alts = (StrategyFamily.BULL_CALL_DEBIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
        else:
            primary = StrategyFamily.BULL_CALL_DEBIT
            alts = (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.DIRECTIONAL_BUTTERFLY) if is_premium_eligible else (StrategyFamily.DIRECTIONAL_BUTTERFLY,)
    elif is_bearish:
        direction_view = "דובי (Bearish)"
        if (is_vol_rich or is_vol_contracting) and is_premium_eligible:
            primary = StrategyFamily.BEAR_CALL_CREDIT
            alts = (StrategyFamily.BEAR_PUT_DEBIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
        else:
            primary = StrategyFamily.BEAR_PUT_DEBIT
            alts = (StrategyFamily.BEAR_CALL_CREDIT, StrategyFamily.DIRECTIONAL_BUTTERFLY) if is_premium_eligible else (StrategyFamily.DIRECTIONAL_BUTTERFLY,)
    else:
        direction_view = "נייטרלי (Neutral / Rangebound)"
        if is_vol_expanding:
            primary = StrategyFamily.LONG_STRADDLE
            alts = (StrategyFamily.LONG_STRANGLE, StrategyFamily.LONG_IRON_BUTTERFLY)
        elif (is_vol_contracting or is_vol_rich) and is_premium_eligible:
            primary = StrategyFamily.IRON_CONDOR
            alts = (StrategyFamily.IRON_BUTTERFLY, StrategyFamily.LONG_BUTTERFLY)
        else:
            primary = StrategyFamily.LONG_BUTTERFLY
            alts = (StrategyFamily.IRON_CONDOR, StrategyFamily.DEBIT_CONDOR) if is_premium_eligible else (StrategyFamily.DEBIT_CONDOR,)
            
    return primary, alts, direction_view, vol_view


def compute_eod_statistical_legs(
    spot_price: float,
    forecast_rv: float,
    horizon_days: int,
    family: StrategyFamily,
    prob_up: float = 0.50,
    *args: Any,
    **kwargs: Any,
) -> tuple[dict[str, Any], ...]:
    """Calculates theoretical leg positions (strikes & sigma offsets) for EOD Strategy Mode based on standard deviations."""
    sigma_1d = spot_price * forecast_rv * math.sqrt(max(1.0, horizon_days) / 365.0)

    def round_strike(val: float) -> float:
        return round(val / 10.0) * 10.0

    legs: list[dict[str, Any]] = []

    if family in (StrategyFamily.BULL_CALL_DEBIT, StrategyFamily.BEAR_CALL_CREDIT):
        k1 = round_strike(spot_price)
        k2 = round_strike(spot_price + 0.8 * sigma_1d)
        if family == StrategyFamily.BULL_CALL_DEBIT:
            legs = [
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k1, "ratio": 1, "label": f"קניית Call ATM ({k1:,.0f})"},
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": k2, "ratio": 1, "label": f"מכירת Call OTM (+0.8σ: {k2:,.0f})"},
            ]
        else:
            legs = [
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.5, "estimated_strike": k1, "ratio": 1, "label": f"מכירת Call (+0.5σ: {k1:,.0f})"},
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.3, "estimated_strike": k2, "ratio": 1, "label": f"קניית Call הגנה (+1.3σ: {k2:,.0f})"},
            ]

    elif family in (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.BEAR_PUT_DEBIT):
        if family == StrategyFamily.BULL_PUT_CREDIT:
            k1 = round_strike(spot_price - 0.5 * sigma_1d)
            k2 = round_strike(spot_price - 1.2 * sigma_1d)
            legs = [
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.5, "estimated_strike": k1, "ratio": 1, "label": f"מכירת Put OTM (-0.5σ: {k1:,.0f})"},
                {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.2, "estimated_strike": k2, "ratio": 1, "label": f"קניית Put הגנה (-1.2σ: {k2:,.0f})"},
            ]
        else:
            kp_atm = round_strike(spot_price)
            kp_otm = round_strike(spot_price - 0.8 * sigma_1d)
            legs = [
                {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": kp_atm, "ratio": 1, "label": f"קניית Put ATM ({kp_atm:,.0f})"},
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": kp_otm, "ratio": 1, "label": f"מכירת Put OTM (-0.8σ: {kp_otm:,.0f})"},
            ]

    elif family == StrategyFamily.IRON_CONDOR:
        kp_long = round_strike(spot_price - 1.5 * sigma_1d)
        kp_short = round_strike(spot_price - 0.8 * sigma_1d)
        kc_short = round_strike(spot_price + 0.8 * sigma_1d)
        kc_long = round_strike(spot_price + 1.5 * sigma_1d)
        legs = [
            {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.5, "estimated_strike": kp_long, "ratio": 1, "label": f"קניית Put כנף (-1.5σ: {kp_long:,.0f})"},
            {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": kp_short, "ratio": 1, "label": f"מכירת Put (-0.8σ: {kp_short:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": kc_short, "ratio": 1, "label": f"מכירת Call (+0.8σ: {kc_short:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.5, "estimated_strike": kc_long, "ratio": 1, "label": f"קניית Call כנף (+1.5σ: {kc_long:,.0f})"},
        ]

    elif family == StrategyFamily.DIRECTIONAL_BUTTERFLY:
        if prob_up >= 0.50:
            # Bullish Directional Butterfly: Centered at upward target (+0.8 sigma)
            k_left = round_strike(spot_price)
            k_center = round_strike(spot_price + 0.8 * sigma_1d)
            k_right = round_strike(spot_price + 1.6 * sigma_1d)
            legs = [
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Call כנף תחתונה (ATM: {k_left:,.0f})"},
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Calls יעד מרכזי (+0.8σ: {k_center:,.0f})"},
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.6, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Call כנף עליונה (+1.6σ: {k_right:,.0f})"},
            ]
        else:
            # Bearish Directional Butterfly: Centered at downward target (-0.8 sigma)
            k_right = round_strike(spot_price)
            k_center = round_strike(spot_price - 0.8 * sigma_1d)
            k_left = round_strike(spot_price - 1.6 * sigma_1d)
            legs = [
                {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.6, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Put כנף תחתונה (-1.6σ: {k_left:,.0f})"},
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Puts יעד מרכזי (-0.8σ: {k_center:,.0f})"},
                {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Put כנף עליונה (ATM: {k_right:,.0f})"},
            ]

    elif family in (StrategyFamily.LONG_BUTTERFLY, StrategyFamily.IRON_BUTTERFLY):
        k_center = round_strike(spot_price)
        k_left = round_strike(spot_price - 0.8 * sigma_1d)
        k_right = round_strike(spot_price + 0.8 * sigma_1d)
        legs = [
            {"option_type": "CALL", "action": "BUY", "sigma_offset": -0.8, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Call כנף שמאל (-0.8σ: {k_left:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Calls מרכז (ATM: {k_center:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.8, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Call כנף ימין (+0.8σ: {k_right:,.0f})"},
        ]

    else:
        k_atm = round_strike(spot_price)
        legs = [
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Call ATM ({k_atm:,.0f})"},
            {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Put ATM ({k_atm:,.0f})"},
        ]

    return tuple(legs)
