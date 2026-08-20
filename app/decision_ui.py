"""Streamlit UI components for rendering TA-35 Trade Decision Engine outputs (100% EOD Architecture)."""

from __future__ import annotations

import math
from typing import Any

import streamlit as st

from ta35_dashboard.analytics.payoff import (
    build_plotly_payoff_chart,
    generate_strategy_payoff_data,
)
from ta35_dashboard.decision_engine import (
    StrategyFamily,
    StrategyRecommendation,
    Verdict,
)


def _compute_statistical_legs_ui(
    spot_price: float,
    forecast_rv: float,
    horizon_days: int,
    family: StrategyFamily,
    prob_up: float = 0.50,
) -> tuple[dict[str, Any], ...]:
    """Self-contained statistical legs calculation for the UI."""
    sigma_1d = spot_price * forecast_rv * math.sqrt(max(1.0, horizon_days) / 365.0)

    def round_strike(val: float) -> float:
        return round(val / 10.0) * 10.0

    if family in (StrategyFamily.BULL_CALL_DEBIT, StrategyFamily.BEAR_CALL_CREDIT):
        k1 = round_strike(spot_price)
        k2 = round_strike(spot_price + 0.8 * sigma_1d)
        if family == StrategyFamily.BULL_CALL_DEBIT:
            return (
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k1, "ratio": 1, "label": f"קניית Call ATM ({k1:,.0f})"},
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": k2, "ratio": 1, "label": f"מכירת Call OTM (+0.8σ: {k2:,.0f})"},
            )
        else:
            return (
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.5, "estimated_strike": k1, "ratio": 1, "label": f"מכירת Call (+0.5σ: {k1:,.0f})"},
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.3, "estimated_strike": k2, "ratio": 1, "label": f"קניית Call הגנה (+1.3σ: {k2:,.0f})"},
            )

    elif family in (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.BEAR_PUT_DEBIT):
        if family == StrategyFamily.BULL_PUT_CREDIT:
            k1 = round_strike(spot_price - 0.5 * sigma_1d)
            k2 = round_strike(spot_price - 1.2 * sigma_1d)
            return (
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.5, "estimated_strike": k1, "ratio": 1, "label": f"מכירת Put OTM (-0.5σ: {k1:,.0f})"},
                {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.2, "estimated_strike": k2, "ratio": 1, "label": f"קניית Put הגנה (-1.2σ: {k2:,.0f})"},
            )
        else:
            kp_atm = round_strike(spot_price)
            kp_otm = round_strike(spot_price - 0.8 * sigma_1d)
            return (
                {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": kp_atm, "ratio": 1, "label": f"קניית Put ATM ({kp_atm:,.0f})"},
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": kp_otm, "ratio": 1, "label": f"מכירת Put OTM (-0.8σ: {kp_otm:,.0f})"},
            )

    elif family == StrategyFamily.DIRECTIONAL_BUTTERFLY:
        if prob_up >= 0.50:
            k_left = round_strike(spot_price)
            k_center = round_strike(spot_price + 0.8 * sigma_1d)
            k_right = round_strike(spot_price + 1.6 * sigma_1d)
            return (
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Call כנף תחתונה (ATM: {k_left:,.0f})"},
                {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Calls יעד מרכזי (+0.8σ: {k_center:,.0f})"},
                {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.6, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Call כנף עליונה (+1.6σ: {k_right:,.0f})"},
            )
        else:
            k_right = round_strike(spot_price)
            k_center = round_strike(spot_price - 0.8 * sigma_1d)
            k_left = round_strike(spot_price - 1.6 * sigma_1d)
            return (
                {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.6, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Put כנף תחתונה (-1.6σ: {k_left:,.0f})"},
                {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Puts יעד מרכזי (-0.8σ: {k_center:,.0f})"},
                {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Put כנף עליונה (ATM: {k_right:,.0f})"},
            )

    elif family == StrategyFamily.IRON_BUTTERFLY:
        k_atm = round_strike(spot_price)
        kp_long = round_strike(spot_price - 0.8 * sigma_1d)
        kc_long = round_strike(spot_price + 0.8 * sigma_1d)
        return (
            {"option_type": "PUT", "action": "BUY", "sigma_offset": -0.8, "estimated_strike": kp_long, "ratio": 1, "label": f"קניית Put כנף תחתונה (-0.8σ: {kp_long:,.0f})"},
            {"option_type": "PUT", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"מכירת Put מרכז בכסף (ATM: {k_atm:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"מכירת Call מרכז בכסף (ATM: {k_atm:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.8, "estimated_strike": kc_long, "ratio": 1, "label": f"קניית Call כנף עליונה (+0.8σ: {kc_long:,.0f})"},
        )

    elif family == StrategyFamily.LONG_BUTTERFLY:
        k_center = round_strike(spot_price)
        k_left = round_strike(spot_price - 0.8 * sigma_1d)
        k_right = round_strike(spot_price + 0.8 * sigma_1d)
        return (
            {"option_type": "CALL", "action": "BUY", "sigma_offset": -0.8, "estimated_strike": k_left, "ratio": 1, "label": f"קניית Call כנף שמאל (-0.8σ: {k_left:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_center, "ratio": 2, "label": f"מכירת 2 Calls מרכז (ATM: {k_center:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.8, "estimated_strike": k_right, "ratio": 1, "label": f"קניית Call כנף ימין (+0.8σ: {k_right:,.0f})"},
        )

    elif family == StrategyFamily.IRON_CONDOR:
        kp_long = round_strike(spot_price - 1.5 * sigma_1d)
        kp_short = round_strike(spot_price - 0.7 * sigma_1d)
        kc_short = round_strike(spot_price + 0.7 * sigma_1d)
        kc_long = round_strike(spot_price + 1.5 * sigma_1d)
        return (
            {"option_type": "PUT", "action": "BUY", "sigma_offset": -1.5, "estimated_strike": kp_long, "ratio": 1, "label": f"קניית Put כנף שמאל (-1.5σ: {kp_long:,.0f})"},
            {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.7, "estimated_strike": kp_short, "ratio": 1, "label": f"מכירת Put תחתון (-0.7σ: {kp_short:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.7, "estimated_strike": kc_short, "ratio": 1, "label": f"מכירת Call עליון (+0.7σ: {kc_short:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 1.5, "estimated_strike": kc_long, "ratio": 1, "label": f"קניית Call כנף ימין (+1.5σ: {kc_long:,.0f})"},
        )

    elif family == StrategyFamily.DEBIT_CONDOR:
        kp_long = round_strike(spot_price - 0.7 * sigma_1d)
        kp_short = round_strike(spot_price - 1.5 * sigma_1d)
        kc_long = round_strike(spot_price + 0.7 * sigma_1d)
        kc_short = round_strike(spot_price + 1.5 * sigma_1d)
        return (
            {"option_type": "PUT", "action": "BUY", "sigma_offset": -0.7, "estimated_strike": kp_long, "ratio": 1, "label": f"קניית Put (-0.7σ: {kp_long:,.0f})"},
            {"option_type": "PUT", "action": "SELL", "sigma_offset": -1.5, "estimated_strike": kp_short, "ratio": 1, "label": f"מכירת Put (-1.5σ: {kp_short:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.7, "estimated_strike": kc_long, "ratio": 1, "label": f"קניית Call (+0.7σ: {kc_long:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 1.5, "estimated_strike": kc_short, "ratio": 1, "label": f"מכירת Call (+1.5σ: {kc_short:,.0f})"},
        )

    elif family == StrategyFamily.LONG_STRADDLE:
        k_atm = round_strike(spot_price)
        return (
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Call ATM ({k_atm:,.0f})"},
            {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Put ATM ({k_atm:,.0f})"},
        )

    elif family == StrategyFamily.SHORT_STRADDLE:
        k_atm = round_strike(spot_price)
        return (
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"מכירת Call ATM ({k_atm:,.0f})"},
            {"option_type": "PUT", "action": "SELL", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"מכירת Put ATM ({k_atm:,.0f})"},
        )

    elif family == StrategyFamily.LONG_STRANGLE:
        kp = round_strike(spot_price - 0.8 * sigma_1d)
        kc = round_strike(spot_price + 0.8 * sigma_1d)
        return (
            {"option_type": "PUT", "action": "BUY", "sigma_offset": -0.8, "estimated_strike": kp, "ratio": 1, "label": f"קניית Put OTM (-0.8σ: {kp:,.0f})"},
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.8, "estimated_strike": kc, "ratio": 1, "label": f"קניית Call OTM (+0.8σ: {kc:,.0f})"},
        )

    elif family == StrategyFamily.SHORT_STRANGLE:
        kp = round_strike(spot_price - 0.8 * sigma_1d)
        kc = round_strike(spot_price + 0.8 * sigma_1d)
        return (
            {"option_type": "PUT", "action": "SELL", "sigma_offset": -0.8, "estimated_strike": kp, "ratio": 1, "label": f"מכירת Put OTM (-0.8σ: {kp:,.0f})"},
            {"option_type": "CALL", "action": "SELL", "sigma_offset": 0.8, "estimated_strike": kc, "ratio": 1, "label": f"מכירת Call OTM (+0.8σ: {kc:,.0f})"},
        )

    else:
        k_atm = round_strike(spot_price)
        return (
            {"option_type": "CALL", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Call ATM ({k_atm:,.0f})"},
            {"option_type": "PUT", "action": "BUY", "sigma_offset": 0.0, "estimated_strike": k_atm, "ratio": 1, "label": f"קניית Put ATM ({k_atm:,.0f})"},
        )


def get_strategy_rationale_and_considerations(
    family: StrategyFamily,
    prob_up: float,
    forecast_rv: float,
    regime: str,
) -> dict[str, str]:
    """Provides granular, quantitative considerations for each strategy family."""
    if family == StrategyFamily.BULL_PUT_CREDIT:
        return {
            "title": "Bull Put Credit Spread (מרווח פוט שורי לגביית פרמיה)",
            "role": "🥇 עדיפות 1 — אסטרטגיה ראשית (גביית פרמיית IV עודפת)",
            "rationale": (
                f"השוק במגמה עולה עם צפי לירידת תנודתיות ופרמיית שונות חיובית (VRP > 0). "
                f"מכירת מרווח פוט מאפשרת לנצל שחיקת זמן (Theta) מהירה ומרווח ביטחון סטטיסטי מתחת לספוט."
            ),
            "pros": "• הסתברות הצלחה גבוהה (PoP > 70%).\n• רווח מלא מתקבל גם אם המדד ידרוך במקום או יעלה קלות.\n• שחיקת תטא חיובית יומית.",
            "cons": "• סיכון/סיכוי א-סימטרי (הפסד מקסימלי גבוה מהרווח המקסימלי במקרה של קריסה).\n• דורש הקצאת ביטחונות בבורסה.",
            "when_to_choose": "מומלץ כברירת מחדל במשטר של מגמה חיובית וסביבת תנודתיות רגועה/יורדת.",
        }
    elif family == StrategyFamily.BULL_CALL_DEBIT:
        return {
            "title": "Bull Call Debit Spread (מרווח קול שורי בהשקעה מוגדרת)",
            "role": "🥈 עדיפות 2 — חלופה כיוונית מוגדרת סיכון (Debit)",
            "rationale": (
                f"רכישת מרווח קול לכידת מהלך עולה ישיר אל עבר טווח היעד. "
                f"הסיכון מוגבל מראש לעלות הפרמיה ששולמה בלבד ללא חשיפה לסיכון מכירת פוטים."
            ),
            "pros": "• סיכון מקסימלי מוגדר וידוע מראש (עלות המרווח בלבד).\n• אינו דורש ביטחונות מורכבים.\n• יחס סיכוי/סיכון אטרקטיבי אם המדד פורץ בעוצמה.",
            "cons": "• שחיקת תטא מתונה נגד הפוזיציה אם המדד דורך במקום.\n• נדרשת תנועה כיוונית בפועל כדי לממש רווח מלא.",
            "when_to_choose": "מומלץ אם מעדיפים להימנע ממכירת פוטים או אם חוששים מאירוע זנב גלובלי/ביטחוני פתאומי.",
        }
    elif family == StrategyFamily.DIRECTIONAL_BUTTERFLY:
        return {
            "title": "Directional Call Butterfly (פרפר כיווני ממוקד יעד)",
            "role": "🥉 עדיפות 3 — חלופה א-סימטרית ביחס סיכוי/סיכון מרבי",
            "rationale": (
                f"בניית פרפר א-סימטרי שמרכזו ממוקם בטווח היעד הסטטיסטי. "
                f"מאפשר להשיג יחס רווח להפסד של מעל 1:4 בעלות מינימלית."
            ),
            "pros": "• יחס סיכוי/סיכון מעולה (Risk/Reward גבוה במיוחד).\n• עלות כניסה זולה מאוד.\n• סיכון מוגבל לחלוטין.",
            "cons": "• חלון הרווח המקסימלי צר וממוקד סביב יעד הסטרייק המרכזי.\n• תנועה חדה מעבר ליעד שוחקת את הרווח המרבי.",
            "when_to_choose": "מומלץ למשקיע שמחפש מינוף סטטיסטי גבוה עם סיכון כספי מינימלי בנקודת היעד.",
        }
    elif family == StrategyFamily.BEAR_CALL_CREDIT:
        return {
            "title": "Bear Call Credit Spread (מרווח קול דובי לגביית פרמיה)",
            "role": "🥇 עדיפות 1 — אסטרטגיה ראשית (משטר דובי)",
            "rationale": "ניצול מגמת ירידה בשוק באמצעות גביית פרמיות Call מעל השוק.",
            "pros": "• הסתברות הצלחה גבוהה.\n• שחיקת תטא חיובית.",
            "cons": "• סיכון מוגבל אך גבוה מהרווח המקסימלי.",
            "when_to_choose": "במשטר דובי עם תנודתיות מתונה.",
        }
    elif family == StrategyFamily.BEAR_PUT_DEBIT:
        return {
            "title": "Bear Put Debit Spread (מרווח פוט דובי מוגדר סיכון)",
            "role": "🥈 עדיפות 2 — חלופה כיוונית יורדת",
            "rationale": "הגנה ורווח ממהלך ירידות מובהק בעלות מוגדרת.",
            "pros": "• רווח ממהלך ירידות מהיר.\n• סיכון מוגבל לפרמיה בלבד.",
            "cons": "• שחיקת זמן.",
            "when_to_choose": "כאשר צפויה התפרצות תנודתיות כלפי מטה.",
        }
    elif family == StrategyFamily.IRON_CONDOR:
        return {
            "title": "Iron Condor (קונדור ברזל לדשדוש וגביית פרמיות)",
            "role": "🥇 עדיפות 1 — אסטרטגיה ראשית (שוק מדשדש)",
            "rationale": "מכירת מרווח פוט ומרווח קול מחוץ לכסף לגביית פרמיה כפולה בשוק ללא מגמה.",
            "pros": "• שחיקת תטא כפולה משני הצדדים.\n• רווח מלא כל עוד המדד נשאר בתוך הטווח הרחב.",
            "cons": "• חשיפה לפריצה חדה באחד הצדדים.",
            "when_to_choose": "במשטר ניטרלי עם תנודתיות נרגעת.",
        }
    elif family == StrategyFamily.IRON_BUTTERFLY:
        return {
            "title": "Iron Butterfly (פרפר ברזל לגביית פרמיה מרבית בכסף)",
            "role": "🥈 עדיפות 2 — גביית פרמיה מרבית בכסף (Credit)",
            "rationale": "מכירת אוכף בכסף (ATM Call + Put) ורכישת כנפי הגנה (OTM Wings). מניב פרמיה כספית מקסימלית באפס כיווניות.",
            "pros": "• גביית פרמיה נטו גבוהה ביותר (Credit מקסימלי).\n• שחיקת תטא מואצת סביב הספוט.\n• סיכון מוגדר מראש על ידי הכנפיים.",
            "cons": "• חלון הפקיעה הרווחי צר יותר מקונדור (שיא הרווח ממוקד סביב שער הספוט בלבד).",
            "when_to_choose": "במשטר דשדוש מוחלט כשרמות ה-IV גבוהות ומצפים לדעיכת תנודתיות מהירה ללא תנועה במדד.",
        }
    elif family == StrategyFamily.LONG_BUTTERFLY:
        return {
            "title": "Long Call Butterfly (פרפר קנוי בעלות מינימלית)",
            "role": "🥉 עדיפות 3 — חלופה קנויה מוגדרת סיכון (Debit)",
            "rationale": "רכישת מבנה פרפר קולים (All-Call) בעלות דביט נמוכה ליצירת יחס סיכוי/סיכון גבוה ללא מכירת פוטים.",
            "pros": "• עלות כניסה זולה במיוחד (Debit מזערי).\n• סיכון מוגבל מראש לפרמיה הנמוכה ששולמה בלבד.\n• אינו דורש ביטחונות מורכבים.",
            "cons": "• שחיקת זמן (תטא שלילית) אם המדד מתרחק מהמרכז.\n• דורש פקיעה קרובה מאוד לספוט למימוש רווח מלא.",
            "when_to_choose": "במשטר דשדוש כשרמות ה-IV נמוכות ומחפשים מינוף סטטיסטי גבוה סביב הספוט בעלות סיכון כספי מינימלי.",
        }
    else:
        return {
            "title": f"{family.value} (אסטרטגיה מותאמת משטר)",
            "role": "חלופת מסחר משטר",
            "rationale": f"מבנה מותאם לפי תנאי השוק והתנודתיות באופק {regime}.",
            "pros": "• התאמה לטווח הסטטיסטי.",
            "cons": "• תלות בתנועת המדד.",
            "when_to_choose": "לפי העדפת ניהול הסיכונים של הסוחר.",
        }


def render_decision_hero(
    result: StrategyRecommendation,
    spot_price: float = 4150.0,
) -> None:
    """Renders the top Decision Hero view (100% EOD Quantitative Architecture)."""
    render_eod_strategy_hero(result, spot_price=spot_price)


def render_eod_strategy_hero(
    rec: StrategyRecommendation,
    spot_price: float = 4150.0,
) -> None:
    """Renders 3 prioritized StrategyRecommendation cards with explicit instructions, statistical legs, and visual charts."""
    st.caption(":green[📊 מודל קוואנטי סוף יום (EOD) — מבוסס נתונים רשמיים בלבד (בורסת ת״א / בנק ישראל / CBOE)]")

    # Top Macro & Market State Summary
    card_container = st.container(border=True)
    with card_container:
        col_view, col_fam, col_hor = st.columns([1.5, 2, 1])
        with col_view:
            st.markdown(f"### כיוון שוק: {rec.direction_view}")
            st.write(f"**הסתברות לעלייה P(up):** `{rec.direction_probability:.1%}`")
            st.write(f"**צפי תנודתיות:** `{rec.volatility_view}` ({rec.forecast_rv:.1%})")
            st.write(f"**משטר תנודתיות:** `{rec.regime}`")
            
        with col_fam:
            st.markdown(f"### מבנה מומלץ מוביל: {rec.primary_strategy_family.value}")
            alts_str = ", ".join(a.value for a in rec.alternatives)
            st.write(f"**חלופות מדורגות:** {alts_str}")
            st.write(f"**נימוק מרכזי:** {rec.rationale}")

        with col_hor:
            st.metric("אופק מומלץ", f"{rec.horizon_days} ימים")
            st.write(f"**רמת ביטחון בתחזית:** `{rec.forecast_confidence:.0%}`")
            st.write(f"**איכות נתונים:** `{rec.data_quality_score:.0%}`")

    # Target range & invalidation
    col_sc1, col_sc2 = st.columns(2)
    with col_sc1:
        with st.container(border=True):
            st.markdown("##### 🎯 טווח יעד סטטיסטי במדד")
            st.write(f"**טווח יעד צפוי:** `{rec.target_range[0]:,.1f} – {rec.target_range[1]:,.1f}`")
            st.write(f"**מניפת הסתברות (68%):** `{rec.probability_band[0]:,.1f} – {rec.probability_band[1]:,.1f}`")
    with col_sc2:
        with st.container(border=True):
            st.markdown("##### 🛑 רמת ביטול תזה (Invalidation)")
            st.write(f"**רמת מדד המבטלת את התזה:** `{rec.invalidation_level:,.1f}`")
            st.caption("חציית רמה זו מעידה על שינוי משטר שוק ומחייבת בחינה מחדש של הפוזיציה.")

    st.markdown("---")
    st.subheader("🏆 3 אסטרטגיות מומלצות לפי סדר עדיפויות ושיקולי מסחר")
    st.caption("לכל אסטרטגיה מפורטים השיקולים הכמותיים, מיקומי הרגליים והסטרייקים הסטטיסטיים, ותרשים רווח/הפסד (P&L) ויזואלי מלא.")

    # Gather top 3 distinct strategies
    strategies_to_render: list[tuple[int, StrategyFamily]] = [(1, rec.primary_strategy_family)]
    priority_counter = 2
    for alt in rec.alternatives:
        if alt != rec.primary_strategy_family and priority_counter <= 3:
            strategies_to_render.append((priority_counter, alt))
            priority_counter += 1

    # If fewer than 3, add fallback alternatives
    if len(strategies_to_render) < 3:
        all_families = [
            StrategyFamily.BULL_PUT_CREDIT,
            StrategyFamily.BULL_CALL_DEBIT,
            StrategyFamily.DIRECTIONAL_BUTTERFLY,
            StrategyFamily.IRON_CONDOR,
        ]
        for fam in all_families:
            if fam not in [s[1] for s in strategies_to_render] and len(strategies_to_render) < 3:
                strategies_to_render.append((len(strategies_to_render) + 1, fam))

    tab_titles = [
        f"{'🥇' if p == 1 else '🥈' if p == 2 else '🥉'} עדיפות {p}: {fam.value}"
        for p, fam in strategies_to_render
    ]
    strat_tabs = st.tabs(tab_titles)

    for tab, (prio, fam) in zip(strat_tabs, strategies_to_render, strict=False):
        with tab:
            details = get_strategy_rationale_and_considerations(
                fam, rec.direction_probability, rec.forecast_rv, rec.regime
            )
            
            with st.container(border=True):
                st.markdown(f"#### {details['role']}")
                st.markdown(f"**💡 רציונל כמותי:** {details['rationale']}")
                
                col_p, col_c = st.columns(2)
                with col_p:
                    st.markdown("**✅ יתרונות מרכזיים:**")
                    st.markdown(details["pros"])
                with col_c:
                    st.markdown("**⚠️ חסרונות ונקודות תורפה:**")
                    st.markdown(details["cons"])
                
                st.info(f"**🎯 מתי לבחור בחלופה זו?** {details['when_to_choose']}")

            # Compute statistical legs for this specific family
            legs = _compute_statistical_legs_ui(
                spot_price=spot_price,
                forecast_rv=rec.forecast_rv,
                horizon_days=rec.horizon_days,
                family=fam,
                prob_up=rec.direction_probability,
            )

            col_table, col_chart = st.columns([1.1, 1.4])
            with col_table:
                st.markdown("##### 📜 מיקומי רגליים מחושבים (לפי סטיות תקן σ)")
                leg_rows = []
                for l in legs:
                    leg_rows.append({
                        "תיאור רגל": l.get("label", ""),
                        "פעולה": l.get("action", ""),
                        "מיקום ב-σ": f"{l.get('sigma_offset', 0.0):+.1f}σ",
                        "סטרייק משוער": f"{l.get('estimated_strike', 0.0):,.0f}",
                        "יחס": l.get("ratio", 1),
                    })
                st.dataframe(leg_rows, use_container_width=True, hide_index=True)

                st.markdown("##### 📋 הנחיות ביצוע")
                st.markdown(
                    f"1. **פקיעה:** אופק מומלץ של **{rec.horizon_days} ימי מסחר**.\n"
                    f"2. **Stop Loss:** ביטול תזה אם ת״א־35 חוצה את **{rec.invalidation_level:,.1f}**."
                )

            with col_chart:
                st.markdown("##### 📈 פרופיל P&L בפקיעה והתפלגות הסתברות")
                render_single_strategy_chart(
                    fam=fam,
                    legs=legs,
                    spot_price=spot_price,
                    forecast_rv=rec.forecast_rv,
                    horizon_days=rec.horizon_days,
                )


def render_single_strategy_chart(
    fam: StrategyFamily,
    legs: tuple[dict[str, any], ...],
    spot_price: float,
    forecast_rv: float,
    horizon_days: int,
) -> None:
    """Builds and renders Plotly Payoff Chart for a single strategy family."""
    legs_payload = []
    for leg in legs:
        legs_payload.append({
            "action": leg.get("action", "BUY"),
            "option_type": leg.get("option_type", "CALL"),
            "strike": leg.get("estimated_strike", spot_price),
            "quantity": leg.get("ratio", 1),
            "label": leg.get("label", ""),
        })

    payoff_data = generate_strategy_payoff_data(
        spot=spot_price if spot_price > 0 else 4150.0,
        forecast_volatility=forecast_rv if forecast_rv > 0 else 0.15,
        horizon_days=max(1, horizon_days),
        legs=legs_payload,
    )

    fig = build_plotly_payoff_chart(
        payoff_data,
        title=f"P&L בפקיעה: {fam.value}",
    )
    st.plotly_chart(fig, use_container_width=True)

