"""Implied Volatility Solver and Term Structure Modeling.

Calculates Black-Scholes ATM option pricing, implied volatility solving via bisection,
and statistical horizon moves (1, 3, 7, 14, 30 trading days) using EOD volatility/VTA35.
Pure Python implementation using math.erf for standard normal CDF (no external scipy dependency).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


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


def calculate_term_structure_expectations_from_vol(
    spot_price: float,
    base_volatility: float,
    target_horizons: tuple[int, ...] = (1, 3, 7, 14, 30),
) -> dict[int, HorizonExpectation]:
    """Calculate term structure expectations across target horizons using annualized EOD volatility."""
    results: dict[int, HorizonExpectation] = {}
    vol = max(0.01, base_volatility)

    for h in target_horizons:
        T_h = h / 365.0
        one_sigma = spot_price * vol * math.sqrt(T_h)
        two_sigma = 2.0 * one_sigma

        results[h] = HorizonExpectation(
            horizon_days=h,
            implied_volatility=vol,
            one_sigma_move=one_sigma,
            two_sigma_move=two_sigma,
            lower_1s=spot_price - one_sigma,
            upper_1s=spot_price + one_sigma,
            lower_2s=spot_price - two_sigma,
            upper_2s=spot_price + two_sigma,
        )

    return results
