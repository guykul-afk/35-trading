"""Implied Volatility Solver and Term Structure Interpolation.

Calculates Black-Scholes ATM implied volatility from real options quotes and
interpolates implied volatilities across target horizons (1, 3, 7, 14 trading days).
Pure Python implementation using math.erf for standard normal CDF (no external scipy dependency).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from ta35_dashboard.connectors.dde_parser import ParsedOptionChain


@dataclass(frozen=True, slots=True)
class HorizonExpectation:
    horizon_days: int
    implied_volatility: float
    one_sigma_move: float
    two_sigma_move: float
    lower_1s: float
    upper_1s: float
    lower_2s: float
    upper_2s: float


def _norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function using math.erf."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Black-Scholes European Call option price."""
    if T <= 0 or sigma <= 0:
        return max(0.0, S - K)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return S * _norm_cdf(d1) - K * math.exp(-r * T) * _norm_cdf(d2)


def bs_put_price(S: float, K: float, T: float, r: float, sigma: float) -> float:
    """Black-Scholes European Put option price."""
    if T <= 0 or sigma <= 0:
        return max(0.0, K - S)
    d1 = (math.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)
    return K * math.exp(-r * T) * _norm_cdf(-d2) - S * _norm_cdf(-d1)


def bs_implied_volatility(
    price: float,
    S: float,
    K: float,
    T: float,
    option_type: str = "call",
    r: float = 0.0,
) -> float | None:
    """Solve Black-Scholes implied volatility using bisection."""
    intrinsic = max(0.0, S - K) if option_type.lower() == "call" else max(0.0, K - S)
    if price <= intrinsic or T <= 0 or S <= 0 or K <= 0:
        return None

    low, high = 0.001, 3.0
    func = bs_call_price if option_type.lower() == "call" else bs_put_price

    for _ in range(35):
        mid = (low + high) / 2.0
        p = func(S, K, T, r, mid)
        if p < price:
            low = mid
        else:
            high = mid

    iv = (low + high) / 2.0
    return iv if 0.002 <= iv <= 2.5 else None


def extract_atm_implied_volatility(
    chain: ParsedOptionChain,
    spot_price: float,
    r: float = 0.0,
) -> float | None:
    """Extract ATM implied volatility from a parsed option chain."""
    effective_spot = chain.synthetic_spot if chain.synthetic_spot is not None else spot_price
    if not chain.quotes or effective_spot <= 0:
        return None

    T = max(0.001, chain.days_to_expiration / 365.0)
    sorted_quotes = sorted(chain.quotes, key=lambda q: abs(q.strike - effective_spot))
    
    ivs: list[float] = []
    for q in sorted_quotes[:3]:
        if q.call_mid is not None:
            c_iv = bs_implied_volatility(q.call_mid, effective_spot, q.strike, T, "call", r)
            if c_iv is not None:
                ivs.append(c_iv)

        if q.put_mid is not None:
            p_iv = bs_implied_volatility(q.put_mid, effective_spot, q.strike, T, "put", r)
            if p_iv is not None:
                ivs.append(p_iv)

    return float(np.median(ivs)) if ivs else None


def calculate_term_structure_expectations(
    weekly_chain: ParsedOptionChain | None,
    monthly_chain: ParsedOptionChain | None,
    spot_price: float,
    target_horizons: tuple[int, ...] = (1, 3, 7, 14),
    fallback_iv: float = 0.12,
    chains: list[ParsedOptionChain] | None = None,
) -> dict[int, HorizonExpectation]:
    """Calculate term structure implied volatilities and price ranges across target horizons dynamically."""
    # 1. Build a list of active chains with their extracted ATM IVs
    active_chains = []
    if chains:
        active_chains = list(chains)
    else:
        if weekly_chain:
            active_chains.append(weekly_chain)
        if monthly_chain:
            active_chains.append(monthly_chain)

    # Resolve ATM IV and expiration T for each chain
    points = []
    for c in active_chains:
        iv = extract_atm_implied_volatility(c, spot_price)
        if iv is not None:
            T = max(0.001, c.days_to_expiration / 365.0)
            points.append((T, iv, c.days_to_expiration))

    # Sort points by time to expiration
    points.sort(key=lambda p: p[0])

    # Fallback if no points parsed
    if not points:
        points = [(2.0 / 365.0, fallback_iv, 2.0), (16.0 / 365.0, fallback_iv, 16.0)]

    results: dict[int, HorizonExpectation] = {}

    for h in target_horizons:
        T_h = h / 365.0

        # Boundary conditions
        if T_h <= points[0][0]:
            iv_h = points[0][1]
        elif T_h >= points[-1][0]:
            iv_h = points[-1][1]
        else:
            # Find the bracketing points
            t_idx = 0
            for i in range(len(points) - 1):
                if points[i][0] <= T_h < points[i+1][0]:
                    t_idx = i
                    break
            
            t1, iv1, _ = points[t_idx]
            t2, iv2, _ = points[t_idx + 1]
            
            var1 = (iv1**2) * t1
            var2 = (iv2**2) * t2
            
            # Interpolate variance linearly in time
            var_h = var1 + (var2 - var1) * (T_h - t1) / (t2 - t1)
            iv_h = math.sqrt(max(0.0001, var_h / T_h))

        one_sigma = spot_price * iv_h * math.sqrt(h / 365.0)
        two_sigma = 2.0 * one_sigma

        results[h] = HorizonExpectation(
            horizon_days=h,
            implied_volatility=iv_h,
            one_sigma_move=one_sigma,
            two_sigma_move=two_sigma,
            lower_1s=spot_price - one_sigma,
            upper_1s=spot_price + one_sigma,
            lower_2s=spot_price - two_sigma,
            upper_2s=spot_price + two_sigma,
        )

    return results
