# TA-35 dashboard — comprehensive backtest research

Generated: 2026-08-10 05:23 UTC

TA-35 sample: 2023-08-08 to 2026-08-07 (738 sessions)

Horizons: 3, 7, 14, 30 trading days

## Executive interpretation

This document is a research knowledge base for recommendation calibration. It tests every dashboard indicator output and every strategy family at every requested horizon. A positive lift means that the rule beat the relevant historical base rate; it does not guarantee future performance.


- 3d indicator leader: vrp_spread / volatility (lift +11.8%, n=715, strength 8/10, FDR q=0.000).
- 3d strategy-scenario leader: פרפר Put דובי / Broken-Wing Butterfly (uplift +6.1%, n=56, strength 3/10, FDR q=0.979; exploratory unless it passes the knowledge-tier gates).
- 7d indicator leader: vrp_spread / volatility (lift +16.4%, n=711, strength 10/10, FDR q=0.000).
- 7d strategy-scenario leader: פרפר Put דובי / Broken-Wing Butterfly (uplift +9.0%, n=55, strength 3/10, FDR q=0.763; exploratory unless it passes the knowledge-tier gates).
- 14d indicator leader: vrp_spread / volatility (lift +15.1%, n=704, strength 10/10, FDR q=0.000).
- 14d strategy-scenario leader: Bear Put Spread (uplift +9.5%, n=72, strength 4/10, FDR q=0.635; exploratory unless it passes the knowledge-tier gates).
- 30d indicator leader: vrp_spread / volatility (lift +16.9%, n=688, strength 10/10, FDR q=0.000).
- 30d strategy-scenario leader: Bear Put Spread (uplift +13.7%, n=71, strength 6/10, FDR q=0.114; exploratory unless it passes the knowledge-tier gates).
- No strategy-selection rule passed the minimum sample plus 10% FDR gate; strategy rankings are exploratory and should not yet alter live recommendations automatically.


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


## Limitations

- All features are computed as-of date t; outcomes begin after that close.
- Overlapping horizons create serial dependence; non-overlapping robustness columns are reported.
- P-values are one-sided score approximations and FDR q-values control the many-test discovery rate.
- Strategy results are market-scenario proxies, not option P&L; premiums, skew, spreads and slippage are unavailable.
- Calendar/Diagonal is untestable without historical IV for at least two expiries.
- The 738-day TA-35 sample spans only about three years; regime and annual results can be fragile.
- forecast_rv_3d and expected_move_3d_points emit the same direction rule, so their similar results are duplicate evidence rather than independent confirmation.
- Cross-market EOD alignment assumes the recommendation is generated only after every same-date source has published; the database has dates, not intraday publication timestamps.
- The current rule thresholds were not frozen before this historical sample. Treat discoveries as in-sample research and require a future frozen holdout before automatic deployment.

## Recommendation knowledge tiers and deployment gates

| kind | name | axis | horizon | n | edge | fdr_q | year_stability | regime_stability | tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| indicator | vrp_spread | volatility | 3 | 715 | 0.1176 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | expected_move_3d_points | volatility | 3 | 715 | 0.0591 | 0.0014 | 4/4 | 3/4 | A — recommendation input |
| indicator | forecast_rv_3d | volatility | 3 | 715 | 0.0591 | 0.0014 | 4/4 | 3/4 | A — recommendation input |
| indicator | vrp_spread | volatility | 7 | 711 | 0.1635 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | expected_move_3d_points | volatility | 7 | 711 | 0.0842 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | forecast_rv_3d | volatility | 7 | 711 | 0.0842 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | vta35_change_5d | volatility | 7 | 711 | 0.0663 | 0.0011 | 4/4 | 4/4 | A — recommendation input |
| indicator | atr_5_20_ratio | volatility | 7 | 711 | 0.0437 | 0.0363 | 3/4 | 3/4 | A — recommendation input |
| indicator | vrp_spread | volatility | 14 | 704 | 0.1511 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | expected_move_3d_points | volatility | 14 | 704 | 0.1095 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | forecast_rv_3d | volatility | 14 | 704 | 0.1095 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | vta35_change_5d | volatility | 14 | 704 | 0.0716 | 0.0005 | 4/4 | 4/4 | A — recommendation input |
| indicator | atr_5_20_ratio | volatility | 14 | 704 | 0.0701 | 0.0005 | 4/4 | 3/4 | A — recommendation input |
| indicator | usdils_change_5d | volatility | 14 | 704 | 0.0613 | 0.0024 | 4/4 | 4/4 | A — recommendation input |
| indicator | vrp_spread | volatility | 30 | 688 | 0.1690 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | expected_move_3d_points | volatility | 30 | 688 | 0.0982 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | forecast_rv_3d | volatility | 30 | 688 | 0.0982 | 0.0000 | 4/4 | 4/4 | A — recommendation input |
| indicator | atr_5_20_ratio | volatility | 30 | 688 | 0.0803 | 0.0001 | 4/4 | 3/4 | A — recommendation input |
| indicator | usdils_change_5d | volatility | 30 | 688 | 0.0533 | 0.0104 | 3/4 | 3/4 | A — recommendation input |
| indicator | vta35_change_5d | volatility | 30 | 688 | 0.0469 | 0.0291 | 3/4 | 3/4 | A — recommendation input |
| indicator | usdils_change_5d | volatility | 7 | 711 | 0.0443 | 0.0345 | 4/4 | 2/4 | B — supporting input |
| indicator | vta35 | volatility | 3 | 676 | 0.0336 | 0.1317 | 3/4 | 3/4 | C — context only |
| indicator | vta35_zscore_60 | volatility | 3 | 676 | 0.0336 | 0.1317 | 3/4 | 3/4 | C — context only |
| indicator | usdils_change_5d | volatility | 3 | 715 | 0.0292 | 0.1650 | 3/4 | 2/4 | C — context only |
| indicator | vta35_change_5d | volatility | 3 | 715 | 0.0259 | 0.2301 | 1/4 | 2/4 | C — context only |
| indicator | atr_5_20_ratio | volatility | 3 | 715 | 0.0252 | 0.2356 | 3/4 | 2/4 | C — context only |
| indicator | rv_acceleration | volatility | 3 | 715 | 0.0176 | 0.4038 | 3/4 | 3/4 | C — context only |
| indicator | vix9d_vix_ratio | market | 3 | 630 | 0.0170 | 0.4280 | 4/4 | 3/4 | C — context only |
| indicator | vix_curve_ratio | volatility | 3 | 715 | 0.0075 | 0.6681 | 3/4 | 2/4 | C — context only |
| indicator | usdils_change_5d | market | 3 | 630 | 0.0063 | 0.7169 | 2/4 | 2/4 | C — context only |
| indicator | vix_vix3m_ratio | volatility | 3 | 715 | 0.0026 | 0.8283 | 2/4 | 2/4 | C — context only |
| indicator | vix9d_vix_ratio | volatility | 3 | 715 | 0.0002 | 0.8847 | 2/4 | 2/4 | C — context only |
| indicator | vix_curve_ratio | market | 3 | 710 | -0.0010 | 0.8923 | 2/4 | 1/4 | C — context only |
| indicator | vta35_change_5d | market | 3 | 680 | -0.0019 | 0.9019 | 1/4 | 1/4 | C — context only |
| indicator | gap_share_20 | volatility | 3 | 715 | -0.0079 | 0.9831 | 2/4 | 2/4 | C — context only |
| indicator | vix_vix3m_ratio | market | 3 | 690 | -0.0125 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | vta35 | market | 3 | 603 | -0.0215 | 1.0000 | 0/4 | 1/4 | C — context only |
| indicator | vta35_zscore_60 | market | 3 | 603 | -0.0215 | 1.0000 | 0/4 | 1/4 | C — context only |
| indicator | rv_20_60_ratio | volatility | 3 | 675 | -0.0527 | 1.0000 | 0/4 | 1/4 | C — context only |
| indicator | vta35 | volatility | 7 | 672 | 0.0365 | 0.1023 | 2/4 | 3/4 | C — context only |
| indicator | vta35_zscore_60 | volatility | 7 | 672 | 0.0365 | 0.1023 | 2/4 | 3/4 | C — context only |
| indicator | vix_curve_ratio | volatility | 7 | 711 | 0.0107 | 0.5995 | 3/4 | 2/4 | C — context only |
| indicator | vix9d_vix_ratio | market | 7 | 626 | 0.0098 | 0.6203 | 4/4 | 3/4 | C — context only |
| indicator | vix_vix3m_ratio | volatility | 7 | 711 | -0.0006 | 0.8923 | 2/4 | 2/4 | C — context only |
| indicator | vix9d_vix_ratio | volatility | 7 | 711 | -0.0066 | 0.9761 | 2/4 | 1/4 | C — context only |
| indicator | gap_share_20 | volatility | 7 | 711 | -0.0083 | 0.9831 | 3/4 | 1/4 | C — context only |
| indicator | vix_curve_ratio | market | 7 | 706 | -0.0173 | 1.0000 | 2/4 | 0/4 | C — context only |
| indicator | vix_vix3m_ratio | market | 7 | 686 | -0.0178 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | usdils_change_5d | market | 7 | 627 | -0.0180 | 1.0000 | 1/4 | 2/4 | C — context only |
| indicator | rv_acceleration | volatility | 7 | 711 | -0.0201 | 1.0000 | 1/4 | 1/4 | C — context only |
| indicator | vta35_change_5d | market | 7 | 677 | -0.0384 | 1.0000 | 1/4 | 1/4 | C — context only |
| indicator | vta35 | market | 7 | 601 | -0.0960 | 1.0000 | 1/4 | 0/4 | C — context only |
| indicator | vta35_zscore_60 | market | 7 | 601 | -0.0960 | 1.0000 | 1/4 | 0/4 | C — context only |
| indicator | rv_20_60_ratio | volatility | 7 | 671 | -0.1108 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | vta35 | volatility | 14 | 665 | 0.0330 | 0.1317 | 1/4 | 3/4 | C — context only |
| indicator | vta35_zscore_60 | volatility | 14 | 665 | 0.0330 | 0.1317 | 1/4 | 3/4 | C — context only |
| indicator | usdils_change_5d | market | 14 | 620 | 0.0319 | 0.1650 | 3/4 | 3/4 | C — context only |
| indicator | rv_acceleration | volatility | 14 | 704 | 0.0225 | 0.2910 | 3/4 | 2/4 | C — context only |
| indicator | vix9d_vix_ratio | volatility | 14 | 704 | 0.0195 | 0.3531 | 3/4 | 3/4 | C — context only |
| indicator | vix_curve_ratio | volatility | 14 | 704 | 0.0172 | 0.4074 | 2/4 | 3/4 | C — context only |
| indicator | vta35_change_5d | market | 14 | 670 | 0.0020 | 0.8367 | 2/4 | 1/4 | C — context only |
| indicator | vix_vix3m_ratio | volatility | 14 | 704 | -0.0031 | 0.9019 | 1/4 | 3/4 | C — context only |
| indicator | vix_vix3m_ratio | market | 14 | 679 | -0.0032 | 0.9019 | 1/4 | 2/4 | C — context only |
| indicator | vix_curve_ratio | market | 14 | 699 | -0.0083 | 0.9831 | 3/4 | 0/4 | C — context only |
| indicator | vix9d_vix_ratio | market | 14 | 620 | -0.0195 | 1.0000 | 2/4 | 1/4 | C — context only |
| indicator | vta35 | market | 14 | 595 | -0.0291 | 1.0000 | 0/4 | 1/4 | C — context only |
| indicator | vta35_zscore_60 | market | 14 | 595 | -0.0291 | 1.0000 | 0/4 | 1/4 | C — context only |
| indicator | gap_share_20 | volatility | 14 | 704 | -0.0563 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | rv_20_60_ratio | volatility | 14 | 664 | -0.1242 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | rv_acceleration | volatility | 30 | 688 | 0.0249 | 0.2452 | 3/4 | 3/4 | C — context only |
| indicator | vta35_change_5d | market | 30 | 657 | 0.0205 | 0.3531 | 2/4 | 2/4 | C — context only |
| indicator | vta35 | volatility | 30 | 649 | 0.0106 | 0.5995 | 1/4 | 3/4 | C — context only |
| indicator | vta35_zscore_60 | volatility | 30 | 649 | 0.0106 | 0.5995 | 1/4 | 3/4 | C — context only |
| indicator | vix_vix3m_ratio | volatility | 30 | 688 | -0.0025 | 0.9019 | 1/4 | 2/4 | C — context only |
| indicator | usdils_change_5d | market | 30 | 605 | -0.0051 | 0.9322 | 1/4 | 2/4 | C — context only |
| indicator | vix_vix3m_ratio | market | 30 | 663 | -0.0098 | 0.9831 | 0/4 | 0/4 | C — context only |
| indicator | vta35 | market | 30 | 582 | -0.0110 | 0.9831 | 2/4 | 2/4 | C — context only |
| indicator | vta35_zscore_60 | market | 30 | 582 | -0.0110 | 0.9831 | 2/4 | 2/4 | C — context only |
| indicator | vix_curve_ratio | volatility | 30 | 688 | -0.0153 | 1.0000 | 2/4 | 2/4 | C — context only |
| indicator | vix_curve_ratio | market | 30 | 683 | -0.0206 | 1.0000 | 1/4 | 0/4 | C — context only |
| indicator | vix9d_vix_ratio | market | 30 | 604 | -0.0315 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | vix9d_vix_ratio | volatility | 30 | 688 | -0.0316 | 1.0000 | 1/4 | 1/4 | C — context only |
| indicator | gap_share_20 | volatility | 30 | 688 | -0.1077 | 1.0000 | 0/4 | 0/4 | C — context only |
| indicator | rv_20_60_ratio | volatility | 30 | 648 | -0.1568 | 1.0000 | 0/4 | 0/4 | C — context only |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 3 | 56 | 0.0612 | 0.9785 | 3/4 | 3/3 | C — exploratory / unavailable |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 3 | 32 | 0.0583 | 0.9785 | 3/4 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 3 | 286 | -0.0053 | 0.9785 | 1/4 | 0/3 | C — exploratory / unavailable |
| strategy_proxy | Bull Call Spread | scenario | 3 | 195 | -0.0137 | 0.9785 | 1/4 | 1/4 | C — exploratory / unavailable |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 3 | 23 | -0.0418 | 0.9785 | 1/2 | 0/2 | C — exploratory / unavailable |
| strategy_proxy | Bear Put Spread | scenario | 3 | 75 | -0.0735 | 0.9785 | 1/4 | 1/4 | C — exploratory / unavailable |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 3 | 6 | -0.2137 | 0.9785 | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Long Straddle / Strangle | scenario | 3 | 5 | -0.3425 | 0.9785 | 0/1 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Call Spread | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bull Put Spread | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Calendar / Diagonal | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Butterfly | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Condor | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 7 | 55 | 0.0898 | 0.7625 | 3/4 | 3/3 | C — exploratory / unavailable |
| strategy_proxy | Bull Call Spread | scenario | 7 | 195 | 0.0137 | 0.9785 | 1/4 | 3/4 | C — exploratory / unavailable |
| strategy_proxy | Bear Put Spread | scenario | 7 | 74 | 0.0090 | 0.9785 | 2/4 | 2/4 | C — exploratory / unavailable |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 7 | 23 | -0.0040 | 0.9785 | 1/2 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 7 | 31 | -0.0102 | 0.9785 | 2/3 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 7 | 286 | -0.0433 | 0.9785 | 1/4 | 1/3 | C — exploratory / unavailable |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 7 | 6 | -0.2521 | 0.9785 | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Long Straddle / Strangle | scenario | 7 | 5 | -0.3430 | 0.9785 | 0/1 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Call Spread | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bull Put Spread | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Calendar / Diagonal | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Butterfly | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Condor | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Put Spread | scenario | 14 | 72 | 0.0954 | 0.6347 | 3/4 | 3/4 | C — exploratory / unavailable |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 14 | 283 | 0.0066 | 0.9785 | 2/4 | 1/3 | C — exploratory / unavailable |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 14 | 55 | -0.0056 | 0.9785 | 2/4 | 2/3 | C — exploratory / unavailable |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 14 | 23 | -0.0219 | 0.9785 | 0/2 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | Bull Call Spread | scenario | 14 | 194 | -0.0225 | 0.9785 | 1/4 | 2/4 | C — exploratory / unavailable |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 14 | 31 | -0.0616 | 0.9785 | 1/3 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | Long Straddle / Strangle | scenario | 14 | 5 | -0.1547 | 0.9785 | 0/1 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 14 | 6 | -0.2893 | 0.9785 | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Call Spread | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bull Put Spread | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Calendar / Diagonal | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Butterfly | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Condor | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Put Spread | scenario | 30 | 71 | 0.1370 | 0.1139 | 3/4 | 4/4 | C — exploratory / unavailable |
| strategy_proxy | Bull Call Spread | scenario | 30 | 194 | -0.0093 | 0.9785 | 1/4 | 3/4 | C — exploratory / unavailable |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 30 | 23 | -0.0234 | 0.9785 | 0/2 | 1/2 | C — exploratory / unavailable |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 30 | 282 | -0.0266 | 0.9785 | 1/4 | 1/3 | C — exploratory / unavailable |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 30 | 44 | -0.0628 | 0.9785 | 0/3 | 1/3 | C — exploratory / unavailable |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 30 | 28 | -0.1786 | 0.9785 | 0/3 | 0/2 | C — exploratory / unavailable |
| strategy_proxy | Long Straddle / Strangle | scenario | 30 | 5 | -0.2495 | 0.9785 | 0/1 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 30 | 6 | -0.3826 | 0.9785 | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bear Call Spread | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Bull Put Spread | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Calendar / Diagonal | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Butterfly | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | Iron Condor | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — exploratory / unavailable |

## Data coverage

| series | n | start | end |
| --- | --- | --- | --- |
| TA35 | 738 | 2023-08-08 | 2026-08-07 |
| VTA35 | 738 | 2023-08-08 | 2026-08-07 |
| USDILS | 13,253 | 1948-05-15 | 2026-08-07 |
| VIX9D | 3,921 | 2011-01-04 | 2026-08-07 |
| VIX | 9,246 | 1990-01-02 | 2026-08-07 |
| VIX3M | 4,247 | 2009-09-18 | 2026-08-07 |

## Forecast calibration and probability-band coverage

| source | horizon | n | mean_estimate | mean_forward_rv | bias | mae | rmse | rv_rank_ic | coverage_0.5sigma | coverage_1.0sigma | coverage_1.5sigma | coverage_2.0sigma |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| combined_RV_forecast | 3 | 730 | 0.1614 | 0.1451 | 0.0163 | 0.0703 | 0.0918 | 0.2001 | 34.8% | 65.8% | 83.0% | 93.2% |
| VTA35_proxy | 3 | 735 | 0.1761 | 0.1448 | 0.0313 | 0.0723 | 0.0924 | 0.2522 | 39.0% | 69.4% | 88.6% | 97.3% |
| combined_RV_forecast | 7 | 726 | 0.1612 | 0.1595 | 0.0017 | 0.0493 | 0.0684 | 0.2686 | 36.5% | 65.7% | 83.1% | 93.1% |
| VTA35_proxy | 7 | 731 | 0.1759 | 0.1591 | 0.0168 | 0.0479 | 0.0641 | 0.4043 | 41.2% | 68.0% | 88.8% | 97.1% |
| combined_RV_forecast | 14 | 719 | 0.1609 | 0.1640 | -0.0031 | 0.0429 | 0.0605 | 0.2850 | 35.2% | 64.5% | 82.9% | 91.7% |
| VTA35_proxy | 14 | 724 | 0.1755 | 0.1635 | 0.0121 | 0.0433 | 0.0555 | 0.3517 | 36.6% | 69.8% | 89.4% | 96.8% |
| combined_RV_forecast | 30 | 703 | 0.1602 | 0.1668 | -0.0066 | 0.0428 | 0.0581 | 0.1150 | 32.1% | 55.0% | 75.7% | 86.8% |
| VTA35_proxy | 30 | 708 | 0.1745 | 0.1663 | 0.0082 | 0.0389 | 0.0493 | 0.2037 | 34.7% | 57.6% | 79.2% | 92.1% |

## Indicator aggregate direction tests

