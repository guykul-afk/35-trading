"""Layer 4: Dual Distribution Edge Engine.

Computes Risk-Neutral Market EV (P_market x Payoff) vs Empirical Model EV (P_model x Payoff).
The difference post-costs is the Estimated Edge.
"""

from __future__ import annotations

import math
from typing import Sequence

from ta35_dashboard.config import CALENDAR_DAYS_PER_YEAR
from ta35_dashboard.decision_engine.models import CandidateTrade, ModelDistribution


def _norm_ppf(p: float) -> float:
    """Normal quantile function (Phi^-1) with fallback to math.erf binary search."""
    try:
        from scipy.stats import norm
        return float(norm.ppf(p))
    except ImportError:
        # Fallback using binary search over math.erf
        # Phi(x) = 0.5 * (1 + erf(x / sqrt(2)))
        p_c = max(0.000001, min(0.999999, p))
        low = -10.0
        high = 10.0
        for _ in range(50):
            mid = (low + high) / 2.0
            p_mid = 0.5 * (1.0 + math.erf(mid / math.sqrt(2.0)))
            if p_mid < p_c:
                low = mid
            else:
                high = mid
        return float((low + high) / 2.0)


def evaluate_payoff_at_spot(candidate: CandidateTrade, spot_at_exp: float) -> float:
    """Calculates the net P&L (in NIS) of a candidate trade at expiration for a given spot price."""
    mult = 50.0  # TASE TA-35 multiplier
    pnl = 0.0
    for leg in candidate.legs:
        if leg.option_type == "CALL":
            intrinsic = max(0.0, spot_at_exp - leg.strike)
        else:
            intrinsic = max(0.0, leg.strike - spot_at_exp)
            
        if leg.action == "BUY":
            pnl += (intrinsic - leg.executable_price) * leg.ratio * mult
        else:
            pnl += (leg.executable_price - intrinsic) * leg.ratio * mult
            
    return pnl


def compute_dual_distribution_edge(
    candidate: CandidateTrade,
    spot_price: float,
    model_dist: ModelDistribution,
    fees_per_leg_nis: float = 3.0,
    expected_slippage_nis: float = 5.0,
) -> tuple[float, float, float, float]:
    """Computes (market_ev, model_ev_after_costs, estimated_edge, market_pop).
    
    Uses numerical integration over a lognormal / calibrated grid.
    """
    total_legs = sum(l.ratio for l in candidate.legs)
    total_costs = (fees_per_leg_nis * total_legs) + expected_slippage_nis
    
    # 1. Model Distribution (Log-normal around spot with model direction & RV)
    forecast_rv = max(0.05, model_dist.forecast_rv)
    days_to_exp = max(1.0, candidate.expiry.days_to_expiration)
    t_years = days_to_exp / CALENDAR_DAYS_PER_YEAR
    sigma_t = forecast_rv * math.sqrt(t_years)
    
    # Adjust drift for model direction probability: sigma_t * Phi^-1(p)
    prob_up = max(0.001, min(0.999, model_dist.direction_probability))
    drift_bias = sigma_t * _norm_ppf(prob_up)
    
    # Grid of prices around spot (from -4 sigma to +4 sigma)
    steps = 100
    grid_min = spot_price * math.exp(-4.0 * sigma_t)
    grid_max = spot_price * math.exp(4.0 * sigma_t)
    step_size = (grid_max - grid_min) / steps

    model_ev_raw = 0.0
    market_ev_raw = 0.0
    market_prof_weight = 0.0
    total_model_weight = 0.0
    total_market_weight = 0.0

    for i in range(steps):
        s_i = grid_min + (i + 0.5) * step_size
        payoff = evaluate_payoff_at_spot(candidate, s_i)
        
        # Model PDF (log-normal with direction bias)
        z_model = (math.log(s_i / spot_price) - drift_bias) / sigma_t
        w_model = math.exp(-0.5 * z_model * z_model) / (s_i * sigma_t * math.sqrt(2 * math.pi))
        
        # Market PDF (risk-neutral log-normal centered at spot)
        z_market = math.log(s_i / spot_price) / sigma_t
        w_market = math.exp(-0.5 * z_market * z_market) / (s_i * sigma_t * math.sqrt(2 * math.pi))

        model_ev_raw += payoff * w_model * step_size
        market_ev_raw += payoff * w_market * step_size

        total_model_weight += w_model * step_size
        total_market_weight += w_market * step_size
        
        if payoff > 0:
            market_prof_weight += w_market * step_size

    # Normalize EV
    if total_model_weight > 0:
        model_ev_raw /= total_model_weight
    if total_market_weight > 0:
        market_ev_raw /= total_market_weight
        market_pop = market_prof_weight / total_market_weight
    else:
        market_pop = 0.5

    model_ev_after_costs = model_ev_raw - total_costs
    market_ev_after_costs = market_ev_raw - total_costs
    estimated_edge = model_ev_after_costs - market_ev_after_costs

    return market_ev_after_costs, model_ev_after_costs, estimated_edge, market_pop
