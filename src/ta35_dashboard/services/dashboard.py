"""Framework-neutral view model for the Lite Streamlit dashboard."""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import UTC, date, datetime

from ta35_dashboard.analytics import indicator_signal
from ta35_dashboard.storage import SQLiteRepository

from .backtest import DEFAULT_STRENGTH_HORIZON, BacktestReport, run_backtest
from .research import run_research_backtest


@dataclass(frozen=True, slots=True)
class SnapshotMeta:
    as_of: date
    source: str
    market_data_type: str
    stale: bool
    age_days: int


@dataclass(frozen=True, slots=True)
class MetricCard:
    key: str
    label: str
    value: float | None
    format: str
    help: str
    volatility_arrow: str
    volatility_strength: int
    volatility_backtest_observations: int
    volatility_hit_rate: float | None
    market_arrow: str
    market_strength: int
    market_backtest_observations: int
    market_hit_rate: float | None
    signal_note: str


@dataclass(frozen=True, slots=True)
class SeriesHealth:
    symbol: str
    last_date: date | None
    observations: int
    status: str
    source: str | None


@dataclass(frozen=True, slots=True)
class EvidenceCard:
    horizon_days: int
    n_eff: int
    lift: float | None
    fdr_q: float | None
    nonoverlap_rate: float | None
    positive_regimes: int
    tested_regimes: int
    eligible: bool
    status: str


@dataclass(frozen=True, slots=True)
class RegimeMatrix:
    market_state: str
    volatility_state: str
    cell: str


@dataclass(frozen=True, slots=True)
class DashboardBundle:
    meta: SnapshotMeta
    regime: str
    cards: tuple[MetricCard, ...]
    health: tuple[SeriesHealth, ...]
    ta35_dates: tuple[date, ...]
    ta35_closes: tuple[float, ...]
    vta35_dates: tuple[date, ...]
    vta35_values: tuple[float, ...]
    forecast_volatility: float | None
    volatility_direction: str
    volatility_direction_score: float | None
    market_trend: str
    market_trend_score: float | None
    implied_volatility: float | None
    backtest: BacktestReport
    premium_evidence: EvidenceCard
    regime_matrix: RegimeMatrix
    context_ablation: tuple[dict[str, object], ...]


