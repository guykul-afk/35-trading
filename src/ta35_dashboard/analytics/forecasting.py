"""Small-sample, transparent volatility and probability forecasting helpers."""

from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np

from .results import ScalarResult


def har_eod_forecast(
    prices: Iterable[float], *, horizon: int = 3, minimum_training: int = 80
) -> ScalarResult:
    """Forecast annualized RV with a log-HAR proxy built from EOD returns.

    The last ``horizon`` observations are never used as training targets, so
    the latest estimate only uses outcomes that would already have matured.
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
    daily = np.abs(returns) * math.sqrt(252)
    rows: list[list[float]] = []
    targets: list[float] = []
    # Feature position refers to the return ending at close[position + 1].
    last_matured = len(daily) - horizon - 1
    for position in range(21, last_matured + 1):
        future = returns[position + 1 : position + horizon + 1]
        if len(future) < 2:
            continue
        rows.append(
            [
                1.0,
                math.log(max(daily[position], 1e-6)),
                math.log(max(float(np.mean(daily[position - 4 : position + 1])), 1e-6)),
                math.log(max(float(np.mean(daily[position - 21 : position + 1])), 1e-6)),
            ]
        )
        targets.append(math.log(max(float(np.std(future, ddof=0) * math.sqrt(252)), 1e-6)))
    if len(rows) < minimum_training:
        return ScalarResult(None, quality_flags=("insufficient_har_training",))
    beta = np.linalg.lstsq(np.asarray(rows), np.asarray(targets), rcond=None)[0]
    current = np.asarray(
        [
            1.0,
            math.log(max(daily[-1], 1e-6)),
            math.log(max(float(np.mean(daily[-5:])), 1e-6)),
            math.log(max(float(np.mean(daily[-22:])), 1e-6)),
        ]
    )
    forecast = float(math.exp(float(current @ beta)))
    return ScalarResult(min(2.0, max(0.01, forecast)))


def gjr_eod_forecast(
    returns: Iterable[float],
    *,
    alpha: float = 0.06,
    gamma: float = 0.08,
    beta: float = 0.86,
) -> ScalarResult:
    """Fixed-parameter GJR-style EOD benchmark with a leverage term."""

    values = np.asarray(tuple(returns), dtype=float)
    if values.ndim != 1 or len(values) < 30 or np.any(~np.isfinite(values)):
        return ScalarResult(None, quality_flags=("insufficient_gjr_history",))
    if min(alpha, gamma, beta) < 0 or alpha + gamma / 2 + beta >= 1:
        return ScalarResult(None, quality_flags=("invalid_gjr_parameters",))
    unconditional = float(np.var(values, ddof=0))
    omega = unconditional * (1 - alpha - gamma / 2 - beta)
    variance = unconditional
    for residual in values:
        variance = (
            omega
            + alpha * residual**2
            + gamma * residual**2 * (residual < 0)
            + beta * variance
        )
    return ScalarResult(math.sqrt(max(variance, 0.0) * 252))


def variance_risk_premium(
    implied_volatility_decimal: float, physical_forecast_decimal: float
) -> ScalarResult:
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
