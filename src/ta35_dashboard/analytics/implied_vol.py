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
    r: float = 0.04,
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
    r: float = 0.04,
) -> float | None:
    """Extract ATM implied volatility from a parsed option chain."""
    if not chain.quotes or spot_price <= 0:
        return None

    T = max(0.001, chain.days_to_expiration / 365.0)
    sorted_quotes = sorted(chain.quotes, key=lambda q: abs(q.strike - spot_price))
    
    ivs: list[float] = []
    for q in sorted_quotes[:3]:
        if q.call_mid is not None:
            c_iv = bs_implied_volatility(q.call_mid, spot_price, q.strike, T, "call", r)
            if c_iv is not None:
                ivs.append(c_iv)

        if q.put_mid is not None:
            p_iv = bs_implied_volatility(q.put_mid, spot_price, q.strike, T, "put", r)
            if p_iv is not None:
                ivs.append(p_iv)

    return float(np.median(ivs)) if ivs else None


def calculate_term_structure_expectations(
    weekly_chain: ParsedOptionChain | None,
    monthly_chain: ParsedOptionChain | None,
    spot_price: float,
    target_horizons: tuple[int, ...] = (1, 3, 7, 14),
    fallback_iv: float = 0.12,
) -> dict[int, HorizonExpectation]:
    """Calculate term structure implied volatilities and price ranges across target horizons."""
    iv_w = extract_atm_implied_volatility(weekly_chain, spot_price) if weekly_chain else None
    iv_m = extract_atm_implied_volatility(monthly_chain, spot_price) if monthly_chain else None

    T_w = max(0.001, (weekly_chain.days_to_expiration if weekly_chain else 2.0) / 365.0)
    T_m = max(0.001, (monthly_chain.days_to_expiration if monthly_chain else 16.0) / 365.0)

    if iv_w is None and iv_m is None:
        iv_w, iv_m = fallback_iv, fallback_iv
    elif iv_w is None:
        iv_w = iv_m
    elif iv_m is None:
        iv_m = iv_w

    var_w = (iv_w**2) * T_w
    var_m = (iv_m**2) * T_m

    results: dict[int, HorizonExpectation] = {}

    for h in target_horizons:
        T_h = h / 365.0
        if T_h <= T_w:
            iv_h = iv_w
        elif T_h >= T_m:
            iv_h = iv_m
        else:
            var_h = var_w + (var_m - var_w) * (T_h - T_w) / (T_m - T_w)
            iv_h = math.sqrt(max(0.0001, var_h / T_h))

        one_sigma = spot_price * iv_h * math.sqrt(h / 252.0)
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