CARD_DEFINITIONS = (
    (
        "vta35",
        "VTA35",
        ".1f",
        """**מהו המדד?** מדד התנודתיות הגלומה של אופציות על ת״א־35, המבטא את
ציפיית השוק לתנודתיות שנתית בקירוב ל־30 הימים הבאים, בנקודות אחוז.

**איך הוא בנוי?** הבורסה מחשבת אותו ממחירי אופציות ת״א־35 במגוון מחירי מימוש,
כך שהוא משקף את התנודתיות הגלומה בעקום האופציות ולא את כיוון המדד הצפוי.

**איך מפרשים?** ערך גבוה מעיד על אי־ודאות ותמחור הגנה גבוהים יותר; ערך נמוך
מעיד על שוק רגוע יחסית.

**חשוב לדעת:** ערך 20 פירושו תנודתיות שנתית גלומה של כ־20%, לא צפי לירידה
של 20%. המדד משקף גם ביקוש והיצע לאופציות ולא רק תחזית טהורה.""",
    ),
    (
        "forecast_rv_3d",
        "תחזית RV ל־3 ימים",
        ".1%",
        """**מהו המדד?** אומדן לתנודתיות הממומשת השנתית הצפויה בטווח הקצר,
המוצג באחוזים ומשמש גם לחישוב מניפת ההסתברות.

**איך הוא בנוי?** חציון האומדנים הזמינים: RV של 5 ימים, RV של 20 ימים,
EWMA ל־60 תשואות עם מקדם דעיכה 0.94, ו־Yang–Zhang ל־20 ימי OHLC. כל האומדנים
מחושבים מתשואות לוגריתמיות ומותאמים לשנה לפי 252 ימי מסחר.

**איך מפרשים?** עלייה מצביעה על התרחבות צפויה בטווח התנועות היומי, וירידה על
התכווצות.

**חשוב לדעת:** החציון מפחית רגישות לאומדן חריג, אך כל רכיב מבוסס בעיקר על
העבר הקרוב. זו תחזית סטטיסטית, לא הבטחה לתנודה שתתממש.""",
    ),
    (
        "vrp_spread",
        "פרמיית IV–RV",
        ".1%",
        """**מהו המדד?** הפער בין התנודתיות הגלומה באופציות לבין התנודתיות
שהתממשה בפועל במדד.

**איך הוא בנוי?** `VTA35 / 100 − RV20`, כאשר RV20 היא סטיית התקן השנתית של
התשואות הלוגריתמיות ב־20 ימי המסחר האחרונים.

**איך מפרשים?** פער חיובי אומר שהאופציות מתמחרות תנודתיות גבוהה מזו שנמדדה
לאחרונה — לעיתים פרמיית ביטוח/אי־ודאות. פער שלילי אומר שהתנודתיות האחרונה גבוהה
מהגלומה.

**חשוב לדעת:** הפער אינו לבדו הוכחה שאופציות יקרות או זולות, משום שאופק VTA35
וחלון RV20 אינם זהים וגם הסיכון העתידי עשוי להשתנות.""",
    ),
    (
        "rv_acceleration",
        "האצת תנודתיות",
        ".2f",
        """**מהו המדד?** יחס הבוחן אם התנודתיות האחרונה מאיצה או נרגעת ביחס
לחודש המסחר האחרון.

**איך הוא בנוי?** `RV5 / RV20`: תנודתיות ממומשת שנתית מחמשת הימים האחרונים
חלקי התנודתיות הממומשת מ־20 הימים האחרונים.

**איך מפרשים?** מעל 1 פירושו שהטווח הקצר תנודתי יותר; מתחת ל־1 פירושו שהוא
רגוע יותר. ערך 1.20, למשל, משמעו ש־RV5 גבוהה ב־20% מ־RV20.

**חשוב לדעת:** בגלל חלון של חמישה ימים, המדד רגיש במיוחד ליום קיצוני ועלול
להשתנות במהירות כאשר אותו יום יוצא מהחלון.""",
    ),
    (
        "gap_share_20",
        "משקל Gap",
        ".0%",
        """**מהו המדד?** שיעור התנודתיות שמתרחש בין סגירת יום אחד לפתיחת יום
המסחר הבא, לעומת התנועה הכוללת מחוץ ובתוך יום המסחר.

**איך הוא בנוי?** ב־20 ימי OHLC מחושבת שונות ה־Gap באמצעות
`ln(פתיחה / סגירה קודמת)` ושונות תוך־יומית באמצעות `ln(סגירה / פתיחה)`;
הכרטיס מציג `שונות Gap / (שונות Gap + שונות תוך־יומית)`.

**איך מפרשים?** שיעור גבוה מעיד שחלק גדול מהסיכון מגיע מחדשות לילה ומפתיחות
חדות, כשהשוק סגור וקשה יותר להגיב.

**חשוב לדעת:** זהו פירוק שונות, לא שיעור הימים שנפתחו ב־Gap, והוא אינו מצביע
על כיוון הפתיחה אלא רק על גודל התרומה לתנודתיות.""",
    ),
    (
        "expected_move_3d_points",
        "טווח 3 ימים",
        ".0f",
        """**מהו המדד?** רוחב מהלך של סטיית תקן אחת בת״א־35 לאורך שלושת ימי
המסחר הבאים, בנקודות מדד, לכל כיוון סביב הרמה הנוכחית.

**איך הוא בנוי?** `רמת ת״א־35 × תחזית RV × √(3 / 252)`. תחזית ה־RV היא
החציון המשולב המתואר בכרטיס התחזית.

**איך מפרשים?** בהנחת תשואות נורמליות ותנודתיות קבועה, הטווח `מדד ± הערך`
מכיל בקירוב 68.3% מהתוצאות.

**חשוב לדעת:** בפועל התשואות עשויות להיות מוטות ובעלות זנבות עבים, והתנודתיות
עשויה להשתנות. לכן זהו אומדן הסתברותי, לא יעד מחיר או גבול לתנועה.""",
    ),
    (
        "vix_curve_ratio",
        "VIX9D / VIX3M",
        ".2f",
        """**מהו המדד?** היחס בין התנודתיות הגלומה הקצרה מאוד בארה״ב
(VIX9D, כתשעה ימים) לבין התנודתיות הגלומה לשלושה חודשים (VIX3M).

**איך הוא בנוי?** הערך האחרון של `VIX9D` מחולק בערך האחרון של `VIX3M`.

**איך מפרשים?** יחס מעל 1 מצביע על עקום הפוך ולחץ מיידי: השוק מתמחר את הימים
הקרובים כתנודתיים יותר מהחודשים הבאים. מתחת ל־1 הוא המבנה הרגיל יותר.

**חשוב לדעת:** זהו מדד לחץ גלובלי שמקורו באופציות בארה״ב; הוא יכול להשפיע על
השוק המקומי, אך אינו חייב לעבור לת״א־35 באותו כיוון או באותה עוצמה.""",
    ),
    (
        "usdils_change_5d",
        "דולר/שקל 5 ימים",
        ".1%",
        """**מהו המדד?** השינוי המצטבר בשער דולר/שקל בחמשת ימי הנתונים
האחרונים, כאינדיקציה ללחץ מטבע מקומי.

**איך הוא בנוי?** `שער אחרון / שער לפני 5 ימי נתונים − 1`, על בסיס סדרת השער
היציג. החישוב משתמש בשש תצפיות כדי למדוד חמישה שינויים.

**איך מפרשים?** ערך חיובי פירושו התחזקות הדולר והיחלשות השקל; ערך שלילי פירושו
התחזקות השקל. תנועה חיובית חדה יכולה להתלוות לעלייה באי־ודאות המקומית.

**חשוב לדעת:** השער מושפע גם מפערי ריבית, מהדולר בעולם, מגידורים ומזרימות הון;
לכן שינוי של חמישה ימים אינו מדד נקי לסיכון מקומי.""",
    ),
    (
        "rv_20_60_ratio",
        "מבנה RV 20/60",
        ".2f",
        """**מהו המדד?** יחס בין התנודתיות הממומשת בחודש האחרון לבין הרבעון האחרון.

**איך הוא בנוי?** `RV20 / RV60`, כאשר שני הרכיבים הם סטיית התקן השנתית של
התשואות הלוגריתמיות ב־20 וב־60 ימי מסחר.

**איך מפרשים?** מעל 1 מצביע על האצה בחודש האחרון; מתחת ל־1 מצביע על רגיעה
יחסית ועל אפשרות לחזרה הדרגתית לממוצע הארוך יותר.

**חשוב לדעת:** זהו מדד יחסי ותיאורי. יחס נמוך אינו מבטיח שהתנודתיות תעלה,
ויחס גבוה יכול לרדת גם משום ש־RV60 עולה כשהימים התנודתיים נכנסים לחלון.""",
    ),
    (
        "atr_5_20_ratio",
        "לחץ טווח ATR 5/20",
        ".2f",
        """**מהו המדד?** בוחן אם טווחי המסחר האמיתיים מתרחבים או נדחסים בטווח הקצר.

**איך הוא בנוי?** ATR מנורמל למחיר מחושב כגבוה מבין גבוה–נמוך, גבוה–סגירה
קודמת ונמוך–סגירה קודמת. הכרטיס מציג `ATR5 / ATR20`.

**איך מפרשים?** מעל 1 מעיד שהטווחים האחרונים רחבים מהרגיל בחודש; מתחת ל־1
מעיד על דחיסה. מעבר מדחיסה להתרחבות עשוי לסמן שינוי במשטר התנודתיות.

**חשוב לדעת:** ATR מודד גודל תנועה ולא כיוון, ויום חריג יחיד יכול להשפיע מאוד
על חלון חמשת הימים.""",
    ),
    (
        "vta35_change_5d",
        "שינוי VTA35 ב־5 ימים",
        ".1%",
        """**מהו המדד?** קצב השינוי השבועי בציפיות התנודתיות הגלומות בת״א־35.

**איך הוא בנוי?** `VTA35 אחרון / VTA35 לפני חמישה ימי נתונים − 1`.

**איך מפרשים?** ערך חיובי מעיד שתמחור התנודתיות עולה; ערך שלילי מעיד שהוא
נרגע. הוא מוסיף כיוון לרמה המוחלטת של VTA35.

**חשוב לדעת:** שינוי חד יכול לנבוע מאירוע נקודתי או מגלגול אופציות, ואינו
תחזית ישירה לכיוון מדד המניות.""",
    ),
    (
        "vta35_zscore_60",
        "VTA35 ציון תקן 60",
        ".2f",
        """**מהו המדד?** מיקום VTA35 ביחס לרמתו הרגילה בשלושת חודשי המסחר האחרונים.

**איך הוא בנוי?** הרמה האחרונה פחות ממוצע 60 התצפיות, חלקי סטיית התקן שלהן.

**איך מפרשים?** 1 פירושו סטיית תקן אחת מעל הממוצע; ‎−1 פירושו סטיית תקן אחת
מתחתיו. כך ניתן להבחין בין רמה גבוהה או נמוכה יחסית למשטר האחרון.

**חשוב לדעת:** הממוצע וסטיית התקן משתנים עם הזמן, וההתפלגות אינה בהכרח
נורמלית; אין לפרש את הציון כהסתברות מדויקת.""",
    ),
    (
        "vix9d_vix_ratio",
        "VIX9D / VIX",
        ".2f",
        """**מהו המדד?** לחץ גלובלי מיידי לכ־9 ימים ביחס לציפייה לחודש.

**איך הוא בנוי?** הערך האחרון של VIX9D מחולק בערך האחרון של VIX.

**איך מפרשים?** מעל 1 מצביע שהימים הקרובים מתומחרים כתנודתיים מהחודש כולו;
מתחת ל־1 מצביע על עקום קצר רגיל יותר.

**חשוב לדעת:** שני המדדים מבוססים על אופציות S&P 500, ולכן הם הקשר גלובלי
לת״א־35 ולא מדידה ישירה של הסיכון המקומי.""",
    ),
    (
        "vix_vix3m_ratio",
        "VIX / VIX3M",
        ".2f",
        """**מהו המדד?** ציפיית התנודתיות לחודש ביחס לציפייה לכשלושה חודשים.

**איך הוא בנוי?** הערך האחרון של VIX מחולק בערך האחרון של VIX3M.

**איך מפרשים?** מעל 1 מעיד על לחץ חודשי חריג ועקום הפוך; מתחת ל־1 מעיד בדרך
כלל על עקום עולה, שבו אי־הוודאות הארוכה מתומחרת גבוה יותר.

**חשוב לדעת:** יחס נמוך מאוד יכול לשקף רגיעה מיידית או סיכון עתידי מתומחר;
ללא בחינת הרמות עצמן אין להבדיל ביניהם בוודאות.""",
    ),
)


