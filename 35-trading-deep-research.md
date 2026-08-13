# מחקר עומק: מנגנון המלצת הטריידים והאינדיקטורים — 35-trading

**תאריך:** 2026-08-12 · **בסיס:** קריאת קוד מלאה של `guykul-afk/35-trading` (analytics, decision_engine, services, frozen_rules) + סקירת ספרות אקדמית ופרקטית עדכנית.

---

## חלק 1 — מיפוי המנגנון כפי שהוא היום

שרשרת ההמלצה בפועל:

1. **פיצ'רים (backtest.py `_historical_features`)** — RV מרובה-אומדנים (close-to-close, EWMA, Yang-Zhang, Parkinson/RS), אינדיקטורים מחקריים (downside_share_20, rs_range_5_20, trend_efficiency_20, reversal_5_vol_scaled...), VTA35 (z-score, change, vol-of-vol), VIX/VIX3M/VIX9D עם lag יום (נכון!), USDILS, ו-regime מבוסס ניקוד stress.
2. **תחזית תנודתיות** — `forecast_rv_3d = median(rv_5, rv_20, rv_ewma, rv_yz_20)`. HAR-3d מחושב אך משמש כ-benchmark/אינדיקטור בלבד, לא כתחזית המנוע.
3. **הסתברות כיוון** — `_probabilistic_family_model`: expanding percentile ranks → 6 משפחות → Ridge-Logit (IRLS) עם purge, non-overlap, walk-forward. זה החלק הכי סולידי במערכת.
4. **מנוע החלטה (engine.py)** — EOD mode: מיפוי דטרמיניסטי (prob_up, vol_state) → משפחת אסטרטגיה + רגליים בהיסטי-סיגמא קבועים. DDE mode: יצירת מועמדים מהשרשרת → `compute_dual_distribution_edge` → gates → Opportunity Score → TradeTicket.

---

## חלק 2 — ממצאים קריטיים בקוד הקיים (מסודר לפי חומרה)

### P0-1: "התפלגות השוק" ב-Dual-Edge אינה התפלגות השוק
`dual_edge.py` בונה את שתי ההתפלגויות — של המודל ושל "השוק" — כלוג-נורמליות עם **אותה סיגמא** (`forecast_rv`, שהיא תחזית פיזית!), כשההבדל היחיד הוא הסטת drift לפי `prob_up`. המשמעויות:

- **ה-Edge הוא פונקציה דטרמיניסטית של prob_up בלבד.** אין כאן שום זיהוי mispricing אמיתי — המנוע לא משווה את המודל שלך למה שהשוק באמת מתמחר, אלא לגרסה מנוטרלת-drift של המודל שלך עצמו.
- **עיוורון ל-skew:** השוק האמיתי מתמחר smile — פוטים OTM יקרים יותר מלוג-נורמל שטוח. מול לוג-נורמל שטוח, מכירת פוטים תיראה תמיד "עשירה" ותייצר edge פיקטיבי שיטתי לכיוון מכירת skew. זה בדיוק המלכוד הקלאסי: המערכת תמליץ בעקביות למכור את הביטוח שהשוק מתמחר ביוקר מסיבה.
- **market_iv=forecast_rv בכרטיס** — תנודתיות פיזית מוצגת כ-implied. שדה שקרי.

**תיקון:** חילוץ RND אמיתי מהשרשרת (חלק 3.B).

### P0-2: סטטיסטיקות מפוברקות בכרטיס הטרייד
ב-`engine.py` מקודדים קשיח: `similar_cases=38/42`, `forward_track_record_winrate=0.62/0.58`, `strategy_fit=0.90/0.85`, `quote_age=12.0`, `bid_ask_width=0.05`, `skew=0.02`, `term_structure=0.01`, `tail_loss=max_loss*1.1`, ו-confidence כפונקציית מדרגה `0.82/0.88`. ב-`gates.py`: `exec_score=15`, `fit_score=8`, `evidence_score=7` קבועים. זו התבנית שחזרה גם ב-vixtrader — נתונים מומצאים שנראים כמו מדידות. **המשמעות המצטברת:** מתוך 100 נק' Opportunity Score, ~42-43 ניתנות בחינם, כך שסף TRADE=60 נחצה עם edge/risk של ~11.5% בלבד — על edge שכבר ראינו שהוא ארטיפקט.