| indicator | horizon | axis | n | accuracy | baseline | lift | adjusted_accuracy | ci_low | ci_high | p_value | strength | brier_walk_forward | brier_baseline | nonoverlap_n_min | nonoverlap_accuracy | rank_ic | top_bottom_quintile_spread | positive_years | tested_years | positive_regimes | tested_regimes | sample_quality | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | 715 | 45.3% | 42.8% | 2.5% | 45.2% | 41.7% | 49.0% | 0.0870 | 2 | 0.2501 | 24.5% | 238 | 45.3% | 0.1480 | 0.2394 | 3 | 4 | 2 | 4 | גבוהה | 0.2356 |
| atr_5_20_ratio | 7 | volatility | 711 | 46.0% | 41.6% | 4.4% | 45.9% | 42.4% | 49.7% | 0.0091 | 4 | 0.2544 | 24.3% | 101 | 46.0% | 0.1968 | 0.2495 | 3 | 4 | 3 | 4 | גבוהה | 0.0363 |
| atr_5_20_ratio | 14 | volatility | 704 | 48.6% | 41.6% | 7.0% | 48.4% | 44.9% | 52.3% | 0.0001 | 5 | 0.2549 | 24.3% | 50 | 48.6% | 0.2171 | 0.2177 | 4 | 4 | 3 | 4 | גבוהה | 0.0005 |
| atr_5_20_ratio | 30 | volatility | 688 | 49.7% | 41.7% | 8.0% | 49.5% | 46.0% | 53.4% | 0.0000 | 6 | 0.2570 | 24.3% | 22 | 49.7% | 0.1693 | 0.1479 | 4 | 4 | 3 | 4 | גבוהה | 0.0001 |
| expected_move_3d_points | 3 | volatility | 715 | 35.7% | 29.8% | 5.9% | 35.5% | 32.2% | 39.2% | 0.0003 | 4 | 0.2321 | 20.9% | 238 | 35.7% | 0.2277 | 0.4205 | 4 | 4 | 3 | 4 | גבוהה | 0.0014 |
| expected_move_3d_points | 7 | volatility | 711 | 38.3% | 29.8% | 8.4% | 38.0% | 34.8% | 41.9% | 0.0000 | 6 | 0.2418 | 20.9% | 101 | 38.2% | 0.2979 | 0.3415 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| expected_move_3d_points | 14 | volatility | 704 | 40.6% | 29.7% | 11.0% | 40.3% | 37.1% | 44.3% | 0.0000 | 7 | 0.2479 | 20.9% | 50 | 40.6% | 0.3468 | 0.3622 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| expected_move_3d_points | 30 | volatility | 688 | 39.4% | 29.6% | 9.8% | 39.1% | 35.8% | 43.1% | 0.0000 | 7 | 0.2442 | 20.8% | 22 | 39.4% | 0.3569 | 0.3719 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| forecast_rv_3d | 3 | volatility | 715 | 35.7% | 29.8% | 5.9% | 35.5% | 32.2% | 39.2% | 0.0003 | 4 | 0.2321 | 20.9% | 238 | 35.7% | 0.2375 | 0.4351 | 4 | 4 | 3 | 4 | גבוהה | 0.0014 |
| forecast_rv_3d | 7 | volatility | 711 | 38.3% | 29.8% | 8.4% | 38.0% | 34.8% | 41.9% | 0.0000 | 6 | 0.2418 | 20.9% | 101 | 38.2% | 0.3129 | 0.3656 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| forecast_rv_3d | 14 | volatility | 704 | 40.6% | 29.7% | 11.0% | 40.3% | 37.1% | 44.3% | 0.0000 | 7 | 0.2479 | 20.9% | 50 | 40.6% | 0.3705 | 0.4180 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| forecast_rv_3d | 30 | volatility | 688 | 39.4% | 29.6% | 9.8% | 39.1% | 35.8% | 43.1% | 0.0000 | 7 | 0.2442 | 20.8% | 22 | 39.4% | 0.3817 | 0.4201 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| gap_share_20 | 3 | volatility | 715 | 33.1% | 33.9% | -0.8% | 33.2% | 29.8% | 36.7% | 0.6726 | 1 | 0.2239 | 22.4% | 238 | 33.1% | -0.0781 | -0.2480 | 2 | 4 | 2 | 4 | גבוהה | 0.9831 |
| gap_share_20 | 7 | volatility | 711 | 32.8% | 33.6% | -0.8% | 32.8% | 29.4% | 36.3% | 0.6798 | 1 | 0.2251 | 22.3% | 101 | 32.8% | -0.1552 | -0.2415 | 3 | 4 | 1 | 4 | גבוהה | 0.9831 |
| gap_share_20 | 14 | volatility | 704 | 28.0% | 33.6% | -5.6% | 28.1% | 24.8% | 31.4% | 0.9992 | 1 | 0.2084 | 22.3% | 50 | 28.0% | -0.2291 | -0.2492 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | 688 | 23.4% | 34.2% | -10.8% | 23.7% | 20.4% | 26.7% | 1.0000 | 1 | 0.1875 | 22.5% | 22 | 23.4% | -0.3080 | -0.3139 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | 675 | 39.6% | 44.8% | -5.3% | 39.7% | 35.9% | 43.3% | 0.9971 | 1 | 0.2415 | 24.7% | 225 | 39.6% | -0.1707 | -0.2728 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | 671 | 31.6% | 42.7% | -11.1% | 31.9% | 28.2% | 35.2% | 1.0000 | 1 | 0.2209 | 24.5% | 95 | 31.6% | -0.3453 | -0.3968 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | 664 | 29.5% | 41.9% | -12.4% | 29.9% | 26.2% | 33.1% | 1.0000 | 1 | 0.2169 | 24.3% | 47 | 29.5% | -0.4063 | -0.3981 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | 648 | 26.1% | 41.8% | -15.7% | 26.5% | 22.8% | 29.6% | 1.0000 | 1 | 0.2176 | 24.3% | 21 | 26.0% | -0.4621 | -0.3744 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 3 | volatility | 715 | 48.0% | 46.2% | 1.8% | 47.9% | 44.3% | 51.6% | 0.1731 | 2 | 0.2515 | 24.9% | 238 | 48.0% | 0.0901 | 0.1451 | 3 | 4 | 3 | 4 | גבוהה | 0.4038 |
| rv_acceleration | 7 | volatility | 711 | 41.8% | 43.8% | -2.0% | 41.8% | 38.2% | 45.4% | 0.8604 | 1 | 0.2478 | 24.6% | 101 | 41.8% | 0.0552 | 0.1575 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 14 | volatility | 704 | 45.5% | 43.2% | 2.2% | 45.4% | 41.8% | 49.1% | 0.1143 | 2 | 0.2523 | 24.5% | 50 | 45.5% | 0.0833 | 0.1677 | 3 | 4 | 2 | 4 | גבוהה | 0.2910 |
| rv_acceleration | 30 | volatility | 688 | 45.5% | 43.0% | 2.5% | 45.4% | 41.8% | 49.2% | 0.0934 | 2 | 0.2524 | 24.5% | 22 | 45.5% | 0.0739 | 0.1608 | 3 | 4 | 3 | 4 | גבוהה | 0.2452 |
| usdils_change_5d | 3 | market | 630 | 51.0% | 50.3% | 0.6% | 50.9% | 47.1% | 54.8% | 0.3755 | 1 | 0.2521 | 25.0% | 206 | 50.9% | -0.0083 | 0.0002 | 2 | 4 | 2 | 4 | גבוהה | 0.7169 |
| usdils_change_5d | 3 | volatility | 715 | 45.6% | 42.7% | 2.9% | 45.5% | 42.0% | 49.3% | 0.0570 | 3 | 0.2501 | 24.5% | 238 | 45.6% | 0.0545 | 0.0802 | 3 | 4 | 2 | 4 | גבוהה | 0.1650 |
| usdils_change_5d | 7 | market | 627 | 48.6% | 50.4% | -1.8% | 48.7% | 44.8% | 52.6% | 0.8169 | 1 | 0.2544 | 25.0% | 85 | 48.7% | -0.0168 | -0.0024 | 1 | 4 | 2 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | 711 | 45.7% | 41.3% | 4.4% | 45.6% | 42.1% | 49.4% | 0.0082 | 4 | 0.2525 | 24.2% | 101 | 45.7% | 0.1506 | 0.1854 | 4 | 4 | 2 | 4 | גבוהה | 0.0345 |
| usdils_change_5d | 14 | market | 620 | 54.0% | 50.8% | 3.2% | 53.9% | 50.1% | 57.9% | 0.0561 | 3 | 0.2533 | 25.0% | 40 | 54.0% | 0.0358 | -0.0017 | 3 | 4 | 3 | 4 | גבוהה | 0.1650 |
| usdils_change_5d | 14 | volatility | 704 | 47.2% | 41.0% | 6.1% | 47.0% | 43.5% | 50.9% | 0.0005 | 5 | 0.2533 | 24.2% | 50 | 47.2% | 0.1300 | 0.1224 | 4 | 4 | 4 | 4 | גבוהה | 0.0024 |
| usdils_change_5d | 30 | market | 605 | 50.9% | 51.4% | -0.5% | 50.9% | 46.9% | 54.9% | 0.5993 | 1 | 0.2535 | 25.0% | 18 | 50.9% | -0.0113 | -0.0134 | 1 | 4 | 2 | 4 | גבוהה | 0.9322 |
| usdils_change_5d | 30 | volatility | 688 | 46.2% | 40.9% | 5.3% | 46.1% | 42.5% | 50.0% | 0.0022 | 4 | 0.2499 | 24.2% | 22 | 46.2% | 0.0960 | 0.0984 | 3 | 4 | 3 | 4 | גבוהה | 0.0104 |
| vix9d_vix_ratio | 3 | market | 630 | 59.7% | 58.0% | 1.7% | 59.6% | 55.8% | 63.4% | 0.1936 | 2 | 0.2430 | 24.4% | 207 | 59.7% | 0.0178 | 0.0016 | 4 | 4 | 3 | 4 | גבוהה | 0.4280 |
| vix9d_vix_ratio | 3 | volatility | 715 | 49.2% | 49.2% | 0.0% | 49.2% | 45.6% | 52.9% | 0.4950 | 1 | 0.2523 | 25.0% | 238 | 49.2% | -0.0033 | 0.0058 | 2 | 4 | 2 | 4 | גבוהה | 0.8847 |
| vix9d_vix_ratio | 7 | market | 626 | 59.4% | 58.4% | 1.0% | 59.4% | 55.5% | 63.2% | 0.3102 | 2 | 0.2460 | 24.3% | 82 | 59.5% | 0.0190 | 0.0040 | 4 | 4 | 3 | 4 | גבוהה | 0.6203 |
| vix9d_vix_ratio | 7 | volatility | 711 | 42.9% | 43.6% | -0.7% | 42.9% | 39.3% | 46.6% | 0.6391 | 1 | 0.2499 | 24.6% | 101 | 42.9% | 0.0109 | 0.0444 | 2 | 4 | 1 | 4 | גבוהה | 0.9761 |
| vix9d_vix_ratio | 14 | market | 620 | 61.3% | 63.2% | -1.9% | 61.4% | 57.4% | 65.0% | 0.8425 | 1 | 0.2457 | 23.2% | 41 | 61.3% | -0.0011 | 0.0053 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | 704 | 43.3% | 41.4% | 1.9% | 43.3% | 39.7% | 47.0% | 0.1471 | 2 | 0.2526 | 24.3% | 50 | 43.3% | 0.0727 | 0.0783 | 3 | 4 | 3 | 4 | גבוהה | 0.3531 |
| vix9d_vix_ratio | 30 | market | 604 | 63.7% | 66.9% | -3.1% | 63.8% | 59.8% | 67.5% | 0.9498 | 1 | 0.2492 | 22.1% | 15 | 63.6% | 0.0130 | 0.0089 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | 688 | 37.8% | 41.0% | -3.2% | 37.9% | 34.2% | 41.5% | 0.9543 | 1 | 0.2447 | 24.2% | 22 | 37.8% | -0.0191 | 0.0149 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 3 | market | 710 | 57.7% | 57.8% | -0.1% | 57.7% | 54.1% | 61.3% | 0.5205 | 1 | 0.2466 | 24.4% | 234 | 57.7% | -0.0346 | -0.0000 | 2 | 4 | 1 | 4 | גבוהה | 0.8923 |
| vix_curve_ratio | 3 | volatility | 715 | 57.5% | 56.7% | 0.8% | 57.5% | 53.8% | 61.1% | 0.3420 | 1 | 0.2467 | 24.5% | 238 | 57.5% | 0.0191 | -0.0246 | 3 | 4 | 2 | 4 | גבוהה | 0.6681 |
| vix_curve_ratio | 7 | market | 706 | 57.8% | 59.5% | -1.7% | 57.8% | 54.1% | 61.4% | 0.8259 | 1 | 0.2492 | 24.1% | 99 | 57.8% | -0.0369 | 0.0022 | 2 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 7 | volatility | 711 | 49.9% | 48.9% | 1.1% | 49.9% | 46.3% | 53.6% | 0.2844 | 2 | 0.2566 | 25.0% | 101 | 49.9% | 0.0348 | 0.0155 | 3 | 4 | 2 | 4 | גבוהה | 0.5995 |
| vix_curve_ratio | 14 | market | 699 | 64.5% | 65.3% | -0.8% | 64.5% | 60.9% | 68.0% | 0.6767 | 1 | 0.2389 | 22.6% | 48 | 64.5% | -0.0391 | -0.0019 | 3 | 4 | 0 | 4 | גבוהה | 0.9831 |
| vix_curve_ratio | 14 | volatility | 704 | 47.6% | 45.9% | 1.7% | 47.5% | 43.9% | 51.3% | 0.1795 | 2 | 0.2633 | 24.8% | 50 | 47.6% | 0.0523 | 0.0136 | 2 | 4 | 3 | 4 | גבוהה | 0.4074 |
| vix_curve_ratio | 30 | market | 683 | 68.5% | 70.6% | -2.1% | 68.6% | 64.9% | 71.9% | 0.8809 | 1 | 0.2395 | 20.8% | 20 | 68.6% | 0.0203 | 0.0040 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | volatility | 688 | 43.9% | 45.4% | -1.5% | 43.9% | 40.2% | 47.6% | 0.7901 | 1 | 0.2683 | 24.8% | 22 | 43.9% | 0.0303 | 0.0067 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | market | 690 | 57.5% | 58.8% | -1.3% | 57.6% | 53.8% | 61.2% | 0.7481 | 1 | 0.2471 | 24.2% | 228 | 57.5% | -0.0115 | -0.0013 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | 715 | 56.5% | 56.2% | 0.3% | 56.5% | 52.8% | 60.1% | 0.4437 | 1 | 0.2484 | 24.6% | 238 | 56.5% | 0.0289 | 0.0308 | 2 | 4 | 2 | 4 | גבוהה | 0.8283 |
| vix_vix3m_ratio | 7 | market | 686 | 57.7% | 59.5% | -1.8% | 57.8% | 54.0% | 61.4% | 0.8287 | 1 | 0.2498 | 24.1% | 97 | 57.7% | -0.0007 | -0.0034 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | 711 | 48.0% | 48.0% | -0.1% | 48.0% | 44.3% | 51.6% | 0.5132 | 1 | 0.2572 | 25.0% | 101 | 48.0% | 0.0117 | 0.0109 | 2 | 4 | 2 | 4 | גבוהה | 0.8923 |
| vix_vix3m_ratio | 14 | market | 679 | 65.8% | 66.1% | -0.3% | 65.8% | 62.2% | 69.3% | 0.5690 | 1 | 0.2363 | 22.4% | 46 | 65.8% | 0.0361 | -0.0007 | 1 | 4 | 2 | 4 | גבוהה | 0.9019 |
| vix_vix3m_ratio | 14 | volatility | 704 | 44.5% | 44.8% | -0.3% | 44.5% | 40.8% | 48.2% | 0.5667 | 1 | 0.2627 | 24.7% | 50 | 44.5% | 0.0164 | 0.0017 | 1 | 4 | 3 | 4 | גבוהה | 0.9019 |
| vix_vix3m_ratio | 30 | market | 663 | 71.0% | 72.0% | -1.0% | 71.1% | 67.5% | 74.4% | 0.7139 | 1 | 0.2327 | 20.1% | 19 | 71.0% | 0.1128 | 0.0165 | 0 | 4 | 0 | 4 | גבוהה | 0.9831 |
| vix_vix3m_ratio | 30 | volatility | 688 | 44.0% | 44.3% | -0.3% | 44.0% | 40.4% | 47.8% | 0.5532 | 1 | 0.2702 | 24.7% | 22 | 44.0% | 0.0093 | 0.0055 | 1 | 4 | 2 | 4 | גבוהה | 0.9019 |
| vrp_spread | 3 | volatility | 715 | 51.7% | 40.0% | 11.8% | 51.4% | 48.1% | 55.4% | 0.0000 | 8 | 0.2525 | 24.0% | 238 | 51.7% | 0.3014 | 0.4915 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| vrp_spread | 7 | volatility | 711 | 57.7% | 41.3% | 16.4% | 57.2% | 54.0% | 61.2% | 0.0000 | 10 | 0.2499 | 24.2% | 101 | 57.7% | 0.5023 | 0.5745 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| vrp_spread | 14 | volatility | 704 | 57.7% | 42.6% | 15.1% | 57.3% | 54.0% | 61.3% | 0.0000 | 10 | 0.2565 | 24.4% | 50 | 57.7% | 0.5292 | 0.5408 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| vrp_spread | 30 | volatility | 688 | 59.4% | 42.5% | 16.9% | 59.0% | 55.7% | 63.1% | 0.0000 | 10 | 0.2646 | 24.4% | 22 | 59.5% | 0.5839 | 0.5918 | 4 | 4 | 4 | 4 | גבוהה | 0.0000 |
| vta35 | 3 | market | 603 | 48.9% | 51.1% | -2.2% | 49.0% | 45.0% | 52.9% | 0.8546 | 1 | 0.2527 | 25.0% | 198 | 48.9% | -0.0817 | -0.0047 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35 | 3 | volatility | 676 | 48.1% | 44.7% | 3.4% | 48.0% | 44.3% | 51.8% | 0.0393 | 3 | 0.2522 | 24.7% | 225 | 48.1% | 0.0926 | 0.1304 | 3 | 4 | 3 | 4 | גבוהה | 0.1317 |
| vta35 | 7 | market | 601 | 41.8% | 51.4% | -9.6% | 42.1% | 37.9% | 45.7% | 1.0000 | 1 | 0.2498 | 25.0% | 83 | 41.8% | -0.1560 | -0.0110 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35 | 7 | volatility | 672 | 46.6% | 42.9% | 3.6% | 46.5% | 42.8% | 50.4% | 0.0280 | 3 | 0.2538 | 24.5% | 96 | 46.6% | 0.0693 | 0.0561 | 2 | 4 | 3 | 4 | גבוהה | 0.1023 |
| vta35 | 14 | market | 595 | 49.4% | 52.3% | -2.9% | 49.5% | 45.4% | 53.4% | 0.9221 | 1 | 0.2599 | 24.9% | 38 | 49.3% | -0.1287 | -0.0082 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35 | 14 | volatility | 665 | 45.7% | 42.4% | 3.3% | 45.6% | 42.0% | 49.5% | 0.0423 | 3 | 0.2530 | 24.4% | 47 | 45.7% | -0.0032 | -0.0297 | 1 | 4 | 3 | 4 | גבוהה | 0.1317 |
| vta35 | 30 | market | 582 | 52.6% | 53.7% | -1.1% | 52.6% | 48.5% | 56.6% | 0.7031 | 1 | 0.2567 | 24.9% | 17 | 52.8% | -0.0023 | 0.0086 | 2 | 4 | 2 | 4 | גבוהה | 0.9831 |
| vta35 | 30 | volatility | 649 | 43.5% | 42.4% | 1.1% | 43.4% | 39.7% | 47.3% | 0.2926 | 2 | 0.2576 | 24.4% | 21 | 43.3% | -0.0759 | -0.0947 | 1 | 4 | 3 | 4 | גבוהה | 0.5995 |
| vta35_change_5d | 3 | market | 680 | 50.3% | 50.5% | -0.2% | 50.3% | 46.5% | 54.0% | 0.5396 | 1 | 0.2523 | 25.0% | 226 | 50.3% | -0.0610 | -0.0051 | 1 | 4 | 1 | 4 | גבוהה | 0.9019 |
| vta35_change_5d | 3 | volatility | 715 | 48.4% | 45.8% | 2.6% | 48.3% | 44.7% | 52.1% | 0.0822 | 3 | 0.2518 | 24.8% | 238 | 48.4% | 0.0769 | 0.1511 | 1 | 4 | 2 | 4 | גבוהה | 0.2301 |
| vta35_change_5d | 7 | market | 677 | 46.8% | 50.7% | -3.8% | 46.9% | 43.1% | 50.6% | 0.9770 | 1 | 0.2516 | 25.0% | 94 | 46.8% | -0.0964 | -0.0139 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | 711 | 50.8% | 44.1% | 6.6% | 50.6% | 47.1% | 54.4% | 0.0002 | 5 | 0.2532 | 24.7% | 101 | 50.8% | 0.1879 | 0.2002 | 4 | 4 | 4 | 4 | גבוהה | 0.0011 |
| vta35_change_5d | 14 | market | 670 | 51.3% | 51.1% | 0.2% | 51.3% | 47.6% | 55.1% | 0.4582 | 1 | 0.2522 | 25.0% | 45 | 51.2% | -0.1029 | -0.0147 | 2 | 4 | 1 | 4 | גבוהה | 0.8367 |
| vta35_change_5d | 14 | volatility | 704 | 51.1% | 44.0% | 7.2% | 50.9% | 47.4% | 54.8% | 0.0001 | 5 | 0.2538 | 24.6% | 50 | 51.1% | 0.1630 | 0.1213 | 4 | 4 | 4 | 4 | גבוהה | 0.0005 |
| vta35_change_5d | 30 | market | 657 | 53.4% | 51.4% | 2.1% | 53.4% | 49.6% | 57.2% | 0.1465 | 2 | 0.2528 | 25.0% | 20 | 53.5% | -0.0459 | -0.0085 | 2 | 4 | 2 | 4 | גבוהה | 0.3531 |
| vta35_change_5d | 30 | volatility | 688 | 48.7% | 44.0% | 4.7% | 48.6% | 45.0% | 52.4% | 0.0066 | 4 | 0.2512 | 24.6% | 22 | 48.6% | 0.1421 | 0.1329 | 3 | 4 | 3 | 4 | גבוהה | 0.0291 |
| vta35_zscore_60 | 3 | market | 603 | 48.9% | 51.1% | -2.2% | 49.0% | 45.0% | 52.9% | 0.8546 | 1 | 0.2527 | 25.0% | 198 | 48.9% | -0.1110 | -0.0079 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | 676 | 48.1% | 44.7% | 3.4% | 48.0% | 44.3% | 51.8% | 0.0393 | 3 | 0.2522 | 24.7% | 225 | 48.1% | 0.1042 | 0.1733 | 3 | 4 | 3 | 4 | גבוהה | 0.1317 |
| vta35_zscore_60 | 7 | market | 601 | 41.8% | 51.4% | -9.6% | 42.1% | 37.9% | 45.7% | 1.0000 | 1 | 0.2498 | 25.0% | 83 | 41.8% | -0.1789 | -0.0161 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | 672 | 46.6% | 42.9% | 3.6% | 46.5% | 42.8% | 50.4% | 0.0280 | 3 | 0.2538 | 24.5% | 96 | 46.6% | 0.1244 | 0.1071 | 2 | 4 | 3 | 4 | גבוהה | 0.1023 |
| vta35_zscore_60 | 14 | market | 595 | 49.4% | 52.3% | -2.9% | 49.5% | 45.4% | 53.4% | 0.9221 | 1 | 0.2599 | 24.9% | 38 | 49.3% | -0.2000 | -0.0187 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | 665 | 45.7% | 42.4% | 3.3% | 45.6% | 42.0% | 49.5% | 0.0423 | 3 | 0.2530 | 24.4% | 47 | 45.7% | 0.0293 | -0.0056 | 1 | 4 | 3 | 4 | גבוהה | 0.1317 |
| vta35_zscore_60 | 30 | market | 582 | 52.6% | 53.7% | -1.1% | 52.6% | 48.5% | 56.6% | 0.7031 | 1 | 0.2567 | 24.9% | 17 | 52.8% | -0.0975 | -0.0105 | 2 | 4 | 2 | 4 | גבוהה | 0.9831 |
| vta35_zscore_60 | 30 | volatility | 649 | 43.5% | 42.4% | 1.1% | 43.4% | 39.7% | 47.3% | 0.2926 | 2 | 0.2576 | 24.4% | 21 | 43.3% | -0.0293 | -0.0582 | 1 | 4 | 3 | 4 | גבוהה | 0.5995 |

## Indicator results for every emitted arrow

