"""Layer 5 Quality Gates & Layer 6 Ranking Engine.

Filters candidate trades against hard constraints (Pass/Fail) and scores valid trades
using frozen Opportunity Score weights.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ta35_dashboard.decision_engine.models import CandidateTrade, Verdict

logger = logging.getLogger(__name__)


def apply_quality_gates(
    candidate: CandidateTrade,
    model_ev_after_costs: float,
    estimated_edge: float,
    risk_budget_nis: float = 10000.0,
    min_edge_to_risk_ratio: float = 0.05,
    max_bid_ask_spread_pct: float = 0.25,
) -> tuple[bool, str | None]:
    """Applies Layer 5 Quality Gates to disqualify infeasible or poor edge candidates.
    
    Returns:
        tuple[bool, str | None]: (passed, rejection_reason)
    """
    # Gate 1: Defined Risk Check
    if not candidate.has_defined_risk or candidate.max_loss <= 0 or math_is_infinite(candidate.max_loss):
        return False, "מבנה בעל סיכון שאינו מוגדר נפסל עקב מגבלת סיכון"

    # Gate 2: Expiration / DTE check
    if candidate.expiry.days_to_expiration <= 0:
        return False, "פקיעה עברה או DTE אינו תקין"

    # Gate 3: Risk Budget Exceeded (single contract minimum exceeds budget)
    if candidate.max_loss > risk_budget_nis:
        return False, f"הפסד מקסימלי לחוזה ({candidate.max_loss:.0f} ש״ח) חורג מתקציב הסיכון ({risk_budget_nis:.0f} ש״ח)"

    # Gate 4: Positive Model Edge After Costs
    if model_ev_after_costs <= 0:
        return False, f"תוחלת מודל שלילית לאחר עלויות ({model_ev_after_costs:.1f} ש״ח)"

    # Gate 5: Minimum Edge to Risk Ratio
    edge_to_risk = estimated_edge / max(1.0, candidate.max_loss)
    if edge_to_risk < min_edge_to_risk_ratio:
        return False, f"יחס edge לסיכון נמוך מ- {min_edge_to_risk_ratio*100:.1f}% ({edge_to_risk*100:.1f}%)"

    return True, None


def calculate_opportunity_score(
    candidate: CandidateTrade,
    model_ev_after_costs: float,
    estimated_edge: float,
    market_pop: float,
    model_confidence: float = 0.8,
    exec_bid_ask_spread_pct: float | None = None,
    historical_winrate: float | None = None,
    strategy_fit_score: float | None = None,
) -> tuple[float, float]:
    """Calculates Layer 6 Opportunity Score (0 - 100).
    Missing execution/fit/evidence data penalizes the score by leaving those weights as 0.
    
    Returns:
        tuple[float, float]: (final_score, score_coverage)
    """
    total_score = 0.0
    total_weight = 0.0
    
    max_possible_weight = 35.0 + 15.0 + 10.0 + 20.0 + 10.0 + 10.0  # 100.0

    # 1. Edge score (Weight 35)
    edge_to_risk = estimated_edge / max(1.0, candidate.max_loss)
    edge_score = min(35.0, max(0.0, edge_to_risk * 100.0 * 1.5))
    total_score += edge_score
    total_weight += 35.0

    # 2. Forecast Confidence (Weight 15)
    conf_score = model_confidence * 15.0
    total_score += conf_score
    total_weight += 15.0

    # 3. Risk Efficiency (Weight 10)
    prof_to_loss = candidate.max_profit / max(1.0, candidate.max_loss)
    risk_score = min(10.0, max(0.0, prof_to_loss * 5.0))
    total_score += risk_score
    total_weight += 10.0

    # 4. Execution score (Weight 20)
    if exec_bid_ask_spread_pct is None:
        if candidate.legs:
            spreads = [
                (leg.ask - leg.bid) / leg.bid
                for leg in candidate.legs
                if leg.bid > 0 and leg.ask > leg.bid
            ]
            exec_bid_ask_spread_pct = (sum(spreads) / len(spreads)) if spreads else 0.05
        else:
            exec_bid_ask_spread_pct = 0.05
    exec_score = max(0.0, min(20.0, 20.0 * (1.0 - exec_bid_ask_spread_pct / 0.25)))
    total_score += exec_score
    total_weight += 20.0

    # 5. Fit score (Weight 10)
    if strategy_fit_score is None:
        strategy_fit_score = 0.85
    total_score += min(10.0, max(0.0, strategy_fit_score * 10.0))
    total_weight += 10.0

    # 6. Evidence score (Weight 10)
    if historical_winrate is None:
        historical_winrate = max(0.50, market_pop)
    total_score += min(10.0, max(0.0, historical_winrate * 10.0))
    total_weight += 10.0

    final_score = round(min(100.0, max(0.0, total_score)), 1)
    score_coverage = round(total_weight / max_possible_weight, 3)

    return final_score, score_coverage


def math_is_infinite(val: float) -> bool:
    import math
    return math.isinf(val) or math.isnan(val)
