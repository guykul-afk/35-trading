"""Comprehensive, reproducible research backtests for the Lite dashboard.

The research layer deliberately separates *market-scenario* validation from
option P&L.  The local database has index, volatility-index, FX and US-volatility
history, but no historical TA-35 option chain, bid/ask quotes or expiry-matched
implied volatility.  Strategy tests therefore answer "did the market scenario
selected by the rule occur?" and never claim to estimate tradable option return.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

from ta35_dashboard.analytics import indicator_signal, qlike, recommend_strategy
from ta35_dashboard.storage import SQLiteRepository

from .backtest import (
    BACKTEST_HORIZONS,
    PRIOR_OBSERVATIONS,
    STRATEGY_NAMES,
    _arrow_value,
    _historical_features,
    _outcomes,
    _score,
    _strategy_success,
    _wilson,
)


@dataclass(frozen=True, slots=True)
class ResearchReport:
    generated_at: datetime
    start_date: object | None
    end_date: object | None
    observations: int
    tables: dict[str, pd.DataFrame]
    findings: tuple[str, ...]
    warnings: tuple[str, ...]


def _finite(value: object) -> bool:
    try:
        return bool(pd.notna(value) and math.isfinite(float(value)))
    except (TypeError, ValueError):
        return False


def _normal_sf(value: float) -> float:
    return 0.5 * math.erfc(value / math.sqrt(2))


def _proportion_pvalue(
    hits: int, observations: int, baseline: float, *, horizon: int = 1
) -> float | None:
    """Conservative one-sided test using the non-overlapping effective n."""

    if observations <= 0 or not 0 < baseline < 1:
        return None
    rate = hits / observations
    effective_n = max(1, observations // max(1, horizon))
    standard_error = math.sqrt(baseline * (1 - baseline) / effective_n)
    if standard_error == 0:
        return None
    return min(1.0, max(0.0, _normal_sf((rate - baseline) / standard_error)))


def _bh_adjust(values: pd.Series) -> pd.Series:
    """Holm adjustment, valid under arbitrary dependence.

    The function name is retained for report-schema compatibility; the values
    are conservative family-wise adjusted p-values, not BH FDR estimates.
    """

    result = pd.Series(np.nan, index=values.index, dtype=float)
    valid = values.dropna().sort_values()
    if valid.empty:
        return result
    count = len(valid)
    adjusted = np.empty(count, dtype=float)
    running = 0.0
    raw = valid.to_numpy(dtype=float)
    for index in range(count):
        running = max(running, raw[index] * (count - index))
        adjusted[index] = min(1.0, running)
    result.loc[valid.index] = adjusted
    return result


def _spearman(left: pd.Series, right: pd.Series) -> float | None:
    valid = pd.concat([left, right], axis=1).dropna()
    if len(valid) < 10 or valid.iloc[:, 0].nunique() < 2:
        return None
    value = valid.iloc[:, 0].rank().corr(valid.iloc[:, 1].rank())
    return float(value) if pd.notna(value) else None


def _quality(observations: int) -> str:
    if observations >= 200:
        return "גבוהה"
    if observations >= 80:
        return "בינונית"
    if observations >= 30:
        return "נמוכה"
    return "לא מספקת"


def _walk_forward_brier(group: pd.DataFrame, baseline: float, horizon: int) -> float | None:
    """Brier score using only labels whose horizon had elapsed at prediction time."""

    if group.empty:
        return None
    ordered = group.sort_values("position")
    settled: list[tuple[int, bool]] = []
    probabilities: list[float] = []
    outcomes: list[float] = []
    for row in ordered.itertuples(index=False):
        known = [hit for position, hit in settled if position + horizon <= row.position]
        probability = (sum(known) + PRIOR_OBSERVATIONS * baseline) / (
            len(known) + PRIOR_OBSERVATIONS
        )
        probabilities.append(probability)
        outcomes.append(float(row.hit))
        settled.append((int(row.position), bool(row.hit)))
    return float(np.mean((np.asarray(probabilities) - np.asarray(outcomes)) ** 2))


def _nonoverlap_rate(
    group: pd.DataFrame, horizon: int
) -> tuple[int, float | None, float | None, float | None]:
    if group.empty:
        return 0, None, None, None
    rates: list[float] = []
    sizes: list[int] = []
    positions = group["position"].astype(int)
    for offset in range(horizon):
        sample = group[positions % horizon == offset]
        if len(sample):
            rates.append(float(sample["hit"].mean()))
            sizes.append(len(sample))
    return (
        min(sizes) if sizes else 0,
        float(np.min(rates)) if rates else None,
        float(np.median(rates)) if rates else None,
        float(np.max(rates)) if rates else None,
    )


def _indicator_records(
    frame: pd.DataFrame,
    indicator_keys: tuple[str, ...],
    horizons: tuple[int, ...],
) -> pd.DataFrame:
    metric_columns = set(indicator_keys) | {"rv_20"}
    records: list[dict[str, object]] = []
    for horizon in horizons:
        outcomes = _outcomes(frame, horizon)
        for position, (timestamp, row) in enumerate(frame.iterrows()):
            if position + horizon >= len(frame):
                continue
            metrics = {
                name: SimpleNamespace(
                    value=float(row[name]) if name in row and _finite(row[name]) else None
                )
                for name in metric_columns
            }
            future_rv = outcomes["forward_rv"].iloc[position]
            trailing_rv = row.get("rv_20")
            vol_change = (
                math.log(float(future_rv) / float(trailing_rv))
                if _finite(future_rv) and _finite(trailing_rv) and float(trailing_rv) > 0
                else np.nan
            )
            forward_return = outcomes["forward_return"].iloc[position]
            for key in indicator_keys:
                value = metrics[key].value if key in metrics else None
                vol_arrow, market_arrow, _, _ = indicator_signal(key, value, metrics)
                for axis, predicted_arrow, actual, continuous in (
                    (
                        "volatility",
                        vol_arrow,
                        outcomes["volatility_direction"].iloc[position],
                        vol_change,
                    ),
                    (
                        "market",
                        market_arrow,
                        outcomes["market_direction"].iloc[position],
                        forward_return,
                    ),
                ):
                    predicted = _arrow_value(predicted_arrow)
                    if predicted is None or not _finite(actual):
                        continue
                    if axis == "market" and (predicted == 0 or int(actual) == 0):
                        continue
                    records.append(
                        {
                            "date": timestamp,
                            "year": int(timestamp.year),
                            "position": position,
                            "horizon": horizon,
                            "indicator": key,
                            "axis": axis,
                            "arrow": predicted_arrow,
                            "predicted": predicted,
                            "actual": int(actual),
                            "hit": predicted == int(actual),
                            "value": value,
                            "continuous_outcome": continuous,
                            "regime": str(row.get("regime", "לא זמין")),
                            "rv_level_bucket": row.get("rv_level_bucket", "unknown"),
                        }
                    )
    return pd.DataFrame(records)


def _marginal_baseline(group: pd.DataFrame) -> float:
    """Class-marginal baseline conditioned on the current RV-level bucket."""

    weighted = 0.0
    for _, sample in group.groupby("rv_level_bucket", dropna=False):
        actual_rates = sample["actual"].value_counts(normalize=True)
        prediction_rates = sample["predicted"].value_counts(normalize=True)
        bucket_rate = sum(
            prediction_rates.get(value, 0.0) * actual_rates.get(value, 0.0)
            for value in (-1, 0, 1)
        )
        weighted += len(sample) / len(group) * bucket_rate
    return float(weighted)


def _indicator_tables(records: pd.DataFrame) -> dict[str, pd.DataFrame]:
    aggregate_rows: list[dict[str, object]] = []
    arrow_rows: list[dict[str, object]] = []
    regime_rows: list[dict[str, object]] = []
    year_rows: list[dict[str, object]] = []
    intensity_rows: list[dict[str, object]] = []

    aggregate_keys = ["indicator", "horizon", "axis"]
    for keys, group in records.groupby(aggregate_keys, sort=True):
        indicator, horizon, axis = keys
        baseline = _marginal_baseline(group)
        hits = int(group["hit"].sum())
        observations = len(group)
        accuracy = hits / observations
        low, high = _wilson(hits, observations)
        nonoverlap_n, nonoverlap_min, nonoverlap_median, nonoverlap_max = (
            _nonoverlap_rate(group, int(horizon))
        )
        signal_rank = group["value"].rank(pct=True) - 0.5
        signal_score = group["predicted"] * signal_rank.abs()
        ic = _spearman(signal_score, group["continuous_outcome"])
        valid_score = pd.DataFrame(
            {"score": signal_score, "outcome": group["continuous_outcome"]}
        ).dropna()
        quintile_spread = None
        if len(valid_score) >= 40 and valid_score["score"].nunique() >= 5:
            low_cut = valid_score["score"].quantile(0.2)
            high_cut = valid_score["score"].quantile(0.8)
            quintile_spread = float(
                valid_score.loc[valid_score["score"] >= high_cut, "outcome"].mean()
                - valid_score.loc[valid_score["score"] <= low_cut, "outcome"].mean()
            )
        score, adjusted = _score(hits, observations, baseline=baseline)
        yearly = []
        for _, sample in group.groupby("year"):
            if len(sample) >= 10:
                yearly.append(float(sample["hit"].mean()) - _marginal_baseline(sample))
        regimes = []
        for _, sample in group.groupby("regime"):
            if len(sample) >= 10:
                regimes.append(float(sample["hit"].mean()) - _marginal_baseline(sample))
        aggregate_rows.append(
            {
                "indicator": indicator,
                "horizon": horizon,
                "axis": axis,
                "n": observations,
                "accuracy": accuracy,
                "baseline": baseline,
                "lift": accuracy - baseline,
                "adjusted_accuracy": adjusted,
                "ci_low": low,
                "ci_high": high,
                "p_value": _proportion_pvalue(
                    hits, observations, baseline, horizon=int(horizon)
                ),
                "strength": score,
                "brier_walk_forward": _walk_forward_brier(group, baseline, int(horizon)),
                "brier_baseline": baseline * (1 - baseline),
                "nonoverlap_n_min": nonoverlap_n,
                "n_eff": observations // int(horizon),
                "nonoverlap_accuracy_min": nonoverlap_min,
                "nonoverlap_accuracy": nonoverlap_median,
                "nonoverlap_accuracy_max": nonoverlap_max,
                "rank_ic": ic,
                "top_bottom_quintile_spread": quintile_spread,
                "positive_years": sum(value > 0 for value in yearly),
                "tested_years": len(yearly),
                "positive_regimes": sum(value > 0 for value in regimes),
                "tested_regimes": len(regimes),
                "sample_quality": _quality(observations),
            }
        )

        absolute_rank = (group["value"].rank(pct=True) - 0.5).abs()
        for retained, quantile in (("all", 0.0), ("top 50% intensity", 0.5), ("top 25% intensity", 0.75)):
            sample = group[absolute_rank >= absolute_rank.quantile(quantile)]
            if sample.empty:
                continue
            sample_baseline = _marginal_baseline(sample)
            intensity_rows.append(
                {
                    "indicator": indicator,
                    "horizon": horizon,
                    "axis": axis,
                    "filter": retained,
                    "n": len(sample),
                    "accuracy": float(sample["hit"].mean()),
                    "baseline": sample_baseline,
                    "lift": float(sample["hit"].mean()) - sample_baseline,
                }
            )

    aggregate = pd.DataFrame(aggregate_rows)
    if not aggregate.empty:
        aggregate["fdr_q"] = _bh_adjust(aggregate["p_value"])

    for keys, group in records.groupby(
        ["indicator", "horizon", "axis", "arrow"], sort=True
    ):
        indicator, horizon, axis, arrow = keys
        observations = len(group)
        hits = int(group["hit"].sum())
        # Conditional baseline: unconditional frequency of the class predicted
        # by this arrow within the same indicator/horizon/axis sample.
        parent = records[
            (records["indicator"] == indicator)
            & (records["horizon"] == horizon)
            & (records["axis"] == axis)
        ]
        predicted = int(group["predicted"].iloc[0])
        baseline = float((parent["actual"] == predicted).mean())
        low, high = _wilson(hits, observations)
        score, adjusted = _score(hits, observations, baseline=baseline)
        nonoverlap_n, nonoverlap_min, nonoverlap_median, nonoverlap_max = (
            _nonoverlap_rate(group, int(horizon))
        )
        arrow_rows.append(
            {
                "indicator": indicator,
                "horizon": horizon,
                "axis": axis,
                "arrow": arrow,
                "n": observations,
                "hits": hits,
                "hit_rate": hits / observations,
                "baseline": baseline,
                "lift": hits / observations - baseline,
                "adjusted_hit_rate": adjusted,
                "ci_low": low,
                "ci_high": high,
                "p_value": _proportion_pvalue(
                    hits, observations, baseline, horizon=int(horizon)
                ),
                "strength": score,
                "nonoverlap_n_min": nonoverlap_n,
                "n_eff": observations // int(horizon),
                "nonoverlap_hit_rate_min": nonoverlap_min,
                "nonoverlap_hit_rate": nonoverlap_median,
                "nonoverlap_hit_rate_max": nonoverlap_max,
                "sample_quality": _quality(observations),
            }
        )
    arrows = pd.DataFrame(arrow_rows)
    if not arrows.empty:
        arrows["fdr_q"] = _bh_adjust(arrows["p_value"])

    for dimensions, destination in (("regime", regime_rows), ("year", year_rows)):
        for keys, group in records.groupby(
            ["indicator", "horizon", "axis", dimensions], sort=True
        ):
            indicator, horizon, axis, segment = keys
            if len(group) < 8:
                continue
            baseline = _marginal_baseline(group)
            rate = float(group["hit"].mean())
            destination.append(
                {
                    "indicator": indicator,
                    "horizon": horizon,
                    "axis": axis,
                    dimensions: segment,
                    "n": len(group),
                    "accuracy": rate,
                    "baseline": baseline,
                    "lift": rate - baseline,
                }
            )

    return {
        "indicator_aggregate": aggregate,
        "indicator_by_arrow": arrows,
        "indicator_intensity": pd.DataFrame(intensity_rows),
        "indicator_by_regime": pd.DataFrame(regime_rows),
        "indicator_by_year": pd.DataFrame(year_rows),
    }


def _strategy_score(name: str, normalized_move: float) -> float | None:
    if name == "Bull Call Spread":
        return normalized_move
    if name == "Bear Put Spread":
        return -normalized_move
    if name == "Bull Put Spread":
        return normalized_move + 0.5
    if name == "Bear Call Spread":
        return 0.5 - normalized_move
    if name == "פרפר Call שורי / Broken-Wing Butterfly":
        return 0.5 - abs(normalized_move - 0.5)
    if name == "פרפר Put דובי / Broken-Wing Butterfly":
        return 0.5 - abs(normalized_move + 0.5)
    if name == "Call Ratio Backspread 1×2":
        return normalized_move - 1
    if name == "Put Ratio Backspread 1×2":
        return -normalized_move - 1
    if name in {"Long Straddle / Strangle", "פרפר הפוך / Long Iron Condor"}:
        return abs(normalized_move) - 1
    if name == "Iron Condor":
        return 1 - abs(normalized_move)
    if name in {"Iron Butterfly", "Long Butterfly / Condor קנוי"}:
        return 0.5 - abs(normalized_move)
    return None


def _strategy_records(
    frame: pd.DataFrame, horizons: tuple[int, ...]
) -> tuple[pd.DataFrame, pd.DataFrame]:
    records: list[dict[str, object]] = []
    sensitivity: list[dict[str, object]] = []
    for horizon in horizons:
        for position, (timestamp, row) in enumerate(frame.iterrows()):
            if position + horizon >= len(frame):
                continue
            required = (
                row.get("forecast_rv_3d"),
                row.get("vta35"),
                row.get("market_trend_score"),
                row.get("volatility_direction_score"),
            )
            if not all(_finite(value) for value in required):
                continue
            spot = float(row["close"])
            forecast = float(row["forecast_rv_3d"])
            future = float(frame["close"].iloc[position + horizon])
            width = spot * forecast * math.sqrt(horizon / 252)
            if width <= 0:
                continue
            normalized_move = (future - spot) / width
            recommendation = recommend_strategy(
                spot=spot,
                forecast_volatility=forecast,
                implied_volatility=float(row["vta35"]) / 100,
                trend_score=float(row["market_trend_score"]),
                volatility_score=float(row["volatility_direction_score"]),
                regime=str(row["regime"]),
                horizon_days=horizon,
                premium_sale_eligible=True,
            )
            selected_name = recommendation.primary.name if recommendation.primary else None
            for name in STRATEGY_NAMES:
                assessed = _strategy_success(
                    name,
                    spot=spot,
                    future=future,
                    forecast=forecast,
                    horizon=horizon,
                )
                records.append(
                    {
                        "date": timestamp,
                        "year": int(timestamp.year),
                        "position": position,
                        "horizon": horizon,
                        "strategy": name,
                        "selected": name == selected_name,
                        "testable": assessed is not None,
                        "success": assessed[0] if assessed is not None else np.nan,
                        "normalized_move": normalized_move,
                        "scenario_score": _strategy_score(name, normalized_move),
                        "regime": str(row["regime"]),
                    }
                )
            if selected_name:
                for multiplier in (0.75, 1.0, 1.25):
                    assessed = _strategy_success(
                        selected_name,
                        spot=spot,
                        future=future,
                        forecast=forecast * multiplier,
                        horizon=horizon,
                    )
                    if assessed is not None:
                        sensitivity.append(
                            {
                                "date": timestamp,
                                "year": int(timestamp.year),
                                "position": position,
                                "horizon": horizon,
                                "strategy": selected_name,
                                "band_multiplier": multiplier,
                                "success": assessed[0],
                                "regime": str(row["regime"]),
                            }
                        )
    return pd.DataFrame(records), pd.DataFrame(sensitivity)


def _strategy_tables(
    records: pd.DataFrame, sensitivity: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    summary_rows: list[dict[str, object]] = []
    regime_rows: list[dict[str, object]] = []
    year_rows: list[dict[str, object]] = []
    for keys, group in records.groupby(["strategy", "horizon"], sort=True):
        name, horizon = keys
        testable = group[group["testable"]]
        selected = testable[testable["selected"]]
        baseline = float(testable["success"].mean()) if len(testable) else None
        observations = len(selected)
        successes = int(selected["success"].sum()) if observations else 0
        rate = successes / observations if observations else None
        low, high = _wilson(successes, observations)
        if baseline is None:
            strength, adjusted = 1, None
        else:
            strength, adjusted = _score(successes, observations, baseline=baseline)
        nonoverlap_n, nonoverlap_min, nonoverlap_median, nonoverlap_max = (
            _nonoverlap_rate(selected.rename(columns={"success": "hit"}), int(horizon))
            if observations
            else (0, None, None, None)
        )
        yearly_lifts: list[float] = []
        regime_lifts: list[float] = []
        for dimensions, destination, stability in (
            ("year", year_rows, yearly_lifts),
            ("regime", regime_rows, regime_lifts),
        ):
            for segment, segment_all in testable.groupby(dimensions):
                segment_selected = segment_all[segment_all["selected"]]
                if len(segment_selected) < 5:
                    continue
                segment_baseline = float(segment_all["success"].mean())
                segment_rate = float(segment_selected["success"].mean())
                stability.append(segment_rate - segment_baseline)
                destination.append(
                    {
                        "strategy": name,
                        "horizon": horizon,
                        dimensions: segment,
                        "selected_n": len(segment_selected),
                        "success_rate": segment_rate,
                        "unconditional_baseline": segment_baseline,
                        "uplift": segment_rate - segment_baseline,
                    }
                )
        summary_rows.append(
            {
                "strategy": name,
                "horizon": horizon,
                "available_days": len(testable),
                "selected_n": observations,
                "selection_rate": observations / len(testable) if len(testable) else None,
                "successes": successes,
                "success_rate": rate,
                "unconditional_baseline": baseline,
                "uplift": rate - baseline if rate is not None and baseline is not None else None,
                "adjusted_success_rate": adjusted,
                "ci_low": low,
                "ci_high": high,
                "p_value": (
                    _proportion_pvalue(
                        successes, observations, baseline, horizon=int(horizon)
                    )
                    if baseline is not None
                    else None
                ),
                "strength": strength,
                "mean_scenario_score": (
                    float(selected["scenario_score"].mean()) if observations else None
                ),
                "median_normalized_move": (
                    float(selected["normalized_move"].median()) if observations else None
                ),
                "nonoverlap_n_min": nonoverlap_n,
                "n_eff": observations // int(horizon),
                "nonoverlap_success_rate_min": nonoverlap_min,
                "nonoverlap_success_rate": nonoverlap_median,
                "nonoverlap_success_rate_max": nonoverlap_max,
                "positive_years": sum(value > 0 for value in yearly_lifts),
                "tested_years": len(yearly_lifts),
                "positive_regimes": sum(value > 0 for value in regime_lifts),
                "tested_regimes": len(regime_lifts),
                "sample_quality": _quality(observations),
                "limitation": (
                    "requires two-expiry IV history"
                    if name == "Calendar / Diagonal"
                    else "market-scenario proxy; no option P&L"
                ),
            }
        )
    summary = pd.DataFrame(summary_rows)
    if not summary.empty:
        summary["fdr_q"] = _bh_adjust(summary["p_value"])

    sensitivity_rows: list[dict[str, object]] = []
    if not sensitivity.empty:
        for keys, group in sensitivity.groupby(
            ["strategy", "horizon", "band_multiplier"], sort=True
        ):
            name, horizon, multiplier = keys
            sensitivity_rows.append(
                {
                    "strategy": name,
                    "horizon": horizon,
                    "band_multiplier": multiplier,
                    "selected_n": len(group),
                    "success_rate": float(group["success"].mean()),
                }
            )
    return {
        "strategy_summary": summary,
        "strategy_sensitivity": pd.DataFrame(sensitivity_rows),
        "strategy_by_regime": pd.DataFrame(regime_rows),
        "strategy_by_year": pd.DataFrame(year_rows),
    }


def _forecast_table(frame: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for horizon in horizons:
        outcomes = _outcomes(frame, horizon)
        forecast = frame["forecast_rv_3d"].astype(float)
        implied = frame["vta35"].astype(float) / 100
        scale = forecast * math.sqrt(horizon / 252)
        forward_return = outcomes["forward_return"].astype(float)
        normalized = forward_return / scale
        for source, estimate in (("combined_RV_forecast", forecast), ("VTA35_proxy", implied)):
            valid = pd.DataFrame(
                {
                    "estimate": estimate,
                    "realized": outcomes["forward_rv"],
                    "z": normalized if source == "combined_RV_forecast" else forward_return / (estimate * math.sqrt(horizon / 252)),
                }
            ).replace([np.inf, -np.inf], np.nan).dropna()
            if valid.empty:
                continue
            error = valid["estimate"] - valid["realized"]
            row: dict[str, object] = {
                "source": source,
                "horizon": horizon,
                "n": len(valid),
                "mean_estimate": float(valid["estimate"].mean()),
                "mean_forward_rv": float(valid["realized"].mean()),
                "bias": float(error.mean()),
                "mae": float(error.abs().mean()),
                "rmse": float(math.sqrt(float((error**2).mean()))),
                "rv_rank_ic": _spearman(valid["estimate"], valid["realized"]),
            }
            for sigma in (0.5, 1.0, 1.5, 2.0):
                row[f"coverage_{sigma}sigma"] = float((valid["z"].abs() <= sigma).mean())
            rows.append(row)
    return pd.DataFrame(rows)


def _har_rv_benchmark(frame: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    """Expanding HAR-RV benchmark and incremental VTA35 ablation.

    At position t the fit ends at t-h, so every training target has fully
    matured. Evaluation uses one fixed non-overlapping offset per horizon.
    """

    daily_rv = np.log(frame["close"].astype(float)).diff().abs() * math.sqrt(252)
    features = pd.DataFrame(
        {
            "const": 1.0,
            "rv_daily": np.log(daily_rv.clip(lower=1e-6)),
            "rv_weekly": np.log(daily_rv.rolling(5).mean().clip(lower=1e-6)),
            "rv_monthly": np.log(daily_rv.rolling(22).mean().clip(lower=1e-6)),
            "downside_share_20": frame["downside_share_20"],
            "vta35": frame["vta35"].astype(float) / 100,
            "local_global_stress_spread": frame["local_global_stress_spread"],
        },
        index=frame.index,
    )
    rows: list[dict[str, object]] = []
    for horizon in horizons:
        target = _outcomes(frame, horizon)["forward_rv"]
        predictions: list[dict[str, float]] = []
        for position in range(120 + horizon, len(frame) - horizon):
            if position % horizon != 0:
                continue
            train_end = position - horizon
            train = features.iloc[: train_end + 1].copy()
            train["target"] = np.log(target.iloc[: train_end + 1].clip(lower=1e-6))
            train = train.replace([np.inf, -np.inf], np.nan).dropna()
            current = features.iloc[position]
            actual = target.iloc[position]
            if len(train) < 80 or not _finite(actual):
                continue
            base_columns = ["const", "rv_daily", "rv_weekly", "rv_monthly"]
            x_columns = [
                *base_columns,
                "downside_share_20",
                "vta35",
                "local_global_stress_spread",
            ]
            if current[x_columns].isna().any():
                continue
            base_beta = np.linalg.lstsq(
                train[base_columns].to_numpy(), train["target"].to_numpy(), rcond=None
            )[0]
            x_beta = np.linalg.lstsq(
                train[x_columns].to_numpy(),
                train["target"].to_numpy(),
                rcond=None,
            )[0]
            predictions.append(
                {
                    "actual": float(actual),
                    "naive_rv20": float(frame["rv_20"].iloc[position]),
                    "combined": float(frame["forecast_rv_3d"].iloc[position]),
                    "vta35": float(frame["vta35"].iloc[position]) / 100,
                    "gjr": float(frame["gjr_rv_1d"].iloc[position]),
                    "har": float(math.exp(current[base_columns].to_numpy() @ base_beta)),
                    "har_x": float(math.exp(current[x_columns].to_numpy() @ x_beta)),
                    "rv_20": float(frame["rv_20"].iloc[position]),
                }
            )
        sample = pd.DataFrame(predictions)
        if sample.empty:
            rows.append({"horizon": horizon, "n_eff": 0})
            continue
        actual_variance = sample["actual"].to_numpy() ** 2
        model_losses: dict[str, np.ndarray] = {}
        for model in ("naive_rv20", "combined", "vta35", "gjr", "har", "har_x"):
            forecast_values = sample[model].clip(lower=1e-6).to_numpy()
            forecast_variance = forecast_values**2
            ratio = actual_variance / forecast_variance
            losses = ratio - np.log(ratio) - 1
            model_losses[model] = losses
            direction_accuracy = float(
                (
                    np.sign(sample[model] - sample["rv_20"])
                    == np.sign(sample["actual"] - sample["rv_20"])
                ).mean()
            )
            rows.append(
                {
                    "horizon": horizon,
                    "model": model,
                    "n_eff": len(sample),
                    "mae": float((sample[model] - sample["actual"]).abs().mean()),
                    "mse_variance": float(np.mean((forecast_variance - actual_variance) ** 2)),
                    "qlike": qlike(actual_variance, forecast_variance),
                    "direction_accuracy": direction_accuracy,
                }
            )
        naive_loss = model_losses["naive_rv20"]
        for row in rows[-6:]:
            model = str(row["model"])
            row["qlike_improvement_vs_naive"] = float(
                np.mean(naive_loss - model_losses[model])
            )
            row["block_bootstrap_p"] = _bootstrap_pvalue(
                naive_loss - model_losses[model], block=max(2, horizon)
            )
    return pd.DataFrame(rows)


def _bootstrap_pvalue(
    improvement: np.ndarray,
    *,
    block: int = 5,
    draws: int = 100,
) -> float:
    """Vectorized circular moving-block bootstrap under a zero-mean null."""

    values = np.asarray(improvement, dtype=float)
    values = values[np.isfinite(values)]
    n = len(values)
    if n < 12:
        return math.nan
    observed = float(np.mean(values))
    centered = values - observed
    rng = np.random.default_rng(35_2026)
    actual_block = max(1, min(block, n))
    blocks_needed = (n + actual_block - 1) // actual_block
    starts = rng.integers(0, n, size=(draws, blocks_needed))
    offsets = np.arange(actual_block)
    idx = (starts[:, :, None] + offsets[None, None, :]) % n
    sample_matrix = centered[idx.reshape(draws, -1)[:, :n]]
    boot_means = np.mean(sample_matrix, axis=1)
    return float((1 + np.sum(boot_means >= observed)) / (draws + 1))


def _offset_detail(records: pd.DataFrame) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, group in records.groupby(["indicator", "horizon", "axis"], sort=True):
        indicator, horizon, axis = keys
        for offset in range(int(horizon)):
            sample = group[group["position"].astype(int) % int(horizon) == offset]
            if sample.empty:
                continue
            baseline = _marginal_baseline(sample)
            rows.append(
                {
                    "indicator": indicator,
                    "horizon": horizon,
                    "axis": axis,
                    "offset": offset,
                    "n": len(sample),
                    "accuracy": float(sample["hit"].mean()),
                    "baseline": baseline,
                    "lift": float(sample["hit"].mean()) - baseline,
                }
            )
    return pd.DataFrame(rows)


def _ridge_logit_predict(
    x: np.ndarray, y: np.ndarray, current: np.ndarray, alpha: float = 1.0
) -> float:
    """Fast IRLS/Newton solver for Ridge L2-regularized logistic regression on small EOD samples."""

    mean = np.mean(x, axis=0)
    scale = np.std(x, axis=0)
    scale[scale < 1e-8] = 1.0
    train = (x - mean) / scale
    point = (current - mean) / scale

    n_samples, n_features = train.shape
    design = np.column_stack((np.ones(n_samples), train))
    beta = np.zeros(n_features + 1)
    L = np.diag(np.r_[0.0, np.full(n_features, alpha)])

    for _ in range(6):
        logits = np.clip(design @ beta, -20, 20)
        p = 1.0 / (1.0 + np.exp(-logits))
        w = p * (1.0 - p)
        w = np.maximum(w, 1e-5)

        grad = design.T @ (p - y) + L @ beta
        H = (design.T * w) @ design + L

        try:
            step = np.linalg.solve(H, grad)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, grad, rcond=None)[0]

        beta -= step
        if np.max(np.abs(step)) < 1e-4:
            break

    return float(1.0 / (1.0 + math.exp(-float(np.clip(np.r_[1.0, point] @ beta, -20, 20)))))


def _probabilistic_family_model(
    frame: pd.DataFrame, horizons: tuple[int, ...]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Purged, non-overlapping OOS model with separate trend and reversal family signals."""

    def expanding_rank(series: pd.Series) -> pd.Series:
        return series.expanding(min_periods=60).apply(
            lambda values: float(np.mean(values <= values[-1])), raw=True
        )

    ranked = frame[
        [
            "downside_share_20",
            "rs_range_5_20",
            "rv_20_60_ratio",
            "vta35_zscore_60",
            "vta35_change_5d",
            "vta_vol_of_vol_20",
            "local_global_stress_spread",
            "vix_vix3m_ratio",
            "usdils_change_5d",
            "trend_efficiency_20",
            "range_position_20",
            "reversal_5_vol_scaled",
            "matched_vrp_3d",
        ]
    ].apply(expanding_rank)
    families = pd.DataFrame(
        {
            "rv_local": ranked[["downside_share_20", "rs_range_5_20", "rv_20_60_ratio"]].mean(axis=1),
            "iv_local": ranked[["vta35_zscore_60", "vta35_change_5d", "vta_vol_of_vol_20"]].mean(axis=1),
            "global_fx": ranked[["local_global_stress_spread", "vix_vix3m_ratio", "usdils_change_5d"]].mean(axis=1),
            "trend_regime": ranked[["trend_efficiency_20", "range_position_20"]].mean(axis=1),
            "reversal_regime": ranked["reversal_5_vol_scaled"],
            "forecast_gap": ranked["matched_vrp_3d"],
        },
        index=frame.index,
    )
    names = list(families.columns)
    predictions: list[dict[str, object]] = []
    ablations: list[dict[str, object]] = []
    for horizon in horizons:
        outcomes = _outcomes(frame, horizon)
        targets = {
            "volatility": (outcomes["forward_rv"] > frame["rv_20"]).astype(float),
            "market": (outcomes["forward_return"] > 0).astype(float),
        }
        for axis, target in targets.items():
            for position in range(160 + horizon, len(frame) - horizon):
                if position % horizon:
                    continue
                train_end = position - horizon
                train = families.iloc[: train_end + 1].copy()
                train["target"] = target.iloc[: train_end + 1]
                train = train.replace([np.inf, -np.inf], np.nan).dropna()
                current = families.iloc[position]
                if len(train) < 100 or current.isna().any():
                    continue
                x = train[names].to_numpy(dtype=float)
                y = train["target"].to_numpy(dtype=float)
                actual = float(target.iloc[position])
                probability = _ridge_logit_predict(x, y, current.to_numpy(dtype=float))
                predictions.append(
                    {
                        "date": frame.index[position],
                        "horizon": horizon,
                        "axis": axis,
                        "position": position,
                        "probability": probability,
                        "actual": actual,
                    }
                )
                full_loss = (probability - actual) ** 2
                for dropped in names:
                    retained = [name for name in names if name != dropped]
                    reduced = _ridge_logit_predict(
                        train[retained].to_numpy(dtype=float),
                        y,
                        current[retained].to_numpy(dtype=float),
                    )
                    ablations.append(
                        {
                            "horizon": horizon,
                            "axis": axis,
                            "position": position,
                            "family": dropped,
                            "full_brier": full_loss,
                            "without_family_brier": (reduced - actual) ** 2,
                        }
                    )
    prediction_frame = pd.DataFrame(predictions)
    summary_rows: list[dict[str, object]] = []
    calibration_rows: list[dict[str, object]] = []
    if not prediction_frame.empty:
        for keys, group in prediction_frame.groupby(["horizon", "axis"]):
            horizon, axis = keys
            baseline = float(group["actual"].mean())
            clipped = group["probability"].clip(1e-6, 1 - 1e-6)
            summary_rows.append(
                {
                    "horizon": horizon,
                    "axis": axis,
                    "n_eff": len(group),
                    "brier": float(np.mean((clipped - group["actual"]) ** 2)),
                    "baseline_brier": float(np.mean((baseline - group["actual"]) ** 2)),
                    "log_loss": float(-np.mean(group["actual"] * np.log(clipped) + (1 - group["actual"]) * np.log(1 - clipped))),
                    "mean_probability": float(clipped.mean()),
                    "event_rate": baseline,
                    "latest_probability": float(clipped.iloc[-1]),
                    "status": "research/context",
                }
            )
            bins = pd.cut(clipped, bins=[0, 0.4, 0.5, 0.6, 1], include_lowest=True)
            for bucket, sample in group.groupby(bins, observed=True):
                calibration_rows.append(
                    {
                        "horizon": horizon,
                        "axis": axis,
                        "probability_bin": str(bucket),
                        "n": len(sample),
                        "mean_probability": float(sample["probability"].mean()),
                        "event_rate": float(sample["actual"].mean()),
                    }
                )
    ablation_frame = pd.DataFrame(ablations)
    if not ablation_frame.empty:
        ablation_frame = (
            ablation_frame.groupby(["horizon", "axis", "family"], as_index=False)
            .agg(n_eff=("position", "size"), full_brier=("full_brier", "mean"), without_family_brier=("without_family_brier", "mean"))
        )
        ablation_frame["incremental_brier_value"] = (
            ablation_frame["without_family_brier"] - ablation_frame["full_brier"]
        )
        ablation_frame["status"] = "research/context"
    return pd.DataFrame(summary_rows), pd.DataFrame(calibration_rows), ablation_frame


