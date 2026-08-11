# מתודולוגיית החישוב והאגרגציה — TA-35 Volatility Dashboard

מסמך זה מתאר בצורה מפורטת ומדויקת את אופן החישוב, האגרגציה והשקילת האינדיקטורים במערכת **TA-35 Volatility Dashboard (Lite Edition)**.

---

## 1. ארכיטקטורת החישוב הכללית

המערכת מבוססת על תפיסת **מדגם EOD קטן (Small-Sample Transparency)** שנועדה למנוע התאמת יתר (Overfitting) ומציגה חלוקה ברורה בין:
1. **תחזית תנודתיות כמותית ממומשת (`forecast_rv_3d`)** — מבוססת חציון חסין.
2. **מודל הסתברויות משוקלל ב-2 שלבים (`probabilistic_family_model`)** — מבוסס רגרסיה לוגיסטית מיושרת ($L_2$ Ridge).
3. **פילטרי משטר סיכון (Regime & Stress Indicators)** — מזהים מצבי קיצון בשוק.
4. **אינדיקטורים בודדים לתצוגת דאשבורד ומחקר (UI & Research Signals)**.

---

## 2. תחזית תנודתיות ממומשת משולבת (`forecast_rv_3d`)

### אופן החישוב והאגרגציה
לתחזית התנודתיות 3 ימים קדימה, המערכת מפיקה 4 אומדני תנודתיות מבוססי מחיר סגירה וטווח מסחר:
* **`rv_5`**: תנודתיות ממומשת מנורמלת ל-5 ימי מסחר ($RV_5 = \sqrt{\sum r_t^2} \times \sqrt{252/5}$).
* **`rv_20`**: תנודתיות ממומשת מנורמלת ל-20 ימי מסחר.
* **`rv_ewma`**: ממוצע נע ממושקל אקספוננציאלית (Exponentially Weighted Moving Average).
* **`rv_yang_zhang_20`**: אומדן Yang-Zhang 20 יום המשקף גאפים בפתיחה וטווחי מסחר תוך-יומיים ($OHLC$).

האגרגציה מתבצעת באמצעות **חציון חסין (Unweighted Median)**:
$$\text{forecast\_rv\_3d} = \text{Median}\big(\text{rv\_5}, \text{rv\_20}, \text{rv\_ewma}, \text{rv\_yang\_zhang\_20}\big)$$

### טווח התנועה הצפוי בנקודות
$$\text{expected\_move\_3d\_points} = \text{Close} \times \text{forecast\_rv\_3d} \times \sqrt{\frac{3}{252}}$$

### משקולות וקביעותן
* **משקולות קבועות/חסינות (Median):** החציון מעניק משקל שווה לכל אומדן תוך סינון ערכי קיצון. המשקולות קבועות ואינן משתנות פרמטרית כדי למנוע הטיות מדגם.

---

## 3. מודל ההסתברויות המשוקלל (Purged L2 Shrunk Family Model)

המודל מיועד לחישוב ההסתברויות המותנות $P(\text{RV rises})$ ו-$P(\text{TA35 rises})$ לאופקי זמן של 3, 7, 14 ו-30 ימים.

### שלב א': הקבצה ל-5 משפחות מידע (Information Families)
13 אינדיקטורים מומרים לדרגות אחוזון מתרחבות (`Expanding Percentile Rank`) לאורך כל ההיסטוריה הידועה ($t \ge 60$). בתוך כל משפחה מבוצע **ממוצע שווה**:

1. **`rv_local` (תנודתיות מקומית):**
   $$\text{rv\_local} = \text{Mean}\big(\text{downside\_share\_20}, \text{rs\_range\_5\_20}, \text{rv\_20\_60\_ratio}\big)$$
2. **`iv_local` (תנודתיות גלויה):**
   $$\text{iv\_local} = \text{Mean}\big(\text{vta35\_zscore\_60}, \text{vta35\_change\_5d}, \text{vta\_vol\_of_vol\_20}\big)$$
