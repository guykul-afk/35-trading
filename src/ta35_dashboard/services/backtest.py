"""Walk-forward backtests for dashboard arrows and strategy scenarios.

Every feature at date *t* uses observations dated no later than *t*. Outcomes
start after that close, so the report does not leak future TA-35 observations.
Strategy results are market-scenario proxies, not option P&L, because the Lite
database intentionally contains no historical option chain or premiums.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import date
from types import SimpleNamespace

import numpy as np
import pandas as pd

from ta35_dashboard.analytics import (
    downside_variance_share,
    direction,
    ewma_volatility_forecast,
    gap_variance_share,
    indicator_signal,
    recommend_strategy,
    yang_zhang_volatility,
)
from ta35_dashboard.config import TRADING_DAYS_PER_YEAR
from ta35_dashboard.storage import SQLiteRepository

BACKTEST_HORIZONS = (3, 7, 14, 30)
DEFAULT_STRENGTH_HORIZON = 14
MINIMUM_SAMPLE = 20
PRIOR_OBSERVATIONS = 20

STRATEGY_NAMES = (
    "Bull Call Spread",
    "Bear Put Spread",
    "Bull Put Spread",
    "Bear Call Spread",
    "פרפר Call שורי / Broken-Wing Butterfly",
    "פרפר Put דובי / Broken-Wing Butterfly",
    "Call Ratio Backspread 1×2",
    "Put Ratio Backspread 1×2",
    "Long Straddle / Strangle",
    "פרפר הפוך / Long Iron Condor",
    "Iron Condor",
    "Iron Butterfly",
    "Long Butterfly / Condor קנוי",
    "Calendar / Diagonal",
)


@dataclass(frozen=True, slots=True)
class SignalBacktest:
    indicator_key: str
    horizon_days: int
    axis: str
    signal_arrow: str
    observations: int
    hits: int
    hit_rate: float | None
    baseline_rate: float | None
    adjusted_hit_rate: float | None
    confidence_low: float | None
    confidence_high: float | None
    strength: int
    sample_quality: str


@dataclass(frozen=True, slots=True)
class StrategyBacktest:
    strategy_name: str
    horizon_days: int
    observations: int
    successes: int
    success_rate: float | None
    baseline_rate: float | None
    adjusted_success_rate: float | None
    confidence_low: float | None
    confidence_high: float | None
    strength: int
    sample_quality: str


@dataclass(frozen=True, slots=True)
class BacktestReport:
    start_date: date | None
    end_date: date | None
    ta35_observations: int
    indicator_results: tuple[SignalBacktest, ...]
    strategy_results: tuple[StrategyBacktest, ...]
    warnings: tuple[str, ...]

    def indicator(
        self, key: str, horizon_days: int, axis: str, signal_arrow: str
    ) -> SignalBacktest | None:
        return next(
            (
                result
                for result in self.indicator_results
                if result.indicator_key == key
                and result.horizon_days == horizon_days
                and result.axis == axis
                and result.signal_arrow == signal_arrow
            ),
            None,
        )

    def strategy(self, name: str, horizon_days: int) -> StrategyBacktest | None:
        return next(
            (
                result
                for result in self.strategy_results
                if result.strategy_name == name
                and result.horizon_days == horizon_days
            ),
            None,
        )


def _sample_quality(observations: int) -> str:
    if observations >= 100:
        return "גבוהה"
    if observations >= 40:
        return "בינונית"
    if observations >= MINIMUM_SAMPLE:
        return "נמוכה"
    return "לא מספיק"


def _wilson(hits: int, observations: int) -> tuple[float | None, float | None]:
    if observations <= 0:
        return None, None
    z = 1.959963984540054
    rate = hits / observations
    denominator = 1 + z * z / observations
    center = (rate + z * z / (2 * observations)) / denominator
    margin = (
        z
        * math.sqrt(
            rate * (1 - rate) / observations
            + z * z / (4 * observations * observations)
        )
        / denominator
    )
    return max(0.0, center - margin), min(1.0, center + margin)


def _score(hits: int, observations: int, *, baseline: float) -> tuple[int, float | None]:
    if observations <= 0:
        return 1, None
    adjusted = (hits + PRIOR_OBSERVATIONS * baseline) / (
        observations + PRIOR_OBSERVATIONS
    )
    if observations < MINIMUM_SAMPLE:
        return 1, adjusted
    edge = max(0.0, adjusted - baseline)
    scaled_edge = min(1.0, edge / 0.15)
    reliability = min(1.0, observations / 100)
    return 1 + round(9 * scaled_edge * reliability), adjusted


def _bars_frame(repository: SQLiteRepository, symbol: str) -> pd.DataFrame:
    bars = repository.bar_history(symbol, 100_000)
    if not bars:
        return pd.DataFrame()
    frame = pd.DataFrame(
        {
            "date": pd.to_datetime([bar.session_date for bar in bars]),
            "open": [bar.open for bar in bars],
            "high": [bar.high for bar in bars],
            "low": [bar.low for bar in bars],
            "close": [bar.close for bar in bars],
        }
    ).set_index("date")
    return frame[~frame.index.duplicated(keep="last")].sort_index()


def _asof(series: pd.Series, index: pd.DatetimeIndex) -> pd.Series:
    return series.reindex(series.index.union(index)).sort_index().ffill().reindex(index)


def _historical_features(repository: SQLiteRepository) -> pd.DataFrame:
    ta = _bars_frame(repository, "TA35")
    if ta.empty:
        return ta
    close = ta["close"].astype(float)
    returns = np.log(close).diff()
    for window in (5, 20, 60):
        # Population volatility keeps short and long windows on the same scale.
        # ddof=1 creates a material small-window bias (especially at h=3).
        ta[f"rv_{window}"] = returns.rolling(window).std(ddof=0) * math.sqrt(TRADING_DAYS_PER_YEAR)

    ewma_values = np.full(len(ta), np.nan)
    yz_values = np.full(len(ta), np.nan)
    gap_values = np.full(len(ta), np.nan)
    for position in range(len(ta)):
        if position >= 60:
            window_returns = returns.iloc[position - 59 : position + 1].to_numpy()
            ewma_values[position] = ewma_volatility_forecast(window_returns).value
        if position >= 19:
            window = ta.iloc[position - 19 : position + 1]
            if window[["open", "high", "low"]].notna().all().all():
                yz_values[position] = yang_zhang_volatility(
                    window["open"], window["high"], window["low"], window["close"]
                ).value
                gap_values[position] = gap_variance_share(
                    window["open"], window["close"]
                ).value
    ta["rv_ewma"] = ewma_values
    ta["rv_yang_zhang_20"] = yz_values
    ta["gap_share_20"] = gap_values
    ta["rv_acceleration"] = ta["rv_5"] / ta["rv_20"]
    ta["rv_20_60_ratio"] = ta["rv_20"] / ta["rv_60"]
    rv_median_120 = ta["rv_20"].rolling(120, min_periods=60).median()
    ta["rv_level_ratio"] = ta["rv_20"] / rv_median_120
    ta["rv_level_bucket"] = pd.cut(
        ta["rv_level_ratio"],
        bins=[-np.inf, 0.85, 1.15, np.inf],
        labels=["low", "mid", "high"],
    ).astype(object)

    previous_close = close.shift(1)
    true_range = pd.concat(
        [
            ta["high"] - ta["low"],
            (ta["high"] - previous_close).abs(),
            (ta["low"] - previous_close).abs(),
        ],
        axis=1,
    ).max(axis=1, skipna=False)
    atr5 = true_range.rolling(5).mean() / close
    atr20 = true_range.rolling(20).mean() / close
    ta["atr_5_20_ratio"] = atr5 / atr20

    ta["downside_share_20"] = returns.rolling(20).apply(
        lambda values: downside_variance_share(values).value, raw=True
    )
    rs_daily = (
        np.log(ta["high"] / ta["close"]) * np.log(ta["high"] / ta["open"])
        + np.log(ta["low"] / ta["close"]) * np.log(ta["low"] / ta["open"])
    ).clip(lower=0)
    ta["rs_range_5_20"] = np.sqrt(
        rs_daily.rolling(5).mean() / rs_daily.rolling(20).mean()
    ).replace([np.inf, -np.inf], np.nan)
    log_price = np.log(close)
    absolute_path = returns.abs().rolling(20).sum()
    ta["trend_efficiency_20"] = (
        (log_price - log_price.shift(20)) / absolute_path
    ).replace([np.inf, -np.inf], np.nan)
    ta["range_position_20"] = range_position = (
        (close - close.rolling(20).min())
        / (close.rolling(20).max() - close.rolling(20).min())
    ).replace([np.inf, -np.inf], np.nan)
    ta["reversal_5_vol_scaled"] = (
        -(log_price - log_price.shift(5)) / (ta["rv_20"] * math.sqrt(5 / TRADING_DAYS_PER_YEAR))
    ).replace([np.inf, -np.inf], np.nan)

    candidates = pd.concat(
        [ta["rv_5"], ta["rv_20"], ta["rv_ewma"], ta["rv_yang_zhang_20"]],
        axis=1,
    )
    ta["forecast_rv_3d"] = candidates.median(axis=1, skipna=True)
    ta["expected_move_3d_points"] = (
        close * ta["forecast_rv_3d"] * math.sqrt(3 / TRADING_DAYS_PER_YEAR)
    )

    vta = _bars_frame(repository, "VTA35")
    if not vta.empty:
        vta_close = vta["close"].astype(float)
        vta_frame = pd.DataFrame(index=vta.index)
        vta_frame["vta35"] = vta_close
        vta_frame["vta35_change_5d"] = vta_close.pct_change(5)
        vta_frame["vta_vol_of_vol_20"] = np.log(vta_close).diff().rolling(20).std(ddof=1)
        mean60 = vta_close.rolling(60).mean()
        std60 = vta_close.rolling(60).std(ddof=1)
        vta_frame["vta35_zscore_60"] = (vta_close - mean60) / std60
        vta_frame["vta35_percentile_252"] = vta_close.rolling(
            252, min_periods=2
        ).apply(lambda values: float(np.mean(values <= values[-1])), raw=True)
        for column in vta_frame:
            ta[column] = _asof(vta_frame[column], ta.index)
    else:
        for column in (
            "vta35",
            "vta35_change_5d",
            "vta35_zscore_60",
            "vta35_percentile_252",
            "vta_vol_of_vol_20",
        ):
            ta[column] = np.nan
    ta["vrp_spread"] = ta["vta35"] / 100 - ta["rv_20"]
    local_iv_votes = pd.DataFrame(
        {
            "change": np.sign(ta["vta35_change_5d"]),
            "level": np.sign(ta["vta35_zscore_60"]),
            "vrp": np.sign(ta["vrp_spread"]),
        },
        index=ta.index,
    )
    ta["local_iv_family_score"] = local_iv_votes.mean(axis=1)

    usd = _bars_frame(repository, "USDILS")
    usd_change = (
        _asof(usd["close"].astype(float).pct_change(5), ta.index)
        if not usd.empty
        else np.nan
    )
    ta["usdils_change_5d"] = usd_change
    ta["fx_equity_state"] = -np.sign(usd_change) * np.sign(close.pct_change(5))
    ta_returns = close.pct_change()
    if not vta.empty:
        vta_returns = _asof(vta["close"].astype(float).pct_change(), ta.index)
        ta["ta35_vta35_corr_60"] = ta_returns.rolling(60).corr(vta_returns)
    else:
        ta["ta35_vta35_corr_60"] = np.nan

    aligned: dict[str, pd.Series] = {}
    for symbol in ("VIX9D", "VIX", "VIX3M"):
        frame = _bars_frame(repository, symbol)
        # A US close becomes observable in Israel on the following calendar
        # day. Moving the availability index by one day preserves Friday's
        # close for Sunday while preventing same-date Mon-Thu look-ahead.
        available = frame["close"].astype(float).copy()
        available.index = available.index + pd.Timedelta(days=1)
        aligned[symbol] = (
            _asof(available, ta.index)
            if not frame.empty
            else pd.Series(np.nan, index=ta.index)
        )
    ta["vix_curve_ratio"] = aligned["VIX9D"] / aligned["VIX3M"]
    ta["vix9d_vix_ratio"] = aligned["VIX9D"] / aligned["VIX"]
    ta["vix_vix3m_ratio"] = aligned["VIX"] / aligned["VIX3M"]
    ta["vix_slope"] = (aligned["VIX9D"] / aligned["VIX"]) - (aligned["VIX"] / aligned["VIX3M"])

    banks = _bars_frame(repository, "TA_BANKS5")
    if not banks.empty:
        banks_close = _asof(banks["close"].astype(float), ta.index)
        rs = np.log(banks_close / close)
        ta["banks_rs_spread"] = rs - rs.rolling(20, min_periods=5).mean()
    else:
        ta["banks_rs_spread"] = np.nan

    # Bond & Credit indicators
    tel_gov_all = _bars_frame(repository, "TEL_GOV_ALL")
    tel_gov_10y = _bars_frame(repository, "TEL_GOV_10Y")
    tel_gov_2y = _bars_frame(repository, "TEL_GOV_2Y")
    tel_bond60 = _bars_frame(repository, "TEL_BOND60")

    gov_all_close = (
        _asof(tel_gov_all["close"].astype(float), ta.index)
        if not tel_gov_all.empty
        else pd.Series(np.nan, index=ta.index)
    )
    gov_10y_close = (
        _asof(tel_gov_10y["close"].astype(float), ta.index)
        if not tel_gov_10y.empty
        else gov_all_close
    )
    gov_2y_close = (
        _asof(tel_gov_2y["close"].astype(float), ta.index)
        if not tel_gov_2y.empty
        else pd.Series(np.nan, index=ta.index)
    )
    bond60_close = (
        _asof(tel_bond60["close"].astype(float), ta.index)
        if not tel_bond60.empty
        else pd.Series(np.nan, index=ta.index)
    )

    if not tel_bond60.empty and not tel_gov_all.empty:
        rs_credit = np.log(bond60_close / gov_all_close)
        roll_mean = rs_credit.rolling(20, min_periods=5).mean()
        roll_std = rs_credit.rolling(20, min_periods=5).std(ddof=1).clip(lower=1e-6)
        ta["credit_spread_stress"] = (rs_credit - roll_mean) / roll_std
    else:
        ta["credit_spread_stress"] = np.nan

    if not tel_gov_all.empty:
        ta_ret_5d = close.pct_change(5)
        gov_ret_5d = gov_all_close.pct_change(5)
        scale = (ta["rv_20"] * np.sqrt(5 / TRADING_DAYS_PER_YEAR)).clip(lower=1e-6)
        ta["flight_to_safety"] = (ta_ret_5d - gov_ret_5d) / scale
    else:
        ta["flight_to_safety"] = np.nan

    if not tel_gov_10y.empty and not tel_gov_2y.empty:
        slope = np.log(gov_10y_close / gov_2y_close)
        ta["yield_curve_slope"] = slope - slope.rolling(20, min_periods=5).mean()
    elif not tel_gov_10y.empty and not tel_gov_all.empty:
        slope = np.log(gov_10y_close / gov_all_close)
        ta["yield_curve_slope"] = slope - slope.rolling(20, min_periods=5).mean()
    else:
        ta["yield_curve_slope"] = np.nan

    gov_series = gov_10y_close if not tel_gov_10y.empty else gov_all_close
    if not gov_series.isna().all():
        gov_ret = gov_series.pct_change()
        gov_rv20 = gov_ret.rolling(20, min_periods=10).std(ddof=1) * np.sqrt(TRADING_DAYS_PER_YEAR)
        gov_rv5 = gov_ret.rolling(5, min_periods=3).std(ddof=1) * np.sqrt(TRADING_DAYS_PER_YEAR)
        ta["gov_move_proxy"] = gov_rv5 / gov_rv20.clip(lower=1e-6)
    else:
        ta["gov_move_proxy"] = np.nan

    local_mean = ta["vta35"].rolling(252, min_periods=120).mean()
    local_std = ta["vta35"].rolling(252, min_periods=120).std(ddof=1)
    global_mean = aligned["VIX"].rolling(252, min_periods=120).mean()
    global_std = aligned["VIX"].rolling(252, min_periods=120).std(ddof=1)
    ta["local_global_stress_spread"] = (
        (ta["vta35"] - local_mean) / local_std
        - (aligned["VIX"] - global_mean) / global_std
    )

    # Fixed-parameter GJR is a benchmark, not an automatically selected model.
    variance = float(returns.dropna().iloc[:30].var(ddof=0)) if returns.notna().sum() >= 30 else np.nan
    gjr_values = np.full(len(ta), np.nan)
    unconditional = variance
    if math.isfinite(variance):
        omega = unconditional * (1 - 0.06 - 0.08 / 2 - 0.86)
        for position, residual in enumerate(returns.fillna(0).to_numpy(dtype=float)):
            variance = omega + 0.06 * residual**2 + 0.08 * residual**2 * (residual < 0) + 0.86 * variance
            if position >= 30:
                gjr_values[position] = math.sqrt(max(variance, 0) * TRADING_DAYS_PER_YEAR)
    ta["gjr_rv_1d"] = gjr_values

    har_features = pd.DataFrame(
        {
            "const": 1.0,
            "daily": np.log((returns.abs() * math.sqrt(TRADING_DAYS_PER_YEAR)).clip(lower=1e-6)),
            "weekly": np.log(
                (returns.abs() * math.sqrt(TRADING_DAYS_PER_YEAR)).rolling(5).mean().clip(lower=1e-6)
            ),
            "monthly": np.log(
                (returns.abs() * math.sqrt(TRADING_DAYS_PER_YEAR)).rolling(22).mean().clip(lower=1e-6)
            ),
        },
        index=ta.index,
    )
    for horizon in BACKTEST_HORIZONS:
        har_target = _outcomes(ta, horizon)["forward_rv"]
        har_values = np.full(len(ta), np.nan)
        beta: np.ndarray | None = None
        har_sigma2_resid: float = 0.0
        har_columns = ["const", "daily", "weekly", "monthly"]
        for position in range(123, len(ta)):
            if beta is None or position % 5 == 0:
                train_end = position - horizon
                train = har_features.iloc[: train_end + 1].copy()
                train["target"] = np.log(
                    har_target.iloc[: train_end + 1].clip(lower=1e-6)
                )
                train = train.replace([np.inf, -np.inf], np.nan).dropna()
                if len(train) >= 80:
                    X_mat = train[har_columns].to_numpy()
                    y_vec = train["target"].to_numpy()
                    beta = np.linalg.lstsq(X_mat, y_vec, rcond=None)[0]
                    resids = y_vec - X_mat @ beta
                    har_sigma2_resid = float(np.var(resids, ddof=len(beta))) if len(resids) > len(beta) else 0.0
            current = har_features.iloc[position]
            if beta is not None and current[har_columns].notna().all():
                log_pred = float(current[har_columns].to_numpy() @ beta)
                har_values[position] = math.exp(log_pred + 0.5 * har_sigma2_resid)
        ta[f"har_rv_{horizon}d"] = har_values
        ta[f"matched_vrp_{horizon}d"] = (ta["vta35"] / 100) ** 2 - ta[f"har_rv_{horizon}d"] ** 2

        # In absence of other horizon-specific models, use the base forecast candidates for median
        ta[f"forecast_rv_{horizon}d"] = candidates.median(axis=1, skipna=True)
        ta[f"expected_move_{horizon}d_points"] = (
            close * ta[f"forecast_rv_{horizon}d"] * math.sqrt(horizon / TRADING_DAYS_PER_YEAR)
        )

    vol_inputs = pd.DataFrame(
        {
            "rv": np.where(ta["rv_20_60_ratio"] > 1, 1, -1),
            "atr": np.where(ta["atr_5_20_ratio"] > 1, 1, -1),
            "local_iv": np.sign(ta["local_iv_family_score"]),
            "vix_short": np.where(ta["vix9d_vix_ratio"] > 1, 1, -1),
            "vix_curve": np.where(ta["vix_vix3m_ratio"] > 1, 1, -1),
        },
        index=ta.index,
    )
    source_columns = (
        "rv_20_60_ratio",
        "atr_5_20_ratio",
        "local_iv_family_score",
        "vix9d_vix_ratio",
        "vix_vix3m_ratio",
    )
    vol_inputs = vol_inputs.where(ta[list(source_columns)].notna().to_numpy())
    ta["volatility_direction_score"] = vol_inputs.mean(axis=1)

    ma20, ma60 = close.rolling(20).mean(), close.rolling(60).mean()
    range_position = ta["range_position_20"]
    trend_inputs = pd.DataFrame(
        {
            "ma20": np.where(close >= ma20, 1, -1),
            "ma60": np.where(close >= ma60, 1, -1),
            "return5": np.where(close.pct_change(5) >= 0, 1, -1),
            "return20": np.where(close.pct_change(20) >= 0, 1, -1),
            "range": np.where(range_position >= 0.5, 1, -1),
        },
        index=ta.index,
    )
    trend_inputs["ma20"] = trend_inputs["ma20"].where(ma20.notna())
    trend_inputs["ma60"] = trend_inputs["ma60"].where(ma60.notna())
    trend_inputs["return5"] = trend_inputs["return5"].where(close.shift(5).notna())
    trend_inputs["return20"] = trend_inputs["return20"].where(close.shift(20).notna())
    trend_inputs["range"] = trend_inputs["range"].where(range_position.notna())
    ta["market_trend_score"] = trend_inputs.mean(axis=1)

    stress = pd.Series(0, index=ta.index, dtype=float)
    stress += (ta["vta35_percentile_252"] >= 0.8).astype(float) * 2
    stress += (ta["rv_acceleration"] >= 1.2).astype(float) * 2
    stress += (ta["gap_share_20"] >= 0.45).astype(float)
    stress += (ta["vix_curve_ratio"] >= 1).astype(float)
    stress += (ta["usdils_change_5d"] >= 0.01).astype(float)
    ta["regime"] = np.select(
        [stress >= 5, stress >= 3, stress >= 1],
        ["לחץ גבוה", "זהירות", "רגיל"],
        default="רגוע",
    )
    return ta


def _outcomes(frame: pd.DataFrame, horizon: int) -> pd.DataFrame:
    result = pd.DataFrame(index=frame.index)
    result["forward_return"] = frame["close"].shift(-horizon) / frame["close"] - 1
    forward_rv = np.full(len(frame), np.nan)
    log_close = np.log(frame["close"].to_numpy(dtype=float))
    for position in range(len(frame) - horizon):
        changes = np.diff(log_close[position : position + horizon + 1])
        if len(changes) >= 2:
            forward_rv[position] = float(np.std(changes, ddof=0) * math.sqrt(TRADING_DAYS_PER_YEAR))
    result["forward_rv"] = forward_rv
    result["volatility_direction"] = [
        (
            direction(future / trailing, neutral=1.0, deadband=0.03)
            if math.isfinite(future)
            and math.isfinite(trailing)
            and trailing > 0
            else np.nan
        )
        for future, trailing in zip(
            result["forward_rv"], frame["rv_20"], strict=True
        )
    ]
    result["market_direction"] = np.sign(result["forward_return"])
    return result


def _arrow_value(value: str) -> int | None:
    return {"↑": 1, "↓": -1, "↔": 0}.get(value)


def _signal_result(
    key: str,
    horizon: int,
    axis: str,
    signal_arrow: str,
    matches: list[bool],
    baseline: float,
) -> SignalBacktest:
    observations = len(matches)
    hits = sum(matches)
    score, adjusted = _score(hits, observations, baseline=baseline)
    low, high = _wilson(hits, observations)
    return SignalBacktest(
        indicator_key=key,
        horizon_days=horizon,
        axis=axis,
        signal_arrow=signal_arrow,
        observations=observations,
        hits=hits,
        hit_rate=hits / observations if observations else None,
        baseline_rate=baseline,
        adjusted_hit_rate=adjusted,
        confidence_low=low,
        confidence_high=high,
        strength=score,
        sample_quality=_sample_quality(observations),
    )


def _strategy_success(
    name: str,
    *,
    spot: float,
    future: float,
    forecast: float,
    horizon: int,
) -> tuple[bool, float] | None:
    width = spot * forecast * math.sqrt(horizon / TRADING_DAYS_PER_YEAR)
    lower_half, upper_half = spot - 0.5 * width, spot + 0.5 * width
    lower, upper = spot - width, spot + width
    if name == "Bull Call Spread":
        return future > spot, 0.5
    if name == "Bear Put Spread":
        return future < spot, 0.5
    if name == "Bull Put Spread":
        return future >= lower_half, 0.6915
    if name == "Bear Call Spread":
        return future <= upper_half, 0.6915
    if name == "פרפר Call שורי / Broken-Wing Butterfly":
        return spot <= future <= upper, 0.3413
    if name == "פרפר Put דובי / Broken-Wing Butterfly":
        return lower <= future <= spot, 0.3413
    if name == "Call Ratio Backspread 1×2":
        return future > upper, 0.1587
    if name == "Put Ratio Backspread 1×2":
        return future < lower, 0.1587
    if name in {"Long Straddle / Strangle", "פרפר הפוך / Long Iron Condor"}:
        return future < lower or future > upper, 0.3173
    if name == "Iron Condor":
        return lower <= future <= upper, 0.6827
    if name in {"Iron Butterfly", "Long Butterfly / Condor קנוי"}:
        return lower_half <= future <= upper_half, 0.3829
    # Calendar/Diagonal cannot be assessed without two-expiry IV history.
    return None


def run_backtest(
    repository: SQLiteRepository,
    *,
    indicator_keys: tuple[str, ...],
    horizons: tuple[int, ...] = BACKTEST_HORIZONS,
) -> BacktestReport:
    frame = _historical_features(repository)
    if frame.empty:
        return BacktestReport(
            None,
            None,
            0,
            (),
            (),
            ("אין נתוני ת״א־35 לבקטסט.",),
        )

    indicator_results: list[SignalBacktest] = []
    strategy_buckets: dict[tuple[str, int], list[bool]] = {
        (name, horizon): [] for name in STRATEGY_NAMES for horizon in horizons
    }
    strategy_baselines: dict[tuple[str, int], float] = {}

    metric_columns = set(indicator_keys) | {"rv_20"}
    for horizon in horizons:
        outcomes = _outcomes(frame, horizon)
        baselines: dict[tuple[str, str], float] = {}
        for axis, outcome_column in (
            ("volatility", "volatility_direction"),
            ("market", "market_direction"),
        ):
            valid = outcomes[outcome_column].dropna()
            if axis == "market":
                valid = valid[valid != 0]
            for signal_arrow in ("↑", "↓", "↔"):
                target = _arrow_value(signal_arrow)
                baselines[(axis, signal_arrow)] = (
                    float((valid == target).mean()) if len(valid) else 0.5
                )
        buckets: dict[tuple[str, str, str], list[bool]] = {}
        for position, (_, row) in enumerate(frame.iterrows()):
            if position + horizon >= len(frame):
                continue
            metrics = {
                name: SimpleNamespace(
                    value=(
                        float(row[name])
                        if name in row and pd.notna(row[name])
                        else None
                    )
                )
                for name in metric_columns
            }
            for key in indicator_keys:
                value = metrics[key].value if key in metrics else None
                vol_arrow, market_arrow, _, _ = indicator_signal(key, value, metrics)
                actual_vol = outcomes["volatility_direction"].iloc[position]
                predicted_vol = _arrow_value(vol_arrow)
                if predicted_vol is not None and pd.notna(actual_vol):
                    buckets.setdefault((key, "volatility", vol_arrow), []).append(
                        predicted_vol == int(actual_vol)
                    )
                actual_market = outcomes["market_direction"].iloc[position]
                predicted_market = _arrow_value(market_arrow)
                # A neutral market arrow means "no directional information",
                # not a flat-market forecast, so it is intentionally unscored.
                if (
                    predicted_market not in (None, 0)
                    and pd.notna(actual_market)
                    and int(actual_market) != 0
                ):
                    buckets.setdefault((key, "market", market_arrow), []).append(
                        predicted_market == int(actual_market)
                    )

            required = (
                row.get("forecast_rv_3d"),
                row.get("vta35"),
                row.get("market_trend_score"),
                row.get("volatility_direction_score"),
            )
            if all(pd.notna(value) for value in required):
                recommendation = recommend_strategy(
                    spot=float(row["close"]),
                    forecast_volatility=float(row["forecast_rv_3d"]),
                    implied_volatility=float(row["vta35"]) / 100,
                    trend_score=float(row["market_trend_score"]),
                    volatility_score=float(row["volatility_direction_score"]),
                    regime=str(row["regime"]),
                    horizon_days=horizon,
                    # Research evaluates the candidate rule. Deployment
                    # eligibility is a separate, forcibly closed safety gate.
                    premium_sale_eligible=True,
                )
                if recommendation.primary is not None:
                    future = float(frame["close"].iloc[position + horizon])
                    assessed = _strategy_success(
                        recommendation.primary.name,
                        spot=float(row["close"]),
                        future=future,
                        forecast=float(row["forecast_rv_3d"]),
                        horizon=horizon,
                    )
                    if assessed is not None:
                        success, baseline = assessed
                        bucket_key = (recommendation.primary.name, horizon)
                        strategy_buckets[bucket_key].append(success)
                        strategy_baselines[bucket_key] = baseline

        for key in indicator_keys:
            for axis in ("volatility", "market"):
                for signal_arrow in ("↑", "↓", "↔"):
                    matches = buckets.get((key, axis, signal_arrow), [])
                    if matches or axis == "volatility":
                        indicator_results.append(
                            _signal_result(
                                key,
                                horizon,
                                axis,
                                signal_arrow,
                                matches,
                                baselines[(axis, signal_arrow)],
                            )
                        )

    strategy_results: list[StrategyBacktest] = []
    for name in STRATEGY_NAMES:
        for horizon in horizons:
            matches = strategy_buckets[(name, horizon)]
            observations = len(matches)
            successes = sum(matches)
            baseline = strategy_baselines.get((name, horizon))
            if baseline is None:
                score, adjusted = 1, None
            else:
                score, adjusted = _score(successes, observations, baseline=baseline)
            low, high = _wilson(successes, observations)
            strategy_results.append(
                StrategyBacktest(
                    strategy_name=name,
                    horizon_days=horizon,
                    observations=observations,
                    successes=successes,
                    success_rate=(
                        successes / observations if observations else None
                    ),
                    baseline_rate=baseline,
                    adjusted_success_rate=adjusted,
                    confidence_low=low,
                    confidence_high=high,
                    strength=score,
                    sample_quality=_sample_quality(observations),
                )
            )

    return BacktestReport(
        start_date=frame.index[0].date(),
        end_date=frame.index[-1].date(),
        ta35_observations=len(frame),
        indicator_results=tuple(indicator_results),
        strategy_results=tuple(strategy_results),
        warnings=(
            "ציוני 1–10 מושבתים עד להשלמת ולידציה סטטיסטית מתוקנת.",
            "בדיקת האסטרטגיות מודדת הצלחת תרחיש מדד בלבד, לא P&L של אופציות.",
            "Calendar/Diagonal אינה ניתנת לבדיקה ללא היסטוריית IV לשתי פקיעות.",
        ),
    )