| indicator | horizon | axis | arrow | n | hits | hit_rate | baseline | lift | adjusted_hit_rate | ci_low | ci_high | p_value | strength | nonoverlap_n_min | nonoverlap_hit_rate | sample_quality | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | ↑ | 304 | 118 | 38.8% | 35.8% | 3.0% | 38.6% | 33.5% | 44.4% | 0.1367 | 3 | 97 | 38.9% | גבוהה | 0.4455 |
| atr_5_20_ratio | 3 | volatility | ↓ | 319 | 203 | 63.6% | 60.8% | 2.8% | 63.5% | 58.2% | 68.7% | 0.1530 | 3 | 105 | 63.6% | גבוהה | 0.4695 |
| atr_5_20_ratio | 3 | volatility | ↔ | 92 | 3 | 3.3% | 3.4% | -0.1% | 3.3% | 1.1% | 9.2% | 0.5203 | 1 | 27 | 3.3% | בינונית | 0.9450 |
| atr_5_20_ratio | 7 | volatility | ↑ | 302 | 137 | 45.4% | 42.1% | 3.3% | 45.2% | 39.8% | 51.0% | 0.1219 | 3 | 41 | 45.2% | גבוהה | 0.4300 |
| atr_5_20_ratio | 7 | volatility | ↓ | 318 | 183 | 57.5% | 51.2% | 6.4% | 57.2% | 52.1% | 62.9% | 0.0117 | 5 | 41 | 57.6% | גבוהה | 0.0730 |
| atr_5_20_ratio | 7 | volatility | ↔ | 91 | 7 | 7.7% | 6.8% | 0.9% | 7.5% | 3.8% | 15.0% | 0.3602 | 1 | 9 | 7.2% | בינונית | 0.8150 |
| atr_5_20_ratio | 14 | volatility | ↑ | 298 | 159 | 53.4% | 45.9% | 7.5% | 52.9% | 47.7% | 58.9% | 0.0048 | 5 | 16 | 53.4% | גבוהה | 0.0336 |
| atr_5_20_ratio | 14 | volatility | ↓ | 316 | 177 | 56.0% | 47.4% | 8.6% | 55.5% | 50.5% | 61.4% | 0.0011 | 6 | 19 | 56.2% | גבוהה | 0.0098 |
| atr_5_20_ratio | 14 | volatility | ↔ | 90 | 6 | 6.7% | 6.7% | -0.0% | 6.7% | 3.1% | 13.8% | 0.5014 | 1 | 2 | 5.1% | בינונית | 0.9450 |
| atr_5_20_ratio | 30 | volatility | ↑ | 297 | 161 | 54.2% | 46.2% | 8.0% | 53.7% | 48.5% | 59.8% | 0.0029 | 5 | 4 | 55.5% | גבוהה | 0.0222 |
| atr_5_20_ratio | 30 | volatility | ↓ | 306 | 172 | 56.2% | 46.9% | 9.3% | 55.6% | 50.6% | 61.7% | 0.0006 | 6 | 6 | 56.4% | גבוהה | 0.0052 |
| atr_5_20_ratio | 30 | volatility | ↔ | 85 | 9 | 10.6% | 6.8% | 3.8% | 9.9% | 5.7% | 18.9% | 0.0849 | 3 | 1 | 11.6% | בינונית | 0.3494 |
| expected_move_3d_points | 3 | volatility | ↑ | 183 | 88 | 48.1% | 35.8% | 12.3% | 46.9% | 41.0% | 55.3% | 0.0003 | 8 | 58 | 48.2% | בינונית | 0.0027 |
| expected_move_3d_points | 3 | volatility | ↓ | 225 | 162 | 72.0% | 60.8% | 11.2% | 71.1% | 65.8% | 77.5% | 0.0003 | 7 | 72 | 71.9% | גבוהה | 0.0028 |
| expected_move_3d_points | 3 | volatility | ↔ | 307 | 5 | 1.6% | 3.4% | -1.7% | 1.7% | 0.7% | 3.8% | 0.9536 | 1 | 97 | 1.6% | גבוהה | 1.0000 |
| expected_move_3d_points | 7 | volatility | ↑ | 183 | 105 | 57.4% | 42.1% | 15.3% | 55.9% | 50.1% | 64.3% | 0.0000 | 9 | 22 | 57.6% | בינונית | 0.0002 |
| expected_move_3d_points | 7 | volatility | ↓ | 224 | 145 | 64.7% | 51.2% | 13.5% | 63.6% | 58.3% | 70.7% | 0.0000 | 8 | 27 | 64.9% | גבוהה | 0.0003 |
| expected_move_3d_points | 7 | volatility | ↔ | 304 | 22 | 7.2% | 6.8% | 0.5% | 7.2% | 4.8% | 10.7% | 0.3678 | 1 | 40 | 7.2% | גבוהה | 0.8158 |
| expected_move_3d_points | 14 | volatility | ↑ | 180 | 125 | 69.4% | 45.9% | 23.6% | 67.1% | 62.4% | 75.7% | 0.0000 | 10 | 10 | 70.8% | בינונית | 0.0000 |
| expected_move_3d_points | 14 | volatility | ↓ | 224 | 137 | 61.2% | 47.4% | 13.7% | 60.0% | 54.6% | 67.3% | 0.0000 | 9 | 12 | 61.4% | גבוהה | 0.0003 |
| expected_move_3d_points | 14 | volatility | ↔ | 300 | 24 | 8.0% | 6.7% | 1.3% | 7.9% | 5.4% | 11.6% | 0.1791 | 2 | 17 | 8.3% | גבוהה | 0.5145 |
| expected_move_3d_points | 30 | volatility | ↑ | 169 | 114 | 67.5% | 46.2% | 21.2% | 65.2% | 60.1% | 74.1% | 0.0000 | 10 | 3 | 64.9% | בינונית | 0.0000 |
| expected_move_3d_points | 30 | volatility | ↓ | 224 | 139 | 62.1% | 46.9% | 15.1% | 60.8% | 55.5% | 68.2% | 0.0000 | 9 | 4 | 61.4% | גבוהה | 0.0001 |
| expected_move_3d_points | 30 | volatility | ↔ | 295 | 18 | 6.1% | 6.8% | -0.7% | 6.1% | 3.9% | 9.4% | 0.6903 | 1 | 6 | 6.4% | גבוהה | 0.9912 |
| forecast_rv_3d | 3 | volatility | ↑ | 183 | 88 | 48.1% | 35.8% | 12.3% | 46.9% | 41.0% | 55.3% | 0.0003 | 8 | 58 | 48.2% | בינונית | 0.0027 |
| forecast_rv_3d | 3 | volatility | ↓ | 225 | 162 | 72.0% | 60.8% | 11.2% | 71.1% | 65.8% | 77.5% | 0.0003 | 7 | 72 | 71.9% | גבוהה | 0.0028 |
| forecast_rv_3d | 3 | volatility | ↔ | 307 | 5 | 1.6% | 3.4% | -1.7% | 1.7% | 0.7% | 3.8% | 0.9536 | 1 | 97 | 1.6% | גבוהה | 1.0000 |
| forecast_rv_3d | 7 | volatility | ↑ | 183 | 105 | 57.4% | 42.1% | 15.3% | 55.9% | 50.1% | 64.3% | 0.0000 | 9 | 22 | 57.6% | בינונית | 0.0002 |
| forecast_rv_3d | 7 | volatility | ↓ | 224 | 145 | 64.7% | 51.2% | 13.5% | 63.6% | 58.3% | 70.7% | 0.0000 | 8 | 27 | 64.9% | גבוהה | 0.0003 |
| forecast_rv_3d | 7 | volatility | ↔ | 304 | 22 | 7.2% | 6.8% | 0.5% | 7.2% | 4.8% | 10.7% | 0.3678 | 1 | 40 | 7.2% | גבוהה | 0.8158 |
| forecast_rv_3d | 14 | volatility | ↑ | 180 | 125 | 69.4% | 45.9% | 23.6% | 67.1% | 62.4% | 75.7% | 0.0000 | 10 | 10 | 70.8% | בינונית | 0.0000 |
| forecast_rv_3d | 14 | volatility | ↓ | 224 | 137 | 61.2% | 47.4% | 13.7% | 60.0% | 54.6% | 67.3% | 0.0000 | 9 | 12 | 61.4% | גבוהה | 0.0003 |
| forecast_rv_3d | 14 | volatility | ↔ | 300 | 24 | 8.0% | 6.7% | 1.3% | 7.9% | 5.4% | 11.6% | 0.1791 | 2 | 17 | 8.3% | גבוהה | 0.5145 |
| forecast_rv_3d | 30 | volatility | ↑ | 169 | 114 | 67.5% | 46.2% | 21.2% | 65.2% | 60.1% | 74.1% | 0.0000 | 10 | 3 | 64.9% | בינונית | 0.0000 |
| forecast_rv_3d | 30 | volatility | ↓ | 224 | 139 | 62.1% | 46.9% | 15.1% | 60.8% | 55.5% | 68.2% | 0.0000 | 9 | 4 | 61.4% | גבוהה | 0.0001 |
| forecast_rv_3d | 30 | volatility | ↔ | 295 | 18 | 6.1% | 6.8% | -0.7% | 6.1% | 3.9% | 9.4% | 0.6903 | 1 | 6 | 6.4% | גבוהה | 0.9912 |
| gap_share_20 | 3 | volatility | ↑ | 231 | 74 | 32.0% | 35.8% | -3.8% | 32.3% | 26.4% | 38.3% | 0.8840 | 1 | 76 | 32.1% | גבוהה | 1.0000 |
| gap_share_20 | 3 | volatility | ↓ | 250 | 154 | 61.6% | 60.8% | 0.8% | 61.5% | 55.4% | 67.4% | 0.4027 | 1 | 83 | 61.6% | גבוהה | 0.8474 |
| gap_share_20 | 3 | volatility | ↔ | 234 | 9 | 3.8% | 3.4% | 0.5% | 3.8% | 2.0% | 7.1% | 0.3388 | 1 | 76 | 3.8% | גבוהה | 0.7824 |
| gap_share_20 | 7 | volatility | ↑ | 231 | 85 | 36.8% | 42.1% | -5.3% | 37.2% | 30.8% | 43.2% | 0.9472 | 1 | 29 | 37.0% | גבוהה | 1.0000 |
| gap_share_20 | 7 | volatility | ↓ | 246 | 123 | 50.0% | 51.2% | -1.2% | 50.1% | 43.8% | 56.2% | 0.6462 | 1 | 32 | 49.8% | גבוהה | 0.9912 |
| gap_share_20 | 7 | volatility | ↔ | 234 | 25 | 10.7% | 6.8% | 3.9% | 10.4% | 7.3% | 15.3% | 0.0082 | 3 | 30 | 10.4% | גבוהה | 0.0528 |
| gap_share_20 | 14 | volatility | ↑ | 230 | 78 | 33.9% | 45.9% | -12.0% | 34.9% | 28.1% | 40.3% | 0.9999 | 1 | 13 | 34.0% | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | ↓ | 244 | 99 | 40.6% | 47.4% | -6.9% | 41.1% | 34.6% | 46.8% | 0.9842 | 1 | 15 | 40.1% | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | ↔ | 230 | 20 | 8.7% | 6.7% | 2.0% | 8.5% | 5.7% | 13.0% | 0.1099 | 2 | 14 | 8.5% | גבוהה | 0.4103 |
| gap_share_20 | 30 | volatility | ↑ | 229 | 67 | 29.3% | 46.2% | -17.0% | 30.6% | 23.7% | 35.5% | 1.0000 | 1 | 5 | 28.6% | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | ↓ | 244 | 85 | 34.8% | 46.9% | -12.1% | 35.8% | 29.1% | 41.0% | 0.9999 | 1 | 4 | 33.5% | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | ↔ | 215 | 9 | 4.2% | 6.8% | -2.6% | 4.4% | 2.2% | 7.8% | 0.9379 | 1 | 3 | 4.0% | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↑ | 252 | 76 | 30.2% | 35.4% | -5.2% | 30.5% | 24.8% | 36.1% | 0.9593 | 1 | 82 | 30.2% | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↓ | 345 | 191 | 55.4% | 61.0% | -5.7% | 55.7% | 50.1% | 60.5% | 0.9847 | 1 | 112 | 55.4% | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↔ | 78 | 0 | 0.0% | 3.6% | -3.6% | 0.7% | 0.0% | 4.7% | 0.9550 | 1 | 23 | 0.0% | נמוכה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↑ | 252 | 74 | 29.4% | 41.1% | -11.8% | 30.2% | 24.1% | 35.3% | 0.9999 | 1 | 34 | 29.3% | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↓ | 341 | 135 | 39.6% | 52.0% | -12.4% | 40.3% | 34.5% | 44.9% | 1.0000 | 1 | 44 | 39.5% | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↔ | 78 | 3 | 3.8% | 6.9% | -3.0% | 4.5% | 1.3% | 10.7% | 0.8535 | 1 | 9 | 3.4% | נמוכה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↑ | 252 | 81 | 32.1% | 45.6% | -13.5% | 33.1% | 26.7% | 38.1% | 1.0000 | 1 | 17 | 32.1% | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↓ | 334 | 112 | 33.5% | 47.3% | -13.8% | 34.3% | 28.7% | 38.8% | 1.0000 | 1 | 20 | 33.3% | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↔ | 78 | 3 | 3.8% | 7.1% | -3.2% | 4.5% | 1.3% | 10.7% | 0.8672 | 1 | 2 | 3.0% | נמוכה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↑ | 252 | 68 | 27.0% | 46.0% | -19.0% | 28.4% | 21.9% | 32.8% | 1.0000 | 1 | 5 | 28.0% | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↓ | 319 | 97 | 30.4% | 46.8% | -16.4% | 31.4% | 25.6% | 35.7% | 1.0000 | 1 | 8 | 30.3% | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↔ | 77 | 4 | 5.2% | 7.3% | -2.1% | 5.6% | 2.0% | 12.6% | 0.7569 | 1 | 1 | 4.6% | נמוכה | 1.0000 |
| rv_acceleration | 3 | volatility | ↑ | 273 | 104 | 38.1% | 35.8% | 2.3% | 37.9% | 32.5% | 44.0% | 0.2149 | 2 | 90 | 38.1% | גבוהה | 0.5799 |
| rv_acceleration | 3 | volatility | ↓ | 379 | 238 | 62.8% | 60.8% | 2.0% | 62.7% | 57.8% | 67.5% | 0.2175 | 2 | 121 | 62.9% | גבוהה | 0.5799 |
| rv_acceleration | 3 | volatility | ↔ | 63 | 1 | 1.6% | 3.4% | -1.8% | 2.0% | 0.3% | 8.5% | 0.7822 | 1 | 15 | 2.2% | נמוכה | 1.0000 |
| rv_acceleration | 7 | volatility | ↑ | 270 | 108 | 40.0% | 42.1% | -2.1% | 40.1% | 34.3% | 45.9% | 0.7529 | 1 | 30 | 39.9% | גבוהה | 1.0000 |
| rv_acceleration | 7 | volatility | ↓ | 378 | 184 | 48.7% | 51.2% | -2.5% | 48.8% | 43.7% | 53.7% | 0.8363 | 1 | 51 | 48.7% | גבוהה | 1.0000 |
| rv_acceleration | 7 | volatility | ↔ | 63 | 5 | 7.9% | 6.8% | 1.2% | 7.7% | 3.4% | 17.3% | 0.3538 | 1 | 5 | 7.3% | נמוכה | 0.8087 |
| rv_acceleration | 14 | volatility | ↑ | 265 | 131 | 49.4% | 45.9% | 3.6% | 49.2% | 43.5% | 55.4% | 0.1229 | 3 | 9 | 49.6% | גבוהה | 0.4300 |
| rv_acceleration | 14 | volatility | ↓ | 376 | 185 | 49.2% | 47.4% | 1.8% | 49.1% | 44.2% | 54.2% | 0.2473 | 2 | 19 | 49.6% | גבוהה | 0.6517 |
| rv_acceleration | 14 | volatility | ↔ | 63 | 4 | 6.3% | 6.7% | -0.3% | 6.4% | 2.5% | 15.2% | 0.5414 | 1 | 1 | 5.0% | נמוכה | 0.9474 |
| rv_acceleration | 30 | volatility | ↑ | 257 | 126 | 49.0% | 46.2% | 2.8% | 48.8% | 43.0% | 55.1% | 0.1834 | 3 | 4 | 48.5% | גבוהה | 0.5201 |
| rv_acceleration | 30 | volatility | ↓ | 368 | 184 | 50.0% | 46.9% | 3.1% | 49.8% | 44.9% | 55.1% | 0.1203 | 3 | 8 | 49.7% | גבוהה | 0.4300 |
| rv_acceleration | 30 | volatility | ↔ | 63 | 3 | 4.8% | 6.8% | -2.1% | 5.3% | 1.6% | 13.1% | 0.7425 | 1 | 1 | 4.2% | נמוכה | 1.0000 |
| usdils_change_5d | 3 | market | ↑ | 327 | 193 | 59.0% | 58.4% | 0.6% | 59.0% | 53.6% | 64.2% | 0.4116 | 1 | 100 | 58.8% | גבוהה | 0.8474 |
| usdils_change_5d | 3 | market | ↓ | 303 | 128 | 42.2% | 41.6% | 0.7% | 42.2% | 36.8% | 47.9% | 0.4083 | 1 | 95 | 42.4% | גבוהה | 0.8474 |
| usdils_change_5d | 3 | volatility | ↑ | 287 | 111 | 38.7% | 35.8% | 2.9% | 38.5% | 33.2% | 44.4% | 0.1551 | 3 | 90 | 38.9% | גבוהה | 0.4695 |
| usdils_change_5d | 3 | volatility | ↓ | 327 | 212 | 64.8% | 60.8% | 4.0% | 64.6% | 59.5% | 69.8% | 0.0695 | 3 | 100 | 64.7% | גבוהה | 0.3179 |
| usdils_change_5d | 3 | volatility | ↔ | 101 | 3 | 3.0% | 3.4% | -0.4% | 3.0% | 1.0% | 8.4% | 0.5853 | 1 | 30 | 3.1% | בינונית | 0.9712 |
| usdils_change_5d | 7 | market | ↑ | 326 | 194 | 59.5% | 61.2% | -1.7% | 59.6% | 54.1% | 64.7% | 0.7399 | 1 | 40 | 59.4% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | market | ↓ | 301 | 111 | 36.9% | 38.8% | -1.9% | 37.0% | 31.6% | 42.5% | 0.7483 | 1 | 38 | 36.7% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | ↑ | 285 | 136 | 47.7% | 42.1% | 5.7% | 47.3% | 42.0% | 53.5% | 0.0263 | 4 | 36 | 47.6% | גבוהה | 0.1512 |
| usdils_change_5d | 7 | volatility | ↓ | 326 | 185 | 56.7% | 51.2% | 5.6% | 56.4% | 51.3% | 62.0% | 0.0224 | 4 | 40 | 57.1% | גבוהה | 0.1323 |
| usdils_change_5d | 7 | volatility | ↔ | 100 | 4 | 4.0% | 6.8% | -2.8% | 4.5% | 1.6% | 9.8% | 0.8636 | 1 | 10 | 4.5% | בינונית | 1.0000 |
| usdils_change_5d | 14 | market | ↑ | 325 | 229 | 70.5% | 67.4% | 3.0% | 70.3% | 65.3% | 75.2% | 0.1210 | 3 | 17 | 70.5% | גבוהה | 0.4300 |
| usdils_change_5d | 14 | market | ↓ | 295 | 106 | 35.9% | 32.6% | 3.4% | 35.7% | 30.7% | 41.6% | 0.1097 | 3 | 15 | 36.5% | גבוהה | 0.4103 |
| usdils_change_5d | 14 | volatility | ↑ | 279 | 145 | 52.0% | 45.9% | 6.1% | 51.6% | 46.1% | 57.8% | 0.0206 | 4 | 14 | 52.4% | גבוהה | 0.1247 |
| usdils_change_5d | 14 | volatility | ↓ | 325 | 181 | 55.7% | 47.4% | 8.2% | 55.2% | 50.3% | 61.0% | 0.0014 | 6 | 17 | 55.3% | גבוהה | 0.0120 |
| usdils_change_5d | 14 | volatility | ↔ | 100 | 6 | 6.0% | 6.7% | -0.7% | 6.1% | 2.8% | 12.5% | 0.6068 | 1 | 4 | 5.7% | בינונית | 0.9849 |
| usdils_change_5d | 30 | market | ↑ | 320 | 237 | 74.1% | 74.5% | -0.5% | 74.1% | 69.0% | 78.6% | 0.5786 | 1 | 7 | 73.4% | גבוהה | 0.9712 |
| usdils_change_5d | 30 | market | ↓ | 285 | 71 | 24.9% | 25.5% | -0.5% | 24.9% | 20.2% | 30.2% | 0.5832 | 1 | 6 | 25.4% | גבוהה | 0.9712 |
| usdils_change_5d | 30 | volatility | ↑ | 269 | 138 | 51.3% | 46.2% | 5.1% | 50.9% | 45.4% | 57.2% | 0.0473 | 4 | 6 | 51.1% | גבוהה | 0.2428 |
| usdils_change_5d | 30 | volatility | ↓ | 320 | 172 | 53.8% | 46.9% | 6.8% | 53.3% | 48.3% | 59.1% | 0.0074 | 5 | 7 | 53.9% | גבוהה | 0.0486 |
| usdils_change_5d | 30 | volatility | ↔ | 99 | 8 | 8.1% | 6.8% | 1.2% | 7.9% | 4.2% | 15.1% | 0.3111 | 2 | 1 | 6.4% | בינונית | 0.7624 |
| vix9d_vix_ratio | 3 | market | ↑ | 532 | 333 | 62.6% | 61.6% | 1.0% | 62.6% | 58.4% | 66.6% | 0.3165 | 2 | 176 | 62.6% | גבוהה | 0.7624 |
| vix9d_vix_ratio | 3 | market | ↓ | 98 | 43 | 43.9% | 38.4% | 5.5% | 43.0% | 34.5% | 53.7% | 0.1330 | 4 | 30 | 44.4% | בינונית | 0.4447 |
| vix9d_vix_ratio | 3 | volatility | ↑ | 98 | 35 | 35.7% | 35.8% | -0.1% | 35.7% | 26.9% | 45.6% | 0.5074 | 1 | 30 | 35.5% | בינונית | 0.9450 |
| vix9d_vix_ratio | 3 | volatility | ↓ | 515 | 311 | 60.4% | 60.8% | -0.5% | 60.4% | 56.1% | 64.5% | 0.5830 | 1 | 170 | 60.4% | גבוהה | 0.9712 |
| vix9d_vix_ratio | 3 | volatility | ↔ | 102 | 6 | 5.9% | 3.4% | 2.5% | 5.5% | 2.7% | 12.2% | 0.0783 | 2 | 31 | 5.8% | בינונית | 0.3311 |
| vix9d_vix_ratio | 7 | market | ↑ | 528 | 332 | 62.9% | 62.3% | 0.6% | 62.9% | 58.7% | 66.9% | 0.3919 | 1 | 71 | 62.9% | גבוהה | 0.8474 |
| vix9d_vix_ratio | 7 | market | ↓ | 98 | 40 | 40.8% | 37.7% | 3.1% | 40.3% | 31.6% | 50.7% | 0.2622 | 3 | 10 | 41.0% | בינונית | 0.6829 |
| vix9d_vix_ratio | 7 | volatility | ↑ | 98 | 41 | 41.8% | 42.1% | -0.2% | 41.9% | 32.6% | 51.7% | 0.5173 | 1 | 10 | 42.5% | בינונית | 0.9450 |
| vix9d_vix_ratio | 7 | volatility | ↓ | 511 | 260 | 50.9% | 51.2% | -0.3% | 50.9% | 46.6% | 55.2% | 0.5566 | 1 | 69 | 50.8% | גבוהה | 0.9591 |
| vix9d_vix_ratio | 7 | volatility | ↔ | 102 | 4 | 3.9% | 6.8% | -2.8% | 4.4% | 1.5% | 9.7% | 0.8726 | 1 | 8 | 3.5% | בינונית | 1.0000 |
| vix9d_vix_ratio | 14 | market | ↑ | 522 | 356 | 68.2% | 69.4% | -1.2% | 68.2% | 64.1% | 72.0% | 0.7166 | 1 | 33 | 68.1% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | market | ↓ | 98 | 24 | 24.5% | 30.6% | -6.2% | 25.5% | 17.0% | 33.9% | 0.9069 | 1 | 3 | 23.9% | בינונית | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | ↑ | 98 | 52 | 53.1% | 45.9% | 7.2% | 51.8% | 43.3% | 62.6% | 0.0769 | 5 | 3 | 56.7% | בינונית | 0.3311 |
| vix9d_vix_ratio | 14 | volatility | ↓ | 505 | 245 | 48.5% | 47.4% | 1.1% | 48.5% | 44.2% | 52.9% | 0.3148 | 2 | 32 | 48.5% | גבוהה | 0.7624 |
| vix9d_vix_ratio | 14 | volatility | ↔ | 101 | 8 | 7.9% | 6.7% | 1.2% | 7.7% | 4.1% | 14.9% | 0.3081 | 2 | 4 | 6.6% | בינונית | 0.7624 |
| vix9d_vix_ratio | 30 | market | ↑ | 506 | 370 | 73.1% | 75.0% | -1.9% | 73.2% | 69.1% | 76.8% | 0.8353 | 1 | 11 | 72.9% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | market | ↓ | 98 | 15 | 15.3% | 25.0% | -9.7% | 16.9% | 9.5% | 23.7% | 0.9867 | 1 | 1 | 11.1% | בינונית | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↑ | 98 | 36 | 36.7% | 46.2% | -9.5% | 38.3% | 27.9% | 46.6% | 0.9702 | 1 | 1 | 32.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↓ | 489 | 219 | 44.8% | 46.9% | -2.2% | 44.9% | 40.4% | 49.2% | 0.8310 | 1 | 11 | 45.3% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↔ | 101 | 5 | 5.0% | 6.8% | -1.9% | 5.3% | 2.1% | 11.1% | 0.7732 | 1 | 1 | 3.9% | בינונית | 1.0000 |
| vix_curve_ratio | 3 | market | ↑ | 650 | 386 | 59.4% | 59.4% | -0.1% | 59.4% | 55.6% | 63.1% | 0.5108 | 1 | 215 | 59.4% | גבוהה | 0.9450 |
| vix_curve_ratio | 3 | market | ↓ | 60 | 24 | 40.0% | 40.6% | -0.6% | 40.1% | 28.6% | 52.6% | 0.5354 | 1 | 19 | 40.0% | נמוכה | 0.9450 |
| vix_curve_ratio | 3 | volatility | ↑ | 60 | 25 | 41.7% | 35.8% | 5.9% | 40.2% | 30.1% | 54.3% | 0.1718 | 3 | 19 | 41.7% | נמוכה | 0.5063 |
| vix_curve_ratio | 3 | volatility | ↓ | 630 | 386 | 61.3% | 60.8% | 0.4% | 61.3% | 57.4% | 65.0% | 0.4124 | 1 | 209 | 61.3% | גבוהה | 0.8474 |
| vix_curve_ratio | 3 | volatility | ↔ | 25 | 0 | 0.0% | 3.4% | -3.4% | 1.5% | 0.0% | 13.3% | 0.8243 | 1 | 7 | 0.0% | לא מספקת | 1.0000 |
| vix_curve_ratio | 7 | market | ↑ | 646 | 391 | 60.5% | 61.5% | -0.9% | 60.6% | 56.7% | 64.2% | 0.6895 | 1 | 88 | 60.5% | גבוהה | 0.9912 |
| vix_curve_ratio | 7 | market | ↓ | 60 | 17 | 28.3% | 38.5% | -10.2% | 30.9% | 18.5% | 40.8% | 0.9476 | 1 | 7 | 27.4% | נמוכה | 1.0000 |
| vix_curve_ratio | 7 | volatility | ↑ | 60 | 29 | 48.3% | 42.1% | 6.3% | 46.8% | 36.2% | 60.7% | 0.1622 | 3 | 7 | 47.9% | נמוכה | 0.4845 |
| vix_curve_ratio | 7 | volatility | ↓ | 626 | 326 | 52.1% | 51.2% | 0.9% | 52.0% | 48.2% | 56.0% | 0.3296 | 2 | 85 | 52.1% | גבוהה | 0.7784 |
| vix_curve_ratio | 7 | volatility | ↔ | 25 | 0 | 0.0% | 6.8% | -6.8% | 3.0% | 0.0% | 13.3% | 0.9107 | 1 | 2 | 0.0% | לא מספקת | 1.0000 |
| vix_curve_ratio | 14 | market | ↑ | 639 | 435 | 68.1% | 68.5% | -0.5% | 68.1% | 64.4% | 71.6% | 0.5970 | 1 | 43 | 68.0% | גבוהה | 0.9805 |
| vix_curve_ratio | 14 | market | ↓ | 60 | 16 | 26.7% | 31.5% | -4.8% | 27.9% | 17.1% | 39.0% | 0.7886 | 1 | 2 | 27.9% | נמוכה | 1.0000 |
| vix_curve_ratio | 14 | volatility | ↑ | 60 | 34 | 56.7% | 45.9% | 10.8% | 54.0% | 44.1% | 68.4% | 0.0468 | 4 | 2 | 59.8% | נמוכה | 0.2428 |
| vix_curve_ratio | 14 | volatility | ↓ | 619 | 300 | 48.5% | 47.4% | 1.0% | 48.4% | 44.5% | 52.4% | 0.3053 | 2 | 41 | 48.6% | גבוהה | 0.7624 |
| vix_curve_ratio | 14 | volatility | ↔ | 25 | 1 | 4.0% | 6.7% | -2.7% | 5.2% | 0.7% | 19.5% | 0.7040 | 1 | 1 | 7.7% | לא מספקת | 1.0000 |
| vix_curve_ratio | 30 | market | ↑ | 623 | 460 | 73.8% | 75.0% | -1.1% | 73.9% | 70.2% | 77.1% | 0.7420 | 1 | 18 | 73.8% | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | market | ↓ | 60 | 8 | 13.3% | 25.0% | -11.7% | 16.3% | 6.9% | 24.2% | 0.9818 | 1 | 1 | 8.3% | נמוכה | 1.0000 |
| vix_curve_ratio | 30 | volatility | ↑ | 60 | 20 | 33.3% | 46.2% | -12.9% | 36.6% | 22.7% | 45.9% | 0.9774 | 1 | 1 | 25.7% | נמוכה | 1.0000 |
| vix_curve_ratio | 30 | volatility | ↓ | 603 | 280 | 46.4% | 46.9% | -0.5% | 46.5% | 42.5% | 50.4% | 0.5997 | 1 | 17 | 46.6% | גבוהה | 0.9805 |
| vix_curve_ratio | 30 | volatility | ↔ | 25 | 2 | 8.0% | 6.8% | 1.2% | 7.5% | 2.2% | 25.0% | 0.4084 | 1 | 1 | 5.2% | לא מספקת | 0.8474 |
| vix_vix3m_ratio | 3 | market | ↑ | 662 | 390 | 58.9% | 59.6% | -0.7% | 58.9% | 55.1% | 62.6% | 0.6339 | 1 | 218 | 58.9% | גבוהה | 0.9912 |
| vix_vix3m_ratio | 3 | market | ↓ | 28 | 7 | 25.0% | 40.4% | -15.4% | 31.4% | 12.7% | 43.4% | 0.9520 | 1 | 8 | 24.8% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | ↑ | 28 | 10 | 35.7% | 35.8% | -0.1% | 35.8% | 20.7% | 54.2% | 0.5040 | 1 | 8 | 35.7% | לא מספקת | 0.9450 |
| vix_vix3m_ratio | 3 | volatility | ↓ | 642 | 393 | 61.2% | 60.8% | 0.4% | 61.2% | 57.4% | 64.9% | 0.4227 | 1 | 211 | 61.2% | גבוהה | 0.8586 |
| vix_vix3m_ratio | 3 | volatility | ↔ | 45 | 1 | 2.2% | 3.4% | -1.1% | 2.6% | 0.4% | 11.6% | 0.6637 | 1 | 12 | 2.0% | נמוכה | 0.9912 |
| vix_vix3m_ratio | 7 | market | ↑ | 658 | 391 | 59.4% | 60.3% | -0.9% | 59.4% | 55.6% | 63.1% | 0.6866 | 1 | 93 | 59.4% | גבוהה | 0.9912 |
| vix_vix3m_ratio | 7 | market | ↓ | 28 | 5 | 17.9% | 39.7% | -21.8% | 26.9% | 7.9% | 35.6% | 0.9908 | 1 | 3 | 19.5% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | ↑ | 28 | 9 | 32.1% | 42.1% | -9.9% | 36.3% | 17.9% | 50.7% | 0.8560 | 1 | 3 | 33.6% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | ↓ | 638 | 329 | 51.6% | 51.2% | 0.4% | 51.6% | 47.7% | 55.4% | 0.4255 | 1 | 90 | 51.5% | גבוהה | 0.8586 |
| vix_vix3m_ratio | 7 | volatility | ↔ | 45 | 3 | 6.7% | 6.8% | -0.1% | 6.7% | 2.3% | 17.9% | 0.5090 | 1 | 5 | 6.5% | נמוכה | 0.9450 |
| vix_vix3m_ratio | 14 | market | ↑ | 651 | 439 | 67.4% | 67.6% | -0.2% | 67.4% | 63.7% | 70.9% | 0.5358 | 1 | 45 | 67.4% | גבוהה | 0.9450 |
| vix_vix3m_ratio | 14 | market | ↓ | 28 | 8 | 28.6% | 32.4% | -3.8% | 30.2% | 15.3% | 47.1% | 0.6675 | 1 | 1 | 34.5% | לא מספקת | 0.9912 |
| vix_vix3m_ratio | 14 | volatility | ↑ | 28 | 12 | 42.9% | 45.9% | -3.0% | 44.1% | 26.5% | 60.9% | 0.6259 | 1 | 1 | 45.2% | לא מספקת | 0.9874 |
| vix_vix3m_ratio | 14 | volatility | ↓ | 631 | 301 | 47.7% | 47.4% | 0.3% | 47.7% | 43.8% | 51.6% | 0.4482 | 1 | 43 | 47.7% | גבוהה | 0.8964 |
| vix_vix3m_ratio | 14 | volatility | ↔ | 45 | 0 | 0.0% | 6.7% | -6.7% | 2.1% | 0.0% | 7.9% | 0.9636 | 1 | 1 | 0.0% | נמוכה | 1.0000 |
| vix_vix3m_ratio | 30 | market | ↑ | 635 | 467 | 73.5% | 74.1% | -0.5% | 73.6% | 70.0% | 76.8% | 0.6162 | 1 | 18 | 73.5% | גבוהה | 0.9874 |
| vix_vix3m_ratio | 30 | market | ↓ | 28 | 4 | 14.3% | 25.9% | -11.7% | 19.1% | 5.7% | 31.5% | 0.9203 | 1 | 1 | 10.3% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | ↑ | 28 | 10 | 35.7% | 46.2% | -10.5% | 40.1% | 20.7% | 54.2% | 0.8676 | 1 | 1 | 28.4% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | ↓ | 615 | 287 | 46.7% | 46.9% | -0.3% | 46.7% | 42.8% | 50.6% | 0.5555 | 1 | 18 | 46.6% | גבוהה | 0.9591 |
| vix_vix3m_ratio | 30 | volatility | ↔ | 45 | 6 | 13.3% | 6.8% | 6.5% | 11.3% | 6.3% | 26.2% | 0.0419 | 2 | 1 | 8.3% | נמוכה | 0.2291 |
| vrp_spread | 3 | volatility | ↑ | 437 | 197 | 45.1% | 35.8% | 9.3% | 44.7% | 40.5% | 49.8% | 0.0000 | 6 | 143 | 45.1% | גבוהה | 0.0003 |
| vrp_spread | 3 | volatility | ↓ | 209 | 171 | 81.8% | 60.8% | 21.0% | 80.0% | 76.0% | 86.5% | 0.0000 | 10 | 67 | 81.8% | גבוהה | 0.0000 |
| vrp_spread | 3 | volatility | ↔ | 69 | 2 | 2.9% | 3.4% | -0.5% | 3.0% | 0.8% | 10.0% | 0.5837 | 1 | 22 | 2.8% | נמוכה | 0.9712 |
| vrp_spread | 7 | volatility | ↑ | 433 | 240 | 55.4% | 42.1% | 13.4% | 54.8% | 50.7% | 60.0% | 0.0000 | 9 | 58 | 55.4% | גבוהה | 0.0000 |
| vrp_spread | 7 | volatility | ↓ | 209 | 166 | 79.4% | 51.2% | 28.2% | 77.0% | 73.4% | 84.4% | 0.0000 | 10 | 26 | 79.2% | גבוהה | 0.0000 |
| vrp_spread | 7 | volatility | ↔ | 69 | 4 | 5.8% | 6.8% | -1.0% | 6.0% | 2.3% | 14.0% | 0.6239 | 1 | 5 | 4.8% | נמוכה | 0.9874 |
| vrp_spread | 14 | volatility | ↑ | 428 | 255 | 59.6% | 45.9% | 13.7% | 59.0% | 54.9% | 64.1% | 0.0000 | 9 | 27 | 59.8% | גבוהה | 0.0000 |
| vrp_spread | 14 | volatility | ↓ | 208 | 148 | 71.2% | 47.4% | 23.7% | 69.1% | 64.7% | 76.9% | 0.0000 | 10 | 10 | 71.6% | גבוהה | 0.0000 |
| vrp_spread | 14 | volatility | ↔ | 68 | 3 | 4.4% | 6.7% | -2.3% | 4.9% | 1.5% | 12.2% | 0.7728 | 1 | 1 | 4.0% | נמוכה | 1.0000 |
| vrp_spread | 30 | volatility | ↑ | 412 | 251 | 60.9% | 46.2% | 14.7% | 60.2% | 56.1% | 65.5% | 0.0000 | 9 | 11 | 61.1% | גבוהה | 0.0000 |
| vrp_spread | 30 | volatility | ↓ | 208 | 154 | 74.0% | 46.9% | 27.1% | 71.7% | 67.7% | 79.5% | 0.0000 | 10 | 5 | 74.1% | גבוהה | 0.0000 |
| vrp_spread | 30 | volatility | ↔ | 68 | 4 | 5.9% | 6.8% | -0.9% | 6.1% | 2.3% | 14.2% | 0.6218 | 1 | 1 | 4.4% | נמוכה | 0.9874 |
| vta35 | 3 | market | ↑ | 336 | 193 | 57.4% | 59.4% | -1.9% | 57.5% | 52.1% | 62.6% | 0.7643 | 1 | 110 | 57.4% | גבוהה | 1.0000 |
| vta35 | 3 | market | ↓ | 267 | 102 | 38.2% | 40.6% | -2.4% | 38.4% | 32.6% | 44.2% | 0.7904 | 1 | 85 | 38.2% | גבוהה | 1.0000 |
| vta35 | 3 | volatility | ↑ | 267 | 105 | 39.3% | 35.4% | 4.0% | 39.0% | 33.7% | 45.3% | 0.0874 | 3 | 85 | 39.3% | גבוהה | 0.3494 |
| vta35 | 3 | volatility | ↓ | 336 | 217 | 64.6% | 61.1% | 3.5% | 64.4% | 59.3% | 69.5% | 0.0948 | 3 | 110 | 64.6% | גבוהה | 0.3662 |
| vta35 | 3 | volatility | ↔ | 73 | 3 | 4.1% | 3.6% | 0.6% | 4.0% | 1.4% | 11.4% | 0.3981 | 1 | 19 | 4.8% | נמוכה | 0.8474 |
| vta35 | 7 | market | ↑ | 334 | 179 | 53.6% | 62.2% | -8.6% | 54.1% | 48.2% | 58.9% | 0.9994 | 1 | 42 | 53.3% | גבוהה | 1.0000 |
| vta35 | 7 | market | ↓ | 267 | 72 | 27.0% | 37.8% | -10.8% | 27.7% | 22.0% | 32.6% | 0.9999 | 1 | 34 | 26.7% | גבוהה | 1.0000 |
| vta35 | 7 | volatility | ↑ | 267 | 122 | 45.7% | 41.1% | 4.6% | 45.4% | 39.8% | 51.7% | 0.0624 | 4 | 34 | 45.5% | גבוהה | 0.2912 |
| vta35 | 7 | volatility | ↓ | 334 | 188 | 56.3% | 52.1% | 4.2% | 56.0% | 50.9% | 61.5% | 0.0620 | 3 | 42 | 56.3% | גבוהה | 0.2912 |
| vta35 | 7 | volatility | ↔ | 71 | 3 | 4.2% | 6.8% | -2.6% | 4.8% | 1.4% | 11.7% | 0.8090 | 1 | 9 | 4.3% | נמוכה | 1.0000 |
| vta35 | 14 | market | ↑ | 331 | 225 | 68.0% | 70.6% | -2.6% | 68.1% | 62.8% | 72.8% | 0.8515 | 1 | 20 | 67.8% | גבוהה | 1.0000 |
| vta35 | 14 | market | ↓ | 264 | 69 | 26.1% | 29.4% | -3.3% | 26.4% | 21.2% | 31.8% | 0.8786 | 1 | 17 | 26.1% | גבוהה | 1.0000 |
| vta35 | 14 | volatility | ↑ | 264 | 129 | 48.9% | 45.6% | 3.3% | 48.6% | 42.9% | 54.9% | 0.1408 | 3 | 17 | 48.7% | גבוהה | 0.4455 |
| vta35 | 14 | volatility | ↓ | 331 | 170 | 51.4% | 47.4% | 4.0% | 51.1% | 46.0% | 56.7% | 0.0729 | 3 | 20 | 51.7% | גבוהה | 0.3204 |
| vta35 | 14 | volatility | ↔ | 70 | 5 | 7.1% | 7.1% | 0.1% | 7.1% | 3.1% | 15.7% | 0.4902 | 1 | 3 | 7.7% | נמוכה | 0.9450 |
| vta35 | 30 | market | ↑ | 329 | 254 | 77.2% | 78.2% | -1.0% | 77.3% | 72.4% | 81.4% | 0.6657 | 1 | 6 | 77.1% | גבוהה | 0.9912 |
| vta35 | 30 | market | ↓ | 253 | 52 | 20.6% | 21.8% | -1.3% | 20.6% | 16.0% | 26.0% | 0.6873 | 1 | 5 | 20.7% | גבוהה | 0.9912 |
| vta35 | 30 | volatility | ↑ | 253 | 120 | 47.4% | 45.9% | 1.5% | 47.3% | 41.4% | 53.6% | 0.3145 | 2 | 5 | 47.0% | גבוהה | 0.7624 |
| vta35 | 30 | volatility | ↓ | 329 | 158 | 48.0% | 46.8% | 1.2% | 48.0% | 42.7% | 53.4% | 0.3336 | 2 | 6 | 47.7% | גבוהה | 0.7784 |
| vta35 | 30 | volatility | ↔ | 67 | 4 | 6.0% | 7.2% | -1.3% | 6.3% | 2.3% | 14.4% | 0.6560 | 1 | 1 | 5.4% | נמוכה | 0.9912 |
| vta35_change_5d | 3 | market | ↑ | 359 | 210 | 58.5% | 58.7% | -0.2% | 58.5% | 53.3% | 63.5% | 0.5277 | 1 | 117 | 58.5% | גבוהה | 0.9450 |
| vta35_change_5d | 3 | market | ↓ | 321 | 132 | 41.1% | 41.3% | -0.2% | 41.1% | 35.9% | 46.6% | 0.5293 | 1 | 103 | 41.1% | גבוהה | 0.9450 |
| vta35_change_5d | 3 | volatility | ↑ | 317 | 123 | 38.8% | 35.8% | 3.0% | 38.6% | 33.6% | 44.3% | 0.1328 | 3 | 101 | 38.8% | גבוהה | 0.4447 |
| vta35_change_5d | 3 | volatility | ↓ | 349 | 220 | 63.0% | 60.8% | 2.2% | 62.9% | 57.9% | 67.9% | 0.2001 | 2 | 113 | 63.0% | גבוהה | 0.5466 |
| vta35_change_5d | 3 | volatility | ↔ | 49 | 3 | 6.1% | 3.4% | 2.8% | 5.3% | 2.1% | 16.5% | 0.1412 | 2 | 15 | 6.4% | נמוכה | 0.4455 |
| vta35_change_5d | 7 | market | ↑ | 358 | 207 | 57.8% | 61.4% | -3.6% | 58.0% | 52.6% | 62.8% | 0.9207 | 1 | 48 | 57.6% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | market | ↓ | 319 | 110 | 34.5% | 38.6% | -4.1% | 34.7% | 29.5% | 39.9% | 0.9323 | 1 | 41 | 34.4% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | ↑ | 315 | 157 | 49.8% | 42.1% | 7.8% | 49.4% | 44.4% | 55.3% | 0.0026 | 5 | 40 | 49.9% | גבוהה | 0.0204 |
| vta35_change_5d | 7 | volatility | ↓ | 348 | 202 | 58.0% | 51.2% | 6.9% | 57.7% | 52.8% | 63.1% | 0.0053 | 5 | 47 | 57.9% | גבוהה | 0.0359 |
| vta35_change_5d | 7 | volatility | ↔ | 48 | 2 | 4.2% | 6.8% | -2.6% | 4.9% | 1.2% | 14.0% | 0.7623 | 1 | 5 | 3.2% | נמוכה | 1.0000 |
| vta35_change_5d | 14 | market | ↑ | 355 | 246 | 69.3% | 69.1% | 0.2% | 69.3% | 64.3% | 73.9% | 0.4689 | 1 | 18 | 68.5% | גבוהה | 0.9214 |
| vta35_change_5d | 14 | market | ↓ | 315 | 98 | 31.1% | 30.9% | 0.2% | 31.1% | 26.3% | 36.4% | 0.4670 | 1 | 15 | 31.4% | גבוהה | 0.9214 |
| vta35_change_5d | 14 | volatility | ↑ | 311 | 166 | 53.4% | 45.9% | 7.5% | 52.9% | 47.8% | 58.8% | 0.0040 | 5 | 15 | 54.0% | גבוהה | 0.0288 |
| vta35_change_5d | 14 | volatility | ↓ | 345 | 189 | 54.8% | 47.4% | 7.3% | 54.4% | 49.5% | 60.0% | 0.0032 | 5 | 17 | 54.4% | גבוהה | 0.0236 |
| vta35_change_5d | 14 | volatility | ↔ | 48 | 5 | 10.4% | 6.7% | 3.7% | 9.3% | 4.5% | 22.2% | 0.1496 | 2 | 1 | 11.4% | נמוכה | 0.4654 |
| vta35_change_5d | 30 | market | ↑ | 346 | 269 | 77.7% | 75.8% | 1.9% | 77.6% | 73.1% | 81.8% | 0.1989 | 2 | 8 | 78.1% | גבוהה | 0.5466 |
| vta35_change_5d | 30 | market | ↓ | 311 | 82 | 26.4% | 24.2% | 2.2% | 26.2% | 21.8% | 31.5% | 0.1863 | 2 | 6 | 25.9% | גבוהה | 0.5216 |
| vta35_change_5d | 30 | volatility | ↑ | 307 | 157 | 51.1% | 46.2% | 4.9% | 50.8% | 45.6% | 56.7% | 0.0419 | 4 | 6 | 51.8% | גבוהה | 0.2291 |
| vta35_change_5d | 30 | volatility | ↓ | 336 | 173 | 51.5% | 46.9% | 4.5% | 51.2% | 46.2% | 56.8% | 0.0477 | 4 | 7 | 50.2% | גבוהה | 0.2428 |
| vta35_change_5d | 30 | volatility | ↔ | 45 | 5 | 11.1% | 6.8% | 4.3% | 9.8% | 4.8% | 23.5% | 0.1276 | 2 | 1 | 12.5% | נמוכה | 0.4396 |
| vta35_zscore_60 | 3 | market | ↑ | 336 | 193 | 57.4% | 59.4% | -1.9% | 57.5% | 52.1% | 62.6% | 0.7643 | 1 | 110 | 57.4% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | market | ↓ | 267 | 102 | 38.2% | 40.6% | -2.4% | 38.4% | 32.6% | 44.2% | 0.7904 | 1 | 85 | 38.2% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | ↑ | 267 | 105 | 39.3% | 35.4% | 4.0% | 39.0% | 33.7% | 45.3% | 0.0874 | 3 | 85 | 39.3% | גבוהה | 0.3494 |
| vta35_zscore_60 | 3 | volatility | ↓ | 336 | 217 | 64.6% | 61.1% | 3.5% | 64.4% | 59.3% | 69.5% | 0.0948 | 3 | 110 | 64.6% | גבוהה | 0.3662 |
| vta35_zscore_60 | 3 | volatility | ↔ | 73 | 3 | 4.1% | 3.6% | 0.6% | 4.0% | 1.4% | 11.4% | 0.3981 | 1 | 19 | 4.8% | נמוכה | 0.8474 |
| vta35_zscore_60 | 7 | market | ↑ | 334 | 179 | 53.6% | 62.2% | -8.6% | 54.1% | 48.2% | 58.9% | 0.9994 | 1 | 42 | 53.3% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | market | ↓ | 267 | 72 | 27.0% | 37.8% | -10.8% | 27.7% | 22.0% | 32.6% | 0.9999 | 1 | 34 | 26.7% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | ↑ | 267 | 122 | 45.7% | 41.1% | 4.6% | 45.4% | 39.8% | 51.7% | 0.0624 | 4 | 34 | 45.5% | גבוהה | 0.2912 |
| vta35_zscore_60 | 7 | volatility | ↓ | 334 | 188 | 56.3% | 52.1% | 4.2% | 56.0% | 50.9% | 61.5% | 0.0620 | 3 | 42 | 56.3% | גבוהה | 0.2912 |
| vta35_zscore_60 | 7 | volatility | ↔ | 71 | 3 | 4.2% | 6.8% | -2.6% | 4.8% | 1.4% | 11.7% | 0.8090 | 1 | 9 | 4.3% | נמוכה | 1.0000 |
| vta35_zscore_60 | 14 | market | ↑ | 331 | 225 | 68.0% | 70.6% | -2.6% | 68.1% | 62.8% | 72.8% | 0.8515 | 1 | 20 | 67.8% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | market | ↓ | 264 | 69 | 26.1% | 29.4% | -3.3% | 26.4% | 21.2% | 31.8% | 0.8786 | 1 | 17 | 26.1% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | ↑ | 264 | 129 | 48.9% | 45.6% | 3.3% | 48.6% | 42.9% | 54.9% | 0.1408 | 3 | 17 | 48.7% | גבוהה | 0.4455 |
| vta35_zscore_60 | 14 | volatility | ↓ | 331 | 170 | 51.4% | 47.4% | 4.0% | 51.1% | 46.0% | 56.7% | 0.0729 | 3 | 20 | 51.7% | גבוהה | 0.3204 |
| vta35_zscore_60 | 14 | volatility | ↔ | 70 | 5 | 7.1% | 7.1% | 0.1% | 7.1% | 3.1% | 15.7% | 0.4902 | 1 | 3 | 7.7% | נמוכה | 0.9450 |
| vta35_zscore_60 | 30 | market | ↑ | 329 | 254 | 77.2% | 78.2% | -1.0% | 77.3% | 72.4% | 81.4% | 0.6657 | 1 | 6 | 77.1% | גבוהה | 0.9912 |
| vta35_zscore_60 | 30 | market | ↓ | 253 | 52 | 20.6% | 21.8% | -1.3% | 20.6% | 16.0% | 26.0% | 0.6873 | 1 | 5 | 20.7% | גבוהה | 0.9912 |
| vta35_zscore_60 | 30 | volatility | ↑ | 253 | 120 | 47.4% | 45.9% | 1.5% | 47.3% | 41.4% | 53.6% | 0.3145 | 2 | 5 | 47.0% | גבוהה | 0.7624 |
| vta35_zscore_60 | 30 | volatility | ↓ | 329 | 158 | 48.0% | 46.8% | 1.2% | 48.0% | 42.7% | 53.4% | 0.3336 | 2 | 6 | 47.7% | גבוהה | 0.7784 |
| vta35_zscore_60 | 30 | volatility | ↔ | 67 | 4 | 6.0% | 7.2% | -1.3% | 6.3% | 2.3% | 14.4% | 0.6560 | 1 | 1 | 5.4% | נמוכה | 0.9912 |

