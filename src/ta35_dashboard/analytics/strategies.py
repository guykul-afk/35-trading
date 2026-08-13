"""General option-strategy families derived from the Lite market state.

The module deliberately stops before contract selection, payoff estimation or
order advice.  It maps the dashboard's descriptive state to a transparent
strategy family and statistical scenario range.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import math
from typing import Any

from ..config import TRADING_DAYS_PER_YEAR
from .volatility import probability_band


@dataclass(frozen=True, slots=True)
class StrategyCandidate:
    name: str
    rationale: str
    risk_note: str


@dataclass(frozen=True, slots=True)
class StrategyRecommendation:
    status: str
    primary: StrategyCandidate | None
    alternatives: tuple[StrategyCandidate, ...]
    horizon_days: int
    market_view: str
    volatility_view: str
    pricing_view: str
    core_range: tuple[float, float] | None
    base_range: tuple[float, float] | None
    focus_range: tuple[float, float] | None
    focus_label: str
    target_level: float | None
    explanation: str
    warnings: tuple[str, ...]
    scenario_fit: tuple[tuple[str, str, str], ...]
    premium_sale_eligible: bool
    suggested_strikes: dict[str, dict[str, Any]] = field(default_factory=dict)


def calculate_strategy_strikes(
    spot: float | None,
    forecast_volatility: float | None,
    horizon_days: int,
    strategy_name: str | None,
    regime: str = "רגוע",
    step: int = 10,
) -> dict[str, dict[str, Any]]:
    """Derive recommended option legs by risk profile based on standard deviations."""
    if spot is None or forecast_volatility is None or spot <= 0 or forecast_volatility <= 0:
        return {}

    one_sigma = spot * forecast_volatility * math.sqrt(horizon_days / TRADING_DAYS_PER_YEAR)
    is_stressed = regime in {"זהירות", "לחץ גבוה"}
    stress_buffer = 0.5 if is_stressed else 0.0
    skew_put_offset = 0.2  # Put skew offset OTM

    def round_strike(val: float) -> int:
        return int(round(val / step) * step)

    profiles: dict[str, dict[str, Any]] = {}

    for risk_key, risk_label in [
        ("balanced", "מאוזן (Balanced)"),
        ("conservative", "שמרני (Conservative)"),
        ("aggressive", "אגרסיבי (Aggressive)"),
    ]:
        legs: list[dict[str, Any]] = []
        name = (strategy_name or "").lower()

        # 1. Bull Call Spread
        if "bull call" in name:
            if risk_key == "conservative":
                lc_sigma, sc_sigma = 0.0, 1.5
            elif risk_key == "balanced":
                lc_sigma, sc_sigma = 0.5, 1.2
            else:
                lc_sigma, sc_sigma = 0.5, 0.8

            k1 = round_strike(spot + lc_sigma * one_sigma)
            k2 = round_strike(spot + sc_sigma * one_sigma)
            if k2 <= k1:
                k2 = k1 + step

            legs = [
                {"action": "Buy", "option_type": "Call", "strike": k1, "quantity": 1, "label": "Long Call (קנייה)"},
                {"action": "Sell", "option_type": "Call", "strike": k2, "quantity": 1, "label": "Short Call (מכירה)"},
            ]

        # 2. Bull Put Spread
        elif "bull put" in name:
            if risk_key == "conservative":
                sp_sigma = 1.5 + skew_put_offset + stress_buffer
                lp_sigma = 2.0 + skew_put_offset
            elif risk_key == "balanced":
                sp_sigma = 1.0 + skew_put_offset + stress_buffer
                lp_sigma = 1.5 + skew_put_offset
            else:
                sp_sigma = 0.5 + skew_put_offset + stress_buffer
                lp_sigma = 1.0 + skew_put_offset

            k2 = round_strike(spot - sp_sigma * one_sigma)  # Short Put (higher strike)
            k1 = round_strike(spot - lp_sigma * one_sigma)  # Long Put (lower strike)
            if k2 <= k1:
                k1 = k2 - step

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Long Put (הגנה)"},
                {"action": "Sell", "option_type": "Put", "strike": k2, "quantity": 1, "label": "Short Put (מכירה)"},
            ]

        # 3. Bear Put Spread
        elif "bear put" in name:
            if risk_key == "conservative":
                lp_sigma, sp_sigma = 0.0, 1.5 + skew_put_offset
            elif risk_key == "balanced":
                lp_sigma, sp_sigma = 0.5 + skew_put_offset, 1.0 + skew_put_offset
            else:
                lp_sigma, sp_sigma = 0.5 + skew_put_offset, 0.8 + skew_put_offset

            k2 = round_strike(spot - lp_sigma * one_sigma)  # Long Put (higher strike)
            k1 = round_strike(spot - sp_sigma * one_sigma)  # Short Put (lower strike)
            if k2 <= k1:
                k1 = k2 - step

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k2, "quantity": 1, "label": "Long Put (קנייה)"},
                {"action": "Sell", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Short Put (מכירה)"},
            ]

        # 4. Bear Call Spread
        elif "bear call" in name:
            if risk_key == "conservative":
                sc_sigma = 1.5 + stress_buffer
                lc_sigma = 2.0
            elif risk_key == "balanced":
                sc_sigma = 1.0 + stress_buffer
                lc_sigma = 1.5
            else:
                sc_sigma = 0.5 + stress_buffer
                lc_sigma = 1.0

            k1 = round_strike(spot + sc_sigma * one_sigma)  # Short Call (lower strike)
            k2 = round_strike(spot + lc_sigma * one_sigma)  # Long Call (higher strike)
            if k2 <= k1:
                k2 = k1 + step

            legs = [
                {"action": "Sell", "option_type": "Call", "strike": k1, "quantity": 1, "label": "Short Call (מכירה)"},
                {"action": "Buy", "option_type": "Call", "strike": k2, "quantity": 1, "label": "Long Call (הגנה)"},
            ]

        # 5. Bullish Butterfly / Broken-Wing Butterfly (פרפר Call שורי)
        elif "shuri" in name or ("butterfly" in name and "call" in name) or "שורי" in name:
            if risk_key == "conservative":
                center_sigma, wing_sigma = 0.5, 0.8
            elif risk_key == "balanced":
                center_sigma, wing_sigma = 0.8, 0.6
            else:
                center_sigma, wing_sigma = 1.0, 0.5

            k2 = round_strike(spot + center_sigma * one_sigma)
            w_pts = max(step, round_strike(wing_sigma * one_sigma))
            k1 = k2 - w_pts
            k3 = k2 + int(round(1.5 * w_pts / step) * step)  # Broken wing wider

            legs = [
                {"action": "Buy", "option_type": "Call", "strike": k1, "quantity": 1, "label": "Long Call (כנף תחתונה)"},
                {"action": "Sell", "option_type": "Call", "strike": k2, "quantity": 2, "label": "Short 2 Calls (מרכז)"},
                {"action": "Buy", "option_type": "Call", "strike": k3, "quantity": 1, "label": "Long Call (כנף עליונה)"},
            ]

        # 6. Bearish Butterfly / Broken-Wing Butterfly (פרפר Put דובי)
        elif "dubi" in name or ("butterfly" in name and "put" in name) or "דובי" in name:
            if risk_key == "conservative":
                center_sigma, wing_sigma = 0.5 + skew_put_offset, 0.8
            elif risk_key == "balanced":
                center_sigma, wing_sigma = 0.8 + skew_put_offset, 0.6
            else:
                center_sigma, wing_sigma = 1.0 + skew_put_offset, 0.5

            k2 = round_strike(spot - center_sigma * one_sigma)
            w_pts = max(step, round_strike(wing_sigma * one_sigma))
            k3 = k2 + w_pts
            k1 = k2 - int(round(1.5 * w_pts / step) * step)  # Broken wing wider

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Long Put (כנף תחתונה)"},
                {"action": "Sell", "option_type": "Put", "strike": k2, "quantity": 2, "label": "Short 2 Puts (מרכז)"},
                {"action": "Buy", "option_type": "Put", "strike": k3, "quantity": 1, "label": "Long Put (כנף עליונה)"},
            ]

        # 7. Iron Condor or Default Neutral Baseline
        elif "iron condor" in name or not name:
            if risk_key == "conservative":
                sp_sigma, lp_sigma = 1.5 + skew_put_offset + stress_buffer, 2.0 + skew_put_offset
                sc_sigma, lc_sigma = 1.5 + stress_buffer, 2.0
            elif risk_key == "balanced":
                sp_sigma, lp_sigma = 1.0 + skew_put_offset + stress_buffer, 1.5 + skew_put_offset
                sc_sigma, lc_sigma = 1.0 + stress_buffer, 1.5
            else:
                sp_sigma, lp_sigma = 0.5 + skew_put_offset + stress_buffer, 1.0 + skew_put_offset
                sc_sigma, lc_sigma = 0.5 + stress_buffer, 1.0

            k1 = round_strike(spot - lp_sigma * one_sigma)
            k2 = round_strike(spot - sp_sigma * one_sigma)
            k3 = round_strike(spot + sc_sigma * one_sigma)
            k4 = round_strike(spot + lc_sigma * one_sigma)

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Long Put (כנף)"},
                {"action": "Sell", "option_type": "Put", "strike": k2, "quantity": 1, "label": "Short Put"},
                {"action": "Sell", "option_type": "Call", "strike": k3, "quantity": 1, "label": "Short Call"},
                {"action": "Buy", "option_type": "Call", "strike": k4, "quantity": 1, "label": "Long Call (כנף)"},
            ]

        # 8. Iron Butterfly / Long Butterfly
        elif "iron butterfly" in name or "butterfly" in name or "פרפר" in name:
            if risk_key == "conservative":
                wing_sigma = 1.5
            elif risk_key == "balanced":
                wing_sigma = 1.0
            else:
                wing_sigma = 0.5

            k2 = round_strike(spot)
            w_pts = max(step, round_strike(wing_sigma * one_sigma))
            k1 = k2 - w_pts
            k3 = k2 + w_pts

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Long Put כנף"},
                {"action": "Sell", "option_type": "Put", "strike": k2, "quantity": 1, "label": "Short Put מרכז"},
                {"action": "Sell", "option_type": "Call", "strike": k2, "quantity": 1, "label": "Short Call מרכז"},
                {"action": "Buy", "option_type": "Call", "strike": k3, "quantity": 1, "label": "Long Call כנף"},
            ]

        # 9. Call Ratio Backspread 1x2
        elif "backspread" in name and "call" in name:
            if risk_key == "conservative":
                sc_sigma, lc_sigma = 0.0, 1.0
            elif risk_key == "balanced":
                sc_sigma, lc_sigma = 0.3, 0.8
            else:
                sc_sigma, lc_sigma = 0.5, 1.0

            k1 = round_strike(spot + sc_sigma * one_sigma)
            k2 = round_strike(spot + lc_sigma * one_sigma)
            if k2 <= k1:
                k2 = k1 + step

            legs = [
                {"action": "Sell", "option_type": "Call", "strike": k1, "quantity": 1, "label": "Short 1 Call"},
                {"action": "Buy", "option_type": "Call", "strike": k2, "quantity": 2, "label": "Long 2 Calls"},
            ]

        # 10. Put Ratio Backspread 1x2
        elif "backspread" in name:
            if risk_key == "conservative":
                sp_sigma, lp_sigma = 0.0, 1.0 + skew_put_offset
            elif risk_key == "balanced":
                sp_sigma, lp_sigma = 0.3 + skew_put_offset, 0.8 + skew_put_offset
            else:
                sp_sigma, lp_sigma = 0.5 + skew_put_offset, 1.0 + skew_put_offset

            k2 = round_strike(spot - sp_sigma * one_sigma)  # Short Put (higher strike)
            k1 = round_strike(spot - lp_sigma * one_sigma)  # Long Put (lower strike)
            if k2 <= k1:
                k1 = k2 - step

            legs = [
                {"action": "Sell", "option_type": "Put", "strike": k2, "quantity": 1, "label": "Short 1 Put"},
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 2, "label": "Long 2 Puts"},
            ]

        # 11. Long Straddle / Strangle
        elif "straddle" in name or "strangle" in name:
            if risk_key == "conservative":
                c_sigma, p_sigma = 0.5, 0.5 + skew_put_offset
            else:
                c_sigma, p_sigma = 0.0, 0.0

            k1 = round_strike(spot - p_sigma * one_sigma)
            k2 = round_strike(spot + c_sigma * one_sigma)

            legs = [
                {"action": "Buy", "option_type": "Put", "strike": k1, "quantity": 1, "label": "Long Put"},
                {"action": "Buy", "option_type": "Call", "strike": k2, "quantity": 1, "label": "Long Call"},
            ]

        else:
            k1 = round_strike(spot + 0.5 * one_sigma)
            k2 = round_strike(spot + 1.0 * one_sigma)
            legs = [
                {"action": "Buy", "option_type": "Call", "strike": k1, "quantity": 1, "label": "Long Call"},
                {"action": "Sell", "option_type": "Call", "strike": k2, "quantity": 1, "label": "Short Call"},
            ]

        summary_parts = [
            f"{leg['action']} {leg['quantity']}x {leg['option_type']} {leg['strike']}"
            for leg in legs
        ]

        strikes_dict: dict[str, int | None] = {
            "long_put": next((l["strike"] for l in legs if l["action"] == "Buy" and l["option_type"] == "Put"), None),
            "short_put": next((l["strike"] for l in legs if l["action"] == "Sell" and l["option_type"] == "Put"), None),
            "short_call": next((l["strike"] for l in legs if l["action"] == "Sell" and l["option_type"] == "Call"), None),
            "long_call": next((l["strike"] for l in legs if l["action"] == "Buy" and l["option_type"] == "Call"), None),
        }

        profiles[risk_key] = {
            "label": risk_label,
            "legs": legs,
            "strikes": strikes_dict,
            "summary": " · ".join(summary_parts),
            "one_sigma_pts": round(one_sigma, 1),
        }

    return profiles


def _candidate(name: str, rationale: str, risk_note: str) -> StrategyCandidate:
    return StrategyCandidate(name=name, rationale=rationale, risk_note=risk_note)


def _pricing_view(
    implied_volatility: float | None, forecast_volatility: float | None
) -> tuple[str, float | None]:
    if implied_volatility is None or forecast_volatility is None:
        return "לא זמין", None
    premium = implied_volatility - forecast_volatility
    threshold = max(0.02, forecast_volatility * 0.10)
    if premium >= threshold:
        return "פרמיה גלומה עשירה יחסית", premium
    if premium <= -threshold:
        return "פרמיה גלומה זולה יחסית", premium
    return "תמחור גלום קרוב לתחזית", premium


def recommend_strategy(
    *,
    spot: float | None,
    forecast_volatility: float | None,
    implied_volatility: float | None,
    trend_score: float | None,
    volatility_score: float | None,
    regime: str,
    horizon_days: int = 14,
    premium_sale_eligible: bool = False,
) -> StrategyRecommendation:
    """Return a bounded, general strategy-family recommendation.

    ``implied_volatility`` and ``forecast_volatility`` are annualized decimals.
    The IV comparison is only a proxy because VTA35 and the forecast do not
    necessarily match the selected expiry.
    """

    if horizon_days not in (3, 7, 14, 30):
        raise ValueError("horizon_days must be one of 3, 7, 14 or 30")

    core = (
        probability_band(spot, forecast_volatility, horizon_days, 0.5)
        if spot is not None
        else None
    )
    base = (
        probability_band(spot, forecast_volatility, horizon_days, 1.0)
        if spot is not None
        else None
    )
    pricing, premium = _pricing_view(implied_volatility, forecast_volatility)

    missing = []
    if spot is None or forecast_volatility is None:
        missing.append("חסרים מחיר מדד או תחזית תנודתיות לחישוב הטווח")
    if trend_score is None:
        missing.append("חסר ציון מגמה")
    if volatility_score is None:
        missing.append("חסר ציון מצב תנודתיות")
    if missing:
        return StrategyRecommendation(
            status="אין המלצה",
            primary=None,
            alternatives=(),
            horizon_days=horizon_days,
            market_view="לא זמין",
            volatility_view="לא זמין",
            pricing_view=pricing,
            core_range=core,
            base_range=base,
            focus_range=None,
            focus_label="לא ניתן לחשב אזור פעולה",
            target_level=None,
            explanation="אין די נתונים לבחירת משפחת אסטרטגיה באופן עקבי.",
            warnings=tuple(missing),
            scenario_fit=(),
            premium_sale_eligible=False,
        )

    if trend_score >= 0.4:
        direction = "חיובי"
    elif trend_score <= -0.4:
        direction = "שלילי"
    else:
        direction = "ניטרלי / מעורב"

    if volatility_score >= 1 / 3:
        vol_state = "מתרחבת"
    elif volatility_score <= -1 / 3:
        vol_state = "מתכווצת"
    else:
        vol_state = "מעורבת"

    rich = premium is not None and pricing.startswith("פרמיה גלומה עשירה")
    cheap = premium is not None and pricing.startswith("פרמיה גלומה זולה")
    stressed = regime in {"זהירות", "לחץ גבוה"}

    bull_call = _candidate(
        "Bull Call Spread",
        "הטיה חיובית עם סיכון מוגבל ואזור רווח רחב יותר מפרפר.",
        "הרווח מוגבל; שחיקת זמן פועלת נגד הצד הקנוי.",
    )
    bear_put = _candidate(
        "Bear Put Spread",
        "הטיה שלילית עם סיכון מוגבל ואזור רווח רחב יותר מפרפר.",
        "הרווח מוגבל; שחיקת זמן פועלת נגד הצד הקנוי.",
    )
    bull_put = _candidate(
        "Bull Put Spread",
        "מבנה אשראי מוגבל־סיכון לשוק יציב עד עולה כאשר הפרמיה עשירה.",
        "חשוף לירידה חדה; יש לאמת פרמיה, נזילות והפסד מרבי לפני ביצוע.",
    )
    bear_call = _candidate(
        "Bear Call Spread",
        "מבנה אשראי מוגבל־סיכון לשוק יציב עד יורד כאשר הפרמיה עשירה.",
        "חשוף לעלייה חדה; יש לאמת פרמיה, נזילות והפסד מרבי לפני ביצוע.",
    )
    bullish_butterfly = _candidate(
        "פרפר Call שורי / Broken-Wing Butterfly",
        "מתאים לעלייה מתונה לעבר אזור יעד, תוך סיכון מוגבל.",
        "אזור הרווח צר יחסית ותלוי בהגעה לאזור המרכז סמוך לפקיעה.",
    )
    bearish_butterfly = _candidate(
        "פרפר Put דובי / Broken-Wing Butterfly",
        "מתאים לירידה מתונה לעבר אזור יעד, תוך סיכון מוגבל.",
        "אזור הרווח צר יחסית ותלוי בהגעה לאזור המרכז סמוך לפקיעה.",
    )
    call_backspread = _candidate(
        "Call Ratio Backspread 1×2",
        "מתאים רק לתרחיש פריצה חדה מעלה יחד עם התרחבות תנודתיות.",
        "קיים עמק הפסד באזור שבין הרגל הקצרה לרגליים הקנויות.",
    )
    put_backspread = _candidate(
        "Put Ratio Backspread 1×2",
        "מתאים רק לתרחיש שבירה חדה מטה יחד עם התרחבות תנודתיות.",
        "קיים עמק הפסד באזור שבין הרגל הקצרה לרגליים הקנויות.",
    )
    long_vol = _candidate(
        "Long Straddle / Strangle",
        "מתאים לצפי לתנועה גדולה ללא כיוון כאשר התנודתיות הגלומה אינה יקרה.",
        "Theta שלילית; נדרשת תנועה גדולה מספיק כדי לכסות את שתי הפרמיות.",
    )
    long_wings = _candidate(
        "פרפר הפוך / Long Iron Condor",
        "חלופה מוגבלת־סיכון לתנועה גדולה לשני הכיוונים.",
        "עלול להפסיד אם המדד נשאר באזור המרכז עד הפקיעה.",
    )
    iron_condor = _candidate(
        "Iron Condor",
        "מתאים לטווח רחב ויציב כאשר הפרמיה הגלומה עשירה.",
        "הפסד עלול להצטבר במהירות בפריצה; הכנפיים אינן מבטלות סיכון זנב.",
    )
    iron_butterfly = _candidate(
        "Iron Butterfly",
        "מתאים לצפי ממוקד שהמדד יישאר קרוב למרכז כאשר הפרמיה גבוהה.",
        "אזור הרווח צר וסיכון Gamma גדל סמוך לפקיעה.",
    )
    long_butterfly = _candidate(
        "Long Butterfly / Condor קנוי",
        "מבנה מוגבל־סיכון לתרחיש ניטרלי עם אזור יעד מוגדר.",
        "דורש שהמדד יסיים בתוך אזור ממוקד; מחיר הכניסה קובע את נקודות האיזון.",
    )
    calendar = _candidate(
        "Calendar / Diagonal",
        "חלופה למצב שקט כעת אך תנועה או תנודתיות צפויות מאוחר יותר.",
        "דורש עקום IV לשתי פקיעות ולכן נשאר מועמד מותנה בלבד.",
    )

    target = spot
    focus = core
    focus_label = "טווח ליבה ניטרלי (±0.5σ)"
    warnings = [
        "ההשוואה בין VTA35 לתחזית היא קירוב בלבד ואינה IV של פקיעה וסטרייק מסוימים.",
        "הטווחים סטטיסטיים ואינם נקודות איזון או אזורי רווח מדויקים.",
    ]

    if direction == "חיובי":
        target = core[1] if core else None
        focus = (spot, base[1]) if base and spot is not None else None
        focus_label = "אזור פעולה שורי: מחיר נוכחי עד ‎+1σ"
        if vol_state == "מתרחבת" and trend_score >= 0.8:
            primary = call_backspread
            alternatives = (bull_call, bullish_butterfly)
            explanation = "המגמה חיובית חזקה והטווחים מתרחבים; המבנה נותן עדיפות לפריצה משמעותית על פני עלייה מתונה."
            focus = (base[1], base[1] * 1.01) if base else None
            focus_label = "תרחיש הצלחה דורש מעבר משוער של ‎+1σ"
            target = base[1] if base else None
        elif rich and not stressed and premium_sale_eligible:
            primary = bull_put
            alternatives = (bullish_butterfly, bull_call)
            explanation = "המגמה חיובית והפרמיה הגלומה עשירה יחסית; מרווח אשראי מוגבל־סיכון מתאים לשוק יציב עד עולה."
        elif vol_state == "מתכווצת":
            primary = bullish_butterfly
            alternatives = (
                bull_call,
                bull_put if rich and not stressed and premium_sale_eligible else calendar,
            )
            explanation = "המגמה חיובית אך התנודתיות בדחיסה; פרפר שורי מתאים יותר לעלייה מדודה לעבר אזור יעד מאשר להימור על פריצה."
        else:
            primary = bull_call
            alternatives = (bullish_butterfly, call_backspread)
            explanation = "המגמה חיובית אך מצב התנודתיות אינו חד; מרווח חיובי פשוט שומר על סיכון מוגבל ואזור פעולה רחב."
    elif direction == "שלילי":
        target = core[0] if core else None
        focus = (base[0], spot) if base and spot is not None else None
        focus_label = "אזור פעולה דובי: ‎−1σ עד המחיר הנוכחי"
        if vol_state == "מתרחבת" and trend_score <= -0.8:
            primary = put_backspread
            alternatives = (bear_put, bearish_butterfly)
            explanation = "המגמה שלילית חזקה והטווחים מתרחבים; המבנה נותן עדיפות לשבירה משמעותית על פני ירידה מתונה."
            focus = (base[0] * 0.99, base[0]) if base else None
            focus_label = "תרחיש הצלחה דורש מעבר משוער של ‎−1σ"
            target = base[0] if base else None
        elif rich and not stressed and premium_sale_eligible:
            primary = bear_call
            alternatives = (bearish_butterfly, bear_put)
            explanation = "המגמה שלילית והפרמיה הגלומה עשירה יחסית; מרווח אשראי מוגבל־סיכון מתאים לשוק יציב עד יורד."
        elif vol_state == "מתכווצת":
            primary = bearish_butterfly
            alternatives = (
                bear_put,
                bear_call if rich and not stressed and premium_sale_eligible else calendar,
            )
            explanation = "המגמה שלילית אך התנודתיות בדחיסה; פרפר דובי מתאים לירידה מדודה לעבר אזור יעד."
        else:
            primary = bear_put
            alternatives = (bearish_butterfly, put_backspread)
            explanation = "המגמה שלילית אך מצב התנודתיות אינו חד; מרווח דובי פשוט שומר על סיכון מוגבל ואזור פעולה רחב."
    else:
        target = spot
        if vol_state == "מתרחבת" and (cheap or not rich):
            primary = long_vol
            alternatives = (long_wings, calendar)
            explanation = "אין כיוון מובהק אך התנודתיות מתרחבת; המבנה מחפש תנועה גדולה באחד משני הכיוונים."
            focus = base
            focus_label = "נדרשת יציאה מעבר לטווח ‎±1σ בקירוב"
        elif (
            vol_state == "מתכווצת"
            and rich
            and not stressed
            and premium_sale_eligible
        ):
            primary = iron_condor
            alternatives = (iron_butterfly, long_butterfly)
            explanation = "המגמה ניטרלית, הטווחים בדחיסה והפרמיה עשירה; Condor מוגבל־סיכון מתאים לתרחיש של הישארות בטווח."
            focus = base
            focus_label = "טווח שמירה משוער: ‎±1σ"
        elif abs(trend_score) <= 0.2 and vol_state == "מתכווצת":
            primary = long_butterfly
            alternatives = (calendar, iron_condor)
            explanation = "המדד ניטרלי והתנודתיות מתכווצת, אך אין יתרון תמחורי ברור למכירת פרמיה; עדיף מבנה יעד מוגבל־סיכון."
        else:
            return StrategyRecommendation(
                status="אין עסקה מועדפת",
                primary=None,
                alternatives=(long_butterfly, calendar),
                horizon_days=horizon_days,
                market_view=direction,
                volatility_view=vol_state,
                pricing_view=pricing,
                core_range=core,
                base_range=base,
                focus_range=core,
                focus_label="טווח ליבה לצפייה בלבד",
                target_level=spot,
                explanation="אותות הכיוון והתנודתיות אינם יוצרים כרגע תרחיש עקבי מספיק לבחירת מבנה עיקרי.",
                warnings=tuple(warnings),
                scenario_fit=(),
                premium_sale_eligible=premium_sale_eligible,
            )

    if stressed and primary in {bull_put, bear_call, iron_condor, iron_butterfly}:
        warnings.append(
            "משטר הלחץ חוסם העדפה למכירת פרמיה; הוצגה חלופה קנויה ומוגבלת־סיכון."
        )
    if rich and not premium_sale_eligible:
        warnings.append(
            "מכירת פרמיה חסומה: כרטיס הראיות טרם עבר מדגם, lift OOS, FDR, "
            "non-overlap ויציבות משטרים."
        )
    if horizon_days == 3:
        warnings.append(
            "אופק של 3 ימים מוצג לצפייה בלבד; נתוני סוף־יום אינם מתאימים כברירת מחדל לעסקאות קצרות מאוד."
        )
    if horizon_days == 30:
        warnings.append(
            "באופק 30 יום Calendar/Diagonal דורשים נתוני IV לשתי פקיעות לפני בחירה מעשית."
        )

    scenario_fit = (
        ("מגמה", direction, "מתאים" if direction != "ניטרלי / מעורב" else "מותנה"),
        ("תנודתיות", vol_state, "מתאים" if vol_state != "מעורבת" else "מותנה"),
        (
            "תמחור IV",
            pricing,
            "זכאי" if premium_sale_eligible else "הקשר בלבד",
        ),
        ("משטר לחץ", regime, "חסום" if stressed else "תקין"),
    )
    strikes_map = calculate_strategy_strikes(
        spot,
        forecast_volatility,
        horizon_days,
        primary.name if primary else None,
        regime=regime,
    )
    return StrategyRecommendation(
        status="מועמד כללי",
        primary=primary,
        alternatives=alternatives,
        horizon_days=horizon_days,
        market_view=direction,
        volatility_view=vol_state,
        pricing_view=pricing,
        core_range=core,
        base_range=base,
        focus_range=focus,
        focus_label=focus_label,
        target_level=target,
        explanation=explanation,
        warnings=tuple(warnings),
        scenario_fit=scenario_fit,
        premium_sale_eligible=premium_sale_eligible,
        suggested_strikes=strikes_map,
    )
