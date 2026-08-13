"""Small-sample, transparent volatility and probability forecasting helpers."""

from __future__ import annotations

from collections.abc import Iterable
import math
import numpy as np

from .results import ScalarResult


from ..config import TRADING_DAYS_PER_YEAR
from .results import ScalarResult


def har_eod_forecast(
    prices: Iterable[float], *, horizon: int = 3, minimum_training: int = 80
) -> ScalarResult:
    """Forecast annualized RV with a log-HAR proxy with SHAR (semivariance) & HAR-Q adjustments.

    Target is un-demeaned realized variance (sum of squared returns) over future horizon.
    Includes Jensen's inequality correction (+ 0.5 * residual_variance) for log-normal forecast.
    """

    close = np.asarray(tuple(prices), dtype=float)
    if (
        close.ndim != 1
        or len(close) < minimum_training + horizon + 23
        or np.any(~np.isfinite(close))
        or np.any(close <= 0)
        or horizon < 2
    ):
        return ScalarResult(None, quality_flags=("insufficient_har_history",))

    returns = np.diff(np.log(close))
    # Un-demeaned realized variance proxy
    daily_rv = returns**2 * TRADING_DAYS_PER_YEAR
    daily_vol = np.sqrt(np.maximum(1e-8, daily_rv))
    downside_rv = np.minimum(returns, 0.0)**2 * TRADING_DAYS_PER_YEAR
    quarticity = (TRADING_DAYS_PER_YEAR / 3.0) * (returns**4)

    rows: list[list[float]] = []
    targets: list[float] = []
    last_matured = len(returns) - horizon - 1

    for position in range(21, last_matured + 1):
        future = returns[position + 1 : position + horizon + 1]
        if len(future) < 2:
            continue

        # Realized Variance over future horizon (un-demeaned)
        fut_var = float(np.sum(future**2) / len(future)) * TRADING_DAYS_PER_YEAR
        
        # Features: Daily, Weekly, Monthly RV + Downside Semivariance (SHAR) + Quarticity (HAR-Q)
        r_d = math.log(max(daily_rv[position], 1e-6))
        r_w = math.log(max(float(np.mean(daily_rv[position - 4 : position + 1])), 1e-6))
        r_m = math.log(max(float(np.mean(daily_rv[position - 21 : position + 1])), 1e-6))
        r_down = math.log(max(float(np.mean(downside_rv[position - 4 : position + 1])), 1e-6))
        rq = math.sqrt(max(float(np.mean(quarticity[position - 4 : position + 1])), 1e-6))

        rows.append([1.0, r_d, r_w, r_m, r_down, rq])
        targets.append(math.log(max(fut_var, 1e-6)))

    if len(rows) < minimum_training:
        return ScalarResult(None, quality_flags=("insufficient_har_training",))

    X = np.asarray(rows)
    y = np.asarray(targets)
    beta = np.linalg.lstsq(X, y, rcond=None)[0]
    
    # Jensen's inequality correction factor for log-normal distribution: exp(E[log X] + 0.5 * Var(res))
    residuals = y - X @ beta
    sigma2_resid = float(np.var(residuals, ddof=len(beta))) if len(residuals) > len(beta) else 0.0

    current = np.asarray(
        [
            1.0,
            math.log(max(daily_rv[-1], 1e-6)),
            math.log(max(float(np.mean(daily_rv[-5:])), 1e-6)),
            math.log(max(float(np.mean(daily_rv[-22:])), 1e-6)),
            math.log(max(float(np.mean(downside_rv[-5:])), 1e-6)),
            math.sqrt(max(float(np.mean(quarticity[-5:])), 1e-6)),
        ]
    )
    
    forecast_log_var = float(current @ beta)
    forecast_var = float(math.exp(forecast_log_var + 0.5 * sigma2_resid))
    forecast_vol = math.sqrt(max(1e-6, forecast_var))
    return ScalarResult(min(2.0, max(0.01, forecast_vol)))


def gjr_eod_forecast(
    returns: Iterable[float],
    *,
    alpha: float = 0.06,
    gamma: float = 0.08,
    beta: float = 0.86,
    optimize_params: bool = True,
) -> ScalarResult:
    """GJR-GARCH EOD forecast with parameter optimization via QMLE on expanding window."""

    values = np.asarray(tuple(returns), dtype=float)
    if values.ndim != 1 or len(values) < 30 or np.any(~np.isfinite(values)):
        return ScalarResult(None, quality_flags=("insufficient_gjr_history",))

    # Grid search optimization for QMLE parameters if requested
    if optimize_params and len(values) >= 100:
        best_nll = float("inf")
        best_params = (alpha, gamma, beta)
        
        # Coarse grid search for stable stationary GJR-GARCH parameters
        for a_c in [0.03, 0.06, 0.09]:
            for g_c in [0.04, 0.08, 0.12]:
                for b_c in [0.80, 0.85, 0.90]:
                    if a_c + g_c / 2.0 + b_c < 0.99:
                        uncond = float(np.var(values, ddof=0))
                        om = uncond * (1.0 - a_c - g_c / 2.0 - b_c)
                        v_t = uncond
                        nll = 0.0
                        for res in values:
                            v_t = om + a_c * res**2 + g_c * (res**2) * (res < 0) + b_c * v_t
                            if v_t <= 0:
                                nll = float("inf")
                                break
                            nll += math.log(v_t) + (res**2) / v_t
                        if nll < best_nll:
                            best_nll = nll
                            best_params = (a_c, g_c, b_c)
        alpha, gamma, beta = best_params

    if min(alpha, gamma, beta) < 0 or alpha + gamma / 2.0 + beta >= 1.0:
        return ScalarResult(None, quality_flags=("invalid_gjr_parameters",))

    unconditional = float(np.var(values, ddof=0))
    omega = unconditional * (1.0 - alpha - gamma / 2.0 - beta)
    variance = unconditional
    for residual in values:
        variance = (
            omega
            + alpha * residual**2
            + gamma * residual**2 * (residual < 0)
            + beta * variance
        )
    return ScalarResult(math.sqrt(max(variance, 0.0) * TRADING_DAYS_PER_YEAR))


def variance_risk_premium(
    implied_volatility_decimal: float, physical_forecast_decimal: float
) -> ScalarResult:
    """Calculate VRP strictly in Variance Space (IV^2 - RV^2)."""
    if (
        not math.isfinite(implied_volatility_decimal)
        or not math.isfinite(physical_forecast_decimal)
        or min(implied_volatility_decimal, physical_forecast_decimal) < 0
    ):
        return ScalarResult(None, quality_flags=("invalid_matched_vrp_input",))
    return ScalarResult(implied_volatility_decimal**2 - physical_forecast_decimal**2)


def qlike(actual_variance: np.ndarray, forecast_variance: np.ndarray) -> float:
    """Mean QLIKE loss; both arrays must be positive variances."""

    valid = (
        np.isfinite(actual_variance)
        & np.isfinite(forecast_variance)
        & (actual_variance > 0)
        & (forecast_variance > 0)
    )
    if not np.any(valid):
        return math.nan
    ratio = actual_variance[valid] / forecast_variance[valid]
    return float(np.mean(ratio - np.log(ratio) - 1))

