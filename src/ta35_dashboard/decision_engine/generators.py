"""Layer 2: Strategy Candidate Universe Generator.

Generates candidate options structures across strategy families, expirations,
and strikes based on model quantiles, market deltas, and risk limits.
Also provides strategy family selection logic for EOD General Mode.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ta35_dashboard.decision_engine.models import (
    CandidateTrade,
    Expiry,
    LegQuote,
    ModelDistribution,
    StrategyFamily,
)

logger = logging.getLogger(__name__)


def map_eod_strategy_families(
    prob_up: float,
    forecast_rv: float,
    current_rv: float,
    regime: str,
    volatility_state: str = "מתכווצת",
    market_state: str = "ניטרלי",
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
    is_vol_expanding = "מתרחבת" in vol_state_clean or "expanding" in vol_state_clean.lower()
    is_vol_contracting = "מתכווצת" in vol_state_clean or "contracting" in vol_state_clean.lower()
    is_vol_rich = forecast_rv > 0.22 or regime == "STRESS"

    if is_vol_expanding:
        vol_view = "ציפייה לעליית תנודתיות (מתרחבת)"
    elif is_vol_contracting:
        vol_view = "ציפייה לירידת תנודתיות (מתכווצת)"
    else:
        vol_view = f"תנודתיות מעורבת ({vol_state_clean})"

    if is_bullish:
        direction_view = "שורי (Bullish)"
        if is_vol_rich or is_vol_contracting:
            primary = StrategyFamily.BULL_PUT_CREDIT
            alts = (StrategyFamily.BULL_CALL_DEBIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
        else:
            primary = StrategyFamily.BULL_CALL_DEBIT
            alts = (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
    elif is_bearish:
        direction_view = "דובי (Bearish)"
        if is_vol_rich or is_vol_contracting:
            primary = StrategyFamily.BEAR_CALL_CREDIT
            alts = (StrategyFamily.BEAR_PUT_DEBIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
        else:
            primary = StrategyFamily.BEAR_PUT_DEBIT
            alts = (StrategyFamily.BEAR_CALL_CREDIT, StrategyFamily.DIRECTIONAL_BUTTERFLY)
    else:
        direction_view = "נייטרלי (Neutral / Rangebound)"
        if is_vol_expanding:
            primary = StrategyFamily.LONG_STRADDLE
            alts = (StrategyFamily.LONG_STRANGLE, StrategyFamily.LONG_IRON_BUTTERFLY)
        elif is_vol_contracting or is_vol_rich:
            primary = StrategyFamily.IRON_CONDOR
            alts = (StrategyFamily.IRON_BUTTERFLY, StrategyFamily.LONG_BUTTERFLY)
        else:
            primary = StrategyFamily.LONG_BUTTERFLY
            alts = (StrategyFamily.IRON_CONDOR, StrategyFamily.DEBIT_CONDOR)
            
    return primary, alts, direction_view, vol_view


def compute_eod_statistical_legs(
    spot_price: float,
    forecast_rv: float,
    horizon_days: int,
    family: StrategyFamily,
) -> tuple[dict[str, Any], ...]:
    """Calculates theoretical leg positions (strikes & sigma offsets) for EOD Strategy Mode based on standard deviations."""
    import math

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
        k1 = round_strike(spot_price - 0.5 * sigma_1d)
        k2 = round_strike(spot_price - 1.2 * sigma_1d)
        if family == StrategyFamily.BULL_PUT_CREDIT:
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

    elif family in (StrategyFamily.LONG_BUTTERFLY, StrategyFamily.DIRECTIONAL_BUTTERFLY, StrategyFamily.IRON_BUTTERFLY):
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


def generate_candidate_trades(
    chain: Any,
    spot_price: float,
    model_dist: ModelDistribution,
    contract_multiplier: float = 50.0,
) -> list[CandidateTrade]:
    """Generates candidate defined-risk trades for FULL_DDE mode across Core Families."""
    candidates: list[CandidateTrade] = []
    quotes = getattr(chain, "quotes", [])
    if not quotes or len(quotes) < 3:
        return candidates

    days_to_exp = float(getattr(chain, "days_to_expiration", 14.0))
    exp_label = getattr(chain, "expiration_label", "Standard Expiration")
    expiry = Expiry(
        expiration_date=exp_label,
        days_to_expiration=days_to_exp,
        is_weekly="שבועית" in exp_label,
    )

    # Sort quotes by strike
    sorted_quotes = sorted(quotes, key=lambda q: q.strike)
    strikes = [q.strike for q in sorted_quotes]

    # Helper lookup
    quote_map = {q.strike: q for q in sorted_quotes}

    # Find ATM index
    atm_quote = min(sorted_quotes, key=lambda q: abs(q.strike - spot_price))
    atm_idx = sorted_quotes.index(atm_quote)

    step = 10.0  # Strike spacing standard in TA-35

    # 1. Bull Call Spreads (Debit) & Bull Put Spreads (Credit)
    for i in range(max(0, atm_idx - 5), min(len(sorted_quotes) - 1, atm_idx + 5)):
        k1 = strikes[i]
        for j in range(i + 1, min(len(sorted_quotes), i + 4)):
            k2 = strikes[j]
            q1, q2 = quote_map[k1], quote_map[k2]
            width = k2 - k1

            # Bull Call Spread (Buy Call K1, Sell Call K2)
            c1_ask = getattr(q1, "call_ask", 0.0) or (q1.call_mid or 0.0)
            c2_bid = getattr(q2, "call_bid", 0.0) or (q2.call_mid or 0.0)
            if c1_ask > 0 and c2_bid > 0:
                net_debit = c1_ask - c2_bid
                if 0 < net_debit < width:
                    max_prof = (width - net_debit) * contract_multiplier
                    max_l = net_debit * contract_multiplier
                    legs = (
                        LegQuote("CALL", k1, "BUY", 1, q1.call_bid or 0.0, c1_ask, c1_ask, contract_multiplier),
                        LegQuote("CALL", k2, "SELL", 1, c2_bid, q2.call_ask or 0.0, c2_bid, contract_multiplier),
                    )
                    candidates.append(
                        CandidateTrade(
                            candidate_id=f"BULL_CALL_{k1}_{k2}",
                            strategy_family=StrategyFamily.BULL_CALL_DEBIT,
                            strategy_variant=f"{k1}/{k2} Call Spread",
                            expiry=expiry,
                            legs=legs,
                            net_debit_credit=net_debit,
                            limit_price=net_debit,
                            max_profit=max_prof,
                            max_loss=max_l,
                            breakevens=(k1 + net_debit,),
                        )
                    )

            # Bull Put Spread (Sell Put K2, Buy Put K1)
            p2_bid = getattr(q2, "put_bid", 0.0) or (q2.put_mid or 0.0)
            p1_ask = getattr(q1, "put_ask", 0.0) or (q1.put_ask or 0.0)
            if p2_bid > 0 and p1_ask > 0:
                net_credit = p2_bid - p1_ask
                if 0 < net_credit < width:
                    max_prof = net_credit * contract_multiplier
                    max_l = (width - net_credit) * contract_multiplier
                    legs = (
                        LegQuote("PUT", k2, "SELL", 1, p2_bid, q2.put_ask or 0.0, p2_bid, contract_multiplier),
                        LegQuote("PUT", k1, "BUY", 1, q1.put_bid or 0.0, p1_ask, p1_ask, contract_multiplier),
                    )
                    candidates.append(
                        CandidateTrade(
                            candidate_id=f"BULL_PUT_{k1}_{k2}",
                            strategy_family=StrategyFamily.BULL_PUT_CREDIT,
                            strategy_variant=f"{k1}/{k2} Put Credit Spread",
                            expiry=expiry,
                            legs=legs,
                            net_debit_credit=-net_credit,
                            limit_price=-net_credit,
                            max_profit=max_prof,
                            max_loss=max_l,
                            breakevens=(k2 - net_credit,),
                        )
                    )

    # 2. Long Butterflies (1:-2:1)
    for i in range(max(0, atm_idx - 4), min(len(sorted_quotes) - 2, atm_idx + 3)):
        k1 = strikes[i]
        k2 = strikes[i + 1]
        k3 = strikes[i + 2]
        if abs((k3 - k2) - (k2 - k1)) < 1e-4:  # Symmetric
            w = k2 - k1
            q1, q2, q3 = quote_map[k1], quote_map[k2], quote_map[k3]
            c1_ask = getattr(q1, "call_ask", 0.0) or (q1.call_mid or 0.0)
            c2_bid = getattr(q2, "call_bid", 0.0) or (q2.call_mid or 0.0)
            c3_ask = getattr(q3, "call_ask", 0.0) or (q3.call_mid or 0.0)
            if c1_ask > 0 and c2_bid > 0 and c3_ask > 0:
                cost = c1_ask - (2 * c2_bid) + c3_ask
                if 0 < cost < w:
                    max_prof = (w - cost) * contract_multiplier
                    max_l = cost * contract_multiplier
                    legs = (
                        LegQuote("CALL", k1, "BUY", 1, q1.call_bid or 0.0, c1_ask, c1_ask, contract_multiplier),
                        LegQuote("CALL", k2, "SELL", 2, c2_bid, q2.call_ask or 0.0, c2_bid, contract_multiplier),
                        LegQuote("CALL", k3, "BUY", 1, q3.call_bid or 0.0, c3_ask, c3_ask, contract_multiplier),
                    )
                    fam = StrategyFamily.LONG_BUTTERFLY if k2 == atm_quote.strike else StrategyFamily.DIRECTIONAL_BUTTERFLY
                    candidates.append(
                        CandidateTrade(
                            candidate_id=f"BUTTERFLY_{k1}_{k2}_{k3}",
                            strategy_family=fam,
                            strategy_variant=f"{k1}/{k2}/{k3} Butterfly",
                            expiry=expiry,
                            legs=legs,
                            net_debit_credit=cost,
                            limit_price=cost,
                            max_profit=max_prof,
                            max_loss=max_l,
                            breakevens=(k1 + cost, k3 - cost),
                        )
                    )

    # 3. Iron Condors (Bull Put + Bear Call)
    for i in range(max(0, atm_idx - 5), atm_idx - 1):
        for j in range(atm_idx + 1, min(len(sorted_quotes) - 1, atm_idx + 5)):
            kp1, kp2 = strikes[i], strikes[i + 1]
            kc1, kc2 = strikes[j], strikes[j + 1]
            qp1, qp2 = quote_map[kp1], quote_map[kp2]
            qc1, qc2 = quote_map[kc1], quote_map[kc2]
            
            p2_bid = getattr(qp2, "put_bid", 0.0) or (qp2.put_mid or 0.0)
            p1_ask = getattr(qp1, "put_ask", 0.0) or (qp1.put_ask or 0.0)
            c1_bid = getattr(qc1, "call_bid", 0.0) or (qc1.call_mid or 0.0)
            c2_ask = getattr(qc2, "call_ask", 0.0) or (qc2.call_ask or 0.0)

            if p2_bid > 0 and p1_ask > 0 and c1_bid > 0 and c2_ask > 0:
                credit = (p2_bid - p1_ask) + (c1_bid - c2_ask)
                w_put = kp2 - kp1
                w_call = kc2 - kc1
                w_max = max(w_put, w_call)
                if 0 < credit < w_max:
                    max_l = (w_max - credit) * contract_multiplier
                    max_prof = credit * contract_multiplier
                    legs = (
                        LegQuote("PUT", kp1, "BUY", 1, qp1.put_bid or 0.0, p1_ask, p1_ask, contract_multiplier),
                        LegQuote("PUT", kp2, "SELL", 1, p2_bid, qp2.put_ask or 0.0, p2_bid, contract_multiplier),
                        LegQuote("CALL", kc1, "SELL", 1, c1_bid, qc1.call_ask or 0.0, c1_bid, contract_multiplier),
                        LegQuote("CALL", kc2, "BUY", 1, qc2.call_bid or 0.0, c2_ask, c2_ask, contract_multiplier),
                    )
                    candidates.append(
                        CandidateTrade(
                            candidate_id=f"IRON_CONDOR_{kp1}_{kp2}_{kc1}_{kc2}",
                            strategy_family=StrategyFamily.IRON_CONDOR,
                            strategy_variant=f"{kp1}/{kp2}/{kc1}/{kc2} Iron Condor",
                            expiry=expiry,
                            legs=legs,
                            net_debit_credit=-credit,
                            limit_price=-credit,
                            max_profit=max_prof,
                            max_loss=max_l,
                            breakevens=(kp2 - credit, kc1 + credit),
                        )
                    )

    logger.info("Generated %d candidate trades for expiration %s", len(candidates), exp_label)
    return candidates