## Indicator intensity / threshold sensitivity

| indicator | horizon | axis | filter | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | all | 715 | 45.3% | 42.8% | 2.5% |
| atr_5_20_ratio | 3 | volatility | top 50% intensity | 358 | 56.4% | 48.6% | 7.8% |
| atr_5_20_ratio | 3 | volatility | top 25% intensity | 179 | 61.5% | 49.4% | 12.1% |
| atr_5_20_ratio | 7 | volatility | all | 711 | 46.0% | 41.6% | 4.4% |
| atr_5_20_ratio | 7 | volatility | top 50% intensity | 357 | 53.8% | 46.5% | 7.3% |
| atr_5_20_ratio | 7 | volatility | top 25% intensity | 178 | 56.7% | 45.4% | 11.3% |
| atr_5_20_ratio | 14 | volatility | all | 704 | 48.6% | 41.6% | 7.0% |
| atr_5_20_ratio | 14 | volatility | top 50% intensity | 353 | 56.7% | 46.9% | 9.8% |
| atr_5_20_ratio | 14 | volatility | top 25% intensity | 177 | 58.8% | 46.3% | 12.5% |
| atr_5_20_ratio | 30 | volatility | all | 688 | 49.7% | 41.7% | 8.0% |
| atr_5_20_ratio | 30 | volatility | top 50% intensity | 345 | 58.8% | 46.9% | 11.9% |
| atr_5_20_ratio | 30 | volatility | top 25% intensity | 173 | 56.6% | 47.1% | 9.6% |
| expected_move_3d_points | 3 | volatility | all | 715 | 35.7% | 29.8% | 5.9% |
| expected_move_3d_points | 3 | volatility | top 50% intensity | 358 | 36.3% | 28.3% | 8.0% |
| expected_move_3d_points | 3 | volatility | top 25% intensity | 179 | 36.9% | 31.0% | 5.9% |
| expected_move_3d_points | 7 | volatility | all | 711 | 38.3% | 29.8% | 8.4% |
| expected_move_3d_points | 7 | volatility | top 50% intensity | 357 | 39.2% | 29.0% | 10.2% |
| expected_move_3d_points | 7 | volatility | top 25% intensity | 178 | 39.3% | 30.3% | 9.0% |
| expected_move_3d_points | 14 | volatility | all | 704 | 40.6% | 29.7% | 11.0% |
| expected_move_3d_points | 14 | volatility | top 50% intensity | 353 | 41.4% | 28.7% | 12.7% |
| expected_move_3d_points | 14 | volatility | top 25% intensity | 177 | 38.4% | 29.5% | 8.9% |
| expected_move_3d_points | 30 | volatility | all | 688 | 39.4% | 29.6% | 9.8% |
| expected_move_3d_points | 30 | volatility | top 50% intensity | 345 | 43.2% | 28.6% | 14.6% |
| expected_move_3d_points | 30 | volatility | top 25% intensity | 173 | 42.2% | 28.9% | 13.3% |
| forecast_rv_3d | 3 | volatility | all | 715 | 35.7% | 29.8% | 5.9% |
| forecast_rv_3d | 3 | volatility | top 50% intensity | 358 | 39.1% | 31.1% | 8.0% |
| forecast_rv_3d | 3 | volatility | top 25% intensity | 179 | 43.0% | 30.8% | 12.3% |
| forecast_rv_3d | 7 | volatility | all | 711 | 38.3% | 29.8% | 8.4% |
| forecast_rv_3d | 7 | volatility | top 50% intensity | 357 | 42.3% | 30.2% | 12.1% |
| forecast_rv_3d | 7 | volatility | top 25% intensity | 178 | 44.4% | 30.3% | 14.1% |
| forecast_rv_3d | 14 | volatility | all | 704 | 40.6% | 29.7% | 11.0% |
| forecast_rv_3d | 14 | volatility | top 50% intensity | 353 | 42.2% | 29.4% | 12.8% |
| forecast_rv_3d | 14 | volatility | top 25% intensity | 177 | 46.3% | 29.0% | 17.3% |
| forecast_rv_3d | 30 | volatility | all | 688 | 39.4% | 29.6% | 9.8% |
| forecast_rv_3d | 30 | volatility | top 50% intensity | 345 | 45.2% | 29.8% | 15.4% |
| forecast_rv_3d | 30 | volatility | top 25% intensity | 173 | 47.4% | 28.2% | 19.2% |
| gap_share_20 | 3 | volatility | all | 715 | 33.1% | 33.9% | -0.8% |
| gap_share_20 | 3 | volatility | top 50% intensity | 358 | 43.6% | 48.2% | -4.6% |
| gap_share_20 | 3 | volatility | top 25% intensity | 179 | 40.8% | 47.4% | -6.6% |
| gap_share_20 | 7 | volatility | all | 711 | 32.8% | 33.6% | -0.8% |
| gap_share_20 | 7 | volatility | top 50% intensity | 357 | 41.5% | 47.3% | -5.9% |
| gap_share_20 | 7 | volatility | top 25% intensity | 178 | 38.8% | 48.5% | -9.8% |
| gap_share_20 | 14 | volatility | all | 704 | 28.0% | 33.6% | -5.6% |
| gap_share_20 | 14 | volatility | top 50% intensity | 353 | 34.6% | 47.6% | -13.0% |
| gap_share_20 | 14 | volatility | top 25% intensity | 177 | 33.9% | 48.3% | -14.4% |
| gap_share_20 | 30 | volatility | all | 688 | 23.4% | 34.2% | -10.8% |
| gap_share_20 | 30 | volatility | top 50% intensity | 345 | 31.3% | 46.5% | -15.2% |
| gap_share_20 | 30 | volatility | top 25% intensity | 173 | 31.8% | 44.5% | -12.7% |
| rv_20_60_ratio | 3 | volatility | all | 675 | 39.6% | 44.8% | -5.3% |
| rv_20_60_ratio | 3 | volatility | top 50% intensity | 339 | 35.1% | 47.9% | -12.8% |
| rv_20_60_ratio | 3 | volatility | top 25% intensity | 169 | 30.8% | 47.9% | -17.1% |
| rv_20_60_ratio | 7 | volatility | all | 671 | 31.6% | 42.7% | -11.1% |
| rv_20_60_ratio | 7 | volatility | top 50% intensity | 336 | 26.2% | 47.6% | -21.4% |
| rv_20_60_ratio | 7 | volatility | top 25% intensity | 169 | 21.3% | 47.6% | -26.3% |
| rv_20_60_ratio | 14 | volatility | all | 664 | 29.5% | 41.9% | -12.4% |
| rv_20_60_ratio | 14 | volatility | top 50% intensity | 333 | 26.1% | 47.3% | -21.2% |
| rv_20_60_ratio | 14 | volatility | top 25% intensity | 167 | 20.4% | 47.0% | -26.6% |
| rv_20_60_ratio | 30 | volatility | all | 648 | 26.1% | 41.8% | -15.7% |
| rv_20_60_ratio | 30 | volatility | top 50% intensity | 325 | 24.9% | 47.1% | -22.1% |
| rv_20_60_ratio | 30 | volatility | top 25% intensity | 163 | 19.6% | 47.2% | -27.5% |
| rv_acceleration | 3 | volatility | all | 715 | 48.0% | 46.2% | 1.8% |
| rv_acceleration | 3 | volatility | top 50% intensity | 358 | 50.3% | 47.6% | 2.7% |
| rv_acceleration | 3 | volatility | top 25% intensity | 179 | 53.6% | 48.0% | 5.7% |
| rv_acceleration | 7 | volatility | all | 711 | 41.8% | 43.8% | -2.0% |
| rv_acceleration | 7 | volatility | top 50% intensity | 357 | 45.9% | 45.9% | 0.0% |
| rv_acceleration | 7 | volatility | top 25% intensity | 178 | 47.8% | 45.5% | 2.3% |
| rv_acceleration | 14 | volatility | all | 704 | 45.5% | 43.2% | 2.2% |
| rv_acceleration | 14 | volatility | top 50% intensity | 353 | 52.4% | 46.9% | 5.5% |
| rv_acceleration | 14 | volatility | top 25% intensity | 177 | 52.0% | 46.9% | 5.1% |
| rv_acceleration | 30 | volatility | all | 688 | 45.5% | 43.0% | 2.5% |
| rv_acceleration | 30 | volatility | top 50% intensity | 345 | 55.1% | 46.2% | 8.8% |
| rv_acceleration | 30 | volatility | top 25% intensity | 173 | 53.2% | 45.4% | 7.8% |
| usdils_change_5d | 3 | market | all | 630 | 51.0% | 50.3% | 0.6% |
| usdils_change_5d | 3 | market | top 50% intensity | 315 | 51.4% | 50.0% | 1.4% |
| usdils_change_5d | 3 | market | top 25% intensity | 158 | 56.3% | 50.0% | 6.3% |
| usdils_change_5d | 3 | volatility | all | 715 | 45.6% | 42.7% | 2.9% |
| usdils_change_5d | 3 | volatility | top 50% intensity | 358 | 51.4% | 48.0% | 3.4% |
| usdils_change_5d | 3 | volatility | top 25% intensity | 179 | 50.3% | 47.7% | 2.6% |
| usdils_change_5d | 7 | market | all | 627 | 48.6% | 50.4% | -1.8% |
| usdils_change_5d | 7 | market | top 50% intensity | 315 | 46.0% | 50.0% | -3.9% |
| usdils_change_5d | 7 | market | top 25% intensity | 158 | 48.1% | 49.9% | -1.8% |
| usdils_change_5d | 7 | volatility | all | 711 | 45.7% | 41.3% | 4.4% |
| usdils_change_5d | 7 | volatility | top 50% intensity | 357 | 53.2% | 46.3% | 6.9% |
| usdils_change_5d | 7 | volatility | top 25% intensity | 178 | 56.2% | 46.9% | 9.3% |
| usdils_change_5d | 14 | market | all | 620 | 54.0% | 50.8% | 3.2% |
| usdils_change_5d | 14 | market | top 50% intensity | 311 | 54.0% | 49.9% | 4.1% |
| usdils_change_5d | 14 | market | top 25% intensity | 155 | 56.1% | 49.9% | 6.2% |
| usdils_change_5d | 14 | volatility | all | 704 | 47.2% | 41.0% | 6.1% |
| usdils_change_5d | 14 | volatility | top 50% intensity | 353 | 55.2% | 47.7% | 7.5% |
| usdils_change_5d | 14 | volatility | top 25% intensity | 177 | 50.8% | 48.0% | 2.9% |
| usdils_change_5d | 30 | market | all | 605 | 50.9% | 51.4% | -0.5% |
| usdils_change_5d | 30 | market | top 50% intensity | 303 | 45.5% | 49.9% | -4.4% |
| usdils_change_5d | 30 | market | top 25% intensity | 153 | 44.4% | 49.8% | -5.4% |
| usdils_change_5d | 30 | volatility | all | 688 | 46.2% | 40.9% | 5.3% |
| usdils_change_5d | 30 | volatility | top 50% intensity | 345 | 51.9% | 46.5% | 5.4% |
| usdils_change_5d | 30 | volatility | top 25% intensity | 173 | 51.4% | 47.1% | 4.4% |
| vix9d_vix_ratio | 3 | market | all | 630 | 59.7% | 58.0% | 1.7% |
| vix9d_vix_ratio | 3 | market | top 50% intensity | 315 | 56.8% | 54.0% | 2.8% |
| vix9d_vix_ratio | 3 | market | top 25% intensity | 159 | 54.7% | 49.9% | 4.8% |
| vix9d_vix_ratio | 3 | volatility | all | 715 | 49.2% | 49.2% | 0.0% |
| vix9d_vix_ratio | 3 | volatility | top 50% intensity | 358 | 41.6% | 41.1% | 0.5% |
| vix9d_vix_ratio | 3 | volatility | top 25% intensity | 179 | 44.1% | 48.3% | -4.1% |
| vix9d_vix_ratio | 7 | market | all | 626 | 59.4% | 58.4% | 1.0% |
| vix9d_vix_ratio | 7 | market | top 50% intensity | 313 | 57.8% | 55.1% | 2.8% |
| vix9d_vix_ratio | 7 | market | top 25% intensity | 157 | 54.8% | 49.9% | 4.9% |
| vix9d_vix_ratio | 7 | volatility | all | 711 | 42.9% | 43.6% | -0.7% |
| vix9d_vix_ratio | 7 | volatility | top 50% intensity | 357 | 38.7% | 38.8% | -0.1% |
| vix9d_vix_ratio | 7 | volatility | top 25% intensity | 178 | 44.4% | 47.2% | -2.8% |
| vix9d_vix_ratio | 14 | market | all | 620 | 61.3% | 63.2% | -1.9% |
| vix9d_vix_ratio | 14 | market | top 50% intensity | 310 | 55.2% | 57.8% | -2.7% |
| vix9d_vix_ratio | 14 | market | top 25% intensity | 155 | 51.0% | 49.8% | 1.1% |
| vix9d_vix_ratio | 14 | volatility | all | 704 | 43.3% | 41.4% | 1.9% |
| vix9d_vix_ratio | 14 | volatility | top 50% intensity | 353 | 42.2% | 37.9% | 4.3% |
| vix9d_vix_ratio | 14 | volatility | top 25% intensity | 177 | 53.7% | 47.2% | 6.5% |
| vix9d_vix_ratio | 30 | market | all | 604 | 63.7% | 66.9% | -3.1% |
| vix9d_vix_ratio | 30 | market | top 50% intensity | 303 | 53.8% | 59.3% | -5.5% |
| vix9d_vix_ratio | 30 | market | top 25% intensity | 151 | 47.7% | 49.8% | -2.1% |
| vix9d_vix_ratio | 30 | volatility | all | 688 | 37.8% | 41.0% | -3.2% |
| vix9d_vix_ratio | 30 | volatility | top 50% intensity | 345 | 33.6% | 38.0% | -4.4% |
| vix9d_vix_ratio | 30 | volatility | top 25% intensity | 173 | 39.3% | 43.6% | -4.3% |
| vix_curve_ratio | 3 | market | all | 710 | 57.7% | 57.8% | -0.1% |
| vix_curve_ratio | 3 | market | top 50% intensity | 355 | 55.2% | 55.7% | -0.5% |
| vix_curve_ratio | 3 | market | top 25% intensity | 178 | 52.2% | 52.9% | -0.7% |
| vix_curve_ratio | 3 | volatility | all | 715 | 57.5% | 56.7% | 0.8% |
| vix_curve_ratio | 3 | volatility | top 50% intensity | 358 | 55.0% | 53.2% | 1.8% |
| vix_curve_ratio | 3 | volatility | top 25% intensity | 179 | 44.1% | 43.7% | 0.4% |
| vix_curve_ratio | 7 | market | all | 706 | 57.8% | 59.5% | -1.7% |
| vix_curve_ratio | 7 | market | top 50% intensity | 353 | 55.8% | 58.7% | -2.9% |
| vix_curve_ratio | 7 | market | top 25% intensity | 177 | 55.4% | 56.5% | -1.1% |
| vix_curve_ratio | 7 | volatility | all | 711 | 49.9% | 48.9% | 1.1% |
| vix_curve_ratio | 7 | volatility | top 50% intensity | 357 | 49.0% | 46.8% | 2.2% |
| vix_curve_ratio | 7 | volatility | top 25% intensity | 178 | 43.8% | 41.9% | 1.9% |
| vix_curve_ratio | 14 | market | all | 699 | 64.5% | 65.3% | -0.8% |
| vix_curve_ratio | 14 | market | top 50% intensity | 351 | 62.4% | 63.4% | -1.0% |
| vix_curve_ratio | 14 | market | top 25% intensity | 175 | 56.6% | 57.1% | -0.5% |
| vix_curve_ratio | 14 | volatility | all | 704 | 47.6% | 45.9% | 1.7% |
| vix_curve_ratio | 14 | volatility | top 50% intensity | 353 | 50.7% | 46.1% | 4.6% |
| vix_curve_ratio | 14 | volatility | top 25% intensity | 177 | 49.2% | 41.8% | 7.4% |
| vix_curve_ratio | 30 | market | all | 683 | 68.5% | 70.6% | -2.1% |
| vix_curve_ratio | 30 | market | top 50% intensity | 343 | 64.7% | 67.9% | -3.2% |
| vix_curve_ratio | 30 | market | top 25% intensity | 171 | 53.8% | 58.8% | -5.0% |
| vix_curve_ratio | 30 | volatility | all | 688 | 43.9% | 45.4% | -1.5% |
| vix_curve_ratio | 30 | volatility | top 50% intensity | 345 | 42.9% | 44.8% | -1.9% |
| vix_curve_ratio | 30 | volatility | top 25% intensity | 173 | 38.2% | 40.5% | -2.3% |
| vix_vix3m_ratio | 3 | market | all | 690 | 57.5% | 58.8% | -1.3% |
| vix_vix3m_ratio | 3 | market | top 50% intensity | 345 | 56.8% | 59.1% | -2.3% |
| vix_vix3m_ratio | 3 | market | top 25% intensity | 173 | 53.8% | 58.0% | -4.3% |
| vix_vix3m_ratio | 3 | volatility | all | 715 | 56.5% | 56.2% | 0.3% |
| vix_vix3m_ratio | 3 | volatility | top 50% intensity | 358 | 52.8% | 52.0% | 0.8% |
| vix_vix3m_ratio | 3 | volatility | top 25% intensity | 179 | 43.0% | 42.1% | 0.9% |
| vix_vix3m_ratio | 7 | market | all | 686 | 57.7% | 59.5% | -1.8% |
| vix_vix3m_ratio | 7 | market | top 50% intensity | 343 | 59.2% | 62.1% | -2.9% |
| vix_vix3m_ratio | 7 | market | top 25% intensity | 173 | 55.5% | 60.8% | -5.3% |
| vix_vix3m_ratio | 7 | volatility | all | 711 | 48.0% | 48.0% | -0.1% |
| vix_vix3m_ratio | 7 | volatility | top 50% intensity | 357 | 44.8% | 44.9% | -0.1% |
| vix_vix3m_ratio | 7 | volatility | top 25% intensity | 178 | 37.6% | 38.3% | -0.7% |
| vix_vix3m_ratio | 14 | market | all | 679 | 65.8% | 66.1% | -0.3% |
| vix_vix3m_ratio | 14 | market | top 50% intensity | 341 | 65.4% | 65.8% | -0.4% |
| vix_vix3m_ratio | 14 | market | top 25% intensity | 171 | 63.2% | 63.6% | -0.4% |
| vix_vix3m_ratio | 14 | volatility | all | 704 | 44.5% | 44.8% | -0.3% |
| vix_vix3m_ratio | 14 | volatility | top 50% intensity | 353 | 43.9% | 43.8% | 0.1% |
| vix_vix3m_ratio | 14 | volatility | top 25% intensity | 177 | 40.1% | 38.7% | 1.4% |
| vix_vix3m_ratio | 30 | market | all | 663 | 71.0% | 72.0% | -1.0% |
| vix_vix3m_ratio | 30 | market | top 50% intensity | 333 | 72.4% | 73.6% | -1.2% |
| vix_vix3m_ratio | 30 | market | top 25% intensity | 167 | 67.7% | 69.7% | -2.0% |
| vix_vix3m_ratio | 30 | volatility | all | 688 | 44.0% | 44.3% | -0.3% |
| vix_vix3m_ratio | 30 | volatility | top 50% intensity | 345 | 42.3% | 42.6% | -0.3% |
| vix_vix3m_ratio | 30 | volatility | top 25% intensity | 173 | 39.9% | 38.8% | 1.1% |
| vrp_spread | 3 | volatility | all | 715 | 51.7% | 40.0% | 11.8% |
| vrp_spread | 3 | volatility | top 50% intensity | 358 | 66.5% | 47.8% | 18.7% |
| vrp_spread | 3 | volatility | top 25% intensity | 179 | 73.7% | 48.0% | 25.8% |
| vrp_spread | 7 | volatility | all | 711 | 57.7% | 41.3% | 16.4% |
| vrp_spread | 7 | volatility | top 50% intensity | 357 | 75.1% | 47.5% | 27.6% |
| vrp_spread | 7 | volatility | top 25% intensity | 178 | 84.3% | 48.5% | 35.7% |
| vrp_spread | 14 | volatility | all | 704 | 57.7% | 42.6% | 15.1% |
| vrp_spread | 14 | volatility | top 50% intensity | 353 | 73.4% | 47.3% | 26.1% |
| vrp_spread | 14 | volatility | top 25% intensity | 177 | 84.2% | 49.1% | 35.0% |
| vrp_spread | 30 | volatility | all | 688 | 59.4% | 42.5% | 16.9% |
| vrp_spread | 30 | volatility | top 50% intensity | 345 | 74.5% | 46.7% | 27.8% |
| vrp_spread | 30 | volatility | top 25% intensity | 173 | 86.1% | 48.0% | 38.2% |
| vta35 | 3 | market | all | 603 | 48.9% | 51.1% | -2.2% |
| vta35 | 3 | market | top 50% intensity | 302 | 49.3% | 48.6% | 0.8% |
| vta35 | 3 | market | top 25% intensity | 151 | 47.7% | 48.9% | -1.3% |
| vta35 | 3 | volatility | all | 676 | 48.1% | 44.7% | 3.4% |
| vta35 | 3 | volatility | top 50% intensity | 339 | 50.1% | 45.1% | 5.0% |
| vta35 | 3 | volatility | top 25% intensity | 169 | 49.1% | 44.8% | 4.3% |
| vta35 | 7 | market | all | 601 | 41.8% | 51.4% | -9.6% |
| vta35 | 7 | market | top 50% intensity | 301 | 43.2% | 47.5% | -4.3% |
| vta35 | 7 | market | top 25% intensity | 151 | 41.7% | 48.9% | -7.2% |
| vta35 | 7 | volatility | all | 672 | 46.6% | 42.9% | 3.6% |
| vta35 | 7 | volatility | top 50% intensity | 337 | 47.2% | 44.4% | 2.8% |
| vta35 | 7 | volatility | top 25% intensity | 169 | 45.0% | 44.2% | 0.7% |
| vta35 | 14 | market | all | 595 | 49.4% | 52.3% | -2.9% |
| vta35 | 14 | market | top 50% intensity | 298 | 50.3% | 47.2% | 3.1% |
| vta35 | 14 | market | top 25% intensity | 149 | 46.3% | 48.8% | -2.5% |
| vta35 | 14 | volatility | all | 665 | 45.7% | 42.4% | 3.3% |
| vta35 | 14 | volatility | top 50% intensity | 334 | 47.0% | 45.4% | 1.6% |
| vta35 | 14 | volatility | top 25% intensity | 167 | 43.1% | 46.1% | -3.0% |
| vta35 | 30 | market | all | 582 | 52.6% | 53.7% | -1.1% |
| vta35 | 30 | market | top 50% intensity | 292 | 49.0% | 46.6% | 2.4% |
| vta35 | 30 | market | top 25% intensity | 147 | 48.3% | 48.0% | 0.3% |
| vta35 | 30 | volatility | all | 649 | 43.5% | 42.4% | 1.1% |
| vta35 | 30 | volatility | top 50% intensity | 328 | 39.6% | 45.4% | -5.8% |
| vta35 | 30 | volatility | top 25% intensity | 163 | 29.4% | 47.3% | -17.8% |
| vta35_change_5d | 3 | market | all | 680 | 50.3% | 50.5% | -0.2% |
| vta35_change_5d | 3 | market | top 50% intensity | 341 | 49.0% | 50.0% | -1.0% |
| vta35_change_5d | 3 | market | top 25% intensity | 171 | 45.0% | 49.9% | -4.9% |
| vta35_change_5d | 3 | volatility | all | 715 | 48.4% | 45.8% | 2.6% |
| vta35_change_5d | 3 | volatility | top 50% intensity | 358 | 52.5% | 48.0% | 4.5% |
| vta35_change_5d | 3 | volatility | top 25% intensity | 179 | 54.2% | 47.7% | 6.5% |
| vta35_change_5d | 7 | market | all | 677 | 46.8% | 50.7% | -3.8% |
| vta35_change_5d | 7 | market | top 50% intensity | 339 | 44.0% | 50.0% | -6.0% |
| vta35_change_5d | 7 | market | top 25% intensity | 171 | 40.9% | 49.9% | -9.0% |
| vta35_change_5d | 7 | volatility | all | 711 | 50.8% | 44.1% | 6.6% |
| vta35_change_5d | 7 | volatility | top 50% intensity | 357 | 57.1% | 46.8% | 10.4% |
| vta35_change_5d | 7 | volatility | top 25% intensity | 178 | 63.5% | 48.1% | 15.4% |
| vta35_change_5d | 14 | market | all | 670 | 51.3% | 51.1% | 0.2% |
| vta35_change_5d | 14 | market | top 50% intensity | 335 | 51.6% | 49.9% | 1.7% |
| vta35_change_5d | 14 | market | top 25% intensity | 169 | 52.7% | 49.9% | 2.8% |
| vta35_change_5d | 14 | volatility | all | 704 | 51.1% | 44.0% | 7.2% |
| vta35_change_5d | 14 | volatility | top 50% intensity | 353 | 55.5% | 48.0% | 7.5% |
| vta35_change_5d | 14 | volatility | top 25% intensity | 177 | 59.3% | 48.9% | 10.4% |
| vta35_change_5d | 30 | market | all | 657 | 53.4% | 51.4% | 2.1% |
| vta35_change_5d | 30 | market | top 50% intensity | 329 | 52.6% | 49.9% | 2.7% |
| vta35_change_5d | 30 | market | top 25% intensity | 165 | 50.3% | 49.8% | 0.5% |
| vta35_change_5d | 30 | volatility | all | 688 | 48.7% | 44.0% | 4.7% |
| vta35_change_5d | 30 | volatility | top 50% intensity | 345 | 52.2% | 47.1% | 5.1% |
| vta35_change_5d | 30 | volatility | top 25% intensity | 173 | 56.6% | 47.4% | 9.2% |
| vta35_zscore_60 | 3 | market | all | 603 | 48.9% | 51.1% | -2.2% |
| vta35_zscore_60 | 3 | market | top 50% intensity | 302 | 45.7% | 49.9% | -4.2% |
| vta35_zscore_60 | 3 | market | top 25% intensity | 151 | 46.4% | 49.9% | -3.5% |
| vta35_zscore_60 | 3 | volatility | all | 676 | 48.1% | 44.7% | 3.4% |
| vta35_zscore_60 | 3 | volatility | top 50% intensity | 339 | 51.6% | 48.2% | 3.4% |
| vta35_zscore_60 | 3 | volatility | top 25% intensity | 169 | 56.2% | 48.1% | 8.1% |
| vta35_zscore_60 | 7 | market | all | 601 | 41.8% | 51.4% | -9.6% |
| vta35_zscore_60 | 7 | market | top 50% intensity | 301 | 41.9% | 49.9% | -8.1% |
| vta35_zscore_60 | 7 | market | top 25% intensity | 151 | 40.4% | 49.9% | -9.5% |
| vta35_zscore_60 | 7 | volatility | all | 672 | 46.6% | 42.9% | 3.6% |
| vta35_zscore_60 | 7 | volatility | top 50% intensity | 337 | 51.6% | 45.8% | 5.8% |
| vta35_zscore_60 | 7 | volatility | top 25% intensity | 169 | 58.0% | 46.7% | 11.2% |
| vta35_zscore_60 | 14 | market | all | 595 | 49.4% | 52.3% | -2.9% |
| vta35_zscore_60 | 14 | market | top 50% intensity | 299 | 46.8% | 49.9% | -3.1% |
| vta35_zscore_60 | 14 | market | top 25% intensity | 149 | 47.0% | 49.8% | -2.8% |
| vta35_zscore_60 | 14 | volatility | all | 665 | 45.7% | 42.4% | 3.3% |
| vta35_zscore_60 | 14 | volatility | top 50% intensity | 333 | 50.2% | 46.5% | 3.6% |
| vta35_zscore_60 | 14 | volatility | top 25% intensity | 167 | 49.7% | 46.7% | 3.0% |
| vta35_zscore_60 | 30 | market | all | 582 | 52.6% | 53.7% | -1.1% |
| vta35_zscore_60 | 30 | market | top 50% intensity | 291 | 47.8% | 49.9% | -2.1% |
| vta35_zscore_60 | 30 | market | top 25% intensity | 147 | 47.6% | 49.7% | -2.1% |
| vta35_zscore_60 | 30 | volatility | all | 649 | 43.5% | 42.4% | 1.1% |
| vta35_zscore_60 | 30 | volatility | top 50% intensity | 325 | 44.6% | 46.0% | -1.4% |
| vta35_zscore_60 | 30 | volatility | top 25% intensity | 163 | 38.7% | 44.8% | -6.2% |