def load_dashboard_bundle(
    repository: SQLiteRepository, *, now: datetime | None = None
) -> DashboardBundle:
    snapshot = repository.latest_snapshot()
    if snapshot is None:
        raise LookupError("no Lite EOD data; run the importer first")
    now = now or datetime.now(UTC)
    metrics = {metric.metric_name: metric for metric in repository.latest_metrics()}
    score = metrics.get("stress_score")
    regime = str(score.dimensions.get("regime", "לא זמין")) if score else "לא זמין"
    vol_direction = metrics.get("volatility_direction_score")
    trend = metrics.get("market_trend_state")
    backtest = run_backtest(
        repository,
        indicator_keys=tuple(definition[0] for definition in CARD_DEFINITIONS),
    )
    research = run_research_backtest(
        repository,
        indicator_keys=tuple(definition[0] for definition in CARD_DEFINITIONS),
    )
    short_names = {"Bull Put Spread", "Bear Call Spread", "Iron Condor", "Iron Butterfly"}
    strategy_table = research.tables.get("strategy_summary")
    candidates = strategy_table[
        (strategy_table["horizon"] == DEFAULT_STRENGTH_HORIZON)
        & strategy_table["strategy"].isin(short_names)
    ] if strategy_table is not None and not strategy_table.empty else None
    best = (
        candidates.sort_values(["fdr_q", "uplift"], ascending=[True, False]).iloc[0]
        if candidates is not None and not candidates.empty
        else None
    )
    eligible = bool(
        best is not None
        and best["selected_n"] >= 80
        and best["uplift"] > 0
        and best["fdr_q"] <= 0.05
        and best["nonoverlap_n_min"] >= 20
        and best["nonoverlap_success_rate"] > best["unconditional_baseline"]
        and best["positive_regimes"] >= 2
    )
    def finite_float(value: object) -> float | None:
        try:
            parsed = float(value)
        except (TypeError, ValueError):
            return None
        return parsed if math.isfinite(parsed) else None

    evidence = EvidenceCard(
        horizon_days=DEFAULT_STRENGTH_HORIZON,
        n_eff=int(best["nonoverlap_n_min"]) if best is not None else 0,
        lift=finite_float(best["uplift"]) if best is not None else None,
        fdr_q=finite_float(best["fdr_q"]) if best is not None else None,
        nonoverlap_rate=(finite_float(best["nonoverlap_success_rate"]) if best is not None else None),
        positive_regimes=int(best["positive_regimes"]) if best is not None else 0,
        tested_regimes=int(best["tested_regimes"]) if best is not None else 0,
        eligible=eligible,
        status="זכאי למכירת פרמיה" if eligible else "חסום — ראיות לא מספיקות",
    )
    cards_list: list[MetricCard] = []
    for key, label, fmt, help_text in CARD_DEFINITIONS:
        value = metrics[key].value if key in metrics else None
        vol_arrow, market_arrow, strength, signal_note = indicator_signal(
            key, value, metrics
        )
        vol_history = backtest.indicator(
            key, DEFAULT_STRENGTH_HORIZON, "volatility", vol_arrow
        )
        market_history = backtest.indicator(
            key, DEFAULT_STRENGTH_HORIZON, "market", market_arrow
        )
        cards_list.append(
            MetricCard(
                key=key,
                label=label,
                value=value,
                format=fmt,
                help=help_text,
                volatility_arrow=vol_arrow,
                volatility_strength=(vol_history.strength if vol_history else 1),
                volatility_backtest_observations=(
                    vol_history.observations if vol_history else 0
                ),
                volatility_hit_rate=(vol_history.hit_rate if vol_history else None),
                market_arrow=market_arrow,
                market_strength=(market_history.strength if market_history else strength),
                market_backtest_observations=(
                    market_history.observations if market_history else 0
                ),
                market_hit_rate=(market_history.hit_rate if market_history else None),
                signal_note=signal_note,
            )
        )
    cards = tuple(cards_list)
    symbols = ("TA35", "VTA35", "USDILS", "VIX9D", "VIX", "VIX3M")
    health: list[SeriesHealth] = []
    for symbol in symbols:
        history = repository.bar_history(symbol)
        last = history[-1] if history else None
        age = (now.date() - last.session_date).days if last else 9999
        health.append(
            SeriesHealth(
                symbol,
                last.session_date if last else None,
                len(history),
                "תקין" if age <= 3 else "ישן" if last else "חסר",
                last.source if last else None,
            )
        )
    ta = repository.bar_history("TA35", 252)
    vta = repository.bar_history("VTA35", 252)
    age_days = (now.date() - snapshot.session_date).days
    market_score = trend.value if trend else None
    market_state = (
        "עולה" if market_score is not None and market_score >= 0.4
        else "יורד" if market_score is not None and market_score <= -0.4
        else "ניטרלי"
    )
    volatility_score = vol_direction.value if vol_direction else None
    volatility_state = (
        "מתרחבת" if volatility_score is not None and volatility_score >= 1 / 3
        else "מתכווצת" if volatility_score is not None and volatility_score <= -1 / 3
        else "מעורבת"
    )
    ablation = research.tables.get("context_ablation_oos")
    return DashboardBundle(
        meta=SnapshotMeta(
            snapshot.session_date,
            snapshot.source,
            snapshot.market_data_type.value,
            age_days > 3,
            age_days,
        ),
        regime=regime,
        cards=cards,
        health=tuple(health),
        ta35_dates=tuple(bar.session_date for bar in ta),
        ta35_closes=tuple(bar.close for bar in ta),
        vta35_dates=tuple(bar.session_date for bar in vta),
        vta35_values=tuple(bar.close for bar in vta),
        forecast_volatility=(
            metrics["forecast_rv_3d"].value if "forecast_rv_3d" in metrics else None
        ),
        volatility_direction=(
            str(vol_direction.dimensions.get("state", "לא זמין"))
            if vol_direction
            else "לא זמין"
        ),
        volatility_direction_score=vol_direction.value if vol_direction else None,
        market_trend=(
            str(trend.dimensions.get("state", "לא זמין")) if trend else "לא זמין"
        ),
        market_trend_score=trend.value if trend else None,
        implied_volatility=(
            metrics["vta35"].value / 100
            if "vta35" in metrics and metrics["vta35"].value is not None
            else None
        ),
        backtest=backtest,
        premium_evidence=evidence,
        regime_matrix=RegimeMatrix(
            market_state=market_state,
            volatility_state=volatility_state,
            cell=f"{market_state} × {volatility_state}",
        ),
        context_ablation=(
            tuple(ablation.to_dict(orient="records"))
            if ablation is not None and not ablation.empty
            else ()
        ),
    )
