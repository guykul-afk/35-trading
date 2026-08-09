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

from ta35_dashboard.analytics import indicator_signal, recommend_strategy
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


def _proportion_pvalue(hits: int, observations: int, baseline: float) -> float | None:
    """One-sided score-test p-value for improvement over a declared baseline."""

    if observations <= 0 or not 0 < baseline < 1:
        return None
    rate = hits / observations
    standard_error = math.sqrt(baseline * (1 - baseline) / observations)
    if standard_error == 0:
        return None
    return min(1.0, max(0.0, _normal_sf((rate - baseline) / standard_error)))


def _bh_adjust(values: pd.Series) -> pd.Series:
    """Benjamini-Hochberg false-discovery-rate adjustment."""

    result = pd.Series(np.nan, index=values.index, dtype=float)
    valid = values.dropna().sort_values()
    if valid.empty:
        return result
    count = len(valid)
    adjusted = np.empty(count, dtype=float)
    running = 1.0
    raw = valid.to_numpy(dtype=float)
    for index in range(count - 1, -1, -1):
        running = min(running, raw[index] * count / (index + 1))
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


def _nonoverlap_rate(group: pd.DataFrame, horizon: int) -> tuple[int, float | None]:
    if group.empty:
        return 0, None
    # Average every possible offset rather than letting one arbitrary start date
    # determine the robustness check.
    rates: list[float] = []
    sizes: list[int] = []
    positions = group["position"].astype(int)
    for offset in range(horizon):
        sample = group[positions % horizon == offset]
        if len(sample):
            rates.append(float(sample["hit"].mean()))
            sizes.append(len(sample))
    return (min(sizes) if sizes else 0), (float(np.mean(rates)) if rates else None)


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
                        }
                    )
    return pd.DataFrame(records)


def _marginal_baseline(group: pd.DataFrame) -> float:
    actual_rates = group["actual"].value_counts(normalize=True)
    prediction_rates = group["predicted"].value_counts(normalize=True)
    return float(
        sum(prediction_rates.get(value, 0.0) * actual_rates.get(value, 0.0) for value in (-1, 0, 1))
    )


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
        nonoverlap_n, nonoverlap_rate = _nonoverlap_rate(group, int(horizon))
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
                "p_value": _proportion_pvalue(hits, observations, baseline),
                "strength": score,
                "brier_walk_forward": _walk_forward_brier(group, baseline, int(horizon)),
                "brier_baseline": baseline * (1 - baseline),
                "nonoverlap_n_min": nonoverlap_n,
                "nonoverlap_accuracy": nonoverlap_rate,
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
        nonoverlap_n, nonoverlap_rate = _nonoverlap_rate(group, int(horizon))
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
                "p_value": _proportion_pvalue(hits, observations, baseline),
                "strength": score,
                "nonoverlap_n_min": nonoverlap_n,
                "nonoverlap_hit_rate": nonoverlap_rate,
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
        nonoverlap_n, nonoverlap_rate = (
            _nonoverlap_rate(selected.rename(columns={"success": "hit"}), int(horizon))
            if observations
            else (0, None)
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
                    _proportion_pvalue(successes, observations, baseline)
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
                "nonoverlap_success_rate": nonoverlap_rate,
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
    rows: list[dict[str, object]] = []
    indicators = tables["indicator_aggregate"]
    for row in indicators.itertuples(index=False):
        robust = (
            row.n >= 80
            and row.lift > 0
            and _finite(row.fdr_q)
            and row.fdr_q <= 0.05
            and row.positive_years >= 3
            and row.positive_regimes >= 3
            and _finite(row.nonoverlap_accuracy)
            and row.nonoverlap_accuracy > row.baseline
        )
        candidate = (
            row.n >= 40
            and row.lift > 0
            and _finite(row.fdr_q)
            and row.fdr_q <= 0.10
            and row.positive_years >= 2
        )
        tier = "A — recommendation input" if robust else "B — supporting input" if candidate else "C — context only"
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
                "tier": tier,
            }
        )
    strategies = tables["strategy_summary"]
    for row in strategies.itertuples(index=False):
        robust = (
            row.selected_n >= 80
            and _finite(row.uplift)
            and row.uplift > 0
            and _finite(row.fdr_q)
            and row.fdr_q <= 0.05
            and row.positive_years >= 3
            and row.positive_regimes >= 3
        )
        candidate = (
            row.selected_n >= 40
            and _finite(row.uplift)
            and row.uplift > 0
            and _finite(row.fdr_q)
            and row.fdr_q <= 0.10
            and row.positive_years >= 2
        )
        tier = "A — recommendation rule" if robust else "B — conditional candidate" if candidate else "C — exploratory / unavailable"
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
                "tier": tier,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["tier", "horizon", "edge"], ascending=[True, True, False], na_position="last"
    )


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
        **_indicator_tables(indicator_records),
        **_strategy_tables(strategy_records, sensitivity),
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
            "P-values are one-sided score approximations and FDR q-values control the many-test discovery rate.",
            "Strategy results are market-scenario proxies, not option P&L; premiums, skew, spreads and slippage are unavailable.",
            "Calendar/Diagonal is untestable without historical IV for at least two expiries.",
            "The 738-day TA-35 sample spans only about three years; regime and annual results can be fragile.",
            "forecast_rv_3d and expected_move_3d_points emit the same direction rule, so their similar results are duplicate evidence rather than independent confirmation.",
            "Cross-market EOD alignment assumes the recommendation is generated only after every same-date source has published; the database has dates, not intraday publication timestamps.",
            "The current rule thresholds were not frozen before this historical sample. Treat discoveries as in-sample research and require a future frozen holdout before automatic deployment.",
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
    "indicator_aggregate": "Indicator aggregate direction tests",
    "indicator_by_arrow": "Indicator results for every emitted arrow",
    "indicator_intensity": "Indicator intensity / threshold sensitivity",
    "indicator_by_regime": "Indicator robustness by market regime",
    "indicator_by_year": "Indicator robustness by calendar year",
    "strategy_summary": "Every strategy family: selected-rule performance versus unconditional baseline",
    "strategy_sensitivity": "Strategy scenario sensitivity to 0.75x / 1.00x / 1.25x volatility bands",
    "strategy_by_regime": "Strategy robustness by market regime",
    "strategy_by_year": "Strategy robustness by calendar year",
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
- Direction tests: accuracy, class-marginal baseline, lift, Wilson 95% interval, shrunken 1–10 strength, one-sided p-value and Benjamini-Hochberg FDR q-value.
- Calibration tests: delayed walk-forward Brier score, so a label enters the historical score only after its horizon has elapsed.
- Robustness: non-overlapping samples, calendar years, dashboard regimes and signal-intensity subsets.
- Continuous tests: rank information coefficient and top-versus-bottom quintile outcome spread.
- Volatility forecast tests: bias, MAE, RMSE, realized-volatility rank IC and empirical ±0.5/1/1.5/2σ coverage.
- Strategy tests: scenario success when selected, empirical unconditional scenario frequency, recommendation uplift, sensitivity to forecast-band width, and year/regime stability.
- Strength scores are shrinkage-based and sample-size penalized. Statistical significance and economic usefulness are shown separately.
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