## Indicator robustness by market regime

| indicator | horizon | axis | regime | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | זהירות | 99 | 40.4% | 37.3% | 3.1% |
| atr_5_20_ratio | 3 | volatility | לחץ גבוה | 39 | 43.6% | 45.0% | -1.4% |
| atr_5_20_ratio | 3 | volatility | רגוע | 279 | 41.6% | 44.1% | -2.5% |
| atr_5_20_ratio | 3 | volatility | רגיל | 298 | 50.7% | 44.2% | 6.5% |
| atr_5_20_ratio | 7 | volatility | זהירות | 99 | 43.4% | 43.4% | 0.0% |
| atr_5_20_ratio | 7 | volatility | לחץ גבוה | 39 | 51.3% | 52.7% | -1.4% |
| atr_5_20_ratio | 7 | volatility | רגוע | 277 | 47.7% | 40.6% | 7.0% |
| atr_5_20_ratio | 7 | volatility | רגיל | 296 | 44.6% | 42.8% | 1.8% |
| atr_5_20_ratio | 14 | volatility | זהירות | 96 | 47.9% | 45.3% | 2.6% |
| atr_5_20_ratio | 14 | volatility | לחץ גבוה | 39 | 35.9% | 37.5% | -1.6% |
| atr_5_20_ratio | 14 | volatility | רגוע | 276 | 47.8% | 38.9% | 9.0% |
| atr_5_20_ratio | 14 | volatility | רגיל | 293 | 51.2% | 42.7% | 8.5% |
| atr_5_20_ratio | 30 | volatility | זהירות | 91 | 49.5% | 43.9% | 5.5% |
| atr_5_20_ratio | 30 | volatility | לחץ גבוה | 39 | 28.2% | 30.2% | -2.0% |
| atr_5_20_ratio | 30 | volatility | רגוע | 271 | 51.3% | 39.0% | 12.2% |
| atr_5_20_ratio | 30 | volatility | רגיל | 287 | 51.2% | 41.9% | 9.4% |
| expected_move_3d_points | 3 | volatility | זהירות | 99 | 29.3% | 26.3% | 3.0% |
| expected_move_3d_points | 3 | volatility | לחץ גבוה | 39 | 15.4% | 17.0% | -1.6% |
| expected_move_3d_points | 3 | volatility | רגוע | 279 | 36.2% | 30.7% | 5.5% |
| expected_move_3d_points | 3 | volatility | רגיל | 298 | 39.9% | 32.0% | 8.0% |
| expected_move_3d_points | 7 | volatility | זהירות | 99 | 42.4% | 27.5% | 14.9% |
| expected_move_3d_points | 7 | volatility | לחץ גבוה | 39 | 28.2% | 23.5% | 4.7% |
| expected_move_3d_points | 7 | volatility | רגוע | 277 | 37.9% | 30.2% | 7.7% |
| expected_move_3d_points | 7 | volatility | רגיל | 296 | 38.5% | 31.9% | 6.6% |
| expected_move_3d_points | 14 | volatility | זהירות | 96 | 44.8% | 28.0% | 16.8% |
| expected_move_3d_points | 14 | volatility | לחץ גבוה | 39 | 23.1% | 15.0% | 8.1% |
| expected_move_3d_points | 14 | volatility | רגוע | 276 | 37.0% | 29.8% | 7.2% |
| expected_move_3d_points | 14 | volatility | רגיל | 293 | 45.1% | 31.6% | 13.4% |
| expected_move_3d_points | 30 | volatility | זהירות | 91 | 49.5% | 27.0% | 22.5% |
| expected_move_3d_points | 30 | volatility | לחץ גבוה | 39 | 20.5% | 17.6% | 3.0% |
| expected_move_3d_points | 30 | volatility | רגוע | 271 | 33.6% | 28.7% | 4.9% |
| expected_move_3d_points | 30 | volatility | רגיל | 287 | 44.3% | 31.7% | 12.5% |
| forecast_rv_3d | 3 | volatility | זהירות | 99 | 29.3% | 26.3% | 3.0% |
| forecast_rv_3d | 3 | volatility | לחץ גבוה | 39 | 15.4% | 17.0% | -1.6% |
| forecast_rv_3d | 3 | volatility | רגוע | 279 | 36.2% | 30.7% | 5.5% |
| forecast_rv_3d | 3 | volatility | רגיל | 298 | 39.9% | 32.0% | 8.0% |
| forecast_rv_3d | 7 | volatility | זהירות | 99 | 42.4% | 27.5% | 14.9% |
| forecast_rv_3d | 7 | volatility | לחץ גבוה | 39 | 28.2% | 23.5% | 4.7% |
| forecast_rv_3d | 7 | volatility | רגוע | 277 | 37.9% | 30.2% | 7.7% |
| forecast_rv_3d | 7 | volatility | רגיל | 296 | 38.5% | 31.9% | 6.6% |
| forecast_rv_3d | 14 | volatility | זהירות | 96 | 44.8% | 28.0% | 16.8% |
| forecast_rv_3d | 14 | volatility | לחץ גבוה | 39 | 23.1% | 15.0% | 8.1% |
| forecast_rv_3d | 14 | volatility | רגוע | 276 | 37.0% | 29.8% | 7.2% |
| forecast_rv_3d | 14 | volatility | רגיל | 293 | 45.1% | 31.6% | 13.4% |
| forecast_rv_3d | 30 | volatility | זהירות | 91 | 49.5% | 27.0% | 22.5% |
| forecast_rv_3d | 30 | volatility | לחץ גבוה | 39 | 20.5% | 17.6% | 3.0% |
| forecast_rv_3d | 30 | volatility | רגוע | 271 | 33.6% | 28.7% | 4.9% |
| forecast_rv_3d | 30 | volatility | רגיל | 287 | 44.3% | 31.7% | 12.5% |
| gap_share_20 | 3 | volatility | זהירות | 99 | 31.3% | 33.4% | -2.1% |
| gap_share_20 | 3 | volatility | לחץ גבוה | 39 | 41.0% | 36.9% | 4.1% |
| gap_share_20 | 3 | volatility | רגוע | 279 | 33.3% | 32.6% | 0.7% |
| gap_share_20 | 3 | volatility | רגיל | 298 | 32.6% | 35.5% | -2.9% |
| gap_share_20 | 7 | volatility | זהירות | 99 | 33.3% | 34.1% | -0.8% |
| gap_share_20 | 7 | volatility | לחץ גבוה | 39 | 48.7% | 44.0% | 4.7% |
| gap_share_20 | 7 | volatility | רגוע | 277 | 30.7% | 30.9% | -0.2% |
| gap_share_20 | 7 | volatility | רגיל | 296 | 32.4% | 35.4% | -3.0% |
| gap_share_20 | 14 | volatility | זהירות | 96 | 28.1% | 34.8% | -6.7% |
| gap_share_20 | 14 | volatility | לחץ גבוה | 39 | 30.8% | 31.2% | -0.4% |
| gap_share_20 | 14 | volatility | רגוע | 276 | 26.1% | 30.1% | -4.0% |
| gap_share_20 | 14 | volatility | רגיל | 293 | 29.4% | 36.0% | -6.7% |
| gap_share_20 | 30 | volatility | זהירות | 91 | 25.3% | 35.7% | -10.4% |
| gap_share_20 | 30 | volatility | לחץ גבוה | 39 | 20.5% | 26.8% | -6.3% |
| gap_share_20 | 30 | volatility | רגוע | 271 | 23.6% | 29.4% | -5.8% |
| gap_share_20 | 30 | volatility | רגיל | 287 | 23.0% | 36.3% | -13.3% |
| rv_20_60_ratio | 3 | volatility | זהירות | 84 | 29.8% | 38.4% | -8.6% |
| rv_20_60_ratio | 3 | volatility | לחץ גבוה | 32 | 50.0% | 42.6% | 7.4% |
| rv_20_60_ratio | 3 | volatility | רגוע | 274 | 43.8% | 48.5% | -4.7% |
| rv_20_60_ratio | 3 | volatility | רגיל | 285 | 37.2% | 43.8% | -6.6% |
| rv_20_60_ratio | 7 | volatility | זהירות | 84 | 23.8% | 40.4% | -16.6% |
| rv_20_60_ratio | 7 | volatility | לחץ גבוה | 32 | 31.2% | 42.0% | -10.7% |
| rv_20_60_ratio | 7 | volatility | רגוע | 272 | 34.2% | 43.4% | -9.2% |
| rv_20_60_ratio | 7 | volatility | רגיל | 283 | 31.4% | 42.5% | -11.0% |
| rv_20_60_ratio | 14 | volatility | זהירות | 81 | 24.7% | 40.3% | -15.6% |
| rv_20_60_ratio | 14 | volatility | לחץ גבוה | 32 | 28.1% | 40.4% | -12.3% |
| rv_20_60_ratio | 14 | volatility | רגוע | 271 | 31.0% | 40.9% | -9.9% |
| rv_20_60_ratio | 14 | volatility | רגיל | 280 | 29.6% | 42.6% | -13.0% |
| rv_20_60_ratio | 30 | volatility | זהירות | 76 | 21.1% | 40.0% | -18.9% |
| rv_20_60_ratio | 30 | volatility | לחץ גבוה | 32 | 18.8% | 33.4% | -14.6% |
| rv_20_60_ratio | 30 | volatility | רגוע | 266 | 30.8% | 40.9% | -10.0% |
| rv_20_60_ratio | 30 | volatility | רגיל | 274 | 23.7% | 41.4% | -17.7% |
| rv_acceleration | 3 | volatility | זהירות | 99 | 37.4% | 40.2% | -2.8% |
| rv_acceleration | 3 | volatility | לחץ גבוה | 39 | 46.2% | 45.0% | 1.2% |
| rv_acceleration | 3 | volatility | רגוע | 279 | 48.7% | 48.6% | 0.2% |
| rv_acceleration | 3 | volatility | רגיל | 298 | 51.0% | 47.3% | 3.7% |
| rv_acceleration | 7 | volatility | זהירות | 99 | 44.4% | 43.5% | 0.9% |
| rv_acceleration | 7 | volatility | לחץ גבוה | 39 | 51.3% | 52.7% | -1.4% |
| rv_acceleration | 7 | volatility | רגוע | 277 | 37.9% | 43.4% | -5.5% |
| rv_acceleration | 7 | volatility | רגיל | 296 | 43.2% | 45.2% | -2.0% |
| rv_acceleration | 14 | volatility | זהירות | 96 | 53.1% | 43.9% | 9.2% |
| rv_acceleration | 14 | volatility | לחץ גבוה | 39 | 35.9% | 37.5% | -1.6% |
| rv_acceleration | 14 | volatility | רגוע | 276 | 38.8% | 40.8% | -2.1% |
| rv_acceleration | 14 | volatility | רגיל | 293 | 50.5% | 44.7% | 5.8% |
| rv_acceleration | 30 | volatility | זהירות | 91 | 54.9% | 43.3% | 11.6% |
| rv_acceleration | 30 | volatility | לחץ גבוה | 39 | 33.3% | 30.2% | 3.2% |
| rv_acceleration | 30 | volatility | רגוע | 271 | 38.7% | 40.6% | -1.9% |
| rv_acceleration | 30 | volatility | רגיל | 287 | 50.5% | 43.4% | 7.1% |
| usdils_change_5d | 3 | market | זהירות | 93 | 51.6% | 48.6% | 3.0% |
| usdils_change_5d | 3 | market | לחץ גבוה | 33 | 36.4% | 40.0% | -3.7% |
| usdils_change_5d | 3 | market | רגוע | 237 | 48.5% | 52.4% | -3.9% |
| usdils_change_5d | 3 | market | רגיל | 267 | 54.7% | 50.1% | 4.6% |
| usdils_change_5d | 3 | volatility | זהירות | 99 | 34.3% | 39.5% | -5.2% |
| usdils_change_5d | 3 | volatility | לחץ גבוה | 39 | 35.9% | 39.3% | -3.4% |
| usdils_change_5d | 3 | volatility | רגוע | 279 | 47.0% | 44.5% | 2.5% |
| usdils_change_5d | 3 | volatility | רגיל | 298 | 49.3% | 43.1% | 6.3% |
| usdils_change_5d | 7 | market | זהירות | 93 | 50.5% | 44.9% | 5.6% |
| usdils_change_5d | 7 | market | לחץ גבוה | 33 | 33.3% | 37.2% | -3.9% |
| usdils_change_5d | 7 | market | רגוע | 235 | 48.1% | 52.8% | -4.7% |
| usdils_change_5d | 7 | market | רגיל | 266 | 50.4% | 50.2% | 0.2% |
| usdils_change_5d | 7 | volatility | זהירות | 99 | 37.4% | 43.9% | -6.5% |
| usdils_change_5d | 7 | volatility | לחץ גבוה | 39 | 43.6% | 46.4% | -2.8% |
| usdils_change_5d | 7 | volatility | רגוע | 277 | 43.0% | 40.5% | 2.5% |
| usdils_change_5d | 7 | volatility | רגיל | 296 | 51.4% | 42.1% | 9.3% |
| usdils_change_5d | 14 | market | זהירות | 90 | 50.0% | 45.7% | 4.3% |
| usdils_change_5d | 14 | market | לחץ גבוה | 33 | 30.3% | 34.3% | -4.0% |
| usdils_change_5d | 14 | market | רגוע | 234 | 57.3% | 57.1% | 0.2% |
| usdils_change_5d | 14 | market | רגיל | 263 | 55.5% | 50.5% | 5.0% |
| usdils_change_5d | 14 | volatility | זהירות | 96 | 47.9% | 44.7% | 3.2% |
| usdils_change_5d | 14 | volatility | לחץ גבוה | 39 | 33.3% | 33.1% | 0.2% |
| usdils_change_5d | 14 | volatility | רגוע | 276 | 41.7% | 38.6% | 3.1% |
| usdils_change_5d | 14 | volatility | רגיל | 293 | 53.9% | 42.2% | 11.7% |
| usdils_change_5d | 30 | market | זהירות | 85 | 49.4% | 40.2% | 9.2% |
| usdils_change_5d | 30 | market | לחץ גבוה | 33 | 21.2% | 25.8% | -4.6% |
| usdils_change_5d | 30 | market | רגוע | 229 | 59.0% | 58.2% | 0.7% |
| usdils_change_5d | 30 | market | רגיל | 258 | 48.1% | 50.8% | -2.7% |
| usdils_change_5d | 30 | volatility | זהירות | 91 | 46.2% | 43.7% | 2.5% |
| usdils_change_5d | 30 | volatility | לחץ גבוה | 39 | 20.5% | 28.0% | -7.5% |
| usdils_change_5d | 30 | volatility | רגוע | 271 | 43.2% | 38.2% | 4.9% |
| usdils_change_5d | 30 | volatility | רגיל | 287 | 52.6% | 41.3% | 11.3% |
| vix9d_vix_ratio | 3 | market | זהירות | 70 | 60.0% | 54.3% | 5.7% |
| vix9d_vix_ratio | 3 | market | לחץ גבוה | 31 | 41.9% | 48.2% | -6.2% |
| vix9d_vix_ratio | 3 | market | רגוע | 265 | 59.6% | 58.3% | 1.3% |
| vix9d_vix_ratio | 3 | market | רגיל | 264 | 61.7% | 59.6% | 2.2% |
| vix9d_vix_ratio | 3 | volatility | זהירות | 99 | 34.3% | 38.6% | -4.3% |
| vix9d_vix_ratio | 3 | volatility | לחץ גבוה | 39 | 43.6% | 39.3% | 4.3% |
| vix9d_vix_ratio | 3 | volatility | רגוע | 279 | 52.7% | 53.6% | -0.9% |
| vix9d_vix_ratio | 3 | volatility | רגיל | 298 | 51.7% | 50.9% | 0.8% |
| vix9d_vix_ratio | 7 | market | זהירות | 70 | 65.7% | 58.0% | 7.8% |
| vix9d_vix_ratio | 7 | market | לחץ גבוה | 31 | 45.2% | 47.7% | -2.5% |
| vix9d_vix_ratio | 7 | market | רגוע | 263 | 58.6% | 57.4% | 1.2% |
| vix9d_vix_ratio | 7 | market | רגיל | 262 | 60.3% | 59.6% | 0.7% |
| vix9d_vix_ratio | 7 | volatility | זהירות | 99 | 26.3% | 35.1% | -8.9% |
| vix9d_vix_ratio | 7 | volatility | לחץ גבוה | 39 | 33.3% | 39.3% | -5.9% |
| vix9d_vix_ratio | 7 | volatility | רגוע | 277 | 45.1% | 45.4% | -0.2% |
| vix9d_vix_ratio | 7 | volatility | רגיל | 296 | 47.6% | 46.5% | 1.1% |
| vix9d_vix_ratio | 14 | market | זהירות | 67 | 56.7% | 56.3% | 0.4% |
| vix9d_vix_ratio | 14 | market | לחץ גבוה | 31 | 32.3% | 47.7% | -15.4% |
| vix9d_vix_ratio | 14 | market | רגוע | 262 | 65.3% | 67.8% | -2.5% |
| vix9d_vix_ratio | 14 | market | רגיל | 260 | 61.9% | 63.3% | -1.4% |
| vix9d_vix_ratio | 14 | volatility | זהירות | 96 | 32.3% | 33.5% | -1.2% |
| vix9d_vix_ratio | 14 | volatility | לחץ גבוה | 39 | 41.0% | 38.3% | 2.8% |
| vix9d_vix_ratio | 14 | volatility | רגוע | 276 | 43.1% | 41.3% | 1.8% |
| vix9d_vix_ratio | 14 | volatility | רגיל | 293 | 47.4% | 43.3% | 4.1% |
| vix9d_vix_ratio | 30 | market | זהירות | 62 | 54.8% | 59.7% | -4.9% |
| vix9d_vix_ratio | 30 | market | לחץ גבוה | 31 | 35.5% | 46.1% | -10.6% |
| vix9d_vix_ratio | 30 | market | רגוע | 257 | 68.1% | 69.6% | -1.5% |
| vix9d_vix_ratio | 30 | market | רגיל | 254 | 65.0% | 67.9% | -3.0% |
| vix9d_vix_ratio | 30 | volatility | זהירות | 91 | 23.1% | 34.2% | -11.1% |
| vix9d_vix_ratio | 30 | volatility | לחץ גבוה | 39 | 46.2% | 36.3% | 9.9% |
| vix9d_vix_ratio | 30 | volatility | רגוע | 271 | 39.1% | 40.4% | -1.3% |
| vix9d_vix_ratio | 30 | volatility | רגיל | 287 | 40.1% | 42.0% | -1.9% |
| vix_curve_ratio | 3 | market | זהירות | 93 | 51.6% | 52.5% | -0.9% |
| vix_curve_ratio | 3 | market | לחץ גבוה | 33 | 45.5% | 51.1% | -5.7% |
| vix_curve_ratio | 3 | market | רגוע | 287 | 57.8% | 57.8% | 0.0% |
| vix_curve_ratio | 3 | market | רגיל | 297 | 60.9% | 60.3% | 0.6% |
| vix_curve_ratio | 3 | volatility | זהירות | 99 | 50.5% | 51.0% | -0.5% |
| vix_curve_ratio | 3 | volatility | לחץ גבוה | 39 | 53.8% | 42.8% | 11.0% |
| vix_curve_ratio | 3 | volatility | רגוע | 279 | 59.5% | 59.7% | -0.2% |
| vix_curve_ratio | 3 | volatility | רגיל | 298 | 58.4% | 58.3% | 0.1% |
| vix_curve_ratio | 7 | market | זהירות | 93 | 55.9% | 59.5% | -3.6% |
| vix_curve_ratio | 7 | market | לחץ גבוה | 33 | 36.4% | 52.5% | -16.2% |
| vix_curve_ratio | 7 | market | רגוע | 285 | 58.2% | 58.2% | 0.0% |
| vix_curve_ratio | 7 | market | רגיל | 295 | 60.3% | 60.4% | -0.1% |
| vix_curve_ratio | 7 | volatility | זהירות | 99 | 39.4% | 44.4% | -5.0% |
| vix_curve_ratio | 7 | volatility | לחץ גבוה | 39 | 28.2% | 39.3% | -11.0% |
| vix_curve_ratio | 7 | volatility | רגוע | 277 | 49.8% | 49.2% | 0.6% |
| vix_curve_ratio | 7 | volatility | רגיל | 296 | 56.4% | 52.3% | 4.1% |
| vix_curve_ratio | 14 | market | זהירות | 90 | 57.8% | 59.3% | -1.5% |
| vix_curve_ratio | 14 | market | לחץ גבוה | 33 | 39.4% | 52.1% | -12.7% |
| vix_curve_ratio | 14 | market | רגוע | 284 | 70.4% | 70.4% | 0.0% |
| vix_curve_ratio | 14 | market | רגיל | 292 | 63.7% | 64.7% | -1.0% |
| vix_curve_ratio | 14 | volatility | זהירות | 96 | 44.8% | 41.3% | 3.5% |
| vix_curve_ratio | 14 | volatility | לחץ גבוה | 39 | 38.5% | 43.8% | -5.3% |
| vix_curve_ratio | 14 | volatility | רגוע | 276 | 44.6% | 44.1% | 0.5% |
| vix_curve_ratio | 14 | volatility | רגיל | 293 | 52.6% | 48.1% | 4.4% |
| vix_curve_ratio | 30 | market | זהירות | 85 | 65.9% | 68.7% | -2.8% |
| vix_curve_ratio | 30 | market | לחץ גבוה | 33 | 45.5% | 53.9% | -8.4% |
| vix_curve_ratio | 30 | market | רגוע | 279 | 72.4% | 72.4% | 0.0% |
| vix_curve_ratio | 30 | market | רגיל | 286 | 68.2% | 70.4% | -2.3% |
| vix_curve_ratio | 30 | volatility | זהירות | 91 | 39.6% | 44.7% | -5.1% |
| vix_curve_ratio | 30 | volatility | לחץ גבוה | 39 | 43.6% | 42.2% | 1.4% |
| vix_curve_ratio | 30 | volatility | רגוע | 271 | 42.8% | 43.0% | -0.2% |
| vix_curve_ratio | 30 | volatility | רגיל | 287 | 46.3% | 46.3% | 0.1% |
| vix_vix3m_ratio | 3 | market | זהירות | 89 | 53.9% | 54.5% | -0.6% |
| vix_vix3m_ratio | 3 | market | לחץ גבוה | 33 | 39.4% | 55.4% | -16.0% |
| vix_vix3m_ratio | 3 | market | רגוע | 289 | 57.8% | 57.8% | 0.0% |
| vix_vix3m_ratio | 3 | market | רגיל | 279 | 60.6% | 61.2% | -0.6% |
| vix_vix3m_ratio | 3 | volatility | זהירות | 99 | 49.5% | 51.6% | -2.1% |
| vix_vix3m_ratio | 3 | volatility | לחץ גבוה | 39 | 51.3% | 43.6% | 7.7% |
| vix_vix3m_ratio | 3 | volatility | רגוע | 279 | 60.6% | 60.2% | 0.4% |
| vix_vix3m_ratio | 3 | volatility | רגיל | 298 | 55.7% | 56.3% | -0.6% |
| vix_vix3m_ratio | 7 | market | זהירות | 89 | 57.3% | 61.5% | -4.2% |
| vix_vix3m_ratio | 7 | market | לחץ גבוה | 33 | 36.4% | 54.2% | -17.8% |
| vix_vix3m_ratio | 7 | market | רגוע | 287 | 57.8% | 57.8% | 0.0% |
| vix_vix3m_ratio | 7 | market | רגיל | 277 | 60.3% | 61.0% | -0.7% |
| vix_vix3m_ratio | 7 | volatility | זהירות | 99 | 34.3% | 42.8% | -8.5% |
| vix_vix3m_ratio | 7 | volatility | לחץ גבוה | 39 | 28.2% | 37.7% | -9.5% |
| vix_vix3m_ratio | 7 | volatility | רגוע | 277 | 49.8% | 49.5% | 0.3% |
| vix_vix3m_ratio | 7 | volatility | רגיל | 296 | 53.4% | 50.3% | 3.0% |
| vix_vix3m_ratio | 14 | market | זהירות | 86 | 60.5% | 60.3% | 0.2% |
| vix_vix3m_ratio | 14 | market | לחץ גבוה | 33 | 42.4% | 56.6% | -14.1% |
| vix_vix3m_ratio | 14 | market | רגוע | 286 | 70.6% | 70.6% | 0.0% |
| vix_vix3m_ratio | 14 | market | רגיל | 274 | 65.3% | 64.9% | 0.5% |
| vix_vix3m_ratio | 14 | volatility | זהירות | 96 | 39.6% | 39.0% | 0.6% |
| vix_vix3m_ratio | 14 | volatility | לחץ גבוה | 39 | 30.8% | 46.2% | -15.4% |
| vix_vix3m_ratio | 14 | volatility | רגוע | 276 | 44.6% | 44.3% | 0.3% |
| vix_vix3m_ratio | 14 | volatility | רגיל | 293 | 47.8% | 45.6% | 2.1% |
| vix_vix3m_ratio | 30 | market | זהירות | 81 | 74.1% | 74.3% | -0.3% |
| vix_vix3m_ratio | 30 | market | לחץ גבוה | 33 | 51.5% | 60.1% | -8.6% |
| vix_vix3m_ratio | 30 | market | רגוע | 281 | 72.6% | 72.6% | 0.0% |
| vix_vix3m_ratio | 30 | market | רגיל | 268 | 70.9% | 71.9% | -1.0% |
| vix_vix3m_ratio | 30 | volatility | זהירות | 91 | 42.9% | 43.1% | -0.2% |
| vix_vix3m_ratio | 30 | volatility | לחץ גבוה | 39 | 35.9% | 45.4% | -9.5% |
| vix_vix3m_ratio | 30 | volatility | רגוע | 271 | 43.5% | 43.3% | 0.3% |
| vix_vix3m_ratio | 30 | volatility | רגיל | 287 | 46.0% | 44.0% | 2.0% |
| vrp_spread | 3 | volatility | זהירות | 99 | 52.5% | 40.2% | 12.3% |
| vrp_spread | 3 | volatility | לחץ גבוה | 39 | 38.5% | 38.3% | 0.2% |
| vrp_spread | 3 | volatility | רגוע | 279 | 52.7% | 39.3% | 13.4% |
| vrp_spread | 3 | volatility | רגיל | 298 | 52.3% | 40.8% | 11.6% |
| vrp_spread | 7 | volatility | זהירות | 99 | 62.6% | 43.5% | 19.1% |
| vrp_spread | 7 | volatility | לחץ גבוה | 39 | 56.4% | 41.2% | 15.2% |
| vrp_spread | 7 | volatility | רגוע | 277 | 59.6% | 40.6% | 19.0% |
| vrp_spread | 7 | volatility | רגיל | 296 | 54.4% | 41.4% | 13.0% |
| vrp_spread | 14 | volatility | זהירות | 96 | 55.2% | 44.4% | 10.8% |
| vrp_spread | 14 | volatility | לחץ גבוה | 39 | 59.0% | 35.3% | 23.7% |
| vrp_spread | 14 | volatility | רגוע | 276 | 58.0% | 41.4% | 16.6% |
| vrp_spread | 14 | volatility | רגיל | 293 | 58.0% | 43.8% | 14.2% |
| vrp_spread | 30 | volatility | זהירות | 91 | 63.7% | 43.8% | 19.9% |
| vrp_spread | 30 | volatility | לחץ גבוה | 39 | 48.7% | 32.3% | 16.4% |
| vrp_spread | 30 | volatility | רגוע | 271 | 57.9% | 43.2% | 14.8% |
| vrp_spread | 30 | volatility | רגיל | 287 | 61.0% | 42.8% | 18.1% |
| vta35 | 3 | market | זהירות | 81 | 46.9% | 47.2% | -0.3% |
| vta35 | 3 | market | לחץ גבוה | 32 | 34.4% | 34.4% | 0.0% |
| vta35 | 3 | market | רגוע | 237 | 56.1% | 55.1% | 1.0% |
| vta35 | 3 | market | רגיל | 253 | 44.7% | 51.2% | -6.6% |
| vta35 | 3 | volatility | זהירות | 84 | 36.9% | 35.7% | 1.2% |
| vta35 | 3 | volatility | לחץ גבוה | 32 | 43.8% | 43.8% | 0.0% |
| vta35 | 3 | volatility | רגוע | 275 | 51.6% | 48.6% | 3.1% |
| vta35 | 3 | volatility | רגיל | 285 | 48.4% | 44.7% | 3.7% |
| vta35 | 7 | market | זהירות | 81 | 34.6% | 36.1% | -1.5% |
| vta35 | 7 | market | לחץ גבוה | 32 | 25.0% | 25.0% | 0.0% |
| vta35 | 7 | market | רגוע | 236 | 48.3% | 56.0% | -7.7% |
| vta35 | 7 | market | רגיל | 252 | 40.1% | 51.2% | -11.1% |
| vta35 | 7 | volatility | זהירות | 84 | 50.0% | 47.1% | 2.9% |
| vta35 | 7 | volatility | לחץ גבוה | 32 | 43.8% | 43.8% | 0.0% |
| vta35 | 7 | volatility | רגוע | 273 | 48.4% | 42.9% | 5.4% |
| vta35 | 7 | volatility | רגיל | 283 | 44.2% | 43.2% | 1.0% |
| vta35 | 14 | market | זהירות | 78 | 39.7% | 37.0% | 2.8% |
| vta35 | 14 | market | לחץ גבוה | 32 | 21.9% | 21.9% | 0.0% |
| vta35 | 14 | market | רגוע | 236 | 59.3% | 62.8% | -3.5% |
| vta35 | 14 | market | רגיל | 249 | 46.6% | 52.2% | -5.6% |
| vta35 | 14 | volatility | זהירות | 81 | 51.9% | 49.8% | 2.1% |
| vta35 | 14 | volatility | לחץ גבוה | 32 | 40.6% | 40.6% | 0.0% |
| vta35 | 14 | volatility | רגוע | 272 | 43.8% | 40.1% | 3.6% |
| vta35 | 14 | volatility | רגיל | 280 | 46.4% | 43.0% | 3.4% |
| vta35 | 30 | market | זהירות | 74 | 17.6% | 16.5% | 1.1% |
| vta35 | 30 | market | לחץ גבוה | 32 | 15.6% | 15.6% | 0.0% |
| vta35 | 30 | market | רגוע | 232 | 69.0% | 66.0% | 3.0% |
| vta35 | 30 | market | רגיל | 244 | 52.5% | 53.4% | -0.9% |
| vta35 | 30 | volatility | זהירות | 76 | 47.4% | 46.2% | 1.1% |
| vta35 | 30 | volatility | לחץ גבוה | 32 | 31.2% | 31.2% | 0.0% |
| vta35 | 30 | volatility | רגוע | 267 | 44.9% | 39.7% | 5.3% |
| vta35 | 30 | volatility | רגיל | 274 | 42.3% | 42.0% | 0.3% |
| vta35_change_5d | 3 | market | זהירות | 95 | 46.3% | 48.4% | -2.0% |
| vta35_change_5d | 3 | market | לחץ גבוה | 39 | 38.5% | 40.8% | -2.4% |
| vta35_change_5d | 3 | market | רגוע | 260 | 53.5% | 51.7% | 1.8% |
| vta35_change_5d | 3 | market | רגיל | 286 | 50.3% | 51.0% | -0.7% |
| vta35_change_5d | 3 | volatility | זהירות | 99 | 39.4% | 41.6% | -2.2% |
| vta35_change_5d | 3 | volatility | לחץ גבוה | 39 | 46.2% | 46.9% | -0.8% |
| vta35_change_5d | 3 | volatility | רגוע | 279 | 47.0% | 46.8% | 0.2% |
| vta35_change_5d | 3 | volatility | רגיל | 298 | 53.0% | 47.1% | 6.0% |
| vta35_change_5d | 7 | market | זהירות | 95 | 37.9% | 46.0% | -8.1% |
| vta35_change_5d | 7 | market | לחץ גבוה | 39 | 41.0% | 38.8% | 2.2% |
| vta35_change_5d | 7 | market | רגוע | 259 | 50.2% | 52.0% | -1.8% |
| vta35_change_5d | 7 | market | רגיל | 284 | 47.5% | 51.4% | -3.8% |
| vta35_change_5d | 7 | volatility | זהירות | 99 | 53.5% | 45.2% | 8.4% |
| vta35_change_5d | 7 | volatility | לחץ גבוה | 39 | 53.8% | 52.3% | 1.6% |
| vta35_change_5d | 7 | volatility | רגוע | 277 | 48.7% | 43.3% | 5.4% |
| vta35_change_5d | 7 | volatility | רגיל | 296 | 51.4% | 45.3% | 6.0% |
| vta35_change_5d | 14 | market | זהירות | 92 | 41.3% | 45.4% | -4.1% |
| vta35_change_5d | 14 | market | לחץ גבוה | 39 | 33.3% | 36.8% | -3.4% |
| vta35_change_5d | 14 | market | רגוע | 258 | 57.8% | 55.9% | 1.9% |
| vta35_change_5d | 14 | market | רגיל | 281 | 51.2% | 51.7% | -0.5% |
| vta35_change_5d | 14 | volatility | זהירות | 96 | 54.2% | 45.7% | 8.5% |
| vta35_change_5d | 14 | volatility | לחץ גבוה | 39 | 43.6% | 40.8% | 2.8% |
| vta35_change_5d | 14 | volatility | רגוע | 276 | 50.7% | 41.7% | 9.0% |
| vta35_change_5d | 14 | volatility | רגיל | 293 | 51.5% | 45.2% | 6.3% |
| vta35_change_5d | 30 | market | זהירות | 87 | 37.9% | 40.9% | -3.0% |
| vta35_change_5d | 30 | market | לחץ גבוה | 39 | 28.2% | 28.6% | -0.4% |
| vta35_change_5d | 30 | market | רגוע | 254 | 61.4% | 56.0% | 5.4% |
| vta35_change_5d | 30 | market | רגיל | 277 | 54.5% | 52.4% | 2.2% |
| vta35_change_5d | 30 | volatility | זהירות | 91 | 50.5% | 45.1% | 5.4% |
| vta35_change_5d | 30 | volatility | לחץ גבוה | 39 | 30.8% | 33.9% | -3.2% |
| vta35_change_5d | 30 | volatility | רגוע | 271 | 51.7% | 42.3% | 9.3% |
| vta35_change_5d | 30 | volatility | רגיל | 287 | 47.7% | 44.2% | 3.6% |
| vta35_zscore_60 | 3 | market | זהירות | 81 | 46.9% | 47.2% | -0.3% |
| vta35_zscore_60 | 3 | market | לחץ גבוה | 32 | 34.4% | 34.4% | 0.0% |
| vta35_zscore_60 | 3 | market | רגוע | 237 | 56.1% | 55.1% | 1.0% |
| vta35_zscore_60 | 3 | market | רגיל | 253 | 44.7% | 51.2% | -6.6% |
| vta35_zscore_60 | 3 | volatility | זהירות | 84 | 36.9% | 35.7% | 1.2% |
| vta35_zscore_60 | 3 | volatility | לחץ גבוה | 32 | 43.8% | 43.8% | 0.0% |
| vta35_zscore_60 | 3 | volatility | רגוע | 275 | 51.6% | 48.6% | 3.1% |
| vta35_zscore_60 | 3 | volatility | רגיל | 285 | 48.4% | 44.7% | 3.7% |
| vta35_zscore_60 | 7 | market | זהירות | 81 | 34.6% | 36.1% | -1.5% |
| vta35_zscore_60 | 7 | market | לחץ גבוה | 32 | 25.0% | 25.0% | 0.0% |
| vta35_zscore_60 | 7 | market | רגוע | 236 | 48.3% | 56.0% | -7.7% |
| vta35_zscore_60 | 7 | market | רגיל | 252 | 40.1% | 51.2% | -11.1% |
| vta35_zscore_60 | 7 | volatility | זהירות | 84 | 50.0% | 47.1% | 2.9% |
| vta35_zscore_60 | 7 | volatility | לחץ גבוה | 32 | 43.8% | 43.8% | 0.0% |
| vta35_zscore_60 | 7 | volatility | רגוע | 273 | 48.4% | 42.9% | 5.4% |
| vta35_zscore_60 | 7 | volatility | רגיל | 283 | 44.2% | 43.2% | 1.0% |
| vta35_zscore_60 | 14 | market | זהירות | 78 | 39.7% | 37.0% | 2.8% |
| vta35_zscore_60 | 14 | market | לחץ גבוה | 32 | 21.9% | 21.9% | 0.0% |
| vta35_zscore_60 | 14 | market | רגוע | 236 | 59.3% | 62.8% | -3.5% |
| vta35_zscore_60 | 14 | market | רגיל | 249 | 46.6% | 52.2% | -5.6% |
| vta35_zscore_60 | 14 | volatility | זהירות | 81 | 51.9% | 49.8% | 2.1% |
| vta35_zscore_60 | 14 | volatility | לחץ גבוה | 32 | 40.6% | 40.6% | 0.0% |
| vta35_zscore_60 | 14 | volatility | רגוע | 272 | 43.8% | 40.1% | 3.6% |
| vta35_zscore_60 | 14 | volatility | רגיל | 280 | 46.4% | 43.0% | 3.4% |
| vta35_zscore_60 | 30 | market | זהירות | 74 | 17.6% | 16.5% | 1.1% |
| vta35_zscore_60 | 30 | market | לחץ גבוה | 32 | 15.6% | 15.6% | 0.0% |
| vta35_zscore_60 | 30 | market | רגוע | 232 | 69.0% | 66.0% | 3.0% |
| vta35_zscore_60 | 30 | market | רגיל | 244 | 52.5% | 53.4% | -0.9% |
| vta35_zscore_60 | 30 | volatility | זהירות | 76 | 47.4% | 46.2% | 1.1% |
| vta35_zscore_60 | 30 | volatility | לחץ גבוה | 32 | 31.2% | 31.2% | 0.0% |
| vta35_zscore_60 | 30 | volatility | רגוע | 267 | 44.9% | 39.7% | 5.3% |
| vta35_zscore_60 | 30 | volatility | רגיל | 274 | 42.3% | 42.0% | 0.3% |

