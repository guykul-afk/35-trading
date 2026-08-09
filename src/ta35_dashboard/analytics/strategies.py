"""General option-strategy families derived from the Lite market state.

The module deliberately stops before contract selection, payoff estimation or
order advice.  It maps the dashboard's descriptive state to a transparent
strategy family and statistical scenario range.
"""

from __future__ import annotations

from dataclasses import dataclass

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
        elif rich and not stressed:
            primary = bull_put
            alternatives = (bullish_butterfly, bull_call)
            explanation = "המגמה חיובית והפרמיה הגלומה עשירה יחסית; מרווח אשראי מוגבל־סיכון מתאים לשוק יציב עד עולה."
        elif vol_state == "מתכווצת":
            primary = bullish_butterfly
            alternatives = (bull_call, bull_put if rich and not stressed else calendar)
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
        elif rich and not stressed:
            primary = bear_call
            alternatives = (bearish_butterfly, bear_put)
            explanation = "המגמה שלילית והפרמיה הגלומה עשירה יחסית; מרווח אשראי מוגבל־סיכון מתאים לשוק יציב עד יורד."
        elif vol_state == "מתכווצת":
            primary = bearish_butterfly
            alternatives = (bear_put, bear_call if rich and not stressed else calendar)
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
        elif vol_state == "מתכווצת" and rich and not stressed:
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
            )

    if stressed and primary in {bull_put, bear_call, iron_condor, iron_butterfly}:
        warnings.append(
            "משטר הלחץ חוסם העדפה למכירת פרמיה; הוצגה חלופה קנויה ומוגבלת־סיכון."
        )
    if horizon_days == 3:
        warnings.append(
            "אופק של 3 ימים מוצג לצפייה בלבד; נתוני סוף־יום אינם מתאימים כברירת מחדל לעסקאות קצרות מאוד."
        )
    if horizon_days == 30:
        warnings.append(
            "באופק 30 יום Calendar/Diagonal דורשים נתוני IV לשתי פקיעות לפני בחירה מעשית."
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
    )