3. **`global_fx` (לחץ גלובלי ומט"ח):**
   $$\text{global\_fx} = \text{Mean}\big(\text{local\_global\_stress\_spread}, \text{vix\_vix3m\_ratio}, \text{usdils\_change_5d}\big)$$
4. **`price_regime` (משטר מחירים ומגמה):**
   $$\text{price\_regime} = \text{Mean}\big(\text{trend\_efficiency\_20}, \text{range\_position\_20}, \text{reversal\_5\_vol\_scaled}\big)$$
5. **`forecast_gap` (פער תמחור תנודתיות):**
   $$\text{forecast\_gap} = \text{ExpandingRank}\big(\text{matched\_vrp\_3d}\big)$$

### שלב ב': רגרסיה לוגיסטית מיושרת ($L_2$ Ridge Logistic Regression)
1. **תקנון (Standardization):**
   $$X_{\text{train}} = \frac{X - \mu}{\sigma}$$
2. **מודל לוגיסטי עם ענישת $L_2$ (Ridge Penalty):**
   גראדיאנט העדכון עבור המשקולות $\beta$:
   $$\nabla = \frac{1}{N} D^T (p - y), \quad \nabla_{1:} \leftarrow \nabla_{1:} + \frac{0.25}{N} \beta_{1:}$$
   $$\beta \leftarrow \beta - 0.25 \times \nabla$$
3. **חישוב ההסתברות:**
   $$P(\text{Target}=1) = \frac{1}{1 + e^{- \text{clip}(D_{\text{current}} \cdot \beta, -20, 20)}}$$

### משקולות וקביעותן
* **משקולות דינמיות מתעדכנות (Expanding Window):** המשקולות $\beta$ אינן קבועות מראש. המודל מאמן מחדש את המשקולות בכל נקודת זמן $t$ אך ורק על גבי הנתונים שהבשילו במלואם (`Purged Targets`), למניעת Data Leakage.
* **מקדם ענישה קבוע:** מקדם הכיווץ $L_2$ מיוצב על $0.25$ כדי למנוע תנודות חריפות במשקולות בשל גודל המדגם.

---

## 4. מודלי ייחוס נוספים (Benchmarks)

* **GJR-GARCH Proxy (`gjr_eod_forecast`):**
  מודל פרמטרי בעל משקולות **קבועות מראש**:
  $$\omega = \text{Var} \times (1 - \alpha - \gamma/2 - \beta), \quad \alpha=0.06, \; \gamma=0.08, \; \beta=0.86$$
* **HAR-EOD Proxy (`har_eod_forecast`):**
  רגרסיה ליניארית (OLS) על $\log(\text{RV})$ ברמה יומית, שבועית (5 ימים) וחודשית (21 ימים). המקדמים **מתעדכנים דינמית** בחלון היסטורי מתרחב שהבדיקה לגביו הבשילה.

---

## 5. מיפוי קבצי הקוד במערכת

| רכיב | קובץ קוד במערכת |
|---|---|
| אומדני תנודתיות וחישוב חציון `forecast_rv_3d` | [`src/ta35_dashboard/services/backtest.py`](file:///Users/guy/Desktop/vix35/src/ta35_dashboard/services/backtest.py#L259-L266) |
| מודל הסתברויות 5 המשפחות ו-Ridge Logit | [`src/ta35_dashboard/services/research.py`](file:///Users/guy/Desktop/vix35/src/ta35_dashboard/services/research.py#L834-L941) |
| מודלי HAR-EOD ו-GJR-GARCH | [`src/ta35_dashboard/analytics/forecasting.py`](file:///Users/guy/Desktop/vix35/src/ta35_dashboard/analytics/forecasting.py) |
| חוקי חצים, כיוון ועוצמת אינדיקטורים בדאשבורד | [`src/ta35_dashboard/analytics/signals.py`](file:///Users/guy/Desktop/vix35/src/ta35_dashboard/analytics/signals.py) |
| כללי המחקר וההגדרות הקפואות | [`frozen_rules.json`](file:///Users/guy/Desktop/vix35/frozen_rules.json) |
