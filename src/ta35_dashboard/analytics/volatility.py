"""End-of-day volatility estimators used by the Lite dashboard."""

from __future__ import annotations

import math
from collections.abc import Iterable

import numpy as np

from .results import ScalarResult


def _array(values: Iterable[float], minimum: int = 1) -> np.ndarray | None:
    result = np.asarray(tuple(values), dtype=float)
    if result.ndim != 1 or len(result) < minimum or not np.all(np.isfinite(result)):
        return None
    return result


def expected_move(
    level: float,
    annualized_volatility: float,
    horizon_days: float,
    *,
    days_per_year: float = 252.0,
) -> ScalarResult:
    if not all(
        math.isfinite(value)
        for value in (level, annualized_volatility, horizon_days, days_per_year)
    ):
        return ScalarResult(None, quality_flags=("invalid_non_finite_input",))
    if (
        level <= 0
        or annualized_volatility < 0
        or horizon_days < 0
        or days_per_year <= 0
    ):
        return ScalarResult(None, quality_flags=("invalid_expected_move_input",))
    return ScalarResult(
        level * annualized_volatility * math.sqrt(horizon_days / days_per_year)
    )


def probability_band(
    level: float,
    annualized_volatility: float,
    horizon_days: float,
    standard_deviations: float,
    *,
    days_per_year: float = 252.0,
) -> tuple[float, float] | None:
    """Symmetric normal-return range around ``level`` for a trading horizon."""

    if not math.isfinite(standard_deviations) or standard_deviations < 0:
        return None
    move = expected_move(
        level,
        annualized_volatility,
        horizon_days,
        days_per_year=days_per_year,
    ).value
    if move is None:
        return None
    width = standard_deviations * move
    return max(0.0, level - width), level + width


def realized_volatility(
    prices: Iterable[float], *, periods_per_year: float = 252.0
) -> ScalarResult:
    values = _array(prices, 3)
    if values is None or periods_per_year <= 0:
        return ScalarResult(
            None, quality_flags=("insufficient_or_invalid_price_history",)
        )
    if np.any(values <= 0):
        return ScalarResult(None, quality_flags=("invalid_non_positive_price",))
    return ScalarResult(
        float(np.std(np.diff(np.log(values)), ddof=1) * math.sqrt(periods_per_year))
    )


def ewma_volatility_forecast(
    returns: Iterable[float],
    *,
    decay: float = 0.94,
    periods_per_year: float = 252.0,
    initial_variance: float | None = None,
) -> ScalarResult:
    values = _array(returns, 2)
    if values is None or not 0 < decay < 1 or periods_per_year <= 0:
        return ScalarResult(None, quality_flags=("invalid_ewma_input",))
    variance = (
        float(np.var(values, ddof=1)) if initial_variance is None else initial_variance
    )
    if not math.isfinite(variance) or variance < 0:
        return ScalarResult(None, quality_flags=("invalid_initial_variance",))
    for value in values:
        variance = decay * variance + (1 - decay) * float(value) ** 2
    return ScalarResult(math.sqrt(variance * periods_per_year))


def parkinson_volatility(
    highs: Iterable[float], lows: Iterable[float], *, periods_per_year: float = 252.0
) -> ScalarResult:
    high, low = _array(highs, 2), _array(lows, 2)
    if (
        high is None
        or low is None
        or len(high) != len(low)
        or np.any(low <= 0)
        or np.any(high < low)
    ):
        return ScalarResult(None, quality_flags=("invalid_parkinson_input",))
    variance = float(np.mean(np.log(high / low) ** 2) / (4 * math.log(2)))
    return ScalarResult(math.sqrt(max(variance, 0) * periods_per_year))


def yang_zhang_volatility(
    opens: Iterable[float],
    highs: Iterable[float],
    lows: Iterable[float],
    closes: Iterable[float],
    *,
    periods_per_year: float = 252.0,
) -> ScalarResult:
    o, h, low, c = (_array(values, 3) for values in (opens, highs, lows, closes))
    if any(value is None for value in (o, h, low, c)):
        return ScalarResult(None, quality_flags=("insufficient_ohlc_history",))
    assert o is not None and h is not None and low is not None and c is not None
    if (
        len({len(o), len(h), len(low), len(c)}) != 1
        or np.any(low <= 0)
        or np.any(h < low)
    ):
        return ScalarResult(None, quality_flags=("invalid_yang_zhang_input",))
    overnight = np.log(o[1:] / c[:-1])
    open_close = np.log(c / o)
    rs = np.log(h / o) * np.log(h / c) + np.log(low / o) * np.log(low / c)
    n = len(c)
    k = 0.34 / (1.34 + (n + 1) / (n - 1))
    variance = float(
        np.var(overnight, ddof=1)
        + k * np.var(open_close, ddof=1)
        + (1 - k) * np.mean(rs)
    )
    return ScalarResult(math.sqrt(max(variance, 0) * periods_per_year))


def gap_variance_share(opens: Iterable[float], closes: Iterable[float]) -> ScalarResult:
    o, c = _array(opens, 3), _array(closes, 3)
    if o is None or c is None or len(o) != len(c) or np.any(o <= 0) or np.any(c <= 0):
        return ScalarResult(None, quality_flags=("insufficient_ohlc_history",))
    gap_variance = float(np.mean(np.log(o[1:] / c[:-1]) ** 2))
    intraday_variance = float(np.mean(np.log(c[1:] / o[1:]) ** 2))
    total = gap_variance + intraday_variance
    return ScalarResult(gap_variance / total if total else 0.0)


def percentile_rank(
    history: Iterable[float], value: float | None = None
) -> ScalarResult:
    values = _array(history, 2)
    if values is None:
        return ScalarResult(None, quality_flags=("insufficient_percentile_history",))
    target = float(values[-1] if value is None else value)
    if not math.isfinite(target):
        return ScalarResult(None, quality_flags=("invalid_percentile_value",))
    return ScalarResult(float(np.mean(values <= target)))


def zscore(history: Iterable[float], value: float | None = None) -> ScalarResult:
    values = _array(history, 3)
    if values is None:
        return ScalarResult(None, quality_flags=("insufficient_zscore_history",))
    deviation = float(np.std(values, ddof=1))
    target = float(values[-1] if value is None else value)
    return ScalarResult(
        (target - float(np.mean(values))) / deviation if deviation else 0.0
    )


def volatility_spread(implied_percent: float, realized_decimal: float) -> ScalarResult:
    if (
        not math.isfinite(implied_percent)
        or not math.isfinite(realized_decimal)
        or min(implied_percent, realized_decimal) < 0
    ):
        return ScalarResult(None, quality_flags=("invalid_volatility_spread_input",))
    return ScalarResult(implied_percent / 100.0 - realized_decimal)


def volatility_ratio(implied_percent: float, realized_decimal: float) -> ScalarResult:
    if (
        not math.isfinite(implied_percent)
        or not math.isfinite(realized_decimal)
        or implied_percent < 0
        or realized_decimal <= 0
    ):
        return ScalarResult(None, quality_flags=("invalid_volatility_ratio_input",))
    return ScalarResult((implied_percent / 100.0) / realized_decimal)