**תיקון:** כל שדה שאין לו מקור חישוב → `None`/"לא זמין", והורדת המשקל שלו מה-score (score מנורמל רק על רכיבים מדודים). את `similar_cases` ו-winrate לחשב באמת מ-shadow_log (שכבר קיים!).

### P0-3: אי-עקביות בספירת ימים (245/252/365)
- `volatility.py`: ברירת מחדל 252 ברוב הפונקציות, אבל 245 ב-Garman-Klass וב-reversal.
- `forecasting.py`: 245 בכל מקום.
- `backtest.py`: 252 בכל מקום (כולל reversal_5_vol_scaled — סתירה ישירה מול volatility.py!).
- `engine.py` + `generators.py` + `dual_edge.py`: **365** (`sqrt(14/365)`, `sqrt(7/365)`).

RV שנתי מחושב על בסיס ~245-252 ימי מסחר ואז מומר לנקודות עם √(d/365) — הטיה שיטתית של √(252/365)≈0.83, כלומר **expected move מוקטן ב-~17%**, מה שמכווץ סטרייקים של Iron Condor פנימה ומעלה סיכון פקיעה בתוך הכנפיים. בת"א יש ~245 ימי מסחר בשנה — לקבע `TRADING_DAYS_PER_YEAR=245` בקונפיג אחד ולתקן את כל האתרים. (אם רוצים דיוק: המרה כיוון-הפוכה עם calendar days דורשת גם dt קלנדרי בסיגמא — העיקר עקביות.)

### P1-4: forecast_rv_3d אינו באמת תחזית
חציון של 4 אומדנים **אחוריים** = מדידה חלקה של העבר, לא תחזית. אין בו mean-reversion, אין תגובת HAR לזעזוע, ואין שימוש ב-VTA35 שהוא החזאי החזק ביותר הזמין לך (IV מגלם ציפיות שוק). ה-HAR שכבר בניתם (כולל SHAR+HAR-Q ב-forecasting.py — יפה) יושב בצד. בנוסף:

- **הטיית Jensen ב-log-HAR:** שני מימושי ה-HAR חוזים log(RV) ומחזירים `exp(תחזית)` בלי תיקון ½σ̂². זה אומדן החציון, לא התוחלת → תת-אמידה שיטתית של RV, שמנפחת מלאכותית את matched_vrp_3d (VRP נראה חיובי מדי → הטיה קבועה לכיוון "IV יקר").
- **פרוקסי RV גרוע ב-backtest.py:** ה-HAR שם משתמש ב-|r|·√252 יומי — אומדן רועש מאוד. ב-forecasting.py משתמשים ב-r² — עדיף, אבל עדיין הכי רועש שיש כשיש לכם OHLC. אומדן יומי Garman-Klass/Yang-Zhang כקלט ל-HAR משפר דרמטית את יחס אות/רעש בלי נתונים תוך-יומיים.

### P1-5: הסטת ה-drift במודל אינה עקבית עם prob_up
`drift_bias=(p−0.5)·2·σ_t` — הקירוב הליניארי ל-Φ⁻¹. ההגדרה הנכונה: אם רוצים P(S_T>S_0)=p תחת לוג-נורמל, אז median-shift = σ_t·Φ⁻¹(p). ליד 0.5 הנגזרת של Φ⁻¹ היא √(2π)≈2.507, כלומר הקירוב 2.0 **מקטין את ההסתברות האפקטיבית** (p=0.60 הופך בפועל ל-≈0.579). בנוסף אין risk-free/דיבידנד בהתפלגות השוק (forward≠spot).

### P1-6: chain_indicators — BKM חלקי ו-fallbacks שקטים
- `bkm_kurt=0.0` קבוע — שדה מוצהר שלא מחושב.
- נוסחת ה-skew חסרה: BKM המלא דורש μ≡e^{rT}−1−e^{rT}V/2−… ומקדמי היוון; הגרסה הנוכחית `(W−3V^1.5)/V^1.5` אינה הנוסחה, והשמטת X (המומנט הרביעי) גם מהמונה.
- `atm_iv = call_iv or put_iv or 0.15` ו-`c_25d_iv = call_iv or atm_iv` — **fallbacks שקטים** (הדפוס שחזר אצלך שוב ושוב): כשחסר IV, ה-RR25 מתאפס בשקט במקום להיות None+flag.
- קירוב 25Δ עם 0.675σ הוא קוונטיל 25%, לא דלתא 25 (עם skew הם שונים). מספיק טוב כקירוב ראשון אבל צריך תיוג "approx".