## Indicator robustness by calendar year

| indicator | horizon | axis | year | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | 2,023 | 81 | 51.9% | 45.8% | 6.1% |
| atr_5_20_ratio | 3 | volatility | 2,024 | 245 | 37.1% | 42.8% | -5.7% |
| atr_5_20_ratio | 3 | volatility | 2,025 | 246 | 46.3% | 41.1% | 5.2% |
| atr_5_20_ratio | 3 | volatility | 2,026 | 143 | 53.8% | 43.5% | 10.3% |
| atr_5_20_ratio | 7 | volatility | 2,023 | 81 | 56.8% | 43.2% | 13.6% |
| atr_5_20_ratio | 7 | volatility | 2,024 | 245 | 35.5% | 41.6% | -6.1% |
| atr_5_20_ratio | 7 | volatility | 2,025 | 246 | 52.8% | 40.7% | 12.1% |
| atr_5_20_ratio | 7 | volatility | 2,026 | 139 | 46.0% | 42.9% | 3.1% |
| atr_5_20_ratio | 14 | volatility | 2,023 | 81 | 51.9% | 45.8% | 6.1% |
| atr_5_20_ratio | 14 | volatility | 2,024 | 245 | 47.3% | 42.1% | 5.2% |
| atr_5_20_ratio | 14 | volatility | 2,025 | 246 | 49.6% | 40.5% | 9.1% |
| atr_5_20_ratio | 14 | volatility | 2,026 | 132 | 47.0% | 43.2% | 3.8% |
| atr_5_20_ratio | 30 | volatility | 2,023 | 81 | 51.9% | 47.6% | 4.3% |
| atr_5_20_ratio | 30 | volatility | 2,024 | 245 | 46.1% | 41.3% | 4.8% |
| atr_5_20_ratio | 30 | volatility | 2,025 | 246 | 52.0% | 40.9% | 11.1% |
| atr_5_20_ratio | 30 | volatility | 2,026 | 116 | 50.9% | 44.1% | 6.8% |
| expected_move_3d_points | 3 | volatility | 2,023 | 81 | 39.5% | 30.0% | 9.5% |
| expected_move_3d_points | 3 | volatility | 2,024 | 245 | 26.9% | 23.9% | 3.1% |
| expected_move_3d_points | 3 | volatility | 2,025 | 246 | 38.6% | 33.6% | 5.0% |
| expected_move_3d_points | 3 | volatility | 2,026 | 143 | 43.4% | 33.1% | 10.2% |
| expected_move_3d_points | 7 | volatility | 2,023 | 81 | 43.2% | 30.4% | 12.8% |
| expected_move_3d_points | 7 | volatility | 2,024 | 245 | 26.9% | 25.1% | 1.8% |
| expected_move_3d_points | 7 | volatility | 2,025 | 246 | 41.5% | 32.1% | 9.4% |
| expected_move_3d_points | 7 | volatility | 2,026 | 139 | 49.6% | 32.9% | 16.8% |
| expected_move_3d_points | 14 | volatility | 2,023 | 81 | 44.4% | 32.5% | 11.9% |
| expected_move_3d_points | 14 | volatility | 2,024 | 245 | 30.6% | 24.6% | 6.0% |
| expected_move_3d_points | 14 | volatility | 2,025 | 246 | 43.1% | 30.8% | 12.3% |
| expected_move_3d_points | 14 | volatility | 2,026 | 132 | 52.3% | 32.9% | 19.4% |
| expected_move_3d_points | 30 | volatility | 2,023 | 81 | 46.9% | 33.0% | 13.9% |
| expected_move_3d_points | 30 | volatility | 2,024 | 245 | 29.0% | 25.5% | 3.5% |
| expected_move_3d_points | 30 | volatility | 2,025 | 246 | 39.4% | 30.1% | 9.3% |
| expected_move_3d_points | 30 | volatility | 2,026 | 116 | 56.0% | 34.0% | 22.0% |
| forecast_rv_3d | 3 | volatility | 2,023 | 81 | 39.5% | 30.0% | 9.5% |
| forecast_rv_3d | 3 | volatility | 2,024 | 245 | 26.9% | 23.9% | 3.1% |
| forecast_rv_3d | 3 | volatility | 2,025 | 246 | 38.6% | 33.6% | 5.0% |
| forecast_rv_3d | 3 | volatility | 2,026 | 143 | 43.4% | 33.1% | 10.2% |
| forecast_rv_3d | 7 | volatility | 2,023 | 81 | 43.2% | 30.4% | 12.8% |
| forecast_rv_3d | 7 | volatility | 2,024 | 245 | 26.9% | 25.1% | 1.8% |
| forecast_rv_3d | 7 | volatility | 2,025 | 246 | 41.5% | 32.1% | 9.4% |
| forecast_rv_3d | 7 | volatility | 2,026 | 139 | 49.6% | 32.9% | 16.8% |
| forecast_rv_3d | 14 | volatility | 2,023 | 81 | 44.4% | 32.5% | 11.9% |
| forecast_rv_3d | 14 | volatility | 2,024 | 245 | 30.6% | 24.6% | 6.0% |
| forecast_rv_3d | 14 | volatility | 2,025 | 246 | 43.1% | 30.8% | 12.3% |
| forecast_rv_3d | 14 | volatility | 2,026 | 132 | 52.3% | 32.9% | 19.4% |
| forecast_rv_3d | 30 | volatility | 2,023 | 81 | 46.9% | 33.0% | 13.9% |
| forecast_rv_3d | 30 | volatility | 2,024 | 245 | 29.0% | 25.5% | 3.5% |
| forecast_rv_3d | 30 | volatility | 2,025 | 246 | 39.4% | 30.1% | 9.3% |
| forecast_rv_3d | 30 | volatility | 2,026 | 116 | 56.0% | 34.0% | 22.0% |
| gap_share_20 | 3 | volatility | 2,023 | 81 | 29.6% | 31.6% | -2.0% |
| gap_share_20 | 3 | volatility | 2,024 | 245 | 35.1% | 32.9% | 2.2% |
| gap_share_20 | 3 | volatility | 2,025 | 246 | 30.9% | 35.5% | -4.6% |
| gap_share_20 | 3 | volatility | 2,026 | 143 | 35.7% | 35.4% | 0.2% |
| gap_share_20 | 7 | volatility | 2,023 | 81 | 35.8% | 32.0% | 3.8% |
| gap_share_20 | 7 | volatility | 2,024 | 245 | 35.5% | 33.0% | 2.5% |
| gap_share_20 | 7 | volatility | 2,025 | 246 | 27.2% | 34.8% | -7.5% |
| gap_share_20 | 7 | volatility | 2,026 | 139 | 36.0% | 32.5% | 3.4% |
| gap_share_20 | 14 | volatility | 2,023 | 81 | 19.8% | 31.4% | -11.7% |
| gap_share_20 | 14 | volatility | 2,024 | 245 | 31.8% | 33.0% | -1.2% |
| gap_share_20 | 14 | volatility | 2,025 | 246 | 26.0% | 34.1% | -8.1% |
| gap_share_20 | 14 | volatility | 2,026 | 132 | 29.5% | 31.7% | -2.2% |
| gap_share_20 | 30 | volatility | 2,023 | 81 | 23.5% | 31.1% | -7.6% |
| gap_share_20 | 30 | volatility | 2,024 | 245 | 26.9% | 33.2% | -6.2% |
| gap_share_20 | 30 | volatility | 2,025 | 246 | 20.3% | 34.0% | -13.6% |
| gap_share_20 | 30 | volatility | 2,026 | 116 | 22.4% | 36.6% | -14.2% |
| rv_20_60_ratio | 3 | volatility | 2,023 | 41 | 46.3% | 53.8% | -7.5% |
| rv_20_60_ratio | 3 | volatility | 2,024 | 245 | 40.8% | 44.8% | -3.9% |
| rv_20_60_ratio | 3 | volatility | 2,025 | 246 | 41.1% | 44.3% | -3.2% |
| rv_20_60_ratio | 3 | volatility | 2,026 | 143 | 32.9% | 41.9% | -9.1% |
| rv_20_60_ratio | 7 | volatility | 2,023 | 41 | 48.8% | 58.5% | -9.7% |
| rv_20_60_ratio | 7 | volatility | 2,024 | 245 | 33.1% | 43.1% | -10.0% |
| rv_20_60_ratio | 7 | volatility | 2,025 | 246 | 31.7% | 43.0% | -11.2% |
| rv_20_60_ratio | 7 | volatility | 2,026 | 139 | 23.7% | 41.3% | -17.6% |
| rv_20_60_ratio | 14 | volatility | 2,023 | 41 | 61.0% | 66.6% | -5.6% |
| rv_20_60_ratio | 14 | volatility | 2,024 | 245 | 35.1% | 43.4% | -8.3% |
| rv_20_60_ratio | 14 | volatility | 2,025 | 246 | 27.6% | 42.0% | -14.4% |
| rv_20_60_ratio | 14 | volatility | 2,026 | 132 | 12.9% | 41.9% | -29.0% |
| rv_20_60_ratio | 30 | volatility | 2,023 | 41 | 73.2% | 75.1% | -2.0% |
| rv_20_60_ratio | 30 | volatility | 2,024 | 245 | 30.2% | 42.1% | -11.9% |
| rv_20_60_ratio | 30 | volatility | 2,025 | 246 | 22.0% | 42.3% | -20.3% |
| rv_20_60_ratio | 30 | volatility | 2,026 | 116 | 9.5% | 39.5% | -30.0% |
| rv_acceleration | 3 | volatility | 2,023 | 81 | 53.1% | 43.5% | 9.6% |
| rv_acceleration | 3 | volatility | 2,024 | 245 | 42.0% | 44.6% | -2.6% |
| rv_acceleration | 3 | volatility | 2,025 | 246 | 49.6% | 47.5% | 2.1% |
| rv_acceleration | 3 | volatility | 2,026 | 143 | 52.4% | 48.2% | 4.2% |
| rv_acceleration | 7 | volatility | 2,023 | 81 | 63.0% | 41.7% | 21.3% |
| rv_acceleration | 7 | volatility | 2,024 | 245 | 33.5% | 43.0% | -9.6% |
| rv_acceleration | 7 | volatility | 2,025 | 246 | 41.9% | 44.0% | -2.1% |
| rv_acceleration | 7 | volatility | 2,026 | 139 | 43.9% | 45.5% | -1.6% |
| rv_acceleration | 14 | volatility | 2,023 | 81 | 56.8% | 41.2% | 15.6% |
| rv_acceleration | 14 | volatility | 2,024 | 245 | 44.9% | 43.4% | 1.5% |
| rv_acceleration | 14 | volatility | 2,025 | 246 | 43.5% | 41.2% | 2.3% |
| rv_acceleration | 14 | volatility | 2,026 | 132 | 43.2% | 44.5% | -1.3% |
| rv_acceleration | 30 | volatility | 2,023 | 81 | 59.3% | 41.8% | 17.5% |
| rv_acceleration | 30 | volatility | 2,024 | 245 | 40.8% | 42.3% | -1.5% |
| rv_acceleration | 30 | volatility | 2,025 | 246 | 43.9% | 40.7% | 3.2% |
| rv_acceleration | 30 | volatility | 2,026 | 116 | 49.1% | 45.6% | 3.5% |
| usdils_change_5d | 3 | market | 2,023 | 89 | 64.0% | 50.1% | 14.0% |
| usdils_change_5d | 3 | market | 2,024 | 202 | 45.5% | 49.5% | -3.9% |
| usdils_change_5d | 3 | market | 2,025 | 213 | 53.1% | 52.3% | 0.8% |
| usdils_change_5d | 3 | market | 2,026 | 126 | 46.8% | 50.4% | -3.6% |
| usdils_change_5d | 3 | volatility | 2,023 | 81 | 45.7% | 45.9% | -0.2% |
| usdils_change_5d | 3 | volatility | 2,024 | 245 | 43.7% | 39.7% | 4.0% |
| usdils_change_5d | 3 | volatility | 2,025 | 246 | 44.7% | 43.7% | 1.0% |
| usdils_change_5d | 3 | volatility | 2,026 | 143 | 50.3% | 44.5% | 5.9% |
| usdils_change_5d | 7 | market | 2,023 | 89 | 65.2% | 49.7% | 15.5% |
| usdils_change_5d | 7 | market | 2,024 | 202 | 45.5% | 49.4% | -3.8% |
| usdils_change_5d | 7 | market | 2,025 | 213 | 48.8% | 53.1% | -4.3% |
| usdils_change_5d | 7 | market | 2,026 | 123 | 41.5% | 50.4% | -8.9% |
| usdils_change_5d | 7 | volatility | 2,023 | 81 | 50.6% | 43.4% | 7.2% |
| usdils_change_5d | 7 | volatility | 2,024 | 245 | 44.5% | 38.9% | 5.5% |
| usdils_change_5d | 7 | volatility | 2,025 | 246 | 43.1% | 41.2% | 1.9% |
| usdils_change_5d | 7 | volatility | 2,026 | 139 | 49.6% | 42.8% | 6.9% |
| usdils_change_5d | 14 | market | 2,023 | 89 | 61.8% | 49.1% | 12.6% |
| usdils_change_5d | 14 | market | 2,024 | 202 | 48.5% | 48.8% | -0.3% |
| usdils_change_5d | 14 | market | 2,025 | 213 | 55.9% | 54.0% | 1.9% |
| usdils_change_5d | 14 | market | 2,026 | 116 | 54.3% | 51.1% | 3.2% |
| usdils_change_5d | 14 | volatility | 2,023 | 81 | 55.6% | 44.5% | 11.1% |
| usdils_change_5d | 14 | volatility | 2,024 | 245 | 46.9% | 39.4% | 7.6% |
| usdils_change_5d | 14 | volatility | 2,025 | 246 | 45.1% | 39.3% | 5.8% |
| usdils_change_5d | 14 | volatility | 2,026 | 132 | 46.2% | 42.0% | 4.2% |
| usdils_change_5d | 30 | market | 2,023 | 89 | 62.9% | 49.7% | 13.2% |
| usdils_change_5d | 30 | market | 2,024 | 202 | 47.0% | 47.7% | -0.6% |
| usdils_change_5d | 30 | market | 2,025 | 213 | 53.1% | 55.1% | -2.0% |
| usdils_change_5d | 30 | market | 2,026 | 101 | 43.6% | 50.3% | -6.7% |
| usdils_change_5d | 30 | volatility | 2,023 | 81 | 58.0% | 45.8% | 12.2% |
| usdils_change_5d | 30 | volatility | 2,024 | 245 | 47.8% | 38.9% | 8.9% |
| usdils_change_5d | 30 | volatility | 2,025 | 246 | 44.3% | 39.0% | 5.3% |
| usdils_change_5d | 30 | volatility | 2,026 | 116 | 38.8% | 43.0% | -4.3% |
| vix9d_vix_ratio | 3 | market | 2,023 | 72 | 56.9% | 56.3% | 0.7% |
| vix9d_vix_ratio | 3 | market | 2,024 | 209 | 58.4% | 56.9% | 1.4% |
| vix9d_vix_ratio | 3 | market | 2,025 | 225 | 64.9% | 62.2% | 2.6% |
| vix9d_vix_ratio | 3 | market | 2,026 | 124 | 54.0% | 52.4% | 1.6% |
| vix9d_vix_ratio | 3 | volatility | 2,023 | 81 | 35.8% | 38.2% | -2.4% |
| vix9d_vix_ratio | 3 | volatility | 2,024 | 245 | 50.2% | 47.4% | 2.8% |
| vix9d_vix_ratio | 3 | volatility | 2,025 | 246 | 48.8% | 51.5% | -2.7% |
| vix9d_vix_ratio | 3 | volatility | 2,026 | 143 | 55.9% | 54.7% | 1.2% |
| vix9d_vix_ratio | 7 | market | 2,023 | 72 | 55.6% | 55.2% | 0.3% |
| vix9d_vix_ratio | 7 | market | 2,024 | 209 | 57.9% | 57.8% | 0.1% |
| vix9d_vix_ratio | 7 | market | 2,025 | 225 | 63.6% | 62.6% | 1.0% |
| vix9d_vix_ratio | 7 | market | 2,026 | 120 | 56.7% | 53.1% | 3.5% |
| vix9d_vix_ratio | 7 | volatility | 2,023 | 81 | 35.8% | 36.7% | -0.9% |
| vix9d_vix_ratio | 7 | volatility | 2,024 | 245 | 46.5% | 45.2% | 1.3% |
| vix9d_vix_ratio | 7 | volatility | 2,025 | 246 | 39.8% | 42.8% | -3.0% |
| vix9d_vix_ratio | 7 | volatility | 2,026 | 139 | 46.0% | 45.0% | 1.1% |
| vix9d_vix_ratio | 14 | market | 2,023 | 72 | 58.3% | 59.4% | -1.0% |
| vix9d_vix_ratio | 14 | market | 2,024 | 209 | 54.5% | 62.3% | -7.7% |
| vix9d_vix_ratio | 14 | market | 2,025 | 225 | 68.9% | 68.1% | 0.7% |
| vix9d_vix_ratio | 14 | market | 2,026 | 114 | 60.5% | 57.1% | 3.4% |
| vix9d_vix_ratio | 14 | volatility | 2,023 | 81 | 49.4% | 42.3% | 7.1% |
| vix9d_vix_ratio | 14 | volatility | 2,024 | 245 | 50.2% | 45.2% | 5.0% |
| vix9d_vix_ratio | 14 | volatility | 2,025 | 246 | 36.6% | 35.7% | 0.9% |
| vix9d_vix_ratio | 14 | volatility | 2,026 | 132 | 39.4% | 40.4% | -1.0% |
| vix9d_vix_ratio | 30 | market | 2,023 | 72 | 50.0% | 51.0% | -1.0% |
| vix9d_vix_ratio | 30 | market | 2,024 | 209 | 70.3% | 72.6% | -2.3% |
| vix9d_vix_ratio | 30 | market | 2,025 | 225 | 70.7% | 73.1% | -2.4% |
| vix9d_vix_ratio | 30 | market | 2,026 | 98 | 43.9% | 49.3% | -5.4% |
| vix9d_vix_ratio | 30 | volatility | 2,023 | 81 | 51.9% | 44.6% | 7.3% |
| vix9d_vix_ratio | 30 | volatility | 2,024 | 245 | 43.3% | 43.5% | -0.2% |
| vix9d_vix_ratio | 30 | volatility | 2,025 | 246 | 28.0% | 33.2% | -5.1% |
| vix9d_vix_ratio | 30 | volatility | 2,026 | 116 | 37.1% | 44.4% | -7.3% |
| vix_curve_ratio | 3 | market | 2,023 | 98 | 51.0% | 50.0% | 1.0% |
| vix_curve_ratio | 3 | market | 2,024 | 237 | 57.8% | 58.5% | -0.7% |
| vix_curve_ratio | 3 | market | 2,025 | 239 | 63.2% | 61.9% | 1.2% |
| vix_curve_ratio | 3 | market | 2,026 | 136 | 52.9% | 53.1% | -0.1% |
| vix_curve_ratio | 3 | volatility | 2,023 | 81 | 59.3% | 56.8% | 2.4% |
| vix_curve_ratio | 3 | volatility | 2,024 | 245 | 59.2% | 55.8% | 3.4% |
| vix_curve_ratio | 3 | volatility | 2,025 | 246 | 52.4% | 54.9% | -2.5% |
| vix_curve_ratio | 3 | volatility | 2,026 | 143 | 62.2% | 61.1% | 1.1% |
| vix_curve_ratio | 7 | market | 2,023 | 98 | 55.1% | 54.0% | 1.1% |
| vix_curve_ratio | 7 | market | 2,024 | 237 | 55.3% | 58.5% | -3.2% |
| vix_curve_ratio | 7 | market | 2,025 | 239 | 62.3% | 64.4% | -2.1% |
| vix_curve_ratio | 7 | market | 2,026 | 132 | 56.1% | 54.4% | 1.6% |
| vix_curve_ratio | 7 | volatility | 2,023 | 81 | 53.1% | 51.2% | 1.9% |
| vix_curve_ratio | 7 | volatility | 2,024 | 245 | 55.5% | 52.3% | 3.2% |
| vix_curve_ratio | 7 | volatility | 2,025 | 246 | 41.9% | 45.0% | -3.1% |
| vix_curve_ratio | 7 | volatility | 2,026 | 139 | 52.5% | 49.3% | 3.2% |
| vix_curve_ratio | 14 | market | 2,023 | 98 | 60.2% | 59.0% | 1.2% |
| vix_curve_ratio | 14 | market | 2,024 | 237 | 63.7% | 67.2% | -3.5% |
| vix_curve_ratio | 14 | market | 2,025 | 239 | 70.7% | 69.4% | 1.3% |
| vix_curve_ratio | 14 | market | 2,026 | 125 | 57.6% | 56.9% | 0.7% |
| vix_curve_ratio | 14 | volatility | 2,023 | 81 | 65.4% | 62.8% | 2.7% |
| vix_curve_ratio | 14 | volatility | 2,024 | 245 | 55.9% | 52.4% | 3.5% |
| vix_curve_ratio | 14 | volatility | 2,025 | 246 | 35.8% | 37.0% | -1.2% |
| vix_curve_ratio | 14 | volatility | 2,026 | 132 | 43.2% | 43.6% | -0.5% |
| vix_curve_ratio | 30 | market | 2,023 | 98 | 54.1% | 53.0% | 1.1% |
| vix_curve_ratio | 30 | market | 2,024 | 237 | 80.6% | 81.6% | -1.0% |
| vix_curve_ratio | 30 | market | 2,025 | 239 | 72.4% | 74.3% | -1.9% |
| vix_curve_ratio | 30 | market | 2,026 | 109 | 46.8% | 51.1% | -4.3% |
| vix_curve_ratio | 30 | volatility | 2,023 | 81 | 71.6% | 68.5% | 3.1% |
| vix_curve_ratio | 30 | volatility | 2,024 | 245 | 51.0% | 49.6% | 1.4% |
| vix_curve_ratio | 30 | volatility | 2,025 | 246 | 28.9% | 34.2% | -5.3% |
| vix_curve_ratio | 30 | volatility | 2,026 | 116 | 41.4% | 49.4% | -8.0% |
| vix_vix3m_ratio | 3 | market | 2,023 | 101 | 51.5% | 51.5% | 0.0% |
| vix_vix3m_ratio | 3 | market | 2,024 | 227 | 56.8% | 58.6% | -1.8% |
| vix_vix3m_ratio | 3 | market | 2,025 | 230 | 63.5% | 64.0% | -0.5% |
| vix_vix3m_ratio | 3 | market | 2,026 | 132 | 53.0% | 53.6% | -0.6% |
| vix_vix3m_ratio | 3 | volatility | 2,023 | 81 | 59.3% | 59.3% | 0.0% |
| vix_vix3m_ratio | 3 | volatility | 2,024 | 245 | 55.5% | 54.7% | 0.8% |
| vix_vix3m_ratio | 3 | volatility | 2,025 | 246 | 53.3% | 53.9% | -0.7% |
| vix_vix3m_ratio | 3 | volatility | 2,026 | 143 | 62.2% | 61.4% | 0.8% |
| vix_vix3m_ratio | 7 | market | 2,023 | 101 | 53.5% | 53.5% | 0.0% |
| vix_vix3m_ratio | 7 | market | 2,024 | 227 | 56.8% | 57.8% | -1.0% |
| vix_vix3m_ratio | 7 | market | 2,025 | 230 | 62.6% | 65.4% | -2.8% |
| vix_vix3m_ratio | 7 | market | 2,026 | 128 | 53.9% | 54.5% | -0.6% |
| vix_vix3m_ratio | 7 | volatility | 2,023 | 81 | 53.1% | 53.1% | 0.0% |
| vix_vix3m_ratio | 7 | volatility | 2,024 | 245 | 53.1% | 51.3% | 1.8% |
| vix_vix3m_ratio | 7 | volatility | 2,025 | 246 | 39.4% | 43.5% | -4.1% |
| vix_vix3m_ratio | 7 | volatility | 2,026 | 139 | 51.1% | 48.6% | 2.5% |
| vix_vix3m_ratio | 14 | market | 2,023 | 101 | 58.4% | 58.4% | 0.0% |
| vix_vix3m_ratio | 14 | market | 2,024 | 227 | 66.5% | 67.9% | -1.4% |
| vix_vix3m_ratio | 14 | market | 2,025 | 230 | 73.0% | 71.2% | 1.9% |
| vix_vix3m_ratio | 14 | market | 2,026 | 121 | 57.0% | 57.5% | -0.4% |
| vix_vix3m_ratio | 14 | volatility | 2,023 | 81 | 65.4% | 65.4% | 0.0% |
| vix_vix3m_ratio | 14 | volatility | 2,024 | 245 | 51.8% | 51.2% | 0.7% |
| vix_vix3m_ratio | 14 | volatility | 2,025 | 246 | 32.9% | 35.0% | -2.1% |
| vix_vix3m_ratio | 14 | volatility | 2,026 | 132 | 39.4% | 42.2% | -2.8% |
| vix_vix3m_ratio | 30 | market | 2,023 | 101 | 52.5% | 52.5% | 0.0% |
| vix_vix3m_ratio | 30 | market | 2,024 | 227 | 84.6% | 85.2% | -0.6% |
| vix_vix3m_ratio | 30 | market | 2,025 | 230 | 75.7% | 76.2% | -0.6% |
| vix_vix3m_ratio | 30 | market | 2,026 | 105 | 49.5% | 50.4% | -0.9% |
| vix_vix3m_ratio | 30 | volatility | 2,023 | 81 | 71.6% | 71.6% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 2,024 | 245 | 50.2% | 48.4% | 1.8% |
| vix_vix3m_ratio | 30 | volatility | 2,025 | 246 | 28.5% | 31.9% | -3.4% |
| vix_vix3m_ratio | 30 | volatility | 2,026 | 116 | 44.8% | 48.6% | -3.7% |
| vrp_spread | 3 | volatility | 2,023 | 81 | 71.6% | 45.9% | 25.7% |
| vrp_spread | 3 | volatility | 2,024 | 245 | 41.6% | 35.2% | 6.4% |
| vrp_spread | 3 | volatility | 2,025 | 246 | 56.1% | 42.9% | 13.2% |
| vrp_spread | 3 | volatility | 2,026 | 143 | 50.3% | 40.4% | 9.9% |
| vrp_spread | 7 | volatility | 2,023 | 81 | 77.8% | 43.5% | 34.2% |
| vrp_spread | 7 | volatility | 2,024 | 245 | 44.1% | 35.6% | 8.5% |
| vrp_spread | 7 | volatility | 2,025 | 246 | 65.0% | 43.2% | 21.8% |
| vrp_spread | 7 | volatility | 2,026 | 139 | 56.8% | 41.8% | 15.0% |
| vrp_spread | 14 | volatility | 2,023 | 81 | 76.5% | 43.9% | 32.7% |
| vrp_spread | 14 | volatility | 2,024 | 245 | 46.5% | 36.8% | 9.8% |
| vrp_spread | 14 | volatility | 2,025 | 246 | 62.6% | 43.6% | 19.0% |
| vrp_spread | 14 | volatility | 2,026 | 132 | 57.6% | 43.1% | 14.4% |
| vrp_spread | 30 | volatility | 2,023 | 81 | 71.6% | 44.9% | 26.7% |
| vrp_spread | 30 | volatility | 2,024 | 245 | 47.8% | 37.4% | 10.3% |
| vrp_spread | 30 | volatility | 2,025 | 246 | 62.6% | 44.5% | 18.1% |
| vrp_spread | 30 | volatility | 2,026 | 116 | 69.0% | 42.2% | 26.8% |
| vta35 | 3 | market | 2,023 | 38 | 60.5% | 61.6% | -1.1% |
| vta35 | 3 | market | 2,024 | 221 | 49.3% | 53.0% | -3.7% |
| vta35 | 3 | market | 2,025 | 212 | 49.5% | 50.6% | -1.0% |
| vta35 | 3 | market | 2,026 | 132 | 43.9% | 49.4% | -5.5% |
| vta35 | 3 | volatility | 2,023 | 42 | 40.5% | 52.0% | -11.6% |
| vta35 | 3 | volatility | 2,024 | 245 | 47.8% | 47.7% | 0.0% |
| vta35 | 3 | volatility | 2,025 | 246 | 50.8% | 42.3% | 8.5% |
| vta35 | 3 | volatility | 2,026 | 143 | 46.2% | 38.3% | 7.8% |
| vta35 | 7 | market | 2,023 | 38 | 68.4% | 66.6% | 1.8% |
| vta35 | 7 | market | 2,024 | 221 | 43.4% | 52.8% | -9.4% |
| vta35 | 7 | market | 2,025 | 212 | 42.0% | 50.7% | -8.7% |
| vta35 | 7 | market | 2,026 | 130 | 30.8% | 47.1% | -16.4% |
| vta35 | 7 | volatility | 2,023 | 42 | 42.9% | 55.6% | -12.8% |
| vta35 | 7 | volatility | 2,024 | 245 | 45.3% | 45.6% | -0.3% |
| vta35 | 7 | volatility | 2,025 | 246 | 49.6% | 41.2% | 8.4% |
| vta35 | 7 | volatility | 2,026 | 139 | 44.6% | 42.3% | 2.3% |
| vta35 | 14 | market | 2,023 | 38 | 63.2% | 69.9% | -6.8% |
| vta35 | 14 | market | 2,024 | 221 | 56.1% | 57.9% | -1.8% |
| vta35 | 14 | market | 2,025 | 212 | 42.5% | 51.0% | -8.5% |
| vta35 | 14 | market | 2,026 | 124 | 45.2% | 45.4% | -0.3% |
| vta35 | 14 | volatility | 2,023 | 42 | 54.8% | 62.1% | -7.3% |
| vta35 | 14 | volatility | 2,024 | 245 | 44.9% | 45.9% | -1.0% |
| vta35 | 14 | volatility | 2,025 | 246 | 47.2% | 40.4% | 6.8% |
| vta35 | 14 | volatility | 2,026 | 132 | 41.7% | 45.6% | -3.9% |
| vta35 | 30 | market | 2,023 | 38 | 55.3% | 65.0% | -9.7% |
| vta35 | 30 | market | 2,024 | 221 | 66.1% | 64.9% | 1.2% |
| vta35 | 30 | market | 2,025 | 212 | 52.4% | 51.2% | 1.2% |
| vta35 | 30 | market | 2,026 | 111 | 25.2% | 47.6% | -22.4% |
| vta35 | 30 | volatility | 2,023 | 42 | 66.7% | 69.2% | -2.6% |
| vta35 | 30 | volatility | 2,024 | 245 | 42.4% | 44.3% | -1.9% |
| vta35 | 30 | volatility | 2,025 | 246 | 41.1% | 40.6% | 0.5% |
| vta35 | 30 | volatility | 2,026 | 116 | 42.2% | 43.3% | -1.0% |
| vta35_change_5d | 3 | market | 2,023 | 93 | 41.9% | 50.6% | -8.7% |
| vta35_change_5d | 3 | market | 2,024 | 226 | 57.1% | 50.2% | 6.8% |
| vta35_change_5d | 3 | market | 2,025 | 225 | 50.7% | 50.9% | -0.2% |
| vta35_change_5d | 3 | market | 2,026 | 136 | 44.1% | 50.0% | -5.8% |
| vta35_change_5d | 3 | volatility | 2,023 | 81 | 43.2% | 50.5% | -7.3% |
| vta35_change_5d | 3 | volatility | 2,024 | 245 | 43.7% | 44.8% | -1.2% |
| vta35_change_5d | 3 | volatility | 2,025 | 246 | 56.5% | 44.8% | 11.7% |
| vta35_change_5d | 3 | volatility | 2,026 | 143 | 45.5% | 46.1% | -0.6% |
| vta35_change_5d | 7 | market | 2,023 | 93 | 44.1% | 51.1% | -7.0% |
| vta35_change_5d | 7 | market | 2,024 | 226 | 49.1% | 50.3% | -1.1% |
| vta35_change_5d | 7 | market | 2,025 | 225 | 52.0% | 51.1% | 0.9% |
| vta35_change_5d | 7 | market | 2,026 | 133 | 36.1% | 50.0% | -13.9% |
| vta35_change_5d | 7 | volatility | 2,023 | 81 | 49.4% | 47.1% | 2.3% |
| vta35_change_5d | 7 | volatility | 2,024 | 245 | 45.7% | 43.4% | 2.3% |
| vta35_change_5d | 7 | volatility | 2,025 | 246 | 58.1% | 43.3% | 14.9% |
| vta35_change_5d | 7 | volatility | 2,026 | 139 | 47.5% | 45.3% | 2.2% |
| vta35_change_5d | 14 | market | 2,023 | 93 | 52.7% | 52.5% | 0.1% |
| vta35_change_5d | 14 | market | 2,024 | 226 | 50.0% | 50.5% | -0.5% |
| vta35_change_5d | 14 | market | 2,025 | 225 | 49.3% | 51.6% | -2.2% |
| vta35_change_5d | 14 | market | 2,026 | 126 | 56.3% | 50.0% | 6.3% |
| vta35_change_5d | 14 | volatility | 2,023 | 81 | 50.6% | 49.3% | 1.3% |
| vta35_change_5d | 14 | volatility | 2,024 | 245 | 48.2% | 44.0% | 4.2% |
| vta35_change_5d | 14 | volatility | 2,025 | 246 | 56.5% | 42.1% | 14.4% |
| vta35_change_5d | 14 | volatility | 2,026 | 132 | 47.0% | 45.4% | 1.5% |
| vta35_change_5d | 30 | market | 2,023 | 93 | 48.4% | 51.1% | -2.7% |
| vta35_change_5d | 30 | market | 2,024 | 226 | 57.1% | 51.0% | 6.1% |
| vta35_change_5d | 30 | market | 2,025 | 225 | 53.8% | 51.9% | 1.9% |
| vta35_change_5d | 30 | market | 2,026 | 113 | 49.6% | 49.8% | -0.3% |
| vta35_change_5d | 30 | volatility | 2,023 | 81 | 51.9% | 51.4% | 0.5% |
| vta35_change_5d | 30 | volatility | 2,024 | 245 | 47.3% | 43.0% | 4.4% |
| vta35_change_5d | 30 | volatility | 2,025 | 246 | 50.8% | 42.3% | 8.5% |
| vta35_change_5d | 30 | volatility | 2,026 | 116 | 44.8% | 46.1% | -1.2% |
| vta35_zscore_60 | 3 | market | 2,023 | 38 | 60.5% | 61.6% | -1.1% |
| vta35_zscore_60 | 3 | market | 2,024 | 221 | 49.3% | 53.0% | -3.7% |
| vta35_zscore_60 | 3 | market | 2,025 | 212 | 49.5% | 50.6% | -1.0% |
| vta35_zscore_60 | 3 | market | 2,026 | 132 | 43.9% | 49.4% | -5.5% |
| vta35_zscore_60 | 3 | volatility | 2,023 | 42 | 40.5% | 52.0% | -11.6% |
| vta35_zscore_60 | 3 | volatility | 2,024 | 245 | 47.8% | 47.7% | 0.0% |
| vta35_zscore_60 | 3 | volatility | 2,025 | 246 | 50.8% | 42.3% | 8.5% |
| vta35_zscore_60 | 3 | volatility | 2,026 | 143 | 46.2% | 38.3% | 7.8% |
| vta35_zscore_60 | 7 | market | 2,023 | 38 | 68.4% | 66.6% | 1.8% |
| vta35_zscore_60 | 7 | market | 2,024 | 221 | 43.4% | 52.8% | -9.4% |
| vta35_zscore_60 | 7 | market | 2,025 | 212 | 42.0% | 50.7% | -8.7% |
| vta35_zscore_60 | 7 | market | 2,026 | 130 | 30.8% | 47.1% | -16.4% |
| vta35_zscore_60 | 7 | volatility | 2,023 | 42 | 42.9% | 55.6% | -12.8% |
| vta35_zscore_60 | 7 | volatility | 2,024 | 245 | 45.3% | 45.6% | -0.3% |
| vta35_zscore_60 | 7 | volatility | 2,025 | 246 | 49.6% | 41.2% | 8.4% |
| vta35_zscore_60 | 7 | volatility | 2,026 | 139 | 44.6% | 42.3% | 2.3% |
| vta35_zscore_60 | 14 | market | 2,023 | 38 | 63.2% | 69.9% | -6.8% |
| vta35_zscore_60 | 14 | market | 2,024 | 221 | 56.1% | 57.9% | -1.8% |
| vta35_zscore_60 | 14 | market | 2,025 | 212 | 42.5% | 51.0% | -8.5% |
| vta35_zscore_60 | 14 | market | 2,026 | 124 | 45.2% | 45.4% | -0.3% |
| vta35_zscore_60 | 14 | volatility | 2,023 | 42 | 54.8% | 62.1% | -7.3% |
| vta35_zscore_60 | 14 | volatility | 2,024 | 245 | 44.9% | 45.9% | -1.0% |
| vta35_zscore_60 | 14 | volatility | 2,025 | 246 | 47.2% | 40.4% | 6.8% |
| vta35_zscore_60 | 14 | volatility | 2,026 | 132 | 41.7% | 45.6% | -3.9% |
| vta35_zscore_60 | 30 | market | 2,023 | 38 | 55.3% | 65.0% | -9.7% |
| vta35_zscore_60 | 30 | market | 2,024 | 221 | 66.1% | 64.9% | 1.2% |
| vta35_zscore_60 | 30 | market | 2,025 | 212 | 52.4% | 51.2% | 1.2% |
| vta35_zscore_60 | 30 | market | 2,026 | 111 | 25.2% | 47.6% | -22.4% |
| vta35_zscore_60 | 30 | volatility | 2,023 | 42 | 66.7% | 69.2% | -2.6% |
| vta35_zscore_60 | 30 | volatility | 2,024 | 245 | 42.4% | 44.3% | -1.9% |
| vta35_zscore_60 | 30 | volatility | 2,025 | 246 | 41.1% | 40.6% | 0.5% |
| vta35_zscore_60 | 30 | volatility | 2,026 | 116 | 42.2% | 43.3% | -1.0% |