def _recommendation_findings(tables: dict[str, pd.DataFrame]) -> tuple[str, ...]:
    findings: list[str] = []
    indicators = tables["indicator_aggregate"]
    strategies = tables["strategy_summary"]
    for horizon in BACKTEST_HORIZONS:
        sample = indicators[
            (indicators["horizon"] == horizon)
            & (indicators["n"] >= 30)
            & (indicators["lift"] > 0)
        ].sort_values(["lift", "n"], ascending=False)
        if len(sample):
            best = sample.iloc[0]
            findings.append(
                f"{horizon}d indicator leader: {best['indicator']} / {best['axis']} "
                f"(lift {best['lift']:+.1%}, n={int(best['n'])}, strength {int(best['strength'])}/10, "
                f"FDR q={best['fdr_q']:.3f})."
            )
        strategy_sample = strategies[
            (strategies["horizon"] == horizon)
            & (strategies["selected_n"] >= 20)
            & strategies["uplift"].notna()
        ].sort_values(["uplift", "selected_n"], ascending=False)
        if len(strategy_sample):
            best = strategy_sample.iloc[0]
            findings.append(
                f"{horizon}d strategy-scenario leader: {best['strategy']} "
                f"(uplift {best['uplift']:+.1%}, n={int(best['selected_n'])}, strength {int(best['strength'])}/10, "
                f"FDR q={best['fdr_q']:.3f}; exploratory unless it passes the knowledge-tier gates)."
            )
    deployable_strategies = strategies[
        (strategies["selected_n"] >= 40)
        & (strategies["uplift"] > 0)
        & (strategies["fdr_q"] <= 0.10)
    ]
    if deployable_strategies.empty:
        findings.append(
            "No strategy-selection rule passed the minimum sample plus 10% FDR gate; strategy rankings are exploratory and should not yet alter live recommendations automatically."
        )
    return tuple(findings)