### P1-7: רגליים בהיסטי-סיגמא קבועים במקום אופטימיזציה על השרשרת
±0.8σ/±1.5σ הם מספרי קסם. כשיש DDE, הסטרייקים צריכים להיבחר ע"י מקסום EV_model/CVaR על השרשרת בפועל (מחירי bid/ask אמיתיים), לא ע"י תבנית. גם עלויות קבועות (slippage=5 ש"ח, fee=3 ש"ח/רגל) — באופציות מעו"ף המרווחים ב-OTM יכולים להיות גדולים בהרבה; חצי-מרווח בפועל מהציטוט חייב להיכנס ל-EV.

### P2-8: שונות
- GJR grid-search ממקסם NLL על כל המדגם בכל קריאה — in-sample. כ-benchmark זה נסבל, אבל אסור שיזלוג לחזית.
- Stop=50% max-loss, Target=50% max-profit, time-exit=70%·DTE — סטטיים; ראו 3.F.
- `market_state` מזוהה ע"י חיפוש תת-מחרוזת בעברית — שביר. עדיף enum.
- הצד החיובי שראוי לציון: frozen_rules.json עם purge/embargo/Holm/nonoverlap, Wilson CI עם shrinkage prior, ה-lag של VIX, וה-shadow_log — כל אלה משקפים משמעת מתודולוגית טובה מהסבבים הקודמים. אל תשברו אותה בשם "שיפורים".

---

## חלק 3 — שיפורים מבוססי מחקר (אקדמי + פרקטי)

### A. תחזית התנודתיות: שדרוג ה-HAR למרכז הבמה

הקונצנזוס העדכני (2024-2026): HAR ונגזרותיו נשארים benchmark קשה מאוד להכות, ובאינפורמציה מוגבלת (כמו EOD בלבד) מודלים אקונומטריים עם החלפת משטר (THAR/STHAR) מנצחים גם ML (Kilic, Fed FEDS 2025-061). ML (עצים/רשתות) מנצח בעיקר באופקים ארוכים ועם predictors רבים (Christensen-Siggaard-Veliyev). לכן:

1. **החלפת ה-median כתחזית ראשית** ב-ensemble: HAR-log (עם תיקון Jensen: `exp(ŷ + ½σ̂²_resid)`) + SHAR (כבר יש) + HARQ (כבר יש quarticity) + רכיב IV: רגרסיה `log(RV_fwd) ~ HAR-terms + log(VTA35)`. VTA35 כרגרסור הוא כמעט בחינם ומוסיף את המידע הצופה-קדימה החסר.
2. **קלט HAR מ-OHLC:** daily RV = Garman-Klass או Rogers-Satchell יומי במקום r². שיפור אות/רעש מיידי, בלי דאטה חדשה.
3. **HAR עם החלפת משטר פשוטה (THAR):** שני סטים של מקדמים לפי סף על ה-regime הקיים שלכם (רגוע/לחץ) — בדיוק המבנה שהספרות מצאה כמנצח בסביבת מידע דלה.
4. **הערכה:** QLIKE (כבר ממומש!) + Diebold-Mariano מול ה-median הנוכחי, walk-forward על אותם offsets. אם ה-ensemble לא מנצח ב-QLIKE — לא מחליפים. 
5. **שילוב תחזיות:** trimmed-mean/median על *תחזיות* (HAR, GJR, EWMA, IV-implied) עדיף על median של *מדידות עבר* — זה ההבדל המהותי מהמצב היום.

### B. הפיכת ה-Dual-Edge לאמיתי: חילוץ RND מהשרשרת

זה השדרוג בעל התשואה הגבוהה ביותר במערכת. Pipeline מומלץ ל-DDE mode:

1. **Forward:** מ-put-call parity על 2-3 סטרייקים סביב ה-ATM (יש כבר synthetic_spot — להשתמש בו כ-F בכל מקום, כולל ב-dual_edge).
2. **סינון:** OTM בלבד (calls מעל F, puts מתחת — כפי שממליץ Figlewski), פסילת ציטוטים עם מרווח>סף או מחיר<מינימום טיק.
3. **החלקה במרחב ה-IV:** במעו"ף יש מעט סטרייקים — fit פרמטרי עדיף על spline. **SVI (Gatheral-Jacquier)** הוא הסטנדרט עם תנאי no-arbitrage ידועים; לחלופין פולינום ריבועי ב-log-moneyness (Shimko/Malz) שהוא יציב מאוד ב-5-9 נקודות. בדיקת butterfly-arbitrage: ∂²C/∂K²≥0.
4. **Breeden-Litzenberger** על עקומת המחירים המוחלקת → RND במרכז; **זנבות GPD** (Generalized Pareto) מעבר לטווח הסטרייקים — הפרקטיקה המקובלת לחילוץ RND עם כיסוי סטרייקים חלקי.
5. **Edge אמיתי:** EV_market = ∫payoff·RND, EV_model = ∫payoff·f_model. עכשיו ההשוואה כוללת את ה-skew שהשוק מתמחר, ומכירת פוטים תיראה "עשירה" רק אם היא באמת עשירה מול ה-RND.
6. תוצרי לוואי בחינם: MFIV אמין יותר (אינטגרציה על העקומה המוחלקת במקום על ציטוטים גולמיים), BKM skew/kurt מלאים, ו-market_pop אמיתי לכרטיס.

### C. שיפור הסתברות הכיוון

הצפי הריאלי: כיוון מדד באופק 3-14 יום הוא כמעט-בלתי-חזוי; רוב הערך יגיע מ-**כיול**, לא מפיצ'רים חדשים. ובכל זאת:

1. **כיול הסתברויות:** על תחזיות ה-OOS שכבר נאגרות — isotonic regression או Platt scaling, מוחל walk-forward. מדדי calibration כבר קיימים בדוח; לסגור את הלולאה ולתקן את ההסתברות לפני שהיא נכנסת למנוע. הסתברות מכוילת גרוע × מנוע EV = המלצות עקביות-שגויות.
2. **Shrinkage מפורש ל-0.5:** `p_used = 0.5 + λ(p_model − 0.5)` עם λ שנקבע לפי ה-Brier היחסי מול baseline. כשה-Brier של המודל לא מנצח את ה-baseline באופק נתון — λ=0 באותו אופק (המנוע הופך לנייטרלי-כיוון, וזה נכון).
3. **פיצ'רים מהשרשרת (כשיש DDE):** הספרות מוצאת כושר ניבוי ב-implied skew (Xing-Zhang-Zhao — שכבר מצוטט אצלך ב-docstring אבל לא ממומש כפיצ'ר), ב-skewness risk premium, וב-VRP באופקים חודשיים — עם עדויות מעורבות בין נכסים, אז דרך ה-frozen-rules discipline הקיימת: להוסיף כ-candidate rules ל-forward evaluation, לא להפעיל ישר. גם ה-OFI שכבר גילית ב-MAOF (`put_ofi_sum60`) שייך לכאן כמשפחה שביעית.
4. **פיצ'רים ישראל-ספציפיים:** dummy ליום ראשון (גישור פערי שישי-שבת מול ארה"ב — ה-gap_share שלך כבר רומז שזה מקור שונות מרכזי), מרווח CDS ישראל או TA-Bond spread אם נגיש, וספירלת USDILS+VIX משולבת (אינטראקציה, לא רק סכום דרגות).

### D. תיוג ו-meta-labeling

התיוג היום: sign(forward_return) באופק קבוע. השדרוג לפי López de Prado:

1. **Triple-barrier:** תיוג לפי מה שנפגע קודם — target/stop (מנורמלי-תנודתיות) או מחסום זמן — משקף איך פוזיציה אמיתית מסתיימת, וכבר יש לכם stop/target בכרטיס אז התיוג צריך להתיישר איתם.
2. **Meta-labeling:** מודל משני שלומד "האם לסמוך על ההמלצה של המנוע" מתוך ה-shadow_log — ה-infra כבר קיים! ה-shadow_log הוא בדיוק סט האימון ל-meta-model, וזה מקור אמיתי ל-similar_cases/winrate במקום המספרים הקשיחים.
3. **משקולות uniqueness** לתצפיות חופפות (משלים את גישת ה-nonoverlap הקיימת), ו-purged CV שכבר יש — לשמר.

### E. מבנה הטרייד: מרגליים-תבנית לאופטימיזציה