## Every strategy family: selected-rule performance versus unconditional baseline

| strategy | horizon | available_days | selected_n | selection_rate | successes | success_rate | unconditional_baseline | uplift | adjusted_success_rate | ci_low | ci_high | p_value | strength | mean_scenario_score | median_normalized_move | nonoverlap_n_min | nonoverlap_success_rate | positive_years | tested_years | positive_regimes | tested_regimes | sample_quality | limitation | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bear Call Spread | 3 | 730 | 0 | 0.0% | 0 | — | 58.8% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bear Call Spread | 7 | 726 | 0 | 0.0% | 0 | — | 57.3% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bear Call Spread | 14 | 719 | 0 | 0.0% | 0 | — | 50.5% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bear Call Spread | 30 | 703 | 0 | 0.0% | 0 | — | 42.7% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bear Put Spread | 3 | 730 | 75 | 10.3% | 25 | 33.3% | 40.7% | -7.4% | 34.9% | 23.7% | 44.6% | 0.9025 | 1 | -0.4078 | 0.4694 | 23 | 33.1% | 1 | 4 | 1 | 4 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| Bear Put Spread | 7 | 726 | 74 | 10.2% | 29 | 39.2% | 38.3% | 0.9% | 39.0% | 28.9% | 50.6% | 0.4369 | 1 | -0.2917 | 0.3051 | 7 | 38.7% | 2 | 4 | 2 | 4 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| Bear Put Spread | 14 | 719 | 72 | 10.0% | 29 | 40.3% | 30.7% | 9.5% | 38.2% | 29.7% | 51.8% | 0.0397 | 4 | -0.1886 | 0.2483 | 2 | 44.6% | 3 | 4 | 3 | 4 | נמוכה | market-scenario proxy; no option P&L | 0.6347 |
| Bear Put Spread | 30 | 703 | 71 | 10.1% | 27 | 38.0% | 24.3% | 13.7% | 35.0% | 27.6% | 49.7% | 0.0036 | 6 | -0.4860 | 0.4759 | 1 | 43.3% | 3 | 4 | 4 | 4 | נמוכה | market-scenario proxy; no option P&L | 0.1139 |
| Bull Call Spread | 3 | 730 | 195 | 26.7% | 113 | 57.9% | 59.3% | -1.4% | 58.1% | 50.9% | 64.7% | 0.6511 | 1 | 0.1204 | 0.1863 | 63 | 57.9% | 1 | 4 | 1 | 4 | בינונית | market-scenario proxy; no option P&L | 0.9785 |
| Bull Call Spread | 7 | 726 | 195 | 26.9% | 123 | 63.1% | 61.7% | 1.4% | 62.9% | 56.1% | 69.5% | 0.3471 | 2 | 0.2157 | 0.3238 | 22 | 63.5% | 1 | 4 | 3 | 4 | בינונית | market-scenario proxy; no option P&L | 0.9785 |
| Bull Call Spread | 14 | 719 | 194 | 27.0% | 130 | 67.0% | 69.3% | -2.3% | 67.2% | 60.1% | 73.2% | 0.7517 | 1 | 0.4264 | 0.6647 | 5 | 66.1% | 1 | 4 | 2 | 4 | בינונית | market-scenario proxy; no option P&L | 0.9785 |
| Bull Call Spread | 30 | 703 | 194 | 27.6% | 145 | 74.7% | 75.7% | -0.9% | 74.8% | 68.2% | 80.3% | 0.6191 | 1 | 0.7111 | 0.6604 | 3 | 74.8% | 1 | 4 | 3 | 4 | בינונית | market-scenario proxy; no option P&L | 0.9785 |
| Bull Put Spread | 3 | 730 | 0 | 0.0% | 0 | — | 76.0% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bull Put Spread | 7 | 726 | 0 | 0.0% | 0 | — | 79.2% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bull Put Spread | 14 | 719 | 0 | 0.0% | 0 | — | 84.7% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Bull Put Spread | 30 | 703 | 0 | 0.0% | 0 | — | 89.5% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Calendar / Diagonal | 3 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 7 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 14 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 30 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Call Ratio Backspread 1×2 | 3 | 730 | 6 | 0.8% | 0 | 0.0% | 21.4% | -21.4% | 16.4% | 0.0% | 39.0% | 0.8992 | 1 | -1.8507 | -1.0956 | 1 | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Call Ratio Backspread 1×2 | 7 | 726 | 6 | 0.8% | 0 | 0.0% | 25.2% | -25.2% | 19.4% | 0.0% | 39.0% | 0.9225 | 1 | -1.7229 | -0.4958 | 1 | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Call Ratio Backspread 1×2 | 14 | 719 | 6 | 0.8% | 0 | 0.0% | 28.9% | -28.9% | 22.3% | 0.0% | 39.0% | 0.9409 | 1 | -1.0129 | -0.1308 | 1 | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Call Ratio Backspread 1×2 | 30 | 703 | 6 | 0.9% | 0 | 0.0% | 38.3% | -38.3% | 29.4% | 0.0% | 39.0% | 0.9731 | 1 | -0.8869 | -0.0114 | 1 | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Iron Butterfly | 3 | 730 | 0 | 0.0% | 0 | — | 34.8% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 7 | 726 | 0 | 0.0% | 0 | — | 36.5% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 14 | 719 | 0 | 0.0% | 0 | — | 35.2% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 30 | 703 | 0 | 0.0% | 0 | — | 32.1% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Condor | 3 | 730 | 0 | 0.0% | 0 | — | 65.8% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Condor | 7 | 726 | 0 | 0.0% | 0 | — | 65.7% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Condor | 14 | 719 | 0 | 0.0% | 0 | — | 64.5% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Condor | 30 | 703 | 0 | 0.0% | 0 | — | 55.0% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Long Butterfly / Condor קנוי | 3 | 730 | 32 | 4.4% | 13 | 40.6% | 34.8% | 5.8% | 38.4% | 25.5% | 57.7% | 0.2443 | 2 | -0.3713 | 0.1387 | 8 | 42.7% | 3 | 4 | 1 | 2 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| Long Butterfly / Condor קנוי | 7 | 726 | 31 | 4.3% | 11 | 35.5% | 36.5% | -1.0% | 35.9% | 21.1% | 53.1% | 0.5468 | 1 | -0.3526 | 0.0363 | 1 | 37.6% | 2 | 3 | 1 | 2 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| Long Butterfly / Condor קנוי | 14 | 719 | 31 | 4.3% | 9 | 29.0% | 35.2% | -6.2% | 31.4% | 16.1% | 46.6% | 0.7635 | 1 | -0.3355 | 0.6871 | 1 | 36.4% | 1 | 3 | 1 | 2 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| Long Butterfly / Condor קנוי | 30 | 703 | 28 | 4.0% | 4 | 14.3% | 32.1% | -17.9% | 21.7% | 5.7% | 31.5% | 0.9785 | 1 | -0.5641 | 1.0378 | 1 | 13.9% | 0 | 3 | 0 | 2 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Long Straddle / Strangle | 3 | 730 | 5 | 0.7% | 0 | 0.0% | 34.2% | -34.2% | 27.4% | 0.0% | 43.4% | 0.9467 | 1 | -0.6458 | -0.0464 | 1 | 0.0% | 0 | 1 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Long Straddle / Strangle | 7 | 726 | 5 | 0.7% | 0 | 0.0% | 34.3% | -34.3% | 27.4% | 0.0% | 43.4% | 0.9469 | 1 | -0.2938 | 0.7420 | 1 | 0.0% | 0 | 1 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Long Straddle / Strangle | 14 | 719 | 5 | 0.7% | 1 | 20.0% | 35.5% | -15.5% | 32.4% | 3.6% | 62.4% | 0.7651 | 1 | -0.4170 | 0.4722 | 1 | 20.0% | 0 | 1 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Long Straddle / Strangle | 30 | 703 | 5 | 0.7% | 1 | 20.0% | 45.0% | -25.0% | 40.0% | 3.6% | 62.4% | 0.8690 | 1 | -0.4750 | 0.1200 | 1 | 12.5% | 0 | 1 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Put Ratio Backspread 1×2 | 3 | 730 | 23 | 3.2% | 2 | 8.7% | 12.9% | -4.2% | 10.6% | 2.4% | 26.8% | 0.7253 | 1 | -1.5089 | 0.7226 | 6 | 7.9% | 1 | 2 | 0 | 2 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Put Ratio Backspread 1×2 | 7 | 726 | 23 | 3.2% | 2 | 8.7% | 9.1% | -0.4% | 8.9% | 2.4% | 26.8% | 0.5263 | 1 | -1.5892 | 0.4695 | 1 | 5.2% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Put Ratio Backspread 1×2 | 14 | 719 | 23 | 3.2% | 1 | 4.3% | 6.5% | -2.2% | 5.4% | 0.8% | 21.0% | 0.6645 | 1 | -1.5952 | 0.8635 | 1 | 4.2% | 0 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| Put Ratio Backspread 1×2 | 30 | 703 | 23 | 3.3% | 1 | 4.3% | 6.7% | -2.3% | 5.4% | 0.8% | 21.0% | 0.6732 | 1 | -1.6762 | 0.7341 | 1 | 5.0% | 0 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 730 | 286 | 39.2% | 107 | 37.4% | 37.9% | -0.5% | 37.4% | 32.0% | 43.2% | 0.5736 | 1 | -0.3657 | 0.2446 | 94 | 37.4% | 1 | 4 | 0 | 3 | גבוהה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 726 | 286 | 39.4% | 92 | 32.2% | 36.5% | -4.3% | 32.5% | 27.0% | 37.8% | 0.9360 | 1 | -0.3161 | 0.3299 | 34 | 32.4% | 1 | 4 | 1 | 3 | גבוהה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 719 | 283 | 39.4% | 116 | 41.0% | 40.3% | 0.7% | 40.9% | 35.4% | 46.8% | 0.4111 | 1 | -0.2480 | 0.4657 | 14 | 41.8% | 2 | 4 | 1 | 3 | גבוהה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 703 | 282 | 40.1% | 98 | 34.8% | 37.4% | -2.7% | 34.9% | 29.4% | 40.5% | 0.8220 | 1 | -0.4190 | 0.7203 | 7 | 35.1% | 1 | 4 | 1 | 3 | גבוהה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 730 | 56 | 7.7% | 19 | 33.9% | 27.8% | 6.1% | 32.3% | 22.9% | 47.0% | 0.1533 | 3 | -0.4138 | 0.2675 | 17 | 33.4% | 3 | 4 | 3 | 3 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 726 | 55 | 7.6% | 21 | 38.2% | 29.2% | 9.0% | 35.8% | 26.5% | 51.4% | 0.0715 | 3 | -0.3231 | 0.1148 | 5 | 40.6% | 3 | 4 | 3 | 3 | נמוכה | market-scenario proxy; no option P&L | 0.7625 |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 719 | 55 | 7.6% | 13 | 23.6% | 24.2% | -0.6% | 23.8% | 14.4% | 36.3% | 0.5389 | 1 | -0.5095 | 0.4307 | 2 | 22.2% | 2 | 4 | 2 | 3 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 703 | 44 | 6.3% | 5 | 11.4% | 17.6% | -6.3% | 13.3% | 5.0% | 24.0% | 0.8626 | 1 | -1.0403 | 0.5358 | 1 | 11.4% | 0 | 3 | 1 | 3 | נמוכה | market-scenario proxy; no option P&L | 0.9785 |
| פרפר הפוך / Long Iron Condor | 3 | 730 | 0 | 0.0% | 0 | — | 34.2% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 7 | 726 | 0 | 0.0% | 0 | — | 34.3% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 14 | 719 | 0 | 0.0% | 0 | — | 35.5% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 30 | 703 | 0 | 0.0% | 0 | — | 45.0% | — | — | — | — | — | 1 | — | — | 0 | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |

