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
        "vix_slope": (0.0, 0.20, 0.02, True),
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

    if key == "banks_rs_spread":
        mkt_dir = direction(value, neutral=0.0, deadband=0.005)
        strength = heuristic_strength(value, neutral=0.0, full_scale=0.05)
        return (
            "↔",
            arrow(mkt_dir),
            strength,
            "עוצמה יחסית של סקטור הבנקים מול ת״א־35; ביצועי יתר של הבנקים מסמנים מומנטום חיובי.",
        )

    if key == "credit_spread_stress":
        vol_dir = -direction(value, neutral=0.0, deadband=0.25)
        mkt_dir = direction(value, neutral=0.0, deadband=0.25)
        strength = heuristic_strength(value, neutral=0.0, full_scale=2.0)
        return (
            arrow(vol_dir),
            arrow(mkt_dir),
            strength,
            "מרווח אשראי קונצרני מול ממשלתי; ירידה חדה מסמנת הידוק נזילות ולחץ תנודתי.",
        )

    if key == "flight_to_safety":
        vol_dir = -direction(value, neutral=0.0, deadband=0.30)
        mkt_dir = direction(value, neutral=0.0, deadband=0.30)
        strength = heuristic_strength(value, neutral=0.0, full_scale=2.0)
        return (
            arrow(vol_dir),
            arrow(mkt_dir),
            strength,
            "זרימת הון בין מניות לאג״ח ממשלתי; ערך חיובי מסמן Risk-On, ערך שלילי מסמן מעבר למקלט.",
        )

    if key == "yield_curve_slope":
        mkt_dir = direction(value, neutral=0.0, deadband=0.01)
        strength = heuristic_strength(value, neutral=0.0, full_scale=0.05)
        return (
            "↔",
            arrow(mkt_dir),
            strength,
            "שיפוע עקום האג״ח הממשלתי; עקום תלול תומך בבנקים ובמומנטום כלכלי.",
        )

    if key == "banks_momentum_5d":
        mkt_dir = direction(value, neutral=0.0, deadband=0.005)
        strength = heuristic_strength(value, neutral=0.0, full_scale=0.04)
        return (
            "↔",
            arrow(mkt_dir),
            strength,
            "שינוי 5 ימים בסקטור הבנקים; מומנטום סקטוריאלי מוביל.",
        )

    if key == "banks_ta35_corr_20":
        return (
            "↔",
            "↑" if value >= 0.7 else "↔",
            heuristic_strength(value, neutral=0.5, full_scale=0.5),
            "קורלציה מתגלגלת 20 יום בנקים/ת״א־35; מתאם גבוה מעיד על הובלה רוחבית רחבה של השוק.",
        )

    if key == "stock_bond_corr_20":
        # Positive correlation = inflation / rate hike regime; Negative correlation = flight to safety regime
        return (
            "↔",
            "↔",
            1,
            "קורלציה 20 יום מניות–אג״ח ממשלתי; קורלציה שלילית מסמנת משטר מקלט קלאסי, חיובית מסמנת משטר ריבית/אינפלציה.",
        )

    if key == "gov_bond_momentum_5d":
        mkt_dir = direction(value, neutral=0.0, deadband=0.003)
        return (
            "↔",
            arrow(mkt_dir),
            heuristic_strength(value, neutral=0.0, full_scale=0.02),
            "מומנטום 5 ימים באג״ח ממשלתי כללי; עלייה מעידה על ירידת תשואות ורוגע בריבית.",
        )

    if key == "credit_bond_momentum_5d":
        mkt_dir = direction(value, neutral=0.0, deadband=0.003)
        return (
            "↔",
            arrow(mkt_dir),
            heuristic_strength(value, neutral=0.0, full_scale=0.02),
            "מומנטום 5 ימים בתל-בונד 60; עלייה מסמנת סביבת נזילות ואשראי יציבה.",
        )

    if key in {"forecast_rv_3d", "har_rv_3d", "expected_move_3d_points"}:
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

    research_vol_rules = {
        "downside_share_20": (0.50, 0.05, "חלק גבוה של שונות שלילית מסמן לחץ; EOD proxy מחקרי."),
        "vta_vol_of_vol_20": (0.035, 0.005, "אי־יציבות גבוהה ב־IV עשויה לסמן מעבר משטר; Research בלבד."),
        "rs_range_5_20": (1.0, 0.05, "האצה בטווחי OHLC מצביעה על התרחבות RV; Research בלבד."),
        "local_global_stress_spread": (0.0, 0.15, "לחץ מקומי מעל הגלובלי הוא גורם הקשר, לא אות כיוון עצמאי."),
        "matched_vrp_3d": (0.0, 0.0005, "פרמיית שונות מותאמת אופק; אינה חיזוי RV כיווני ישיר."),
    }
    if key in research_vol_rules:
        neutral, deadband, note = research_vol_rules[key]
        vol_direction = direction(value, neutral=neutral, deadband=deadband)
        return arrow(vol_direction), "↔", 1, note

    if key == "trend_efficiency_20":
        # Strong clean trends were associated with lower future RV in discovery.
        vol_direction = -direction(abs(value), neutral=0.35, deadband=0.05)
        return arrow(vol_direction), "↔", 1, "פילטר משטר רציף; אינו קול כיוון עצמאי."

    if key == "range_position_20":
        return "↔", "↔", 1, "מיקום בטווח משמש פילטר trend/reversal ולא הצבעה עצמאית."

    if key == "reversal_5_vol_scaled":
        market_direction = direction(value, neutral=0.0, deadband=0.75)
        return "↔", arrow(market_direction), 1, "תיקון קצר רק לאחר מהלך קיצוני מנורמל; Research בלבד."

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