def _knowledge_ranking(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Publish research diagnostics without granting deployment authority."""
    rows: list[dict[str, object]] = []
    indicators = tables["indicator_aggregate"]
    for row in indicators.itertuples(index=False):
        rows.append(
            {
                "kind": "indicator",
                "name": row.indicator,
                "axis": row.axis,
                "horizon": row.horizon,
                "n": row.n,
                "edge": row.lift,
                "fdr_q": row.fdr_q,
                "year_stability": f"{row.positive_years}/{row.tested_years}",
                "regime_stability": f"{row.positive_regimes}/{row.tested_regimes}",
                "tier": "C — context only (validation freeze)",
            }
        )
    strategies = tables["strategy_summary"]
    for row in strategies.itertuples(index=False):
        rows.append(
            {
                "kind": "strategy_proxy",
                "name": row.strategy,
                "axis": "scenario",
                "horizon": row.horizon,
                "n": row.selected_n,
                "edge": row.uplift,
                "fdr_q": row.fdr_q,
                "year_stability": f"{row.positive_years}/{row.tested_years}",
                "regime_stability": f"{row.positive_regimes}/{row.tested_regimes}",
                "tier": "C — context only (validation freeze)",
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["tier", "horizon", "edge"], ascending=[True, True, False], na_position="last"
    )


def _context_ablation(frame: pd.DataFrame, horizons: tuple[int, ...]) -> pd.DataFrame:
    """Strict non-overlapping OOS checks for context-only state variables.

    The two diagnostics do not emit dashboard arrows.  Each row uses one
    offset-separated sample, and the candidate orientation is fixed by market
    interpretation rather than selected on the evaluation outcomes.
    """

    rows: list[dict[str, object]] = []
    for horizon in horizons:
        outcomes = _outcomes(frame, horizon)
        actual = outcomes["market_direction"]
        baseline_prediction = np.sign(frame["market_trend_score"])
        candidates = {
            "fx_equity_state": -np.sign(frame["usdils_change_5d"]),
            "ta35_vta35_corr_60": np.where(
                frame["ta35_vta35_corr_60"] < 0,
                -np.sign(frame["vta35_change_5d"]),
                0,
            ),
        }
        for name, candidate in candidates.items():
            sample = pd.DataFrame(
                {
                    "position": np.arange(len(frame)),
                    "actual": actual,
                    "baseline": baseline_prediction,
                    "candidate": candidate,
                    "regime": frame["regime"],
                },
                index=frame.index,
            ).replace([np.inf, -np.inf], np.nan)
            sample = sample.dropna()
            sample = sample[
                (sample["actual"] != 0)
                & (sample["baseline"] != 0)
                & (sample["candidate"] != 0)
                & (sample["position"] % horizon == 0)
            ]
            if sample.empty:
                rows.append(
                    {
                        "feature": name,
                        "horizon": horizon,
                        "n_eff": 0,
                        "baseline_accuracy": np.nan,
                        "augmented_accuracy": np.nan,
                        "lift": np.nan,
                        "p_value": np.nan,
                        "positive_regimes": 0,
                        "tested_regimes": 0,
                    }
                )
                continue
            baseline_hit = sample["baseline"] == sample["actual"]
            candidate_hit = sample["candidate"] == sample["actual"]
            wins = int((candidate_hit & ~baseline_hit).sum())
            losses = int((baseline_hit & ~candidate_hit).sum())
            discordant = wins + losses
            # One-sided paired normal approximation; conservative when tied.
            p_value = (
                _normal_sf((wins - losses) / math.sqrt(discordant))
                if discordant
                else 1.0
            )
            regime_lifts = []
            for _, segment in sample.groupby("regime"):
                if len(segment) >= 8:
                    regime_lifts.append(
                        float(
                            (segment["candidate"] == segment["actual"]).mean()
                            - (segment["baseline"] == segment["actual"]).mean()
                        )
                    )
            baseline_accuracy = float(baseline_hit.mean())
            augmented_accuracy = float(candidate_hit.mean())
            rows.append(
                {
                    "feature": name,
                    "horizon": horizon,
                    "n_eff": len(sample),
                    "baseline_accuracy": baseline_accuracy,
                    "augmented_accuracy": augmented_accuracy,
                    "lift": augmented_accuracy - baseline_accuracy,
                    "p_value": p_value,
                    "positive_regimes": sum(value > 0 for value in regime_lifts),
                    "tested_regimes": len(regime_lifts),
                }
            )
    result = pd.DataFrame(rows)
    if not result.empty:
        result["fdr_q"] = _bh_adjust(result["p_value"])
        result["eligible"] = (
            (result["n_eff"] >= 80)
            & (result["lift"] > 0)
            & (result["fdr_q"] <= 0.05)
            & (result["positive_regimes"] >= 2)
        )
        result["status"] = np.where(
            result["eligible"], "candidate-after-review", "context-only"
        )
    return result


def run_research_backtest(
    repository: SQLiteRepository,
    *,
    indicator_keys: tuple[str, ...],
    horizons: tuple[int, ...] = BACKTEST_HORIZONS,
) -> ResearchReport:
    frame = _historical_features(repository)
    if frame.empty:
        return ResearchReport(
            datetime.now(UTC), None, None, 0, {}, (), ("No TA-35 data available.",)
        )
    indicator_records = _indicator_records(frame, indicator_keys, horizons)
    strategy_records, sensitivity = _strategy_records(frame, horizons)
    family_summary, family_calibration, family_ablation = (
        _probabilistic_family_model(frame, horizons)
    )
    tables = {
        "data_coverage": pd.DataFrame(
            [
                {
                    "series": symbol,
                    "n": len(history := repository.bar_history(symbol, 100_000)),
                    "start": history[0].session_date if history else None,
                    "end": history[-1].session_date if history else None,
                }
                for symbol in ("TA35", "VTA35", "USDILS", "VIX9D", "VIX", "VIX3M")
            ]
        ),
        "forecast_calibration": _forecast_table(frame, horizons),
        "har_rv_benchmark": _har_rv_benchmark(frame, horizons),
        "indicator_nonoverlap_offsets": _offset_detail(indicator_records),
        "probabilistic_family_oos": family_summary,
        "probabilistic_family_calibration": family_calibration,
        "probabilistic_family_ablation": family_ablation,
        **_indicator_tables(indicator_records),
        **_strategy_tables(strategy_records, sensitivity),
        "context_ablation_oos": _context_ablation(frame, horizons),
    }
    tables = {"knowledge_ranking": _knowledge_ranking(tables), **tables}
    return ResearchReport(
        generated_at=datetime.now(UTC),
        start_date=frame.index[0].date(),
        end_date=frame.index[-1].date(),
        observations=len(frame),
        tables=tables,
        findings=_recommendation_findings(tables),
        warnings=(
            "All features are computed as-of date t; outcomes begin after that close.",
            "Overlapping horizons create serial dependence; non-overlapping robustness columns are reported.",
            "P-values use the conservative non-overlapping n=floor(n/h), with Holm family-wise adjustment under arbitrary dependence; they remain diagnostics, not deployment gates.",
            "Strategy results are market-scenario proxies, not option P&L; premiums, skew, spreads and slippage are unavailable.",
            "Calendar/Diagonal is untestable without historical IV for at least two expiries.",
            "The 738-day TA-35 sample spans only about three years; regime and annual results can be fragile.",
            "forecast_rv_3d and expected_move_3d_points emit the same direction rule, so their similar results are duplicate evidence rather than independent confirmation.",
            "US series are made available on the following calendar day before as-of alignment, preserving Friday data for Sunday and preventing same-date Mon-Thu look-ahead.",
            "The current rule thresholds were not frozen before this historical sample. Treat discoveries as in-sample research and require a future frozen holdout before automatic deployment.",
            "The family probability model uses one shrunk input per information family, strict label maturity, and one non-overlapping offset; its probabilities remain unapproved research outputs.",
        ),
    )


def _format_cell(value: object, column: str) -> str:
    if value is None or (isinstance(value, float) and not math.isfinite(value)) or pd.isna(value):
        return "—"
    if isinstance(value, (np.integer, int)):
        return f"{int(value):,}"
    if isinstance(value, (np.floating, float)):
        if any(token in column for token in ("rate", "accuracy", "baseline", "lift", "coverage", "ci_", "adjusted")):
            return f"{float(value):.1%}"
        if column in {"p_value", "fdr_q"}:
            return f"{float(value):.4f}"
        return f"{float(value):.4f}"
    return str(value).replace("|", "\\|").replace("\n", " ")


def _markdown_table(frame: pd.DataFrame) -> str:
    if frame.empty:
        return "_No observations._"
    columns = [str(column) for column in frame.columns]
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append(
            "| "
            + " | ".join(_format_cell(value, column) for value, column in zip(row, columns, strict=True))
            + " |"
        )
    return "\n".join(lines)


TABLE_TITLES = {
    "knowledge_ranking": "Recommendation knowledge tiers and deployment gates",
    "data_coverage": "Data coverage",
    "forecast_calibration": "Forecast calibration and probability-band coverage",
    "har_rv_benchmark": "Expanding HAR-RV benchmark and incremental VTA35 value",
    "indicator_nonoverlap_offsets": "Every non-overlapping offset reported separately",
    "probabilistic_family_oos": "Purged OOS probability model by information family",
    "probabilistic_family_calibration": "Probability calibration by forecast bin",
    "probabilistic_family_ablation": "Incremental OOS value of each information family",
    "indicator_aggregate": "Indicator aggregate direction tests",
    "indicator_by_arrow": "Indicator results for every emitted arrow",
    "indicator_intensity": "Indicator intensity / threshold sensitivity",
    "indicator_by_regime": "Indicator robustness by market regime",
    "indicator_by_year": "Indicator robustness by calendar year",
    "strategy_summary": "Every strategy family: selected-rule performance versus unconditional baseline",
    "strategy_sensitivity": "Strategy scenario sensitivity to 0.75x / 1.00x / 1.25x volatility bands",
    "strategy_by_regime": "Strategy robustness by market regime",
    "strategy_by_year": "Strategy robustness by calendar year",
    "context_ablation_oos": "Context-only OOS ablation: FX-equity state and TA35-VTA35 correlation",
}


def render_research_markdown(report: ResearchReport) -> str:
    header = f"""# TA-35 dashboard — comprehensive backtest research

Generated: {report.generated_at:%Y-%m-%d %H:%M UTC}

TA-35 sample: {report.start_date} to {report.end_date} ({report.observations:,} sessions)

Horizons: {', '.join(str(value) for value in BACKTEST_HORIZONS)} trading days

## Executive interpretation

This document is a research knowledge base for recommendation calibration. It tests every dashboard indicator output and every strategy family at every requested horizon. A positive lift means that the rule beat the relevant historical base rate; it does not guarantee future performance.

"""
    findings = "\n".join(f"- {finding}" for finding in report.findings) or "- No robust leader met the minimum sample gate."
    methods = """

## Test design

- Strict as-of feature construction: a signal on session t uses only data available through t.
- Outcomes: TA-35 close-to-close return and forward realized volatility over 3/7/14/30 sessions.
- Direction tests: accuracy, RV-level-conditioned class-marginal baseline, lift, Wilson 95% interval and a conservative one-sided p-value using floor(n/h).
- Calibration tests: delayed walk-forward Brier score, so a label enters the historical score only after its horizon has elapsed.
- Robustness: min/median/max across every non-overlapping offset, calendar years, dashboard regimes and signal-intensity subsets.
- Continuous tests: rank information coefficient and top-versus-bottom quintile outcome spread.
- Volatility forecast tests: bias, MAE, RMSE, realized-volatility rank IC and empirical ±0.5/1/1.5/2σ coverage.
- Strategy tests: scenario success when selected, empirical unconditional scenario frequency, recommendation uplift, sensitivity to forecast-band width, and year/regime stability.
- Legacy strength scores remain in raw research tables only for compatibility and are disabled in the product UI and deployment logic.
"""
    limitations = "\n".join(f"- {warning}" for warning in report.warnings)
    sections = [header, findings, methods, "\n## Limitations\n", limitations]
    for key, frame in report.tables.items():
        sections.extend(
            [
                f"\n## {TABLE_TITLES.get(key, key)}\n",
                _markdown_table(frame),
            ]
        )
    return "\n".join(sections) + "\n"


def write_research_report(report: ResearchReport, path: Path | str) -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(render_research_markdown(report), encoding="utf-8")
    return destination