## Strategy scenario sensitivity to 0.75x / 1.00x / 1.25x volatility bands

| strategy | horizon | band_multiplier | selected_n | success_rate |
| --- | --- | --- | --- | --- |
| Bear Put Spread | 3 | 0.7500 | 75 | 33.3% |
| Bear Put Spread | 3 | 1.0000 | 75 | 33.3% |
| Bear Put Spread | 3 | 1.2500 | 75 | 33.3% |
| Bear Put Spread | 7 | 0.7500 | 74 | 39.2% |
| Bear Put Spread | 7 | 1.0000 | 74 | 39.2% |
| Bear Put Spread | 7 | 1.2500 | 74 | 39.2% |
| Bear Put Spread | 14 | 0.7500 | 72 | 40.3% |
| Bear Put Spread | 14 | 1.0000 | 72 | 40.3% |
| Bear Put Spread | 14 | 1.2500 | 72 | 40.3% |
| Bear Put Spread | 30 | 0.7500 | 71 | 38.0% |
| Bear Put Spread | 30 | 1.0000 | 71 | 38.0% |
| Bear Put Spread | 30 | 1.2500 | 71 | 38.0% |
| Bull Call Spread | 3 | 0.7500 | 195 | 57.9% |
| Bull Call Spread | 3 | 1.0000 | 195 | 57.9% |
| Bull Call Spread | 3 | 1.2500 | 195 | 57.9% |
| Bull Call Spread | 7 | 0.7500 | 195 | 63.1% |
| Bull Call Spread | 7 | 1.0000 | 195 | 63.1% |
| Bull Call Spread | 7 | 1.2500 | 195 | 63.1% |
| Bull Call Spread | 14 | 0.7500 | 194 | 67.0% |
| Bull Call Spread | 14 | 1.0000 | 194 | 67.0% |
| Bull Call Spread | 14 | 1.2500 | 194 | 67.0% |
| Bull Call Spread | 30 | 0.7500 | 194 | 74.7% |
| Bull Call Spread | 30 | 1.0000 | 194 | 74.7% |
| Bull Call Spread | 30 | 1.2500 | 194 | 74.7% |
| Call Ratio Backspread 1×2 | 3 | 0.7500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 3 | 1.0000 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 3 | 1.2500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 0.7500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 1.0000 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 1.2500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 14 | 0.7500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 14 | 1.0000 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 14 | 1.2500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 30 | 0.7500 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 30 | 1.0000 | 6 | 0.0% |
| Call Ratio Backspread 1×2 | 30 | 1.2500 | 6 | 0.0% |
| Long Butterfly / Condor קנוי | 3 | 0.7500 | 32 | 34.4% |
| Long Butterfly / Condor קנוי | 3 | 1.0000 | 32 | 40.6% |
| Long Butterfly / Condor קנוי | 3 | 1.2500 | 32 | 40.6% |
| Long Butterfly / Condor קנוי | 7 | 0.7500 | 31 | 32.3% |
| Long Butterfly / Condor קנוי | 7 | 1.0000 | 31 | 35.5% |
| Long Butterfly / Condor קנוי | 7 | 1.2500 | 31 | 41.9% |
| Long Butterfly / Condor קנוי | 14 | 0.7500 | 31 | 19.4% |
| Long Butterfly / Condor קנוי | 14 | 1.0000 | 31 | 29.0% |
| Long Butterfly / Condor קנוי | 14 | 1.2500 | 31 | 35.5% |
| Long Butterfly / Condor קנוי | 30 | 0.7500 | 28 | 7.1% |
| Long Butterfly / Condor קנוי | 30 | 1.0000 | 28 | 14.3% |
| Long Butterfly / Condor קנוי | 30 | 1.2500 | 28 | 21.4% |
| Long Straddle / Strangle | 3 | 0.7500 | 5 | 0.0% |
| Long Straddle / Strangle | 3 | 1.0000 | 5 | 0.0% |
| Long Straddle / Strangle | 3 | 1.2500 | 5 | 0.0% |
| Long Straddle / Strangle | 7 | 0.7500 | 5 | 40.0% |
| Long Straddle / Strangle | 7 | 1.0000 | 5 | 0.0% |
| Long Straddle / Strangle | 7 | 1.2500 | 5 | 0.0% |
| Long Straddle / Strangle | 14 | 0.7500 | 5 | 20.0% |
| Long Straddle / Strangle | 14 | 1.0000 | 5 | 20.0% |
| Long Straddle / Strangle | 14 | 1.2500 | 5 | 20.0% |
| Long Straddle / Strangle | 30 | 0.7500 | 5 | 40.0% |
| Long Straddle / Strangle | 30 | 1.0000 | 5 | 20.0% |
| Long Straddle / Strangle | 30 | 1.2500 | 5 | 20.0% |
| Put Ratio Backspread 1×2 | 3 | 0.7500 | 23 | 13.0% |
| Put Ratio Backspread 1×2 | 3 | 1.0000 | 23 | 8.7% |
| Put Ratio Backspread 1×2 | 3 | 1.2500 | 23 | 4.3% |
| Put Ratio Backspread 1×2 | 7 | 0.7500 | 23 | 8.7% |
| Put Ratio Backspread 1×2 | 7 | 1.0000 | 23 | 8.7% |
| Put Ratio Backspread 1×2 | 7 | 1.2500 | 23 | 0.0% |
| Put Ratio Backspread 1×2 | 14 | 0.7500 | 23 | 8.7% |
| Put Ratio Backspread 1×2 | 14 | 1.0000 | 23 | 4.3% |
| Put Ratio Backspread 1×2 | 14 | 1.2500 | 23 | 4.3% |
| Put Ratio Backspread 1×2 | 30 | 0.7500 | 23 | 4.3% |
| Put Ratio Backspread 1×2 | 30 | 1.0000 | 23 | 4.3% |
| Put Ratio Backspread 1×2 | 30 | 1.2500 | 23 | 4.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 0.7500 | 286 | 27.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 1.0000 | 286 | 37.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 1.2500 | 286 | 43.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 0.7500 | 286 | 23.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 1.0000 | 286 | 32.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 1.2500 | 286 | 40.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 0.7500 | 283 | 30.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 1.0000 | 283 | 41.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 1.2500 | 283 | 48.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 0.7500 | 282 | 26.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 1.0000 | 282 | 34.8% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 1.2500 | 282 | 42.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 0.7500 | 56 | 30.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 1.0000 | 56 | 33.9% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 1.2500 | 56 | 35.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 0.7500 | 55 | 34.5% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 1.0000 | 55 | 38.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 1.2500 | 55 | 38.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 0.7500 | 55 | 23.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 1.0000 | 55 | 23.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 1.2500 | 55 | 23.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 0.7500 | 44 | 9.1% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 1.0000 | 44 | 11.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 1.2500 | 44 | 11.4% |

## Strategy robustness by market regime

| strategy | horizon | regime | selected_n | success_rate | unconditional_baseline | uplift |
| --- | --- | --- | --- | --- | --- | --- |
| Bear Put Spread | 3 | זהירות | 23 | 30.4% | 46.5% | -16.0% |
| Bear Put Spread | 3 | לחץ גבוה | 9 | 44.4% | 38.5% | 6.0% |
| Bear Put Spread | 3 | רגוע | 7 | 28.6% | 41.9% | -13.3% |
| Bear Put Spread | 3 | רגיל | 36 | 33.3% | 38.0% | -4.6% |
| Bear Put Spread | 7 | זהירות | 23 | 52.2% | 36.4% | 15.8% |
| Bear Put Spread | 7 | לחץ גבוה | 9 | 55.6% | 35.9% | 19.7% |
| Bear Put Spread | 7 | רגוע | 7 | 0.0% | 41.5% | -41.5% |
| Bear Put Spread | 7 | רגיל | 35 | 34.3% | 36.2% | -1.9% |
| Bear Put Spread | 14 | זהירות | 22 | 36.4% | 35.4% | 0.9% |
| Bear Put Spread | 14 | לחץ גבוה | 9 | 66.7% | 33.3% | 33.3% |
| Bear Put Spread | 14 | רגוע | 7 | 0.0% | 28.7% | -28.7% |
| Bear Put Spread | 14 | רגיל | 34 | 44.1% | 30.9% | 13.2% |
| Bear Put Spread | 30 | זהירות | 21 | 23.8% | 18.7% | 5.1% |
| Bear Put Spread | 30 | לחץ גבוה | 9 | 44.4% | 23.1% | 21.4% |
| Bear Put Spread | 30 | רגוע | 7 | 42.9% | 27.0% | 15.8% |
| Bear Put Spread | 30 | רגיל | 34 | 44.1% | 23.6% | 20.5% |
| Bull Call Spread | 3 | זהירות | 37 | 62.2% | 53.5% | 8.6% |
| Bull Call Spread | 3 | לחץ גבוה | 7 | 57.1% | 61.5% | -4.4% |
| Bull Call Spread | 3 | רגוע | 62 | 50.0% | 58.1% | -8.1% |
| Bull Call Spread | 3 | רגיל | 89 | 61.8% | 62.0% | -0.2% |
| Bull Call Spread | 7 | זהירות | 37 | 73.0% | 63.6% | 9.3% |
| Bull Call Spread | 7 | לחץ גבוה | 7 | 71.4% | 64.1% | 7.3% |
| Bull Call Spread | 7 | רגוע | 62 | 41.9% | 58.5% | -16.6% |
| Bull Call Spread | 7 | רגיל | 89 | 73.0% | 63.8% | 9.2% |
| Bull Call Spread | 14 | זהירות | 37 | 67.6% | 64.6% | 3.0% |
| Bull Call Spread | 14 | לחץ גבוה | 7 | 57.1% | 66.7% | -9.5% |
| Bull Call Spread | 14 | רגוע | 61 | 54.1% | 71.3% | -17.2% |
| Bull Call Spread | 14 | רגיל | 89 | 76.4% | 69.1% | 7.3% |
| Bull Call Spread | 30 | זהירות | 37 | 86.5% | 81.3% | 5.2% |
| Bull Call Spread | 30 | לחץ גבוה | 7 | 85.7% | 76.9% | 8.8% |
| Bull Call Spread | 30 | רגוע | 61 | 57.4% | 73.0% | -15.6% |
| Bull Call Spread | 30 | רגיל | 89 | 80.9% | 76.4% | 4.5% |
| Long Butterfly / Condor קנוי | 3 | רגוע | 19 | 31.6% | 34.9% | -3.4% |
| Long Butterfly / Condor קנוי | 3 | רגיל | 11 | 54.5% | 35.0% | 19.6% |
| Long Butterfly / Condor קנוי | 7 | רגוע | 18 | 44.4% | 40.8% | 3.7% |
| Long Butterfly / Condor קנוי | 7 | רגיל | 11 | 27.3% | 32.6% | -5.3% |
| Long Butterfly / Condor קנוי | 14 | רגוע | 18 | 11.1% | 36.7% | -25.6% |
| Long Butterfly / Condor קנוי | 14 | רגיל | 11 | 54.5% | 33.6% | 21.0% |
| Long Butterfly / Condor קנוי | 30 | רגוע | 17 | 11.8% | 29.9% | -18.1% |
| Long Butterfly / Condor קנוי | 30 | רגיל | 10 | 20.0% | 32.5% | -12.5% |
| Put Ratio Backspread 1×2 | 3 | זהירות | 5 | 0.0% | 12.1% | -12.1% |
| Put Ratio Backspread 1×2 | 3 | לחץ גבוה | 14 | 7.1% | 17.9% | -10.8% |
| Put Ratio Backspread 1×2 | 7 | זהירות | 5 | 40.0% | 7.1% | 32.9% |
| Put Ratio Backspread 1×2 | 7 | לחץ גבוה | 14 | 0.0% | 15.4% | -15.4% |
| Put Ratio Backspread 1×2 | 14 | זהירות | 5 | 0.0% | 5.2% | -5.2% |
| Put Ratio Backspread 1×2 | 14 | לחץ גבוה | 14 | 7.1% | 5.1% | 2.0% |
| Put Ratio Backspread 1×2 | 30 | זהירות | 5 | 0.0% | 6.6% | -6.6% |
| Put Ratio Backspread 1×2 | 30 | לחץ גבוה | 14 | 7.1% | 5.1% | 2.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | זהירות | 6 | 33.3% | 34.3% | -1.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | רגוע | 165 | 34.5% | 35.6% | -1.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | רגיל | 115 | 41.7% | 42.6% | -0.8% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | זהירות | 6 | 50.0% | 40.4% | 9.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | רגוע | 165 | 31.5% | 33.4% | -1.9% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | רגיל | 115 | 32.2% | 38.9% | -6.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | זהירות | 5 | 20.0% | 37.5% | -17.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | רגוע | 165 | 43.6% | 43.0% | 0.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | רגיל | 113 | 38.1% | 38.6% | -0.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | זהירות | 5 | 40.0% | 48.4% | -8.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | רגוע | 164 | 34.1% | 34.5% | -0.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | רגיל | 113 | 35.4% | 34.2% | 1.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | זהירות | 12 | 50.0% | 34.3% | 15.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | רגוע | 20 | 30.0% | 26.6% | 3.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | רגיל | 23 | 30.4% | 27.7% | 2.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | זהירות | 12 | 41.7% | 29.3% | 12.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | רגוע | 19 | 36.8% | 29.6% | 7.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | רגיל | 23 | 39.1% | 29.9% | 9.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | זהירות | 12 | 33.3% | 30.2% | 3.1% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | רגוע | 19 | 5.3% | 22.0% | -16.8% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | רגיל | 23 | 34.8% | 23.8% | 11.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | זהירות | 9 | 33.3% | 12.1% | 21.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | רגוע | 16 | 6.2% | 19.6% | -13.3% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | רגיל | 18 | 5.6% | 17.5% | -11.9% |

## Strategy robustness by calendar year

| strategy | horizon | year | selected_n | success_rate | unconditional_baseline | uplift |
| --- | --- | --- | --- | --- | --- | --- |
| Bear Put Spread | 3 | 2,023 | 13 | 69.2% | 46.9% | 22.4% |
| Bear Put Spread | 3 | 2,024 | 20 | 15.0% | 40.0% | -25.0% |
| Bear Put Spread | 3 | 2,025 | 18 | 27.8% | 35.0% | -7.2% |
| Bear Put Spread | 3 | 2,026 | 24 | 33.3% | 47.6% | -14.2% |
| Bear Put Spread | 7 | 2,023 | 13 | 69.2% | 43.8% | 25.5% |
| Bear Put Spread | 7 | 2,024 | 20 | 20.0% | 39.6% | -19.6% |
| Bear Put Spread | 7 | 2,025 | 18 | 16.7% | 31.3% | -14.6% |
| Bear Put Spread | 7 | 2,026 | 23 | 56.5% | 44.6% | 11.9% |
| Bear Put Spread | 14 | 2,023 | 13 | 53.8% | 38.5% | 15.3% |
| Bear Put Spread | 14 | 2,024 | 20 | 5.0% | 29.0% | -24.0% |
| Bear Put Spread | 14 | 2,025 | 18 | 27.8% | 24.0% | 3.8% |
| Bear Put Spread | 14 | 2,026 | 21 | 76.2% | 40.9% | 35.3% |
| Bear Put Spread | 30 | 2,023 | 13 | 38.5% | 44.8% | -6.3% |
| Bear Put Spread | 30 | 2,024 | 20 | 15.0% | 12.7% | 2.3% |
| Bear Put Spread | 30 | 2,025 | 18 | 22.2% | 17.9% | 4.3% |
| Bear Put Spread | 30 | 2,026 | 20 | 75.0% | 45.7% | 29.3% |
| Bull Call Spread | 3 | 2,023 | 13 | 53.8% | 53.1% | 0.7% |
| Bull Call Spread | 3 | 2,024 | 59 | 55.9% | 60.0% | -4.1% |
| Bull Call Spread | 3 | 2,025 | 79 | 64.6% | 65.0% | -0.5% |
| Bull Call Spread | 3 | 2,026 | 44 | 50.0% | 52.4% | -2.4% |
| Bull Call Spread | 7 | 2,023 | 13 | 53.8% | 56.2% | -2.4% |
| Bull Call Spread | 7 | 2,024 | 59 | 57.6% | 60.4% | -2.8% |
| Bull Call Spread | 7 | 2,025 | 79 | 65.8% | 68.7% | -2.9% |
| Bull Call Spread | 7 | 2,026 | 44 | 68.2% | 55.4% | 12.8% |
| Bull Call Spread | 14 | 2,023 | 13 | 23.1% | 61.5% | -38.4% |
| Bull Call Spread | 14 | 2,024 | 59 | 59.3% | 71.0% | -11.7% |
| Bull Call Spread | 14 | 2,025 | 79 | 75.9% | 76.0% | -0.1% |
| Bull Call Spread | 14 | 2,026 | 43 | 74.4% | 59.1% | 15.3% |
| Bull Call Spread | 30 | 2,023 | 13 | 15.4% | 55.2% | -39.8% |
| Bull Call Spread | 30 | 2,024 | 59 | 72.9% | 87.3% | -14.5% |
| Bull Call Spread | 30 | 2,025 | 79 | 81.0% | 82.1% | -1.1% |
| Bull Call Spread | 30 | 2,026 | 43 | 83.7% | 54.3% | 29.4% |
| Long Butterfly / Condor קנוי | 3 | 2,023 | 8 | 37.5% | 41.7% | -4.2% |
| Long Butterfly / Condor קנוי | 3 | 2,024 | 12 | 50.0% | 35.5% | 14.5% |
| Long Butterfly / Condor קנוי | 3 | 2,025 | 7 | 28.6% | 28.5% | 0.1% |
| Long Butterfly / Condor קנוי | 3 | 2,026 | 5 | 40.0% | 39.9% | 0.1% |
| Long Butterfly / Condor קנוי | 7 | 2,023 | 8 | 62.5% | 55.2% | 7.3% |
| Long Butterfly / Condor קנוי | 7 | 2,024 | 12 | 41.7% | 33.9% | 7.8% |
| Long Butterfly / Condor קנוי | 7 | 2,025 | 7 | 0.0% | 31.3% | -31.3% |
| Long Butterfly / Condor קנוי | 14 | 2,023 | 8 | 0.0% | 39.6% | -39.6% |
| Long Butterfly / Condor קנוי | 14 | 2,024 | 12 | 25.0% | 31.0% | -6.0% |
| Long Butterfly / Condor קנוי | 14 | 2,025 | 7 | 42.9% | 31.3% | 11.6% |
| Long Butterfly / Condor קנוי | 30 | 2,023 | 8 | 0.0% | 24.0% | -24.0% |
| Long Butterfly / Condor קנוי | 30 | 2,024 | 12 | 25.0% | 39.6% | -14.6% |
| Long Butterfly / Condor קנוי | 30 | 2,025 | 7 | 14.3% | 25.6% | -11.3% |
| Long Straddle / Strangle | 3 | 2,025 | 5 | 0.0% | 37.0% | -37.0% |
| Long Straddle / Strangle | 7 | 2,025 | 5 | 0.0% | 42.3% | -42.3% |
| Long Straddle / Strangle | 14 | 2,025 | 5 | 20.0% | 39.8% | -19.8% |
| Long Straddle / Strangle | 30 | 2,025 | 5 | 20.0% | 56.9% | -36.9% |
| Put Ratio Backspread 1×2 | 3 | 2,024 | 6 | 16.7% | 14.3% | 2.4% |
| Put Ratio Backspread 1×2 | 3 | 2,025 | 11 | 9.1% | 12.6% | -3.5% |
| Put Ratio Backspread 1×2 | 7 | 2,024 | 6 | 0.0% | 6.9% | -6.9% |
| Put Ratio Backspread 1×2 | 7 | 2,025 | 11 | 18.2% | 11.0% | 7.2% |
| Put Ratio Backspread 1×2 | 14 | 2,024 | 6 | 0.0% | 6.1% | -6.1% |
| Put Ratio Backspread 1×2 | 14 | 2,025 | 11 | 0.0% | 2.8% | -2.8% |
| Put Ratio Backspread 1×2 | 30 | 2,024 | 6 | 0.0% | 0.0% | 0.0% |
| Put Ratio Backspread 1×2 | 30 | 2,025 | 11 | 0.0% | 0.8% | -0.8% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,023 | 38 | 42.1% | 34.4% | 7.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,024 | 107 | 35.5% | 39.6% | -4.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,025 | 101 | 39.6% | 40.7% | -1.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,026 | 40 | 32.5% | 32.9% | -0.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,023 | 38 | 47.4% | 40.6% | 6.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,024 | 107 | 29.0% | 33.1% | -4.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,025 | 101 | 28.7% | 37.4% | -8.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,026 | 40 | 35.0% | 38.1% | -3.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,023 | 38 | 57.9% | 45.8% | 12.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,024 | 107 | 36.4% | 37.1% | -0.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,025 | 101 | 40.6% | 39.0% | 1.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,026 | 37 | 37.8% | 44.7% | -6.9% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,023 | 38 | 44.7% | 38.5% | 6.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,024 | 107 | 46.7% | 50.2% | -3.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,025 | 101 | 22.8% | 26.0% | -3.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,026 | 36 | 22.2% | 33.6% | -11.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,023 | 21 | 38.1% | 37.5% | 0.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,024 | 12 | 16.7% | 25.7% | -9.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,025 | 7 | 42.9% | 22.4% | 20.5% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,026 | 16 | 37.5% | 34.3% | 3.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,023 | 21 | 33.3% | 33.3% | 0.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,024 | 12 | 50.0% | 32.7% | 17.3% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,025 | 7 | 28.6% | 20.3% | 8.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,026 | 15 | 40.0% | 36.0% | 4.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,023 | 21 | 23.8% | 22.9% | 0.9% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,024 | 12 | 25.0% | 22.9% | 2.1% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,025 | 7 | 14.3% | 21.1% | -6.9% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,026 | 15 | 26.7% | 33.3% | -6.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 2,023 | 21 | 4.8% | 13.5% | -8.8% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 2,024 | 12 | 0.0% | 12.7% | -12.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 2,025 | 7 | 14.3% | 17.1% | -2.8% |

## Context-only OOS ablation: FX-equity state and TA35-VTA35 correlation

| feature | horizon | n_eff | baseline_accuracy | augmented_accuracy | lift | p_value | positive_regimes | tested_regimes | fdr_q | eligible | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fx_equity_state | 3 | 241 | 52.7% | 51.9% | -0.8% | 0.5896 | 0 | 4 | 0.9703 | 0 | context-only |
| ta35_vta35_corr_60 | 3 | 225 | 53.3% | 48.4% | -4.9% | 0.8730 | 0 | 4 | 0.9703 | 0 | context-only |
| fx_equity_state | 7 | 103 | 50.5% | 44.7% | -5.8% | 0.8633 | 0 | 4 | 0.9703 | 0 | context-only |
| ta35_vta35_corr_60 | 7 | 96 | 51.0% | 46.9% | -4.2% | 0.7418 | 1 | 3 | 0.9703 | 0 | context-only |
| fx_equity_state | 14 | 50 | 60.0% | 68.0% | 8.0% | 0.1587 | 1 | 2 | 0.9703 | 0 | context-only |
| ta35_vta35_corr_60 | 14 | 47 | 61.7% | 44.7% | -17.0% | 0.9703 | 0 | 2 | 0.9703 | 0 | context-only |
| fx_equity_state | 30 | 23 | 60.9% | 52.2% | -8.7% | 0.7602 | 1 | 2 | 0.9703 | 0 | context-only |
| ta35_vta35_corr_60 | 30 | 22 | 63.6% | 54.5% | -9.1% | 0.7602 | 1 | 2 | 0.9703 | 0 | context-only |