1. ב-DDE: לכל משפחה, לסרוק קומבינציות סטרייקים אמיתיות ולמקסם `EV_model_after_costs / CVaR_5%` (לא /max_loss — CVaR מבדיל בין מבנים עם אותו max_loss והסתברויות זנב שונות), עם עלויות = חצי-מרווח בפועל לכל רגל + עמלות.
2. ב-EOD: לפחות להצמיד את היסטי-הסיגמא ל-quantiles של ההתפלגות החזויה (כולל skew מ-downside_share) במקום 0.8/1.5 קבועים.
3. **Sizing:** להחליף `floor(budget/max_loss)` ב-fractional Kelly מוגבל: `f = c·edge/variance` עם c≈0.25 ותקרת אחוז תיק, כשה-edge הוא ה-edge המכויל (אחרי C). היום המערכת שמה את כל התקציב על הטרייד המדורג ראשון.
4. **יציאות:** target/stop מ-first-passage תחת התנודתיות החזויה (הסתברות פגיעה במחסום לפני הזמן) במקום 50%/50% — עקבי עם ה-triple-barrier מ-D.

### F. ולידציה — לשמר ולהדק

המסגרת הקיימת (frozen rules, purge=horizon, embargo=30, Holm, moving-block bootstrap, דיווח לפי offset) טובה. תוספות:

1. **CPCV** (Combinatorial Purged CV) לבחירת היפר-פרמטרים של ה-ensemble מ-A — נותן התפלגות ביצועים במקום מסלול יחיד.
2. **SPA/Model Confidence Set** כשמשווים >2 מודלי תחזית (Holm שמרני מדי להשוואת מודלים, מתאים לחוקים).
3. **דוח כיול רבעוני** מה-shadow_log: reliability diagram של prob_up מול תוצאות בפועל — זה ה-KPI האמיתי של המערכת, יותר מ-hit-rate.

---

## חלק 4 — מפת דרכים מומלצת

| שלב | פעולה | מאמץ | השפעה |
|---|---|---|---|
| 1 | קיבוע TRADING_DAYS=245 בכל הקוד + תיקון √(d/365)→√(d/245) | נמוך | גבוהה (מוטה כל סטרייק היום) |
| 2 | הסרת כל הסטטיסטיקות הקשיחות מהכרטיס + נרמול ה-score על רכיבים מדודים | נמוך | גבוהה (אמינות) |
| 3 | תיקון Jensen ב-HAR + קלט GK/RS יומי + drift=σ·Φ⁻¹(p) | נמוך | בינונית-גבוהה |
| 4 | RND מהשרשרת (Shimko-quadratic→SVI, BL, זנבות GPD) והחלפת הלוג-נורמל השטוח ב-dual_edge | בינוני | **הגבוהה ביותר** |
| 5 | ensemble תחזית RV (HAR-log+SHAR+HARQ+IV, THAR לפי regime) מוערך ב-QLIKE מול ה-median | בינוני | גבוהה |
| 6 | כיול isotonic + shrinkage-to-0.5 על prob_up | נמוך | גבוהה |
| 7 | Triple-barrier + meta-model על shadow_log; מילוי similar_cases/winrate אמיתיים | בינוני | בינונית-גבוהה |
| 8 | אופטימיזציית סטרייקים על השרשרת + Kelly חלקי + יציאות first-passage | גבוה | בינונית |
| 9 | פיצ'רים חדשים כ-candidate rules בלבד (RR25, SRP, OFI, Sunday-gap, CDS) דרך frozen-rules | מתמשך | תלוי-עדות |

---

## מקורות עיקריים

- Kilic (2025), *Linear and nonlinear econometric models against ML: realized volatility prediction*, Fed FEDS 2025-061 — regime-switching HAR (THAR/STHAR) מנצח ML ולינאריים כשהמידע מוגבל.
- Christensen, Siggaard, Veliyev, *A Machine Learning Approach to Volatility Forecasting* — ML מנצח HAR בעיקר באופקים ארוכים ועם predictors נוספים.
- Corsi (2009) HAR; Patton-Sheppard (2015) SHAR; Bollerslev-Patton-Quaedvlieg (2016) HARQ; Corsi-Renò (2012) leverage-HAR.
- Breeden-Litzenberger (1978); Shimko (1993); Malz (1997); Gatheral-Jacquier (2014) SVI; Figlewski — OTM-only + זנבות GPD ל-RND.
- Bakshi-Kapadia-Madan (2003) — מומנטים implied model-free; Xing-Zhang-Zhao (2010) — smirk חוזה תשואות.
- Bollerslev-Tauchen-Zhou (2009) VRP; BIS/AFA *Exploring the VRP Across Assets* — עדויות מעורבות בין נכסים.
- López de Prado (2018) *Advances in Financial ML* — triple-barrier, meta-labeling, uniqueness weights, CPCV.
- Yang-Zhang (2000); Garman-Klass (1980); Rogers-Satchell (1991) — אומדני OHLC.
