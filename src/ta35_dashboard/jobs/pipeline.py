"""Replay-safe Lite collection and volatility metric pipeline."""

from __future__ import annotations

from datetime import UTC, date, datetime
from itertools import pairwise
from statistics import median

import numpy as np

from ta35_dashboard.analytics import (
    MODEL_VERSION,
    ewma_volatility_forecast,
    expected_move,
    gap_variance_share,
    parkinson_volatility,
    percentile_rank,
    realized_volatility,
    volatility_ratio,
    volatility_spread,
    yang_zhang_volatility,
    zscore,
)
from ta35_dashboard.connectors import MarketSnapshot, SnapshotProvider
from ta35_dashboard.storage import MetricValue, SQLiteRepository


def _value(result) -> float | None:
    return result.value


def _returns(closes: list[float]) -> list[float]:
    return list(np.diff(np.log(np.asarray(closes, dtype=float))))


def compute_latest_metrics(
    repository: SQLiteRepository, snapshot: MarketSnapshot
) -> list[MetricValue]:
    as_of = datetime.combine(snapshot.session_date, datetime.min.time(), tzinfo=UTC)
    metrics: list[MetricValue] = []

    def add(
        name: str, value: float | None, flags: tuple[str, ...] = (), **dimensions
    ) -> None:
        metrics.append(
            MetricValue(
                name, value, as_of, MODEL_VERSION, snapshot.run_id, flags, dimensions
            )
        )

    ta = repository.bar_history("TA35", 756)
    closes = [bar.close for bar in ta]
    if not closes:
        add("ta35_close", None, ("missing_ta35",))
        return metrics
    add("ta35_close", closes[-1])
    for horizon in (5, 20, 60):
        value = closes[-1] / closes[-horizon - 1] - 1 if len(closes) > horizon else None
        add(
            f"return_{horizon}d",
            value,
            () if value is not None else ("insufficient_history",),
        )

    rv: dict[int, float | None] = {}
    for window in (5, 10, 20, 60):
        result = realized_volatility(closes[-(window + 1) :])
        rv[window] = result.value
        add(f"rv_{window}", result.value, result.quality_flags)
    returns = _returns(closes)
    ewma = ewma_volatility_forecast(returns[-60:])
    add("rv_ewma", ewma.value, ewma.quality_flags)

    ohlc = [bar for bar in ta[-20:] if None not in (bar.open, bar.high, bar.low)]
    if len(ohlc) == min(20, len(ta)) and len(ohlc) >= 3:
        opens = [float(bar.open) for bar in ohlc if bar.open is not None]
        highs = [float(bar.high) for bar in ohlc if bar.high is not None]
        lows = [float(bar.low) for bar in ohlc if bar.low is not None]
        ohlc_closes = [bar.close for bar in ohlc]
        yz = yang_zhang_volatility(opens, highs, lows, ohlc_closes)
        park = parkinson_volatility(highs, lows)
        gap = gap_variance_share(opens, ohlc_closes)
    else:
        yz = park = gap = type(
            "Missing", (), {"value": None, "quality_flags": ("missing_ohlc",)}
        )()
    add("rv_yang_zhang_20", yz.value, yz.quality_flags)
    add("rv_parkinson_20", park.value, park.quality_flags)
    add("gap_share_20", gap.value, gap.quality_flags)

    acceleration = rv[5] / rv[20] if rv[5] is not None and rv[20] else None
    add(
        "rv_acceleration",
        acceleration,
        () if acceleration is not None else ("insufficient_history",),
    )
    rv_structure = rv[20] / rv[60] if rv[20] is not None and rv[60] else None
    add(
        "rv_20_60_ratio",
        rv_structure,
        () if rv_structure is not None else ("insufficient_history",),
    )

    def normalized_atr(window: int) -> float | None:
        bars = ta[-(window + 1) :]
        if len(bars) < window + 1 or any(
            bar.high is None or bar.low is None for bar in bars[1:]
        ):
            return None
        true_ranges = [
            max(
                float(bar.high) - float(bar.low),
                abs(float(bar.high) - previous.close),
                abs(float(bar.low) - previous.close),
            )
            for previous, bar in pairwise(bars)
        ]
        return float(np.mean(true_ranges)) / bars[-1].close

    atr5, atr20 = normalized_atr(5), normalized_atr(20)
    atr_acceleration = atr5 / atr20 if atr5 is not None and atr20 else None
    add(
        "atr_5_20_ratio",
        atr_acceleration,
        () if atr_acceleration is not None else ("missing_ohlc_or_history",),
    )
    candidates = [
        value for value in (rv[5], rv[20], ewma.value, yz.value) if value is not None
    ]
    forecast = median(candidates) if candidates else None
    add("forecast_rv_3d", forecast)
    move = expected_move(closes[-1], forecast, 3) if forecast is not None else None
    add(
        "expected_move_3d_points",
        move.value if move else None,
        move.quality_flags if move else ("missing_forecast",),
    )

    vta = repository.bar_history("VTA35", 756)
    vta_values = [bar.close for bar in vta]
    current_vta = vta_values[-1] if vta_values else None
    add("vta35", current_vta, () if current_vta is not None else ("missing_vta35",))
    percentile = percentile_rank(vta_values[-252:]) if len(vta_values) >= 2 else None
    add(
        "vta35_percentile_252",
        percentile.value if percentile else None,
        percentile.quality_flags if percentile else ("insufficient_history",),
    )
    vta_change = vta_values[-1] / vta_values[-6] - 1 if len(vta_values) >= 6 else None
    add(
        "vta35_change_5d",
        vta_change,
        () if vta_change is not None else ("insufficient_history",),
    )
    vta_z60 = zscore(vta_values[-60:]) if len(vta_values) >= 3 else None
    add(
        "vta35_zscore_60",
        vta_z60.value if vta_z60 else None,
        vta_z60.quality_flags if vta_z60 else ("insufficient_history",),
    )
    if current_vta is not None and rv[20] is not None:
        spread = volatility_spread(current_vta, rv[20])
        ratio = volatility_ratio(current_vta, rv[20])
        add("vrp_spread", spread.value, spread.quality_flags)
        add("vrp_ratio", ratio.value, ratio.quality_flags)
    else:
        add("vrp_spread", None, ("missing_vta35_or_rv",))
        add("vrp_ratio", None, ("missing_vta35_or_rv",))

    usd = repository.bar_history("USDILS", 252)
    usd_values = [bar.close for bar in usd]
    usd_change = usd_values[-1] / usd_values[-6] - 1 if len(usd_values) >= 6 else None
    add(
        "usdils_change_5d",
        usd_change,
        () if usd_change is not None else ("insufficient_history",),
    )
    usd_rv = realized_volatility(usd_values[-11:]) if len(usd_values) >= 3 else None
    add(
        "usdils_rv_10",
        usd_rv.value if usd_rv else None,
        usd_rv.quality_flags if usd_rv else ("insufficient_history",),
    )

    vix9, vix, vix3 = (
        repository.bar_history(symbol, 252) for symbol in ("VIX9D", "VIX", "VIX3M")
    )
    curve = vix9[-1].close / vix3[-1].close if vix9 and vix3 else None
    add("vix_curve_ratio", curve, () if curve is not None else ("missing_vix_curve",))
    vix9_vix = vix9[-1].close / vix[-1].close if vix9 and vix else None
    vix_vix3 = vix[-1].close / vix3[-1].close if vix and vix3 else None
    add(
        "vix9d_vix_ratio",
        vix9_vix,
        () if vix9_vix is not None else ("missing_vix_curve",),
    )
    add(
        "vix_vix3m_ratio",
        vix_vix3,
        () if vix_vix3 is not None else ("missing_vix_curve",),
    )
    local_z = zscore(vta_values[-252:]) if len(vta_values) >= 3 else None
    global_values = [bar.close for bar in vix]
    global_z = zscore(global_values[-252:]) if len(global_values) >= 3 else None
    premium = (
        local_z.value - global_z.value
        if local_z
        and global_z
        and local_z.value is not None
        and global_z.value is not None
        else None
    )
    add(
        "local_stress_premium",
        premium,
        () if premium is not None else ("missing_stress_history",),
    )

    score = 0
    score += (
        2
        if percentile and percentile.value is not None and percentile.value >= 0.8
        else 0
    )
    score += 2 if acceleration is not None and acceleration >= 1.2 else 0
    score += 1 if gap.value is not None and gap.value >= 0.45 else 0
    score += 1 if curve is not None and curve >= 1 else 0
    score += 1 if usd_change is not None and usd_change >= 0.01 else 0
    regime = (
        "לחץ גבוה"
        if score >= 5
        else "זהירות"
        if score >= 3
        else "רגיל"
        if score >= 1
        else "רגוע"
    )
    add("stress_score", float(score), regime=regime)

    # Direction scores summarize current state only; they are deliberately not
    # calibrated as return forecasts or trading signals.
    # The three local-IV transforms are one information family.  Collapse them
    # to a single vote so VTA35 cannot outvote independent RV/global inputs.
    local_iv_inputs = (
        (vta_change, 0.0),
        (vta_z60.value if vta_z60 else None, 0.0),
        (spread.value if current_vta is not None and rv[20] is not None else None, 0.0),
    )
    local_iv_votes = [
        1 if value > neutral else -1 if value < neutral else 0
        for value, neutral in local_iv_inputs
        if value is not None
    ]
    local_iv_score = (
        sum(local_iv_votes) / len(local_iv_votes) if local_iv_votes else None
    )
    add(
        "local_iv_family_score",
        local_iv_score,
        () if local_iv_score is not None else ("insufficient_local_iv_inputs",),
        available_inputs=len(local_iv_votes),
        family="local_iv_no_double_count",
    )

    vol_inputs = (
        (rv_structure, 1.0),
        (atr_acceleration, 1.0),
        (local_iv_score, 0.0),
        (vix9_vix, 1.0),
        (vix_vix3, 1.0),
    )
    vol_votes = [
        1 if value > neutral else -1 if value < neutral else 0
        for value, neutral in vol_inputs
        if value is not None
    ]
    vol_score = sum(vol_votes) / len(vol_votes) if vol_votes else None
    vol_state = (
        "התרחבות"
        if vol_score is not None and vol_score >= 1 / 3
        else "התכווצות"
        if vol_score is not None and vol_score <= -1 / 3
        else "מעורב"
        if vol_score is not None
        else "לא זמין"
    )
    add(
        "volatility_direction_score",
        vol_score,
        () if vol_score is not None else ("insufficient_inputs",),
        state=vol_state,
        available_inputs=len(vol_votes),
    )

    ma20 = float(np.mean(closes[-20:])) if len(closes) >= 20 else None
    ma60 = float(np.mean(closes[-60:])) if len(closes) >= 60 else None
    range20 = closes[-20:] if len(closes) >= 20 else []
    range_position = (
        (closes[-1] - min(range20)) / (max(range20) - min(range20))
        if range20 and max(range20) > min(range20)
        else None
    )
    trend_votes = [
        1 if value else -1
        for value in (
            closes[-1] >= ma20 if ma20 is not None else None,
            closes[-1] >= ma60 if ma60 is not None else None,
            closes[-1] / closes[-6] - 1 >= 0 if len(closes) >= 6 else None,
            closes[-1] / closes[-21] - 1 >= 0 if len(closes) >= 21 else None,
            range_position >= 0.5 if range_position is not None else None,
        )
        if value is not None
    ]
    trend_score = sum(trend_votes) / len(trend_votes) if trend_votes else None
    trend_state = (
        "מגמה חיובית"
        if trend_score is not None and trend_score >= 0.4
        else "מגמה שלילית"
        if trend_score is not None and trend_score <= -0.4
        else "מצב מעורב"
        if trend_score is not None
        else "לא זמין"
    )
    add(
        "market_trend_state",
        trend_score,
        () if trend_score is not None else ("insufficient_inputs",),
        state=trend_state,
        available_inputs=len(trend_votes),
        range_position_20=range_position,
    )
    return metrics


def collect_once(
    provider: SnapshotProvider,
    repository: SQLiteRepository,
    *,
    as_of: datetime | None = None,
) -> MarketSnapshot:
    snapshot = provider.fetch_snapshot(as_of)
    repository.insert_snapshot(snapshot)
    repository.insert_metrics(compute_latest_metrics(repository, snapshot))
    return snapshot


def collect_history(
    provider: SnapshotProvider,
    repository: SQLiteRepository,
    *,
    start: date | None = None,
    end: date | None = None,
) -> list[str]:
    snapshots = provider.fetch_history(start=start, end=end)
    for snapshot in snapshots:
        repository.insert_snapshot(snapshot)
    if snapshots:
        repository.insert_metrics(compute_latest_metrics(repository, snapshots[-1]))
    return [snapshot.run_id for snapshot in snapshots]
