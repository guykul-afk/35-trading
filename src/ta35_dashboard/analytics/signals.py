"""Transparent indicator direction rules shared by the UI and backtests."""

from __future__ import annotations

import math


def direction(value: float, *, neutral: float, deadband: float = 0.0) -> int:
    if value > neutral + deadband:
        return 1
    if value < neutral - deadband:
        return -1
    return 0


def heuristic_strength(value: float, *, neutral: float, full_scale: float) -> int:
    """Map distance from neutral to a coarse fallback 1-10 scale."""

    if not math.isfinite(value) or full_scale <= 0:
        return 1
    return max(1, min(10, 1 + round(9 * abs(value - neutral) / full_scale)))


def arrow(signal_direction: int) -> str:
    return "↑" if signal_direction > 0 else "↓" if signal_direction < 0 else "↔"


def indicator_signal(
    key: str, value: float | None, metrics: dict[str, object]
) -> tuple[str, str, int, str]:
    """Return volatility state and a conservative TA-35 directional heuristic.

    The returned integer is a value-distance fallback for the TA-35 arrow. The
    dashboard replaces it with an empirical score whenever the historical
    backtest has a sufficient matching sample.
    """

    if value is None or not math.isfinite(value):
        return "—", "—", 1, "אין מספיק נתונים לחישוב הסיגנל."

    metric_values = {
        name: metric.value
        for name, metric in metrics.items()
        if getattr(metric, "value", None) is not None
    }

    # key: (neutral level, full-scale distance, deadband, inverse market link)
    ratio_rules = {
        "rv_acceleration": (1.0, 0.50, 0.03, False),
        "rv_20_60_ratio": (1.0, 0.35, 0.03, False),
        "atr_5_20_ratio": (1.0, 0.35, 0.03, False),
        "vix_curve_ratio": (1.0, 0.35, 0.02, True),
        "vix9d_vix_ratio": (1.0, 0.25, 0.02, True),
        "vix_vix3m_ratio": (1.0, 0.25, 0.02, True),
    }
    if key in ratio_rules:
        neutral, scale, deadband, inverse_market = ratio_rules[key]
        vol_direction = direction(value, neutral=neutral, deadband=deadband)
        market_direction = -vol_direction if inverse_market else 0
        note = (
            "קשר הפוך מקובל בין לחץ גלובלי למדדי מניות; אינו קשר ודאי."
            if inverse_market
            else "המדד מתאר גודל תנועה בלבד ולכן כיוון ת״א־35 נשאר ניטרלי."
        )
        return (
            arrow(vol_direction),
            arrow(market_direction),
            (
                heuristic_strength(value, neutral=neutral, full_scale=scale)
                if market_direction
                else 1
            ),
            note,
        )

    if key in {"forecast_rv_3d", "expected_move_3d_points"}:
        forecast = metric_values.get("forecast_rv_3d")
        rv20 = metric_values.get("rv_20")
        if forecast is None or rv20 is None or rv20 <= 0:
            return "—", "↔", 1, "אין בסיס השוואה מספיק לכיוון התנודתיות."
        ratio = forecast / rv20
        vol_direction = direction(ratio, neutral=1.0, deadband=0.03)
        return (
            arrow(vol_direction),
            "↔",
            1,
            "הכיוון משווה את התחזית ל־RV20; הטווח עצמו אינו חוזה כיוון מדד.",
        )

    if key == "vta35":
        zscore = metric_values.get("vta35_zscore_60")
        if zscore is None:
            return "—", "↔", 1, "חסר ציון התקן הדרוש להשוואת הרמה."
        vol_direction = direction(zscore, neutral=0.0, deadband=0.15)
        strength = heuristic_strength(zscore, neutral=0.0, full_scale=2.0)
        return (
            arrow(vol_direction),
            arrow(-vol_direction),
            strength,
            "הרמה מושווית לממוצע 60 יום; כיוון המדד מבוסס על קשר הפוך מקובל.",
        )

    if key == "vta35_zscore_60":
        vol_direction = direction(value, neutral=0.0, deadband=0.15)
        return (
            arrow(vol_direction),
            arrow(-vol_direction),
            heuristic_strength(value, neutral=0.0, full_scale=2.0),
            "כיוון המדד מבוסס על הקשר ההפוך המקובל לתנודתיות גלומה.",
        )

    if key == "vta35_change_5d":
        vol_direction = direction(value, neutral=0.0, deadband=0.01)
        return (
            arrow(vol_direction),
            arrow(-vol_direction),
            heuristic_strength(value, neutral=0.0, full_scale=0.15),
            "כיוון המדד מבוסס על הקשר ההפוך המקובל לשינוי בתנודתיות גלומה.",
        )

    if key == "usdils_change_5d":
        vol_direction = direction(value, neutral=0.0, deadband=0.0025)
        return (
            arrow(vol_direction),
            arrow(-vol_direction),
            heuristic_strength(value, neutral=0.0, full_scale=0.03),
            "דולר מתחזק מסומן כלחץ מקומי; הקשר לת״א־35 אינו ודאי.",
        )

    if key == "gap_share_20":
        vol_direction = direction(value, neutral=0.35, deadband=0.05)
        return (
            arrow(vol_direction),
            "↔",
            1,
            "משקל Gap מתאר מקור סיכון ולא את כיוון הפתיחה הבאה.",
        )

    if key == "vrp_spread":
        vol_direction = direction(value, neutral=0.0, deadband=0.005)
        return (
            arrow(vol_direction),
            "↔",
            1,
            "הפער מתאר תמחור יחסי של תנודתיות ואינו סיגנל כיוון למדד.",
        )

    return "↔", "↔", 1, "לאינדיקטור אין הטיית כיוון אמינה."
