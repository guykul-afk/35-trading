# TA-35 dashboard — comprehensive backtest research

Generated: 2026-08-10 17:02 UTC

TA-35 sample: 2023-08-08 to 2026-08-07 (738 sessions)

Horizons: 3, 7, 14, 30 trading days

## Executive interpretation

This document is a research knowledge base for recommendation calibration. It tests every dashboard indicator output and every strategy family at every requested horizon. A positive lift means that the rule beat the relevant historical base rate; it does not guarantee future performance.


- 3d indicator leader: vrp_spread / volatility (lift +5.5%, n=715, strength 4/10, FDR q=1.000).
- 3d strategy-scenario leader: פרפר Put דובי / Broken-Wing Butterfly (uplift +18.1%, n=22, strength 2/10, FDR q=1.000; exploratory unless it passes the knowledge-tier gates).
- 7d indicator leader: reversal_5_vol_scaled / market (lift +10.1%, n=365, strength 7/10, FDR q=1.000).
- 7d strategy-scenario leader: Bear Put Spread (uplift +12.8%, n=45, strength 3/10, FDR q=1.000; exploratory unless it passes the knowledge-tier gates).
- 14d indicator leader: vta35 / volatility (lift +7.7%, n=665, strength 5/10, FDR q=1.000).
- 14d strategy-scenario leader: Bear Put Spread (uplift +19.3%, n=44, strength 4/10, FDR q=1.000; exploratory unless it passes the knowledge-tier gates).
- 30d indicator leader: rs_range_5_20 / volatility (lift +7.5%, n=688, strength 5/10, FDR q=1.000).
- 30d strategy-scenario leader: Bear Put Spread (uplift +16.6%, n=44, strength 4/10, FDR q=1.000; exploratory unless it passes the knowledge-tier gates).
- No strategy-selection rule passed the minimum sample plus 10% FDR gate; strategy rankings are exploratory and should not yet alter live recommendations automatically.


## Test design

- Strict as-of feature construction: a signal on session t uses only data available through t.
- Outcomes: TA-35 close-to-close return and forward realized volatility over 3/7/14/30 sessions.
- Direction tests: accuracy, RV-level-conditioned class-marginal baseline, lift, Wilson 95% interval and a conservative one-sided p-value using floor(n/h).
- Calibration tests: delayed walk-forward Brier score, so a label enters the historical score only after its horizon has elapsed.
- Robustness: min/median/max across every non-overlapping offset, calendar years, dashboard regimes and signal-intensity subsets.
- Continuous tests: rank information coefficient and top-versus-bottom quintile outcome spread.
- Volatility forecast tests: bias, MAE, RMSE, realized-volatility rank IC and empirical ±0.5/1/1.5/2σ coverage.
- Strategy tests: scenario success when selected, empirical unconditional scenario frequency, recommendation uplift, sensitivity to forecast-band width, and year/regime stability.
- Legacy strength scores remain in raw research tables only for compatibility and are disabled in the product UI and deployment logic.


## Limitations

- All features are computed as-of date t; outcomes begin after that close.
- Overlapping horizons create serial dependence; non-overlapping robustness columns are reported.
- P-values use the conservative non-overlapping n=floor(n/h), with Holm family-wise adjustment under arbitrary dependence; they remain diagnostics, not deployment gates.
- Strategy results are market-scenario proxies, not option P&L; premiums, skew, spreads and slippage are unavailable.
- Calendar/Diagonal is untestable without historical IV for at least two expiries.
- The 738-day TA-35 sample spans only about three years; regime and annual results can be fragile.
- forecast_rv_3d and expected_move_3d_points emit the same direction rule, so their similar results are duplicate evidence rather than independent confirmation.
- US series are made available on the following calendar day before as-of alignment, preserving Friday data for Sunday and preventing same-date Mon-Thu look-ahead.
- The current rule thresholds were not frozen before this historical sample. Treat discoveries as in-sample research and require a future frozen holdout before automatic deployment.
- The family probability model uses one shrunk input per information family, strict label maturity, and one non-overlapping offset; its probabilities remain unapproved research outputs.

## Recommendation knowledge tiers and deployment gates

| kind | name | axis | horizon | n | edge | fdr_q | year_stability | regime_stability | tier |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 3 | 22 | 0.1806 | 1.0000 | 1/2 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 3 | 16 | 0.0950 | 1.0000 | 2/2 | 2/2 | C — context only (validation freeze) |
| strategy_proxy | Bull Call Spread | scenario | 3 | 111 | 0.0645 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vrp_spread | volatility | 3 | 715 | 0.0550 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | market | 3 | 367 | 0.0531 | 1.0000 | 4/4 | 2/4 | C — context only (validation freeze) |
| indicator | vta35 | volatility | 3 | 676 | 0.0522 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | volatility | 3 | 676 | 0.0522 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | volatility | 3 | 715 | 0.0381 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 3 | 184 | 0.0377 | 1.0000 | 3/4 | 1/3 | C — context only (validation freeze) |
| indicator | har_rv_3d | volatility | 3 | 612 | 0.0356 | 1.0000 | 3/3 | 3/4 | C — context only (validation freeze) |
| indicator | expected_move_3d_points | volatility | 3 | 715 | 0.0352 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | forecast_rv_3d | volatility | 3 | 715 | 0.0352 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | atr_5_20_ratio | volatility | 3 | 715 | 0.0344 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | rs_range_5_20 | volatility | 3 | 715 | 0.0332 | 1.0000 | 3/4 | 4/4 | C — context only (validation freeze) |
| indicator | local_global_stress_spread | volatility | 3 | 616 | 0.0306 | 1.0000 | 2/3 | 3/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | volatility | 3 | 715 | 0.0292 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | trend_efficiency_20 | volatility | 3 | 715 | 0.0200 | 1.0000 | 3/4 | 4/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | volatility | 3 | 715 | 0.0194 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | downside_share_20 | volatility | 3 | 715 | 0.0173 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| indicator | rv_20_60_ratio | volatility | 3 | 675 | 0.0169 | 1.0000 | 2/4 | 4/4 | C — context only (validation freeze) |
| indicator | rv_acceleration | volatility | 3 | 715 | 0.0158 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | gap_share_20 | volatility | 3 | 715 | 0.0131 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | volatility | 3 | 715 | 0.0129 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | market | 3 | 635 | 0.0103 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | volatility | 3 | 715 | 0.0090 | 1.0000 | 2/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta_vol_of_vol_20 | volatility | 3 | 715 | 0.0028 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | market | 3 | 680 | 0.0006 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | matched_vrp_3d | volatility | 3 | 612 | 0.0000 | 1.0000 | 1/3 | 0/4 | C — context only (validation freeze) |
| indicator | range_position_20 | volatility | 3 | 715 | 0.0000 | 1.0000 | 0/4 | 1/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | volatility | 3 | 715 | 0.0000 | 1.0000 | 0/4 | 1/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | market | 3 | 630 | -0.0004 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | market | 3 | 715 | -0.0027 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | market | 3 | 693 | -0.0130 | 1.0000 | 0/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta35 | market | 3 | 603 | -0.0215 | 1.0000 | 0/4 | 2/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | market | 3 | 603 | -0.0215 | 1.0000 | 0/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Bear Put Spread | scenario | 3 | 45 | -0.0291 | 1.0000 | 1/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Bear Call Spread | scenario | 3 | 62 | -0.0527 | 1.0000 | 2/4 | 0/2 | C — context only (validation freeze) |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 3 | 25 | -0.0529 | 1.0000 | 0/2 | 1/3 | C — context only (validation freeze) |
| strategy_proxy | Iron Condor | scenario | 3 | 16 | -0.0868 | 1.0000 | 1/1 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Bull Put Spread | scenario | 3 | 184 | -0.0891 | 1.0000 | 1/4 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 3 | 8 | -0.0928 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Long Straddle / Strangle | scenario | 3 | 5 | -0.3507 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Calendar / Diagonal | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Iron Butterfly | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 3 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Bear Put Spread | scenario | 7 | 45 | 0.1282 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | market | 7 | 365 | 0.1013 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | vta35 | volatility | 7 | 672 | 0.0834 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | volatility | 7 | 672 | 0.0834 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 7 | 22 | 0.0758 | 1.0000 | 1/2 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 7 | 25 | 0.0650 | 1.0000 | 1/2 | 2/3 | C — context only (validation freeze) |
| indicator | vrp_spread | volatility | 7 | 711 | 0.0626 | 1.0000 | 3/4 | 4/4 | C — context only (validation freeze) |
| indicator | rs_range_5_20 | volatility | 7 | 711 | 0.0591 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | volatility | 7 | 711 | 0.0483 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | local_global_stress_spread | volatility | 7 | 612 | 0.0464 | 1.0000 | 3/3 | 3/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | volatility | 7 | 711 | 0.0452 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | volatility | 7 | 711 | 0.0423 | 1.0000 | 4/4 | 2/4 | C — context only (validation freeze) |
| indicator | atr_5_20_ratio | volatility | 7 | 711 | 0.0422 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | expected_move_3d_points | volatility | 7 | 711 | 0.0409 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | forecast_rv_3d | volatility | 7 | 711 | 0.0409 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Bull Call Spread | scenario | 7 | 111 | 0.0406 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | volatility | 7 | 711 | 0.0391 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | har_rv_3d | volatility | 7 | 608 | 0.0294 | 1.0000 | 2/3 | 2/4 | C — context only (validation freeze) |
| indicator | gap_share_20 | volatility | 7 | 711 | 0.0259 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 7 | 184 | 0.0237 | 1.0000 | 2/4 | 2/3 | C — context only (validation freeze) |
| indicator | vta_vol_of_vol_20 | volatility | 7 | 711 | 0.0222 | 1.0000 | 2/4 | 4/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | volatility | 7 | 711 | 0.0188 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | trend_efficiency_20 | volatility | 7 | 711 | 0.0181 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | rv_20_60_ratio | volatility | 7 | 671 | 0.0142 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| indicator | downside_share_20 | volatility | 7 | 711 | 0.0076 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | matched_vrp_3d | volatility | 7 | 608 | 0.0000 | 1.0000 | 2/3 | 0/4 | C — context only (validation freeze) |
| indicator | range_position_20 | volatility | 7 | 711 | 0.0000 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | volatility | 7 | 711 | 0.0000 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | rv_acceleration | volatility | 7 | 711 | -0.0007 | 1.0000 | 2/4 | 1/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | market | 7 | 632 | -0.0096 | 1.0000 | 2/4 | 0/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | market | 7 | 689 | -0.0212 | 1.0000 | 0/4 | 0/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | market | 7 | 711 | -0.0224 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | market | 7 | 627 | -0.0252 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | market | 7 | 677 | -0.0348 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| strategy_proxy | Iron Condor | scenario | 7 | 15 | -0.0446 | 1.0000 | 1/1 | 0/2 | C — context only (validation freeze) |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 7 | 16 | -0.0470 | 1.0000 | 1/2 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Bear Call Spread | scenario | 7 | 60 | -0.0550 | 1.0000 | 1/4 | 0/2 | C — context only (validation freeze) |
| strategy_proxy | Bull Put Spread | scenario | 7 | 184 | -0.0596 | 1.0000 | 1/4 | 1/2 | C — context only (validation freeze) |
| indicator | vta35 | market | 7 | 601 | -0.0947 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | market | 7 | 601 | -0.0947 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 7 | 8 | -0.2603 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Long Straddle / Strangle | scenario | 7 | 5 | -0.3554 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Calendar / Diagonal | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Iron Butterfly | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 7 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Bear Put Spread | scenario | 14 | 44 | 0.1926 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Iron Condor | scenario | 14 | 15 | 0.0936 | 1.0000 | 1/1 | 1/2 | C — context only (validation freeze) |
| indicator | vta35 | volatility | 14 | 665 | 0.0770 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | volatility | 14 | 665 | 0.0770 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 14 | 181 | 0.0760 | 1.0000 | 4/4 | 2/3 | C — context only (validation freeze) |
| indicator | expected_move_3d_points | volatility | 14 | 704 | 0.0657 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | forecast_rv_3d | volatility | 14 | 704 | 0.0657 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | atr_5_20_ratio | volatility | 14 | 704 | 0.0627 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | volatility | 14 | 704 | 0.0625 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | rs_range_5_20 | volatility | 14 | 704 | 0.0525 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | volatility | 14 | 704 | 0.0507 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | rv_acceleration | volatility | 14 | 704 | 0.0441 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | volatility | 14 | 704 | 0.0438 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | har_rv_3d | volatility | 14 | 601 | 0.0411 | 1.0000 | 3/3 | 3/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | volatility | 14 | 704 | 0.0398 | 1.0000 | 4/4 | 4/4 | C — context only (validation freeze) |
| indicator | vrp_spread | volatility | 14 | 704 | 0.0381 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | market | 14 | 361 | 0.0277 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Bear Call Spread | scenario | 14 | 59 | 0.0261 | 1.0000 | 2/4 | 1/2 | C — context only (validation freeze) |
| indicator | usdils_change_5d | market | 14 | 620 | 0.0238 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta_vol_of_vol_20 | volatility | 14 | 704 | 0.0221 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | Bull Call Spread | scenario | 14 | 111 | 0.0191 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | volatility | 14 | 704 | 0.0151 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | local_global_stress_spread | volatility | 14 | 605 | 0.0086 | 1.0000 | 1/3 | 2/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | market | 14 | 670 | 0.0081 | 1.0000 | 2/4 | 1/4 | C — context only (validation freeze) |
| indicator | matched_vrp_3d | volatility | 14 | 601 | 0.0000 | 1.0000 | 0/3 | 0/4 | C — context only (validation freeze) |
| indicator | range_position_20 | volatility | 14 | 704 | 0.0000 | 1.0000 | 0/4 | 2/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | volatility | 14 | 704 | 0.0000 | 1.0000 | 0/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | market | 14 | 682 | -0.0035 | 1.0000 | 1/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | market | 14 | 704 | -0.0093 | 1.0000 | 2/4 | 1/4 | C — context only (validation freeze) |
| indicator | rv_20_60_ratio | volatility | 14 | 664 | -0.0098 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 14 | 22 | -0.0133 | 1.0000 | 1/2 | 1/2 | C — context only (validation freeze) |
| indicator | downside_share_20 | volatility | 14 | 704 | -0.0162 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | trend_efficiency_20 | volatility | 14 | 704 | -0.0169 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | market | 14 | 625 | -0.0228 | 1.0000 | 3/4 | 0/4 | C — context only (validation freeze) |
| indicator | gap_share_20 | volatility | 14 | 704 | -0.0231 | 1.0000 | 2/4 | 1/4 | C — context only (validation freeze) |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 14 | 25 | -0.0268 | 1.0000 | 0/2 | 1/3 | C — context only (validation freeze) |
| indicator | vta35 | market | 14 | 595 | -0.0334 | 1.0000 | 0/4 | 0/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | market | 14 | 595 | -0.0334 | 1.0000 | 0/4 | 0/4 | C — context only (validation freeze) |
| strategy_proxy | Bull Put Spread | scenario | 14 | 183 | -0.0723 | 1.0000 | 1/4 | 0/2 | C — context only (validation freeze) |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 14 | 16 | -0.0921 | 1.0000 | 1/2 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Long Straddle / Strangle | scenario | 14 | 5 | -0.1602 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 14 | 8 | -0.1685 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Calendar / Diagonal | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Iron Butterfly | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 14 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Bear Put Spread | scenario | 30 | 44 | 0.1658 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | Bull Call Spread | scenario | 30 | 111 | 0.0901 | 1.0000 | 2/4 | 4/4 | C — context only (validation freeze) |
| indicator | rs_range_5_20 | volatility | 30 | 688 | 0.0751 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | atr_5_20_ratio | volatility | 30 | 688 | 0.0744 | 1.0000 | 4/4 | 3/4 | C — context only (validation freeze) |
| indicator | vta35 | volatility | 30 | 649 | 0.0695 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | volatility | 30 | 649 | 0.0695 | 1.0000 | 2/4 | 2/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | volatility | 30 | 688 | 0.0629 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | expected_move_3d_points | volatility | 30 | 688 | 0.0528 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | forecast_rv_3d | volatility | 30 | 688 | 0.0528 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | rv_acceleration | volatility | 30 | 688 | 0.0506 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vrp_spread | volatility | 30 | 688 | 0.0468 | 1.0000 | 3/4 | 4/4 | C — context only (validation freeze) |
| strategy_proxy | Bear Call Spread | scenario | 30 | 50 | 0.0361 | 1.0000 | 2/3 | 2/2 | C — context only (validation freeze) |
| indicator | vta35_change_5d | market | 30 | 657 | 0.0276 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | volatility | 30 | 688 | 0.0234 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | volatility | 30 | 688 | 0.0220 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | vta35_change_5d | volatility | 30 | 688 | 0.0193 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | trend_efficiency_20 | volatility | 30 | 688 | 0.0162 | 1.0000 | 3/4 | 2/4 | C — context only (validation freeze) |
| indicator | har_rv_3d | volatility | 30 | 585 | 0.0158 | 1.0000 | 2/3 | 2/4 | C — context only (validation freeze) |
| indicator | local_global_stress_spread | volatility | 30 | 589 | 0.0122 | 1.0000 | 1/3 | 3/4 | C — context only (validation freeze) |
| indicator | vta_vol_of_vol_20 | volatility | 30 | 688 | 0.0117 | 1.0000 | 1/4 | 2/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | volatility | 30 | 688 | 0.0084 | 1.0000 | 3/4 | 3/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | market | 30 | 351 | 0.0048 | 1.0000 | 2/4 | 3/4 | C — context only (validation freeze) |
| indicator | matched_vrp_3d | volatility | 30 | 585 | 0.0000 | 1.0000 | 1/3 | 1/4 | C — context only (validation freeze) |
| indicator | range_position_20 | volatility | 30 | 688 | 0.0000 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| indicator | reversal_5_vol_scaled | volatility | 30 | 688 | 0.0000 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| indicator | downside_share_20 | volatility | 30 | 688 | -0.0032 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Call שורי / Broken-Wing Butterfly | scenario | 30 | 180 | -0.0100 | 1.0000 | 1/4 | 2/3 | C — context only (validation freeze) |
| indicator | vta35 | market | 30 | 582 | -0.0116 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | vta35_zscore_60 | market | 30 | 582 | -0.0116 | 1.0000 | 3/4 | 1/4 | C — context only (validation freeze) |
| indicator | vix_vix3m_ratio | market | 30 | 666 | -0.0128 | 1.0000 | 0/4 | 2/4 | C — context only (validation freeze) |
| indicator | usdils_change_5d | market | 30 | 605 | -0.0134 | 1.0000 | 1/4 | 3/4 | C — context only (validation freeze) |
| strategy_proxy | פרפר Put דובי / Broken-Wing Butterfly | scenario | 30 | 19 | -0.0171 | 1.0000 | 0/1 | 1/2 | C — context only (validation freeze) |
| indicator | vix_curve_ratio | market | 30 | 688 | -0.0225 | 1.0000 | 1/4 | 2/4 | C — context only (validation freeze) |
| strategy_proxy | Put Ratio Backspread 1×2 | scenario | 30 | 25 | -0.0283 | 1.0000 | 0/2 | 1/3 | C — context only (validation freeze) |
| indicator | rv_20_60_ratio | volatility | 30 | 648 | -0.0302 | 1.0000 | 0/4 | 1/4 | C — context only (validation freeze) |
| indicator | vix9d_vix_ratio | market | 30 | 609 | -0.0338 | 1.0000 | 1/4 | 1/4 | C — context only (validation freeze) |
| indicator | gap_share_20 | volatility | 30 | 688 | -0.0631 | 1.0000 | 1/4 | 0/4 | C — context only (validation freeze) |
| strategy_proxy | Bull Put Spread | scenario | 30 | 183 | -0.0696 | 1.0000 | 1/4 | 1/2 | C — context only (validation freeze) |
| strategy_proxy | Iron Condor | scenario | 30 | 14 | -0.1834 | 1.0000 | 0/1 | 0/2 | C — context only (validation freeze) |
| strategy_proxy | Long Straddle / Strangle | scenario | 30 | 5 | -0.2595 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Long Butterfly / Condor קנוי | scenario | 30 | 14 | -0.3186 | 1.0000 | 0/2 | 0/1 | C — context only (validation freeze) |
| strategy_proxy | Call Ratio Backspread 1×2 | scenario | 30 | 8 | -0.3912 | 1.0000 | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Calendar / Diagonal | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | Iron Butterfly | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |
| strategy_proxy | פרפר הפוך / Long Iron Condor | scenario | 30 | 0 | — | — | 0/0 | 0/0 | C — context only (validation freeze) |

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
| combined_RV_forecast | 3 | 730 | 0.1581 | 0.1185 | 0.0396 | 0.0685 | 0.0858 | 0.1982 | 34.2% | 64.9% | 82.1% | 92.3% |
| VTA35_proxy | 3 | 735 | 0.1761 | 0.1182 | 0.0578 | 0.0767 | 0.0926 | 0.2522 | 39.0% | 69.4% | 88.6% | 97.3% |
| combined_RV_forecast | 7 | 726 | 0.1579 | 0.1477 | 0.0102 | 0.0478 | 0.0650 | 0.2716 | 36.0% | 64.5% | 82.8% | 92.4% |
| VTA35_proxy | 7 | 731 | 0.1759 | 0.1473 | 0.0286 | 0.0512 | 0.0645 | 0.4043 | 41.2% | 68.0% | 88.8% | 97.1% |
| combined_RV_forecast | 14 | 719 | 0.1576 | 0.1581 | -0.0005 | 0.0419 | 0.0586 | 0.2901 | 34.2% | 64.0% | 82.6% | 91.5% |
| VTA35_proxy | 14 | 724 | 0.1755 | 0.1575 | 0.0180 | 0.0448 | 0.0557 | 0.3517 | 36.6% | 69.8% | 89.4% | 96.8% |
| combined_RV_forecast | 30 | 703 | 0.1569 | 0.1640 | -0.0071 | 0.0420 | 0.0574 | 0.1235 | 31.9% | 54.1% | 74.5% | 85.9% |
| VTA35_proxy | 30 | 708 | 0.1745 | 0.1635 | 0.0110 | 0.0392 | 0.0494 | 0.2037 | 34.7% | 57.6% | 79.2% | 92.1% |

## Expanding HAR-RV benchmark and incremental VTA35 value

| horizon | model | n_eff | mae | mse_variance | qlike | direction_accuracy | qlike_improvement_vs_naive | block_bootstrap_p |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | naive_rv20 | 178 | 0.0714 | 0.0008 | 0.7220 | 0.0% | 0.0000 | 1.0000 |
| 3 | combined | 178 | 0.0706 | 0.0008 | 0.7041 | 52.2% | 0.0179 | 0.0880 |
| 3 | vta35 | 178 | 0.0764 | 0.0008 | 0.7179 | 47.8% | 0.0041 | 0.4640 |
| 3 | gjr | 178 | 0.0624 | 0.0007 | 0.6926 | 69.1% | 0.0293 | 0.1860 |
| 3 | har | 178 | 0.0539 | 0.0007 | 1.1409 | 74.2% | -0.4189 | 1.0000 |
| 3 | har_x | 178 | 0.0547 | 0.0007 | 1.1073 | 73.6% | -0.3853 | 1.0000 |
| 7 | naive_rv20 | 75 | 0.0456 | 0.0005 | 0.2583 | 0.0% | 0.0000 | 1.0000 |
| 7 | combined | 75 | 0.0444 | 0.0005 | 0.2456 | 65.3% | 0.0127 | 0.2180 |
| 7 | vta35 | 75 | 0.0451 | 0.0004 | 0.2037 | 58.7% | 0.0546 | 0.1320 |
| 7 | gjr | 75 | 0.0423 | 0.0004 | 0.2960 | 62.7% | -0.0378 | 0.9320 |
| 7 | har | 75 | 0.0423 | 0.0005 | 0.3479 | 61.3% | -0.0897 | 0.9520 |
| 7 | har_x | 75 | 0.0404 | 0.0004 | 0.3056 | 68.0% | -0.0473 | 0.8820 |
| 14 | naive_rv20 | 36 | 0.0393 | 0.0004 | 0.1649 | 0.0% | 0.0000 | 1.0000 |
| 14 | combined | 36 | 0.0384 | 0.0004 | 0.1620 | 52.8% | 0.0029 | 0.3620 |
| 14 | vta35 | 36 | 0.0423 | 0.0004 | 0.1472 | 58.3% | 0.0178 | 0.1400 |
| 14 | gjr | 36 | 0.0402 | 0.0004 | 0.2362 | 55.6% | -0.0713 | 1.0000 |
| 14 | har | 36 | 0.0343 | 0.0004 | 0.2122 | 52.8% | -0.0473 | 0.9960 |
| 14 | har_x | 36 | 0.0370 | 0.0004 | 0.2310 | 50.0% | -0.0661 | 0.9800 |
| 30 | naive_rv20 | 16 | 0.0528 | 0.0006 | 0.2637 | 0.0% | 0.0000 | 1.0000 |
| 30 | combined | 16 | 0.0505 | 0.0005 | 0.2528 | 56.2% | 0.0109 | 0.0020 |
| 30 | vta35 | 16 | 0.0424 | 0.0003 | 0.1501 | 62.5% | 0.1136 | 0.0020 |
| 30 | gjr | 16 | 0.0476 | 0.0006 | 0.3295 | 50.0% | -0.0658 | 1.0000 |
| 30 | har | 16 | 0.0332 | 0.0003 | 0.1963 | 62.5% | 0.0674 | 0.0020 |
| 30 | har_x | 16 | 0.0349 | 0.0003 | 0.2266 | 68.8% | 0.0372 | 0.0020 |

## Every non-overlapping offset reported separately

| indicator | horizon | axis | offset | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | 0 | 238 | 44.1% | 42.6% | 1.5% |
| atr_5_20_ratio | 3 | volatility | 1 | 238 | 49.6% | 43.3% | 6.3% |
| atr_5_20_ratio | 3 | volatility | 2 | 239 | 46.0% | 43.5% | 2.5% |
| atr_5_20_ratio | 7 | volatility | 0 | 102 | 50.0% | 40.6% | 9.4% |
| atr_5_20_ratio | 7 | volatility | 1 | 102 | 47.1% | 41.6% | 5.5% |
| atr_5_20_ratio | 7 | volatility | 2 | 102 | 44.1% | 42.6% | 1.5% |
| atr_5_20_ratio | 7 | volatility | 3 | 101 | 41.6% | 39.7% | 1.9% |
| atr_5_20_ratio | 7 | volatility | 4 | 101 | 47.5% | 44.6% | 2.9% |
| atr_5_20_ratio | 7 | volatility | 5 | 101 | 48.5% | 43.6% | 4.9% |
| atr_5_20_ratio | 7 | volatility | 6 | 102 | 45.1% | 41.3% | 3.8% |
| atr_5_20_ratio | 14 | volatility | 0 | 50 | 44.0% | 44.8% | -0.8% |
| atr_5_20_ratio | 14 | volatility | 1 | 50 | 52.0% | 45.1% | 6.9% |
| atr_5_20_ratio | 14 | volatility | 2 | 50 | 52.0% | 47.1% | 4.9% |
| atr_5_20_ratio | 14 | volatility | 3 | 50 | 46.0% | 44.8% | 1.2% |
| atr_5_20_ratio | 14 | volatility | 4 | 50 | 58.0% | 49.6% | 8.4% |
| atr_5_20_ratio | 14 | volatility | 5 | 50 | 50.0% | 41.1% | 8.9% |
| atr_5_20_ratio | 14 | volatility | 6 | 51 | 51.0% | 40.9% | 10.1% |
| atr_5_20_ratio | 14 | volatility | 7 | 51 | 41.2% | 39.6% | 1.5% |
| atr_5_20_ratio | 14 | volatility | 8 | 51 | 43.1% | 35.8% | 7.4% |
| atr_5_20_ratio | 14 | volatility | 9 | 51 | 47.1% | 38.4% | 8.7% |
| atr_5_20_ratio | 14 | volatility | 10 | 50 | 42.0% | 34.9% | 7.1% |
| atr_5_20_ratio | 14 | volatility | 11 | 50 | 56.0% | 41.4% | 14.6% |
| atr_5_20_ratio | 14 | volatility | 12 | 50 | 54.0% | 43.0% | 11.0% |
| atr_5_20_ratio | 14 | volatility | 13 | 50 | 42.0% | 40.5% | 1.5% |
| atr_5_20_ratio | 30 | volatility | 0 | 23 | 56.5% | 45.9% | 10.6% |
| atr_5_20_ratio | 30 | volatility | 1 | 23 | 65.2% | 41.0% | 24.2% |
| atr_5_20_ratio | 30 | volatility | 2 | 23 | 69.6% | 40.4% | 29.1% |
| atr_5_20_ratio | 30 | volatility | 3 | 23 | 65.2% | 41.0% | 24.2% |
| atr_5_20_ratio | 30 | volatility | 4 | 23 | 60.9% | 41.2% | 19.7% |
| atr_5_20_ratio | 30 | volatility | 5 | 23 | 60.9% | 42.5% | 18.4% |
| atr_5_20_ratio | 30 | volatility | 6 | 23 | 56.5% | 41.8% | 14.7% |
| atr_5_20_ratio | 30 | volatility | 7 | 23 | 52.2% | 52.2% | 0.0% |
| atr_5_20_ratio | 30 | volatility | 8 | 23 | 56.5% | 44.9% | 11.6% |
| atr_5_20_ratio | 30 | volatility | 9 | 23 | 56.5% | 41.5% | 15.0% |
| atr_5_20_ratio | 30 | volatility | 10 | 23 | 52.2% | 46.4% | 5.8% |
| atr_5_20_ratio | 30 | volatility | 11 | 23 | 43.5% | 42.7% | 0.8% |
| atr_5_20_ratio | 30 | volatility | 12 | 23 | 30.4% | 41.1% | -10.7% |
| atr_5_20_ratio | 30 | volatility | 13 | 23 | 34.8% | 36.3% | -1.5% |
| atr_5_20_ratio | 30 | volatility | 14 | 23 | 39.1% | 33.3% | 5.8% |
| atr_5_20_ratio | 30 | volatility | 15 | 23 | 52.2% | 42.3% | 9.8% |
| atr_5_20_ratio | 30 | volatility | 16 | 23 | 60.9% | 45.2% | 15.7% |
| atr_5_20_ratio | 30 | volatility | 17 | 23 | 56.5% | 41.6% | 14.9% |
| atr_5_20_ratio | 30 | volatility | 18 | 22 | 50.0% | 48.5% | 1.5% |
| atr_5_20_ratio | 30 | volatility | 19 | 22 | 54.5% | 38.0% | 16.5% |
| atr_5_20_ratio | 30 | volatility | 20 | 23 | 52.2% | 48.8% | 3.4% |
| atr_5_20_ratio | 30 | volatility | 21 | 23 | 47.8% | 38.3% | 9.5% |
| atr_5_20_ratio | 30 | volatility | 22 | 23 | 34.8% | 35.6% | -0.8% |
| atr_5_20_ratio | 30 | volatility | 23 | 23 | 39.1% | 38.5% | 0.6% |
| atr_5_20_ratio | 30 | volatility | 24 | 23 | 39.1% | 34.6% | 4.6% |
| atr_5_20_ratio | 30 | volatility | 25 | 23 | 43.5% | 36.9% | 6.6% |
| atr_5_20_ratio | 30 | volatility | 26 | 23 | 43.5% | 37.4% | 6.1% |
| atr_5_20_ratio | 30 | volatility | 27 | 23 | 39.1% | 31.9% | 7.2% |
| atr_5_20_ratio | 30 | volatility | 28 | 23 | 30.4% | 30.9% | -0.4% |
| atr_5_20_ratio | 30 | volatility | 29 | 23 | 52.2% | 47.8% | 4.3% |
| downside_share_20 | 3 | volatility | 0 | 238 | 47.9% | 46.8% | 1.1% |
| downside_share_20 | 3 | volatility | 1 | 238 | 52.1% | 46.8% | 5.3% |
| downside_share_20 | 3 | volatility | 2 | 239 | 44.4% | 45.5% | -1.2% |
| downside_share_20 | 7 | volatility | 0 | 102 | 43.1% | 40.1% | 3.0% |
| downside_share_20 | 7 | volatility | 1 | 102 | 36.3% | 36.8% | -0.5% |
| downside_share_20 | 7 | volatility | 2 | 102 | 37.3% | 36.8% | 0.4% |
| downside_share_20 | 7 | volatility | 3 | 101 | 37.6% | 39.5% | -1.8% |
| downside_share_20 | 7 | volatility | 4 | 101 | 37.6% | 40.3% | -2.7% |
| downside_share_20 | 7 | volatility | 5 | 101 | 45.5% | 42.8% | 2.8% |
| downside_share_20 | 7 | volatility | 6 | 102 | 48.0% | 44.3% | 3.7% |
| downside_share_20 | 14 | volatility | 0 | 50 | 38.0% | 36.8% | 1.2% |
| downside_share_20 | 14 | volatility | 1 | 50 | 30.0% | 34.0% | -4.0% |
| downside_share_20 | 14 | volatility | 2 | 50 | 32.0% | 32.8% | -0.8% |
| downside_share_20 | 14 | volatility | 3 | 50 | 36.0% | 35.5% | 0.5% |
| downside_share_20 | 14 | volatility | 4 | 50 | 38.0% | 37.7% | 0.3% |
| downside_share_20 | 14 | volatility | 5 | 50 | 38.0% | 39.2% | -1.2% |
| downside_share_20 | 14 | volatility | 6 | 51 | 37.3% | 37.1% | 0.1% |
| downside_share_20 | 14 | volatility | 7 | 51 | 31.4% | 32.4% | -1.0% |
| downside_share_20 | 14 | volatility | 8 | 51 | 29.4% | 27.3% | 2.1% |
| downside_share_20 | 14 | volatility | 9 | 51 | 37.3% | 33.6% | 3.6% |
| downside_share_20 | 14 | volatility | 10 | 50 | 28.0% | 34.2% | -6.2% |
| downside_share_20 | 14 | volatility | 11 | 50 | 34.0% | 38.1% | -4.1% |
| downside_share_20 | 14 | volatility | 12 | 50 | 30.0% | 34.2% | -4.2% |
| downside_share_20 | 14 | volatility | 13 | 50 | 36.0% | 39.5% | -3.5% |
| downside_share_20 | 30 | volatility | 0 | 23 | 34.8% | 33.3% | 1.5% |
| downside_share_20 | 30 | volatility | 1 | 23 | 26.1% | 32.4% | -6.3% |
| downside_share_20 | 30 | volatility | 2 | 23 | 34.8% | 38.9% | -4.1% |
| downside_share_20 | 30 | volatility | 3 | 23 | 21.7% | 35.9% | -14.2% |
| downside_share_20 | 30 | volatility | 4 | 23 | 26.1% | 29.0% | -2.9% |
| downside_share_20 | 30 | volatility | 5 | 23 | 21.7% | 32.9% | -11.1% |
| downside_share_20 | 30 | volatility | 6 | 23 | 17.4% | 34.2% | -16.8% |
| downside_share_20 | 30 | volatility | 7 | 23 | 39.1% | 39.9% | -0.7% |
| downside_share_20 | 30 | volatility | 8 | 23 | 34.8% | 40.1% | -5.4% |
| downside_share_20 | 30 | volatility | 9 | 23 | 39.1% | 37.3% | 1.9% |
| downside_share_20 | 30 | volatility | 10 | 23 | 34.8% | 34.8% | 0.0% |
| downside_share_20 | 30 | volatility | 11 | 23 | 30.4% | 35.3% | -4.9% |
| downside_share_20 | 30 | volatility | 12 | 23 | 34.8% | 35.7% | -0.9% |
| downside_share_20 | 30 | volatility | 13 | 23 | 43.5% | 37.0% | 6.5% |
| downside_share_20 | 30 | volatility | 14 | 23 | 34.8% | 34.4% | 0.4% |
| downside_share_20 | 30 | volatility | 15 | 23 | 34.8% | 31.1% | 3.7% |
| downside_share_20 | 30 | volatility | 16 | 23 | 26.1% | 28.7% | -2.6% |
| downside_share_20 | 30 | volatility | 17 | 23 | 34.8% | 31.5% | 3.3% |
| downside_share_20 | 30 | volatility | 18 | 22 | 40.9% | 25.8% | 15.2% |
| downside_share_20 | 30 | volatility | 19 | 22 | 36.4% | 25.0% | 11.4% |
| downside_share_20 | 30 | volatility | 20 | 23 | 30.4% | 25.7% | 4.7% |
| downside_share_20 | 30 | volatility | 21 | 23 | 39.1% | 29.6% | 9.6% |
| downside_share_20 | 30 | volatility | 22 | 23 | 30.4% | 29.6% | 0.8% |
| downside_share_20 | 30 | volatility | 23 | 23 | 26.1% | 30.6% | -4.5% |
| downside_share_20 | 30 | volatility | 24 | 23 | 34.8% | 35.7% | -0.9% |
| downside_share_20 | 30 | volatility | 25 | 23 | 34.8% | 36.0% | -1.2% |
| downside_share_20 | 30 | volatility | 26 | 23 | 39.1% | 37.0% | 2.2% |
| downside_share_20 | 30 | volatility | 27 | 23 | 26.1% | 25.0% | 1.1% |
| downside_share_20 | 30 | volatility | 28 | 23 | 30.4% | 30.0% | 0.4% |
| downside_share_20 | 30 | volatility | 29 | 23 | 34.8% | 36.4% | -1.6% |
| expected_move_3d_points | 3 | volatility | 0 | 238 | 35.3% | 31.5% | 3.8% |
| expected_move_3d_points | 3 | volatility | 1 | 238 | 33.6% | 31.1% | 2.5% |
| expected_move_3d_points | 3 | volatility | 2 | 239 | 37.7% | 33.5% | 4.2% |
| expected_move_3d_points | 7 | volatility | 0 | 102 | 33.3% | 30.0% | 3.3% |
| expected_move_3d_points | 7 | volatility | 1 | 102 | 39.2% | 35.8% | 3.4% |
| expected_move_3d_points | 7 | volatility | 2 | 102 | 38.2% | 34.6% | 3.7% |
| expected_move_3d_points | 7 | volatility | 3 | 101 | 38.6% | 36.0% | 2.6% |
| expected_move_3d_points | 7 | volatility | 4 | 101 | 38.6% | 34.7% | 3.9% |
| expected_move_3d_points | 7 | volatility | 5 | 101 | 38.6% | 34.0% | 4.6% |
| expected_move_3d_points | 7 | volatility | 6 | 102 | 40.2% | 31.9% | 8.3% |
| expected_move_3d_points | 14 | volatility | 0 | 50 | 34.0% | 30.9% | 3.1% |
| expected_move_3d_points | 14 | volatility | 1 | 50 | 36.0% | 33.7% | 2.3% |
| expected_move_3d_points | 14 | volatility | 2 | 50 | 46.0% | 38.3% | 7.7% |
| expected_move_3d_points | 14 | volatility | 3 | 50 | 40.0% | 36.6% | 3.4% |
| expected_move_3d_points | 14 | volatility | 4 | 50 | 42.0% | 34.3% | 7.7% |
| expected_move_3d_points | 14 | volatility | 5 | 50 | 50.0% | 37.7% | 12.3% |
| expected_move_3d_points | 14 | volatility | 6 | 51 | 49.0% | 34.8% | 14.2% |
| expected_move_3d_points | 14 | volatility | 7 | 51 | 39.2% | 31.8% | 7.4% |
| expected_move_3d_points | 14 | volatility | 8 | 51 | 43.1% | 37.7% | 5.4% |
| expected_move_3d_points | 14 | volatility | 9 | 51 | 43.1% | 32.4% | 10.7% |
| expected_move_3d_points | 14 | volatility | 10 | 50 | 34.0% | 35.6% | -1.6% |
| expected_move_3d_points | 14 | volatility | 11 | 50 | 42.0% | 35.0% | 7.0% |
| expected_move_3d_points | 14 | volatility | 12 | 50 | 42.0% | 33.3% | 8.7% |
| expected_move_3d_points | 14 | volatility | 13 | 50 | 40.0% | 32.7% | 7.3% |
| expected_move_3d_points | 30 | volatility | 0 | 23 | 30.4% | 25.9% | 4.5% |
| expected_move_3d_points | 30 | volatility | 1 | 23 | 39.1% | 37.6% | 1.6% |
| expected_move_3d_points | 30 | volatility | 2 | 23 | 52.2% | 42.5% | 9.6% |
| expected_move_3d_points | 30 | volatility | 3 | 23 | 52.2% | 36.2% | 15.9% |
| expected_move_3d_points | 30 | volatility | 4 | 23 | 43.5% | 32.0% | 11.5% |
| expected_move_3d_points | 30 | volatility | 5 | 23 | 43.5% | 38.4% | 5.1% |
| expected_move_3d_points | 30 | volatility | 6 | 23 | 43.5% | 32.4% | 11.1% |
| expected_move_3d_points | 30 | volatility | 7 | 23 | 39.1% | 37.7% | 1.4% |
| expected_move_3d_points | 30 | volatility | 8 | 23 | 43.5% | 39.5% | 3.9% |
| expected_move_3d_points | 30 | volatility | 9 | 23 | 39.1% | 31.6% | 7.6% |
| expected_move_3d_points | 30 | volatility | 10 | 23 | 26.1% | 36.2% | -10.1% |
| expected_move_3d_points | 30 | volatility | 11 | 23 | 26.1% | 33.2% | -7.1% |
| expected_move_3d_points | 30 | volatility | 12 | 23 | 43.5% | 34.3% | 9.1% |
| expected_move_3d_points | 30 | volatility | 13 | 23 | 30.4% | 28.5% | 2.0% |
| expected_move_3d_points | 30 | volatility | 14 | 23 | 30.4% | 29.0% | 1.4% |
| expected_move_3d_points | 30 | volatility | 15 | 23 | 34.8% | 32.2% | 2.6% |
| expected_move_3d_points | 30 | volatility | 16 | 23 | 52.2% | 35.9% | 16.2% |
| expected_move_3d_points | 30 | volatility | 17 | 23 | 47.8% | 34.6% | 13.2% |
| expected_move_3d_points | 30 | volatility | 18 | 22 | 54.5% | 51.1% | 3.4% |
| expected_move_3d_points | 30 | volatility | 19 | 22 | 50.0% | 39.2% | 10.8% |
| expected_move_3d_points | 30 | volatility | 20 | 23 | 52.2% | 38.5% | 13.6% |
| expected_move_3d_points | 30 | volatility | 21 | 23 | 52.2% | 42.5% | 9.7% |
| expected_move_3d_points | 30 | volatility | 22 | 23 | 60.9% | 51.2% | 9.7% |
| expected_move_3d_points | 30 | volatility | 23 | 23 | 43.5% | 34.7% | 8.7% |
| expected_move_3d_points | 30 | volatility | 24 | 23 | 34.8% | 26.9% | 7.8% |
| expected_move_3d_points | 30 | volatility | 25 | 23 | 34.8% | 21.6% | 13.2% |
| expected_move_3d_points | 30 | volatility | 26 | 23 | 47.8% | 33.5% | 14.3% |
| expected_move_3d_points | 30 | volatility | 27 | 23 | 39.1% | 27.9% | 11.2% |
| expected_move_3d_points | 30 | volatility | 28 | 23 | 21.7% | 27.8% | -6.1% |
| expected_move_3d_points | 30 | volatility | 29 | 23 | 26.1% | 35.3% | -9.2% |
| forecast_rv_3d | 3 | volatility | 0 | 238 | 35.3% | 31.5% | 3.8% |
| forecast_rv_3d | 3 | volatility | 1 | 238 | 33.6% | 31.1% | 2.5% |
| forecast_rv_3d | 3 | volatility | 2 | 239 | 37.7% | 33.5% | 4.2% |
| forecast_rv_3d | 7 | volatility | 0 | 102 | 33.3% | 30.0% | 3.3% |
| forecast_rv_3d | 7 | volatility | 1 | 102 | 39.2% | 35.8% | 3.4% |
| forecast_rv_3d | 7 | volatility | 2 | 102 | 38.2% | 34.6% | 3.7% |
| forecast_rv_3d | 7 | volatility | 3 | 101 | 38.6% | 36.0% | 2.6% |
| forecast_rv_3d | 7 | volatility | 4 | 101 | 38.6% | 34.7% | 3.9% |
| forecast_rv_3d | 7 | volatility | 5 | 101 | 38.6% | 34.0% | 4.6% |
| forecast_rv_3d | 7 | volatility | 6 | 102 | 40.2% | 31.9% | 8.3% |
| forecast_rv_3d | 14 | volatility | 0 | 50 | 34.0% | 30.9% | 3.1% |
| forecast_rv_3d | 14 | volatility | 1 | 50 | 36.0% | 33.7% | 2.3% |
| forecast_rv_3d | 14 | volatility | 2 | 50 | 46.0% | 38.3% | 7.7% |
| forecast_rv_3d | 14 | volatility | 3 | 50 | 40.0% | 36.6% | 3.4% |
| forecast_rv_3d | 14 | volatility | 4 | 50 | 42.0% | 34.3% | 7.7% |
| forecast_rv_3d | 14 | volatility | 5 | 50 | 50.0% | 37.7% | 12.3% |
| forecast_rv_3d | 14 | volatility | 6 | 51 | 49.0% | 34.8% | 14.2% |
| forecast_rv_3d | 14 | volatility | 7 | 51 | 39.2% | 31.8% | 7.4% |
| forecast_rv_3d | 14 | volatility | 8 | 51 | 43.1% | 37.7% | 5.4% |
| forecast_rv_3d | 14 | volatility | 9 | 51 | 43.1% | 32.4% | 10.7% |
| forecast_rv_3d | 14 | volatility | 10 | 50 | 34.0% | 35.6% | -1.6% |
| forecast_rv_3d | 14 | volatility | 11 | 50 | 42.0% | 35.0% | 7.0% |
| forecast_rv_3d | 14 | volatility | 12 | 50 | 42.0% | 33.3% | 8.7% |
| forecast_rv_3d | 14 | volatility | 13 | 50 | 40.0% | 32.7% | 7.3% |
| forecast_rv_3d | 30 | volatility | 0 | 23 | 30.4% | 25.9% | 4.5% |
| forecast_rv_3d | 30 | volatility | 1 | 23 | 39.1% | 37.6% | 1.6% |
| forecast_rv_3d | 30 | volatility | 2 | 23 | 52.2% | 42.5% | 9.6% |
| forecast_rv_3d | 30 | volatility | 3 | 23 | 52.2% | 36.2% | 15.9% |
| forecast_rv_3d | 30 | volatility | 4 | 23 | 43.5% | 32.0% | 11.5% |
| forecast_rv_3d | 30 | volatility | 5 | 23 | 43.5% | 38.4% | 5.1% |
| forecast_rv_3d | 30 | volatility | 6 | 23 | 43.5% | 32.4% | 11.1% |
| forecast_rv_3d | 30 | volatility | 7 | 23 | 39.1% | 37.7% | 1.4% |
| forecast_rv_3d | 30 | volatility | 8 | 23 | 43.5% | 39.5% | 3.9% |
| forecast_rv_3d | 30 | volatility | 9 | 23 | 39.1% | 31.6% | 7.6% |
| forecast_rv_3d | 30 | volatility | 10 | 23 | 26.1% | 36.2% | -10.1% |
| forecast_rv_3d | 30 | volatility | 11 | 23 | 26.1% | 33.2% | -7.1% |
| forecast_rv_3d | 30 | volatility | 12 | 23 | 43.5% | 34.3% | 9.1% |
| forecast_rv_3d | 30 | volatility | 13 | 23 | 30.4% | 28.5% | 2.0% |
| forecast_rv_3d | 30 | volatility | 14 | 23 | 30.4% | 29.0% | 1.4% |
| forecast_rv_3d | 30 | volatility | 15 | 23 | 34.8% | 32.2% | 2.6% |
| forecast_rv_3d | 30 | volatility | 16 | 23 | 52.2% | 35.9% | 16.2% |
| forecast_rv_3d | 30 | volatility | 17 | 23 | 47.8% | 34.6% | 13.2% |
| forecast_rv_3d | 30 | volatility | 18 | 22 | 54.5% | 51.1% | 3.4% |
| forecast_rv_3d | 30 | volatility | 19 | 22 | 50.0% | 39.2% | 10.8% |
| forecast_rv_3d | 30 | volatility | 20 | 23 | 52.2% | 38.5% | 13.6% |
| forecast_rv_3d | 30 | volatility | 21 | 23 | 52.2% | 42.5% | 9.7% |
| forecast_rv_3d | 30 | volatility | 22 | 23 | 60.9% | 51.2% | 9.7% |
| forecast_rv_3d | 30 | volatility | 23 | 23 | 43.5% | 34.7% | 8.7% |
| forecast_rv_3d | 30 | volatility | 24 | 23 | 34.8% | 26.9% | 7.8% |
| forecast_rv_3d | 30 | volatility | 25 | 23 | 34.8% | 21.6% | 13.2% |
| forecast_rv_3d | 30 | volatility | 26 | 23 | 47.8% | 33.5% | 14.3% |
| forecast_rv_3d | 30 | volatility | 27 | 23 | 39.1% | 27.9% | 11.2% |
| forecast_rv_3d | 30 | volatility | 28 | 23 | 21.7% | 27.8% | -6.1% |
| forecast_rv_3d | 30 | volatility | 29 | 23 | 26.1% | 35.3% | -9.2% |
| gap_share_20 | 3 | volatility | 0 | 238 | 37.0% | 33.0% | 4.0% |
| gap_share_20 | 3 | volatility | 1 | 238 | 33.6% | 32.6% | 1.0% |
| gap_share_20 | 3 | volatility | 2 | 239 | 31.8% | 32.7% | -0.9% |
| gap_share_20 | 7 | volatility | 0 | 102 | 33.3% | 30.5% | 2.8% |
| gap_share_20 | 7 | volatility | 1 | 102 | 28.4% | 28.7% | -0.3% |
| gap_share_20 | 7 | volatility | 2 | 102 | 36.3% | 32.2% | 4.1% |
| gap_share_20 | 7 | volatility | 3 | 101 | 37.6% | 31.7% | 5.9% |
| gap_share_20 | 7 | volatility | 4 | 101 | 33.7% | 31.5% | 2.2% |
| gap_share_20 | 7 | volatility | 5 | 101 | 34.7% | 31.0% | 3.6% |
| gap_share_20 | 7 | volatility | 6 | 102 | 31.4% | 31.2% | 0.2% |
| gap_share_20 | 14 | volatility | 0 | 50 | 28.0% | 31.8% | -3.8% |
| gap_share_20 | 14 | volatility | 1 | 50 | 30.0% | 29.5% | 0.5% |
| gap_share_20 | 14 | volatility | 2 | 50 | 32.0% | 30.7% | 1.3% |
| gap_share_20 | 14 | volatility | 3 | 50 | 30.0% | 34.6% | -4.6% |
| gap_share_20 | 14 | volatility | 4 | 50 | 32.0% | 31.6% | 0.4% |
| gap_share_20 | 14 | volatility | 5 | 50 | 32.0% | 30.1% | 1.9% |
| gap_share_20 | 14 | volatility | 6 | 51 | 33.3% | 29.6% | 3.8% |
| gap_share_20 | 14 | volatility | 7 | 51 | 23.5% | 28.0% | -4.5% |
| gap_share_20 | 14 | volatility | 8 | 51 | 21.6% | 25.8% | -4.2% |
| gap_share_20 | 14 | volatility | 9 | 51 | 31.4% | 28.6% | 2.8% |
| gap_share_20 | 14 | volatility | 10 | 50 | 30.0% | 26.2% | 3.8% |
| gap_share_20 | 14 | volatility | 11 | 50 | 22.0% | 30.6% | -8.6% |
| gap_share_20 | 14 | volatility | 12 | 50 | 18.0% | 28.3% | -10.3% |
| gap_share_20 | 14 | volatility | 13 | 50 | 28.0% | 29.1% | -1.1% |
| gap_share_20 | 30 | volatility | 0 | 23 | 30.4% | 29.8% | 0.7% |
| gap_share_20 | 30 | volatility | 1 | 23 | 26.1% | 25.6% | 0.5% |
| gap_share_20 | 30 | volatility | 2 | 23 | 26.1% | 30.4% | -4.3% |
| gap_share_20 | 30 | volatility | 3 | 23 | 17.4% | 36.2% | -18.8% |
| gap_share_20 | 30 | volatility | 4 | 23 | 17.4% | 26.1% | -8.7% |
| gap_share_20 | 30 | volatility | 5 | 23 | 4.3% | 22.9% | -18.6% |
| gap_share_20 | 30 | volatility | 6 | 23 | 4.3% | 26.9% | -22.6% |
| gap_share_20 | 30 | volatility | 7 | 23 | 13.0% | 19.6% | -6.5% |
| gap_share_20 | 30 | volatility | 8 | 23 | 17.4% | 24.7% | -7.3% |
| gap_share_20 | 30 | volatility | 9 | 23 | 30.4% | 26.0% | 4.5% |
| gap_share_20 | 30 | volatility | 10 | 23 | 8.7% | 20.3% | -11.6% |
| gap_share_20 | 30 | volatility | 11 | 23 | 26.1% | 28.8% | -2.7% |
| gap_share_20 | 30 | volatility | 12 | 23 | 34.8% | 28.9% | 5.9% |
| gap_share_20 | 30 | volatility | 13 | 23 | 30.4% | 41.7% | -11.3% |
| gap_share_20 | 30 | volatility | 14 | 23 | 26.1% | 35.5% | -9.4% |
| gap_share_20 | 30 | volatility | 15 | 23 | 26.1% | 37.9% | -11.8% |
| gap_share_20 | 30 | volatility | 16 | 23 | 26.1% | 32.5% | -6.4% |
| gap_share_20 | 30 | volatility | 17 | 23 | 30.4% | 32.9% | -2.4% |
| gap_share_20 | 30 | volatility | 18 | 22 | 27.3% | 27.3% | 0.0% |
| gap_share_20 | 30 | volatility | 19 | 22 | 22.7% | 24.2% | -1.5% |
| gap_share_20 | 30 | volatility | 20 | 23 | 13.0% | 24.4% | -11.3% |
| gap_share_20 | 30 | volatility | 21 | 23 | 21.7% | 29.1% | -7.4% |
| gap_share_20 | 30 | volatility | 22 | 23 | 17.4% | 26.7% | -9.3% |
| gap_share_20 | 30 | volatility | 23 | 23 | 26.1% | 24.1% | 2.0% |
| gap_share_20 | 30 | volatility | 24 | 23 | 30.4% | 26.5% | 3.9% |
| gap_share_20 | 30 | volatility | 25 | 23 | 30.4% | 28.1% | 2.4% |
| gap_share_20 | 30 | volatility | 26 | 23 | 34.8% | 29.1% | 5.7% |
| gap_share_20 | 30 | volatility | 27 | 23 | 26.1% | 23.2% | 2.9% |
| gap_share_20 | 30 | volatility | 28 | 23 | 21.7% | 29.6% | -7.8% |
| gap_share_20 | 30 | volatility | 29 | 23 | 30.4% | 33.9% | -3.5% |
| har_rv_3d | 3 | volatility | 0 | 204 | 34.3% | 30.7% | 3.6% |
| har_rv_3d | 3 | volatility | 1 | 204 | 32.4% | 30.6% | 1.8% |
| har_rv_3d | 3 | volatility | 2 | 204 | 37.7% | 32.6% | 5.1% |
| har_rv_3d | 7 | volatility | 0 | 87 | 33.3% | 31.2% | 2.1% |
| har_rv_3d | 7 | volatility | 1 | 87 | 36.8% | 35.2% | 1.6% |
| har_rv_3d | 7 | volatility | 2 | 87 | 36.8% | 34.8% | 2.0% |
| har_rv_3d | 7 | volatility | 3 | 86 | 40.7% | 35.9% | 4.8% |
| har_rv_3d | 7 | volatility | 4 | 87 | 36.8% | 35.2% | 1.5% |
| har_rv_3d | 7 | volatility | 5 | 87 | 39.1% | 35.0% | 4.1% |
| har_rv_3d | 7 | volatility | 6 | 87 | 37.9% | 32.3% | 5.6% |
| har_rv_3d | 14 | volatility | 0 | 43 | 32.6% | 30.2% | 2.4% |
| har_rv_3d | 14 | volatility | 1 | 43 | 37.2% | 33.4% | 3.8% |
| har_rv_3d | 14 | volatility | 2 | 43 | 41.9% | 38.2% | 3.6% |
| har_rv_3d | 14 | volatility | 3 | 43 | 41.9% | 37.5% | 4.3% |
| har_rv_3d | 14 | volatility | 4 | 43 | 39.5% | 36.2% | 3.4% |
| har_rv_3d | 14 | volatility | 5 | 43 | 53.5% | 40.3% | 13.2% |
| har_rv_3d | 14 | volatility | 6 | 43 | 51.2% | 36.7% | 14.4% |
| har_rv_3d | 14 | volatility | 7 | 43 | 41.9% | 35.7% | 6.1% |
| har_rv_3d | 14 | volatility | 8 | 43 | 37.2% | 39.0% | -1.8% |
| har_rv_3d | 14 | volatility | 9 | 43 | 37.2% | 31.7% | 5.6% |
| har_rv_3d | 14 | volatility | 10 | 42 | 28.6% | 37.8% | -9.2% |
| har_rv_3d | 14 | volatility | 11 | 43 | 39.5% | 36.9% | 2.7% |
| har_rv_3d | 14 | volatility | 12 | 43 | 39.5% | 34.1% | 5.5% |
| har_rv_3d | 14 | volatility | 13 | 43 | 39.5% | 32.9% | 6.6% |
| har_rv_3d | 30 | volatility | 0 | 19 | 26.3% | 26.6% | -0.3% |
| har_rv_3d | 30 | volatility | 1 | 19 | 42.1% | 39.7% | 2.4% |
| har_rv_3d | 30 | volatility | 2 | 19 | 47.4% | 44.6% | 2.8% |
| har_rv_3d | 30 | volatility | 3 | 20 | 50.0% | 39.9% | 10.1% |
| har_rv_3d | 30 | volatility | 4 | 20 | 35.0% | 30.5% | 4.5% |
| har_rv_3d | 30 | volatility | 5 | 20 | 40.0% | 40.0% | 0.0% |
| har_rv_3d | 30 | volatility | 6 | 20 | 45.0% | 36.8% | 8.2% |
| har_rv_3d | 30 | volatility | 7 | 20 | 45.0% | 43.3% | 1.7% |
| har_rv_3d | 30 | volatility | 8 | 20 | 45.0% | 43.0% | 2.0% |
| har_rv_3d | 30 | volatility | 9 | 20 | 45.0% | 36.3% | 8.7% |
| har_rv_3d | 30 | volatility | 10 | 20 | 30.0% | 38.3% | -8.3% |
| har_rv_3d | 30 | volatility | 11 | 20 | 25.0% | 28.2% | -3.2% |
| har_rv_3d | 30 | volatility | 12 | 20 | 40.0% | 32.0% | 8.0% |
| har_rv_3d | 30 | volatility | 13 | 20 | 30.0% | 29.0% | 1.0% |
| har_rv_3d | 30 | volatility | 14 | 20 | 30.0% | 30.8% | -0.8% |
| har_rv_3d | 30 | volatility | 15 | 20 | 35.0% | 32.4% | 2.6% |
| har_rv_3d | 30 | volatility | 16 | 20 | 50.0% | 36.2% | 13.8% |
| har_rv_3d | 30 | volatility | 17 | 20 | 45.0% | 35.0% | 10.0% |
| har_rv_3d | 30 | volatility | 18 | 19 | 52.6% | 54.1% | -1.4% |
| har_rv_3d | 30 | volatility | 19 | 19 | 47.4% | 46.7% | 0.7% |
| har_rv_3d | 30 | volatility | 20 | 19 | 52.6% | 45.3% | 7.4% |
| har_rv_3d | 30 | volatility | 21 | 19 | 52.6% | 49.6% | 3.1% |
| har_rv_3d | 30 | volatility | 22 | 19 | 57.9% | 57.6% | 0.3% |
| har_rv_3d | 30 | volatility | 23 | 19 | 31.6% | 34.9% | -3.3% |
| har_rv_3d | 30 | volatility | 24 | 19 | 26.3% | 24.3% | 2.0% |
| har_rv_3d | 30 | volatility | 25 | 19 | 26.3% | 21.2% | 5.1% |
| har_rv_3d | 30 | volatility | 26 | 19 | 42.1% | 35.7% | 6.4% |
| har_rv_3d | 30 | volatility | 27 | 19 | 36.8% | 25.4% | 11.5% |
| har_rv_3d | 30 | volatility | 28 | 19 | 15.8% | 24.2% | -8.4% |
| har_rv_3d | 30 | volatility | 29 | 19 | 26.3% | 40.8% | -14.5% |
| local_global_stress_spread | 3 | volatility | 0 | 205 | 42.9% | 42.1% | 0.8% |
| local_global_stress_spread | 3 | volatility | 1 | 205 | 45.9% | 41.9% | 3.9% |
| local_global_stress_spread | 3 | volatility | 2 | 206 | 47.1% | 42.9% | 4.2% |
| local_global_stress_spread | 7 | volatility | 0 | 88 | 47.7% | 42.8% | 4.9% |
| local_global_stress_spread | 7 | volatility | 1 | 88 | 45.5% | 40.8% | 4.6% |
| local_global_stress_spread | 7 | volatility | 2 | 88 | 42.0% | 42.3% | -0.2% |
| local_global_stress_spread | 7 | volatility | 3 | 87 | 44.8% | 40.9% | 4.0% |
| local_global_stress_spread | 7 | volatility | 4 | 87 | 47.1% | 42.2% | 4.9% |
| local_global_stress_spread | 7 | volatility | 5 | 87 | 49.4% | 42.9% | 6.6% |
| local_global_stress_spread | 7 | volatility | 6 | 87 | 49.4% | 42.3% | 7.1% |
| local_global_stress_spread | 14 | volatility | 0 | 43 | 44.2% | 45.5% | -1.4% |
| local_global_stress_spread | 14 | volatility | 1 | 43 | 30.2% | 38.0% | -7.8% |
| local_global_stress_spread | 14 | volatility | 2 | 43 | 48.8% | 41.7% | 7.2% |
| local_global_stress_spread | 14 | volatility | 3 | 43 | 39.5% | 40.7% | -1.1% |
| local_global_stress_spread | 14 | volatility | 4 | 43 | 44.2% | 40.9% | 3.2% |
| local_global_stress_spread | 14 | volatility | 5 | 43 | 34.9% | 41.4% | -6.5% |
| local_global_stress_spread | 14 | volatility | 6 | 43 | 41.9% | 38.5% | 3.3% |
| local_global_stress_spread | 14 | volatility | 7 | 44 | 43.2% | 42.8% | 0.4% |
| local_global_stress_spread | 14 | volatility | 8 | 44 | 36.4% | 37.6% | -1.3% |
| local_global_stress_spread | 14 | volatility | 9 | 44 | 47.7% | 45.6% | 2.1% |
| local_global_stress_spread | 14 | volatility | 10 | 43 | 37.2% | 41.8% | -4.6% |
| local_global_stress_spread | 14 | volatility | 11 | 43 | 44.2% | 44.6% | -0.4% |
| local_global_stress_spread | 14 | volatility | 12 | 43 | 48.8% | 38.7% | 10.1% |
| local_global_stress_spread | 14 | volatility | 13 | 43 | 51.2% | 41.5% | 9.6% |
| local_global_stress_spread | 30 | volatility | 0 | 20 | 40.0% | 40.0% | 0.0% |
| local_global_stress_spread | 30 | volatility | 1 | 20 | 45.0% | 42.5% | 2.5% |
| local_global_stress_spread | 30 | volatility | 2 | 20 | 60.0% | 44.6% | 15.4% |
| local_global_stress_spread | 30 | volatility | 3 | 20 | 50.0% | 43.7% | 6.3% |
| local_global_stress_spread | 30 | volatility | 4 | 20 | 35.0% | 39.5% | -4.5% |
| local_global_stress_spread | 30 | volatility | 5 | 20 | 30.0% | 37.8% | -7.8% |
| local_global_stress_spread | 30 | volatility | 6 | 20 | 25.0% | 40.7% | -15.7% |
| local_global_stress_spread | 30 | volatility | 7 | 20 | 40.0% | 43.3% | -3.3% |
| local_global_stress_spread | 30 | volatility | 8 | 20 | 60.0% | 50.2% | 9.8% |
| local_global_stress_spread | 30 | volatility | 9 | 20 | 45.0% | 39.6% | 5.4% |
| local_global_stress_spread | 30 | volatility | 10 | 20 | 45.0% | 38.3% | 6.7% |
| local_global_stress_spread | 30 | volatility | 11 | 20 | 50.0% | 42.1% | 7.9% |
| local_global_stress_spread | 30 | volatility | 12 | 20 | 55.0% | 44.0% | 11.0% |
| local_global_stress_spread | 30 | volatility | 13 | 20 | 55.0% | 44.5% | 10.5% |
| local_global_stress_spread | 30 | volatility | 14 | 20 | 55.0% | 47.5% | 7.5% |
| local_global_stress_spread | 30 | volatility | 15 | 20 | 55.0% | 49.5% | 5.5% |
| local_global_stress_spread | 30 | volatility | 16 | 20 | 55.0% | 45.6% | 9.4% |
| local_global_stress_spread | 30 | volatility | 17 | 20 | 45.0% | 40.0% | 5.0% |
| local_global_stress_spread | 30 | volatility | 18 | 19 | 36.8% | 34.0% | 2.9% |
| local_global_stress_spread | 30 | volatility | 19 | 19 | 36.8% | 32.3% | 4.6% |
| local_global_stress_spread | 30 | volatility | 20 | 19 | 36.8% | 39.8% | -3.0% |
| local_global_stress_spread | 30 | volatility | 21 | 19 | 31.6% | 41.7% | -10.1% |
| local_global_stress_spread | 30 | volatility | 22 | 19 | 15.8% | 32.7% | -17.0% |
| local_global_stress_spread | 30 | volatility | 23 | 19 | 31.6% | 40.5% | -8.9% |
| local_global_stress_spread | 30 | volatility | 24 | 19 | 15.8% | 21.2% | -5.4% |
| local_global_stress_spread | 30 | volatility | 25 | 19 | 42.1% | 34.9% | 7.2% |
| local_global_stress_spread | 30 | volatility | 26 | 19 | 36.8% | 36.8% | 0.0% |
| local_global_stress_spread | 30 | volatility | 27 | 19 | 47.4% | 41.1% | 6.2% |
| local_global_stress_spread | 30 | volatility | 28 | 19 | 42.1% | 31.1% | 11.1% |
| local_global_stress_spread | 30 | volatility | 29 | 20 | 35.0% | 33.3% | 1.7% |
| matched_vrp_3d | 3 | volatility | 0 | 204 | 21.6% | 21.6% | 0.0% |
| matched_vrp_3d | 3 | volatility | 1 | 204 | 25.5% | 25.5% | 0.0% |
| matched_vrp_3d | 3 | volatility | 2 | 204 | 26.0% | 26.0% | 0.0% |
| matched_vrp_3d | 7 | volatility | 0 | 87 | 34.5% | 34.5% | 0.0% |
| matched_vrp_3d | 7 | volatility | 1 | 87 | 36.8% | 36.8% | -0.0% |
| matched_vrp_3d | 7 | volatility | 2 | 87 | 37.9% | 37.9% | 0.0% |
| matched_vrp_3d | 7 | volatility | 3 | 86 | 34.9% | 34.9% | 0.0% |
| matched_vrp_3d | 7 | volatility | 4 | 87 | 37.9% | 37.9% | 0.0% |
| matched_vrp_3d | 7 | volatility | 5 | 87 | 35.6% | 35.6% | 0.0% |
| matched_vrp_3d | 7 | volatility | 6 | 87 | 36.8% | 36.8% | 0.0% |
| matched_vrp_3d | 14 | volatility | 0 | 43 | 51.2% | 51.2% | 0.0% |
| matched_vrp_3d | 14 | volatility | 1 | 43 | 48.8% | 48.8% | -0.0% |
| matched_vrp_3d | 14 | volatility | 2 | 43 | 46.5% | 46.5% | -0.0% |
| matched_vrp_3d | 14 | volatility | 3 | 43 | 44.2% | 44.2% | 0.0% |
| matched_vrp_3d | 14 | volatility | 4 | 43 | 48.8% | 48.8% | 0.0% |
| matched_vrp_3d | 14 | volatility | 5 | 43 | 46.5% | 46.5% | 0.0% |
| matched_vrp_3d | 14 | volatility | 6 | 43 | 48.8% | 48.8% | 0.0% |
| matched_vrp_3d | 14 | volatility | 7 | 43 | 48.8% | 48.8% | -0.0% |
| matched_vrp_3d | 14 | volatility | 8 | 43 | 51.2% | 51.2% | 0.0% |
| matched_vrp_3d | 14 | volatility | 9 | 43 | 51.2% | 51.2% | 0.0% |
| matched_vrp_3d | 14 | volatility | 10 | 42 | 45.2% | 45.2% | -0.0% |
| matched_vrp_3d | 14 | volatility | 11 | 43 | 44.2% | 44.2% | 0.0% |
| matched_vrp_3d | 14 | volatility | 12 | 43 | 41.9% | 41.9% | 0.0% |
| matched_vrp_3d | 14 | volatility | 13 | 43 | 41.9% | 41.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 0 | 19 | 52.6% | 52.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | 1 | 19 | 47.4% | 47.4% | 0.0% |
| matched_vrp_3d | 30 | volatility | 2 | 19 | 42.1% | 42.1% | 0.0% |
| matched_vrp_3d | 30 | volatility | 3 | 20 | 45.0% | 45.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 4 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 5 | 20 | 45.0% | 45.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 6 | 20 | 45.0% | 45.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 7 | 20 | 45.0% | 45.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 8 | 20 | 35.0% | 35.0% | -0.0% |
| matched_vrp_3d | 30 | volatility | 9 | 20 | 40.0% | 40.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 10 | 20 | 40.0% | 40.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 11 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 12 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 13 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 14 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 15 | 20 | 60.0% | 60.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 16 | 20 | 55.0% | 55.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | 17 | 20 | 60.0% | 60.0% | -0.0% |
| matched_vrp_3d | 30 | volatility | 18 | 19 | 52.6% | 52.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | 19 | 19 | 57.9% | 57.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 20 | 19 | 68.4% | 68.4% | 0.0% |
| matched_vrp_3d | 30 | volatility | 21 | 19 | 63.2% | 63.2% | 0.0% |
| matched_vrp_3d | 30 | volatility | 22 | 19 | 57.9% | 57.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 23 | 19 | 57.9% | 57.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 24 | 19 | 52.6% | 52.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | 25 | 19 | 57.9% | 57.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 26 | 19 | 57.9% | 57.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | 27 | 19 | 52.6% | 52.6% | -0.0% |
| matched_vrp_3d | 30 | volatility | 28 | 19 | 52.6% | 52.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | 29 | 19 | 47.4% | 47.4% | 0.0% |
| range_position_20 | 3 | volatility | 0 | 238 | 5.0% | 5.0% | 0.0% |
| range_position_20 | 3 | volatility | 1 | 238 | 2.1% | 2.1% | 0.0% |
| range_position_20 | 3 | volatility | 2 | 239 | 3.8% | 3.8% | 0.0% |
| range_position_20 | 7 | volatility | 0 | 102 | 6.9% | 6.9% | 0.0% |
| range_position_20 | 7 | volatility | 1 | 102 | 7.8% | 7.8% | 0.0% |
| range_position_20 | 7 | volatility | 2 | 102 | 8.8% | 8.8% | 0.0% |
| range_position_20 | 7 | volatility | 3 | 101 | 6.9% | 6.9% | 0.0% |
| range_position_20 | 7 | volatility | 4 | 101 | 5.9% | 5.9% | 0.0% |
| range_position_20 | 7 | volatility | 5 | 101 | 4.0% | 4.0% | 0.0% |
| range_position_20 | 7 | volatility | 6 | 102 | 4.9% | 4.9% | 0.0% |
| range_position_20 | 14 | volatility | 0 | 50 | 4.0% | 4.0% | 0.0% |
| range_position_20 | 14 | volatility | 1 | 50 | 10.0% | 10.0% | 0.0% |
| range_position_20 | 14 | volatility | 2 | 50 | 8.0% | 8.0% | 0.0% |
| range_position_20 | 14 | volatility | 3 | 50 | 4.0% | 4.0% | 0.0% |
| range_position_20 | 14 | volatility | 4 | 50 | 2.0% | 2.0% | 0.0% |
| range_position_20 | 14 | volatility | 5 | 50 | 6.0% | 6.0% | 0.0% |
| range_position_20 | 14 | volatility | 6 | 51 | 9.8% | 9.8% | 0.0% |
| range_position_20 | 14 | volatility | 7 | 51 | 3.9% | 3.9% | 0.0% |
| range_position_20 | 14 | volatility | 8 | 51 | 5.9% | 5.9% | 0.0% |
| range_position_20 | 14 | volatility | 9 | 51 | 3.9% | 3.9% | 0.0% |
| range_position_20 | 14 | volatility | 10 | 50 | 10.0% | 10.0% | 0.0% |
| range_position_20 | 14 | volatility | 11 | 50 | 6.0% | 6.0% | 0.0% |
| range_position_20 | 14 | volatility | 12 | 50 | 12.0% | 12.0% | 0.0% |
| range_position_20 | 14 | volatility | 13 | 50 | 8.0% | 8.0% | 0.0% |
| range_position_20 | 30 | volatility | 0 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 1 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 2 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 3 | 23 | 17.4% | 17.4% | 0.0% |
| range_position_20 | 30 | volatility | 4 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 5 | 23 | 13.0% | 13.0% | 0.0% |
| range_position_20 | 30 | volatility | 6 | 23 | 13.0% | 13.0% | 0.0% |
| range_position_20 | 30 | volatility | 7 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 8 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 9 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 10 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 11 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 12 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 13 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 14 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 15 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 16 | 23 | 17.4% | 17.4% | 0.0% |
| range_position_20 | 30 | volatility | 17 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 18 | 22 | 13.6% | 13.6% | 0.0% |
| range_position_20 | 30 | volatility | 19 | 22 | 18.2% | 18.2% | 0.0% |
| range_position_20 | 30 | volatility | 20 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 21 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 22 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 23 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 24 | 23 | 4.3% | 4.3% | 0.0% |
| range_position_20 | 30 | volatility | 25 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 26 | 23 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 30 | volatility | 27 | 23 | 13.0% | 13.0% | 0.0% |
| range_position_20 | 30 | volatility | 28 | 23 | 8.7% | 8.7% | 0.0% |
| range_position_20 | 30 | volatility | 29 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 3 | market | 0 | 123 | 49.6% | 47.0% | 2.6% |
| reversal_5_vol_scaled | 3 | market | 1 | 123 | 54.5% | 44.2% | 10.3% |
| reversal_5_vol_scaled | 3 | market | 2 | 121 | 47.9% | 44.4% | 3.5% |
| reversal_5_vol_scaled | 3 | volatility | 0 | 238 | 5.0% | 5.0% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | 1 | 238 | 2.1% | 2.1% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | 2 | 239 | 3.8% | 3.8% | 0.0% |
| reversal_5_vol_scaled | 7 | market | 0 | 57 | 50.9% | 44.4% | 6.5% |
| reversal_5_vol_scaled | 7 | market | 1 | 56 | 55.4% | 42.4% | 13.0% |
| reversal_5_vol_scaled | 7 | market | 2 | 53 | 66.0% | 49.4% | 16.7% |
| reversal_5_vol_scaled | 7 | market | 3 | 57 | 61.4% | 48.6% | 12.8% |
| reversal_5_vol_scaled | 7 | market | 4 | 46 | 58.7% | 49.6% | 9.1% |
| reversal_5_vol_scaled | 7 | market | 5 | 49 | 44.9% | 43.4% | 1.5% |
| reversal_5_vol_scaled | 7 | market | 6 | 47 | 51.1% | 44.7% | 6.4% |
| reversal_5_vol_scaled | 7 | volatility | 0 | 102 | 6.9% | 6.9% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 1 | 102 | 7.8% | 7.8% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 2 | 102 | 8.8% | 8.8% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 3 | 101 | 6.9% | 6.9% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 4 | 101 | 5.9% | 5.9% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 5 | 101 | 4.0% | 4.0% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 6 | 102 | 4.9% | 4.9% | 0.0% |
| reversal_5_vol_scaled | 14 | market | 0 | 30 | 33.3% | 37.5% | -4.2% |
| reversal_5_vol_scaled | 14 | market | 1 | 29 | 34.5% | 36.2% | -1.7% |
| reversal_5_vol_scaled | 14 | market | 2 | 27 | 22.2% | 20.4% | 1.9% |
| reversal_5_vol_scaled | 14 | market | 3 | 33 | 42.4% | 40.0% | 2.4% |
| reversal_5_vol_scaled | 14 | market | 4 | 28 | 42.9% | 40.2% | 2.7% |
| reversal_5_vol_scaled | 14 | market | 5 | 25 | 48.0% | 42.7% | 5.3% |
| reversal_5_vol_scaled | 14 | market | 6 | 20 | 50.0% | 42.0% | 8.0% |
| reversal_5_vol_scaled | 14 | market | 7 | 27 | 55.6% | 46.9% | 8.6% |
| reversal_5_vol_scaled | 14 | market | 8 | 27 | 59.3% | 50.9% | 8.4% |
| reversal_5_vol_scaled | 14 | market | 9 | 25 | 64.0% | 54.0% | 10.0% |
| reversal_5_vol_scaled | 14 | market | 10 | 23 | 60.9% | 49.6% | 11.3% |
| reversal_5_vol_scaled | 14 | market | 11 | 17 | 41.2% | 43.5% | -2.4% |
| reversal_5_vol_scaled | 14 | market | 12 | 24 | 33.3% | 33.2% | 0.1% |
| reversal_5_vol_scaled | 14 | market | 13 | 26 | 30.8% | 34.1% | -3.3% |
| reversal_5_vol_scaled | 14 | volatility | 0 | 50 | 4.0% | 4.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 1 | 50 | 10.0% | 10.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 2 | 50 | 8.0% | 8.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 3 | 50 | 4.0% | 4.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 4 | 50 | 2.0% | 2.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 5 | 50 | 6.0% | 6.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 6 | 51 | 9.8% | 9.8% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 7 | 51 | 3.9% | 3.9% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 8 | 51 | 5.9% | 5.9% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 9 | 51 | 3.9% | 3.9% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 10 | 50 | 10.0% | 10.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 11 | 50 | 6.0% | 6.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 12 | 50 | 12.0% | 12.0% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 13 | 50 | 8.0% | 8.0% | 0.0% |
| reversal_5_vol_scaled | 30 | market | 0 | 12 | 33.3% | 36.1% | -2.8% |
| reversal_5_vol_scaled | 30 | market | 1 | 15 | 26.7% | 34.7% | -8.0% |
| reversal_5_vol_scaled | 30 | market | 2 | 12 | 33.3% | 37.5% | -4.2% |
| reversal_5_vol_scaled | 30 | market | 3 | 11 | 27.3% | 37.0% | -9.7% |
| reversal_5_vol_scaled | 30 | market | 4 | 9 | 55.6% | 46.7% | 8.9% |
| reversal_5_vol_scaled | 30 | market | 5 | 7 | 57.1% | 66.7% | -9.5% |
| reversal_5_vol_scaled | 30 | market | 6 | 13 | 53.8% | 44.9% | 9.0% |
| reversal_5_vol_scaled | 30 | market | 7 | 11 | 45.5% | 48.5% | -3.0% |
| reversal_5_vol_scaled | 30 | market | 8 | 8 | 50.0% | 42.9% | 7.1% |
| reversal_5_vol_scaled | 30 | market | 9 | 9 | 33.3% | 27.8% | 5.6% |
| reversal_5_vol_scaled | 30 | market | 10 | 11 | 18.2% | 27.3% | -9.1% |
| reversal_5_vol_scaled | 30 | market | 11 | 14 | 50.0% | 43.2% | 6.8% |
| reversal_5_vol_scaled | 30 | market | 12 | 12 | 33.3% | 41.7% | -8.3% |
| reversal_5_vol_scaled | 30 | market | 13 | 11 | 36.4% | 36.4% | 0.0% |
| reversal_5_vol_scaled | 30 | market | 14 | 18 | 38.9% | 37.9% | 1.0% |
| reversal_5_vol_scaled | 30 | market | 15 | 18 | 38.9% | 34.8% | 4.0% |
| reversal_5_vol_scaled | 30 | market | 16 | 16 | 25.0% | 32.5% | -7.5% |
| reversal_5_vol_scaled | 30 | market | 17 | 11 | 36.4% | 27.3% | 9.1% |
| reversal_5_vol_scaled | 30 | market | 18 | 10 | 40.0% | 32.0% | 8.0% |
| reversal_5_vol_scaled | 30 | market | 19 | 9 | 33.3% | 22.2% | 11.1% |
| reversal_5_vol_scaled | 30 | market | 20 | 7 | 0.0% | 21.4% | -21.4% |
| reversal_5_vol_scaled | 30 | market | 21 | 11 | 54.5% | 44.8% | 9.7% |
| reversal_5_vol_scaled | 30 | market | 22 | 13 | 46.2% | 38.5% | 7.7% |
| reversal_5_vol_scaled | 30 | market | 23 | 15 | 53.3% | 44.4% | 8.9% |
| reversal_5_vol_scaled | 30 | market | 24 | 11 | 63.6% | 50.0% | 13.6% |
| reversal_5_vol_scaled | 30 | market | 25 | 12 | 58.3% | 46.4% | 11.9% |
| reversal_5_vol_scaled | 30 | market | 26 | 12 | 58.3% | 50.0% | 8.3% |
| reversal_5_vol_scaled | 30 | market | 27 | 11 | 54.5% | 60.6% | -6.1% |
| reversal_5_vol_scaled | 30 | market | 28 | 11 | 18.2% | 18.2% | 0.0% |
| reversal_5_vol_scaled | 30 | market | 29 | 11 | 27.3% | 27.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 0 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 1 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 2 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 3 | 23 | 17.4% | 17.4% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 4 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 5 | 23 | 13.0% | 13.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 6 | 23 | 13.0% | 13.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 7 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 8 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 9 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 10 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 11 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 12 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 13 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 14 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 15 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 16 | 23 | 17.4% | 17.4% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 17 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 18 | 22 | 13.6% | 13.6% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 19 | 22 | 18.2% | 18.2% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 20 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 21 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 22 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 23 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 24 | 23 | 4.3% | 4.3% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 25 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 26 | 23 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 27 | 23 | 13.0% | 13.0% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 28 | 23 | 8.7% | 8.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 29 | 23 | 4.3% | 4.3% | 0.0% |
| rs_range_5_20 | 3 | volatility | 0 | 238 | 42.9% | 41.7% | 1.2% |
| rs_range_5_20 | 3 | volatility | 1 | 238 | 48.7% | 43.2% | 5.6% |
| rs_range_5_20 | 3 | volatility | 2 | 239 | 46.0% | 43.0% | 3.0% |
| rs_range_5_20 | 7 | volatility | 0 | 102 | 52.0% | 42.0% | 10.0% |
| rs_range_5_20 | 7 | volatility | 1 | 102 | 46.1% | 41.1% | 5.0% |
| rs_range_5_20 | 7 | volatility | 2 | 102 | 37.3% | 38.5% | -1.3% |
| rs_range_5_20 | 7 | volatility | 3 | 101 | 47.5% | 40.7% | 6.9% |
| rs_range_5_20 | 7 | volatility | 4 | 101 | 47.5% | 39.9% | 7.6% |
| rs_range_5_20 | 7 | volatility | 5 | 101 | 48.5% | 44.0% | 4.5% |
| rs_range_5_20 | 7 | volatility | 6 | 102 | 50.0% | 41.5% | 8.5% |
| rs_range_5_20 | 14 | volatility | 0 | 50 | 46.0% | 44.5% | 1.5% |
| rs_range_5_20 | 14 | volatility | 1 | 50 | 46.0% | 41.9% | 4.1% |
| rs_range_5_20 | 14 | volatility | 2 | 50 | 48.0% | 41.3% | 6.7% |
| rs_range_5_20 | 14 | volatility | 3 | 50 | 46.0% | 43.7% | 2.3% |
| rs_range_5_20 | 14 | volatility | 4 | 50 | 50.0% | 44.2% | 5.8% |
| rs_range_5_20 | 14 | volatility | 5 | 50 | 52.0% | 42.8% | 9.2% |
| rs_range_5_20 | 14 | volatility | 6 | 51 | 49.0% | 39.5% | 9.5% |
| rs_range_5_20 | 14 | volatility | 7 | 51 | 41.2% | 38.9% | 2.3% |
| rs_range_5_20 | 14 | volatility | 8 | 51 | 35.3% | 36.6% | -1.3% |
| rs_range_5_20 | 14 | volatility | 9 | 51 | 39.2% | 34.7% | 4.5% |
| rs_range_5_20 | 14 | volatility | 10 | 50 | 42.0% | 35.4% | 6.6% |
| rs_range_5_20 | 14 | volatility | 11 | 50 | 50.0% | 36.0% | 14.0% |
| rs_range_5_20 | 14 | volatility | 12 | 50 | 54.0% | 43.9% | 10.1% |
| rs_range_5_20 | 14 | volatility | 13 | 50 | 48.0% | 39.6% | 8.4% |
| rs_range_5_20 | 30 | volatility | 0 | 23 | 60.9% | 44.9% | 15.9% |
| rs_range_5_20 | 30 | volatility | 1 | 23 | 60.9% | 44.1% | 16.8% |
| rs_range_5_20 | 30 | volatility | 2 | 23 | 56.5% | 40.7% | 15.8% |
| rs_range_5_20 | 30 | volatility | 3 | 23 | 56.5% | 36.9% | 19.6% |
| rs_range_5_20 | 30 | volatility | 4 | 23 | 56.5% | 38.3% | 18.2% |
| rs_range_5_20 | 30 | volatility | 5 | 23 | 60.9% | 42.5% | 18.4% |
| rs_range_5_20 | 30 | volatility | 6 | 23 | 60.9% | 42.1% | 18.8% |
| rs_range_5_20 | 30 | volatility | 7 | 23 | 60.9% | 59.4% | 1.4% |
| rs_range_5_20 | 30 | volatility | 8 | 23 | 47.8% | 40.0% | 7.8% |
| rs_range_5_20 | 30 | volatility | 9 | 23 | 47.8% | 32.5% | 15.3% |
| rs_range_5_20 | 30 | volatility | 10 | 23 | 43.5% | 38.4% | 5.1% |
| rs_range_5_20 | 30 | volatility | 11 | 23 | 34.8% | 32.9% | 1.9% |
| rs_range_5_20 | 30 | volatility | 12 | 23 | 39.1% | 38.3% | 0.9% |
| rs_range_5_20 | 30 | volatility | 13 | 23 | 43.5% | 33.5% | 10.0% |
| rs_range_5_20 | 30 | volatility | 14 | 23 | 47.8% | 38.8% | 9.1% |
| rs_range_5_20 | 30 | volatility | 15 | 23 | 39.1% | 35.8% | 3.3% |
| rs_range_5_20 | 30 | volatility | 16 | 23 | 65.2% | 51.6% | 13.6% |
| rs_range_5_20 | 30 | volatility | 17 | 23 | 56.5% | 42.3% | 14.2% |
| rs_range_5_20 | 30 | volatility | 18 | 22 | 36.4% | 42.4% | -6.1% |
| rs_range_5_20 | 30 | volatility | 19 | 22 | 40.9% | 37.4% | 3.5% |
| rs_range_5_20 | 30 | volatility | 20 | 23 | 47.8% | 44.7% | 3.2% |
| rs_range_5_20 | 30 | volatility | 21 | 23 | 39.1% | 39.0% | 0.1% |
| rs_range_5_20 | 30 | volatility | 22 | 23 | 43.5% | 40.1% | 3.4% |
| rs_range_5_20 | 30 | volatility | 23 | 23 | 39.1% | 38.7% | 0.4% |
| rs_range_5_20 | 30 | volatility | 24 | 23 | 39.1% | 38.1% | 1.0% |
| rs_range_5_20 | 30 | volatility | 25 | 23 | 43.5% | 38.8% | 4.6% |
| rs_range_5_20 | 30 | volatility | 26 | 23 | 56.5% | 45.2% | 11.3% |
| rs_range_5_20 | 30 | volatility | 27 | 23 | 30.4% | 30.8% | -0.4% |
| rs_range_5_20 | 30 | volatility | 28 | 23 | 47.8% | 37.4% | 10.4% |
| rs_range_5_20 | 30 | volatility | 29 | 23 | 56.5% | 45.7% | 10.9% |
| rv_20_60_ratio | 3 | volatility | 0 | 225 | 46.2% | 43.6% | 2.6% |
| rv_20_60_ratio | 3 | volatility | 1 | 225 | 49.3% | 46.2% | 3.2% |
| rv_20_60_ratio | 3 | volatility | 2 | 225 | 41.8% | 42.4% | -0.6% |
| rv_20_60_ratio | 7 | volatility | 0 | 96 | 38.5% | 37.7% | 0.8% |
| rv_20_60_ratio | 7 | volatility | 1 | 96 | 32.3% | 32.9% | -0.6% |
| rv_20_60_ratio | 7 | volatility | 2 | 96 | 33.3% | 32.4% | 0.9% |
| rv_20_60_ratio | 7 | volatility | 3 | 95 | 35.8% | 35.2% | 0.6% |
| rv_20_60_ratio | 7 | volatility | 4 | 96 | 37.5% | 34.7% | 2.8% |
| rv_20_60_ratio | 7 | volatility | 5 | 96 | 39.6% | 36.6% | 3.0% |
| rv_20_60_ratio | 7 | volatility | 6 | 96 | 44.8% | 42.0% | 2.7% |
| rv_20_60_ratio | 14 | volatility | 0 | 47 | 40.4% | 39.6% | 0.9% |
| rv_20_60_ratio | 14 | volatility | 1 | 47 | 27.7% | 33.1% | -5.4% |
| rv_20_60_ratio | 14 | volatility | 2 | 47 | 29.8% | 32.7% | -2.9% |
| rv_20_60_ratio | 14 | volatility | 3 | 47 | 29.8% | 29.6% | 0.2% |
| rv_20_60_ratio | 14 | volatility | 4 | 48 | 29.2% | 29.9% | -0.8% |
| rv_20_60_ratio | 14 | volatility | 5 | 48 | 33.3% | 33.5% | -0.1% |
| rv_20_60_ratio | 14 | volatility | 6 | 48 | 33.3% | 34.9% | -1.5% |
| rv_20_60_ratio | 14 | volatility | 7 | 48 | 27.1% | 29.1% | -2.0% |
| rv_20_60_ratio | 14 | volatility | 8 | 48 | 22.9% | 23.8% | -0.8% |
| rv_20_60_ratio | 14 | volatility | 9 | 48 | 31.2% | 30.1% | 1.2% |
| rv_20_60_ratio | 14 | volatility | 10 | 47 | 34.0% | 30.6% | 3.5% |
| rv_20_60_ratio | 14 | volatility | 11 | 47 | 34.0% | 35.6% | -1.5% |
| rv_20_60_ratio | 14 | volatility | 12 | 47 | 29.8% | 31.3% | -1.6% |
| rv_20_60_ratio | 14 | volatility | 13 | 47 | 40.4% | 39.5% | 0.9% |
| rv_20_60_ratio | 30 | volatility | 0 | 22 | 27.3% | 25.7% | 1.6% |
| rv_20_60_ratio | 30 | volatility | 1 | 22 | 36.4% | 31.1% | 5.3% |
| rv_20_60_ratio | 30 | volatility | 2 | 22 | 40.9% | 34.3% | 6.6% |
| rv_20_60_ratio | 30 | volatility | 3 | 22 | 27.3% | 31.8% | -4.5% |
| rv_20_60_ratio | 30 | volatility | 4 | 22 | 22.7% | 29.9% | -7.1% |
| rv_20_60_ratio | 30 | volatility | 5 | 22 | 22.7% | 28.3% | -5.6% |
| rv_20_60_ratio | 30 | volatility | 6 | 22 | 27.3% | 32.5% | -5.2% |
| rv_20_60_ratio | 30 | volatility | 7 | 22 | 22.7% | 25.8% | -3.0% |
| rv_20_60_ratio | 30 | volatility | 8 | 22 | 31.8% | 37.4% | -5.6% |
| rv_20_60_ratio | 30 | volatility | 9 | 22 | 27.3% | 33.9% | -6.6% |
| rv_20_60_ratio | 30 | volatility | 10 | 22 | 22.7% | 26.5% | -3.8% |
| rv_20_60_ratio | 30 | volatility | 11 | 22 | 27.3% | 34.4% | -7.2% |
| rv_20_60_ratio | 30 | volatility | 12 | 22 | 22.7% | 34.5% | -11.8% |
| rv_20_60_ratio | 30 | volatility | 13 | 22 | 36.4% | 46.4% | -10.0% |
| rv_20_60_ratio | 30 | volatility | 14 | 22 | 36.4% | 38.6% | -2.3% |
| rv_20_60_ratio | 30 | volatility | 15 | 22 | 40.9% | 32.1% | 8.8% |
| rv_20_60_ratio | 30 | volatility | 16 | 22 | 22.7% | 22.4% | 0.3% |
| rv_20_60_ratio | 30 | volatility | 17 | 22 | 36.4% | 28.3% | 8.0% |
| rv_20_60_ratio | 30 | volatility | 18 | 21 | 28.6% | 24.6% | 4.0% |
| rv_20_60_ratio | 30 | volatility | 19 | 21 | 19.0% | 20.0% | -1.0% |
| rv_20_60_ratio | 30 | volatility | 20 | 21 | 14.3% | 24.7% | -10.4% |
| rv_20_60_ratio | 30 | volatility | 21 | 21 | 14.3% | 20.6% | -6.3% |
| rv_20_60_ratio | 30 | volatility | 22 | 21 | 28.6% | 22.1% | 6.5% |
| rv_20_60_ratio | 30 | volatility | 23 | 21 | 19.0% | 26.0% | -6.9% |
| rv_20_60_ratio | 30 | volatility | 24 | 21 | 14.3% | 25.3% | -11.0% |
| rv_20_60_ratio | 30 | volatility | 25 | 21 | 14.3% | 32.2% | -17.9% |
| rv_20_60_ratio | 30 | volatility | 26 | 21 | 14.3% | 23.3% | -9.0% |
| rv_20_60_ratio | 30 | volatility | 27 | 21 | 14.3% | 19.8% | -5.6% |
| rv_20_60_ratio | 30 | volatility | 28 | 21 | 23.8% | 18.6% | 5.2% |
| rv_20_60_ratio | 30 | volatility | 29 | 21 | 33.3% | 25.3% | 8.0% |
| rv_acceleration | 3 | volatility | 0 | 238 | 55.9% | 54.2% | 1.7% |
| rv_acceleration | 3 | volatility | 1 | 238 | 55.0% | 53.1% | 1.9% |
| rv_acceleration | 3 | volatility | 2 | 239 | 54.0% | 53.0% | 1.0% |
| rv_acceleration | 7 | volatility | 0 | 102 | 51.0% | 46.9% | 4.0% |
| rv_acceleration | 7 | volatility | 1 | 102 | 50.0% | 50.0% | 0.0% |
| rv_acceleration | 7 | volatility | 2 | 102 | 44.1% | 45.0% | -0.8% |
| rv_acceleration | 7 | volatility | 3 | 101 | 43.6% | 48.0% | -4.4% |
| rv_acceleration | 7 | volatility | 4 | 101 | 46.5% | 47.6% | -1.1% |
| rv_acceleration | 7 | volatility | 5 | 101 | 51.5% | 50.1% | 1.4% |
| rv_acceleration | 7 | volatility | 6 | 102 | 47.1% | 47.7% | -0.6% |
| rv_acceleration | 14 | volatility | 0 | 50 | 62.0% | 48.6% | 13.4% |
| rv_acceleration | 14 | volatility | 1 | 50 | 48.0% | 44.0% | 4.0% |
| rv_acceleration | 14 | volatility | 2 | 50 | 54.0% | 44.3% | 9.7% |
| rv_acceleration | 14 | volatility | 3 | 50 | 50.0% | 50.1% | -0.1% |
| rv_acceleration | 14 | volatility | 4 | 50 | 50.0% | 44.6% | 5.4% |
| rv_acceleration | 14 | volatility | 5 | 50 | 52.0% | 45.0% | 7.0% |
| rv_acceleration | 14 | volatility | 6 | 51 | 37.3% | 41.5% | -4.3% |
| rv_acceleration | 14 | volatility | 7 | 51 | 39.2% | 38.3% | 0.9% |
| rv_acceleration | 14 | volatility | 8 | 51 | 54.9% | 45.6% | 9.3% |
| rv_acceleration | 14 | volatility | 9 | 51 | 45.1% | 41.3% | 3.8% |
| rv_acceleration | 14 | volatility | 10 | 50 | 40.0% | 40.2% | -0.2% |
| rv_acceleration | 14 | volatility | 11 | 50 | 48.0% | 45.7% | 2.3% |
| rv_acceleration | 14 | volatility | 12 | 50 | 52.0% | 42.6% | 9.4% |
| rv_acceleration | 14 | volatility | 13 | 50 | 50.0% | 43.5% | 6.5% |
| rv_acceleration | 30 | volatility | 0 | 23 | 47.8% | 43.1% | 4.8% |
| rv_acceleration | 30 | volatility | 1 | 23 | 47.8% | 41.4% | 6.4% |
| rv_acceleration | 30 | volatility | 2 | 23 | 47.8% | 41.0% | 6.9% |
| rv_acceleration | 30 | volatility | 3 | 23 | 56.5% | 41.4% | 15.1% |
| rv_acceleration | 30 | volatility | 4 | 23 | 60.9% | 42.1% | 18.8% |
| rv_acceleration | 30 | volatility | 5 | 23 | 60.9% | 46.9% | 14.0% |
| rv_acceleration | 30 | volatility | 6 | 23 | 60.9% | 44.1% | 16.7% |
| rv_acceleration | 30 | volatility | 7 | 23 | 56.5% | 52.2% | 4.3% |
| rv_acceleration | 30 | volatility | 8 | 23 | 60.9% | 51.7% | 9.1% |
| rv_acceleration | 30 | volatility | 9 | 23 | 52.2% | 41.9% | 10.2% |
| rv_acceleration | 30 | volatility | 10 | 23 | 47.8% | 53.6% | -5.8% |
| rv_acceleration | 30 | volatility | 11 | 23 | 43.5% | 47.1% | -3.7% |
| rv_acceleration | 30 | volatility | 12 | 23 | 39.1% | 46.7% | -7.6% |
| rv_acceleration | 30 | volatility | 13 | 23 | 47.8% | 45.9% | 2.0% |
| rv_acceleration | 30 | volatility | 14 | 23 | 52.2% | 47.1% | 5.1% |
| rv_acceleration | 30 | volatility | 15 | 23 | 43.5% | 35.5% | 8.0% |
| rv_acceleration | 30 | volatility | 16 | 23 | 43.5% | 34.2% | 9.3% |
| rv_acceleration | 30 | volatility | 17 | 23 | 52.2% | 38.0% | 14.2% |
| rv_acceleration | 30 | volatility | 18 | 22 | 40.9% | 39.0% | 1.9% |
| rv_acceleration | 30 | volatility | 19 | 22 | 40.9% | 27.7% | 13.2% |
| rv_acceleration | 30 | volatility | 20 | 23 | 47.8% | 40.8% | 7.0% |
| rv_acceleration | 30 | volatility | 21 | 23 | 39.1% | 39.6% | -0.4% |
| rv_acceleration | 30 | volatility | 22 | 23 | 52.2% | 41.3% | 10.9% |
| rv_acceleration | 30 | volatility | 23 | 23 | 43.5% | 40.4% | 3.1% |
| rv_acceleration | 30 | volatility | 24 | 23 | 39.1% | 37.7% | 1.5% |
| rv_acceleration | 30 | volatility | 25 | 23 | 43.5% | 38.7% | 4.8% |
| rv_acceleration | 30 | volatility | 26 | 23 | 60.9% | 51.3% | 9.6% |
| rv_acceleration | 30 | volatility | 27 | 23 | 47.8% | 40.6% | 7.2% |
| rv_acceleration | 30 | volatility | 28 | 23 | 30.4% | 35.7% | -5.2% |
| rv_acceleration | 30 | volatility | 29 | 23 | 34.8% | 45.5% | -10.7% |
| trend_efficiency_20 | 3 | volatility | 0 | 238 | 29.8% | 28.5% | 1.3% |
| trend_efficiency_20 | 3 | volatility | 1 | 238 | 31.5% | 28.7% | 2.8% |
| trend_efficiency_20 | 3 | volatility | 2 | 239 | 29.7% | 27.7% | 2.0% |
| trend_efficiency_20 | 7 | volatility | 0 | 102 | 33.3% | 33.2% | 0.1% |
| trend_efficiency_20 | 7 | volatility | 1 | 102 | 37.3% | 34.1% | 3.2% |
| trend_efficiency_20 | 7 | volatility | 2 | 102 | 34.3% | 33.9% | 0.5% |
| trend_efficiency_20 | 7 | volatility | 3 | 101 | 38.6% | 31.7% | 6.9% |
| trend_efficiency_20 | 7 | volatility | 4 | 101 | 32.7% | 32.0% | 0.7% |
| trend_efficiency_20 | 7 | volatility | 5 | 101 | 30.7% | 31.6% | -0.9% |
| trend_efficiency_20 | 7 | volatility | 6 | 102 | 33.3% | 31.1% | 2.2% |
| trend_efficiency_20 | 14 | volatility | 0 | 50 | 44.0% | 38.7% | 5.3% |
| trend_efficiency_20 | 14 | volatility | 1 | 50 | 36.0% | 38.6% | -2.6% |
| trend_efficiency_20 | 14 | volatility | 2 | 50 | 40.0% | 33.3% | 6.7% |
| trend_efficiency_20 | 14 | volatility | 3 | 50 | 34.0% | 32.7% | 1.3% |
| trend_efficiency_20 | 14 | volatility | 4 | 50 | 28.0% | 29.7% | -1.7% |
| trend_efficiency_20 | 14 | volatility | 5 | 50 | 28.0% | 33.1% | -5.1% |
| trend_efficiency_20 | 14 | volatility | 6 | 51 | 29.4% | 33.8% | -4.4% |
| trend_efficiency_20 | 14 | volatility | 7 | 51 | 25.5% | 35.6% | -10.1% |
| trend_efficiency_20 | 14 | volatility | 8 | 51 | 35.3% | 36.7% | -1.4% |
| trend_efficiency_20 | 14 | volatility | 9 | 51 | 35.3% | 37.9% | -2.7% |
| trend_efficiency_20 | 14 | volatility | 10 | 50 | 40.0% | 36.3% | 3.7% |
| trend_efficiency_20 | 14 | volatility | 11 | 50 | 34.0% | 37.9% | -3.9% |
| trend_efficiency_20 | 14 | volatility | 12 | 50 | 32.0% | 35.2% | -3.2% |
| trend_efficiency_20 | 14 | volatility | 13 | 50 | 34.0% | 33.5% | 0.5% |
| trend_efficiency_20 | 30 | volatility | 0 | 23 | 30.4% | 34.6% | -4.2% |
| trend_efficiency_20 | 30 | volatility | 1 | 23 | 39.1% | 39.3% | -0.2% |
| trend_efficiency_20 | 30 | volatility | 2 | 23 | 43.5% | 36.0% | 7.5% |
| trend_efficiency_20 | 30 | volatility | 3 | 23 | 34.8% | 43.0% | -8.2% |
| trend_efficiency_20 | 30 | volatility | 4 | 23 | 34.8% | 36.1% | -1.3% |
| trend_efficiency_20 | 30 | volatility | 5 | 23 | 43.5% | 32.4% | 11.1% |
| trend_efficiency_20 | 30 | volatility | 6 | 23 | 39.1% | 35.7% | 3.4% |
| trend_efficiency_20 | 30 | volatility | 7 | 23 | 34.8% | 40.6% | -5.8% |
| trend_efficiency_20 | 30 | volatility | 8 | 23 | 34.8% | 34.5% | 0.2% |
| trend_efficiency_20 | 30 | volatility | 9 | 23 | 30.4% | 32.7% | -2.3% |
| trend_efficiency_20 | 30 | volatility | 10 | 23 | 30.4% | 31.9% | -1.4% |
| trend_efficiency_20 | 30 | volatility | 11 | 23 | 30.4% | 37.1% | -6.7% |
| trend_efficiency_20 | 30 | volatility | 12 | 23 | 30.4% | 41.7% | -11.3% |
| trend_efficiency_20 | 30 | volatility | 13 | 23 | 43.5% | 50.9% | -7.4% |
| trend_efficiency_20 | 30 | volatility | 14 | 23 | 39.1% | 42.4% | -3.3% |
| trend_efficiency_20 | 30 | volatility | 15 | 23 | 43.5% | 46.0% | -2.5% |
| trend_efficiency_20 | 30 | volatility | 16 | 23 | 34.8% | 31.9% | 2.9% |
| trend_efficiency_20 | 30 | volatility | 17 | 23 | 34.8% | 30.4% | 4.3% |
| trend_efficiency_20 | 30 | volatility | 18 | 22 | 45.5% | 39.0% | 6.4% |
| trend_efficiency_20 | 30 | volatility | 19 | 22 | 31.8% | 31.8% | 0.0% |
| trend_efficiency_20 | 30 | volatility | 20 | 23 | 30.4% | 34.8% | -4.4% |
| trend_efficiency_20 | 30 | volatility | 21 | 23 | 39.1% | 40.2% | -1.1% |
| trend_efficiency_20 | 30 | volatility | 22 | 23 | 34.8% | 25.9% | 8.9% |
| trend_efficiency_20 | 30 | volatility | 23 | 23 | 39.1% | 33.4% | 5.7% |
| trend_efficiency_20 | 30 | volatility | 24 | 23 | 47.8% | 37.1% | 10.7% |
| trend_efficiency_20 | 30 | volatility | 25 | 23 | 52.2% | 39.8% | 12.4% |
| trend_efficiency_20 | 30 | volatility | 26 | 23 | 47.8% | 38.7% | 9.1% |
| trend_efficiency_20 | 30 | volatility | 27 | 23 | 34.8% | 29.3% | 5.4% |
| trend_efficiency_20 | 30 | volatility | 28 | 23 | 43.5% | 42.6% | 0.9% |
| trend_efficiency_20 | 30 | volatility | 29 | 23 | 39.1% | 38.2% | 1.0% |
| usdils_change_5d | 3 | market | 0 | 206 | 52.4% | 51.8% | 0.6% |
| usdils_change_5d | 3 | market | 1 | 210 | 45.2% | 50.0% | -4.8% |
| usdils_change_5d | 3 | market | 2 | 214 | 55.1% | 51.2% | 3.9% |
| usdils_change_5d | 3 | volatility | 0 | 238 | 45.8% | 43.6% | 2.2% |
| usdils_change_5d | 3 | volatility | 1 | 238 | 44.5% | 41.8% | 2.8% |
| usdils_change_5d | 3 | volatility | 2 | 239 | 50.6% | 44.2% | 6.4% |
| usdils_change_5d | 7 | market | 0 | 85 | 47.1% | 52.6% | -5.5% |
| usdils_change_5d | 7 | market | 1 | 92 | 53.3% | 53.0% | 0.2% |
| usdils_change_5d | 7 | market | 2 | 94 | 45.7% | 49.2% | -3.4% |
| usdils_change_5d | 7 | market | 3 | 90 | 45.6% | 50.7% | -5.2% |
| usdils_change_5d | 7 | market | 4 | 93 | 45.2% | 50.0% | -4.9% |
| usdils_change_5d | 7 | market | 5 | 88 | 50.0% | 49.7% | 0.3% |
| usdils_change_5d | 7 | market | 6 | 85 | 54.1% | 52.1% | 2.1% |
| usdils_change_5d | 7 | volatility | 0 | 102 | 42.2% | 40.1% | 2.1% |
| usdils_change_5d | 7 | volatility | 1 | 102 | 45.1% | 43.2% | 1.9% |
| usdils_change_5d | 7 | volatility | 2 | 102 | 41.2% | 43.6% | -2.4% |
| usdils_change_5d | 7 | volatility | 3 | 101 | 42.6% | 40.5% | 2.1% |
| usdils_change_5d | 7 | volatility | 4 | 101 | 52.5% | 41.7% | 10.8% |
| usdils_change_5d | 7 | volatility | 5 | 101 | 48.5% | 41.8% | 6.8% |
| usdils_change_5d | 7 | volatility | 6 | 102 | 50.0% | 41.1% | 8.9% |
| usdils_change_5d | 14 | market | 0 | 44 | 68.2% | 55.0% | 13.2% |
| usdils_change_5d | 14 | market | 1 | 47 | 53.2% | 51.9% | 1.3% |
| usdils_change_5d | 14 | market | 2 | 45 | 64.4% | 56.9% | 7.6% |
| usdils_change_5d | 14 | market | 3 | 45 | 42.2% | 51.2% | -9.0% |
| usdils_change_5d | 14 | market | 4 | 47 | 44.7% | 50.5% | -5.8% |
| usdils_change_5d | 14 | market | 5 | 42 | 52.4% | 48.4% | 4.0% |
| usdils_change_5d | 14 | market | 6 | 40 | 57.5% | 52.5% | 5.0% |
| usdils_change_5d | 14 | market | 7 | 40 | 42.5% | 44.8% | -2.3% |
| usdils_change_5d | 14 | market | 8 | 44 | 54.5% | 52.3% | 2.3% |
| usdils_change_5d | 14 | market | 9 | 48 | 54.2% | 50.6% | 3.5% |
| usdils_change_5d | 14 | market | 10 | 44 | 54.5% | 51.4% | 3.1% |
| usdils_change_5d | 14 | market | 11 | 45 | 55.6% | 48.6% | 7.0% |
| usdils_change_5d | 14 | market | 12 | 45 | 57.8% | 52.6% | 5.2% |
| usdils_change_5d | 14 | market | 13 | 44 | 54.5% | 52.7% | 1.8% |
| usdils_change_5d | 14 | volatility | 0 | 50 | 56.0% | 45.7% | 10.3% |
| usdils_change_5d | 14 | volatility | 1 | 50 | 52.0% | 44.1% | 7.9% |
| usdils_change_5d | 14 | volatility | 2 | 50 | 42.0% | 41.8% | 0.2% |
| usdils_change_5d | 14 | volatility | 3 | 50 | 40.0% | 42.5% | -2.5% |
| usdils_change_5d | 14 | volatility | 4 | 50 | 44.0% | 45.5% | -1.5% |
| usdils_change_5d | 14 | volatility | 5 | 50 | 44.0% | 37.7% | 6.3% |
| usdils_change_5d | 14 | volatility | 6 | 51 | 35.3% | 35.2% | 0.1% |
| usdils_change_5d | 14 | volatility | 7 | 51 | 21.6% | 30.2% | -8.6% |
| usdils_change_5d | 14 | volatility | 8 | 51 | 41.2% | 36.9% | 4.3% |
| usdils_change_5d | 14 | volatility | 9 | 51 | 52.9% | 42.4% | 10.5% |
| usdils_change_5d | 14 | volatility | 10 | 50 | 54.0% | 38.1% | 15.9% |
| usdils_change_5d | 14 | volatility | 11 | 50 | 62.0% | 39.7% | 22.3% |
| usdils_change_5d | 14 | volatility | 12 | 50 | 58.0% | 41.1% | 16.9% |
| usdils_change_5d | 14 | volatility | 13 | 50 | 58.0% | 43.7% | 14.3% |
| usdils_change_5d | 30 | market | 0 | 20 | 60.0% | 63.3% | -3.3% |
| usdils_change_5d | 30 | market | 1 | 22 | 63.6% | 62.4% | 1.2% |
| usdils_change_5d | 30 | market | 2 | 22 | 59.1% | 58.2% | 0.9% |
| usdils_change_5d | 30 | market | 3 | 22 | 63.6% | 55.2% | 8.5% |
| usdils_change_5d | 30 | market | 4 | 22 | 50.0% | 50.0% | 0.0% |
| usdils_change_5d | 30 | market | 5 | 23 | 65.2% | 48.1% | 17.1% |
| usdils_change_5d | 30 | market | 6 | 21 | 38.1% | 53.0% | -14.9% |
| usdils_change_5d | 30 | market | 7 | 19 | 36.8% | 38.6% | -1.8% |
| usdils_change_5d | 30 | market | 8 | 20 | 65.0% | 49.0% | 16.0% |
| usdils_change_5d | 30 | market | 9 | 18 | 50.0% | 43.7% | 6.3% |
| usdils_change_5d | 30 | market | 10 | 21 | 42.9% | 44.8% | -1.9% |
| usdils_change_5d | 30 | market | 11 | 18 | 33.3% | 47.5% | -14.2% |
| usdils_change_5d | 30 | market | 12 | 18 | 55.6% | 54.4% | 1.1% |
| usdils_change_5d | 30 | market | 13 | 21 | 42.9% | 49.5% | -6.7% |
| usdils_change_5d | 30 | market | 14 | 19 | 73.7% | 58.9% | 14.7% |
| usdils_change_5d | 30 | market | 15 | 18 | 66.7% | 56.5% | 10.2% |
| usdils_change_5d | 30 | market | 16 | 18 | 72.2% | 61.1% | 11.1% |
| usdils_change_5d | 30 | market | 17 | 20 | 50.0% | 59.2% | -9.2% |
| usdils_change_5d | 30 | market | 18 | 18 | 55.6% | 54.3% | 1.2% |
| usdils_change_5d | 30 | market | 19 | 20 | 50.0% | 45.0% | 5.0% |
| usdils_change_5d | 30 | market | 20 | 22 | 54.5% | 56.7% | -2.1% |
| usdils_change_5d | 30 | market | 21 | 22 | 45.5% | 49.1% | -3.6% |
| usdils_change_5d | 30 | market | 22 | 21 | 42.9% | 55.2% | -12.4% |
| usdils_change_5d | 30 | market | 23 | 20 | 55.0% | 52.9% | 2.1% |
| usdils_change_5d | 30 | market | 24 | 20 | 50.0% | 51.7% | -1.7% |
| usdils_change_5d | 30 | market | 25 | 18 | 27.8% | 41.9% | -14.1% |
| usdils_change_5d | 30 | market | 26 | 20 | 35.0% | 50.0% | -15.0% |
| usdils_change_5d | 30 | market | 27 | 21 | 28.6% | 49.0% | -20.4% |
| usdils_change_5d | 30 | market | 28 | 19 | 42.1% | 51.5% | -9.4% |
| usdils_change_5d | 30 | market | 29 | 22 | 50.0% | 52.3% | -2.3% |
| usdils_change_5d | 30 | volatility | 0 | 23 | 56.5% | 39.9% | 16.6% |
| usdils_change_5d | 30 | volatility | 1 | 23 | 47.8% | 40.6% | 7.2% |
| usdils_change_5d | 30 | volatility | 2 | 23 | 52.2% | 42.0% | 10.2% |
| usdils_change_5d | 30 | volatility | 3 | 23 | 47.8% | 37.2% | 10.6% |
| usdils_change_5d | 30 | volatility | 4 | 23 | 69.6% | 43.5% | 26.1% |
| usdils_change_5d | 30 | volatility | 5 | 23 | 56.5% | 47.3% | 9.2% |
| usdils_change_5d | 30 | volatility | 6 | 23 | 69.6% | 41.5% | 28.1% |
| usdils_change_5d | 30 | volatility | 7 | 23 | 60.9% | 46.4% | 14.5% |
| usdils_change_5d | 30 | volatility | 8 | 23 | 47.8% | 44.9% | 3.0% |
| usdils_change_5d | 30 | volatility | 9 | 23 | 52.2% | 43.4% | 8.8% |
| usdils_change_5d | 30 | volatility | 10 | 23 | 39.1% | 47.1% | -8.0% |
| usdils_change_5d | 30 | volatility | 11 | 23 | 34.8% | 41.5% | -6.7% |
| usdils_change_5d | 30 | volatility | 12 | 23 | 39.1% | 44.3% | -5.2% |
| usdils_change_5d | 30 | volatility | 13 | 23 | 43.5% | 47.4% | -3.9% |
| usdils_change_5d | 30 | volatility | 14 | 23 | 39.1% | 44.2% | -5.1% |
| usdils_change_5d | 30 | volatility | 15 | 23 | 26.1% | 27.4% | -1.3% |
| usdils_change_5d | 30 | volatility | 16 | 23 | 39.1% | 33.0% | 6.1% |
| usdils_change_5d | 30 | volatility | 17 | 23 | 43.5% | 34.4% | 9.0% |
| usdils_change_5d | 30 | volatility | 18 | 22 | 40.9% | 36.7% | 4.2% |
| usdils_change_5d | 30 | volatility | 19 | 22 | 22.7% | 33.0% | -10.3% |
| usdils_change_5d | 30 | volatility | 20 | 23 | 43.5% | 44.4% | -0.9% |
| usdils_change_5d | 30 | volatility | 21 | 23 | 56.5% | 48.0% | 8.6% |
| usdils_change_5d | 30 | volatility | 22 | 23 | 34.8% | 38.9% | -4.2% |
| usdils_change_5d | 30 | volatility | 23 | 23 | 39.1% | 40.6% | -1.5% |
| usdils_change_5d | 30 | volatility | 24 | 23 | 60.9% | 47.2% | 13.7% |
| usdils_change_5d | 30 | volatility | 25 | 23 | 43.5% | 38.4% | 5.1% |
| usdils_change_5d | 30 | volatility | 26 | 23 | 52.2% | 43.5% | 8.7% |
| usdils_change_5d | 30 | volatility | 27 | 23 | 39.1% | 37.0% | 2.2% |
| usdils_change_5d | 30 | volatility | 28 | 23 | 47.8% | 42.6% | 5.2% |
| usdils_change_5d | 30 | volatility | 29 | 23 | 52.2% | 44.2% | 8.0% |
| vix9d_vix_ratio | 3 | market | 0 | 212 | 59.0% | 59.8% | -0.9% |
| vix9d_vix_ratio | 3 | market | 1 | 212 | 59.9% | 56.3% | 3.6% |
| vix9d_vix_ratio | 3 | market | 2 | 211 | 56.9% | 56.5% | 0.4% |
| vix9d_vix_ratio | 3 | volatility | 0 | 238 | 58.0% | 55.4% | 2.5% |
| vix9d_vix_ratio | 3 | volatility | 1 | 238 | 57.1% | 55.4% | 1.8% |
| vix9d_vix_ratio | 3 | volatility | 2 | 239 | 55.2% | 53.8% | 1.5% |
| vix9d_vix_ratio | 7 | market | 0 | 89 | 57.3% | 60.4% | -3.0% |
| vix9d_vix_ratio | 7 | market | 1 | 92 | 64.1% | 62.0% | 2.2% |
| vix9d_vix_ratio | 7 | market | 2 | 91 | 59.3% | 58.7% | 0.6% |
| vix9d_vix_ratio | 7 | market | 3 | 85 | 54.1% | 53.7% | 0.4% |
| vix9d_vix_ratio | 7 | market | 4 | 98 | 54.1% | 53.4% | 0.7% |
| vix9d_vix_ratio | 7 | market | 5 | 90 | 58.9% | 62.2% | -3.3% |
| vix9d_vix_ratio | 7 | market | 6 | 87 | 56.3% | 60.3% | -4.0% |
| vix9d_vix_ratio | 7 | volatility | 0 | 102 | 50.0% | 44.6% | 5.4% |
| vix9d_vix_ratio | 7 | volatility | 1 | 102 | 50.0% | 43.5% | 6.5% |
| vix9d_vix_ratio | 7 | volatility | 2 | 102 | 46.1% | 40.9% | 5.2% |
| vix9d_vix_ratio | 7 | volatility | 3 | 101 | 48.5% | 45.5% | 3.0% |
| vix9d_vix_ratio | 7 | volatility | 4 | 101 | 52.5% | 46.9% | 5.5% |
| vix9d_vix_ratio | 7 | volatility | 5 | 101 | 52.5% | 46.8% | 5.6% |
| vix9d_vix_ratio | 7 | volatility | 6 | 102 | 46.1% | 45.9% | 0.1% |
| vix9d_vix_ratio | 14 | market | 0 | 44 | 54.5% | 58.1% | -3.6% |
| vix9d_vix_ratio | 14 | market | 1 | 46 | 56.5% | 65.5% | -9.0% |
| vix9d_vix_ratio | 14 | market | 2 | 45 | 66.7% | 69.3% | -2.6% |
| vix9d_vix_ratio | 14 | market | 3 | 42 | 64.3% | 66.1% | -1.8% |
| vix9d_vix_ratio | 14 | market | 4 | 50 | 64.0% | 64.3% | -0.3% |
| vix9d_vix_ratio | 14 | market | 5 | 45 | 64.4% | 64.0% | 0.4% |
| vix9d_vix_ratio | 14 | market | 6 | 41 | 61.0% | 61.1% | -0.1% |
| vix9d_vix_ratio | 14 | market | 7 | 44 | 63.6% | 68.2% | -4.5% |
| vix9d_vix_ratio | 14 | market | 8 | 45 | 64.4% | 60.3% | 4.2% |
| vix9d_vix_ratio | 14 | market | 9 | 45 | 62.2% | 59.1% | 3.1% |
| vix9d_vix_ratio | 14 | market | 10 | 42 | 61.9% | 65.6% | -3.7% |
| vix9d_vix_ratio | 14 | market | 11 | 47 | 57.4% | 63.5% | -6.1% |
| vix9d_vix_ratio | 14 | market | 12 | 44 | 56.8% | 60.1% | -3.3% |
| vix9d_vix_ratio | 14 | market | 13 | 45 | 62.2% | 68.2% | -5.9% |
| vix9d_vix_ratio | 14 | volatility | 0 | 50 | 42.0% | 38.7% | 3.3% |
| vix9d_vix_ratio | 14 | volatility | 1 | 50 | 46.0% | 37.1% | 8.9% |
| vix9d_vix_ratio | 14 | volatility | 2 | 50 | 46.0% | 38.5% | 7.5% |
| vix9d_vix_ratio | 14 | volatility | 3 | 50 | 50.0% | 40.0% | 10.0% |
| vix9d_vix_ratio | 14 | volatility | 4 | 50 | 54.0% | 43.5% | 10.5% |
| vix9d_vix_ratio | 14 | volatility | 5 | 50 | 52.0% | 40.3% | 11.7% |
| vix9d_vix_ratio | 14 | volatility | 6 | 51 | 43.1% | 35.4% | 7.7% |
| vix9d_vix_ratio | 14 | volatility | 7 | 51 | 41.2% | 37.9% | 3.3% |
| vix9d_vix_ratio | 14 | volatility | 8 | 51 | 43.1% | 34.6% | 8.5% |
| vix9d_vix_ratio | 14 | volatility | 9 | 51 | 39.2% | 35.6% | 3.6% |
| vix9d_vix_ratio | 14 | volatility | 10 | 50 | 32.0% | 36.8% | -4.8% |
| vix9d_vix_ratio | 14 | volatility | 11 | 50 | 42.0% | 42.6% | -0.6% |
| vix9d_vix_ratio | 14 | volatility | 12 | 50 | 38.0% | 39.1% | -1.1% |
| vix9d_vix_ratio | 14 | volatility | 13 | 50 | 50.0% | 43.7% | 6.3% |
| vix9d_vix_ratio | 30 | market | 0 | 19 | 57.9% | 65.8% | -7.9% |
| vix9d_vix_ratio | 30 | market | 1 | 20 | 55.0% | 65.0% | -10.0% |
| vix9d_vix_ratio | 30 | market | 2 | 22 | 50.0% | 56.8% | -6.8% |
| vix9d_vix_ratio | 30 | market | 3 | 22 | 54.5% | 61.3% | -6.7% |
| vix9d_vix_ratio | 30 | market | 4 | 19 | 68.4% | 64.9% | 3.5% |
| vix9d_vix_ratio | 30 | market | 5 | 19 | 63.2% | 59.0% | 4.1% |
| vix9d_vix_ratio | 30 | market | 6 | 17 | 47.1% | 60.1% | -13.0% |
| vix9d_vix_ratio | 30 | market | 7 | 20 | 55.0% | 63.0% | -8.0% |
| vix9d_vix_ratio | 30 | market | 8 | 20 | 70.0% | 72.0% | -2.0% |
| vix9d_vix_ratio | 30 | market | 9 | 22 | 63.6% | 72.7% | -9.1% |
| vix9d_vix_ratio | 30 | market | 10 | 20 | 70.0% | 70.0% | -0.0% |
| vix9d_vix_ratio | 30 | market | 11 | 21 | 61.9% | 67.5% | -5.6% |
| vix9d_vix_ratio | 30 | market | 12 | 21 | 66.7% | 71.4% | -4.8% |
| vix9d_vix_ratio | 30 | market | 13 | 23 | 69.6% | 73.0% | -3.5% |
| vix9d_vix_ratio | 30 | market | 14 | 23 | 73.9% | 73.9% | 0.0% |
| vix9d_vix_ratio | 30 | market | 15 | 24 | 66.7% | 66.7% | -0.0% |
| vix9d_vix_ratio | 30 | market | 16 | 20 | 75.0% | 75.0% | 0.0% |
| vix9d_vix_ratio | 30 | market | 17 | 21 | 71.4% | 77.7% | -6.2% |
| vix9d_vix_ratio | 30 | market | 18 | 22 | 72.7% | 72.7% | 0.0% |
| vix9d_vix_ratio | 30 | market | 19 | 22 | 68.2% | 68.2% | -0.0% |
| vix9d_vix_ratio | 30 | market | 20 | 21 | 81.0% | 82.9% | -1.9% |
| vix9d_vix_ratio | 30 | market | 21 | 20 | 70.0% | 72.5% | -2.5% |
| vix9d_vix_ratio | 30 | market | 22 | 20 | 65.0% | 70.2% | -5.2% |
| vix9d_vix_ratio | 30 | market | 23 | 20 | 65.0% | 61.1% | 3.9% |
| vix9d_vix_ratio | 30 | market | 24 | 21 | 57.1% | 63.9% | -6.8% |
| vix9d_vix_ratio | 30 | market | 25 | 19 | 52.6% | 58.9% | -6.3% |
| vix9d_vix_ratio | 30 | market | 26 | 18 | 66.7% | 69.1% | -2.5% |
| vix9d_vix_ratio | 30 | market | 27 | 15 | 53.3% | 63.3% | -10.0% |
| vix9d_vix_ratio | 30 | market | 28 | 20 | 75.0% | 75.0% | 0.0% |
| vix9d_vix_ratio | 30 | market | 29 | 18 | 55.6% | 56.0% | -0.4% |
| vix9d_vix_ratio | 30 | volatility | 0 | 23 | 47.8% | 36.1% | 11.7% |
| vix9d_vix_ratio | 30 | volatility | 1 | 23 | 47.8% | 39.1% | 8.7% |
| vix9d_vix_ratio | 30 | volatility | 2 | 23 | 47.8% | 44.7% | 3.2% |
| vix9d_vix_ratio | 30 | volatility | 3 | 23 | 47.8% | 40.0% | 7.9% |
| vix9d_vix_ratio | 30 | volatility | 4 | 23 | 34.8% | 29.6% | 5.1% |
| vix9d_vix_ratio | 30 | volatility | 5 | 23 | 56.5% | 37.4% | 19.1% |
| vix9d_vix_ratio | 30 | volatility | 6 | 23 | 43.5% | 31.9% | 11.5% |
| vix9d_vix_ratio | 30 | volatility | 7 | 23 | 34.8% | 38.4% | -3.6% |
| vix9d_vix_ratio | 30 | volatility | 8 | 23 | 39.1% | 40.3% | -1.1% |
| vix9d_vix_ratio | 30 | volatility | 9 | 23 | 43.5% | 37.9% | 5.6% |
| vix9d_vix_ratio | 30 | volatility | 10 | 23 | 52.2% | 48.6% | 3.6% |
| vix9d_vix_ratio | 30 | volatility | 11 | 23 | 47.8% | 43.7% | 4.1% |
| vix9d_vix_ratio | 30 | volatility | 12 | 23 | 30.4% | 33.7% | -3.3% |
| vix9d_vix_ratio | 30 | volatility | 13 | 23 | 43.5% | 47.0% | -3.5% |
| vix9d_vix_ratio | 30 | volatility | 14 | 23 | 47.8% | 49.3% | -1.4% |
| vix9d_vix_ratio | 30 | volatility | 15 | 23 | 43.5% | 40.6% | 2.9% |
| vix9d_vix_ratio | 30 | volatility | 16 | 23 | 21.7% | 28.7% | -7.0% |
| vix9d_vix_ratio | 30 | volatility | 17 | 23 | 30.4% | 32.2% | -1.8% |
| vix9d_vix_ratio | 30 | volatility | 18 | 22 | 27.3% | 27.3% | 0.0% |
| vix9d_vix_ratio | 30 | volatility | 19 | 22 | 22.7% | 23.6% | -0.9% |
| vix9d_vix_ratio | 30 | volatility | 20 | 23 | 26.1% | 27.1% | -1.0% |
| vix9d_vix_ratio | 30 | volatility | 21 | 23 | 26.1% | 28.4% | -2.3% |
| vix9d_vix_ratio | 30 | volatility | 22 | 23 | 21.7% | 31.2% | -9.5% |
| vix9d_vix_ratio | 30 | volatility | 23 | 23 | 26.1% | 36.7% | -10.6% |
| vix9d_vix_ratio | 30 | volatility | 24 | 23 | 34.8% | 41.2% | -6.4% |
| vix9d_vix_ratio | 30 | volatility | 25 | 23 | 30.4% | 34.7% | -4.3% |
| vix9d_vix_ratio | 30 | volatility | 26 | 23 | 34.8% | 33.5% | 1.3% |
| vix9d_vix_ratio | 30 | volatility | 27 | 23 | 30.4% | 34.1% | -3.6% |
| vix9d_vix_ratio | 30 | volatility | 28 | 23 | 34.8% | 40.0% | -5.2% |
| vix9d_vix_ratio | 30 | volatility | 29 | 23 | 30.4% | 41.3% | -10.9% |
| vix_curve_ratio | 3 | market | 0 | 237 | 57.0% | 57.9% | -1.0% |
| vix_curve_ratio | 3 | market | 1 | 241 | 57.7% | 56.3% | 1.4% |
| vix_curve_ratio | 3 | market | 2 | 237 | 57.0% | 58.1% | -1.2% |
| vix_curve_ratio | 3 | volatility | 0 | 238 | 68.9% | 64.5% | 4.4% |
| vix_curve_ratio | 3 | volatility | 1 | 238 | 68.1% | 65.7% | 2.4% |
| vix_curve_ratio | 3 | volatility | 2 | 239 | 65.3% | 63.3% | 2.0% |
| vix_curve_ratio | 7 | market | 0 | 101 | 54.5% | 59.5% | -5.0% |
| vix_curve_ratio | 7 | market | 1 | 99 | 60.6% | 63.6% | -3.0% |
| vix_curve_ratio | 7 | market | 2 | 104 | 58.7% | 60.3% | -1.7% |
| vix_curve_ratio | 7 | market | 3 | 103 | 53.4% | 54.0% | -0.6% |
| vix_curve_ratio | 7 | market | 4 | 102 | 54.9% | 52.6% | 2.3% |
| vix_curve_ratio | 7 | market | 5 | 103 | 59.2% | 63.2% | -4.0% |
| vix_curve_ratio | 7 | market | 6 | 99 | 58.6% | 61.8% | -3.3% |
| vix_curve_ratio | 7 | volatility | 0 | 102 | 54.9% | 52.3% | 2.6% |
| vix_curve_ratio | 7 | volatility | 1 | 102 | 52.0% | 47.1% | 4.9% |
| vix_curve_ratio | 7 | volatility | 2 | 102 | 49.0% | 46.9% | 2.1% |
| vix_curve_ratio | 7 | volatility | 3 | 101 | 58.4% | 55.1% | 3.3% |
| vix_curve_ratio | 7 | volatility | 4 | 101 | 55.4% | 50.3% | 5.1% |
| vix_curve_ratio | 7 | volatility | 5 | 101 | 61.4% | 55.2% | 6.2% |
| vix_curve_ratio | 7 | volatility | 6 | 102 | 56.9% | 54.1% | 2.8% |
| vix_curve_ratio | 14 | market | 0 | 51 | 62.7% | 61.4% | 1.3% |
| vix_curve_ratio | 14 | market | 1 | 48 | 64.6% | 66.1% | -1.5% |
| vix_curve_ratio | 14 | market | 2 | 52 | 71.2% | 69.0% | 2.2% |
| vix_curve_ratio | 14 | market | 3 | 51 | 68.6% | 67.8% | 0.8% |
| vix_curve_ratio | 14 | market | 4 | 51 | 64.7% | 64.7% | 0.0% |
| vix_curve_ratio | 14 | market | 5 | 51 | 64.7% | 67.5% | -2.8% |
| vix_curve_ratio | 14 | market | 6 | 47 | 63.8% | 67.8% | -3.9% |
| vix_curve_ratio | 14 | market | 7 | 49 | 67.3% | 68.4% | -1.1% |
| vix_curve_ratio | 14 | market | 8 | 50 | 62.0% | 61.7% | 0.3% |
| vix_curve_ratio | 14 | market | 9 | 51 | 56.9% | 60.6% | -3.7% |
| vix_curve_ratio | 14 | market | 10 | 51 | 66.7% | 67.1% | -0.4% |
| vix_curve_ratio | 14 | market | 11 | 50 | 62.0% | 64.1% | -2.1% |
| vix_curve_ratio | 14 | market | 12 | 51 | 62.7% | 66.0% | -3.3% |
| vix_curve_ratio | 14 | market | 13 | 51 | 74.5% | 73.4% | 1.1% |
| vix_curve_ratio | 14 | volatility | 0 | 50 | 48.0% | 47.1% | 0.9% |
| vix_curve_ratio | 14 | volatility | 1 | 50 | 44.0% | 38.9% | 5.1% |
| vix_curve_ratio | 14 | volatility | 2 | 50 | 52.0% | 46.3% | 5.7% |
| vix_curve_ratio | 14 | volatility | 3 | 50 | 58.0% | 50.5% | 7.5% |
| vix_curve_ratio | 14 | volatility | 4 | 50 | 54.0% | 46.4% | 7.6% |
| vix_curve_ratio | 14 | volatility | 5 | 50 | 58.0% | 46.2% | 11.8% |
| vix_curve_ratio | 14 | volatility | 6 | 51 | 45.1% | 38.9% | 6.2% |
| vix_curve_ratio | 14 | volatility | 7 | 51 | 45.1% | 42.2% | 2.9% |
| vix_curve_ratio | 14 | volatility | 8 | 51 | 41.2% | 36.4% | 4.8% |
| vix_curve_ratio | 14 | volatility | 9 | 51 | 45.1% | 41.7% | 3.4% |
| vix_curve_ratio | 14 | volatility | 10 | 50 | 44.0% | 43.6% | 0.4% |
| vix_curve_ratio | 14 | volatility | 11 | 50 | 48.0% | 45.6% | 2.4% |
| vix_curve_ratio | 14 | volatility | 12 | 50 | 52.0% | 46.2% | 5.8% |
| vix_curve_ratio | 14 | volatility | 13 | 50 | 52.0% | 50.9% | 1.1% |
| vix_curve_ratio | 30 | market | 0 | 24 | 66.7% | 70.4% | -3.7% |
| vix_curve_ratio | 30 | market | 1 | 23 | 65.2% | 69.1% | -3.9% |
| vix_curve_ratio | 30 | market | 2 | 22 | 63.6% | 66.2% | -2.6% |
| vix_curve_ratio | 30 | market | 3 | 23 | 69.6% | 66.7% | 2.9% |
| vix_curve_ratio | 30 | market | 4 | 23 | 69.6% | 65.0% | 4.6% |
| vix_curve_ratio | 30 | market | 5 | 23 | 56.5% | 63.8% | -7.2% |
| vix_curve_ratio | 30 | market | 6 | 22 | 54.5% | 64.2% | -9.6% |
| vix_curve_ratio | 30 | market | 7 | 24 | 62.5% | 66.3% | -3.8% |
| vix_curve_ratio | 30 | market | 8 | 23 | 65.2% | 71.0% | -5.8% |
| vix_curve_ratio | 30 | market | 9 | 22 | 63.6% | 70.9% | -7.3% |
| vix_curve_ratio | 30 | market | 10 | 22 | 72.7% | 72.7% | 0.0% |
| vix_curve_ratio | 30 | market | 11 | 24 | 62.5% | 67.1% | -4.6% |
| vix_curve_ratio | 30 | market | 12 | 24 | 66.7% | 70.0% | -3.3% |
| vix_curve_ratio | 30 | market | 13 | 24 | 75.0% | 75.0% | 0.0% |
| vix_curve_ratio | 30 | market | 14 | 24 | 75.0% | 75.0% | 0.0% |
| vix_curve_ratio | 30 | market | 15 | 23 | 73.9% | 73.9% | 0.0% |
| vix_curve_ratio | 30 | market | 16 | 24 | 79.2% | 79.2% | 0.0% |
| vix_curve_ratio | 30 | market | 17 | 21 | 81.0% | 81.0% | 0.0% |
| vix_curve_ratio | 30 | market | 18 | 23 | 73.9% | 73.9% | 0.0% |
| vix_curve_ratio | 30 | market | 19 | 23 | 69.6% | 69.6% | 0.0% |
| vix_curve_ratio | 30 | market | 20 | 22 | 81.8% | 83.6% | -1.8% |
| vix_curve_ratio | 30 | market | 21 | 22 | 68.2% | 72.7% | -4.5% |
| vix_curve_ratio | 30 | market | 22 | 23 | 69.6% | 72.5% | -2.9% |
| vix_curve_ratio | 30 | market | 23 | 23 | 60.9% | 63.8% | -2.9% |
| vix_curve_ratio | 30 | market | 24 | 23 | 69.6% | 70.8% | -1.2% |
| vix_curve_ratio | 30 | market | 25 | 23 | 65.2% | 68.1% | -2.9% |
| vix_curve_ratio | 30 | market | 26 | 23 | 65.2% | 65.2% | 0.0% |
| vix_curve_ratio | 30 | market | 27 | 22 | 59.1% | 60.9% | -1.8% |
| vix_curve_ratio | 30 | market | 28 | 23 | 78.3% | 78.3% | 0.0% |
| vix_curve_ratio | 30 | market | 29 | 23 | 73.9% | 69.4% | 4.5% |
| vix_curve_ratio | 30 | volatility | 0 | 23 | 56.5% | 48.4% | 8.1% |
| vix_curve_ratio | 30 | volatility | 1 | 23 | 52.2% | 46.8% | 5.3% |
| vix_curve_ratio | 30 | volatility | 2 | 23 | 52.2% | 47.3% | 4.8% |
| vix_curve_ratio | 30 | volatility | 3 | 23 | 47.8% | 36.0% | 11.8% |
| vix_curve_ratio | 30 | volatility | 4 | 23 | 43.5% | 35.6% | 7.9% |
| vix_curve_ratio | 30 | volatility | 5 | 23 | 52.2% | 41.1% | 11.1% |
| vix_curve_ratio | 30 | volatility | 6 | 23 | 47.8% | 37.1% | 10.7% |
| vix_curve_ratio | 30 | volatility | 7 | 23 | 43.5% | 46.4% | -2.9% |
| vix_curve_ratio | 30 | volatility | 8 | 23 | 52.2% | 50.9% | 1.2% |
| vix_curve_ratio | 30 | volatility | 9 | 23 | 47.8% | 40.8% | 7.0% |
| vix_curve_ratio | 30 | volatility | 10 | 23 | 56.5% | 55.1% | 1.4% |
| vix_curve_ratio | 30 | volatility | 11 | 23 | 52.2% | 50.6% | 1.6% |
| vix_curve_ratio | 30 | volatility | 12 | 23 | 43.5% | 45.2% | -1.7% |
| vix_curve_ratio | 30 | volatility | 13 | 23 | 52.2% | 52.2% | 0.0% |
| vix_curve_ratio | 30 | volatility | 14 | 23 | 52.2% | 52.2% | -0.0% |
| vix_curve_ratio | 30 | volatility | 15 | 23 | 39.1% | 40.6% | -1.4% |
| vix_curve_ratio | 30 | volatility | 16 | 23 | 34.8% | 34.8% | 0.0% |
| vix_curve_ratio | 30 | volatility | 17 | 23 | 39.1% | 35.6% | 3.5% |
| vix_curve_ratio | 30 | volatility | 18 | 22 | 31.8% | 31.8% | 0.0% |
| vix_curve_ratio | 30 | volatility | 19 | 22 | 27.3% | 28.2% | -0.9% |
| vix_curve_ratio | 30 | volatility | 20 | 23 | 26.1% | 28.3% | -2.2% |
| vix_curve_ratio | 30 | volatility | 21 | 23 | 34.8% | 32.8% | 2.0% |
| vix_curve_ratio | 30 | volatility | 22 | 23 | 34.8% | 34.8% | 0.0% |
| vix_curve_ratio | 30 | volatility | 23 | 23 | 39.1% | 42.0% | -2.9% |
| vix_curve_ratio | 30 | volatility | 24 | 23 | 43.5% | 44.1% | -0.6% |
| vix_curve_ratio | 30 | volatility | 25 | 23 | 39.1% | 42.0% | -2.9% |
| vix_curve_ratio | 30 | volatility | 26 | 23 | 39.1% | 39.1% | 0.0% |
| vix_curve_ratio | 30 | volatility | 27 | 23 | 30.4% | 32.6% | -2.2% |
| vix_curve_ratio | 30 | volatility | 28 | 23 | 39.1% | 39.1% | 0.0% |
| vix_curve_ratio | 30 | volatility | 29 | 23 | 52.2% | 49.9% | 2.3% |
| vix_vix3m_ratio | 3 | market | 0 | 228 | 57.9% | 58.5% | -0.7% |
| vix_vix3m_ratio | 3 | market | 1 | 234 | 56.8% | 57.5% | -0.7% |
| vix_vix3m_ratio | 3 | market | 2 | 231 | 56.3% | 58.8% | -2.5% |
| vix_vix3m_ratio | 3 | volatility | 0 | 238 | 67.6% | 64.9% | 2.7% |
| vix_vix3m_ratio | 3 | volatility | 1 | 238 | 66.0% | 65.5% | 0.4% |
| vix_vix3m_ratio | 3 | volatility | 2 | 239 | 64.4% | 63.8% | 0.7% |
| vix_vix3m_ratio | 7 | market | 0 | 100 | 57.0% | 59.7% | -2.7% |
| vix_vix3m_ratio | 7 | market | 1 | 100 | 61.0% | 64.5% | -3.5% |
| vix_vix3m_ratio | 7 | market | 2 | 98 | 58.2% | 61.1% | -3.0% |
| vix_vix3m_ratio | 7 | market | 3 | 99 | 51.5% | 53.9% | -2.4% |
| vix_vix3m_ratio | 7 | market | 4 | 97 | 54.6% | 55.1% | -0.5% |
| vix_vix3m_ratio | 7 | market | 5 | 98 | 61.2% | 62.4% | -1.1% |
| vix_vix3m_ratio | 7 | market | 6 | 97 | 59.8% | 61.2% | -1.4% |
| vix_vix3m_ratio | 7 | volatility | 0 | 102 | 55.9% | 53.1% | 2.8% |
| vix_vix3m_ratio | 7 | volatility | 1 | 102 | 50.0% | 49.9% | 0.1% |
| vix_vix3m_ratio | 7 | volatility | 2 | 102 | 46.1% | 45.4% | 0.7% |
| vix_vix3m_ratio | 7 | volatility | 3 | 101 | 54.5% | 54.5% | -0.1% |
| vix_vix3m_ratio | 7 | volatility | 4 | 101 | 53.5% | 50.0% | 3.4% |
| vix_vix3m_ratio | 7 | volatility | 5 | 101 | 58.4% | 54.2% | 4.2% |
| vix_vix3m_ratio | 7 | volatility | 6 | 102 | 55.9% | 53.7% | 2.1% |
| vix_vix3m_ratio | 14 | market | 0 | 51 | 62.7% | 63.7% | -1.0% |
| vix_vix3m_ratio | 14 | market | 1 | 51 | 70.6% | 70.0% | 0.6% |
| vix_vix3m_ratio | 14 | market | 2 | 48 | 70.8% | 67.8% | 3.0% |
| vix_vix3m_ratio | 14 | market | 3 | 49 | 69.4% | 67.1% | 2.3% |
| vix_vix3m_ratio | 14 | market | 4 | 48 | 66.7% | 65.7% | 1.0% |
| vix_vix3m_ratio | 14 | market | 5 | 49 | 67.3% | 66.3% | 1.0% |
| vix_vix3m_ratio | 14 | market | 6 | 46 | 65.2% | 65.2% | 0.0% |
| vix_vix3m_ratio | 14 | market | 7 | 48 | 70.8% | 69.8% | 1.0% |
| vix_vix3m_ratio | 14 | market | 8 | 48 | 62.5% | 63.5% | -1.0% |
| vix_vix3m_ratio | 14 | market | 9 | 49 | 57.1% | 61.6% | -4.5% |
| vix_vix3m_ratio | 14 | market | 10 | 49 | 65.3% | 67.5% | -2.2% |
| vix_vix3m_ratio | 14 | market | 11 | 48 | 62.5% | 65.1% | -2.6% |
| vix_vix3m_ratio | 14 | market | 12 | 48 | 64.6% | 66.4% | -1.8% |
| vix_vix3m_ratio | 14 | market | 13 | 50 | 74.0% | 72.9% | 1.1% |
| vix_vix3m_ratio | 14 | volatility | 0 | 50 | 48.0% | 47.8% | 0.2% |
| vix_vix3m_ratio | 14 | volatility | 1 | 50 | 42.0% | 42.5% | -0.5% |
| vix_vix3m_ratio | 14 | volatility | 2 | 50 | 48.0% | 42.3% | 5.7% |
| vix_vix3m_ratio | 14 | volatility | 3 | 50 | 52.0% | 49.1% | 2.9% |
| vix_vix3m_ratio | 14 | volatility | 4 | 50 | 48.0% | 45.5% | 2.5% |
| vix_vix3m_ratio | 14 | volatility | 5 | 50 | 52.0% | 46.4% | 5.6% |
| vix_vix3m_ratio | 14 | volatility | 6 | 51 | 41.2% | 39.0% | 2.1% |
| vix_vix3m_ratio | 14 | volatility | 7 | 51 | 43.1% | 41.8% | 1.4% |
| vix_vix3m_ratio | 14 | volatility | 8 | 51 | 41.2% | 38.1% | 3.0% |
| vix_vix3m_ratio | 14 | volatility | 9 | 51 | 43.1% | 42.2% | 0.9% |
| vix_vix3m_ratio | 14 | volatility | 10 | 50 | 44.0% | 43.9% | 0.1% |
| vix_vix3m_ratio | 14 | volatility | 11 | 50 | 44.0% | 45.2% | -1.2% |
| vix_vix3m_ratio | 14 | volatility | 12 | 50 | 46.0% | 44.5% | 1.5% |
| vix_vix3m_ratio | 14 | volatility | 13 | 50 | 50.0% | 50.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 0 | 22 | 68.2% | 72.2% | -4.0% |
| vix_vix3m_ratio | 30 | market | 1 | 24 | 70.8% | 74.5% | -3.7% |
| vix_vix3m_ratio | 30 | market | 2 | 21 | 71.4% | 71.4% | 0.0% |
| vix_vix3m_ratio | 30 | market | 3 | 21 | 71.4% | 66.0% | 5.4% |
| vix_vix3m_ratio | 30 | market | 4 | 20 | 70.0% | 66.7% | 3.3% |
| vix_vix3m_ratio | 30 | market | 5 | 22 | 59.1% | 63.6% | -4.5% |
| vix_vix3m_ratio | 30 | market | 6 | 20 | 65.0% | 68.3% | -3.3% |
| vix_vix3m_ratio | 30 | market | 7 | 24 | 58.3% | 66.9% | -8.5% |
| vix_vix3m_ratio | 30 | market | 8 | 22 | 68.2% | 71.8% | -3.6% |
| vix_vix3m_ratio | 30 | market | 9 | 23 | 69.6% | 72.5% | -2.9% |
| vix_vix3m_ratio | 30 | market | 10 | 24 | 75.0% | 75.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 11 | 22 | 68.2% | 68.2% | 0.0% |
| vix_vix3m_ratio | 30 | market | 12 | 23 | 69.6% | 69.6% | 0.0% |
| vix_vix3m_ratio | 30 | market | 13 | 24 | 75.0% | 75.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 14 | 24 | 75.0% | 75.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 15 | 24 | 75.0% | 75.0% | -0.0% |
| vix_vix3m_ratio | 30 | market | 16 | 24 | 79.2% | 79.2% | 0.0% |
| vix_vix3m_ratio | 30 | market | 17 | 24 | 83.3% | 83.3% | 0.0% |
| vix_vix3m_ratio | 30 | market | 18 | 21 | 81.0% | 81.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 19 | 20 | 75.0% | 75.0% | 0.0% |
| vix_vix3m_ratio | 30 | market | 20 | 20 | 85.0% | 85.0% | -0.0% |
| vix_vix3m_ratio | 30 | market | 21 | 19 | 73.7% | 73.7% | 0.0% |
| vix_vix3m_ratio | 30 | market | 22 | 20 | 70.0% | 72.0% | -2.0% |
| vix_vix3m_ratio | 30 | market | 23 | 22 | 59.1% | 62.1% | -3.0% |
| vix_vix3m_ratio | 30 | market | 24 | 23 | 69.6% | 70.8% | -1.2% |
| vix_vix3m_ratio | 30 | market | 25 | 22 | 68.2% | 70.0% | -1.8% |
| vix_vix3m_ratio | 30 | market | 26 | 23 | 69.6% | 69.6% | 0.0% |
| vix_vix3m_ratio | 30 | market | 27 | 23 | 60.9% | 62.6% | -1.7% |
| vix_vix3m_ratio | 30 | market | 28 | 23 | 78.3% | 78.3% | 0.0% |
| vix_vix3m_ratio | 30 | market | 29 | 22 | 68.2% | 71.6% | -3.4% |
| vix_vix3m_ratio | 30 | volatility | 0 | 23 | 47.8% | 44.1% | 3.7% |
| vix_vix3m_ratio | 30 | volatility | 1 | 23 | 52.2% | 47.3% | 4.8% |
| vix_vix3m_ratio | 30 | volatility | 2 | 23 | 47.8% | 48.9% | -1.1% |
| vix_vix3m_ratio | 30 | volatility | 3 | 23 | 43.5% | 35.6% | 7.9% |
| vix_vix3m_ratio | 30 | volatility | 4 | 23 | 39.1% | 31.4% | 7.7% |
| vix_vix3m_ratio | 30 | volatility | 5 | 23 | 47.8% | 38.6% | 9.2% |
| vix_vix3m_ratio | 30 | volatility | 6 | 23 | 47.8% | 35.9% | 11.9% |
| vix_vix3m_ratio | 30 | volatility | 7 | 23 | 47.8% | 50.7% | -2.9% |
| vix_vix3m_ratio | 30 | volatility | 8 | 23 | 52.2% | 50.3% | 1.9% |
| vix_vix3m_ratio | 30 | volatility | 9 | 23 | 47.8% | 47.3% | 0.5% |
| vix_vix3m_ratio | 30 | volatility | 10 | 23 | 56.5% | 56.5% | -0.0% |
| vix_vix3m_ratio | 30 | volatility | 11 | 23 | 47.8% | 47.0% | 0.8% |
| vix_vix3m_ratio | 30 | volatility | 12 | 23 | 43.5% | 44.3% | -0.9% |
| vix_vix3m_ratio | 30 | volatility | 13 | 23 | 52.2% | 52.2% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 14 | 23 | 52.2% | 52.2% | -0.0% |
| vix_vix3m_ratio | 30 | volatility | 15 | 23 | 43.5% | 43.5% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 16 | 23 | 34.8% | 34.8% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 17 | 23 | 39.1% | 39.1% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 18 | 22 | 31.8% | 31.8% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 19 | 22 | 31.8% | 27.7% | 4.1% |
| vix_vix3m_ratio | 30 | volatility | 20 | 23 | 30.4% | 26.4% | 4.1% |
| vix_vix3m_ratio | 30 | volatility | 21 | 23 | 34.8% | 28.4% | 6.4% |
| vix_vix3m_ratio | 30 | volatility | 22 | 23 | 39.1% | 32.4% | 6.7% |
| vix_vix3m_ratio | 30 | volatility | 23 | 23 | 39.1% | 40.4% | -1.3% |
| vix_vix3m_ratio | 30 | volatility | 24 | 23 | 43.5% | 44.1% | -0.6% |
| vix_vix3m_ratio | 30 | volatility | 25 | 23 | 39.1% | 41.3% | -2.2% |
| vix_vix3m_ratio | 30 | volatility | 26 | 23 | 43.5% | 43.5% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 27 | 23 | 34.8% | 34.8% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 28 | 23 | 39.1% | 39.1% | 0.0% |
| vix_vix3m_ratio | 30 | volatility | 29 | 23 | 43.5% | 47.9% | -4.5% |
| vrp_spread | 3 | volatility | 0 | 238 | 41.2% | 36.6% | 4.6% |
| vrp_spread | 3 | volatility | 1 | 238 | 47.1% | 39.5% | 7.6% |
| vrp_spread | 3 | volatility | 2 | 239 | 44.4% | 40.0% | 4.4% |
| vrp_spread | 7 | volatility | 0 | 102 | 48.0% | 41.9% | 6.1% |
| vrp_spread | 7 | volatility | 1 | 102 | 48.0% | 46.2% | 1.8% |
| vrp_spread | 7 | volatility | 2 | 102 | 52.9% | 48.0% | 5.0% |
| vrp_spread | 7 | volatility | 3 | 101 | 46.5% | 42.8% | 3.8% |
| vrp_spread | 7 | volatility | 4 | 101 | 55.4% | 47.3% | 8.1% |
| vrp_spread | 7 | volatility | 5 | 101 | 57.4% | 48.8% | 8.6% |
| vrp_spread | 7 | volatility | 6 | 102 | 55.9% | 45.5% | 10.3% |
| vrp_spread | 14 | volatility | 0 | 50 | 50.0% | 50.9% | -0.9% |
| vrp_spread | 14 | volatility | 1 | 50 | 50.0% | 52.2% | -2.2% |
| vrp_spread | 14 | volatility | 2 | 50 | 60.0% | 53.7% | 6.3% |
| vrp_spread | 14 | volatility | 3 | 50 | 52.0% | 49.8% | 2.2% |
| vrp_spread | 14 | volatility | 4 | 50 | 62.0% | 55.2% | 6.8% |
| vrp_spread | 14 | volatility | 5 | 50 | 60.0% | 51.7% | 8.3% |
| vrp_spread | 14 | volatility | 6 | 51 | 58.8% | 49.2% | 9.7% |
| vrp_spread | 14 | volatility | 7 | 51 | 56.9% | 47.8% | 9.1% |
| vrp_spread | 14 | volatility | 8 | 51 | 56.9% | 51.3% | 5.6% |
| vrp_spread | 14 | volatility | 9 | 51 | 54.9% | 52.4% | 2.5% |
| vrp_spread | 14 | volatility | 10 | 50 | 46.0% | 46.8% | -0.8% |
| vrp_spread | 14 | volatility | 11 | 50 | 54.0% | 49.6% | 4.4% |
| vrp_spread | 14 | volatility | 12 | 50 | 54.0% | 48.8% | 5.2% |
| vrp_spread | 14 | volatility | 13 | 50 | 46.0% | 46.2% | -0.2% |
| vrp_spread | 30 | volatility | 0 | 23 | 56.5% | 54.2% | 2.4% |
| vrp_spread | 30 | volatility | 1 | 23 | 52.2% | 48.0% | 4.1% |
| vrp_spread | 30 | volatility | 2 | 23 | 60.9% | 53.6% | 7.2% |
| vrp_spread | 30 | volatility | 3 | 23 | 65.2% | 48.1% | 17.1% |
| vrp_spread | 30 | volatility | 4 | 23 | 65.2% | 51.1% | 14.1% |
| vrp_spread | 30 | volatility | 5 | 23 | 47.8% | 50.2% | -2.4% |
| vrp_spread | 30 | volatility | 6 | 23 | 52.2% | 49.5% | 2.7% |
| vrp_spread | 30 | volatility | 7 | 23 | 56.5% | 57.2% | -0.7% |
| vrp_spread | 30 | volatility | 8 | 23 | 56.5% | 46.3% | 10.2% |
| vrp_spread | 30 | volatility | 9 | 23 | 60.9% | 48.1% | 12.7% |
| vrp_spread | 30 | volatility | 10 | 23 | 56.5% | 54.3% | 2.2% |
| vrp_spread | 30 | volatility | 11 | 23 | 56.5% | 57.9% | -1.4% |
| vrp_spread | 30 | volatility | 12 | 23 | 60.9% | 55.9% | 5.0% |
| vrp_spread | 30 | volatility | 13 | 23 | 60.9% | 49.6% | 11.3% |
| vrp_spread | 30 | volatility | 14 | 23 | 52.2% | 51.1% | 1.1% |
| vrp_spread | 30 | volatility | 15 | 23 | 47.8% | 54.2% | -6.4% |
| vrp_spread | 30 | volatility | 16 | 23 | 65.2% | 65.2% | 0.0% |
| vrp_spread | 30 | volatility | 17 | 23 | 56.5% | 62.1% | -5.6% |
| vrp_spread | 30 | volatility | 18 | 22 | 63.6% | 62.1% | 1.5% |
| vrp_spread | 30 | volatility | 19 | 22 | 63.6% | 56.5% | 7.1% |
| vrp_spread | 30 | volatility | 20 | 23 | 78.3% | 65.4% | 12.8% |
| vrp_spread | 30 | volatility | 21 | 23 | 60.9% | 59.1% | 1.7% |
| vrp_spread | 30 | volatility | 22 | 23 | 60.9% | 59.3% | 1.6% |
| vrp_spread | 30 | volatility | 23 | 23 | 60.9% | 56.2% | 4.7% |
| vrp_spread | 30 | volatility | 24 | 23 | 56.5% | 52.6% | 3.9% |
| vrp_spread | 30 | volatility | 25 | 23 | 60.9% | 56.9% | 4.0% |
| vrp_spread | 30 | volatility | 26 | 23 | 56.5% | 51.3% | 5.2% |
| vrp_spread | 30 | volatility | 27 | 23 | 56.5% | 54.3% | 2.2% |
| vrp_spread | 30 | volatility | 28 | 23 | 65.2% | 55.7% | 9.6% |
| vrp_spread | 30 | volatility | 29 | 23 | 52.2% | 49.8% | 2.4% |
| vta35 | 3 | market | 0 | 199 | 49.2% | 51.5% | -2.3% |
| vta35 | 3 | market | 1 | 206 | 47.1% | 50.3% | -3.2% |
| vta35 | 3 | market | 2 | 198 | 50.5% | 51.6% | -1.1% |
| vta35 | 3 | volatility | 0 | 225 | 46.7% | 44.1% | 2.5% |
| vta35 | 3 | volatility | 1 | 225 | 53.8% | 44.7% | 9.1% |
| vta35 | 3 | volatility | 2 | 226 | 46.0% | 42.1% | 3.9% |
| vta35 | 7 | market | 0 | 87 | 37.9% | 51.1% | -13.1% |
| vta35 | 7 | market | 1 | 83 | 43.4% | 53.6% | -10.3% |
| vta35 | 7 | market | 2 | 87 | 41.4% | 49.2% | -7.8% |
| vta35 | 7 | market | 3 | 87 | 41.4% | 50.6% | -9.2% |
| vta35 | 7 | market | 4 | 83 | 38.6% | 48.9% | -10.4% |
| vta35 | 7 | market | 5 | 87 | 44.8% | 52.5% | -7.6% |
| vta35 | 7 | market | 6 | 87 | 44.8% | 53.6% | -8.8% |
| vta35 | 7 | volatility | 0 | 96 | 51.0% | 39.3% | 11.7% |
| vta35 | 7 | volatility | 1 | 96 | 41.7% | 37.6% | 4.1% |
| vta35 | 7 | volatility | 2 | 96 | 42.7% | 38.3% | 4.4% |
| vta35 | 7 | volatility | 3 | 96 | 47.9% | 37.9% | 10.0% |
| vta35 | 7 | volatility | 4 | 96 | 51.0% | 38.5% | 12.5% |
| vta35 | 7 | volatility | 5 | 96 | 51.0% | 42.6% | 8.5% |
| vta35 | 7 | volatility | 6 | 96 | 51.0% | 43.4% | 7.6% |
| vta35 | 14 | market | 0 | 43 | 39.5% | 49.4% | -9.9% |
| vta35 | 14 | market | 1 | 42 | 57.1% | 55.4% | 1.7% |
| vta35 | 14 | market | 2 | 43 | 58.1% | 57.5% | 0.6% |
| vta35 | 14 | market | 3 | 45 | 51.1% | 55.1% | -4.0% |
| vta35 | 14 | market | 4 | 38 | 42.1% | 49.9% | -7.8% |
| vta35 | 14 | market | 5 | 44 | 50.0% | 55.6% | -5.6% |
| vta35 | 14 | market | 6 | 45 | 55.6% | 55.6% | -0.0% |
| vta35 | 14 | market | 7 | 44 | 47.7% | 53.1% | -5.4% |
| vta35 | 14 | market | 8 | 40 | 52.5% | 50.1% | 2.4% |
| vta35 | 14 | market | 9 | 43 | 46.5% | 49.2% | -2.7% |
| vta35 | 14 | market | 10 | 41 | 48.8% | 50.4% | -1.6% |
| vta35 | 14 | market | 11 | 44 | 47.7% | 48.6% | -0.9% |
| vta35 | 14 | market | 12 | 42 | 47.6% | 51.1% | -3.4% |
| vta35 | 14 | market | 13 | 41 | 46.3% | 57.2% | -10.9% |
| vta35 | 14 | volatility | 0 | 47 | 55.3% | 42.7% | 12.6% |
| vta35 | 14 | volatility | 1 | 47 | 38.3% | 39.6% | -1.3% |
| vta35 | 14 | volatility | 2 | 47 | 51.1% | 37.1% | 14.0% |
| vta35 | 14 | volatility | 3 | 48 | 43.8% | 37.9% | 5.8% |
| vta35 | 14 | volatility | 4 | 48 | 41.7% | 37.9% | 3.7% |
| vta35 | 14 | volatility | 5 | 48 | 47.9% | 39.1% | 8.8% |
| vta35 | 14 | volatility | 6 | 48 | 45.8% | 38.3% | 7.5% |
| vta35 | 14 | volatility | 7 | 48 | 39.6% | 33.7% | 5.9% |
| vta35 | 14 | volatility | 8 | 48 | 35.4% | 27.8% | 7.7% |
| vta35 | 14 | volatility | 9 | 48 | 47.9% | 36.6% | 11.3% |
| vta35 | 14 | volatility | 10 | 47 | 44.7% | 35.7% | 9.0% |
| vta35 | 14 | volatility | 11 | 47 | 51.1% | 40.5% | 10.6% |
| vta35 | 14 | volatility | 12 | 47 | 53.2% | 38.1% | 15.1% |
| vta35 | 14 | volatility | 13 | 47 | 44.7% | 40.8% | 3.9% |
| vta35 | 30 | market | 0 | 19 | 42.1% | 54.9% | -12.8% |
| vta35 | 30 | market | 1 | 22 | 50.0% | 56.7% | -6.7% |
| vta35 | 30 | market | 2 | 21 | 47.6% | 56.2% | -8.6% |
| vta35 | 30 | market | 3 | 20 | 45.0% | 56.1% | -11.1% |
| vta35 | 30 | market | 4 | 20 | 35.0% | 46.8% | -11.8% |
| vta35 | 30 | market | 5 | 18 | 33.3% | 40.7% | -7.4% |
| vta35 | 30 | market | 6 | 21 | 47.6% | 50.1% | -2.4% |
| vta35 | 30 | market | 7 | 21 | 52.4% | 51.6% | 0.8% |
| vta35 | 30 | market | 8 | 18 | 38.9% | 54.0% | -15.2% |
| vta35 | 30 | market | 9 | 19 | 52.6% | 58.4% | -5.7% |
| vta35 | 30 | market | 10 | 19 | 47.4% | 54.3% | -6.9% |
| vta35 | 30 | market | 11 | 21 | 61.9% | 59.0% | 2.9% |
| vta35 | 30 | market | 12 | 19 | 63.2% | 54.2% | 9.0% |
| vta35 | 30 | market | 13 | 21 | 61.9% | 56.8% | 5.1% |
| vta35 | 30 | market | 14 | 18 | 61.1% | 53.3% | 7.8% |
| vta35 | 30 | market | 15 | 20 | 65.0% | 50.0% | 15.0% |
| vta35 | 30 | market | 16 | 18 | 72.2% | 57.4% | 14.8% |
| vta35 | 30 | market | 17 | 20 | 50.0% | 55.0% | -5.0% |
| vta35 | 30 | market | 18 | 19 | 63.2% | 56.5% | 6.7% |
| vta35 | 30 | market | 19 | 18 | 72.2% | 57.4% | 14.8% |
| vta35 | 30 | market | 20 | 18 | 61.1% | 53.1% | 8.0% |
| vta35 | 30 | market | 21 | 17 | 64.7% | 65.9% | -1.2% |
| vta35 | 30 | market | 22 | 18 | 55.6% | 54.4% | 1.1% |
| vta35 | 30 | market | 23 | 19 | 52.6% | 45.1% | 7.5% |
| vta35 | 30 | market | 24 | 18 | 55.6% | 53.0% | 2.6% |
| vta35 | 30 | market | 25 | 21 | 42.9% | 45.2% | -2.3% |
| vta35 | 30 | market | 26 | 19 | 52.6% | 51.6% | 1.1% |
| vta35 | 30 | market | 27 | 19 | 47.4% | 51.8% | -4.4% |
| vta35 | 30 | market | 28 | 20 | 50.0% | 54.0% | -4.0% |
| vta35 | 30 | market | 29 | 21 | 38.1% | 56.0% | -17.9% |
| vta35 | 30 | volatility | 0 | 22 | 50.0% | 34.6% | 15.4% |
| vta35 | 30 | volatility | 1 | 22 | 54.5% | 38.0% | 16.6% |
| vta35 | 30 | volatility | 2 | 22 | 59.1% | 40.7% | 18.4% |
| vta35 | 30 | volatility | 3 | 22 | 45.5% | 37.0% | 8.4% |
| vta35 | 30 | volatility | 4 | 22 | 50.0% | 36.2% | 13.8% |
| vta35 | 30 | volatility | 5 | 22 | 36.4% | 30.8% | 5.6% |
| vta35 | 30 | volatility | 6 | 22 | 40.9% | 39.0% | 1.9% |
| vta35 | 30 | volatility | 7 | 22 | 50.0% | 43.9% | 6.1% |
| vta35 | 30 | volatility | 8 | 22 | 50.0% | 45.2% | 4.8% |
| vta35 | 30 | volatility | 9 | 22 | 54.5% | 42.2% | 12.3% |
| vta35 | 30 | volatility | 10 | 22 | 40.9% | 34.8% | 6.1% |
| vta35 | 30 | volatility | 11 | 22 | 50.0% | 43.2% | 6.8% |
| vta35 | 30 | volatility | 12 | 22 | 54.5% | 40.7% | 13.9% |
| vta35 | 30 | volatility | 13 | 22 | 59.1% | 46.4% | 12.7% |
| vta35 | 30 | volatility | 14 | 22 | 59.1% | 41.7% | 17.4% |
| vta35 | 30 | volatility | 15 | 22 | 54.5% | 45.7% | 8.9% |
| vta35 | 30 | volatility | 16 | 22 | 40.9% | 36.1% | 4.8% |
| vta35 | 30 | volatility | 17 | 22 | 31.8% | 34.6% | -2.8% |
| vta35 | 30 | volatility | 18 | 21 | 38.1% | 25.4% | 12.7% |
| vta35 | 30 | volatility | 19 | 21 | 19.0% | 24.9% | -5.9% |
| vta35 | 30 | volatility | 20 | 21 | 28.6% | 30.7% | -2.1% |
| vta35 | 30 | volatility | 21 | 21 | 23.8% | 30.4% | -6.6% |
| vta35 | 30 | volatility | 22 | 21 | 28.6% | 27.5% | 1.1% |
| vta35 | 30 | volatility | 23 | 21 | 28.6% | 34.6% | -6.0% |
| vta35 | 30 | volatility | 24 | 21 | 33.3% | 34.8% | -1.5% |
| vta35 | 30 | volatility | 25 | 21 | 42.9% | 40.6% | 2.2% |
| vta35 | 30 | volatility | 26 | 21 | 42.9% | 33.3% | 9.5% |
| vta35 | 30 | volatility | 27 | 21 | 42.9% | 29.4% | 13.5% |
| vta35 | 30 | volatility | 28 | 21 | 42.9% | 32.4% | 10.5% |
| vta35 | 30 | volatility | 29 | 22 | 36.4% | 34.1% | 2.3% |
| vta35_change_5d | 3 | market | 0 | 227 | 50.2% | 49.7% | 0.5% |
| vta35_change_5d | 3 | market | 1 | 227 | 49.8% | 50.8% | -1.1% |
| vta35_change_5d | 3 | market | 2 | 226 | 50.9% | 49.9% | 1.0% |
| vta35_change_5d | 3 | volatility | 0 | 238 | 46.6% | 46.9% | -0.2% |
| vta35_change_5d | 3 | volatility | 1 | 238 | 51.3% | 48.5% | 2.7% |
| vta35_change_5d | 3 | volatility | 2 | 239 | 46.4% | 46.4% | 0.1% |
| vta35_change_5d | 7 | market | 0 | 98 | 46.9% | 48.8% | -1.8% |
| vta35_change_5d | 7 | market | 1 | 95 | 45.3% | 50.4% | -5.2% |
| vta35_change_5d | 7 | market | 2 | 97 | 41.2% | 49.8% | -8.6% |
| vta35_change_5d | 7 | market | 3 | 94 | 44.7% | 49.8% | -5.2% |
| vta35_change_5d | 7 | market | 4 | 97 | 45.4% | 50.0% | -4.7% |
| vta35_change_5d | 7 | market | 5 | 98 | 49.0% | 51.8% | -2.8% |
| vta35_change_5d | 7 | market | 6 | 98 | 55.1% | 50.1% | 5.0% |
| vta35_change_5d | 7 | volatility | 0 | 102 | 52.9% | 44.2% | 8.8% |
| vta35_change_5d | 7 | volatility | 1 | 102 | 45.1% | 44.2% | 0.9% |
| vta35_change_5d | 7 | volatility | 2 | 102 | 47.1% | 44.8% | 2.3% |
| vta35_change_5d | 7 | volatility | 3 | 101 | 47.5% | 43.4% | 4.1% |
| vta35_change_5d | 7 | volatility | 4 | 101 | 51.5% | 46.8% | 4.7% |
| vta35_change_5d | 7 | volatility | 5 | 101 | 57.4% | 51.8% | 5.7% |
| vta35_change_5d | 7 | volatility | 6 | 102 | 55.9% | 47.7% | 8.2% |
| vta35_change_5d | 14 | market | 0 | 47 | 48.9% | 50.9% | -2.0% |
| vta35_change_5d | 14 | market | 1 | 47 | 55.3% | 49.8% | 5.5% |
| vta35_change_5d | 14 | market | 2 | 49 | 65.3% | 59.9% | 5.5% |
| vta35_change_5d | 14 | market | 3 | 47 | 61.7% | 55.2% | 6.5% |
| vta35_change_5d | 14 | market | 4 | 45 | 44.4% | 49.1% | -4.7% |
| vta35_change_5d | 14 | market | 5 | 47 | 48.9% | 53.4% | -4.5% |
| vta35_change_5d | 14 | market | 6 | 49 | 51.0% | 50.6% | 0.4% |
| vta35_change_5d | 14 | market | 7 | 50 | 46.0% | 47.3% | -1.3% |
| vta35_change_5d | 14 | market | 8 | 47 | 42.6% | 49.0% | -6.5% |
| vta35_change_5d | 14 | market | 9 | 47 | 38.3% | 47.4% | -9.1% |
| vta35_change_5d | 14 | market | 10 | 46 | 43.5% | 47.7% | -4.3% |
| vta35_change_5d | 14 | market | 11 | 51 | 52.9% | 48.9% | 4.1% |
| vta35_change_5d | 14 | market | 12 | 50 | 60.0% | 53.7% | 6.3% |
| vta35_change_5d | 14 | market | 13 | 48 | 58.3% | 49.7% | 8.6% |
| vta35_change_5d | 14 | volatility | 0 | 50 | 50.0% | 47.6% | 2.4% |
| vta35_change_5d | 14 | volatility | 1 | 50 | 38.0% | 46.4% | -8.4% |
| vta35_change_5d | 14 | volatility | 2 | 50 | 48.0% | 44.7% | 3.3% |
| vta35_change_5d | 14 | volatility | 3 | 50 | 48.0% | 47.7% | 0.3% |
| vta35_change_5d | 14 | volatility | 4 | 50 | 66.0% | 49.2% | 16.8% |
| vta35_change_5d | 14 | volatility | 5 | 50 | 52.0% | 47.9% | 4.1% |
| vta35_change_5d | 14 | volatility | 6 | 51 | 56.9% | 45.6% | 11.3% |
| vta35_change_5d | 14 | volatility | 7 | 51 | 52.9% | 43.7% | 9.2% |
| vta35_change_5d | 14 | volatility | 8 | 51 | 49.0% | 42.3% | 6.7% |
| vta35_change_5d | 14 | volatility | 9 | 51 | 41.2% | 42.8% | -1.6% |
| vta35_change_5d | 14 | volatility | 10 | 50 | 40.0% | 42.4% | -2.4% |
| vta35_change_5d | 14 | volatility | 11 | 50 | 56.0% | 48.7% | 7.3% |
| vta35_change_5d | 14 | volatility | 12 | 50 | 58.0% | 48.7% | 9.3% |
| vta35_change_5d | 14 | volatility | 13 | 50 | 50.0% | 46.8% | 3.2% |
| vta35_change_5d | 30 | market | 0 | 22 | 54.5% | 58.3% | -3.8% |
| vta35_change_5d | 30 | market | 1 | 21 | 57.1% | 58.6% | -1.4% |
| vta35_change_5d | 30 | market | 2 | 21 | 57.1% | 53.0% | 4.1% |
| vta35_change_5d | 30 | market | 3 | 23 | 47.8% | 51.6% | -3.7% |
| vta35_change_5d | 30 | market | 4 | 21 | 38.1% | 48.1% | -10.0% |
| vta35_change_5d | 30 | market | 5 | 23 | 52.2% | 53.6% | -1.4% |
| vta35_change_5d | 30 | market | 6 | 23 | 43.5% | 51.4% | -7.9% |
| vta35_change_5d | 30 | market | 7 | 24 | 50.0% | 46.7% | 3.3% |
| vta35_change_5d | 30 | market | 8 | 23 | 47.8% | 51.4% | -3.6% |
| vta35_change_5d | 30 | market | 9 | 22 | 54.5% | 51.5% | 3.0% |
| vta35_change_5d | 30 | market | 10 | 22 | 63.6% | 60.3% | 3.3% |
| vta35_change_5d | 30 | market | 11 | 21 | 52.4% | 52.1% | 0.3% |
| vta35_change_5d | 30 | market | 12 | 20 | 55.0% | 49.0% | 6.0% |
| vta35_change_5d | 30 | market | 13 | 24 | 54.2% | 51.1% | 3.1% |
| vta35_change_5d | 30 | market | 14 | 21 | 57.1% | 47.6% | 9.5% |
| vta35_change_5d | 30 | market | 15 | 22 | 50.0% | 44.6% | 5.4% |
| vta35_change_5d | 30 | market | 16 | 22 | 59.1% | 52.6% | 6.5% |
| vta35_change_5d | 30 | market | 17 | 23 | 52.2% | 47.8% | 4.3% |
| vta35_change_5d | 30 | market | 18 | 22 | 54.5% | 54.5% | 0.0% |
| vta35_change_5d | 30 | market | 19 | 22 | 59.1% | 47.0% | 12.1% |
| vta35_change_5d | 30 | market | 20 | 21 | 61.9% | 56.1% | 5.8% |
| vta35_change_5d | 30 | market | 21 | 20 | 50.0% | 54.1% | -4.1% |
| vta35_change_5d | 30 | market | 22 | 20 | 45.0% | 46.7% | -1.7% |
| vta35_change_5d | 30 | market | 23 | 22 | 40.9% | 45.6% | -4.7% |
| vta35_change_5d | 30 | market | 24 | 23 | 56.5% | 46.4% | 10.1% |
| vta35_change_5d | 30 | market | 25 | 21 | 66.7% | 51.4% | 15.2% |
| vta35_change_5d | 30 | market | 26 | 22 | 63.6% | 53.6% | 10.0% |
| vta35_change_5d | 30 | market | 27 | 21 | 57.1% | 51.7% | 5.4% |
| vta35_change_5d | 30 | market | 28 | 23 | 56.5% | 61.7% | -5.2% |
| vta35_change_5d | 30 | market | 29 | 22 | 45.5% | 48.6% | -3.2% |
| vta35_change_5d | 30 | volatility | 0 | 23 | 52.2% | 52.0% | 0.2% |
| vta35_change_5d | 30 | volatility | 1 | 23 | 56.5% | 45.1% | 11.4% |
| vta35_change_5d | 30 | volatility | 2 | 23 | 65.2% | 46.8% | 18.4% |
| vta35_change_5d | 30 | volatility | 3 | 23 | 52.2% | 43.9% | 8.3% |
| vta35_change_5d | 30 | volatility | 4 | 23 | 60.9% | 46.2% | 14.7% |
| vta35_change_5d | 30 | volatility | 5 | 23 | 43.5% | 43.5% | 0.0% |
| vta35_change_5d | 30 | volatility | 6 | 23 | 43.5% | 46.7% | -3.2% |
| vta35_change_5d | 30 | volatility | 7 | 23 | 34.8% | 58.0% | -23.2% |
| vta35_change_5d | 30 | volatility | 8 | 23 | 52.2% | 46.6% | 5.6% |
| vta35_change_5d | 30 | volatility | 9 | 23 | 52.2% | 43.7% | 8.5% |
| vta35_change_5d | 30 | volatility | 10 | 23 | 60.9% | 44.2% | 16.7% |
| vta35_change_5d | 30 | volatility | 11 | 23 | 60.9% | 44.5% | 16.4% |
| vta35_change_5d | 30 | volatility | 12 | 23 | 52.2% | 46.3% | 5.9% |
| vta35_change_5d | 30 | volatility | 13 | 23 | 56.5% | 54.8% | 1.7% |
| vta35_change_5d | 30 | volatility | 14 | 23 | 52.2% | 46.0% | 6.2% |
| vta35_change_5d | 30 | volatility | 15 | 23 | 47.8% | 45.0% | 2.8% |
| vta35_change_5d | 30 | volatility | 16 | 23 | 52.2% | 47.2% | 4.9% |
| vta35_change_5d | 30 | volatility | 17 | 23 | 34.8% | 41.0% | -6.2% |
| vta35_change_5d | 30 | volatility | 18 | 22 | 36.4% | 39.4% | -3.0% |
| vta35_change_5d | 30 | volatility | 19 | 22 | 31.8% | 41.8% | -10.0% |
| vta35_change_5d | 30 | volatility | 20 | 23 | 39.1% | 40.8% | -1.7% |
| vta35_change_5d | 30 | volatility | 21 | 23 | 21.7% | 39.7% | -18.0% |
| vta35_change_5d | 30 | volatility | 22 | 23 | 21.7% | 37.5% | -15.8% |
| vta35_change_5d | 30 | volatility | 23 | 23 | 34.8% | 46.6% | -11.8% |
| vta35_change_5d | 30 | volatility | 24 | 23 | 56.5% | 58.0% | -1.5% |
| vta35_change_5d | 30 | volatility | 25 | 23 | 56.5% | 45.2% | 11.3% |
| vta35_change_5d | 30 | volatility | 26 | 23 | 60.9% | 47.0% | 13.9% |
| vta35_change_5d | 30 | volatility | 27 | 23 | 56.5% | 44.9% | 11.6% |
| vta35_change_5d | 30 | volatility | 28 | 23 | 60.9% | 53.0% | 7.8% |
| vta35_change_5d | 30 | volatility | 29 | 23 | 60.9% | 50.5% | 10.4% |
| vta35_zscore_60 | 3 | market | 0 | 199 | 49.2% | 51.5% | -2.3% |
| vta35_zscore_60 | 3 | market | 1 | 206 | 47.1% | 50.3% | -3.2% |
| vta35_zscore_60 | 3 | market | 2 | 198 | 50.5% | 51.6% | -1.1% |
| vta35_zscore_60 | 3 | volatility | 0 | 225 | 46.7% | 44.1% | 2.5% |
| vta35_zscore_60 | 3 | volatility | 1 | 225 | 53.8% | 44.7% | 9.1% |
| vta35_zscore_60 | 3 | volatility | 2 | 226 | 46.0% | 42.1% | 3.9% |
| vta35_zscore_60 | 7 | market | 0 | 87 | 37.9% | 51.1% | -13.1% |
| vta35_zscore_60 | 7 | market | 1 | 83 | 43.4% | 53.6% | -10.3% |
| vta35_zscore_60 | 7 | market | 2 | 87 | 41.4% | 49.2% | -7.8% |
| vta35_zscore_60 | 7 | market | 3 | 87 | 41.4% | 50.6% | -9.2% |
| vta35_zscore_60 | 7 | market | 4 | 83 | 38.6% | 48.9% | -10.4% |
| vta35_zscore_60 | 7 | market | 5 | 87 | 44.8% | 52.5% | -7.6% |
| vta35_zscore_60 | 7 | market | 6 | 87 | 44.8% | 53.6% | -8.8% |
| vta35_zscore_60 | 7 | volatility | 0 | 96 | 51.0% | 39.3% | 11.7% |
| vta35_zscore_60 | 7 | volatility | 1 | 96 | 41.7% | 37.6% | 4.1% |
| vta35_zscore_60 | 7 | volatility | 2 | 96 | 42.7% | 38.3% | 4.4% |
| vta35_zscore_60 | 7 | volatility | 3 | 96 | 47.9% | 37.9% | 10.0% |
| vta35_zscore_60 | 7 | volatility | 4 | 96 | 51.0% | 38.5% | 12.5% |
| vta35_zscore_60 | 7 | volatility | 5 | 96 | 51.0% | 42.6% | 8.5% |
| vta35_zscore_60 | 7 | volatility | 6 | 96 | 51.0% | 43.4% | 7.6% |
| vta35_zscore_60 | 14 | market | 0 | 43 | 39.5% | 49.4% | -9.9% |
| vta35_zscore_60 | 14 | market | 1 | 42 | 57.1% | 55.4% | 1.7% |
| vta35_zscore_60 | 14 | market | 2 | 43 | 58.1% | 57.5% | 0.6% |
| vta35_zscore_60 | 14 | market | 3 | 45 | 51.1% | 55.1% | -4.0% |
| vta35_zscore_60 | 14 | market | 4 | 38 | 42.1% | 49.9% | -7.8% |
| vta35_zscore_60 | 14 | market | 5 | 44 | 50.0% | 55.6% | -5.6% |
| vta35_zscore_60 | 14 | market | 6 | 45 | 55.6% | 55.6% | -0.0% |
| vta35_zscore_60 | 14 | market | 7 | 44 | 47.7% | 53.1% | -5.4% |
| vta35_zscore_60 | 14 | market | 8 | 40 | 52.5% | 50.1% | 2.4% |
| vta35_zscore_60 | 14 | market | 9 | 43 | 46.5% | 49.2% | -2.7% |
| vta35_zscore_60 | 14 | market | 10 | 41 | 48.8% | 50.4% | -1.6% |
| vta35_zscore_60 | 14 | market | 11 | 44 | 47.7% | 48.6% | -0.9% |
| vta35_zscore_60 | 14 | market | 12 | 42 | 47.6% | 51.1% | -3.4% |
| vta35_zscore_60 | 14 | market | 13 | 41 | 46.3% | 57.2% | -10.9% |
| vta35_zscore_60 | 14 | volatility | 0 | 47 | 55.3% | 42.7% | 12.6% |
| vta35_zscore_60 | 14 | volatility | 1 | 47 | 38.3% | 39.6% | -1.3% |
| vta35_zscore_60 | 14 | volatility | 2 | 47 | 51.1% | 37.1% | 14.0% |
| vta35_zscore_60 | 14 | volatility | 3 | 48 | 43.8% | 37.9% | 5.8% |
| vta35_zscore_60 | 14 | volatility | 4 | 48 | 41.7% | 37.9% | 3.7% |
| vta35_zscore_60 | 14 | volatility | 5 | 48 | 47.9% | 39.1% | 8.8% |
| vta35_zscore_60 | 14 | volatility | 6 | 48 | 45.8% | 38.3% | 7.5% |
| vta35_zscore_60 | 14 | volatility | 7 | 48 | 39.6% | 33.7% | 5.9% |
| vta35_zscore_60 | 14 | volatility | 8 | 48 | 35.4% | 27.8% | 7.7% |
| vta35_zscore_60 | 14 | volatility | 9 | 48 | 47.9% | 36.6% | 11.3% |
| vta35_zscore_60 | 14 | volatility | 10 | 47 | 44.7% | 35.7% | 9.0% |
| vta35_zscore_60 | 14 | volatility | 11 | 47 | 51.1% | 40.5% | 10.6% |
| vta35_zscore_60 | 14 | volatility | 12 | 47 | 53.2% | 38.1% | 15.1% |
| vta35_zscore_60 | 14 | volatility | 13 | 47 | 44.7% | 40.8% | 3.9% |
| vta35_zscore_60 | 30 | market | 0 | 19 | 42.1% | 54.9% | -12.8% |
| vta35_zscore_60 | 30 | market | 1 | 22 | 50.0% | 56.7% | -6.7% |
| vta35_zscore_60 | 30 | market | 2 | 21 | 47.6% | 56.2% | -8.6% |
| vta35_zscore_60 | 30 | market | 3 | 20 | 45.0% | 56.1% | -11.1% |
| vta35_zscore_60 | 30 | market | 4 | 20 | 35.0% | 46.8% | -11.8% |
| vta35_zscore_60 | 30 | market | 5 | 18 | 33.3% | 40.7% | -7.4% |
| vta35_zscore_60 | 30 | market | 6 | 21 | 47.6% | 50.1% | -2.4% |
| vta35_zscore_60 | 30 | market | 7 | 21 | 52.4% | 51.6% | 0.8% |
| vta35_zscore_60 | 30 | market | 8 | 18 | 38.9% | 54.0% | -15.2% |
| vta35_zscore_60 | 30 | market | 9 | 19 | 52.6% | 58.4% | -5.7% |
| vta35_zscore_60 | 30 | market | 10 | 19 | 47.4% | 54.3% | -6.9% |
| vta35_zscore_60 | 30 | market | 11 | 21 | 61.9% | 59.0% | 2.9% |
| vta35_zscore_60 | 30 | market | 12 | 19 | 63.2% | 54.2% | 9.0% |
| vta35_zscore_60 | 30 | market | 13 | 21 | 61.9% | 56.8% | 5.1% |
| vta35_zscore_60 | 30 | market | 14 | 18 | 61.1% | 53.3% | 7.8% |
| vta35_zscore_60 | 30 | market | 15 | 20 | 65.0% | 50.0% | 15.0% |
| vta35_zscore_60 | 30 | market | 16 | 18 | 72.2% | 57.4% | 14.8% |
| vta35_zscore_60 | 30 | market | 17 | 20 | 50.0% | 55.0% | -5.0% |
| vta35_zscore_60 | 30 | market | 18 | 19 | 63.2% | 56.5% | 6.7% |
| vta35_zscore_60 | 30 | market | 19 | 18 | 72.2% | 57.4% | 14.8% |
| vta35_zscore_60 | 30 | market | 20 | 18 | 61.1% | 53.1% | 8.0% |
| vta35_zscore_60 | 30 | market | 21 | 17 | 64.7% | 65.9% | -1.2% |
| vta35_zscore_60 | 30 | market | 22 | 18 | 55.6% | 54.4% | 1.1% |
| vta35_zscore_60 | 30 | market | 23 | 19 | 52.6% | 45.1% | 7.5% |
| vta35_zscore_60 | 30 | market | 24 | 18 | 55.6% | 53.0% | 2.6% |
| vta35_zscore_60 | 30 | market | 25 | 21 | 42.9% | 45.2% | -2.3% |
| vta35_zscore_60 | 30 | market | 26 | 19 | 52.6% | 51.6% | 1.1% |
| vta35_zscore_60 | 30 | market | 27 | 19 | 47.4% | 51.8% | -4.4% |
| vta35_zscore_60 | 30 | market | 28 | 20 | 50.0% | 54.0% | -4.0% |
| vta35_zscore_60 | 30 | market | 29 | 21 | 38.1% | 56.0% | -17.9% |
| vta35_zscore_60 | 30 | volatility | 0 | 22 | 50.0% | 34.6% | 15.4% |
| vta35_zscore_60 | 30 | volatility | 1 | 22 | 54.5% | 38.0% | 16.6% |
| vta35_zscore_60 | 30 | volatility | 2 | 22 | 59.1% | 40.7% | 18.4% |
| vta35_zscore_60 | 30 | volatility | 3 | 22 | 45.5% | 37.0% | 8.4% |
| vta35_zscore_60 | 30 | volatility | 4 | 22 | 50.0% | 36.2% | 13.8% |
| vta35_zscore_60 | 30 | volatility | 5 | 22 | 36.4% | 30.8% | 5.6% |
| vta35_zscore_60 | 30 | volatility | 6 | 22 | 40.9% | 39.0% | 1.9% |
| vta35_zscore_60 | 30 | volatility | 7 | 22 | 50.0% | 43.9% | 6.1% |
| vta35_zscore_60 | 30 | volatility | 8 | 22 | 50.0% | 45.2% | 4.8% |
| vta35_zscore_60 | 30 | volatility | 9 | 22 | 54.5% | 42.2% | 12.3% |
| vta35_zscore_60 | 30 | volatility | 10 | 22 | 40.9% | 34.8% | 6.1% |
| vta35_zscore_60 | 30 | volatility | 11 | 22 | 50.0% | 43.2% | 6.8% |
| vta35_zscore_60 | 30 | volatility | 12 | 22 | 54.5% | 40.7% | 13.9% |
| vta35_zscore_60 | 30 | volatility | 13 | 22 | 59.1% | 46.4% | 12.7% |
| vta35_zscore_60 | 30 | volatility | 14 | 22 | 59.1% | 41.7% | 17.4% |
| vta35_zscore_60 | 30 | volatility | 15 | 22 | 54.5% | 45.7% | 8.9% |
| vta35_zscore_60 | 30 | volatility | 16 | 22 | 40.9% | 36.1% | 4.8% |
| vta35_zscore_60 | 30 | volatility | 17 | 22 | 31.8% | 34.6% | -2.8% |
| vta35_zscore_60 | 30 | volatility | 18 | 21 | 38.1% | 25.4% | 12.7% |
| vta35_zscore_60 | 30 | volatility | 19 | 21 | 19.0% | 24.9% | -5.9% |
| vta35_zscore_60 | 30 | volatility | 20 | 21 | 28.6% | 30.7% | -2.1% |
| vta35_zscore_60 | 30 | volatility | 21 | 21 | 23.8% | 30.4% | -6.6% |
| vta35_zscore_60 | 30 | volatility | 22 | 21 | 28.6% | 27.5% | 1.1% |
| vta35_zscore_60 | 30 | volatility | 23 | 21 | 28.6% | 34.6% | -6.0% |
| vta35_zscore_60 | 30 | volatility | 24 | 21 | 33.3% | 34.8% | -1.5% |
| vta35_zscore_60 | 30 | volatility | 25 | 21 | 42.9% | 40.6% | 2.2% |
| vta35_zscore_60 | 30 | volatility | 26 | 21 | 42.9% | 33.3% | 9.5% |
| vta35_zscore_60 | 30 | volatility | 27 | 21 | 42.9% | 29.4% | 13.5% |
| vta35_zscore_60 | 30 | volatility | 28 | 21 | 42.9% | 32.4% | 10.5% |
| vta35_zscore_60 | 30 | volatility | 29 | 22 | 36.4% | 34.1% | 2.3% |
| vta_vol_of_vol_20 | 3 | volatility | 0 | 238 | 20.2% | 21.0% | -0.8% |
| vta_vol_of_vol_20 | 3 | volatility | 1 | 238 | 25.2% | 23.9% | 1.3% |
| vta_vol_of_vol_20 | 3 | volatility | 2 | 239 | 24.7% | 24.3% | 0.4% |
| vta_vol_of_vol_20 | 7 | volatility | 0 | 102 | 34.3% | 32.4% | 1.9% |
| vta_vol_of_vol_20 | 7 | volatility | 1 | 102 | 35.3% | 33.2% | 2.1% |
| vta_vol_of_vol_20 | 7 | volatility | 2 | 102 | 41.2% | 37.2% | 4.0% |
| vta_vol_of_vol_20 | 7 | volatility | 3 | 101 | 31.7% | 31.3% | 0.4% |
| vta_vol_of_vol_20 | 7 | volatility | 4 | 101 | 36.6% | 35.3% | 1.3% |
| vta_vol_of_vol_20 | 7 | volatility | 5 | 101 | 35.6% | 33.4% | 2.2% |
| vta_vol_of_vol_20 | 7 | volatility | 6 | 102 | 36.3% | 32.6% | 3.6% |
| vta_vol_of_vol_20 | 14 | volatility | 0 | 50 | 44.0% | 43.1% | 0.9% |
| vta_vol_of_vol_20 | 14 | volatility | 1 | 50 | 44.0% | 43.6% | 0.4% |
| vta_vol_of_vol_20 | 14 | volatility | 2 | 50 | 42.0% | 41.4% | 0.6% |
| vta_vol_of_vol_20 | 14 | volatility | 3 | 50 | 38.0% | 38.0% | 0.0% |
| vta_vol_of_vol_20 | 14 | volatility | 4 | 50 | 44.0% | 42.2% | 1.8% |
| vta_vol_of_vol_20 | 14 | volatility | 5 | 50 | 42.0% | 40.0% | 2.0% |
| vta_vol_of_vol_20 | 14 | volatility | 6 | 51 | 45.1% | 41.2% | 3.9% |
| vta_vol_of_vol_20 | 14 | volatility | 7 | 51 | 43.1% | 40.4% | 2.7% |
| vta_vol_of_vol_20 | 14 | volatility | 8 | 51 | 45.1% | 42.0% | 3.1% |
| vta_vol_of_vol_20 | 14 | volatility | 9 | 51 | 47.1% | 44.2% | 2.8% |
| vta_vol_of_vol_20 | 14 | volatility | 10 | 50 | 44.0% | 41.2% | 2.8% |
| vta_vol_of_vol_20 | 14 | volatility | 11 | 50 | 42.0% | 41.3% | 0.7% |
| vta_vol_of_vol_20 | 14 | volatility | 12 | 50 | 44.0% | 38.2% | 5.8% |
| vta_vol_of_vol_20 | 14 | volatility | 13 | 50 | 38.0% | 36.3% | 1.7% |
| vta_vol_of_vol_20 | 30 | volatility | 0 | 23 | 43.5% | 39.1% | 4.3% |
| vta_vol_of_vol_20 | 30 | volatility | 1 | 23 | 39.1% | 36.4% | 2.7% |
| vta_vol_of_vol_20 | 30 | volatility | 2 | 23 | 34.8% | 34.2% | 0.6% |
| vta_vol_of_vol_20 | 30 | volatility | 3 | 23 | 43.5% | 41.6% | 1.9% |
| vta_vol_of_vol_20 | 30 | volatility | 4 | 23 | 43.5% | 47.0% | -3.5% |
| vta_vol_of_vol_20 | 30 | volatility | 5 | 23 | 43.5% | 39.6% | 3.9% |
| vta_vol_of_vol_20 | 30 | volatility | 6 | 23 | 43.5% | 39.0% | 4.5% |
| vta_vol_of_vol_20 | 30 | volatility | 7 | 23 | 43.5% | 40.6% | 2.9% |
| vta_vol_of_vol_20 | 30 | volatility | 8 | 23 | 34.8% | 33.1% | 1.7% |
| vta_vol_of_vol_20 | 30 | volatility | 9 | 23 | 39.1% | 37.0% | 2.2% |
| vta_vol_of_vol_20 | 30 | volatility | 10 | 23 | 39.1% | 33.3% | 5.8% |
| vta_vol_of_vol_20 | 30 | volatility | 11 | 23 | 43.5% | 44.9% | -1.4% |
| vta_vol_of_vol_20 | 30 | volatility | 12 | 23 | 43.5% | 44.6% | -1.1% |
| vta_vol_of_vol_20 | 30 | volatility | 13 | 23 | 43.5% | 44.6% | -1.1% |
| vta_vol_of_vol_20 | 30 | volatility | 14 | 23 | 43.5% | 44.2% | -0.7% |
| vta_vol_of_vol_20 | 30 | volatility | 15 | 23 | 47.8% | 47.8% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 16 | 23 | 43.5% | 46.4% | -2.9% |
| vta_vol_of_vol_20 | 30 | volatility | 17 | 23 | 47.8% | 47.8% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 18 | 22 | 40.9% | 40.9% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 19 | 22 | 45.5% | 47.0% | -1.5% |
| vta_vol_of_vol_20 | 30 | volatility | 20 | 23 | 65.2% | 65.2% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 21 | 23 | 56.5% | 53.6% | 2.9% |
| vta_vol_of_vol_20 | 30 | volatility | 22 | 23 | 52.2% | 50.2% | 2.0% |
| vta_vol_of_vol_20 | 30 | volatility | 23 | 23 | 47.8% | 46.1% | 1.7% |
| vta_vol_of_vol_20 | 30 | volatility | 24 | 23 | 47.8% | 45.1% | 2.8% |
| vta_vol_of_vol_20 | 30 | volatility | 25 | 23 | 47.8% | 46.1% | 1.7% |
| vta_vol_of_vol_20 | 30 | volatility | 26 | 23 | 47.8% | 45.7% | 2.2% |
| vta_vol_of_vol_20 | 30 | volatility | 27 | 23 | 43.5% | 43.8% | -0.4% |
| vta_vol_of_vol_20 | 30 | volatility | 28 | 23 | 43.5% | 41.7% | 1.7% |
| vta_vol_of_vol_20 | 30 | volatility | 29 | 23 | 39.1% | 36.4% | 2.8% |

## Purged OOS probability model by information family

| horizon | axis | n_eff | brier | baseline_brier | log_loss | mean_probability | event_rate | latest_probability | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | market | 150 | 0.2603 | 23.0% | 0.7217 | 0.6632 | 64.0% | 0.6248 | research/context |
| 3 | volatility | 150 | 0.2070 | 19.6% | 0.6093 | 0.2891 | 26.7% | 0.3132 | research/context |
| 7 | market | 63 | 0.2765 | 22.7% | 0.8097 | 0.6815 | 65.1% | 0.6690 | research/context |
| 7 | volatility | 63 | 0.2746 | 23.9% | 0.7462 | 0.4428 | 39.7% | 0.4788 | research/context |
| 14 | market | 30 | 0.2489 | 21.0% | 0.7602 | 0.7501 | 70.0% | 0.5776 | research/context |
| 14 | volatility | 30 | 0.2363 | 24.6% | 0.6756 | 0.4738 | 56.7% | 0.7429 | research/context |
| 30 | market | 13 | 0.2110 | 17.8% | 0.6599 | 0.8574 | 76.9% | 0.9015 | research/context |
| 30 | volatility | 13 | 0.2987 | 24.9% | 0.8003 | 0.4491 | 46.2% | 0.2716 | research/context |

## Probability calibration by forecast bin

| horizon | axis | probability_bin | n | mean_probability | event_rate |
| --- | --- | --- | --- | --- | --- |
| 3 | market | (-0.001, 0.4] | 6 | 0.2776 | 83.3% |
| 3 | market | (0.4, 0.5] | 10 | 0.4619 | 80.0% |
| 3 | market | (0.5, 0.6] | 27 | 0.5460 | 74.1% |
| 3 | market | (0.6, 1.0] | 107 | 0.7331 | 58.9% |
| 3 | volatility | (-0.001, 0.4] | 130 | 0.2615 | 27.7% |
| 3 | volatility | (0.4, 0.5] | 16 | 0.4415 | 18.8% |
| 3 | volatility | (0.5, 0.6] | 3 | 0.5336 | 33.3% |
| 3 | volatility | (0.6, 1.0] | 1 | 0.6990 | 0.0% |
| 7 | market | (-0.001, 0.4] | 3 | 0.1066 | 66.7% |
| 7 | market | (0.4, 0.5] | 4 | 0.4282 | 100.0% |
| 7 | market | (0.5, 0.6] | 7 | 0.5483 | 71.4% |
| 7 | market | (0.6, 1.0] | 49 | 0.7564 | 61.2% |
| 7 | volatility | (-0.001, 0.4] | 26 | 0.2707 | 42.3% |
| 7 | volatility | (0.4, 0.5] | 10 | 0.4495 | 50.0% |
| 7 | volatility | (0.5, 0.6] | 14 | 0.5583 | 35.7% |
| 7 | volatility | (0.6, 1.0] | 13 | 0.6578 | 30.8% |
| 14 | market | (-0.001, 0.4] | 1 | 0.1442 | 0.0% |
| 14 | market | (0.4, 0.5] | 1 | 0.4647 | 100.0% |
| 14 | market | (0.5, 0.6] | 4 | 0.5695 | 75.0% |
| 14 | market | (0.6, 1.0] | 24 | 0.8174 | 70.8% |
| 14 | volatility | (-0.001, 0.4] | 11 | 0.2643 | 45.5% |
| 14 | volatility | (0.4, 0.5] | 5 | 0.4225 | 20.0% |
| 14 | volatility | (0.5, 0.6] | 5 | 0.5702 | 80.0% |
| 14 | volatility | (0.6, 1.0] | 9 | 0.7047 | 77.8% |
| 30 | market | (0.6, 1.0] | 13 | 0.8574 | 76.9% |
| 30 | volatility | (-0.001, 0.4] | 4 | 0.2884 | 50.0% |
| 30 | volatility | (0.4, 0.5] | 4 | 0.4415 | 75.0% |
| 30 | volatility | (0.5, 0.6] | 4 | 0.5554 | 25.0% |
| 30 | volatility | (0.6, 1.0] | 1 | 0.6977 | 0.0% |

## Incremental OOS value of each information family

| horizon | axis | family | n_eff | full_brier | without_family_brier | incremental_brier_value | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3 | market | forecast_gap | 150 | 0.2603 | 0.2621 | 0.0018 | research/context |
| 3 | market | global_fx | 150 | 0.2603 | 0.2581 | -0.0021 | research/context |
| 3 | market | iv_local | 150 | 0.2603 | 0.2569 | -0.0034 | research/context |
| 3 | market | price_regime | 150 | 0.2603 | 0.2524 | -0.0079 | research/context |
| 3 | market | rv_local | 150 | 0.2603 | 0.2525 | -0.0078 | research/context |
| 3 | volatility | forecast_gap | 150 | 0.2070 | 0.2028 | -0.0042 | research/context |
| 3 | volatility | global_fx | 150 | 0.2070 | 0.2061 | -0.0010 | research/context |
| 3 | volatility | iv_local | 150 | 0.2070 | 0.2066 | -0.0004 | research/context |
| 3 | volatility | price_regime | 150 | 0.2070 | 0.2085 | 0.0015 | research/context |
| 3 | volatility | rv_local | 150 | 0.2070 | 0.2016 | -0.0055 | research/context |
| 7 | market | forecast_gap | 63 | 0.2765 | 0.2688 | -0.0078 | research/context |
| 7 | market | global_fx | 63 | 0.2765 | 0.2751 | -0.0014 | research/context |
| 7 | market | iv_local | 63 | 0.2765 | 0.2738 | -0.0027 | research/context |
| 7 | market | price_regime | 63 | 0.2765 | 0.2725 | -0.0040 | research/context |
| 7 | market | rv_local | 63 | 0.2765 | 0.2679 | -0.0086 | research/context |
| 7 | volatility | forecast_gap | 63 | 0.2746 | 0.2610 | -0.0136 | research/context |
| 7 | volatility | global_fx | 63 | 0.2746 | 0.2729 | -0.0017 | research/context |
| 7 | volatility | iv_local | 63 | 0.2746 | 0.2648 | -0.0099 | research/context |
| 7 | volatility | price_regime | 63 | 0.2746 | 0.2594 | -0.0153 | research/context |
| 7 | volatility | rv_local | 63 | 0.2746 | 0.2710 | -0.0037 | research/context |
| 14 | market | forecast_gap | 30 | 0.2489 | 0.2433 | -0.0056 | research/context |
| 14 | market | global_fx | 30 | 0.2489 | 0.2337 | -0.0152 | research/context |
| 14 | market | iv_local | 30 | 0.2489 | 0.2449 | -0.0040 | research/context |
| 14 | market | price_regime | 30 | 0.2489 | 0.2381 | -0.0108 | research/context |
| 14 | market | rv_local | 30 | 0.2489 | 0.2429 | -0.0060 | research/context |
| 14 | volatility | forecast_gap | 30 | 0.2363 | 0.2141 | -0.0221 | research/context |
| 14 | volatility | global_fx | 30 | 0.2363 | 0.2975 | 0.0612 | research/context |
| 14 | volatility | iv_local | 30 | 0.2363 | 0.2283 | -0.0079 | research/context |
| 14 | volatility | price_regime | 30 | 0.2363 | 0.2341 | -0.0022 | research/context |
| 14 | volatility | rv_local | 30 | 0.2363 | 0.2376 | 0.0013 | research/context |
| 30 | market | forecast_gap | 13 | 0.2110 | 0.1895 | -0.0216 | research/context |
| 30 | market | global_fx | 13 | 0.2110 | 0.2213 | 0.0103 | research/context |
| 30 | market | iv_local | 13 | 0.2110 | 0.2092 | -0.0018 | research/context |
| 30 | market | price_regime | 13 | 0.2110 | 0.2063 | -0.0047 | research/context |
| 30 | market | rv_local | 13 | 0.2110 | 0.2090 | -0.0021 | research/context |
| 30 | volatility | forecast_gap | 13 | 0.2987 | 0.2650 | -0.0337 | research/context |
| 30 | volatility | global_fx | 13 | 0.2987 | 0.3261 | 0.0274 | research/context |
| 30 | volatility | iv_local | 13 | 0.2987 | 0.2876 | -0.0111 | research/context |
| 30 | volatility | price_regime | 13 | 0.2987 | 0.2962 | -0.0025 | research/context |
| 30 | volatility | rv_local | 13 | 0.2987 | 0.2958 | -0.0030 | research/context |

## Indicator aggregate direction tests

| indicator | horizon | axis | n | accuracy | baseline | lift | adjusted_accuracy | ci_low | ci_high | p_value | strength | brier_walk_forward | brier_baseline | nonoverlap_n_min | n_eff | nonoverlap_accuracy_min | nonoverlap_accuracy | nonoverlap_accuracy_max | rank_ic | top_bottom_quintile_spread | positive_years | tested_years | positive_regimes | tested_regimes | sample_quality | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | 715 | 46.6% | 43.1% | 3.4% | 46.5% | 42.9% | 50.2% | 0.1421 | 3 | 0.2516 | 24.5% | 238 | 238 | 44.1% | 46.0% | 49.6% | 0.1480 | 0.2394 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| atr_5_20_ratio | 7 | volatility | 711 | 46.3% | 42.0% | 4.2% | 46.2% | 42.6% | 49.9% | 0.1949 | 3 | 0.2556 | 24.4% | 101 | 101 | 41.6% | 47.1% | 50.0% | 0.1968 | 0.2495 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| atr_5_20_ratio | 14 | volatility | 704 | 48.4% | 42.2% | 6.3% | 48.3% | 44.8% | 52.1% | 0.1845 | 5 | 0.2549 | 24.4% | 50 | 50 | 41.2% | 48.5% | 58.0% | 0.2171 | 0.2177 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| atr_5_20_ratio | 30 | volatility | 688 | 49.9% | 42.4% | 7.4% | 49.6% | 46.1% | 53.6% | 0.2401 | 5 | 0.2571 | 24.4% | 22 | 22 | 30.4% | 52.2% | 69.6% | 0.1693 | 0.1479 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| downside_share_20 | 3 | volatility | 715 | 48.1% | 46.4% | 1.7% | 48.1% | 44.5% | 51.8% | 0.2964 | 2 | 0.2528 | 24.9% | 238 | 238 | 44.4% | 47.9% | 52.1% | -0.0257 | -0.1081 | 2 | 4 | 3 | 4 | גבוהה | 1.0000 |
| downside_share_20 | 7 | volatility | 711 | 40.8% | 40.0% | 0.8% | 40.8% | 37.2% | 44.4% | 0.4382 | 1 | 0.2462 | 24.0% | 101 | 101 | 36.3% | 37.6% | 48.0% | -0.0873 | -0.1108 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| downside_share_20 | 14 | volatility | 704 | 33.9% | 35.6% | -1.6% | 34.0% | 30.5% | 37.5% | 0.5946 | 1 | 0.2347 | 22.9% | 50 | 50 | 28.0% | 35.0% | 38.0% | -0.2238 | -0.2069 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| downside_share_20 | 30 | volatility | 688 | 32.4% | 32.7% | -0.3% | 32.4% | 29.0% | 36.0% | 0.5128 | 1 | 0.2308 | 22.0% | 22 | 22 | 17.4% | 34.8% | 43.5% | -0.2808 | -0.2671 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| expected_move_3d_points | 3 | volatility | 715 | 35.5% | 32.0% | 3.5% | 35.4% | 32.1% | 39.1% | 0.1219 | 3 | 0.2321 | 21.8% | 238 | 238 | 33.6% | 35.3% | 37.7% | 0.2167 | 0.3804 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| expected_move_3d_points | 7 | volatility | 711 | 38.1% | 34.0% | 4.1% | 38.0% | 34.6% | 41.7% | 0.1928 | 3 | 0.2412 | 22.4% | 101 | 101 | 33.3% | 38.6% | 40.2% | 0.3158 | 0.3865 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| expected_move_3d_points | 14 | volatility | 704 | 41.5% | 34.9% | 6.6% | 41.3% | 37.9% | 45.2% | 0.1651 | 5 | 0.2498 | 22.7% | 50 | 50 | 34.0% | 42.0% | 50.0% | 0.3226 | 0.3370 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| expected_move_3d_points | 30 | volatility | 688 | 41.1% | 35.9% | 5.3% | 41.0% | 37.5% | 44.8% | 0.3027 | 4 | 0.2520 | 23.0% | 22 | 22 | 21.7% | 43.5% | 60.9% | 0.3346 | 0.3200 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| forecast_rv_3d | 3 | volatility | 715 | 35.5% | 32.0% | 3.5% | 35.4% | 32.1% | 39.1% | 0.1219 | 3 | 0.2321 | 21.8% | 238 | 238 | 33.6% | 35.3% | 37.7% | 0.2241 | 0.3589 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| forecast_rv_3d | 7 | volatility | 711 | 38.1% | 34.0% | 4.1% | 38.0% | 34.6% | 41.7% | 0.1928 | 3 | 0.2412 | 22.4% | 101 | 101 | 33.3% | 38.6% | 40.2% | 0.3342 | 0.3999 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| forecast_rv_3d | 14 | volatility | 704 | 41.5% | 34.9% | 6.6% | 41.3% | 37.9% | 45.2% | 0.1651 | 5 | 0.2498 | 22.7% | 50 | 50 | 34.0% | 42.0% | 50.0% | 0.3440 | 0.3959 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| forecast_rv_3d | 30 | volatility | 688 | 41.1% | 35.9% | 5.3% | 41.0% | 37.5% | 44.8% | 0.3027 | 4 | 0.2520 | 23.0% | 22 | 22 | 21.7% | 43.5% | 60.9% | 0.3548 | 0.3965 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| gap_share_20 | 3 | volatility | 715 | 34.1% | 32.8% | 1.3% | 34.1% | 30.7% | 37.7% | 0.3329 | 2 | 0.2272 | 22.0% | 238 | 238 | 31.8% | 33.6% | 37.0% | -0.0781 | -0.2480 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| gap_share_20 | 7 | volatility | 711 | 33.6% | 31.0% | 2.6% | 33.5% | 30.2% | 37.2% | 0.2867 | 3 | 0.2281 | 21.4% | 101 | 101 | 28.4% | 33.7% | 37.6% | -0.1552 | -0.2415 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | 704 | 28.0% | 30.3% | -2.3% | 28.0% | 24.8% | 31.4% | 0.6390 | 1 | 0.2087 | 21.1% | 50 | 50 | 18.0% | 30.0% | 33.3% | -0.2291 | -0.2492 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | 688 | 23.3% | 29.6% | -6.3% | 23.4% | 20.3% | 26.6% | 0.7417 | 1 | 0.1859 | 20.8% | 22 | 22 | 4.3% | 26.1% | 34.8% | -0.3080 | -0.3139 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| har_rv_3d | 3 | volatility | 612 | 34.8% | 31.2% | 3.6% | 34.7% | 31.1% | 38.7% | 0.1362 | 3 | 0.2299 | 21.5% | 204 | 204 | 32.4% | 34.3% | 37.7% | 0.2159 | 0.3995 | 3 | 3 | 3 | 4 | גבוהה | 1.0000 |
| har_rv_3d | 7 | volatility | 608 | 37.3% | 34.4% | 2.9% | 37.2% | 33.6% | 41.2% | 0.2830 | 3 | 0.2373 | 22.6% | 86 | 86 | 33.3% | 36.8% | 40.7% | 0.2975 | 0.3246 | 2 | 3 | 2 | 4 | גבוהה | 1.0000 |
| har_rv_3d | 14 | volatility | 601 | 40.1% | 36.0% | 4.1% | 40.0% | 36.3% | 44.1% | 0.2897 | 3 | 0.2455 | 23.0% | 42 | 42 | 28.6% | 39.5% | 53.5% | 0.2751 | 0.2833 | 3 | 3 | 3 | 4 | גבוהה | 1.0000 |
| har_rv_3d | 30 | volatility | 585 | 39.1% | 37.6% | 1.6% | 39.1% | 35.3% | 43.2% | 0.4433 | 2 | 0.2492 | 23.5% | 19 | 19 | 15.8% | 41.1% | 57.9% | 0.2663 | 0.2252 | 2 | 3 | 2 | 4 | גבוהה | 1.0000 |
| local_global_stress_spread | 3 | volatility | 616 | 45.3% | 42.2% | 3.1% | 45.2% | 41.4% | 49.2% | 0.1873 | 3 | 0.2508 | 24.4% | 205 | 205 | 42.9% | 45.9% | 47.1% | 0.0648 | 0.0863 | 2 | 3 | 3 | 4 | גבוהה | 1.0000 |
| local_global_stress_spread | 7 | volatility | 612 | 46.6% | 41.9% | 4.6% | 46.4% | 42.7% | 50.5% | 0.1901 | 4 | 0.2545 | 24.3% | 87 | 87 | 42.0% | 47.1% | 49.4% | 0.1093 | 0.0849 | 3 | 3 | 3 | 4 | גבוהה | 1.0000 |
| local_global_stress_spread | 14 | volatility | 605 | 42.3% | 41.5% | 0.9% | 42.3% | 38.4% | 46.3% | 0.4544 | 1 | 0.2530 | 24.3% | 43 | 43 | 30.2% | 43.7% | 51.2% | 0.0512 | 0.0661 | 1 | 3 | 2 | 4 | גבוהה | 1.0000 |
| local_global_stress_spread | 30 | volatility | 589 | 41.9% | 40.7% | 1.2% | 41.9% | 38.0% | 46.0% | 0.4569 | 2 | 0.2569 | 24.1% | 19 | 19 | 15.8% | 42.1% | 60.0% | 0.0724 | 0.0946 | 1 | 3 | 3 | 4 | גבוהה | 1.0000 |
| matched_vrp_3d | 3 | volatility | 612 | 24.3% | 24.3% | 0.0% | 24.3% | 21.1% | 27.9% | 0.5000 | 1 | 0.1861 | 18.4% | 204 | 204 | 21.6% | 25.5% | 26.0% | -0.0385 | -0.0248 | 1 | 3 | 0 | 4 | גבוהה | 1.0000 |
| matched_vrp_3d | 7 | volatility | 608 | 36.3% | 36.3% | 0.0% | 36.3% | 32.6% | 40.2% | 0.5000 | 1 | 0.2372 | 23.1% | 86 | 86 | 34.5% | 36.8% | 37.9% | 0.0370 | 0.0888 | 2 | 3 | 0 | 4 | גבוהה | 1.0000 |
| matched_vrp_3d | 14 | volatility | 601 | 47.1% | 47.1% | 0.0% | 47.1% | 43.1% | 51.1% | 0.5000 | 1 | 0.2654 | 24.9% | 42 | 42 | 41.9% | 47.7% | 51.2% | 0.0309 | 0.0455 | 0 | 3 | 0 | 4 | גבוהה | 1.0000 |
| matched_vrp_3d | 30 | volatility | 585 | 52.1% | 52.1% | 0.0% | 52.1% | 48.1% | 56.2% | 0.5000 | 1 | 0.2657 | 25.0% | 19 | 19 | 35.0% | 53.8% | 68.4% | 0.0507 | 0.0619 | 1 | 3 | 1 | 4 | גבוהה | 1.0000 |
| range_position_20 | 3 | volatility | 715 | 3.6% | 3.6% | 0.0% | 3.6% | 2.5% | 5.3% | 0.5000 | 1 | 0.0353 | 3.5% | 238 | 238 | 2.1% | 3.8% | 5.0% | — | — | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| range_position_20 | 7 | volatility | 711 | 6.5% | 6.5% | 0.0% | 6.5% | 4.9% | 8.5% | 0.5000 | 1 | 0.0613 | 6.1% | 101 | 101 | 4.0% | 6.9% | 8.8% | — | — | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| range_position_20 | 14 | volatility | 704 | 6.7% | 6.7% | 0.0% | 6.7% | 5.1% | 8.8% | 0.5000 | 1 | 0.0627 | 6.2% | 50 | 50 | 2.0% | 6.0% | 12.0% | — | — | 0 | 4 | 2 | 4 | גבוהה | 1.0000 |
| range_position_20 | 30 | volatility | 688 | 6.7% | 6.7% | 0.0% | 6.7% | 5.0% | 8.8% | 0.5000 | 1 | 0.0632 | 6.2% | 22 | 22 | 0.0% | 4.3% | 18.2% | — | — | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 3 | market | 367 | 50.7% | 45.4% | 5.3% | 50.4% | 45.6% | 55.8% | 0.1195 | 4 | 0.2532 | 24.8% | 121 | 122 | 47.9% | 49.6% | 54.5% | 0.1681 | 0.0129 | 4 | 4 | 2 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 3 | volatility | 715 | 3.6% | 3.6% | 0.0% | 3.6% | 2.5% | 5.3% | 0.5000 | 1 | 0.0353 | 3.5% | 238 | 238 | 2.1% | 3.8% | 5.0% | — | — | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 7 | market | 365 | 55.6% | 45.5% | 10.1% | 55.1% | 50.5% | 60.6% | 0.0713 | 7 | 0.2543 | 24.8% | 46 | 52 | 44.9% | 55.4% | 66.0% | 0.2046 | 0.0200 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 7 | volatility | 711 | 6.5% | 6.5% | 0.0% | 6.5% | 4.9% | 8.5% | 0.5000 | 1 | 0.0613 | 6.1% | 101 | 101 | 4.0% | 6.9% | 8.8% | — | — | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 14 | market | 361 | 43.8% | 41.0% | 2.8% | 43.6% | 38.7% | 48.9% | 0.3890 | 3 | 0.2516 | 24.2% | 17 | 25 | 22.2% | 42.6% | 64.0% | 0.1088 | 0.0093 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 14 | volatility | 704 | 6.7% | 6.7% | 0.0% | 6.7% | 5.1% | 8.8% | 0.5000 | 1 | 0.0627 | 6.2% | 50 | 50 | 2.0% | 6.0% | 12.0% | — | — | 0 | 4 | 2 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 30 | market | 351 | 40.2% | 39.7% | 0.5% | 40.1% | 35.2% | 45.4% | 0.4871 | 1 | 0.2469 | 23.9% | 7 | 11 | 0.0% | 38.9% | 63.6% | 0.0052 | 0.0031 | 2 | 4 | 3 | 4 | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 30 | volatility | 688 | 6.7% | 6.7% | 0.0% | 6.7% | 5.0% | 8.8% | 0.5000 | 1 | 0.0632 | 6.2% | 22 | 22 | 0.0% | 4.3% | 18.2% | — | — | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| rs_range_5_20 | 3 | volatility | 715 | 45.9% | 42.6% | 3.3% | 45.8% | 42.3% | 49.5% | 0.1502 | 3 | 0.2510 | 24.4% | 238 | 238 | 42.9% | 46.0% | 48.7% | 0.1028 | 0.2186 | 3 | 4 | 4 | 4 | גבוהה | 1.0000 |
| rs_range_5_20 | 7 | volatility | 711 | 47.0% | 41.1% | 5.9% | 46.8% | 43.3% | 50.7% | 0.1138 | 4 | 0.2525 | 24.2% | 101 | 101 | 37.3% | 47.5% | 52.0% | 0.1916 | 0.2135 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| rs_range_5_20 | 14 | volatility | 704 | 46.2% | 40.9% | 5.3% | 46.0% | 42.5% | 49.9% | 0.2250 | 4 | 0.2536 | 24.2% | 50 | 50 | 35.3% | 47.0% | 54.0% | 0.2130 | 0.1965 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| rs_range_5_20 | 30 | volatility | 688 | 48.7% | 41.2% | 7.5% | 48.5% | 45.0% | 52.4% | 0.2370 | 5 | 0.2572 | 24.2% | 22 | 22 | 30.4% | 47.8% | 65.2% | 0.2091 | 0.1327 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | 675 | 45.8% | 44.1% | 1.7% | 45.7% | 42.1% | 49.5% | 0.3043 | 2 | 0.2515 | 24.6% | 225 | 225 | 41.8% | 46.2% | 49.3% | -0.1714 | -0.2728 | 2 | 4 | 4 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | 671 | 37.4% | 36.0% | 1.4% | 37.4% | 33.8% | 41.1% | 0.3866 | 2 | 0.2398 | 23.0% | 95 | 95 | 32.3% | 37.5% | 44.8% | -0.3453 | -0.3968 | 2 | 4 | 3 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | 664 | 31.6% | 32.6% | -1.0% | 31.7% | 28.2% | 35.3% | 0.5571 | 1 | 0.2279 | 22.0% | 47 | 47 | 22.9% | 30.5% | 40.4% | -0.4085 | -0.3981 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | 648 | 25.8% | 28.8% | -3.0% | 25.9% | 22.6% | 29.3% | 0.6201 | 1 | 0.2215 | 20.5% | 21 | 21 | 14.3% | 25.5% | 40.9% | -0.4670 | -0.3744 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 3 | volatility | 715 | 55.0% | 53.4% | 1.6% | 54.9% | 51.3% | 58.6% | 0.3128 | 2 | 0.2502 | 24.9% | 238 | 238 | 54.0% | 55.0% | 55.9% | 0.0877 | 0.1451 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 7 | volatility | 711 | 47.7% | 47.8% | -0.1% | 47.7% | 44.0% | 51.4% | 0.5058 | 1 | 0.2553 | 24.9% | 101 | 101 | 43.6% | 47.1% | 51.5% | 0.0732 | 0.1575 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 14 | volatility | 704 | 48.7% | 44.3% | 4.4% | 48.6% | 45.0% | 52.4% | 0.2653 | 4 | 0.2566 | 24.7% | 50 | 50 | 37.3% | 50.0% | 62.0% | 0.0973 | 0.1677 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| rv_acceleration | 30 | volatility | 688 | 48.1% | 43.0% | 5.1% | 48.0% | 44.4% | 51.8% | 0.3157 | 4 | 0.2575 | 24.5% | 22 | 22 | 30.4% | 47.8% | 60.9% | 0.0854 | 0.1608 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| trend_efficiency_20 | 3 | volatility | 715 | 30.3% | 28.4% | 2.0% | 30.3% | 27.1% | 33.8% | 0.2470 | 2 | 0.2138 | 20.3% | 238 | 238 | 29.7% | 29.8% | 31.5% | 0.0305 | 0.0778 | 3 | 4 | 4 | 4 | גבוהה | 1.0000 |
| trend_efficiency_20 | 7 | volatility | 711 | 34.3% | 32.5% | 1.8% | 34.3% | 30.9% | 37.9% | 0.3493 | 2 | 0.2313 | 21.9% | 101 | 101 | 30.7% | 33.3% | 38.6% | -0.0252 | 0.0062 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| trend_efficiency_20 | 14 | volatility | 704 | 33.9% | 35.6% | -1.7% | 34.0% | 30.5% | 37.5% | 0.5987 | 1 | 0.2353 | 22.9% | 50 | 50 | 25.5% | 34.0% | 44.0% | -0.1062 | -0.0656 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| trend_efficiency_20 | 30 | volatility | 688 | 37.9% | 36.3% | 1.6% | 37.9% | 34.4% | 41.6% | 0.4370 | 2 | 0.2524 | 23.1% | 22 | 22 | 30.4% | 37.0% | 52.2% | -0.1404 | -0.0774 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 3 | market | 630 | 51.0% | 51.0% | -0.0% | 51.0% | 47.1% | 54.8% | 0.5047 | 1 | 0.2521 | 25.0% | 206 | 210 | 45.2% | 52.4% | 55.1% | -0.0083 | 0.0002 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 3 | volatility | 715 | 47.0% | 43.2% | 3.8% | 46.9% | 43.4% | 50.7% | 0.1178 | 3 | 0.2515 | 24.5% | 238 | 238 | 44.5% | 45.8% | 50.6% | 0.0545 | 0.0802 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 7 | market | 627 | 48.6% | 51.2% | -2.5% | 48.7% | 44.8% | 52.6% | 0.6830 | 1 | 0.2544 | 25.0% | 85 | 89 | 45.2% | 47.1% | 54.1% | -0.0168 | -0.0024 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | 711 | 46.0% | 41.8% | 4.2% | 45.9% | 42.4% | 49.7% | 0.1946 | 3 | 0.2524 | 24.3% | 101 | 101 | 41.2% | 45.1% | 52.5% | 0.1506 | 0.1854 | 4 | 4 | 2 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 14 | market | 620 | 54.0% | 51.7% | 2.4% | 54.0% | 50.1% | 57.9% | 0.3763 | 2 | 0.2533 | 25.0% | 40 | 44 | 42.2% | 54.5% | 68.2% | 0.0358 | -0.0017 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 14 | volatility | 704 | 47.2% | 40.9% | 6.3% | 47.0% | 43.5% | 50.9% | 0.1843 | 5 | 0.2532 | 24.2% | 50 | 50 | 21.6% | 48.0% | 62.0% | 0.1300 | 0.1224 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 30 | market | 605 | 50.9% | 52.3% | -1.3% | 51.0% | 46.9% | 54.9% | 0.5479 | 1 | 0.2535 | 24.9% | 18 | 20 | 27.8% | 50.0% | 73.7% | -0.0113 | -0.0134 | 1 | 4 | 3 | 4 | גבוהה | 1.0000 |
| usdils_change_5d | 30 | volatility | 688 | 46.7% | 40.4% | 6.3% | 46.5% | 43.0% | 50.4% | 0.2738 | 5 | 0.2503 | 24.1% | 22 | 22 | 22.7% | 45.7% | 69.6% | 0.0960 | 0.0984 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 3 | market | 635 | 58.6% | 57.6% | 1.0% | 58.6% | 54.7% | 62.4% | 0.3810 | 2 | 0.2452 | 24.4% | 211 | 211 | 56.9% | 59.0% | 59.9% | -0.0188 | 0.0010 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 3 | volatility | 715 | 56.8% | 54.8% | 1.9% | 56.7% | 53.1% | 60.4% | 0.2741 | 2 | 0.2481 | 24.8% | 238 | 238 | 55.2% | 57.1% | 58.0% | -0.0019 | -0.0246 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 7 | market | 632 | 57.8% | 58.7% | -1.0% | 57.8% | 53.9% | 61.5% | 0.5735 | 1 | 0.2485 | 24.2% | 85 | 90 | 54.1% | 57.3% | 64.1% | -0.0226 | 0.0027 | 2 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 7 | volatility | 711 | 49.4% | 44.8% | 4.5% | 49.2% | 45.7% | 53.0% | 0.1805 | 4 | 0.2554 | 24.7% | 101 | 101 | 46.1% | 50.0% | 52.5% | 0.0232 | 0.0328 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | market | 625 | 61.4% | 63.7% | -2.3% | 61.5% | 57.6% | 65.2% | 0.6233 | 1 | 0.2457 | 23.1% | 41 | 44 | 54.5% | 62.2% | 66.7% | -0.0013 | 0.0003 | 3 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | 704 | 44.2% | 39.1% | 5.1% | 44.0% | 40.5% | 47.9% | 0.2313 | 4 | 0.2541 | 23.8% | 50 | 50 | 32.0% | 43.1% | 54.0% | 0.0692 | 0.0703 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | market | 609 | 64.4% | 67.7% | -3.4% | 64.5% | 60.5% | 68.1% | 0.6266 | 1 | 0.2501 | 21.9% | 15 | 20 | 47.1% | 65.8% | 81.0% | 0.0314 | 0.0068 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | 688 | 36.9% | 36.1% | 0.8% | 36.9% | 33.4% | 40.6% | 0.4675 | 1 | 0.2428 | 23.1% | 22 | 22 | 21.7% | 34.8% | 56.5% | -0.0359 | -0.0241 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 3 | market | 715 | 57.2% | 57.5% | -0.3% | 57.2% | 53.5% | 60.8% | 0.5341 | 1 | 0.2474 | 24.4% | 237 | 238 | 57.0% | 57.0% | 57.7% | -0.0582 | -0.0018 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 3 | volatility | 715 | 67.4% | 64.5% | 2.9% | 67.3% | 63.9% | 70.7% | 0.1731 | 3 | 0.2221 | 22.9% | 238 | 238 | 65.3% | 68.1% | 68.9% | 0.0298 | 0.0369 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 7 | market | 711 | 57.1% | 59.3% | -2.2% | 57.2% | 53.4% | 60.7% | 0.6770 | 1 | 0.2503 | 24.1% | 99 | 101 | 53.4% | 58.6% | 60.6% | -0.0498 | -0.0003 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 7 | volatility | 711 | 55.4% | 51.5% | 3.9% | 55.3% | 51.7% | 59.0% | 0.2158 | 3 | 0.2548 | 25.0% | 101 | 101 | 49.0% | 55.4% | 61.4% | 0.0408 | 0.0782 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 14 | market | 704 | 65.2% | 66.1% | -0.9% | 65.2% | 61.6% | 68.6% | 0.5552 | 1 | 0.2374 | 22.4% | 47 | 50 | 56.9% | 64.6% | 74.5% | -0.0133 | 0.0006 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 14 | volatility | 704 | 49.0% | 44.6% | 4.4% | 48.9% | 45.3% | 52.7% | 0.2664 | 4 | 0.2652 | 24.7% | 50 | 50 | 41.2% | 48.0% | 58.0% | 0.0636 | 0.0375 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | market | 688 | 68.6% | 70.9% | -2.2% | 68.7% | 65.0% | 72.0% | 0.5918 | 1 | 0.2408 | 20.7% | 21 | 22 | 54.5% | 68.9% | 81.8% | 0.0344 | 0.0042 | 1 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | volatility | 688 | 43.5% | 41.1% | 2.3% | 43.4% | 39.8% | 47.2% | 0.4117 | 2 | 0.2691 | 24.2% | 22 | 22 | 26.1% | 43.5% | 56.5% | 0.0405 | 0.0061 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | market | 693 | 57.0% | 58.3% | -1.3% | 57.0% | 53.3% | 60.6% | 0.6556 | 1 | 0.2479 | 24.3% | 228 | 231 | 56.3% | 56.8% | 57.9% | -0.0021 | -0.0023 | 0 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | 715 | 66.0% | 64.7% | 1.3% | 66.0% | 62.5% | 69.4% | 0.3388 | 2 | 0.2270 | 22.8% | 238 | 238 | 64.4% | 66.0% | 67.6% | 0.0052 | -0.0600 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 7 | market | 689 | 57.6% | 59.7% | -2.1% | 57.7% | 53.9% | 61.3% | 0.6660 | 1 | 0.2499 | 24.1% | 97 | 98 | 51.5% | 58.2% | 61.2% | 0.0395 | -0.0007 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | 711 | 53.4% | 51.6% | 1.9% | 53.4% | 49.8% | 57.1% | 0.3527 | 2 | 0.2571 | 25.0% | 101 | 101 | 46.1% | 54.5% | 58.4% | 0.0043 | -0.0028 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 14 | market | 682 | 66.4% | 66.8% | -0.3% | 66.4% | 62.8% | 69.9% | 0.5202 | 1 | 0.2345 | 22.2% | 46 | 48 | 57.1% | 66.0% | 74.0% | 0.0732 | 0.0064 | 1 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 14 | volatility | 704 | 45.9% | 44.4% | 1.5% | 45.8% | 42.2% | 49.6% | 0.4148 | 2 | 0.2649 | 24.7% | 50 | 50 | 41.2% | 45.0% | 52.0% | 0.0161 | 0.0024 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 30 | market | 666 | 71.0% | 72.3% | -1.3% | 71.1% | 67.5% | 74.3% | 0.5532 | 1 | 0.2330 | 20.0% | 19 | 22 | 58.3% | 70.0% | 85.0% | 0.1481 | 0.0206 | 0 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | 688 | 43.2% | 41.0% | 2.2% | 43.1% | 39.5% | 46.9% | 0.4167 | 2 | 0.2694 | 24.2% | 22 | 22 | 30.4% | 43.5% | 56.5% | 0.0155 | -0.0006 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vrp_spread | 3 | volatility | 715 | 44.2% | 38.7% | 5.5% | 44.0% | 40.6% | 47.9% | 0.0406 | 4 | 0.2492 | 23.7% | 238 | 238 | 41.2% | 44.4% | 47.1% | 0.2916 | 0.4947 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vrp_spread | 7 | volatility | 711 | 52.0% | 45.8% | 6.3% | 51.9% | 48.4% | 55.7% | 0.1033 | 5 | 0.2552 | 24.8% | 101 | 101 | 46.5% | 52.9% | 57.4% | 0.4858 | 0.5684 | 3 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vrp_spread | 14 | volatility | 704 | 54.4% | 50.6% | 3.8% | 54.3% | 50.7% | 58.0% | 0.2950 | 3 | 0.2595 | 25.0% | 50 | 50 | 46.0% | 54.5% | 62.0% | 0.5039 | 0.5336 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vrp_spread | 30 | volatility | 688 | 58.9% | 54.2% | 4.7% | 58.7% | 55.2% | 62.5% | 0.3298 | 4 | 0.2611 | 24.8% | 22 | 22 | 47.8% | 58.7% | 78.3% | 0.5620 | 0.5855 | 3 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vta35 | 3 | market | 603 | 48.9% | 51.1% | -2.2% | 49.0% | 45.0% | 52.9% | 0.7292 | 1 | 0.2527 | 25.0% | 198 | 201 | 47.1% | 49.2% | 50.5% | -0.0817 | -0.0047 | 0 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vta35 | 3 | volatility | 676 | 48.8% | 43.6% | 5.2% | 48.7% | 45.1% | 52.6% | 0.0571 | 4 | 0.2531 | 24.6% | 225 | 225 | 46.0% | 46.7% | 53.8% | 0.0926 | 0.1304 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35 | 7 | market | 601 | 41.8% | 51.2% | -9.5% | 42.1% | 37.9% | 45.7% | 0.9597 | 1 | 0.2498 | 25.0% | 83 | 85 | 37.9% | 41.4% | 44.8% | -0.1560 | -0.0110 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35 | 7 | volatility | 672 | 48.1% | 39.7% | 8.3% | 47.8% | 44.3% | 51.8% | 0.0474 | 6 | 0.2556 | 23.9% | 96 | 96 | 41.7% | 51.0% | 51.0% | 0.0693 | 0.0561 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35 | 14 | market | 595 | 49.4% | 52.8% | -3.3% | 49.5% | 45.4% | 53.4% | 0.6677 | 1 | 0.2599 | 24.9% | 38 | 42 | 39.5% | 48.3% | 58.1% | -0.1287 | -0.0082 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35 | 14 | volatility | 665 | 45.7% | 38.0% | 7.7% | 45.5% | 42.0% | 49.5% | 0.1384 | 5 | 0.2556 | 23.6% | 47 | 47 | 35.4% | 45.3% | 55.3% | -0.0032 | -0.0297 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35 | 30 | market | 582 | 52.6% | 53.7% | -1.2% | 52.6% | 48.5% | 56.6% | 0.5404 | 1 | 0.2567 | 24.9% | 17 | 19 | 33.3% | 52.5% | 72.2% | -0.0023 | 0.0086 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35 | 30 | volatility | 649 | 43.1% | 36.2% | 6.9% | 42.9% | 39.4% | 47.0% | 0.2539 | 5 | 0.2588 | 23.1% | 21 | 21 | 19.0% | 42.9% | 59.1% | -0.0759 | -0.0947 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 3 | market | 680 | 50.3% | 50.2% | 0.1% | 50.3% | 46.5% | 54.0% | 0.4927 | 1 | 0.2523 | 25.0% | 226 | 226 | 49.8% | 50.2% | 50.9% | -0.0610 | -0.0051 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 3 | volatility | 715 | 48.1% | 47.2% | 0.9% | 48.1% | 44.5% | 51.8% | 0.3905 | 2 | 0.2519 | 24.9% | 238 | 238 | 46.4% | 46.6% | 51.3% | 0.0769 | 0.1511 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 7 | market | 677 | 46.8% | 50.3% | -3.5% | 46.9% | 43.1% | 50.6% | 0.7524 | 1 | 0.2516 | 25.0% | 94 | 96 | 41.2% | 45.4% | 55.1% | -0.0964 | -0.0139 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | 711 | 51.1% | 46.2% | 4.8% | 50.9% | 47.4% | 54.7% | 0.1652 | 4 | 0.2530 | 24.9% | 101 | 101 | 45.1% | 51.5% | 57.4% | 0.1879 | 0.2002 | 4 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 14 | market | 670 | 51.3% | 50.5% | 0.8% | 51.3% | 47.6% | 55.1% | 0.4556 | 1 | 0.2522 | 25.0% | 45 | 47 | 38.3% | 50.0% | 65.3% | -0.1029 | -0.0147 | 2 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 14 | volatility | 704 | 50.4% | 46.4% | 4.0% | 50.3% | 46.7% | 54.1% | 0.2861 | 3 | 0.2536 | 24.9% | 50 | 50 | 38.0% | 50.0% | 66.0% | 0.1630 | 0.1213 | 4 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 30 | market | 657 | 53.4% | 50.7% | 2.8% | 53.3% | 49.6% | 57.2% | 0.4001 | 3 | 0.2527 | 25.0% | 20 | 21 | 38.1% | 54.5% | 66.7% | -0.0459 | -0.0085 | 2 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35_change_5d | 30 | volatility | 688 | 49.0% | 47.1% | 1.9% | 48.9% | 45.3% | 52.7% | 0.4282 | 2 | 0.2509 | 24.9% | 22 | 22 | 21.7% | 52.2% | 65.2% | 0.1421 | 0.1329 | 3 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | market | 603 | 48.9% | 51.1% | -2.2% | 49.0% | 45.0% | 52.9% | 0.7292 | 1 | 0.2527 | 25.0% | 198 | 201 | 47.1% | 49.2% | 50.5% | -0.1110 | -0.0079 | 0 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | 676 | 48.8% | 43.6% | 5.2% | 48.7% | 45.1% | 52.6% | 0.0571 | 4 | 0.2531 | 24.6% | 225 | 225 | 46.0% | 46.7% | 53.8% | 0.1042 | 0.1733 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | market | 601 | 41.8% | 51.2% | -9.5% | 42.1% | 37.9% | 45.7% | 0.9597 | 1 | 0.2498 | 25.0% | 83 | 85 | 37.9% | 41.4% | 44.8% | -0.1789 | -0.0161 | 1 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | 672 | 48.1% | 39.7% | 8.3% | 47.8% | 44.3% | 51.8% | 0.0474 | 6 | 0.2556 | 23.9% | 96 | 96 | 41.7% | 51.0% | 51.0% | 0.1244 | 0.1071 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | market | 595 | 49.4% | 52.8% | -3.3% | 49.5% | 45.4% | 53.4% | 0.6677 | 1 | 0.2599 | 24.9% | 38 | 42 | 39.5% | 48.3% | 58.1% | -0.2000 | -0.0187 | 0 | 4 | 0 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | 665 | 45.7% | 38.0% | 7.7% | 45.5% | 42.0% | 49.5% | 0.1384 | 5 | 0.2556 | 23.6% | 47 | 47 | 35.4% | 45.3% | 55.3% | 0.0293 | -0.0056 | 3 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | market | 582 | 52.6% | 53.7% | -1.2% | 52.6% | 48.5% | 56.6% | 0.5404 | 1 | 0.2567 | 24.9% | 17 | 19 | 33.3% | 52.5% | 72.2% | -0.0975 | -0.0105 | 3 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | volatility | 649 | 43.1% | 36.2% | 6.9% | 42.9% | 39.4% | 47.0% | 0.2539 | 5 | 0.2588 | 23.1% | 21 | 21 | 19.0% | 42.9% | 59.1% | -0.0293 | -0.0582 | 2 | 4 | 2 | 4 | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 3 | volatility | 715 | 23.4% | 23.1% | 0.3% | 23.3% | 20.4% | 26.6% | 0.4595 | 1 | 0.1810 | 17.8% | 238 | 238 | 20.2% | 24.7% | 25.2% | -0.0702 | -0.0532 | 1 | 4 | 1 | 4 | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 7 | volatility | 711 | 35.9% | 33.6% | 2.2% | 35.8% | 32.4% | 39.5% | 0.3181 | 2 | 0.2377 | 22.3% | 101 | 101 | 31.7% | 35.6% | 41.2% | -0.1632 | -0.2165 | 2 | 4 | 4 | 4 | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 14 | volatility | 704 | 43.0% | 40.8% | 2.2% | 43.0% | 39.4% | 46.7% | 0.3755 | 2 | 0.2620 | 24.2% | 50 | 50 | 38.0% | 44.0% | 47.1% | -0.1883 | -0.2563 | 2 | 4 | 3 | 4 | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 30 | volatility | 688 | 44.6% | 43.5% | 1.2% | 44.6% | 40.9% | 48.4% | 0.4561 | 2 | 0.2725 | 24.6% | 22 | 22 | 34.8% | 43.5% | 65.2% | -0.3030 | -0.3282 | 1 | 4 | 2 | 4 | גבוהה | 1.0000 |

## Indicator results for every emitted arrow

| indicator | horizon | axis | arrow | n | hits | hit_rate | baseline | lift | adjusted_hit_rate | ci_low | ci_high | p_value | strength | nonoverlap_n_min | n_eff | nonoverlap_hit_rate_min | nonoverlap_hit_rate | nonoverlap_hit_rate_max | sample_quality | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | ↑ | 304 | 86 | 28.3% | 24.8% | 3.5% | 28.1% | 23.5% | 33.6% | 0.2053 | 3 | 97 | 101 | 22.6% | 29.9% | 32.7% | גבוהה | 1.0000 |
| atr_5_20_ratio | 3 | volatility | ↓ | 319 | 242 | 75.9% | 71.6% | 4.3% | 75.6% | 70.9% | 80.2% | 0.1657 | 3 | 105 | 106 | 73.1% | 76.2% | 78.3% | גבוהה | 1.0000 |
| atr_5_20_ratio | 3 | volatility | ↔ | 92 | 5 | 5.4% | 3.6% | 1.8% | 5.1% | 2.3% | 12.1% | 0.2994 | 2 | 27 | 30 | 3.7% | 5.9% | 6.5% | בינונית | 1.0000 |
| atr_5_20_ratio | 7 | volatility | ↑ | 302 | 120 | 39.7% | 36.1% | 3.6% | 39.5% | 34.4% | 45.3% | 0.3121 | 3 | 41 | 43 | 31.7% | 40.9% | 44.4% | גבוהה | 1.0000 |
| atr_5_20_ratio | 7 | volatility | ↓ | 318 | 203 | 63.8% | 57.4% | 6.5% | 63.5% | 58.4% | 68.9% | 0.1907 | 5 | 41 | 45 | 54.0% | 63.8% | 69.8% | גבוהה | 1.0000 |
| atr_5_20_ratio | 7 | volatility | ↔ | 91 | 6 | 6.6% | 6.5% | 0.1% | 6.6% | 3.1% | 13.6% | 0.4928 | 1 | 9 | 13 | 0.0% | 6.2% | 15.8% | בינונית | 1.0000 |
| atr_5_20_ratio | 14 | volatility | ↑ | 298 | 153 | 51.3% | 44.0% | 7.3% | 50.9% | 45.7% | 57.0% | 0.2500 | 5 | 16 | 21 | 42.9% | 52.1% | 62.5% | גבוהה | 1.0000 |
| atr_5_20_ratio | 14 | volatility | ↓ | 316 | 183 | 57.9% | 49.3% | 8.6% | 57.4% | 52.4% | 63.2% | 0.2093 | 6 | 19 | 22 | 47.6% | 57.1% | 73.7% | גבוהה | 1.0000 |
| atr_5_20_ratio | 14 | volatility | ↔ | 90 | 5 | 5.6% | 6.7% | -1.1% | 5.8% | 2.4% | 12.4% | 0.5438 | 1 | 2 | 6 | 0.0% | 0.0% | 22.2% | בינונית | 1.0000 |
| atr_5_20_ratio | 30 | volatility | ↑ | 297 | 164 | 55.2% | 47.4% | 7.8% | 54.7% | 49.5% | 60.8% | 0.3189 | 5 | 4 | 9 | 30.0% | 56.3% | 87.5% | גבוהה | 1.0000 |
| atr_5_20_ratio | 30 | volatility | ↓ | 306 | 170 | 55.6% | 45.9% | 9.6% | 55.0% | 50.0% | 61.0% | 0.2707 | 6 | 6 | 10 | 30.0% | 57.1% | 88.9% | גבוהה | 1.0000 |
| atr_5_20_ratio | 30 | volatility | ↔ | 85 | 9 | 10.6% | 6.7% | 3.9% | 9.8% | 5.7% | 18.9% | 0.4126 | 3 | 1 | 2 | 0.0% | 0.0% | 50.0% | בינונית | 1.0000 |
| downside_share_20 | 3 | volatility | ↑ | 162 | 40 | 24.7% | 24.8% | -0.1% | 24.7% | 18.7% | 31.9% | 0.5043 | 1 | 52 | 54 | 19.2% | 21.4% | 33.3% | בינונית | 1.0000 |
| downside_share_20 | 3 | volatility | ↓ | 421 | 302 | 71.7% | 71.6% | 0.1% | 71.7% | 67.3% | 75.8% | 0.4869 | 1 | 140 | 140 | 67.1% | 72.3% | 75.7% | גבוהה | 1.0000 |
| downside_share_20 | 3 | volatility | ↔ | 132 | 2 | 1.5% | 3.6% | -2.1% | 1.8% | 0.4% | 5.4% | 0.7739 | 1 | 43 | 44 | 0.0% | 0.0% | 4.4% | בינונית | 1.0000 |
| downside_share_20 | 7 | volatility | ↑ | 162 | 54 | 33.3% | 36.1% | -2.8% | 33.6% | 26.5% | 40.9% | 0.6106 | 1 | 19 | 23 | 15.8% | 37.0% | 40.0% | בינונית | 1.0000 |
| downside_share_20 | 7 | volatility | ↓ | 421 | 229 | 54.4% | 57.4% | -3.0% | 54.5% | 49.6% | 59.1% | 0.6802 | 1 | 58 | 60 | 47.5% | 55.9% | 58.5% | גבוהה | 1.0000 |
| downside_share_20 | 7 | volatility | ↔ | 128 | 7 | 5.5% | 6.5% | -1.0% | 5.6% | 2.7% | 10.9% | 0.5685 | 1 | 12 | 18 | 0.0% | 5.0% | 9.5% | בינונית | 1.0000 |
| downside_share_20 | 14 | volatility | ↑ | 162 | 57 | 35.2% | 44.0% | -8.8% | 36.2% | 28.3% | 42.8% | 0.7228 | 1 | 9 | 11 | 11.1% | 34.5% | 54.5% | בינונית | 1.0000 |
| downside_share_20 | 14 | volatility | ↓ | 417 | 178 | 42.7% | 49.3% | -6.6% | 43.0% | 38.0% | 47.5% | 0.7616 | 1 | 28 | 29 | 34.5% | 42.6% | 48.3% | גבוהה | 1.0000 |
| downside_share_20 | 14 | volatility | ↔ | 125 | 4 | 3.2% | 6.7% | -3.5% | 3.7% | 1.3% | 7.9% | 0.6532 | 1 | 6 | 8 | 0.0% | 0.0% | 10.0% | בינונית | 1.0000 |
| downside_share_20 | 30 | volatility | ↑ | 149 | 48 | 32.2% | 47.4% | -15.2% | 34.0% | 25.2% | 40.1% | 0.7283 | 1 | 3 | 4 | 0.0% | 25.0% | 60.0% | בינונית | 1.0000 |
| downside_share_20 | 30 | volatility | ↓ | 416 | 169 | 40.6% | 45.9% | -5.3% | 40.9% | 36.0% | 45.4% | 0.6495 | 1 | 11 | 13 | 21.4% | 42.3% | 53.8% | גבוהה | 1.0000 |
| downside_share_20 | 30 | volatility | ↔ | 123 | 6 | 4.9% | 6.7% | -1.8% | 5.1% | 2.3% | 10.2% | 0.5576 | 1 | 1 | 4 | 0.0% | 0.0% | 50.0% | בינונית | 1.0000 |
| expected_move_3d_points | 3 | volatility | ↑ | 210 | 71 | 33.8% | 24.8% | 9.1% | 33.0% | 27.8% | 40.4% | 0.0396 | 6 | 68 | 70 | 30.4% | 32.4% | 38.4% | גבוהה | 1.0000 |
| expected_move_3d_points | 3 | volatility | ↓ | 212 | 172 | 81.1% | 71.6% | 9.5% | 80.3% | 75.3% | 85.8% | 0.0386 | 6 | 69 | 70 | 79.5% | 80.0% | 84.1% | גבוהה | 1.0000 |
| expected_move_3d_points | 3 | volatility | ↔ | 293 | 11 | 3.8% | 3.6% | 0.1% | 3.7% | 2.1% | 6.6% | 0.4753 | 1 | 93 | 97 | 2.0% | 4.3% | 5.0% | גבוהה | 1.0000 |
| expected_move_3d_points | 7 | volatility | ↑ | 210 | 102 | 48.6% | 36.1% | 12.4% | 47.5% | 41.9% | 55.3% | 0.0783 | 8 | 28 | 30 | 43.8% | 48.3% | 53.3% | גבוהה | 1.0000 |
| expected_move_3d_points | 7 | volatility | ↓ | 212 | 152 | 71.7% | 57.4% | 14.3% | 70.5% | 65.3% | 77.3% | 0.0564 | 9 | 25 | 30 | 64.5% | 72.0% | 80.0% | גבוהה | 1.0000 |
| expected_move_3d_points | 7 | volatility | ↔ | 289 | 17 | 5.9% | 6.5% | -0.6% | 5.9% | 3.7% | 9.2% | 0.5608 | 1 | 36 | 41 | 2.4% | 5.6% | 10.3% | גבוהה | 1.0000 |
| expected_move_3d_points | 14 | volatility | ↑ | 207 | 128 | 61.8% | 44.0% | 17.8% | 60.3% | 55.1% | 68.2% | 0.0898 | 10 | 11 | 14 | 43.8% | 64.1% | 81.8% | גבוהה | 1.0000 |
| expected_move_3d_points | 14 | volatility | ↓ | 212 | 140 | 66.0% | 49.3% | 16.7% | 64.6% | 59.4% | 72.1% | 0.0972 | 10 | 12 | 15 | 50.0% | 66.7% | 76.5% | גבוהה | 1.0000 |
| expected_move_3d_points | 14 | volatility | ↔ | 285 | 24 | 8.4% | 6.7% | 1.7% | 8.3% | 5.7% | 12.2% | 0.3773 | 2 | 17 | 20 | 0.0% | 7.5% | 19.0% | גבוהה | 1.0000 |
| expected_move_3d_points | 30 | volatility | ↑ | 195 | 130 | 66.7% | 47.4% | 19.3% | 64.9% | 59.8% | 72.9% | 0.1721 | 10 | 4 | 6 | 25.0% | 66.7% | 100.0% | בינונית | 1.0000 |
| expected_move_3d_points | 30 | volatility | ↓ | 212 | 135 | 63.7% | 45.9% | 17.7% | 62.1% | 57.0% | 69.9% | 0.1730 | 10 | 3 | 7 | 16.7% | 63.6% | 100.0% | גבוהה | 1.0000 |
| expected_move_3d_points | 30 | volatility | ↔ | 281 | 18 | 6.4% | 6.7% | -0.3% | 6.4% | 4.1% | 9.9% | 0.5134 | 1 | 4 | 9 | 0.0% | 0.0% | 40.0% | גבוהה | 1.0000 |
| forecast_rv_3d | 3 | volatility | ↑ | 210 | 71 | 33.8% | 24.8% | 9.1% | 33.0% | 27.8% | 40.4% | 0.0396 | 6 | 68 | 70 | 30.4% | 32.4% | 38.4% | גבוהה | 1.0000 |
| forecast_rv_3d | 3 | volatility | ↓ | 212 | 172 | 81.1% | 71.6% | 9.5% | 80.3% | 75.3% | 85.8% | 0.0386 | 6 | 69 | 70 | 79.5% | 80.0% | 84.1% | גבוהה | 1.0000 |
| forecast_rv_3d | 3 | volatility | ↔ | 293 | 11 | 3.8% | 3.6% | 0.1% | 3.7% | 2.1% | 6.6% | 0.4753 | 1 | 93 | 97 | 2.0% | 4.3% | 5.0% | גבוהה | 1.0000 |
| forecast_rv_3d | 7 | volatility | ↑ | 210 | 102 | 48.6% | 36.1% | 12.4% | 47.5% | 41.9% | 55.3% | 0.0783 | 8 | 28 | 30 | 43.8% | 48.3% | 53.3% | גבוהה | 1.0000 |
| forecast_rv_3d | 7 | volatility | ↓ | 212 | 152 | 71.7% | 57.4% | 14.3% | 70.5% | 65.3% | 77.3% | 0.0564 | 9 | 25 | 30 | 64.5% | 72.0% | 80.0% | גבוהה | 1.0000 |
| forecast_rv_3d | 7 | volatility | ↔ | 289 | 17 | 5.9% | 6.5% | -0.6% | 5.9% | 3.7% | 9.2% | 0.5608 | 1 | 36 | 41 | 2.4% | 5.6% | 10.3% | גבוהה | 1.0000 |
| forecast_rv_3d | 14 | volatility | ↑ | 207 | 128 | 61.8% | 44.0% | 17.8% | 60.3% | 55.1% | 68.2% | 0.0898 | 10 | 11 | 14 | 43.8% | 64.1% | 81.8% | גבוהה | 1.0000 |
| forecast_rv_3d | 14 | volatility | ↓ | 212 | 140 | 66.0% | 49.3% | 16.7% | 64.6% | 59.4% | 72.1% | 0.0972 | 10 | 12 | 15 | 50.0% | 66.7% | 76.5% | גבוהה | 1.0000 |
| forecast_rv_3d | 14 | volatility | ↔ | 285 | 24 | 8.4% | 6.7% | 1.7% | 8.3% | 5.7% | 12.2% | 0.3773 | 2 | 17 | 20 | 0.0% | 7.5% | 19.0% | גבוהה | 1.0000 |
| forecast_rv_3d | 30 | volatility | ↑ | 195 | 130 | 66.7% | 47.4% | 19.3% | 64.9% | 59.8% | 72.9% | 0.1721 | 10 | 4 | 6 | 25.0% | 66.7% | 100.0% | בינונית | 1.0000 |
| forecast_rv_3d | 30 | volatility | ↓ | 212 | 135 | 63.7% | 45.9% | 17.7% | 62.1% | 57.0% | 69.9% | 0.1730 | 10 | 3 | 7 | 16.7% | 63.6% | 100.0% | גבוהה | 1.0000 |
| forecast_rv_3d | 30 | volatility | ↔ | 281 | 18 | 6.4% | 6.7% | -0.3% | 6.4% | 4.1% | 9.9% | 0.5134 | 1 | 4 | 9 | 0.0% | 0.0% | 40.0% | גבוהה | 1.0000 |
| gap_share_20 | 3 | volatility | ↑ | 231 | 53 | 22.9% | 24.8% | -1.8% | 23.1% | 18.0% | 28.8% | 0.6437 | 1 | 76 | 77 | 21.5% | 22.4% | 25.0% | גבוהה | 1.0000 |
| gap_share_20 | 3 | volatility | ↓ | 250 | 179 | 71.6% | 71.6% | -0.0% | 71.6% | 65.7% | 76.8% | 0.5007 | 1 | 83 | 83 | 66.7% | 71.1% | 77.1% | גבוהה | 1.0000 |
| gap_share_20 | 3 | volatility | ↔ | 234 | 12 | 5.1% | 3.6% | 1.5% | 5.0% | 3.0% | 8.7% | 0.2408 | 2 | 76 | 78 | 2.5% | 3.8% | 9.2% | גבוהה | 1.0000 |
| gap_share_20 | 7 | volatility | ↑ | 231 | 77 | 33.3% | 36.1% | -2.8% | 33.6% | 27.6% | 39.6% | 0.6317 | 1 | 29 | 33 | 24.2% | 33.3% | 43.8% | גבוהה | 1.0000 |
| gap_share_20 | 7 | volatility | ↓ | 246 | 136 | 55.3% | 57.4% | -2.1% | 55.4% | 49.0% | 61.4% | 0.5992 | 1 | 32 | 35 | 50.0% | 55.9% | 60.5% | גבוהה | 1.0000 |
| gap_share_20 | 7 | volatility | ↔ | 234 | 26 | 11.1% | 6.5% | 4.6% | 10.7% | 7.7% | 15.8% | 0.1392 | 4 | 30 | 33 | 5.7% | 12.1% | 13.5% | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | ↑ | 230 | 75 | 32.6% | 44.0% | -11.4% | 33.5% | 26.9% | 38.9% | 0.8214 | 1 | 13 | 16 | 22.2% | 33.3% | 47.1% | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | ↓ | 244 | 104 | 42.6% | 49.3% | -6.7% | 43.1% | 36.6% | 48.9% | 0.7088 | 1 | 15 | 17 | 17.6% | 44.1% | 55.0% | גבוהה | 1.0000 |
| gap_share_20 | 14 | volatility | ↔ | 230 | 18 | 7.8% | 6.7% | 1.1% | 7.7% | 5.0% | 12.0% | 0.4269 | 2 | 14 | 16 | 0.0% | 6.2% | 17.6% | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | ↑ | 229 | 70 | 30.6% | 47.4% | -16.8% | 31.9% | 25.0% | 36.8% | 0.8135 | 1 | 5 | 7 | 14.3% | 31.0% | 45.5% | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | ↓ | 244 | 81 | 33.2% | 45.9% | -12.7% | 34.2% | 27.6% | 39.3% | 0.7651 | 1 | 4 | 8 | 0.0% | 33.3% | 57.1% | גבוהה | 1.0000 |
| gap_share_20 | 30 | volatility | ↔ | 215 | 9 | 4.2% | 6.7% | -2.5% | 4.4% | 2.2% | 7.8% | 0.6044 | 1 | 3 | 7 | 0.0% | 0.0% | 16.7% | גבוהה | 1.0000 |
| har_rv_3d | 3 | volatility | ↑ | 190 | 64 | 33.7% | 24.3% | 9.3% | 32.8% | 27.3% | 40.7% | 0.0421 | 6 | 60 | 63 | 30.0% | 30.2% | 40.3% | בינונית | 1.0000 |
| har_rv_3d | 3 | volatility | ↓ | 167 | 138 | 82.6% | 72.1% | 10.6% | 81.5% | 76.2% | 87.6% | 0.0402 | 7 | 54 | 55 | 80.7% | 82.1% | 85.2% | בינונית | 1.0000 |
| har_rv_3d | 3 | volatility | ↔ | 255 | 11 | 4.3% | 3.6% | 0.7% | 4.3% | 2.4% | 7.6% | 0.3609 | 1 | 81 | 85 | 2.3% | 4.9% | 5.7% | גבוהה | 1.0000 |
| har_rv_3d | 7 | volatility | ↑ | 190 | 94 | 49.5% | 36.3% | 13.1% | 48.2% | 42.4% | 56.5% | 0.0781 | 8 | 25 | 27 | 42.3% | 48.3% | 56.0% | בינונית | 1.0000 |
| har_rv_3d | 7 | volatility | ↓ | 167 | 119 | 71.3% | 57.6% | 13.7% | 69.8% | 64.0% | 77.6% | 0.0920 | 8 | 20 | 23 | 62.5% | 73.1% | 80.0% | בינונית | 1.0000 |
| har_rv_3d | 7 | volatility | ↔ | 251 | 14 | 5.6% | 6.1% | -0.5% | 5.6% | 3.4% | 9.1% | 0.5500 | 1 | 31 | 35 | 2.8% | 5.7% | 8.6% | גבוהה | 1.0000 |
| har_rv_3d | 14 | volatility | ↑ | 187 | 117 | 62.6% | 47.1% | 15.5% | 61.1% | 55.4% | 69.2% | 0.1318 | 9 | 10 | 13 | 40.0% | 65.5% | 80.0% | בינונית | 1.0000 |
| har_rv_3d | 14 | volatility | ↓ | 167 | 101 | 60.5% | 45.9% | 14.6% | 58.9% | 52.9% | 67.6% | 0.1663 | 9 | 9 | 11 | 45.5% | 60.0% | 73.3% | בינונית | 1.0000 |
| har_rv_3d | 14 | volatility | ↔ | 247 | 23 | 9.3% | 7.0% | 2.3% | 9.1% | 6.3% | 13.6% | 0.3536 | 2 | 14 | 17 | 0.0% | 6.7% | 23.5% | גבוהה | 1.0000 |
| har_rv_3d | 30 | volatility | ↑ | 175 | 120 | 68.6% | 52.1% | 16.4% | 66.9% | 61.4% | 75.0% | 0.2310 | 10 | 3 | 5 | 33.3% | 66.7% | 100.0% | בינונית | 1.0000 |
| har_rv_3d | 30 | volatility | ↓ | 167 | 93 | 55.7% | 40.9% | 14.8% | 54.1% | 48.1% | 63.0% | 0.2499 | 9 | 1 | 5 | 0.0% | 56.3% | 100.0% | בינונית | 1.0000 |
| har_rv_3d | 30 | volatility | ↔ | 243 | 16 | 6.6% | 7.0% | -0.4% | 6.6% | 4.1% | 10.4% | 0.5187 | 1 | 3 | 8 | 0.0% | 0.0% | 37.5% | גבוהה | 1.0000 |
| local_global_stress_spread | 3 | volatility | ↑ | 282 | 88 | 31.2% | 24.5% | 6.7% | 30.8% | 26.1% | 36.8% | 0.0657 | 5 | 92 | 94 | 26.0% | 31.9% | 35.9% | גבוהה | 1.0000 |
| local_global_stress_spread | 3 | volatility | ↓ | 263 | 191 | 72.6% | 71.9% | 0.7% | 72.6% | 66.9% | 77.7% | 0.4416 | 1 | 87 | 87 | 71.6% | 72.7% | 73.6% | גבוהה | 1.0000 |
| local_global_stress_spread | 3 | volatility | ↔ | 71 | 0 | 0.0% | 3.6% | -3.6% | 0.8% | 0.0% | 5.1% | 0.8220 | 1 | 21 | 23 | 0.0% | 0.0% | 0.0% | נמוכה | 1.0000 |
| local_global_stress_spread | 7 | volatility | ↑ | 279 | 120 | 43.0% | 36.1% | 6.9% | 42.5% | 37.3% | 48.9% | 0.1848 | 5 | 37 | 39 | 37.5% | 44.2% | 48.6% | גבוהה | 1.0000 |
| local_global_stress_spread | 7 | volatility | ↓ | 263 | 162 | 61.6% | 57.7% | 3.9% | 61.3% | 55.6% | 67.3% | 0.3148 | 3 | 35 | 37 | 54.1% | 65.0% | 66.7% | גבוהה | 1.0000 |
| local_global_stress_spread | 7 | volatility | ↔ | 70 | 3 | 4.3% | 6.2% | -1.9% | 4.7% | 1.5% | 11.9% | 0.5995 | 1 | 8 | 10 | 0.0% | 0.0% | 12.5% | נמוכה | 1.0000 |
| local_global_stress_spread | 14 | volatility | ↑ | 275 | 134 | 48.7% | 46.8% | 2.0% | 48.6% | 42.9% | 54.6% | 0.4324 | 2 | 17 | 19 | 36.8% | 48.8% | 57.9% | גבוהה | 1.0000 |
| local_global_stress_spread | 14 | volatility | ↓ | 261 | 119 | 45.6% | 46.3% | -0.7% | 45.6% | 39.7% | 51.7% | 0.5233 | 1 | 16 | 18 | 28.6% | 50.0% | 57.9% | גבוהה | 1.0000 |
| local_global_stress_spread | 14 | volatility | ↔ | 69 | 3 | 4.3% | 6.9% | -2.6% | 4.9% | 1.5% | 12.0% | 0.5809 | 1 | 3 | 4 | 0.0% | 0.0% | 33.3% | נמוכה | 1.0000 |
| local_global_stress_spread | 30 | volatility | ↑ | 259 | 136 | 52.5% | 51.8% | 0.7% | 52.5% | 46.4% | 58.5% | 0.4836 | 1 | 5 | 8 | 16.7% | 50.0% | 80.0% | גבוהה | 1.0000 |
| local_global_stress_spread | 30 | volatility | ↓ | 261 | 105 | 40.2% | 41.3% | -1.0% | 40.3% | 34.5% | 46.3% | 0.5235 | 1 | 6 | 8 | 11.1% | 42.2% | 75.0% | גבוהה | 1.0000 |
| local_global_stress_spread | 30 | volatility | ↔ | 69 | 6 | 8.7% | 7.0% | 1.7% | 8.3% | 4.0% | 17.7% | 0.4616 | 2 | 1 | 2 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| matched_vrp_3d | 3 | volatility | ↑ | 612 | 149 | 24.3% | 24.3% | 0.0% | 24.3% | 21.1% | 27.9% | 0.5000 | 1 | 204 | 204 | 21.6% | 25.5% | 26.0% | גבוהה | 1.0000 |
| matched_vrp_3d | 7 | volatility | ↑ | 608 | 221 | 36.3% | 36.3% | 0.0% | 36.3% | 32.6% | 40.2% | 0.5000 | 1 | 86 | 86 | 34.5% | 36.8% | 37.9% | גבוהה | 1.0000 |
| matched_vrp_3d | 14 | volatility | ↑ | 601 | 283 | 47.1% | 47.1% | 0.0% | 47.1% | 43.1% | 51.1% | 0.5000 | 1 | 42 | 42 | 41.9% | 47.7% | 51.2% | גבוהה | 1.0000 |
| matched_vrp_3d | 30 | volatility | ↑ | 585 | 305 | 52.1% | 52.1% | 0.0% | 52.1% | 48.1% | 56.2% | 0.5000 | 1 | 19 | 19 | 35.0% | 53.8% | 68.4% | גבוהה | 1.0000 |
| range_position_20 | 3 | volatility | ↔ | 715 | 26 | 3.6% | 3.6% | 0.0% | 3.6% | 2.5% | 5.3% | 0.5000 | 1 | 238 | 238 | 2.1% | 3.8% | 5.0% | גבוהה | 1.0000 |
| range_position_20 | 7 | volatility | ↔ | 711 | 46 | 6.5% | 6.5% | 0.0% | 6.5% | 4.9% | 8.5% | 0.5000 | 1 | 101 | 101 | 4.0% | 6.9% | 8.8% | גבוהה | 1.0000 |
| range_position_20 | 14 | volatility | ↔ | 704 | 47 | 6.7% | 6.7% | 0.0% | 6.7% | 5.1% | 8.8% | 0.5000 | 1 | 50 | 50 | 2.0% | 6.0% | 12.0% | גבוהה | 1.0000 |
| range_position_20 | 30 | volatility | ↔ | 688 | 46 | 6.7% | 6.7% | 0.0% | 6.7% | 5.0% | 8.8% | 0.5000 | 1 | 22 | 22 | 0.0% | 4.3% | 18.2% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 3 | market | ↑ | 113 | 79 | 69.9% | 61.6% | 8.3% | 68.7% | 60.9% | 77.6% | 0.1487 | 5 | 36 | 37 | 62.2% | 67.5% | 80.6% | בינונית | 1.0000 |
| reversal_5_vol_scaled | 3 | market | ↓ | 254 | 107 | 42.1% | 38.4% | 3.7% | 41.9% | 36.2% | 48.3% | 0.2425 | 3 | 81 | 84 | 38.3% | 43.7% | 44.2% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 3 | volatility | ↔ | 715 | 26 | 3.6% | 3.6% | 0.0% | 3.6% | 2.5% | 5.3% | 0.5000 | 1 | 238 | 238 | 2.1% | 3.8% | 5.0% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 7 | market | ↑ | 111 | 86 | 77.5% | 61.1% | 16.4% | 75.0% | 68.9% | 84.3% | 0.0966 | 9 | 12 | 15 | 66.7% | 75.0% | 94.1% | בינונית | 1.0000 |
| reversal_5_vol_scaled | 7 | market | ↓ | 254 | 117 | 46.1% | 38.9% | 7.2% | 45.5% | 40.0% | 52.2% | 0.1891 | 5 | 31 | 36 | 35.3% | 42.9% | 56.4% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 7 | volatility | ↔ | 711 | 46 | 6.5% | 6.5% | 0.0% | 6.5% | 4.9% | 8.5% | 0.5000 | 1 | 101 | 101 | 4.0% | 6.9% | 8.8% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 14 | market | ↑ | 110 | 84 | 76.4% | 72.3% | 4.1% | 75.7% | 67.6% | 83.3% | 0.4051 | 3 | 4 | 7 | 57.1% | 71.4% | 91.7% | בינונית | 1.0000 |
| reversal_5_vol_scaled | 14 | market | ↓ | 251 | 74 | 29.5% | 27.7% | 1.8% | 29.4% | 24.2% | 35.4% | 0.4348 | 2 | 9 | 17 | 13.0% | 33.3% | 43.8% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 14 | volatility | ↔ | 704 | 47 | 6.7% | 6.7% | 0.0% | 6.7% | 5.1% | 8.8% | 0.5000 | 1 | 50 | 50 | 2.0% | 6.0% | 12.0% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 30 | market | ↑ | 105 | 82 | 78.1% | 76.6% | 1.5% | 77.9% | 69.3% | 84.9% | 0.4762 | 2 | 1 | 3 | 0.0% | 77.5% | 100.0% | בינונית | 1.0000 |
| reversal_5_vol_scaled | 30 | market | ↓ | 246 | 59 | 24.0% | 23.4% | 0.6% | 23.9% | 19.1% | 29.7% | 0.4834 | 1 | 3 | 8 | 0.0% | 23.6% | 55.6% | גבוהה | 1.0000 |
| reversal_5_vol_scaled | 30 | volatility | ↔ | 688 | 46 | 6.7% | 6.7% | 0.0% | 6.7% | 5.0% | 8.8% | 0.5000 | 1 | 22 | 22 | 0.0% | 4.3% | 18.2% | גבוהה | 1.0000 |
| rs_range_5_20 | 3 | volatility | ↑ | 255 | 75 | 29.4% | 24.8% | 4.7% | 29.1% | 24.2% | 35.3% | 0.1599 | 4 | 80 | 85 | 26.2% | 28.7% | 33.0% | גבוהה | 1.0000 |
| rs_range_5_20 | 3 | volatility | ↓ | 324 | 247 | 76.2% | 71.6% | 4.6% | 76.0% | 71.3% | 80.5% | 0.1432 | 4 | 106 | 108 | 74.5% | 75.5% | 78.7% | גבוהה | 1.0000 |
| rs_range_5_20 | 3 | volatility | ↔ | 136 | 6 | 4.4% | 3.6% | 0.8% | 4.3% | 2.0% | 9.3% | 0.3906 | 1 | 42 | 45 | 3.8% | 4.8% | 4.8% | בינונית | 1.0000 |
| rs_range_5_20 | 7 | volatility | ↑ | 255 | 111 | 43.5% | 36.1% | 7.4% | 43.0% | 37.6% | 49.7% | 0.1782 | 5 | 33 | 36 | 33.3% | 43.9% | 48.6% | גבוהה | 1.0000 |
| rs_range_5_20 | 7 | volatility | ↓ | 323 | 214 | 66.3% | 57.4% | 8.9% | 65.7% | 60.9% | 71.2% | 0.1119 | 6 | 43 | 46 | 56.2% | 68.2% | 70.8% | גבוהה | 1.0000 |
| rs_range_5_20 | 7 | volatility | ↔ | 133 | 9 | 6.8% | 6.5% | 0.3% | 6.7% | 3.6% | 12.4% | 0.4790 | 1 | 16 | 19 | 0.0% | 5.9% | 14.3% | בינונית | 1.0000 |
| rs_range_5_20 | 14 | volatility | ↑ | 252 | 124 | 49.2% | 44.0% | 5.2% | 48.8% | 43.1% | 55.3% | 0.3292 | 4 | 13 | 18 | 35.0% | 51.5% | 58.8% | גבוהה | 1.0000 |
| rs_range_5_20 | 14 | volatility | ↓ | 322 | 188 | 58.4% | 49.3% | 9.1% | 57.9% | 52.9% | 63.6% | 0.1915 | 6 | 19 | 23 | 47.6% | 58.7% | 71.4% | גבוהה | 1.0000 |
| rs_range_5_20 | 14 | volatility | ↔ | 130 | 13 | 10.0% | 6.7% | 3.3% | 9.6% | 5.9% | 16.4% | 0.3448 | 3 | 6 | 9 | 0.0% | 11.1% | 22.2% | בינונית | 1.0000 |
| rs_range_5_20 | 30 | volatility | ↑ | 252 | 145 | 57.5% | 47.4% | 10.2% | 56.8% | 51.4% | 63.5% | 0.2825 | 7 | 4 | 8 | 33.3% | 54.5% | 100.0% | גבוהה | 1.0000 |
| rs_range_5_20 | 30 | volatility | ↓ | 313 | 180 | 57.5% | 45.9% | 11.6% | 56.8% | 52.0% | 62.9% | 0.2313 | 8 | 5 | 10 | 27.3% | 61.3% | 77.8% | גבוהה | 1.0000 |
| rs_range_5_20 | 30 | volatility | ↔ | 123 | 10 | 8.1% | 6.7% | 1.4% | 7.9% | 4.5% | 14.3% | 0.4540 | 2 | 1 | 4 | 0.0% | 0.0% | 100.0% | בינונית | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↑ | 237 | 42 | 17.7% | 24.1% | -6.4% | 18.2% | 13.4% | 23.1% | 0.9090 | 1 | 78 | 79 | 14.1% | 17.3% | 21.8% | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↓ | 381 | 265 | 69.6% | 72.3% | -2.7% | 69.7% | 64.8% | 74.0% | 0.7551 | 1 | 126 | 127 | 65.1% | 70.6% | 72.9% | גבוהה | 1.0000 |
| rv_20_60_ratio | 3 | volatility | ↔ | 57 | 2 | 3.5% | 3.6% | -0.0% | 3.5% | 1.0% | 11.9% | 0.5044 | 1 | 18 | 19 | 0.0% | 4.8% | 5.6% | נמוכה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↑ | 237 | 57 | 24.1% | 35.0% | -11.0% | 24.9% | 19.1% | 29.9% | 0.9068 | 1 | 31 | 33 | 18.8% | 22.9% | 31.4% | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↓ | 377 | 191 | 50.7% | 58.6% | -7.9% | 51.1% | 45.6% | 55.7% | 0.8787 | 1 | 50 | 53 | 41.4% | 50.9% | 55.8% | גבוהה | 1.0000 |
| rv_20_60_ratio | 7 | volatility | ↔ | 57 | 3 | 5.3% | 6.4% | -1.1% | 5.6% | 1.8% | 14.4% | 0.5526 | 1 | 3 | 8 | 0.0% | 0.0% | 20.0% | נמוכה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↑ | 237 | 65 | 27.4% | 43.7% | -16.2% | 28.7% | 22.1% | 33.4% | 0.9050 | 1 | 15 | 16 | 12.5% | 27.2% | 41.2% | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↓ | 370 | 143 | 38.6% | 49.2% | -10.6% | 39.2% | 33.8% | 43.7% | 0.8601 | 1 | 23 | 26 | 29.2% | 38.8% | 48.1% | גבוהה | 1.0000 |
| rv_20_60_ratio | 14 | volatility | ↔ | 57 | 2 | 3.5% | 7.1% | -3.6% | 4.4% | 1.0% | 11.9% | 0.6096 | 1 | 2 | 4 | 0.0% | 0.0% | 25.0% | נמוכה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↑ | 237 | 58 | 24.5% | 47.2% | -22.7% | 26.2% | 19.4% | 30.3% | 0.8860 | 1 | 4 | 7 | 11.1% | 25.0% | 60.0% | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↓ | 354 | 106 | 29.9% | 45.7% | -15.7% | 30.8% | 25.4% | 34.9% | 0.8526 | 1 | 9 | 11 | 7.7% | 31.7% | 50.0% | גבוהה | 1.0000 |
| rv_20_60_ratio | 30 | volatility | ↔ | 57 | 3 | 5.3% | 7.1% | -1.8% | 5.7% | 1.8% | 14.4% | 0.5285 | 1 | 1 | 1 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| rv_acceleration | 3 | volatility | ↑ | 208 | 56 | 26.9% | 24.8% | 2.2% | 26.7% | 21.4% | 33.3% | 0.3383 | 2 | 67 | 69 | 23.9% | 27.9% | 28.8% | גבוהה | 1.0000 |
| rv_acceleration | 3 | volatility | ↓ | 461 | 335 | 72.7% | 71.6% | 1.1% | 72.6% | 68.4% | 76.5% | 0.3856 | 2 | 152 | 153 | 71.1% | 73.0% | 73.9% | גבוהה | 1.0000 |
| rv_acceleration | 3 | volatility | ↔ | 46 | 2 | 4.3% | 3.6% | 0.7% | 4.1% | 1.2% | 14.5% | 0.4415 | 1 | 14 | 15 | 0.0% | 5.6% | 7.1% | נמוכה | 1.0000 |
| rv_acceleration | 7 | volatility | ↑ | 205 | 75 | 36.6% | 36.1% | 0.4% | 36.5% | 30.3% | 43.4% | 0.4804 | 1 | 27 | 29 | 29.0% | 37.0% | 43.3% | גבוהה | 1.0000 |
| rv_acceleration | 7 | volatility | ↓ | 460 | 263 | 57.2% | 57.4% | -0.2% | 57.2% | 52.6% | 61.6% | 0.5137 | 1 | 63 | 65 | 50.0% | 56.9% | 61.8% | גבוהה | 1.0000 |
| rv_acceleration | 7 | volatility | ↔ | 46 | 1 | 2.2% | 6.5% | -4.3% | 3.5% | 0.4% | 11.3% | 0.6656 | 1 | 3 | 6 | 0.0% | 0.0% | 14.3% | נמוכה | 1.0000 |
| rv_acceleration | 14 | volatility | ↑ | 201 | 98 | 48.8% | 44.0% | 4.7% | 48.3% | 41.9% | 55.6% | 0.3610 | 4 | 8 | 14 | 30.0% | 48.5% | 75.0% | גבוהה | 1.0000 |
| rv_acceleration | 14 | volatility | ↓ | 458 | 240 | 52.4% | 49.3% | 3.1% | 52.3% | 47.8% | 56.9% | 0.3624 | 3 | 26 | 32 | 39.4% | 53.5% | 61.5% | גבוהה | 1.0000 |
| rv_acceleration | 14 | volatility | ↔ | 45 | 5 | 11.1% | 6.7% | 4.4% | 9.7% | 4.8% | 23.5% | 0.3791 | 2 | 1 | 3 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| rv_acceleration | 30 | volatility | ↑ | 197 | 108 | 54.8% | 47.4% | 7.4% | 54.1% | 47.8% | 61.6% | 0.3576 | 5 | 3 | 6 | 0.0% | 52.3% | 100.0% | בינונית | 1.0000 |
| rv_acceleration | 30 | volatility | ↓ | 450 | 220 | 48.9% | 45.9% | 3.0% | 48.8% | 44.3% | 53.5% | 0.4091 | 3 | 11 | 15 | 30.8% | 50.0% | 66.7% | גבוהה | 1.0000 |
| rv_acceleration | 30 | volatility | ↔ | 41 | 3 | 7.3% | 6.7% | 0.6% | 7.1% | 2.5% | 19.4% | 0.4899 | 1 | 1 | 1 | 0.0% | 0.0% | 100.0% | נמוכה | 1.0000 |
| trend_efficiency_20 | 3 | volatility | ↑ | 461 | 117 | 25.4% | 24.8% | 0.6% | 25.4% | 21.6% | 29.5% | 0.4290 | 1 | 152 | 153 | 22.6% | 26.3% | 27.3% | גבוהה | 1.0000 |
| trend_efficiency_20 | 3 | volatility | ↓ | 133 | 95 | 71.4% | 71.6% | -0.2% | 71.5% | 63.2% | 78.4% | 0.5106 | 1 | 41 | 44 | 67.3% | 70.7% | 76.7% | בינונית | 1.0000 |
| trend_efficiency_20 | 3 | volatility | ↔ | 121 | 5 | 4.1% | 3.6% | 0.5% | 4.1% | 1.8% | 9.3% | 0.4335 | 1 | 34 | 40 | 0.0% | 4.3% | 8.8% | בינונית | 1.0000 |
| trend_efficiency_20 | 7 | volatility | ↑ | 457 | 161 | 35.2% | 36.1% | -0.9% | 35.3% | 31.0% | 39.7% | 0.5611 | 1 | 60 | 65 | 30.9% | 35.9% | 37.3% | גבוהה | 1.0000 |
| trend_efficiency_20 | 7 | volatility | ↓ | 133 | 70 | 52.6% | 57.4% | -4.8% | 53.3% | 44.2% | 60.9% | 0.6624 | 1 | 15 | 19 | 40.0% | 54.2% | 63.2% | בינונית | 1.0000 |
| trend_efficiency_20 | 7 | volatility | ↔ | 121 | 13 | 10.7% | 6.5% | 4.3% | 10.1% | 6.4% | 17.5% | 0.2369 | 3 | 14 | 17 | 0.0% | 11.1% | 22.2% | בינונית | 1.0000 |
| trend_efficiency_20 | 14 | volatility | ↑ | 450 | 184 | 40.9% | 44.0% | -3.1% | 41.0% | 36.4% | 45.5% | 0.6400 | 1 | 29 | 32 | 34.3% | 41.2% | 50.0% | גבוהה | 1.0000 |
| trend_efficiency_20 | 14 | volatility | ↓ | 133 | 48 | 36.1% | 49.3% | -13.2% | 37.8% | 28.4% | 44.5% | 0.7858 | 1 | 7 | 9 | 12.5% | 33.2% | 63.6% | בינונית | 1.0000 |
| trend_efficiency_20 | 14 | volatility | ↔ | 121 | 7 | 5.8% | 6.7% | -0.9% | 5.9% | 2.8% | 11.5% | 0.5402 | 1 | 6 | 8 | 0.0% | 0.0% | 25.0% | בינונית | 1.0000 |
| trend_efficiency_20 | 30 | volatility | ↑ | 439 | 197 | 44.9% | 47.4% | -2.5% | 45.0% | 40.3% | 49.6% | 0.5746 | 1 | 12 | 14 | 26.7% | 46.2% | 61.5% | גבוהה | 1.0000 |
| trend_efficiency_20 | 30 | volatility | ↓ | 132 | 48 | 36.4% | 45.9% | -9.6% | 37.6% | 28.7% | 44.8% | 0.6495 | 1 | 3 | 4 | 0.0% | 36.7% | 66.7% | בינונית | 1.0000 |
| trend_efficiency_20 | 30 | volatility | ↔ | 117 | 16 | 13.7% | 6.7% | 7.0% | 12.7% | 8.6% | 21.1% | 0.3140 | 5 | 1 | 3 | 0.0% | 0.0% | 66.7% | בינונית | 1.0000 |
| usdils_change_5d | 3 | market | ↑ | 327 | 193 | 59.0% | 58.4% | 0.6% | 59.0% | 53.6% | 64.2% | 0.4487 | 1 | 100 | 109 | 54.0% | 61.2% | 61.3% | גבוהה | 1.0000 |
| usdils_change_5d | 3 | market | ↓ | 303 | 128 | 42.2% | 41.6% | 0.7% | 42.2% | 36.8% | 47.9% | 0.4467 | 1 | 95 | 101 | 37.3% | 42.1% | 48.0% | גבוהה | 1.0000 |
| usdils_change_5d | 3 | volatility | ↑ | 287 | 82 | 28.6% | 24.8% | 3.8% | 28.3% | 23.7% | 34.1% | 0.1944 | 3 | 90 | 95 | 24.4% | 29.8% | 31.2% | גבוהה | 1.0000 |
| usdils_change_5d | 3 | volatility | ↓ | 327 | 249 | 76.1% | 71.6% | 4.5% | 75.9% | 71.2% | 80.4% | 0.1467 | 4 | 100 | 109 | 74.0% | 76.6% | 77.6% | גבוהה | 1.0000 |
| usdils_change_5d | 3 | volatility | ↔ | 101 | 5 | 5.0% | 3.6% | 1.3% | 4.7% | 2.1% | 11.1% | 0.3434 | 2 | 30 | 33 | 2.9% | 5.4% | 6.7% | בינונית | 1.0000 |
| usdils_change_5d | 7 | market | ↑ | 326 | 194 | 59.5% | 61.2% | -1.7% | 59.6% | 54.1% | 64.7% | 0.5954 | 1 | 40 | 46 | 47.7% | 59.6% | 69.2% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | market | ↓ | 301 | 111 | 36.9% | 38.8% | -1.9% | 37.0% | 31.6% | 42.5% | 0.5998 | 1 | 38 | 43 | 31.6% | 35.4% | 42.9% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | ↑ | 285 | 119 | 41.8% | 36.1% | 5.6% | 41.4% | 36.2% | 47.6% | 0.2302 | 4 | 36 | 40 | 32.4% | 40.0% | 51.4% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | ↓ | 326 | 204 | 62.6% | 57.4% | 5.2% | 62.3% | 57.2% | 67.7% | 0.2382 | 4 | 40 | 46 | 51.0% | 63.8% | 68.1% | גבוהה | 1.0000 |
| usdils_change_5d | 7 | volatility | ↔ | 100 | 4 | 4.0% | 6.5% | -2.5% | 4.4% | 1.6% | 9.8% | 0.6464 | 1 | 10 | 14 | 0.0% | 0.0% | 15.4% | בינונית | 1.0000 |
| usdils_change_5d | 14 | market | ↑ | 325 | 229 | 70.5% | 67.4% | 3.0% | 70.3% | 65.3% | 75.2% | 0.3778 | 3 | 17 | 23 | 58.3% | 71.8% | 81.8% | גבוהה | 1.0000 |
| usdils_change_5d | 14 | market | ↓ | 295 | 106 | 35.9% | 32.6% | 3.4% | 35.7% | 30.7% | 41.6% | 0.3716 | 3 | 15 | 21 | 23.8% | 36.1% | 60.0% | גבוהה | 1.0000 |
| usdils_change_5d | 14 | volatility | ↑ | 279 | 138 | 49.5% | 44.0% | 5.4% | 49.1% | 43.6% | 55.3% | 0.3168 | 4 | 14 | 19 | 22.7% | 50.5% | 66.7% | גבוהה | 1.0000 |
| usdils_change_5d | 14 | volatility | ↓ | 325 | 189 | 58.2% | 49.3% | 8.9% | 57.6% | 52.7% | 63.4% | 0.1976 | 6 | 17 | 23 | 35.3% | 58.8% | 75.0% | גבוהה | 1.0000 |
| usdils_change_5d | 14 | volatility | ↔ | 100 | 5 | 5.0% | 6.7% | -1.7% | 5.3% | 2.2% | 11.2% | 0.5705 | 1 | 4 | 7 | 0.0% | 0.0% | 20.0% | בינונית | 1.0000 |
| usdils_change_5d | 30 | market | ↑ | 320 | 237 | 74.1% | 74.5% | -0.5% | 74.1% | 69.0% | 78.6% | 0.5140 | 1 | 7 | 10 | 45.5% | 74.8% | 90.0% | גבוהה | 1.0000 |
| usdils_change_5d | 30 | market | ↓ | 285 | 71 | 24.9% | 25.5% | -0.5% | 24.9% | 20.2% | 30.2% | 0.5149 | 1 | 6 | 9 | 0.0% | 23.6% | 50.0% | גבוהה | 1.0000 |
| usdils_change_5d | 30 | volatility | ↑ | 269 | 141 | 52.4% | 47.4% | 5.0% | 52.1% | 46.5% | 58.3% | 0.3878 | 4 | 6 | 8 | 27.3% | 50.0% | 75.0% | גבוהה | 1.0000 |
| usdils_change_5d | 30 | volatility | ↓ | 320 | 171 | 53.4% | 45.9% | 7.5% | 53.0% | 48.0% | 58.8% | 0.3169 | 5 | 7 | 10 | 22.2% | 54.5% | 87.5% | גבוהה | 1.0000 |
| usdils_change_5d | 30 | volatility | ↔ | 99 | 9 | 9.1% | 6.7% | 2.4% | 8.7% | 4.9% | 16.4% | 0.4338 | 2 | 1 | 3 | 0.0% | 0.0% | 50.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 3 | market | ↑ | 546 | 334 | 61.2% | 60.6% | 0.5% | 61.2% | 57.0% | 65.2% | 0.4405 | 1 | 182 | 182 | 58.8% | 61.5% | 63.2% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 3 | market | ↓ | 89 | 38 | 42.7% | 39.4% | 3.3% | 42.1% | 32.9% | 53.1% | 0.3569 | 2 | 29 | 29 | 33.3% | 44.8% | 50.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 3 | volatility | ↑ | 89 | 23 | 25.8% | 24.8% | 1.1% | 25.6% | 17.9% | 35.8% | 0.4460 | 1 | 29 | 29 | 23.3% | 26.7% | 27.6% | בינונית | 1.0000 |
| vix9d_vix_ratio | 3 | volatility | ↓ | 529 | 381 | 72.0% | 71.6% | 0.4% | 72.0% | 68.0% | 75.7% | 0.4515 | 1 | 176 | 176 | 69.5% | 72.7% | 73.9% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 3 | volatility | ↔ | 97 | 2 | 2.1% | 3.6% | -1.6% | 2.3% | 0.6% | 7.2% | 0.6829 | 1 | 32 | 32 | 0.0% | 3.0% | 3.1% | בינונית | 1.0000 |
| vix9d_vix_ratio | 7 | market | ↑ | 543 | 334 | 61.5% | 62.0% | -0.5% | 61.5% | 57.4% | 65.5% | 0.5371 | 1 | 74 | 77 | 55.3% | 62.2% | 68.4% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 7 | market | ↓ | 89 | 31 | 34.8% | 38.0% | -3.1% | 35.4% | 25.7% | 45.2% | 0.5888 | 1 | 9 | 12 | 23.1% | 36.4% | 44.4% | בינונית | 1.0000 |
| vix9d_vix_ratio | 7 | volatility | ↑ | 89 | 33 | 37.1% | 36.1% | 0.9% | 36.9% | 27.8% | 47.5% | 0.4732 | 1 | 9 | 12 | 23.1% | 36.4% | 46.2% | בינונית | 1.0000 |
| vix9d_vix_ratio | 7 | volatility | ↓ | 526 | 307 | 58.4% | 57.4% | 1.0% | 58.3% | 54.1% | 62.5% | 0.4318 | 2 | 73 | 75 | 51.9% | 58.9% | 61.3% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 7 | volatility | ↔ | 96 | 11 | 11.5% | 6.5% | 5.0% | 10.6% | 6.5% | 19.4% | 0.2323 | 3 | 6 | 13 | 0.0% | 12.5% | 21.4% | בינונית | 1.0000 |
| vix9d_vix_ratio | 14 | market | ↑ | 536 | 362 | 67.5% | 68.6% | -1.1% | 67.6% | 63.5% | 71.4% | 0.5582 | 1 | 35 | 38 | 59.0% | 68.0% | 71.4% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | market | ↓ | 89 | 22 | 24.7% | 31.4% | -6.6% | 25.9% | 16.9% | 34.6% | 0.6371 | 1 | 3 | 6 | 0.0% | 18.3% | 50.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | ↑ | 89 | 46 | 51.7% | 44.0% | 7.7% | 50.3% | 41.5% | 61.8% | 0.3529 | 4 | 3 | 6 | 16.7% | 53.6% | 100.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | ↓ | 519 | 260 | 50.1% | 49.3% | 0.8% | 50.1% | 45.8% | 54.4% | 0.4609 | 1 | 35 | 37 | 41.7% | 50.0% | 59.5% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 14 | volatility | ↔ | 96 | 5 | 5.2% | 6.7% | -1.5% | 5.5% | 2.2% | 11.6% | 0.5573 | 1 | 2 | 6 | 0.0% | 0.0% | 28.6% | בינונית | 1.0000 |
| vix9d_vix_ratio | 30 | market | ↑ | 520 | 380 | 73.1% | 75.0% | -2.0% | 73.1% | 69.1% | 76.7% | 0.5742 | 1 | 12 | 17 | 58.3% | 73.3% | 85.0% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | market | ↓ | 89 | 12 | 13.5% | 25.0% | -11.5% | 15.6% | 7.9% | 22.1% | 0.6462 | 1 | 1 | 2 | 0.0% | 0.0% | 50.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↑ | 89 | 32 | 36.0% | 47.4% | -11.4% | 38.1% | 26.8% | 46.3% | 0.6269 | 1 | 1 | 2 | 0.0% | 33.3% | 100.0% | בינונית | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↓ | 503 | 217 | 43.1% | 45.9% | -2.8% | 43.2% | 38.9% | 47.5% | 0.5886 | 1 | 12 | 16 | 26.3% | 42.9% | 57.1% | גבוהה | 1.0000 |
| vix9d_vix_ratio | 30 | volatility | ↔ | 96 | 5 | 5.2% | 6.7% | -1.5% | 5.5% | 2.2% | 11.6% | 0.5408 | 1 | 1 | 3 | 0.0% | 0.0% | 50.0% | בינונית | 1.0000 |
| vix_curve_ratio | 3 | market | ↑ | 660 | 389 | 58.9% | 59.3% | -0.4% | 59.0% | 55.1% | 62.6% | 0.5434 | 1 | 218 | 220 | 58.8% | 58.8% | 59.2% | גבוהה | 1.0000 |
| vix_curve_ratio | 3 | market | ↓ | 55 | 20 | 36.4% | 40.7% | -4.3% | 37.5% | 24.9% | 49.6% | 0.6460 | 1 | 16 | 18 | 31.2% | 31.6% | 45.0% | נמוכה | 1.0000 |
| vix_curve_ratio | 3 | volatility | ↑ | 55 | 16 | 29.1% | 24.8% | 4.3% | 27.9% | 18.8% | 42.1% | 0.3350 | 2 | 16 | 18 | 25.0% | 25.0% | 36.8% | נמוכה | 1.0000 |
| vix_curve_ratio | 3 | volatility | ↓ | 640 | 465 | 72.7% | 71.6% | 1.0% | 72.6% | 69.1% | 76.0% | 0.3672 | 2 | 211 | 213 | 70.7% | 72.9% | 74.4% | גבוהה | 1.0000 |
| vix_curve_ratio | 3 | volatility | ↔ | 20 | 1 | 5.0% | 3.6% | 1.4% | 4.3% | 0.9% | 23.6% | 0.4292 | 1 | 4 | 6 | 0.0% | 0.0% | 25.0% | לא מספקת | 1.0000 |
| vix_curve_ratio | 7 | market | ↑ | 656 | 394 | 60.1% | 61.5% | -1.4% | 60.1% | 56.3% | 63.7% | 0.6094 | 1 | 88 | 93 | 54.6% | 61.5% | 65.9% | גבוהה | 1.0000 |
| vix_curve_ratio | 7 | market | ↓ | 55 | 12 | 21.8% | 38.5% | -16.7% | 26.3% | 12.9% | 34.4% | 0.8183 | 1 | 5 | 7 | 0.0% | 18.2% | 50.0% | נמוכה | 1.0000 |
| vix_curve_ratio | 7 | volatility | ↑ | 55 | 19 | 34.5% | 36.1% | -1.6% | 35.0% | 23.4% | 47.7% | 0.5351 | 1 | 5 | 7 | 16.7% | 33.3% | 55.6% | נמוכה | 1.0000 |
| vix_curve_ratio | 7 | volatility | ↓ | 636 | 372 | 58.5% | 57.4% | 1.1% | 58.5% | 54.6% | 62.3% | 0.4159 | 2 | 85 | 90 | 50.5% | 58.7% | 62.6% | גבוהה | 1.0000 |
| vix_curve_ratio | 7 | volatility | ↔ | 20 | 3 | 15.0% | 6.5% | 8.5% | 10.7% | 5.2% | 36.0% | 0.3119 | 2 | 1 | 2 | 0.0% | 0.0% | 33.3% | לא מספקת | 1.0000 |
| vix_curve_ratio | 14 | market | ↑ | 649 | 445 | 68.6% | 69.0% | -0.5% | 68.6% | 64.9% | 72.0% | 0.5273 | 1 | 43 | 46 | 62.2% | 68.8% | 75.5% | גבוהה | 1.0000 |
| vix_curve_ratio | 14 | market | ↓ | 55 | 14 | 25.5% | 31.0% | -5.5% | 26.9% | 15.8% | 38.3% | 0.5818 | 1 | 2 | 3 | 0.0% | 25.0% | 50.0% | נמוכה | 1.0000 |
| vix_curve_ratio | 14 | volatility | ↑ | 55 | 28 | 50.9% | 44.0% | 6.9% | 49.1% | 38.1% | 63.6% | 0.4052 | 3 | 2 | 3 | 16.7% | 55.0% | 100.0% | נמוכה | 1.0000 |
| vix_curve_ratio | 14 | volatility | ↓ | 629 | 316 | 50.2% | 49.3% | 0.9% | 50.2% | 46.3% | 54.1% | 0.4499 | 2 | 41 | 44 | 44.2% | 50.0% | 57.4% | גבוהה | 1.0000 |
| vix_curve_ratio | 14 | volatility | ↔ | 20 | 1 | 5.0% | 6.7% | -1.7% | 5.8% | 0.9% | 23.6% | 0.5268 | 1 | 1 | 1 | 0.0% | 0.0% | 50.0% | לא מספקת | 1.0000 |
| vix_curve_ratio | 30 | market | ↑ | 633 | 467 | 73.8% | 75.1% | -1.4% | 73.8% | 70.2% | 77.1% | 0.5577 | 1 | 18 | 21 | 61.9% | 74.5% | 85.7% | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | market | ↓ | 55 | 5 | 9.1% | 24.9% | -15.8% | 13.3% | 3.9% | 19.6% | 0.6424 | 1 | 1 | 1 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| vix_curve_ratio | 30 | volatility | ↑ | 55 | 17 | 30.9% | 47.4% | -16.5% | 35.3% | 20.3% | 44.0% | 0.6293 | 1 | 1 | 1 | 0.0% | 0.0% | 66.7% | נמוכה | 1.0000 |
| vix_curve_ratio | 30 | volatility | ↓ | 613 | 278 | 45.4% | 45.9% | -0.6% | 45.4% | 41.5% | 49.3% | 0.5207 | 1 | 17 | 20 | 28.6% | 45.5% | 61.9% | גבוהה | 1.0000 |
| vix_curve_ratio | 30 | volatility | ↔ | 20 | 4 | 20.0% | 6.7% | 13.3% | 13.3% | 8.1% | 41.6% | 0.2970 | 2 | 1 | 0 | 0.0% | 0.0% | 100.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 3 | market | ↑ | 668 | 390 | 58.4% | 59.2% | -0.8% | 58.4% | 54.6% | 62.1% | 0.5934 | 1 | 221 | 222 | 58.0% | 58.3% | 58.8% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | market | ↓ | 25 | 5 | 20.0% | 40.8% | -20.8% | 29.3% | 8.9% | 39.1% | 0.8847 | 1 | 7 | 8 | 0.0% | 27.3% | 28.6% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | ↑ | 25 | 3 | 12.0% | 24.8% | -12.8% | 17.7% | 4.2% | 30.0% | 0.7984 | 1 | 7 | 8 | 0.0% | 9.1% | 28.6% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | ↓ | 648 | 467 | 72.1% | 71.6% | 0.5% | 72.1% | 68.5% | 75.4% | 0.4405 | 1 | 214 | 216 | 70.6% | 71.8% | 73.8% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 3 | volatility | ↔ | 42 | 2 | 4.8% | 3.6% | 1.1% | 4.4% | 1.3% | 15.8% | 0.4110 | 1 | 11 | 14 | 0.0% | 5.9% | 9.1% | נמוכה | 1.0000 |
| vix_vix3m_ratio | 7 | market | ↑ | 664 | 395 | 59.5% | 60.7% | -1.2% | 59.5% | 55.7% | 63.2% | 0.5926 | 1 | 93 | 94 | 53.1% | 60.6% | 64.2% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 7 | market | ↓ | 25 | 2 | 8.0% | 39.3% | -31.3% | 21.9% | 2.2% | 25.0% | 0.8667 | 1 | 2 | 3 | 0.0% | 0.0% | 25.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | ↑ | 25 | 2 | 8.0% | 36.1% | -28.1% | 20.5% | 2.2% | 25.0% | 0.8449 | 1 | 2 | 3 | 0.0% | 0.0% | 25.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | ↓ | 644 | 373 | 57.9% | 57.4% | 0.5% | 57.9% | 54.1% | 61.7% | 0.4587 | 1 | 90 | 92 | 51.6% | 58.5% | 62.6% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 7 | volatility | ↔ | 42 | 5 | 11.9% | 6.5% | 5.4% | 10.2% | 5.2% | 25.0% | 0.2942 | 2 | 5 | 6 | 0.0% | 14.3% | 40.0% | נמוכה | 1.0000 |
| vix_vix3m_ratio | 14 | market | ↑ | 657 | 446 | 67.9% | 68.0% | -0.2% | 67.9% | 64.2% | 71.3% | 0.5088 | 1 | 46 | 46 | 60.9% | 67.7% | 75.0% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 14 | market | ↓ | 25 | 7 | 28.0% | 32.0% | -4.0% | 29.8% | 14.3% | 47.6% | 0.5339 | 1 | 1 | 1 | 0.0% | 33.3% | 100.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 14 | volatility | ↑ | 25 | 7 | 28.0% | 44.0% | -16.0% | 35.1% | 14.3% | 47.6% | 0.6266 | 1 | 1 | 1 | 0.0% | 33.3% | 100.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 14 | volatility | ↓ | 637 | 314 | 49.3% | 49.3% | 0.0% | 49.3% | 45.4% | 53.2% | 0.4998 | 1 | 44 | 45 | 43.5% | 48.9% | 55.6% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 14 | volatility | ↔ | 42 | 2 | 4.8% | 6.7% | -1.9% | 5.4% | 1.3% | 15.8% | 0.5528 | 1 | 1 | 3 | 0.0% | 0.0% | 25.0% | נמוכה | 1.0000 |
| vix_vix3m_ratio | 30 | market | ↑ | 641 | 471 | 73.5% | 74.2% | -0.7% | 73.5% | 69.9% | 76.7% | 0.5290 | 1 | 18 | 21 | 63.6% | 72.7% | 85.0% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 30 | market | ↓ | 25 | 2 | 8.0% | 25.8% | -17.8% | 15.9% | 2.2% | 25.0% | 0.6581 | 1 | 1 | 0 | 0.0% | 0.0% | 100.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | ↑ | 25 | 7 | 28.0% | 47.4% | -19.4% | 36.6% | 14.3% | 47.6% | 0.6511 | 1 | 1 | 0 | 0.0% | 0.0% | 100.0% | לא מספקת | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | ↓ | 621 | 282 | 45.4% | 45.9% | -0.5% | 45.4% | 41.5% | 49.3% | 0.5186 | 1 | 17 | 20 | 30.0% | 45.5% | 60.0% | גבוהה | 1.0000 |
| vix_vix3m_ratio | 30 | volatility | ↔ | 42 | 8 | 19.0% | 6.7% | 12.4% | 15.1% | 10.0% | 33.3% | 0.3103 | 3 | 1 | 1 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| vrp_spread | 3 | volatility | ↑ | 468 | 147 | 31.4% | 24.8% | 6.7% | 31.1% | 27.4% | 35.8% | 0.0271 | 5 | 151 | 156 | 27.8% | 31.9% | 34.4% | גבוהה | 1.0000 |
| vrp_spread | 3 | volatility | ↓ | 182 | 165 | 90.7% | 71.6% | 19.1% | 88.8% | 85.6% | 94.1% | 0.0005 | 10 | 59 | 60 | 88.5% | 90.3% | 93.2% | בינונית | 0.1661 |
| vrp_spread | 3 | volatility | ↔ | 65 | 4 | 6.2% | 3.6% | 2.5% | 5.6% | 2.4% | 14.8% | 0.2689 | 2 | 18 | 21 | 3.6% | 5.6% | 10.5% | נמוכה | 1.0000 |
| vrp_spread | 7 | volatility | ↑ | 464 | 216 | 46.6% | 36.1% | 10.4% | 46.1% | 42.1% | 51.1% | 0.0392 | 7 | 61 | 66 | 41.2% | 47.7% | 50.8% | גבוהה | 1.0000 |
| vrp_spread | 7 | volatility | ↓ | 182 | 151 | 83.0% | 57.4% | 25.6% | 80.4% | 76.8% | 87.7% | 0.0042 | 10 | 22 | 26 | 78.3% | 82.1% | 86.4% | בינונית | 1.0000 |
| vrp_spread | 7 | volatility | ↔ | 65 | 3 | 4.6% | 6.5% | -1.9% | 5.1% | 1.6% | 12.7% | 0.5895 | 1 | 7 | 9 | 0.0% | 0.0% | 12.5% | נמוכה | 1.0000 |
| vrp_spread | 14 | volatility | ↑ | 458 | 249 | 54.4% | 44.0% | 10.3% | 53.9% | 49.8% | 58.9% | 0.1195 | 7 | 29 | 32 | 44.4% | 53.5% | 65.5% | גבוהה | 1.0000 |
| vrp_spread | 14 | volatility | ↓ | 182 | 132 | 72.5% | 49.3% | 23.2% | 70.2% | 65.6% | 78.5% | 0.0469 | 10 | 8 | 13 | 53.3% | 72.5% | 88.9% | בינונית | 1.0000 |
| vrp_spread | 14 | volatility | ↔ | 64 | 2 | 3.1% | 6.7% | -3.6% | 4.0% | 0.9% | 10.7% | 0.6120 | 1 | 3 | 4 | 0.0% | 0.0% | 12.5% | נמוכה | 1.0000 |
| vrp_spread | 30 | volatility | ↑ | 442 | 267 | 60.4% | 47.4% | 13.0% | 59.8% | 55.8% | 64.9% | 0.1646 | 8 | 12 | 14 | 43.8% | 60.6% | 87.5% | גבוהה | 1.0000 |
| vrp_spread | 30 | volatility | ↓ | 182 | 134 | 73.6% | 45.9% | 27.7% | 70.9% | 66.8% | 79.5% | 0.0867 | 10 | 3 | 6 | 50.0% | 75.0% | 100.0% | בינונית | 1.0000 |
| vrp_spread | 30 | volatility | ↔ | 64 | 4 | 6.2% | 6.7% | -0.4% | 6.4% | 2.5% | 15.0% | 0.5098 | 1 | 1 | 2 | 0.0% | 0.0% | 100.0% | נמוכה | 1.0000 |
| vta35 | 3 | market | ↑ | 336 | 193 | 57.4% | 59.4% | -1.9% | 57.5% | 52.1% | 62.6% | 0.6612 | 1 | 110 | 112 | 55.4% | 57.9% | 59.1% | גבוהה | 1.0000 |
| vta35 | 3 | market | ↓ | 267 | 102 | 38.2% | 40.6% | -2.4% | 38.4% | 32.6% | 44.2% | 0.6795 | 1 | 85 | 89 | 37.2% | 37.6% | 39.8% | גבוהה | 1.0000 |
| vta35 | 3 | volatility | ↑ | 267 | 77 | 28.8% | 24.1% | 4.7% | 28.5% | 23.7% | 34.5% | 0.1486 | 4 | 85 | 89 | 24.7% | 28.4% | 33.0% | גבוהה | 1.0000 |
| vta35 | 3 | volatility | ↓ | 336 | 252 | 75.0% | 72.3% | 2.7% | 74.9% | 70.1% | 79.3% | 0.2644 | 3 | 110 | 112 | 71.8% | 73.7% | 79.5% | גבוהה | 1.0000 |
| vta35 | 3 | volatility | ↔ | 73 | 1 | 1.4% | 3.6% | -2.2% | 1.8% | 0.2% | 7.4% | 0.7181 | 1 | 19 | 24 | 0.0% | 0.0% | 5.3% | נמוכה | 1.0000 |
| vta35 | 7 | market | ↑ | 334 | 179 | 53.6% | 62.2% | -8.6% | 54.1% | 48.2% | 58.9% | 0.8890 | 1 | 42 | 47 | 45.2% | 54.2% | 60.0% | גבוהה | 1.0000 |
| vta35 | 7 | market | ↓ | 267 | 72 | 27.0% | 37.8% | -10.8% | 27.7% | 22.0% | 32.6% | 0.9152 | 1 | 34 | 38 | 22.9% | 25.0% | 34.1% | גבוהה | 1.0000 |
| vta35 | 7 | volatility | ↑ | 267 | 106 | 39.7% | 35.0% | 4.7% | 39.4% | 34.0% | 45.7% | 0.2705 | 4 | 34 | 38 | 31.4% | 40.0% | 48.8% | גבוהה | 1.0000 |
| vta35 | 7 | volatility | ↓ | 334 | 213 | 63.8% | 58.6% | 5.1% | 63.5% | 58.5% | 68.7% | 0.2371 | 4 | 42 | 47 | 58.3% | 64.3% | 68.1% | גבוהה | 1.0000 |
| vta35 | 7 | volatility | ↔ | 71 | 4 | 5.6% | 6.4% | -0.8% | 5.8% | 2.2% | 13.6% | 0.5394 | 1 | 9 | 10 | 0.0% | 0.0% | 15.4% | נמוכה | 1.0000 |
| vta35 | 14 | market | ↑ | 331 | 225 | 68.0% | 70.6% | -2.6% | 68.1% | 62.8% | 72.8% | 0.6083 | 1 | 20 | 23 | 57.1% | 67.3% | 80.0% | גבוהה | 1.0000 |
| vta35 | 14 | market | ↓ | 264 | 69 | 26.1% | 29.4% | -3.3% | 26.4% | 21.2% | 31.8% | 0.6198 | 1 | 17 | 18 | 17.6% | 24.3% | 35.3% | גבוהה | 1.0000 |
| vta35 | 14 | volatility | ↑ | 264 | 122 | 46.2% | 43.6% | 2.6% | 46.0% | 40.3% | 52.2% | 0.4119 | 2 | 17 | 18 | 29.4% | 47.1% | 59.1% | גבוהה | 1.0000 |
| vta35 | 14 | volatility | ↓ | 331 | 175 | 52.9% | 49.3% | 3.5% | 52.7% | 47.5% | 58.2% | 0.3668 | 3 | 20 | 23 | 44.0% | 54.0% | 60.0% | גבוהה | 1.0000 |
| vta35 | 14 | volatility | ↔ | 70 | 7 | 10.0% | 7.1% | 2.9% | 9.3% | 4.9% | 19.2% | 0.3990 | 2 | 3 | 5 | 0.0% | 0.0% | 40.0% | נמוכה | 1.0000 |
| vta35 | 30 | market | ↑ | 329 | 254 | 77.2% | 78.2% | -1.0% | 77.3% | 72.4% | 81.4% | 0.5298 | 1 | 6 | 10 | 50.0% | 76.4% | 100.0% | גבוהה | 1.0000 |
| vta35 | 30 | market | ↓ | 253 | 52 | 20.6% | 21.8% | -1.3% | 20.6% | 16.0% | 26.0% | 0.5346 | 1 | 5 | 8 | 0.0% | 19.1% | 42.9% | גבוהה | 1.0000 |
| vta35 | 30 | volatility | ↑ | 253 | 122 | 48.2% | 47.1% | 1.1% | 48.1% | 42.1% | 54.4% | 0.4758 | 2 | 5 | 8 | 14.3% | 50.0% | 75.0% | גבוהה | 1.0000 |
| vta35 | 30 | volatility | ↓ | 329 | 154 | 46.8% | 45.8% | 1.0% | 46.7% | 41.5% | 52.2% | 0.4735 | 2 | 6 | 10 | 18.2% | 45.8% | 70.0% | גבוהה | 1.0000 |
| vta35 | 30 | volatility | ↔ | 67 | 4 | 6.0% | 7.1% | -1.1% | 6.2% | 2.3% | 14.4% | 0.5246 | 1 | 1 | 2 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| vta35_change_5d | 3 | market | ↑ | 359 | 210 | 58.5% | 58.7% | -0.2% | 58.5% | 53.3% | 63.5% | 0.5160 | 1 | 117 | 119 | 57.3% | 59.0% | 59.3% | גבוהה | 1.0000 |
| vta35_change_5d | 3 | market | ↓ | 321 | 132 | 41.1% | 41.3% | -0.2% | 41.1% | 35.9% | 46.6% | 0.5169 | 1 | 103 | 107 | 40.4% | 40.8% | 42.2% | גבוהה | 1.0000 |
| vta35_change_5d | 3 | volatility | ↑ | 317 | 87 | 27.4% | 24.8% | 2.7% | 27.3% | 22.8% | 32.6% | 0.2616 | 3 | 101 | 105 | 24.1% | 26.9% | 31.7% | גבוהה | 1.0000 |
| vta35_change_5d | 3 | volatility | ↓ | 349 | 255 | 73.1% | 71.6% | 1.5% | 73.0% | 68.2% | 77.5% | 0.3639 | 2 | 113 | 116 | 72.6% | 73.0% | 73.6% | גבוהה | 1.0000 |
| vta35_change_5d | 3 | volatility | ↔ | 49 | 2 | 4.1% | 3.6% | 0.4% | 4.0% | 1.1% | 13.7% | 0.4621 | 1 | 15 | 16 | 0.0% | 6.2% | 6.7% | נמוכה | 1.0000 |
| vta35_change_5d | 7 | market | ↑ | 358 | 207 | 57.8% | 61.4% | -3.6% | 58.0% | 52.6% | 62.8% | 0.7027 | 1 | 48 | 51 | 49.0% | 59.2% | 64.8% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | market | ↓ | 319 | 110 | 34.5% | 38.6% | -4.1% | 34.7% | 29.5% | 39.9% | 0.7126 | 1 | 41 | 45 | 26.7% | 34.7% | 43.2% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | ↑ | 315 | 136 | 43.2% | 36.1% | 7.0% | 42.8% | 37.8% | 48.7% | 0.1632 | 5 | 40 | 45 | 37.0% | 42.2% | 50.0% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | ↓ | 348 | 225 | 64.7% | 57.4% | 7.3% | 64.3% | 59.5% | 69.5% | 0.1517 | 5 | 47 | 49 | 56.0% | 63.8% | 70.8% | גבוהה | 1.0000 |
| vta35_change_5d | 7 | volatility | ↔ | 48 | 2 | 4.2% | 6.5% | -2.3% | 4.8% | 1.2% | 14.0% | 0.5907 | 1 | 5 | 6 | 0.0% | 0.0% | 14.3% | נמוכה | 1.0000 |
| vta35_change_5d | 14 | market | ↑ | 355 | 246 | 69.3% | 69.1% | 0.2% | 69.3% | 64.3% | 73.9% | 0.4917 | 1 | 18 | 25 | 50.0% | 69.1% | 79.3% | גבוהה | 1.0000 |
| vta35_change_5d | 14 | market | ↓ | 315 | 98 | 31.1% | 30.9% | 0.2% | 31.1% | 26.3% | 36.4% | 0.4913 | 1 | 15 | 22 | 25.0% | 32.2% | 40.0% | גבוהה | 1.0000 |
| vta35_change_5d | 14 | volatility | ↑ | 311 | 158 | 50.8% | 44.0% | 6.8% | 50.4% | 45.3% | 56.3% | 0.2612 | 5 | 15 | 22 | 38.1% | 49.1% | 75.0% | גבוהה | 1.0000 |
| vta35_change_5d | 14 | volatility | ↓ | 345 | 195 | 56.5% | 49.3% | 7.2% | 56.1% | 51.2% | 61.7% | 0.2393 | 5 | 17 | 24 | 42.1% | 57.7% | 72.0% | גבוהה | 1.0000 |
| vta35_change_5d | 14 | volatility | ↔ | 48 | 2 | 4.2% | 6.7% | -2.5% | 4.9% | 1.2% | 14.0% | 0.5691 | 1 | 1 | 3 | 0.0% | 0.0% | 33.3% | נמוכה | 1.0000 |
| vta35_change_5d | 30 | market | ↑ | 346 | 269 | 77.7% | 75.8% | 1.9% | 77.6% | 73.1% | 81.8% | 0.4401 | 2 | 8 | 11 | 58.3% | 78.6% | 91.7% | גבוהה | 1.0000 |
| vta35_change_5d | 30 | market | ↓ | 311 | 82 | 26.4% | 24.2% | 2.2% | 26.2% | 21.8% | 31.5% | 0.4365 | 2 | 6 | 10 | 11.1% | 26.1% | 45.5% | גבוהה | 1.0000 |
| vta35_change_5d | 30 | volatility | ↑ | 307 | 161 | 52.4% | 47.4% | 5.1% | 52.1% | 46.9% | 58.0% | 0.3743 | 4 | 6 | 10 | 27.3% | 55.6% | 77.8% | גבוהה | 1.0000 |
| vta35_change_5d | 30 | volatility | ↓ | 336 | 171 | 50.9% | 45.9% | 5.0% | 50.6% | 45.6% | 56.2% | 0.3706 | 4 | 7 | 11 | 10.0% | 57.1% | 75.0% | גבוהה | 1.0000 |
| vta35_change_5d | 30 | volatility | ↔ | 45 | 5 | 11.1% | 6.7% | 4.4% | 9.7% | 4.8% | 23.5% | 0.4297 | 2 | 1 | 1 | 0.0% | 0.0% | 100.0% | נמוכה | 1.0000 |
| vta35_zscore_60 | 3 | market | ↑ | 336 | 193 | 57.4% | 59.4% | -1.9% | 57.5% | 52.1% | 62.6% | 0.6612 | 1 | 110 | 112 | 55.4% | 57.9% | 59.1% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | market | ↓ | 267 | 102 | 38.2% | 40.6% | -2.4% | 38.4% | 32.6% | 44.2% | 0.6795 | 1 | 85 | 89 | 37.2% | 37.6% | 39.8% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | ↑ | 267 | 77 | 28.8% | 24.1% | 4.7% | 28.5% | 23.7% | 34.5% | 0.1486 | 4 | 85 | 89 | 24.7% | 28.4% | 33.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | ↓ | 336 | 252 | 75.0% | 72.3% | 2.7% | 74.9% | 70.1% | 79.3% | 0.2644 | 3 | 110 | 112 | 71.8% | 73.7% | 79.5% | גבוהה | 1.0000 |
| vta35_zscore_60 | 3 | volatility | ↔ | 73 | 1 | 1.4% | 3.6% | -2.2% | 1.8% | 0.2% | 7.4% | 0.7181 | 1 | 19 | 24 | 0.0% | 0.0% | 5.3% | נמוכה | 1.0000 |
| vta35_zscore_60 | 7 | market | ↑ | 334 | 179 | 53.6% | 62.2% | -8.6% | 54.1% | 48.2% | 58.9% | 0.8890 | 1 | 42 | 47 | 45.2% | 54.2% | 60.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | market | ↓ | 267 | 72 | 27.0% | 37.8% | -10.8% | 27.7% | 22.0% | 32.6% | 0.9152 | 1 | 34 | 38 | 22.9% | 25.0% | 34.1% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | ↑ | 267 | 106 | 39.7% | 35.0% | 4.7% | 39.4% | 34.0% | 45.7% | 0.2705 | 4 | 34 | 38 | 31.4% | 40.0% | 48.8% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | ↓ | 334 | 213 | 63.8% | 58.6% | 5.1% | 63.5% | 58.5% | 68.7% | 0.2371 | 4 | 42 | 47 | 58.3% | 64.3% | 68.1% | גבוהה | 1.0000 |
| vta35_zscore_60 | 7 | volatility | ↔ | 71 | 4 | 5.6% | 6.4% | -0.8% | 5.8% | 2.2% | 13.6% | 0.5394 | 1 | 9 | 10 | 0.0% | 0.0% | 15.4% | נמוכה | 1.0000 |
| vta35_zscore_60 | 14 | market | ↑ | 331 | 225 | 68.0% | 70.6% | -2.6% | 68.1% | 62.8% | 72.8% | 0.6083 | 1 | 20 | 23 | 57.1% | 67.3% | 80.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | market | ↓ | 264 | 69 | 26.1% | 29.4% | -3.3% | 26.4% | 21.2% | 31.8% | 0.6198 | 1 | 17 | 18 | 17.6% | 24.3% | 35.3% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | ↑ | 264 | 122 | 46.2% | 43.6% | 2.6% | 46.0% | 40.3% | 52.2% | 0.4119 | 2 | 17 | 18 | 29.4% | 47.1% | 59.1% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | ↓ | 331 | 175 | 52.9% | 49.3% | 3.5% | 52.7% | 47.5% | 58.2% | 0.3668 | 3 | 20 | 23 | 44.0% | 54.0% | 60.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 14 | volatility | ↔ | 70 | 7 | 10.0% | 7.1% | 2.9% | 9.3% | 4.9% | 19.2% | 0.3990 | 2 | 3 | 5 | 0.0% | 0.0% | 40.0% | נמוכה | 1.0000 |
| vta35_zscore_60 | 30 | market | ↑ | 329 | 254 | 77.2% | 78.2% | -1.0% | 77.3% | 72.4% | 81.4% | 0.5298 | 1 | 6 | 10 | 50.0% | 76.4% | 100.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | market | ↓ | 253 | 52 | 20.6% | 21.8% | -1.3% | 20.6% | 16.0% | 26.0% | 0.5346 | 1 | 5 | 8 | 0.0% | 19.1% | 42.9% | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | volatility | ↑ | 253 | 122 | 48.2% | 47.1% | 1.1% | 48.1% | 42.1% | 54.4% | 0.4758 | 2 | 5 | 8 | 14.3% | 50.0% | 75.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | volatility | ↓ | 329 | 154 | 46.8% | 45.8% | 1.0% | 46.7% | 41.5% | 52.2% | 0.4735 | 2 | 6 | 10 | 18.2% | 45.8% | 70.0% | גבוהה | 1.0000 |
| vta35_zscore_60 | 30 | volatility | ↔ | 67 | 4 | 6.0% | 7.1% | -1.1% | 6.2% | 2.3% | 14.4% | 0.5246 | 1 | 1 | 2 | 0.0% | 0.0% | 50.0% | נמוכה | 1.0000 |
| vta_vol_of_vol_20 | 3 | volatility | ↑ | 670 | 165 | 24.6% | 24.8% | -0.1% | 24.6% | 21.5% | 28.0% | 0.5177 | 1 | 222 | 223 | 21.4% | 25.9% | 26.6% | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 3 | volatility | ↔ | 45 | 2 | 4.4% | 3.6% | 0.8% | 4.2% | 1.2% | 14.8% | 0.4336 | 1 | 14 | 15 | 0.0% | 6.2% | 6.7% | נמוכה | 1.0000 |
| vta_vol_of_vol_20 | 7 | volatility | ↑ | 666 | 250 | 37.5% | 36.1% | 1.4% | 37.5% | 33.9% | 41.3% | 0.3889 | 2 | 94 | 95 | 33.7% | 37.2% | 41.7% | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 7 | volatility | ↔ | 45 | 5 | 11.1% | 6.5% | 4.6% | 9.7% | 4.8% | 23.5% | 0.3220 | 2 | 5 | 6 | 0.0% | 0.0% | 33.3% | נמוכה | 1.0000 |
| vta_vol_of_vol_20 | 14 | volatility | ↑ | 659 | 299 | 45.4% | 44.0% | 1.3% | 45.3% | 41.6% | 49.2% | 0.4267 | 2 | 46 | 47 | 41.3% | 45.7% | 50.0% | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 14 | volatility | ↔ | 45 | 4 | 8.9% | 6.7% | 2.2% | 8.2% | 3.5% | 20.7% | 0.4390 | 1 | 2 | 3 | 0.0% | 0.0% | 66.7% | נמוכה | 1.0000 |
| vta_vol_of_vol_20 | 30 | volatility | ↑ | 643 | 304 | 47.3% | 47.4% | -0.1% | 47.3% | 43.4% | 51.1% | 0.5039 | 1 | 20 | 21 | 36.4% | 45.5% | 65.2% | גבוהה | 1.0000 |
| vta_vol_of_vol_20 | 30 | volatility | ↔ | 45 | 3 | 6.7% | 6.7% | -0.0% | 6.7% | 2.3% | 17.9% | 0.5003 | 1 | 1 | 1 | 0.0% | 0.0% | 100.0% | נמוכה | 1.0000 |

## Indicator intensity / threshold sensitivity

| indicator | horizon | axis | filter | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | all | 715 | 46.6% | 43.1% | 3.4% |
| atr_5_20_ratio | 3 | volatility | top 50% intensity | 358 | 55.9% | 48.8% | 7.0% |
| atr_5_20_ratio | 3 | volatility | top 25% intensity | 179 | 61.5% | 49.4% | 12.1% |
| atr_5_20_ratio | 7 | volatility | all | 711 | 46.3% | 42.0% | 4.2% |
| atr_5_20_ratio | 7 | volatility | top 50% intensity | 357 | 54.9% | 46.9% | 8.0% |
| atr_5_20_ratio | 7 | volatility | top 25% intensity | 178 | 57.9% | 46.6% | 11.3% |
| atr_5_20_ratio | 14 | volatility | all | 704 | 48.4% | 42.2% | 6.3% |
| atr_5_20_ratio | 14 | volatility | top 50% intensity | 353 | 56.4% | 47.5% | 8.9% |
| atr_5_20_ratio | 14 | volatility | top 25% intensity | 177 | 58.2% | 46.3% | 11.9% |
| atr_5_20_ratio | 30 | volatility | all | 688 | 49.9% | 42.4% | 7.4% |
| atr_5_20_ratio | 30 | volatility | top 50% intensity | 345 | 59.1% | 48.5% | 10.7% |
| atr_5_20_ratio | 30 | volatility | top 25% intensity | 173 | 57.8% | 47.3% | 10.5% |
| downside_share_20 | 3 | volatility | all | 715 | 48.1% | 46.4% | 1.7% |
| downside_share_20 | 3 | volatility | top 50% intensity | 358 | 45.5% | 43.6% | 1.9% |
| downside_share_20 | 3 | volatility | top 25% intensity | 179 | 47.5% | 44.9% | 2.6% |
| downside_share_20 | 7 | volatility | all | 711 | 40.8% | 40.0% | 0.8% |
| downside_share_20 | 7 | volatility | top 50% intensity | 357 | 42.0% | 37.7% | 4.3% |
| downside_share_20 | 7 | volatility | top 25% intensity | 178 | 36.0% | 32.5% | 3.4% |
| downside_share_20 | 14 | volatility | all | 704 | 33.9% | 35.6% | -1.6% |
| downside_share_20 | 14 | volatility | top 50% intensity | 353 | 37.1% | 33.9% | 3.2% |
| downside_share_20 | 14 | volatility | top 25% intensity | 177 | 24.9% | 25.1% | -0.2% |
| downside_share_20 | 30 | volatility | all | 688 | 32.4% | 32.7% | -0.3% |
| downside_share_20 | 30 | volatility | top 50% intensity | 345 | 31.0% | 28.9% | 2.1% |
| downside_share_20 | 30 | volatility | top 25% intensity | 173 | 22.5% | 21.7% | 0.9% |
| expected_move_3d_points | 3 | volatility | all | 715 | 35.5% | 32.0% | 3.5% |
| expected_move_3d_points | 3 | volatility | top 50% intensity | 358 | 35.5% | 32.4% | 3.1% |
| expected_move_3d_points | 3 | volatility | top 25% intensity | 179 | 35.8% | 34.0% | 1.8% |
| expected_move_3d_points | 7 | volatility | all | 711 | 38.1% | 34.0% | 4.1% |
| expected_move_3d_points | 7 | volatility | top 50% intensity | 357 | 38.7% | 36.9% | 1.8% |
| expected_move_3d_points | 7 | volatility | top 25% intensity | 178 | 35.4% | 36.0% | -0.6% |
| expected_move_3d_points | 14 | volatility | all | 704 | 41.5% | 34.9% | 6.6% |
| expected_move_3d_points | 14 | volatility | top 50% intensity | 353 | 42.2% | 38.1% | 4.1% |
| expected_move_3d_points | 14 | volatility | top 25% intensity | 177 | 35.0% | 34.8% | 0.2% |
| expected_move_3d_points | 30 | volatility | all | 688 | 41.1% | 35.9% | 5.3% |
| expected_move_3d_points | 30 | volatility | top 50% intensity | 345 | 42.9% | 38.8% | 4.1% |
| expected_move_3d_points | 30 | volatility | top 25% intensity | 173 | 41.0% | 36.2% | 4.9% |
| forecast_rv_3d | 3 | volatility | all | 715 | 35.5% | 32.0% | 3.5% |
| forecast_rv_3d | 3 | volatility | top 50% intensity | 358 | 38.8% | 33.8% | 5.0% |
| forecast_rv_3d | 3 | volatility | top 25% intensity | 179 | 45.8% | 35.7% | 10.1% |
| forecast_rv_3d | 7 | volatility | all | 711 | 38.1% | 34.0% | 4.1% |
| forecast_rv_3d | 7 | volatility | top 50% intensity | 357 | 42.0% | 35.8% | 6.2% |
| forecast_rv_3d | 7 | volatility | top 25% intensity | 178 | 47.8% | 36.1% | 11.6% |
| forecast_rv_3d | 14 | volatility | all | 704 | 41.5% | 34.9% | 6.6% |
| forecast_rv_3d | 14 | volatility | top 50% intensity | 353 | 42.5% | 35.7% | 6.8% |
| forecast_rv_3d | 14 | volatility | top 25% intensity | 177 | 42.9% | 35.4% | 7.6% |
| forecast_rv_3d | 30 | volatility | all | 688 | 41.1% | 35.9% | 5.3% |
| forecast_rv_3d | 30 | volatility | top 50% intensity | 345 | 44.9% | 37.4% | 7.5% |
| forecast_rv_3d | 30 | volatility | top 25% intensity | 173 | 43.9% | 36.6% | 7.4% |
| gap_share_20 | 3 | volatility | all | 715 | 34.1% | 32.8% | 1.3% |
| gap_share_20 | 3 | volatility | top 50% intensity | 358 | 45.3% | 43.8% | 1.4% |
| gap_share_20 | 3 | volatility | top 25% intensity | 179 | 39.7% | 42.7% | -3.1% |
| gap_share_20 | 7 | volatility | all | 711 | 33.6% | 31.0% | 2.6% |
| gap_share_20 | 7 | volatility | top 50% intensity | 357 | 42.9% | 40.7% | 2.2% |
| gap_share_20 | 7 | volatility | top 25% intensity | 178 | 39.3% | 40.8% | -1.4% |
| gap_share_20 | 14 | volatility | all | 704 | 28.0% | 30.3% | -2.3% |
| gap_share_20 | 14 | volatility | top 50% intensity | 353 | 35.4% | 38.8% | -3.4% |
| gap_share_20 | 14 | volatility | top 25% intensity | 177 | 35.6% | 38.4% | -2.8% |
| gap_share_20 | 30 | volatility | all | 688 | 23.3% | 29.6% | -6.3% |
| gap_share_20 | 30 | volatility | top 50% intensity | 345 | 30.7% | 36.8% | -6.1% |
| gap_share_20 | 30 | volatility | top 25% intensity | 173 | 31.2% | 35.2% | -4.0% |
| har_rv_3d | 3 | volatility | all | 612 | 34.8% | 31.2% | 3.6% |
| har_rv_3d | 3 | volatility | top 50% intensity | 307 | 32.2% | 29.4% | 2.9% |
| har_rv_3d | 3 | volatility | top 25% intensity | 153 | 25.5% | 25.4% | 0.1% |
| har_rv_3d | 7 | volatility | all | 608 | 37.3% | 34.4% | 2.9% |
| har_rv_3d | 7 | volatility | top 50% intensity | 305 | 38.0% | 33.9% | 4.1% |
| har_rv_3d | 7 | volatility | top 25% intensity | 153 | 36.6% | 30.4% | 6.2% |
| har_rv_3d | 14 | volatility | all | 601 | 40.1% | 36.0% | 4.1% |
| har_rv_3d | 14 | volatility | top 50% intensity | 301 | 37.9% | 35.2% | 2.6% |
| har_rv_3d | 14 | volatility | top 25% intensity | 151 | 36.4% | 32.0% | 4.4% |
| har_rv_3d | 30 | volatility | all | 585 | 39.1% | 37.6% | 1.6% |
| har_rv_3d | 30 | volatility | top 50% intensity | 293 | 37.2% | 36.5% | 0.7% |
| har_rv_3d | 30 | volatility | top 25% intensity | 147 | 33.3% | 32.7% | 0.6% |
| local_global_stress_spread | 3 | volatility | all | 616 | 45.3% | 42.2% | 3.1% |
| local_global_stress_spread | 3 | volatility | top 50% intensity | 309 | 51.5% | 48.5% | 2.9% |
| local_global_stress_spread | 3 | volatility | top 25% intensity | 155 | 49.0% | 49.5% | -0.5% |
| local_global_stress_spread | 7 | volatility | all | 612 | 46.6% | 41.9% | 4.6% |
| local_global_stress_spread | 7 | volatility | top 50% intensity | 307 | 55.0% | 48.6% | 6.4% |
| local_global_stress_spread | 7 | volatility | top 25% intensity | 153 | 54.9% | 51.2% | 3.7% |
| local_global_stress_spread | 14 | volatility | all | 605 | 42.3% | 41.5% | 0.9% |
| local_global_stress_spread | 14 | volatility | top 50% intensity | 303 | 50.5% | 46.7% | 3.8% |
| local_global_stress_spread | 14 | volatility | top 25% intensity | 153 | 45.8% | 48.5% | -2.8% |
| local_global_stress_spread | 30 | volatility | all | 589 | 41.9% | 40.7% | 1.2% |
| local_global_stress_spread | 30 | volatility | top 50% intensity | 295 | 48.8% | 44.5% | 4.3% |
| local_global_stress_spread | 30 | volatility | top 25% intensity | 149 | 45.0% | 45.8% | -0.9% |
| matched_vrp_3d | 3 | volatility | all | 612 | 24.3% | 24.3% | 0.0% |
| matched_vrp_3d | 3 | volatility | top 50% intensity | 307 | 23.8% | 23.8% | 0.0% |
| matched_vrp_3d | 3 | volatility | top 25% intensity | 153 | 23.5% | 23.5% | 0.0% |
| matched_vrp_3d | 7 | volatility | all | 608 | 36.3% | 36.3% | 0.0% |
| matched_vrp_3d | 7 | volatility | top 50% intensity | 305 | 35.4% | 35.4% | 0.0% |
| matched_vrp_3d | 7 | volatility | top 25% intensity | 153 | 32.0% | 32.0% | 0.0% |
| matched_vrp_3d | 14 | volatility | all | 601 | 47.1% | 47.1% | 0.0% |
| matched_vrp_3d | 14 | volatility | top 50% intensity | 301 | 46.5% | 46.5% | -0.0% |
| matched_vrp_3d | 14 | volatility | top 25% intensity | 151 | 47.0% | 47.0% | 0.0% |
| matched_vrp_3d | 30 | volatility | all | 585 | 52.1% | 52.1% | 0.0% |
| matched_vrp_3d | 30 | volatility | top 50% intensity | 293 | 52.6% | 52.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | top 25% intensity | 147 | 55.8% | 55.8% | 0.0% |
| range_position_20 | 3 | volatility | all | 715 | 3.6% | 3.6% | 0.0% |
| range_position_20 | 3 | volatility | top 50% intensity | 358 | 4.5% | 4.5% | 0.0% |
| range_position_20 | 3 | volatility | top 25% intensity | 251 | 4.4% | 4.4% | 0.0% |
| range_position_20 | 7 | volatility | all | 711 | 6.5% | 6.5% | 0.0% |
| range_position_20 | 7 | volatility | top 50% intensity | 357 | 7.6% | 7.6% | 0.0% |
| range_position_20 | 7 | volatility | top 25% intensity | 251 | 8.0% | 8.0% | 0.0% |
| range_position_20 | 14 | volatility | all | 704 | 6.7% | 6.7% | 0.0% |
| range_position_20 | 14 | volatility | top 50% intensity | 353 | 6.2% | 6.2% | 0.0% |
| range_position_20 | 14 | volatility | top 25% intensity | 248 | 6.0% | 6.0% | 0.0% |
| range_position_20 | 30 | volatility | all | 688 | 6.7% | 6.7% | 0.0% |
| range_position_20 | 30 | volatility | top 50% intensity | 345 | 7.8% | 7.8% | 0.0% |
| range_position_20 | 30 | volatility | top 25% intensity | 247 | 7.3% | 7.3% | 0.0% |
| reversal_5_vol_scaled | 3 | market | all | 367 | 50.7% | 45.4% | 5.3% |
| reversal_5_vol_scaled | 3 | market | top 50% intensity | 184 | 58.7% | 50.5% | 8.2% |
| reversal_5_vol_scaled | 3 | market | top 25% intensity | 93 | 58.1% | 50.4% | 7.6% |
| reversal_5_vol_scaled | 3 | volatility | all | 715 | 3.6% | 3.6% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | top 50% intensity | 358 | 3.4% | 3.4% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | top 25% intensity | 179 | 2.8% | 2.8% | 0.0% |
| reversal_5_vol_scaled | 7 | market | all | 365 | 55.6% | 45.5% | 10.1% |
| reversal_5_vol_scaled | 7 | market | top 50% intensity | 183 | 62.8% | 50.3% | 12.6% |
| reversal_5_vol_scaled | 7 | market | top 25% intensity | 93 | 66.7% | 49.7% | 16.9% |
| reversal_5_vol_scaled | 7 | volatility | all | 711 | 6.5% | 6.5% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | top 50% intensity | 357 | 7.8% | 7.8% | -0.0% |
| reversal_5_vol_scaled | 7 | volatility | top 25% intensity | 178 | 8.4% | 8.4% | 0.0% |
| reversal_5_vol_scaled | 14 | market | all | 361 | 43.8% | 41.0% | 2.8% |
| reversal_5_vol_scaled | 14 | market | top 50% intensity | 181 | 51.4% | 49.4% | 2.0% |
| reversal_5_vol_scaled | 14 | market | top 25% intensity | 91 | 51.6% | 48.6% | 3.1% |
| reversal_5_vol_scaled | 14 | volatility | all | 704 | 6.7% | 6.7% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | top 50% intensity | 353 | 8.2% | 8.2% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | top 25% intensity | 177 | 7.9% | 7.9% | 0.0% |
| reversal_5_vol_scaled | 30 | market | all | 351 | 40.2% | 39.7% | 0.5% |
| reversal_5_vol_scaled | 30 | market | top 50% intensity | 176 | 51.1% | 50.5% | 0.6% |
| reversal_5_vol_scaled | 30 | market | top 25% intensity | 89 | 50.6% | 49.9% | 0.7% |
| reversal_5_vol_scaled | 30 | volatility | all | 688 | 6.7% | 6.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | top 50% intensity | 345 | 8.1% | 8.1% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | top 25% intensity | 173 | 6.4% | 6.4% | 0.0% |
| rs_range_5_20 | 3 | volatility | all | 715 | 45.9% | 42.6% | 3.3% |
| rs_range_5_20 | 3 | volatility | top 50% intensity | 358 | 55.9% | 49.2% | 6.7% |
| rs_range_5_20 | 3 | volatility | top 25% intensity | 179 | 54.2% | 48.8% | 5.4% |
| rs_range_5_20 | 7 | volatility | all | 711 | 47.0% | 41.1% | 5.9% |
| rs_range_5_20 | 7 | volatility | top 50% intensity | 357 | 54.3% | 48.4% | 5.9% |
| rs_range_5_20 | 7 | volatility | top 25% intensity | 178 | 58.4% | 49.9% | 8.5% |
| rs_range_5_20 | 14 | volatility | all | 704 | 46.2% | 40.9% | 5.3% |
| rs_range_5_20 | 14 | volatility | top 50% intensity | 353 | 55.5% | 49.8% | 5.7% |
| rs_range_5_20 | 14 | volatility | top 25% intensity | 177 | 60.5% | 52.2% | 8.3% |
| rs_range_5_20 | 30 | volatility | all | 688 | 48.7% | 41.2% | 7.5% |
| rs_range_5_20 | 30 | volatility | top 50% intensity | 345 | 57.7% | 50.0% | 7.7% |
| rs_range_5_20 | 30 | volatility | top 25% intensity | 173 | 57.8% | 51.7% | 6.1% |
| rv_20_60_ratio | 3 | volatility | all | 675 | 45.8% | 44.1% | 1.7% |
| rv_20_60_ratio | 3 | volatility | top 50% intensity | 339 | 37.2% | 36.4% | 0.8% |
| rv_20_60_ratio | 3 | volatility | top 25% intensity | 169 | 33.7% | 34.1% | -0.3% |
| rv_20_60_ratio | 7 | volatility | all | 671 | 37.4% | 36.0% | 1.4% |
| rv_20_60_ratio | 7 | volatility | top 50% intensity | 336 | 26.8% | 26.9% | -0.1% |
| rv_20_60_ratio | 7 | volatility | top 25% intensity | 169 | 20.7% | 22.2% | -1.5% |
| rv_20_60_ratio | 14 | volatility | all | 664 | 31.6% | 32.6% | -1.0% |
| rv_20_60_ratio | 14 | volatility | top 50% intensity | 333 | 26.7% | 27.2% | -0.5% |
| rv_20_60_ratio | 14 | volatility | top 25% intensity | 167 | 22.2% | 23.7% | -1.6% |
| rv_20_60_ratio | 30 | volatility | all | 648 | 25.8% | 28.8% | -3.0% |
| rv_20_60_ratio | 30 | volatility | top 50% intensity | 325 | 24.0% | 25.1% | -1.1% |
| rv_20_60_ratio | 30 | volatility | top 25% intensity | 163 | 19.6% | 21.3% | -1.6% |
| rv_acceleration | 3 | volatility | all | 715 | 55.0% | 53.4% | 1.6% |
| rv_acceleration | 3 | volatility | top 50% intensity | 358 | 51.4% | 47.8% | 3.6% |
| rv_acceleration | 3 | volatility | top 25% intensity | 179 | 52.5% | 46.3% | 6.3% |
| rv_acceleration | 7 | volatility | all | 711 | 47.7% | 47.8% | -0.1% |
| rv_acceleration | 7 | volatility | top 50% intensity | 357 | 47.9% | 46.7% | 1.2% |
| rv_acceleration | 7 | volatility | top 25% intensity | 178 | 51.7% | 45.5% | 6.2% |
| rv_acceleration | 14 | volatility | all | 704 | 48.7% | 44.3% | 4.4% |
| rv_acceleration | 14 | volatility | top 50% intensity | 353 | 51.6% | 45.7% | 5.8% |
| rv_acceleration | 14 | volatility | top 25% intensity | 177 | 50.8% | 43.9% | 6.9% |
| rv_acceleration | 30 | volatility | all | 688 | 48.1% | 43.0% | 5.1% |
| rv_acceleration | 30 | volatility | top 50% intensity | 345 | 55.1% | 45.7% | 9.4% |
| rv_acceleration | 30 | volatility | top 25% intensity | 173 | 53.8% | 43.8% | 10.0% |
| trend_efficiency_20 | 3 | volatility | all | 715 | 30.3% | 28.4% | 2.0% |
| trend_efficiency_20 | 3 | volatility | top 50% intensity | 358 | 39.1% | 36.5% | 2.6% |
| trend_efficiency_20 | 3 | volatility | top 25% intensity | 179 | 46.9% | 46.2% | 0.7% |
| trend_efficiency_20 | 7 | volatility | all | 711 | 34.3% | 32.5% | 1.8% |
| trend_efficiency_20 | 7 | volatility | top 50% intensity | 357 | 35.3% | 32.5% | 2.8% |
| trend_efficiency_20 | 7 | volatility | top 25% intensity | 178 | 38.2% | 35.7% | 2.5% |
| trend_efficiency_20 | 14 | volatility | all | 704 | 33.9% | 35.6% | -1.7% |
| trend_efficiency_20 | 14 | volatility | top 50% intensity | 353 | 29.5% | 32.3% | -2.9% |
| trend_efficiency_20 | 14 | volatility | top 25% intensity | 177 | 23.2% | 31.1% | -8.0% |
| trend_efficiency_20 | 30 | volatility | all | 688 | 37.9% | 36.3% | 1.6% |
| trend_efficiency_20 | 30 | volatility | top 50% intensity | 345 | 33.3% | 31.6% | 1.7% |
| trend_efficiency_20 | 30 | volatility | top 25% intensity | 173 | 24.9% | 30.6% | -5.7% |
| usdils_change_5d | 3 | market | all | 630 | 51.0% | 51.0% | -0.0% |
| usdils_change_5d | 3 | market | top 50% intensity | 315 | 51.4% | 50.4% | 1.0% |
| usdils_change_5d | 3 | market | top 25% intensity | 158 | 56.3% | 50.4% | 5.9% |
| usdils_change_5d | 3 | volatility | all | 715 | 47.0% | 43.2% | 3.8% |
| usdils_change_5d | 3 | volatility | top 50% intensity | 358 | 53.9% | 48.4% | 5.5% |
| usdils_change_5d | 3 | volatility | top 25% intensity | 179 | 53.1% | 48.8% | 4.3% |
| usdils_change_5d | 7 | market | all | 627 | 48.6% | 51.2% | -2.5% |
| usdils_change_5d | 7 | market | top 50% intensity | 315 | 46.0% | 50.1% | -4.1% |
| usdils_change_5d | 7 | market | top 25% intensity | 158 | 48.1% | 50.0% | -1.9% |
| usdils_change_5d | 7 | volatility | all | 711 | 46.0% | 41.8% | 4.2% |
| usdils_change_5d | 7 | volatility | top 50% intensity | 357 | 53.5% | 46.4% | 7.1% |
| usdils_change_5d | 7 | volatility | top 25% intensity | 178 | 55.1% | 47.9% | 7.1% |
| usdils_change_5d | 14 | market | all | 620 | 54.0% | 51.7% | 2.4% |
| usdils_change_5d | 14 | market | top 50% intensity | 311 | 54.0% | 50.5% | 3.5% |
| usdils_change_5d | 14 | market | top 25% intensity | 155 | 56.1% | 50.0% | 6.2% |
| usdils_change_5d | 14 | volatility | all | 704 | 47.2% | 40.9% | 6.3% |
| usdils_change_5d | 14 | volatility | top 50% intensity | 353 | 54.7% | 46.8% | 7.9% |
| usdils_change_5d | 14 | volatility | top 25% intensity | 177 | 49.7% | 48.7% | 1.0% |
| usdils_change_5d | 30 | market | all | 605 | 50.9% | 52.3% | -1.3% |
| usdils_change_5d | 30 | market | top 50% intensity | 303 | 45.5% | 49.6% | -4.1% |
| usdils_change_5d | 30 | market | top 25% intensity | 153 | 44.4% | 49.4% | -4.9% |
| usdils_change_5d | 30 | volatility | all | 688 | 46.7% | 40.4% | 6.3% |
| usdils_change_5d | 30 | volatility | top 50% intensity | 345 | 52.2% | 45.3% | 6.9% |
| usdils_change_5d | 30 | volatility | top 25% intensity | 173 | 52.0% | 47.9% | 4.2% |
| vix9d_vix_ratio | 3 | market | all | 635 | 58.6% | 57.6% | 1.0% |
| vix9d_vix_ratio | 3 | market | top 50% intensity | 318 | 54.7% | 53.7% | 1.0% |
| vix9d_vix_ratio | 3 | market | top 25% intensity | 159 | 54.1% | 49.8% | 4.2% |
| vix9d_vix_ratio | 3 | volatility | all | 715 | 56.8% | 54.8% | 1.9% |
| vix9d_vix_ratio | 3 | volatility | top 50% intensity | 359 | 42.3% | 40.3% | 2.0% |
| vix9d_vix_ratio | 3 | volatility | top 25% intensity | 179 | 45.8% | 44.2% | 1.6% |
| vix9d_vix_ratio | 7 | market | all | 632 | 57.8% | 58.7% | -1.0% |
| vix9d_vix_ratio | 7 | market | top 50% intensity | 316 | 55.7% | 56.7% | -1.0% |
| vix9d_vix_ratio | 7 | market | top 25% intensity | 158 | 53.8% | 49.1% | 4.7% |
| vix9d_vix_ratio | 7 | volatility | all | 711 | 49.4% | 44.8% | 4.5% |
| vix9d_vix_ratio | 7 | volatility | top 50% intensity | 356 | 43.5% | 36.7% | 6.9% |
| vix9d_vix_ratio | 7 | volatility | top 25% intensity | 178 | 44.4% | 40.6% | 3.8% |
| vix9d_vix_ratio | 14 | market | all | 625 | 61.4% | 63.7% | -2.3% |
| vix9d_vix_ratio | 14 | market | top 50% intensity | 314 | 55.7% | 60.1% | -4.3% |
| vix9d_vix_ratio | 14 | market | top 25% intensity | 158 | 52.5% | 49.7% | 2.9% |
| vix9d_vix_ratio | 14 | volatility | all | 704 | 44.2% | 39.1% | 5.1% |
| vix9d_vix_ratio | 14 | volatility | top 50% intensity | 353 | 42.5% | 34.9% | 7.6% |
| vix9d_vix_ratio | 14 | volatility | top 25% intensity | 177 | 58.8% | 44.7% | 14.0% |
| vix9d_vix_ratio | 30 | market | all | 609 | 64.4% | 67.7% | -3.4% |
| vix9d_vix_ratio | 30 | market | top 50% intensity | 305 | 55.4% | 60.6% | -5.2% |
| vix9d_vix_ratio | 30 | market | top 25% intensity | 153 | 45.1% | 46.5% | -1.4% |
| vix9d_vix_ratio | 30 | volatility | all | 688 | 36.9% | 36.1% | 0.8% |
| vix9d_vix_ratio | 30 | volatility | top 50% intensity | 345 | 33.3% | 32.7% | 0.6% |
| vix9d_vix_ratio | 30 | volatility | top 25% intensity | 173 | 42.2% | 38.2% | 4.0% |
| vix_curve_ratio | 3 | market | all | 715 | 57.2% | 57.5% | -0.3% |
| vix_curve_ratio | 3 | market | top 50% intensity | 358 | 53.1% | 54.4% | -1.3% |
| vix_curve_ratio | 3 | market | top 25% intensity | 180 | 53.3% | 54.4% | -1.1% |
| vix_curve_ratio | 3 | volatility | all | 715 | 67.4% | 64.5% | 2.9% |
| vix_curve_ratio | 3 | volatility | top 50% intensity | 358 | 62.6% | 58.0% | 4.6% |
| vix_curve_ratio | 3 | volatility | top 25% intensity | 180 | 47.8% | 43.3% | 4.5% |
| vix_curve_ratio | 7 | market | all | 711 | 57.1% | 59.3% | -2.2% |
| vix_curve_ratio | 7 | market | top 50% intensity | 357 | 55.2% | 58.5% | -3.3% |
| vix_curve_ratio | 7 | market | top 25% intensity | 179 | 55.9% | 57.6% | -1.8% |
| vix_curve_ratio | 7 | volatility | all | 711 | 55.4% | 51.5% | 3.9% |
| vix_curve_ratio | 7 | volatility | top 50% intensity | 357 | 52.9% | 47.1% | 5.8% |
| vix_curve_ratio | 7 | volatility | top 25% intensity | 179 | 48.0% | 39.9% | 8.1% |
| vix_curve_ratio | 14 | market | all | 704 | 65.2% | 66.1% | -0.9% |
| vix_curve_ratio | 14 | market | top 50% intensity | 353 | 63.2% | 63.9% | -0.7% |
| vix_curve_ratio | 14 | market | top 25% intensity | 179 | 63.7% | 62.0% | 1.7% |
| vix_curve_ratio | 14 | volatility | all | 704 | 49.0% | 44.6% | 4.4% |
| vix_curve_ratio | 14 | volatility | top 50% intensity | 353 | 51.6% | 45.1% | 6.4% |
| vix_curve_ratio | 14 | volatility | top 25% intensity | 179 | 54.2% | 43.0% | 11.2% |
| vix_curve_ratio | 30 | market | all | 688 | 68.6% | 70.9% | -2.2% |
| vix_curve_ratio | 30 | market | top 50% intensity | 344 | 64.0% | 67.1% | -3.2% |
| vix_curve_ratio | 30 | market | top 25% intensity | 172 | 55.8% | 59.5% | -3.7% |
| vix_curve_ratio | 30 | volatility | all | 688 | 43.5% | 41.1% | 2.3% |
| vix_curve_ratio | 30 | volatility | top 50% intensity | 344 | 44.8% | 41.4% | 3.4% |
| vix_curve_ratio | 30 | volatility | top 25% intensity | 172 | 40.1% | 34.5% | 5.7% |
| vix_vix3m_ratio | 3 | market | all | 693 | 57.0% | 58.3% | -1.3% |
| vix_vix3m_ratio | 3 | market | top 50% intensity | 347 | 56.5% | 59.1% | -2.6% |
| vix_vix3m_ratio | 3 | market | top 25% intensity | 174 | 54.6% | 59.3% | -4.7% |
| vix_vix3m_ratio | 3 | volatility | all | 715 | 66.0% | 64.7% | 1.3% |
| vix_vix3m_ratio | 3 | volatility | top 50% intensity | 358 | 58.1% | 56.7% | 1.4% |
| vix_vix3m_ratio | 3 | volatility | top 25% intensity | 179 | 43.6% | 41.9% | 1.6% |
| vix_vix3m_ratio | 7 | market | all | 689 | 57.6% | 59.7% | -2.1% |
| vix_vix3m_ratio | 7 | market | top 50% intensity | 345 | 60.6% | 63.7% | -3.1% |
| vix_vix3m_ratio | 7 | market | top 25% intensity | 174 | 58.6% | 63.2% | -4.6% |
| vix_vix3m_ratio | 7 | volatility | all | 711 | 53.4% | 51.6% | 1.9% |
| vix_vix3m_ratio | 7 | volatility | top 50% intensity | 356 | 50.8% | 47.9% | 3.0% |
| vix_vix3m_ratio | 7 | volatility | top 25% intensity | 178 | 42.7% | 38.3% | 4.4% |
| vix_vix3m_ratio | 14 | market | all | 682 | 66.4% | 66.8% | -0.3% |
| vix_vix3m_ratio | 14 | market | top 50% intensity | 342 | 67.8% | 67.6% | 0.2% |
| vix_vix3m_ratio | 14 | market | top 25% intensity | 171 | 67.3% | 67.1% | 0.2% |
| vix_vix3m_ratio | 14 | volatility | all | 704 | 45.9% | 44.4% | 1.5% |
| vix_vix3m_ratio | 14 | volatility | top 50% intensity | 352 | 45.2% | 43.5% | 1.7% |
| vix_vix3m_ratio | 14 | volatility | top 25% intensity | 176 | 40.9% | 39.0% | 2.0% |
| vix_vix3m_ratio | 30 | market | all | 666 | 71.0% | 72.3% | -1.3% |
| vix_vix3m_ratio | 30 | market | top 50% intensity | 333 | 71.2% | 72.6% | -1.5% |
| vix_vix3m_ratio | 30 | market | top 25% intensity | 167 | 68.3% | 70.6% | -2.4% |
| vix_vix3m_ratio | 30 | volatility | all | 688 | 43.2% | 41.0% | 2.2% |
| vix_vix3m_ratio | 30 | volatility | top 50% intensity | 344 | 41.9% | 38.6% | 3.2% |
| vix_vix3m_ratio | 30 | volatility | top 25% intensity | 172 | 40.1% | 34.5% | 5.6% |
| vrp_spread | 3 | volatility | all | 715 | 44.2% | 38.7% | 5.5% |
| vrp_spread | 3 | volatility | top 50% intensity | 358 | 64.5% | 56.1% | 8.4% |
| vrp_spread | 3 | volatility | top 25% intensity | 179 | 70.4% | 62.5% | 7.9% |
| vrp_spread | 7 | volatility | all | 711 | 52.0% | 45.8% | 6.3% |
| vrp_spread | 7 | volatility | top 50% intensity | 357 | 72.5% | 59.3% | 13.2% |
| vrp_spread | 7 | volatility | top 25% intensity | 178 | 80.3% | 70.2% | 10.2% |
| vrp_spread | 14 | volatility | all | 704 | 54.4% | 50.6% | 3.8% |
| vrp_spread | 14 | volatility | top 50% intensity | 353 | 72.8% | 61.8% | 11.0% |
| vrp_spread | 14 | volatility | top 25% intensity | 177 | 83.6% | 73.7% | 9.9% |
| vrp_spread | 30 | volatility | all | 688 | 58.9% | 54.2% | 4.7% |
| vrp_spread | 30 | volatility | top 50% intensity | 345 | 75.1% | 65.8% | 9.3% |
| vrp_spread | 30 | volatility | top 25% intensity | 173 | 86.1% | 75.8% | 10.3% |
| vta35 | 3 | market | all | 603 | 48.9% | 51.1% | -2.2% |
| vta35 | 3 | market | top 50% intensity | 302 | 49.3% | 50.2% | -0.8% |
| vta35 | 3 | market | top 25% intensity | 151 | 47.7% | 51.2% | -3.5% |
| vta35 | 3 | volatility | all | 676 | 48.8% | 43.6% | 5.2% |
| vta35 | 3 | volatility | top 50% intensity | 339 | 47.8% | 41.2% | 6.6% |
| vta35 | 3 | volatility | top 25% intensity | 169 | 48.5% | 44.0% | 4.6% |
| vta35 | 7 | market | all | 601 | 41.8% | 51.2% | -9.5% |
| vta35 | 7 | market | top 50% intensity | 301 | 43.2% | 46.9% | -3.7% |
| vta35 | 7 | market | top 25% intensity | 151 | 41.7% | 48.0% | -6.2% |
| vta35 | 7 | volatility | all | 672 | 48.1% | 39.7% | 8.3% |
| vta35 | 7 | volatility | top 50% intensity | 337 | 49.0% | 38.5% | 10.5% |
| vta35 | 7 | volatility | top 25% intensity | 169 | 44.4% | 39.6% | 4.8% |
| vta35 | 14 | market | all | 595 | 49.4% | 52.8% | -3.3% |
| vta35 | 14 | market | top 50% intensity | 298 | 50.3% | 48.9% | 1.4% |
| vta35 | 14 | market | top 25% intensity | 149 | 46.3% | 50.1% | -3.8% |
| vta35 | 14 | volatility | all | 665 | 45.7% | 38.0% | 7.7% |
| vta35 | 14 | volatility | top 50% intensity | 334 | 46.7% | 37.9% | 8.8% |
| vta35 | 14 | volatility | top 25% intensity | 167 | 42.5% | 37.4% | 5.2% |
| vta35 | 30 | market | all | 582 | 52.6% | 53.7% | -1.2% |
| vta35 | 30 | market | top 50% intensity | 292 | 49.0% | 46.1% | 2.9% |
| vta35 | 30 | market | top 25% intensity | 147 | 48.3% | 46.5% | 1.8% |
| vta35 | 30 | volatility | all | 649 | 43.1% | 36.2% | 6.9% |
| vta35 | 30 | volatility | top 50% intensity | 328 | 39.0% | 33.9% | 5.1% |
| vta35 | 30 | volatility | top 25% intensity | 163 | 28.8% | 28.7% | 0.2% |
| vta35_change_5d | 3 | market | all | 680 | 50.3% | 50.2% | 0.1% |
| vta35_change_5d | 3 | market | top 50% intensity | 341 | 49.0% | 49.8% | -0.8% |
| vta35_change_5d | 3 | market | top 25% intensity | 171 | 45.0% | 49.5% | -4.4% |
| vta35_change_5d | 3 | volatility | all | 715 | 48.1% | 47.2% | 0.9% |
| vta35_change_5d | 3 | volatility | top 50% intensity | 358 | 52.0% | 49.0% | 3.0% |
| vta35_change_5d | 3 | volatility | top 25% intensity | 179 | 54.2% | 49.5% | 4.7% |
| vta35_change_5d | 7 | market | all | 677 | 46.8% | 50.3% | -3.5% |
| vta35_change_5d | 7 | market | top 50% intensity | 339 | 44.0% | 49.5% | -5.5% |
| vta35_change_5d | 7 | market | top 25% intensity | 171 | 40.9% | 48.9% | -7.9% |
| vta35_change_5d | 7 | volatility | all | 711 | 51.1% | 46.2% | 4.8% |
| vta35_change_5d | 7 | volatility | top 50% intensity | 357 | 56.9% | 47.8% | 9.0% |
| vta35_change_5d | 7 | volatility | top 25% intensity | 178 | 61.8% | 47.5% | 14.3% |
| vta35_change_5d | 14 | market | all | 670 | 51.3% | 50.5% | 0.8% |
| vta35_change_5d | 14 | market | top 50% intensity | 335 | 51.6% | 49.7% | 1.9% |
| vta35_change_5d | 14 | market | top 25% intensity | 169 | 52.7% | 49.6% | 3.1% |
| vta35_change_5d | 14 | volatility | all | 704 | 50.4% | 46.4% | 4.0% |
| vta35_change_5d | 14 | volatility | top 50% intensity | 353 | 54.4% | 50.2% | 4.1% |
| vta35_change_5d | 14 | volatility | top 25% intensity | 177 | 57.6% | 50.9% | 6.8% |
| vta35_change_5d | 30 | market | all | 657 | 53.4% | 50.7% | 2.8% |
| vta35_change_5d | 30 | market | top 50% intensity | 329 | 52.6% | 49.2% | 3.4% |
| vta35_change_5d | 30 | market | top 25% intensity | 165 | 50.3% | 49.3% | 1.0% |
| vta35_change_5d | 30 | volatility | all | 688 | 49.0% | 47.1% | 1.9% |
| vta35_change_5d | 30 | volatility | top 50% intensity | 345 | 53.0% | 50.6% | 2.4% |
| vta35_change_5d | 30 | volatility | top 25% intensity | 173 | 57.8% | 51.3% | 6.5% |
| vta35_zscore_60 | 3 | market | all | 603 | 48.9% | 51.1% | -2.2% |
| vta35_zscore_60 | 3 | market | top 50% intensity | 302 | 45.7% | 49.9% | -4.2% |
| vta35_zscore_60 | 3 | market | top 25% intensity | 151 | 46.4% | 50.8% | -4.5% |
| vta35_zscore_60 | 3 | volatility | all | 676 | 48.8% | 43.6% | 5.2% |
| vta35_zscore_60 | 3 | volatility | top 50% intensity | 339 | 51.0% | 44.7% | 6.3% |
| vta35_zscore_60 | 3 | volatility | top 25% intensity | 169 | 56.2% | 45.9% | 10.4% |
| vta35_zscore_60 | 7 | market | all | 601 | 41.8% | 51.2% | -9.5% |
| vta35_zscore_60 | 7 | market | top 50% intensity | 301 | 41.9% | 50.7% | -8.9% |
| vta35_zscore_60 | 7 | market | top 25% intensity | 151 | 40.4% | 48.3% | -7.9% |
| vta35_zscore_60 | 7 | volatility | all | 672 | 48.1% | 39.7% | 8.3% |
| vta35_zscore_60 | 7 | volatility | top 50% intensity | 337 | 54.3% | 42.2% | 12.1% |
| vta35_zscore_60 | 7 | volatility | top 25% intensity | 169 | 59.8% | 41.8% | 18.0% |
| vta35_zscore_60 | 14 | market | all | 595 | 49.4% | 52.8% | -3.3% |
| vta35_zscore_60 | 14 | market | top 50% intensity | 299 | 46.8% | 48.7% | -1.9% |
| vta35_zscore_60 | 14 | market | top 25% intensity | 149 | 47.0% | 46.4% | 0.6% |
| vta35_zscore_60 | 14 | volatility | all | 665 | 45.7% | 38.0% | 7.7% |
| vta35_zscore_60 | 14 | volatility | top 50% intensity | 333 | 48.9% | 40.4% | 8.5% |
| vta35_zscore_60 | 14 | volatility | top 25% intensity | 167 | 48.5% | 38.4% | 10.1% |
| vta35_zscore_60 | 30 | market | all | 582 | 52.6% | 53.7% | -1.2% |
| vta35_zscore_60 | 30 | market | top 50% intensity | 291 | 47.8% | 49.6% | -1.8% |
| vta35_zscore_60 | 30 | market | top 25% intensity | 147 | 47.6% | 48.3% | -0.7% |
| vta35_zscore_60 | 30 | volatility | all | 649 | 43.1% | 36.2% | 6.9% |
| vta35_zscore_60 | 30 | volatility | top 50% intensity | 325 | 44.3% | 38.3% | 6.0% |
| vta35_zscore_60 | 30 | volatility | top 25% intensity | 163 | 38.7% | 31.9% | 6.8% |
| vta_vol_of_vol_20 | 3 | volatility | all | 715 | 23.4% | 23.1% | 0.3% |
| vta_vol_of_vol_20 | 3 | volatility | top 50% intensity | 358 | 17.3% | 17.7% | -0.4% |
| vta_vol_of_vol_20 | 3 | volatility | top 25% intensity | 179 | 12.8% | 14.3% | -1.4% |
| vta_vol_of_vol_20 | 7 | volatility | all | 711 | 35.9% | 33.6% | 2.2% |
| vta_vol_of_vol_20 | 7 | volatility | top 50% intensity | 357 | 27.7% | 24.2% | 3.5% |
| vta_vol_of_vol_20 | 7 | volatility | top 25% intensity | 178 | 20.2% | 16.1% | 4.1% |
| vta_vol_of_vol_20 | 14 | volatility | all | 704 | 43.0% | 40.8% | 2.2% |
| vta_vol_of_vol_20 | 14 | volatility | top 50% intensity | 353 | 37.1% | 33.1% | 4.1% |
| vta_vol_of_vol_20 | 14 | volatility | top 25% intensity | 177 | 24.3% | 18.9% | 5.4% |
| vta_vol_of_vol_20 | 30 | volatility | all | 688 | 44.6% | 43.5% | 1.2% |
| vta_vol_of_vol_20 | 30 | volatility | top 50% intensity | 345 | 34.5% | 31.8% | 2.7% |
| vta_vol_of_vol_20 | 30 | volatility | top 25% intensity | 173 | 18.5% | 17.0% | 1.5% |

## Indicator robustness by market regime

| indicator | horizon | axis | regime | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | זהירות | 90 | 42.2% | 35.8% | 6.4% |
| atr_5_20_ratio | 3 | volatility | לחץ גבוה | 31 | 32.3% | 32.3% | 0.0% |
| atr_5_20_ratio | 3 | volatility | רגוע | 310 | 45.8% | 46.4% | -0.6% |
| atr_5_20_ratio | 3 | volatility | רגיל | 284 | 50.4% | 47.5% | 2.8% |
| atr_5_20_ratio | 7 | volatility | זהירות | 90 | 46.7% | 39.4% | 7.2% |
| atr_5_20_ratio | 7 | volatility | לחץ גבוה | 31 | 41.9% | 41.9% | 0.0% |
| atr_5_20_ratio | 7 | volatility | רגוע | 307 | 47.2% | 44.2% | 3.0% |
| atr_5_20_ratio | 7 | volatility | רגיל | 283 | 45.6% | 46.9% | -1.3% |
| atr_5_20_ratio | 14 | volatility | זהירות | 89 | 47.2% | 43.8% | 3.4% |
| atr_5_20_ratio | 14 | volatility | לחץ גבוה | 31 | 25.8% | 25.8% | 0.0% |
| atr_5_20_ratio | 14 | volatility | רגוע | 306 | 48.7% | 42.2% | 6.5% |
| atr_5_20_ratio | 14 | volatility | רגיל | 278 | 51.1% | 46.7% | 4.4% |
| atr_5_20_ratio | 30 | volatility | זהירות | 86 | 50.0% | 43.1% | 6.9% |
| atr_5_20_ratio | 30 | volatility | לחץ גבוה | 31 | 25.8% | 25.8% | 0.0% |
| atr_5_20_ratio | 30 | volatility | רגוע | 300 | 51.7% | 42.5% | 9.2% |
| atr_5_20_ratio | 30 | volatility | רגיל | 271 | 50.6% | 46.4% | 4.2% |
| downside_share_20 | 3 | volatility | זהירות | 90 | 36.7% | 36.5% | 0.2% |
| downside_share_20 | 3 | volatility | לחץ גבוה | 31 | 41.9% | 42.0% | -0.1% |
| downside_share_20 | 3 | volatility | רגוע | 310 | 54.8% | 53.3% | 1.5% |
| downside_share_20 | 3 | volatility | רגיל | 284 | 45.1% | 44.4% | 0.7% |
| downside_share_20 | 7 | volatility | זהירות | 90 | 26.7% | 33.2% | -6.5% |
| downside_share_20 | 7 | volatility | לחץ גבוה | 31 | 22.6% | 38.7% | -16.1% |
| downside_share_20 | 7 | volatility | רגוע | 307 | 49.2% | 44.8% | 4.4% |
| downside_share_20 | 7 | volatility | רגיל | 283 | 38.2% | 40.3% | -2.2% |
| downside_share_20 | 14 | volatility | זהירות | 89 | 22.5% | 34.3% | -11.8% |
| downside_share_20 | 14 | volatility | לחץ גבוה | 31 | 6.5% | 21.0% | -14.6% |
| downside_share_20 | 14 | volatility | רגוע | 306 | 38.9% | 36.9% | 1.9% |
| downside_share_20 | 14 | volatility | רגיל | 278 | 35.3% | 36.8% | -1.5% |
| downside_share_20 | 30 | volatility | זהירות | 86 | 25.6% | 32.8% | -7.3% |
| downside_share_20 | 30 | volatility | לחץ גבוה | 31 | 9.7% | 25.2% | -15.5% |
| downside_share_20 | 30 | volatility | רגוע | 300 | 36.0% | 33.7% | 2.3% |
| downside_share_20 | 30 | volatility | רגיל | 271 | 33.2% | 33.5% | -0.3% |
| expected_move_3d_points | 3 | volatility | זהירות | 90 | 30.0% | 24.2% | 5.8% |
| expected_move_3d_points | 3 | volatility | לחץ גבוה | 31 | 12.9% | 15.2% | -2.3% |
| expected_move_3d_points | 3 | volatility | רגוע | 310 | 35.5% | 32.6% | 2.9% |
| expected_move_3d_points | 3 | volatility | רגיל | 284 | 39.8% | 38.8% | 1.0% |
| expected_move_3d_points | 7 | volatility | זהירות | 90 | 43.3% | 35.2% | 8.1% |
| expected_move_3d_points | 7 | volatility | לחץ גבוה | 31 | 19.4% | 22.3% | -2.9% |
| expected_move_3d_points | 7 | volatility | רגוע | 307 | 38.4% | 33.5% | 5.0% |
| expected_move_3d_points | 7 | volatility | רגיל | 283 | 38.2% | 41.1% | -3.0% |
| expected_move_3d_points | 14 | volatility | זהירות | 89 | 40.4% | 32.4% | 8.1% |
| expected_move_3d_points | 14 | volatility | לחץ גבוה | 31 | 16.1% | 20.5% | -4.4% |
| expected_move_3d_points | 14 | volatility | רגוע | 306 | 37.9% | 33.6% | 4.3% |
| expected_move_3d_points | 14 | volatility | רגיל | 278 | 48.6% | 42.0% | 6.6% |
| expected_move_3d_points | 30 | volatility | זהירות | 86 | 50.0% | 38.0% | 12.0% |
| expected_move_3d_points | 30 | volatility | לחץ גבוה | 31 | 12.9% | 18.7% | -5.8% |
| expected_move_3d_points | 30 | volatility | רגוע | 300 | 34.7% | 32.9% | 1.8% |
| expected_move_3d_points | 30 | volatility | רגיל | 271 | 48.7% | 43.2% | 5.5% |
| forecast_rv_3d | 3 | volatility | זהירות | 90 | 30.0% | 24.2% | 5.8% |
| forecast_rv_3d | 3 | volatility | לחץ גבוה | 31 | 12.9% | 15.2% | -2.3% |
| forecast_rv_3d | 3 | volatility | רגוע | 310 | 35.5% | 32.6% | 2.9% |
| forecast_rv_3d | 3 | volatility | רגיל | 284 | 39.8% | 38.8% | 1.0% |
| forecast_rv_3d | 7 | volatility | זהירות | 90 | 43.3% | 35.2% | 8.1% |
| forecast_rv_3d | 7 | volatility | לחץ גבוה | 31 | 19.4% | 22.3% | -2.9% |
| forecast_rv_3d | 7 | volatility | רגוע | 307 | 38.4% | 33.5% | 5.0% |
| forecast_rv_3d | 7 | volatility | רגיל | 283 | 38.2% | 41.1% | -3.0% |
| forecast_rv_3d | 14 | volatility | זהירות | 89 | 40.4% | 32.4% | 8.1% |
| forecast_rv_3d | 14 | volatility | לחץ גבוה | 31 | 16.1% | 20.5% | -4.4% |
| forecast_rv_3d | 14 | volatility | רגוע | 306 | 37.9% | 33.6% | 4.3% |
| forecast_rv_3d | 14 | volatility | רגיל | 278 | 48.6% | 42.0% | 6.6% |
| forecast_rv_3d | 30 | volatility | זהירות | 86 | 50.0% | 38.0% | 12.0% |
| forecast_rv_3d | 30 | volatility | לחץ גבוה | 31 | 12.9% | 18.7% | -5.8% |
| forecast_rv_3d | 30 | volatility | רגוע | 300 | 34.7% | 32.9% | 1.8% |
| forecast_rv_3d | 30 | volatility | רגיל | 271 | 48.7% | 43.2% | 5.5% |
| gap_share_20 | 3 | volatility | זהירות | 90 | 34.4% | 33.4% | 1.0% |
| gap_share_20 | 3 | volatility | לחץ גבוה | 31 | 32.3% | 27.5% | 4.7% |
| gap_share_20 | 3 | volatility | רגוע | 310 | 35.5% | 34.4% | 1.1% |
| gap_share_20 | 3 | volatility | רגיל | 284 | 32.7% | 33.6% | -0.9% |
| gap_share_20 | 7 | volatility | זהירות | 90 | 33.3% | 32.0% | 1.3% |
| gap_share_20 | 7 | volatility | לחץ גבוה | 31 | 41.9% | 37.8% | 4.1% |
| gap_share_20 | 7 | volatility | רגוע | 307 | 33.6% | 30.8% | 2.7% |
| gap_share_20 | 7 | volatility | רגיל | 283 | 32.9% | 34.1% | -1.3% |
| gap_share_20 | 14 | volatility | זהירות | 89 | 30.3% | 34.6% | -4.3% |
| gap_share_20 | 14 | volatility | לחץ גבוה | 31 | 22.6% | 20.2% | 2.4% |
| gap_share_20 | 14 | volatility | רגוע | 306 | 26.8% | 27.8% | -1.0% |
| gap_share_20 | 14 | volatility | רגיל | 278 | 29.1% | 34.8% | -5.6% |
| gap_share_20 | 30 | volatility | זהירות | 86 | 24.4% | 33.6% | -9.2% |
| gap_share_20 | 30 | volatility | לחץ גבוה | 31 | 19.4% | 20.3% | -1.0% |
| gap_share_20 | 30 | volatility | רגוע | 300 | 22.0% | 26.0% | -4.0% |
| gap_share_20 | 30 | volatility | רגיל | 271 | 24.7% | 34.2% | -9.5% |
| har_rv_3d | 3 | volatility | זהירות | 76 | 27.6% | 23.2% | 4.4% |
| har_rv_3d | 3 | volatility | לחץ גבוה | 26 | 15.4% | 18.1% | -2.7% |
| har_rv_3d | 3 | volatility | רגוע | 251 | 33.1% | 29.3% | 3.8% |
| har_rv_3d | 3 | volatility | רגיל | 259 | 40.5% | 39.8% | 0.7% |
| har_rv_3d | 7 | volatility | זהירות | 76 | 42.1% | 36.3% | 5.9% |
| har_rv_3d | 7 | volatility | לחץ גבוה | 26 | 23.1% | 26.5% | -3.5% |
| har_rv_3d | 7 | volatility | רגוע | 248 | 35.5% | 31.3% | 4.2% |
| har_rv_3d | 7 | volatility | רגיל | 258 | 39.1% | 42.0% | -2.9% |
| har_rv_3d | 14 | volatility | זהירות | 75 | 37.3% | 33.1% | 4.3% |
| har_rv_3d | 14 | volatility | לחץ גבוה | 26 | 19.2% | 24.4% | -5.2% |
| har_rv_3d | 14 | volatility | רגוע | 247 | 34.0% | 32.2% | 1.8% |
| har_rv_3d | 14 | volatility | רגיל | 253 | 49.0% | 43.8% | 5.2% |
| har_rv_3d | 30 | volatility | זהירות | 72 | 48.6% | 39.8% | 8.8% |
| har_rv_3d | 30 | volatility | לחץ גבוה | 26 | 15.4% | 22.3% | -6.9% |
| har_rv_3d | 30 | volatility | רגוע | 241 | 29.5% | 31.5% | -2.1% |
| har_rv_3d | 30 | volatility | רגיל | 246 | 48.4% | 45.6% | 2.8% |
| local_global_stress_spread | 3 | volatility | זהירות | 76 | 46.1% | 40.2% | 5.9% |
| local_global_stress_spread | 3 | volatility | לחץ גבוה | 26 | 42.3% | 43.6% | -1.3% |
| local_global_stress_spread | 3 | volatility | רגוע | 255 | 47.8% | 44.9% | 3.0% |
| local_global_stress_spread | 3 | volatility | רגיל | 259 | 42.9% | 41.8% | 1.1% |
| local_global_stress_spread | 7 | volatility | זהירות | 76 | 48.7% | 49.2% | -0.5% |
| local_global_stress_spread | 7 | volatility | לחץ גבוה | 26 | 53.8% | 49.9% | 3.9% |
| local_global_stress_spread | 7 | volatility | רגוע | 252 | 45.6% | 41.6% | 4.0% |
| local_global_stress_spread | 7 | volatility | רגיל | 258 | 46.1% | 43.2% | 2.9% |
| local_global_stress_spread | 14 | volatility | זהירות | 75 | 42.7% | 49.7% | -7.1% |
| local_global_stress_spread | 14 | volatility | לחץ גבוה | 26 | 50.0% | 50.6% | -0.6% |
| local_global_stress_spread | 14 | volatility | רגוע | 251 | 39.4% | 38.5% | 1.0% |
| local_global_stress_spread | 14 | volatility | רגיל | 253 | 44.3% | 43.1% | 1.1% |
| local_global_stress_spread | 30 | volatility | זהירות | 72 | 44.4% | 53.0% | -8.6% |
| local_global_stress_spread | 30 | volatility | לחץ גבוה | 26 | 53.8% | 48.1% | 5.8% |
| local_global_stress_spread | 30 | volatility | רגוע | 245 | 40.0% | 37.1% | 2.9% |
| local_global_stress_spread | 30 | volatility | רגיל | 246 | 41.9% | 41.2% | 0.7% |
| matched_vrp_3d | 3 | volatility | זהירות | 76 | 30.3% | 30.3% | 0.0% |
| matched_vrp_3d | 3 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| matched_vrp_3d | 3 | volatility | רגוע | 251 | 23.5% | 23.5% | 0.0% |
| matched_vrp_3d | 3 | volatility | רגיל | 259 | 22.8% | 22.8% | -0.0% |
| matched_vrp_3d | 7 | volatility | זהירות | 76 | 43.4% | 43.4% | 0.0% |
| matched_vrp_3d | 7 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| matched_vrp_3d | 7 | volatility | רגוע | 248 | 37.1% | 37.1% | 0.0% |
| matched_vrp_3d | 7 | volatility | רגיל | 258 | 34.1% | 34.1% | 0.0% |
| matched_vrp_3d | 14 | volatility | זהירות | 75 | 49.3% | 49.3% | -0.0% |
| matched_vrp_3d | 14 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| matched_vrp_3d | 14 | volatility | רגוע | 247 | 51.4% | 51.4% | -0.0% |
| matched_vrp_3d | 14 | volatility | רגיל | 253 | 43.9% | 43.9% | 0.0% |
| matched_vrp_3d | 30 | volatility | זהירות | 72 | 48.6% | 48.6% | 0.0% |
| matched_vrp_3d | 30 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| matched_vrp_3d | 30 | volatility | רגוע | 241 | 62.7% | 62.7% | -0.0% |
| matched_vrp_3d | 30 | volatility | רגיל | 246 | 45.1% | 45.1% | 0.0% |
| range_position_20 | 3 | volatility | זהירות | 90 | 1.1% | 1.1% | 0.0% |
| range_position_20 | 3 | volatility | לחץ גבוה | 31 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 3 | volatility | רגוע | 310 | 4.8% | 4.8% | -0.0% |
| range_position_20 | 3 | volatility | רגיל | 284 | 3.5% | 3.5% | 0.0% |
| range_position_20 | 7 | volatility | זהירות | 90 | 8.9% | 8.9% | 0.0% |
| range_position_20 | 7 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| range_position_20 | 7 | volatility | רגוע | 307 | 7.8% | 7.8% | -0.0% |
| range_position_20 | 7 | volatility | רגיל | 283 | 4.6% | 4.6% | 0.0% |
| range_position_20 | 14 | volatility | זהירות | 89 | 6.7% | 6.7% | 0.0% |
| range_position_20 | 14 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| range_position_20 | 14 | volatility | רגוע | 306 | 8.8% | 8.8% | 0.0% |
| range_position_20 | 14 | volatility | רגיל | 278 | 4.7% | 4.7% | 0.0% |
| range_position_20 | 30 | volatility | זהירות | 86 | 5.8% | 5.8% | 0.0% |
| range_position_20 | 30 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| range_position_20 | 30 | volatility | רגוע | 300 | 5.7% | 5.7% | -0.0% |
| range_position_20 | 30 | volatility | רגיל | 271 | 8.5% | 8.5% | 0.0% |
| reversal_5_vol_scaled | 3 | market | זהירות | 44 | 59.1% | 59.3% | -0.2% |
| reversal_5_vol_scaled | 3 | market | לחץ גבוה | 19 | 42.1% | 43.4% | -1.3% |
| reversal_5_vol_scaled | 3 | market | רגוע | 168 | 47.6% | 45.5% | 2.1% |
| reversal_5_vol_scaled | 3 | market | רגיל | 136 | 52.9% | 44.6% | 8.3% |
| reversal_5_vol_scaled | 3 | volatility | זהירות | 90 | 1.1% | 1.1% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | לחץ גבוה | 31 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | רגוע | 310 | 4.8% | 4.8% | -0.0% |
| reversal_5_vol_scaled | 3 | volatility | רגיל | 284 | 3.5% | 3.5% | 0.0% |
| reversal_5_vol_scaled | 7 | market | זהירות | 44 | 54.5% | 54.2% | 0.3% |
| reversal_5_vol_scaled | 7 | market | לחץ גבוה | 19 | 52.6% | 51.0% | 1.6% |
| reversal_5_vol_scaled | 7 | market | רגוע | 167 | 57.5% | 47.0% | 10.5% |
| reversal_5_vol_scaled | 7 | market | רגיל | 135 | 54.1% | 46.0% | 8.1% |
| reversal_5_vol_scaled | 7 | volatility | זהירות | 90 | 8.9% | 8.9% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | רגוע | 307 | 7.8% | 7.8% | -0.0% |
| reversal_5_vol_scaled | 7 | volatility | רגיל | 283 | 4.6% | 4.6% | 0.0% |
| reversal_5_vol_scaled | 14 | market | זהירות | 44 | 65.9% | 62.1% | 3.8% |
| reversal_5_vol_scaled | 14 | market | לחץ גבוה | 19 | 42.1% | 42.4% | -0.3% |
| reversal_5_vol_scaled | 14 | market | רגוע | 167 | 41.9% | 36.1% | 5.8% |
| reversal_5_vol_scaled | 14 | market | רגיל | 131 | 38.9% | 40.8% | -1.8% |
| reversal_5_vol_scaled | 14 | volatility | זהירות | 89 | 6.7% | 6.7% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | רגוע | 306 | 8.8% | 8.8% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | רגיל | 278 | 4.7% | 4.7% | 0.0% |
| reversal_5_vol_scaled | 30 | market | זהירות | 43 | 58.1% | 58.1% | 0.1% |
| reversal_5_vol_scaled | 30 | market | לחץ גבוה | 19 | 57.9% | 60.8% | -2.9% |
| reversal_5_vol_scaled | 30 | market | רגוע | 163 | 34.4% | 34.2% | 0.1% |
| reversal_5_vol_scaled | 30 | market | רגיל | 126 | 38.9% | 38.0% | 0.9% |
| reversal_5_vol_scaled | 30 | volatility | זהירות | 86 | 5.8% | 5.8% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | לחץ גבוה | 31 | 3.2% | 3.2% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | רגוע | 300 | 5.7% | 5.7% | -0.0% |
| reversal_5_vol_scaled | 30 | volatility | רגיל | 271 | 8.5% | 8.5% | 0.0% |
| rs_range_5_20 | 3 | volatility | זהירות | 90 | 36.7% | 34.8% | 1.9% |
| rs_range_5_20 | 3 | volatility | לחץ גבוה | 31 | 35.5% | 32.5% | 3.0% |
| rs_range_5_20 | 3 | volatility | רגוע | 310 | 46.5% | 44.8% | 1.6% |
| rs_range_5_20 | 3 | volatility | רגיל | 284 | 49.3% | 47.1% | 2.2% |
| rs_range_5_20 | 7 | volatility | זהירות | 90 | 34.4% | 39.7% | -5.2% |
| rs_range_5_20 | 7 | volatility | לחץ גבוה | 31 | 41.9% | 46.3% | -4.4% |
| rs_range_5_20 | 7 | volatility | רגוע | 307 | 51.1% | 42.6% | 8.5% |
| rs_range_5_20 | 7 | volatility | רגיל | 283 | 47.0% | 44.9% | 2.1% |
| rs_range_5_20 | 14 | volatility | זהירות | 89 | 37.1% | 43.3% | -6.3% |
| rs_range_5_20 | 14 | volatility | לחץ גבוה | 31 | 25.8% | 30.8% | -4.9% |
| rs_range_5_20 | 14 | volatility | רגוע | 306 | 49.3% | 40.2% | 9.1% |
| rs_range_5_20 | 14 | volatility | רגיל | 278 | 47.8% | 45.0% | 2.9% |
| rs_range_5_20 | 30 | volatility | זהירות | 86 | 43.0% | 43.3% | -0.3% |
| rs_range_5_20 | 30 | volatility | לחץ גבוה | 31 | 25.8% | 29.4% | -3.5% |
| rs_range_5_20 | 30 | volatility | רגוע | 300 | 49.7% | 40.2% | 9.5% |
| rs_range_5_20 | 30 | volatility | רגיל | 271 | 52.0% | 45.0% | 7.0% |
| rv_20_60_ratio | 3 | volatility | זהירות | 76 | 40.8% | 38.1% | 2.7% |
| rv_20_60_ratio | 3 | volatility | לחץ גבוה | 26 | 46.2% | 39.0% | 7.2% |
| rv_20_60_ratio | 3 | volatility | רגוע | 301 | 51.5% | 51.4% | 0.1% |
| rv_20_60_ratio | 3 | volatility | רגיל | 272 | 40.8% | 38.0% | 2.8% |
| rv_20_60_ratio | 7 | volatility | זהירות | 76 | 30.3% | 25.5% | 4.8% |
| rv_20_60_ratio | 7 | volatility | לחץ גבוה | 26 | 23.1% | 25.5% | -2.4% |
| rv_20_60_ratio | 7 | volatility | רגוע | 298 | 43.0% | 42.2% | 0.8% |
| rv_20_60_ratio | 7 | volatility | רגיל | 271 | 34.7% | 32.9% | 1.8% |
| rv_20_60_ratio | 14 | volatility | זהירות | 75 | 33.3% | 32.0% | 1.3% |
| rv_20_60_ratio | 14 | volatility | לחץ גבוה | 26 | 23.1% | 23.3% | -0.3% |
| rv_20_60_ratio | 14 | volatility | רגוע | 297 | 33.7% | 36.0% | -2.4% |
| rv_20_60_ratio | 14 | volatility | רגיל | 266 | 29.7% | 30.0% | -0.3% |
| rv_20_60_ratio | 30 | volatility | זהירות | 72 | 25.0% | 23.7% | 1.3% |
| rv_20_60_ratio | 30 | volatility | לחץ גבוה | 26 | 23.1% | 27.7% | -4.6% |
| rv_20_60_ratio | 30 | volatility | רגוע | 291 | 29.9% | 34.0% | -4.1% |
| rv_20_60_ratio | 30 | volatility | רגיל | 259 | 21.6% | 24.4% | -2.8% |
| rv_acceleration | 3 | volatility | זהירות | 90 | 52.2% | 46.8% | 5.4% |
| rv_acceleration | 3 | volatility | לחץ גבוה | 31 | 29.0% | 31.3% | -2.3% |
| rv_acceleration | 3 | volatility | רגוע | 310 | 57.4% | 57.6% | -0.2% |
| rv_acceleration | 3 | volatility | רגיל | 284 | 56.0% | 57.1% | -1.1% |
| rv_acceleration | 7 | volatility | זהירות | 90 | 50.0% | 43.0% | 7.0% |
| rv_acceleration | 7 | volatility | לחץ גבוה | 31 | 38.7% | 41.6% | -2.9% |
| rv_acceleration | 7 | volatility | רגוע | 307 | 46.6% | 50.7% | -4.1% |
| rv_acceleration | 7 | volatility | רגיל | 283 | 49.1% | 52.8% | -3.7% |
| rv_acceleration | 14 | volatility | זהירות | 89 | 52.8% | 42.5% | 10.3% |
| rv_acceleration | 14 | volatility | לחץ גבוה | 31 | 22.6% | 25.3% | -2.7% |
| rv_acceleration | 14 | volatility | רגוע | 306 | 44.8% | 44.4% | 0.4% |
| rv_acceleration | 14 | volatility | רגיל | 278 | 54.7% | 49.3% | 5.4% |
| rv_acceleration | 30 | volatility | זהירות | 86 | 64.0% | 44.6% | 19.4% |
| rv_acceleration | 30 | volatility | לחץ גבוה | 31 | 22.6% | 25.2% | -2.6% |
| rv_acceleration | 30 | volatility | רגוע | 300 | 43.0% | 42.8% | 0.2% |
| rv_acceleration | 30 | volatility | רגיל | 271 | 51.7% | 47.0% | 4.7% |
| trend_efficiency_20 | 3 | volatility | זהירות | 90 | 27.8% | 25.2% | 2.6% |
| trend_efficiency_20 | 3 | volatility | לחץ גבוה | 31 | 29.0% | 28.2% | 0.9% |
| trend_efficiency_20 | 3 | volatility | רגוע | 310 | 30.6% | 29.5% | 1.1% |
| trend_efficiency_20 | 3 | volatility | רגיל | 284 | 31.0% | 28.2% | 2.8% |
| trend_efficiency_20 | 7 | volatility | זהירות | 90 | 32.2% | 26.7% | 5.5% |
| trend_efficiency_20 | 7 | volatility | לחץ גבוה | 31 | 19.4% | 22.0% | -2.7% |
| trend_efficiency_20 | 7 | volatility | רגוע | 307 | 32.2% | 32.1% | 0.2% |
| trend_efficiency_20 | 7 | volatility | רגיל | 283 | 38.9% | 34.7% | 4.2% |
| trend_efficiency_20 | 14 | volatility | זהירות | 89 | 39.3% | 31.2% | 8.1% |
| trend_efficiency_20 | 14 | volatility | לחץ גבוה | 31 | 16.1% | 19.9% | -3.8% |
| trend_efficiency_20 | 14 | volatility | רגוע | 306 | 30.7% | 36.0% | -5.3% |
| trend_efficiency_20 | 14 | volatility | רגיל | 278 | 37.8% | 38.2% | -0.4% |
| trend_efficiency_20 | 30 | volatility | זהירות | 86 | 33.7% | 26.3% | 7.5% |
| trend_efficiency_20 | 30 | volatility | לחץ גבוה | 31 | 16.1% | 22.6% | -6.5% |
| trend_efficiency_20 | 30 | volatility | רגוע | 300 | 37.0% | 39.0% | -2.0% |
| trend_efficiency_20 | 30 | volatility | רגיל | 271 | 42.8% | 37.9% | 4.9% |
| usdils_change_5d | 3 | market | זהירות | 85 | 51.8% | 49.2% | 2.6% |
| usdils_change_5d | 3 | market | לחץ גבוה | 27 | 40.7% | 45.7% | -4.9% |
| usdils_change_5d | 3 | market | רגוע | 264 | 49.2% | 52.2% | -3.0% |
| usdils_change_5d | 3 | market | רגיל | 254 | 53.5% | 50.7% | 2.8% |
| usdils_change_5d | 3 | volatility | זהירות | 90 | 36.7% | 36.3% | 0.3% |
| usdils_change_5d | 3 | volatility | לחץ גבוה | 31 | 22.6% | 29.5% | -6.9% |
| usdils_change_5d | 3 | volatility | רגוע | 310 | 51.3% | 47.9% | 3.4% |
| usdils_change_5d | 3 | volatility | רגיל | 284 | 48.2% | 45.6% | 2.6% |
| usdils_change_5d | 7 | market | זהירות | 85 | 49.4% | 49.4% | 0.0% |
| usdils_change_5d | 7 | market | לחץ גבוה | 27 | 33.3% | 39.5% | -6.2% |
| usdils_change_5d | 7 | market | רגוע | 261 | 47.1% | 52.9% | -5.7% |
| usdils_change_5d | 7 | market | רגיל | 254 | 51.6% | 49.6% | 1.9% |
| usdils_change_5d | 7 | volatility | זהירות | 90 | 33.3% | 37.6% | -4.3% |
| usdils_change_5d | 7 | volatility | לחץ גבוה | 31 | 35.5% | 38.0% | -2.5% |
| usdils_change_5d | 7 | volatility | רגוע | 307 | 46.6% | 43.8% | 2.8% |
| usdils_change_5d | 7 | volatility | רגיל | 283 | 50.5% | 47.0% | 3.6% |
| usdils_change_5d | 14 | market | זהירות | 84 | 45.2% | 46.3% | -1.0% |
| usdils_change_5d | 14 | market | לחץ גבוה | 27 | 37.0% | 42.8% | -5.8% |
| usdils_change_5d | 14 | market | רגוע | 260 | 56.2% | 56.6% | -0.5% |
| usdils_change_5d | 14 | market | רגיל | 249 | 56.6% | 51.7% | 4.9% |
| usdils_change_5d | 14 | volatility | זהירות | 89 | 50.6% | 39.0% | 11.6% |
| usdils_change_5d | 14 | volatility | לחץ גבוה | 31 | 22.6% | 22.8% | -0.2% |
| usdils_change_5d | 14 | volatility | רגוע | 306 | 42.2% | 40.2% | 2.0% |
| usdils_change_5d | 14 | volatility | רגיל | 278 | 54.3% | 47.9% | 6.4% |
| usdils_change_5d | 30 | market | זהירות | 81 | 46.9% | 43.1% | 3.8% |
| usdils_change_5d | 30 | market | לחץ גבוה | 27 | 25.9% | 24.7% | 1.2% |
| usdils_change_5d | 30 | market | רגוע | 254 | 58.7% | 57.3% | 1.4% |
| usdils_change_5d | 30 | market | רגיל | 243 | 46.9% | 50.4% | -3.5% |
| usdils_change_5d | 30 | volatility | זהירות | 86 | 45.3% | 38.8% | 6.6% |
| usdils_change_5d | 30 | volatility | לחץ גבוה | 31 | 16.1% | 23.2% | -7.1% |
| usdils_change_5d | 30 | volatility | רגוע | 300 | 43.7% | 39.0% | 4.7% |
| usdils_change_5d | 30 | volatility | רגיל | 271 | 53.9% | 47.9% | 6.0% |
| vix9d_vix_ratio | 3 | market | זהירות | 69 | 50.7% | 55.7% | -5.0% |
| vix9d_vix_ratio | 3 | market | לחץ גבוה | 25 | 40.0% | 42.7% | -2.7% |
| vix9d_vix_ratio | 3 | market | רגוע | 293 | 60.1% | 57.5% | 2.6% |
| vix9d_vix_ratio | 3 | market | רגיל | 248 | 60.9% | 60.1% | 0.8% |
| vix9d_vix_ratio | 3 | volatility | זהירות | 90 | 43.3% | 40.9% | 2.4% |
| vix9d_vix_ratio | 3 | volatility | לחץ גבוה | 31 | 45.2% | 38.3% | 6.9% |
| vix9d_vix_ratio | 3 | volatility | רגוע | 310 | 61.3% | 61.7% | -0.4% |
| vix9d_vix_ratio | 3 | volatility | רגיל | 284 | 57.4% | 55.7% | 1.7% |
| vix9d_vix_ratio | 7 | market | זהירות | 69 | 60.9% | 61.7% | -0.8% |
| vix9d_vix_ratio | 7 | market | לחץ גבוה | 25 | 32.0% | 33.3% | -1.3% |
| vix9d_vix_ratio | 7 | market | רגוע | 291 | 57.4% | 57.6% | -0.2% |
| vix9d_vix_ratio | 7 | market | רגיל | 247 | 59.9% | 60.7% | -0.8% |
| vix9d_vix_ratio | 7 | volatility | זהירות | 90 | 37.8% | 29.5% | 8.3% |
| vix9d_vix_ratio | 7 | volatility | לחץ גבוה | 31 | 29.0% | 21.7% | 7.4% |
| vix9d_vix_ratio | 7 | volatility | רגוע | 307 | 53.4% | 51.5% | 2.0% |
| vix9d_vix_ratio | 7 | volatility | רגיל | 283 | 50.9% | 47.1% | 3.7% |
| vix9d_vix_ratio | 14 | market | זהירות | 68 | 60.3% | 60.5% | -0.2% |
| vix9d_vix_ratio | 14 | market | לחץ גבוה | 25 | 24.0% | 36.9% | -12.9% |
| vix9d_vix_ratio | 14 | market | רגוע | 290 | 65.2% | 67.2% | -2.0% |
| vix9d_vix_ratio | 14 | market | רגיל | 242 | 61.2% | 63.7% | -2.6% |
| vix9d_vix_ratio | 14 | volatility | זהירות | 89 | 38.2% | 29.9% | 8.3% |
| vix9d_vix_ratio | 14 | volatility | לחץ גבוה | 31 | 35.5% | 30.8% | 4.7% |
| vix9d_vix_ratio | 14 | volatility | רגוע | 306 | 42.2% | 41.8% | 0.4% |
| vix9d_vix_ratio | 14 | volatility | רגיל | 278 | 49.3% | 41.8% | 7.5% |
| vix9d_vix_ratio | 30 | market | זהירות | 65 | 60.0% | 57.1% | 2.9% |
| vix9d_vix_ratio | 30 | market | לחץ גבוה | 25 | 28.0% | 45.3% | -17.3% |
| vix9d_vix_ratio | 30 | market | רגוע | 284 | 68.7% | 69.2% | -0.5% |
| vix9d_vix_ratio | 30 | market | רגיל | 235 | 64.3% | 69.1% | -4.9% |
| vix9d_vix_ratio | 30 | volatility | זהירות | 86 | 29.1% | 26.6% | 2.4% |
| vix9d_vix_ratio | 30 | volatility | לחץ גבוה | 31 | 41.9% | 34.2% | 7.7% |
| vix9d_vix_ratio | 30 | volatility | רגוע | 300 | 36.0% | 38.2% | -2.2% |
| vix9d_vix_ratio | 30 | volatility | רגיל | 271 | 39.9% | 38.6% | 1.3% |
| vix_curve_ratio | 3 | market | זהירות | 82 | 51.2% | 50.7% | 0.6% |
| vix_curve_ratio | 3 | market | לחץ גבוה | 30 | 40.0% | 45.3% | -5.3% |
| vix_curve_ratio | 3 | market | רגוע | 319 | 57.4% | 57.4% | 0.0% |
| vix_curve_ratio | 3 | market | רגיל | 284 | 60.6% | 60.6% | 0.0% |
| vix_curve_ratio | 3 | volatility | זהירות | 90 | 57.8% | 54.8% | 3.0% |
| vix_curve_ratio | 3 | volatility | לחץ גבוה | 31 | 54.8% | 50.0% | 4.8% |
| vix_curve_ratio | 3 | volatility | רגוע | 310 | 70.6% | 70.2% | 0.4% |
| vix_curve_ratio | 3 | volatility | רגיל | 284 | 68.3% | 65.0% | 3.3% |
| vix_curve_ratio | 7 | market | זהירות | 82 | 56.1% | 60.9% | -4.8% |
| vix_curve_ratio | 7 | market | לחץ גבוה | 30 | 33.3% | 39.3% | -6.0% |
| vix_curve_ratio | 7 | market | רגוע | 316 | 57.9% | 57.9% | 0.0% |
| vix_curve_ratio | 7 | market | רגיל | 283 | 59.0% | 60.8% | -1.8% |
| vix_curve_ratio | 7 | volatility | זהירות | 90 | 42.2% | 38.3% | 4.0% |
| vix_curve_ratio | 7 | volatility | לחץ גבוה | 31 | 25.8% | 27.3% | -1.5% |
| vix_curve_ratio | 7 | volatility | רגוע | 307 | 58.0% | 57.3% | 0.7% |
| vix_curve_ratio | 7 | volatility | רגיל | 283 | 60.1% | 53.5% | 6.6% |
| vix_curve_ratio | 14 | market | זהירות | 81 | 64.2% | 63.9% | 0.3% |
| vix_curve_ratio | 14 | market | לחץ גבוה | 30 | 33.3% | 41.1% | -7.7% |
| vix_curve_ratio | 14 | market | רגוע | 315 | 70.2% | 70.2% | -0.0% |
| vix_curve_ratio | 14 | market | רגיל | 278 | 63.3% | 64.9% | -1.6% |
| vix_curve_ratio | 14 | volatility | זהירות | 89 | 44.9% | 37.9% | 7.1% |
| vix_curve_ratio | 14 | volatility | לחץ גבוה | 31 | 38.7% | 41.1% | -2.4% |
| vix_curve_ratio | 14 | volatility | רגוע | 306 | 45.8% | 45.5% | 0.3% |
| vix_curve_ratio | 14 | volatility | רגיל | 278 | 55.0% | 47.1% | 7.9% |
| vix_curve_ratio | 30 | market | זהירות | 78 | 67.9% | 67.5% | 0.5% |
| vix_curve_ratio | 30 | market | לחץ גבוה | 30 | 40.0% | 52.6% | -12.6% |
| vix_curve_ratio | 30 | market | רגוע | 309 | 70.9% | 70.9% | 0.0% |
| vix_curve_ratio | 30 | market | רגיל | 271 | 69.4% | 71.8% | -2.4% |
| vix_curve_ratio | 30 | volatility | זהירות | 86 | 41.9% | 35.5% | 6.4% |
| vix_curve_ratio | 30 | volatility | לחץ גבוה | 31 | 45.2% | 45.2% | 0.0% |
| vix_curve_ratio | 30 | volatility | רגוע | 300 | 41.3% | 41.4% | -0.0% |
| vix_curve_ratio | 30 | volatility | רגיל | 271 | 46.1% | 42.9% | 3.2% |
| vix_vix3m_ratio | 3 | market | זהירות | 79 | 53.2% | 53.0% | 0.2% |
| vix_vix3m_ratio | 3 | market | לחץ גבוה | 29 | 34.5% | 46.7% | -12.3% |
| vix_vix3m_ratio | 3 | market | רגוע | 321 | 57.3% | 57.3% | 0.0% |
| vix_vix3m_ratio | 3 | market | רגיל | 264 | 60.2% | 61.6% | -1.3% |
| vix_vix3m_ratio | 3 | volatility | זהירות | 90 | 57.8% | 57.6% | 0.2% |
| vix_vix3m_ratio | 3 | volatility | לחץ גבוה | 31 | 51.6% | 50.3% | 1.3% |
| vix_vix3m_ratio | 3 | volatility | רגוע | 310 | 71.0% | 70.8% | 0.2% |
| vix_vix3m_ratio | 3 | volatility | רגיל | 284 | 64.8% | 63.6% | 1.2% |
| vix_vix3m_ratio | 7 | market | זהירות | 79 | 58.2% | 62.3% | -4.1% |
| vix_vix3m_ratio | 7 | market | לחץ גבוה | 29 | 34.5% | 42.1% | -7.7% |
| vix_vix3m_ratio | 7 | market | רגוע | 318 | 57.9% | 57.9% | 0.0% |
| vix_vix3m_ratio | 7 | market | רגיל | 263 | 59.7% | 61.3% | -1.6% |
| vix_vix3m_ratio | 7 | volatility | זהירות | 90 | 43.3% | 41.2% | 2.1% |
| vix_vix3m_ratio | 7 | volatility | לחץ גבוה | 31 | 25.8% | 29.0% | -3.2% |
| vix_vix3m_ratio | 7 | volatility | רגוע | 307 | 58.0% | 57.8% | 0.2% |
| vix_vix3m_ratio | 7 | volatility | רגיל | 283 | 54.8% | 51.6% | 3.2% |
| vix_vix3m_ratio | 14 | market | זהירות | 78 | 65.4% | 64.8% | 0.6% |
| vix_vix3m_ratio | 14 | market | לחץ גבוה | 29 | 34.5% | 42.9% | -8.4% |
| vix_vix3m_ratio | 14 | market | רגוע | 317 | 70.0% | 70.0% | 0.0% |
| vix_vix3m_ratio | 14 | market | רגיל | 258 | 65.9% | 65.5% | 0.4% |
| vix_vix3m_ratio | 14 | volatility | זהירות | 89 | 41.6% | 38.3% | 3.3% |
| vix_vix3m_ratio | 14 | volatility | לחץ גבוה | 31 | 35.5% | 42.9% | -7.4% |
| vix_vix3m_ratio | 14 | volatility | רגוע | 306 | 45.8% | 46.0% | -0.2% |
| vix_vix3m_ratio | 14 | volatility | רגיל | 278 | 48.6% | 44.8% | 3.8% |
| vix_vix3m_ratio | 30 | market | זהירות | 75 | 76.0% | 74.6% | 1.4% |
| vix_vix3m_ratio | 30 | market | לחץ גבוה | 29 | 44.8% | 56.3% | -11.5% |
| vix_vix3m_ratio | 30 | market | רגוע | 311 | 71.1% | 71.1% | 0.0% |
| vix_vix3m_ratio | 30 | market | רגיל | 251 | 72.5% | 74.0% | -1.5% |
| vix_vix3m_ratio | 30 | volatility | זהירות | 86 | 40.7% | 38.2% | 2.5% |
| vix_vix3m_ratio | 30 | volatility | לחץ גבוה | 31 | 38.7% | 46.5% | -7.7% |
| vix_vix3m_ratio | 30 | volatility | רגוע | 300 | 42.0% | 41.9% | 0.1% |
| vix_vix3m_ratio | 30 | volatility | רגיל | 271 | 45.8% | 40.8% | 5.0% |
| vrp_spread | 3 | volatility | זהירות | 90 | 50.0% | 41.8% | 8.2% |
| vrp_spread | 3 | volatility | לחץ גבוה | 31 | 35.5% | 32.9% | 2.6% |
| vrp_spread | 3 | volatility | רגוע | 310 | 42.9% | 36.2% | 6.7% |
| vrp_spread | 3 | volatility | רגיל | 284 | 44.7% | 44.2% | 0.6% |
| vrp_spread | 7 | volatility | זהירות | 90 | 57.8% | 52.2% | 5.6% |
| vrp_spread | 7 | volatility | לחץ גבוה | 31 | 48.4% | 42.6% | 5.8% |
| vrp_spread | 7 | volatility | רגוע | 307 | 50.8% | 43.0% | 7.8% |
| vrp_spread | 7 | volatility | רגיל | 283 | 51.9% | 51.8% | 0.1% |
| vrp_spread | 14 | volatility | זהירות | 89 | 52.8% | 51.0% | 1.8% |
| vrp_spread | 14 | volatility | לחץ גבוה | 31 | 41.9% | 36.1% | 5.8% |
| vrp_spread | 14 | volatility | רגוע | 306 | 54.6% | 49.0% | 5.6% |
| vrp_spread | 14 | volatility | רגיל | 278 | 56.1% | 56.3% | -0.2% |
| vrp_spread | 30 | volatility | זהירות | 86 | 64.0% | 56.3% | 7.7% |
| vrp_spread | 30 | volatility | לחץ גבוה | 31 | 41.9% | 34.2% | 7.7% |
| vrp_spread | 30 | volatility | רגוע | 300 | 57.3% | 53.5% | 3.9% |
| vrp_spread | 30 | volatility | רגיל | 271 | 60.9% | 58.7% | 2.2% |
| vta35 | 3 | market | זהירות | 74 | 47.3% | 47.3% | 0.0% |
| vta35 | 3 | market | לחץ גבוה | 26 | 34.6% | 34.6% | 0.0% |
| vta35 | 3 | market | רגוע | 260 | 56.2% | 54.4% | 1.8% |
| vta35 | 3 | market | רגיל | 243 | 43.2% | 50.7% | -7.5% |
| vta35 | 3 | volatility | זהירות | 76 | 30.3% | 29.3% | 1.0% |
| vta35 | 3 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35 | 3 | volatility | רגוע | 302 | 55.6% | 53.1% | 2.5% |
| vta35 | 3 | volatility | רגיל | 272 | 48.2% | 42.6% | 5.6% |
| vta35 | 7 | market | זהירות | 74 | 31.1% | 31.1% | -0.0% |
| vta35 | 7 | market | לחץ גבוה | 26 | 19.2% | 19.2% | 0.0% |
| vta35 | 7 | market | רגוע | 259 | 47.5% | 55.1% | -7.6% |
| vta35 | 7 | market | רגיל | 242 | 41.3% | 50.7% | -9.3% |
| vta35 | 7 | volatility | זהירות | 76 | 43.4% | 42.2% | 1.3% |
| vta35 | 7 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35 | 7 | volatility | רגוע | 299 | 55.2% | 46.2% | 9.0% |
| vta35 | 7 | volatility | רגיל | 271 | 43.2% | 40.2% | 2.9% |
| vta35 | 14 | market | זהירות | 73 | 35.6% | 35.6% | 0.0% |
| vta35 | 14 | market | לחץ גבוה | 26 | 26.9% | 26.9% | -0.0% |
| vta35 | 14 | market | רגוע | 259 | 57.5% | 62.0% | -4.4% |
| vta35 | 14 | market | רגיל | 237 | 47.3% | 51.8% | -4.5% |
| vta35 | 14 | volatility | זהירות | 75 | 49.3% | 47.9% | 1.4% |
| vta35 | 14 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35 | 14 | volatility | רגוע | 298 | 46.3% | 39.6% | 6.7% |
| vta35 | 14 | volatility | רגיל | 266 | 45.5% | 39.1% | 6.4% |
| vta35 | 30 | market | זהירות | 70 | 15.7% | 15.7% | 0.0% |
| vta35 | 30 | market | לחץ גבוה | 26 | 15.4% | 15.4% | 0.0% |
| vta35 | 30 | market | רגוע | 255 | 66.7% | 63.4% | 3.2% |
| vta35 | 30 | market | רגיל | 231 | 52.4% | 54.5% | -2.1% |
| vta35 | 30 | volatility | זהירות | 72 | 45.8% | 47.0% | -1.2% |
| vta35 | 30 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35 | 30 | volatility | רגוע | 292 | 45.9% | 37.5% | 8.3% |
| vta35 | 30 | volatility | רגיל | 259 | 40.5% | 36.2% | 4.3% |
| vta35_change_5d | 3 | market | זהירות | 87 | 44.8% | 47.8% | -3.0% |
| vta35_change_5d | 3 | market | לחץ גבוה | 31 | 41.9% | 45.9% | -4.0% |
| vta35_change_5d | 3 | market | רגוע | 289 | 54.0% | 50.7% | 3.3% |
| vta35_change_5d | 3 | market | רגיל | 273 | 49.1% | 50.5% | -1.4% |
| vta35_change_5d | 3 | volatility | זהירות | 90 | 37.8% | 41.6% | -3.9% |
| vta35_change_5d | 3 | volatility | לחץ גבוה | 31 | 32.3% | 37.2% | -4.9% |
| vta35_change_5d | 3 | volatility | רגוע | 310 | 49.4% | 51.3% | -1.9% |
| vta35_change_5d | 3 | volatility | רגיל | 284 | 51.8% | 49.3% | 2.5% |
| vta35_change_5d | 7 | market | זהירות | 87 | 39.1% | 40.8% | -1.7% |
| vta35_change_5d | 7 | market | לחץ גבוה | 31 | 38.7% | 40.1% | -1.4% |
| vta35_change_5d | 7 | market | רגוע | 287 | 49.5% | 50.8% | -1.3% |
| vta35_change_5d | 7 | market | רגיל | 272 | 47.4% | 50.5% | -3.1% |
| vta35_change_5d | 7 | volatility | זהירות | 90 | 54.4% | 48.8% | 5.6% |
| vta35_change_5d | 7 | volatility | לחץ גבוה | 31 | 45.2% | 46.1% | -0.9% |
| vta35_change_5d | 7 | volatility | רגוע | 307 | 50.5% | 49.2% | 1.3% |
| vta35_change_5d | 7 | volatility | רגיל | 283 | 51.2% | 48.1% | 3.2% |
| vta35_change_5d | 14 | market | זהירות | 86 | 33.7% | 42.2% | -8.4% |
| vta35_change_5d | 14 | market | לחץ גבוה | 31 | 38.7% | 44.6% | -5.9% |
| vta35_change_5d | 14 | market | רגוע | 286 | 55.2% | 55.3% | -0.1% |
| vta35_change_5d | 14 | market | רגיל | 267 | 54.3% | 50.4% | 3.9% |
| vta35_change_5d | 14 | volatility | זהירות | 89 | 52.8% | 49.8% | 3.1% |
| vta35_change_5d | 14 | volatility | לחץ גבוה | 31 | 32.3% | 29.9% | 2.4% |
| vta35_change_5d | 14 | volatility | רגוע | 306 | 49.7% | 46.9% | 2.7% |
| vta35_change_5d | 14 | volatility | רגיל | 278 | 52.5% | 48.7% | 3.9% |
| vta35_change_5d | 30 | market | זהירות | 83 | 33.7% | 38.3% | -4.5% |
| vta35_change_5d | 30 | market | לחץ גבוה | 31 | 32.3% | 28.3% | 4.0% |
| vta35_change_5d | 30 | market | רגוע | 281 | 60.5% | 54.5% | 6.0% |
| vta35_change_5d | 30 | market | רגיל | 262 | 54.6% | 50.2% | 4.4% |
| vta35_change_5d | 30 | volatility | זהירות | 86 | 52.3% | 52.5% | -0.2% |
| vta35_change_5d | 30 | volatility | לחץ גבוה | 31 | 25.8% | 30.0% | -4.2% |
| vta35_change_5d | 30 | volatility | רגוע | 300 | 50.0% | 47.8% | 2.2% |
| vta35_change_5d | 30 | volatility | רגיל | 271 | 49.4% | 48.4% | 1.0% |
| vta35_zscore_60 | 3 | market | זהירות | 74 | 47.3% | 47.3% | 0.0% |
| vta35_zscore_60 | 3 | market | לחץ גבוה | 26 | 34.6% | 34.6% | 0.0% |
| vta35_zscore_60 | 3 | market | רגוע | 260 | 56.2% | 54.4% | 1.8% |
| vta35_zscore_60 | 3 | market | רגיל | 243 | 43.2% | 50.7% | -7.5% |
| vta35_zscore_60 | 3 | volatility | זהירות | 76 | 30.3% | 29.3% | 1.0% |
| vta35_zscore_60 | 3 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35_zscore_60 | 3 | volatility | רגוע | 302 | 55.6% | 53.1% | 2.5% |
| vta35_zscore_60 | 3 | volatility | רגיל | 272 | 48.2% | 42.6% | 5.6% |
| vta35_zscore_60 | 7 | market | זהירות | 74 | 31.1% | 31.1% | -0.0% |
| vta35_zscore_60 | 7 | market | לחץ גבוה | 26 | 19.2% | 19.2% | 0.0% |
| vta35_zscore_60 | 7 | market | רגוע | 259 | 47.5% | 55.1% | -7.6% |
| vta35_zscore_60 | 7 | market | רגיל | 242 | 41.3% | 50.7% | -9.3% |
| vta35_zscore_60 | 7 | volatility | זהירות | 76 | 43.4% | 42.2% | 1.3% |
| vta35_zscore_60 | 7 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35_zscore_60 | 7 | volatility | רגוע | 299 | 55.2% | 46.2% | 9.0% |
| vta35_zscore_60 | 7 | volatility | רגיל | 271 | 43.2% | 40.2% | 2.9% |
| vta35_zscore_60 | 14 | market | זהירות | 73 | 35.6% | 35.6% | 0.0% |
| vta35_zscore_60 | 14 | market | לחץ גבוה | 26 | 26.9% | 26.9% | -0.0% |
| vta35_zscore_60 | 14 | market | רגוע | 259 | 57.5% | 62.0% | -4.4% |
| vta35_zscore_60 | 14 | market | רגיל | 237 | 47.3% | 51.8% | -4.5% |
| vta35_zscore_60 | 14 | volatility | זהירות | 75 | 49.3% | 47.9% | 1.4% |
| vta35_zscore_60 | 14 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35_zscore_60 | 14 | volatility | רגוע | 298 | 46.3% | 39.6% | 6.7% |
| vta35_zscore_60 | 14 | volatility | רגיל | 266 | 45.5% | 39.1% | 6.4% |
| vta35_zscore_60 | 30 | market | זהירות | 70 | 15.7% | 15.7% | 0.0% |
| vta35_zscore_60 | 30 | market | לחץ גבוה | 26 | 15.4% | 15.4% | 0.0% |
| vta35_zscore_60 | 30 | market | רגוע | 255 | 66.7% | 63.4% | 3.2% |
| vta35_zscore_60 | 30 | market | רגיל | 231 | 52.4% | 54.5% | -2.1% |
| vta35_zscore_60 | 30 | volatility | זהירות | 72 | 45.8% | 47.0% | -1.2% |
| vta35_zscore_60 | 30 | volatility | לחץ גבוה | 26 | 30.8% | 30.8% | 0.0% |
| vta35_zscore_60 | 30 | volatility | רגוע | 292 | 45.9% | 37.5% | 8.3% |
| vta35_zscore_60 | 30 | volatility | רגיל | 259 | 40.5% | 36.2% | 4.3% |
| vta_vol_of_vol_20 | 3 | volatility | זהירות | 90 | 25.6% | 25.6% | 0.0% |
| vta_vol_of_vol_20 | 3 | volatility | לחץ גבוה | 31 | 32.3% | 32.3% | 0.0% |
| vta_vol_of_vol_20 | 3 | volatility | רגוע | 310 | 22.3% | 22.4% | -0.1% |
| vta_vol_of_vol_20 | 3 | volatility | רגיל | 284 | 22.9% | 21.9% | 1.0% |
| vta_vol_of_vol_20 | 7 | volatility | זהירות | 90 | 35.6% | 35.3% | 0.3% |
| vta_vol_of_vol_20 | 7 | volatility | לחץ גבוה | 31 | 41.9% | 41.9% | 0.0% |
| vta_vol_of_vol_20 | 7 | volatility | רגוע | 307 | 34.9% | 31.6% | 3.3% |
| vta_vol_of_vol_20 | 7 | volatility | רגיל | 283 | 36.4% | 34.3% | 2.1% |
| vta_vol_of_vol_20 | 14 | volatility | זהירות | 89 | 42.7% | 42.1% | 0.6% |
| vta_vol_of_vol_20 | 14 | volatility | לחץ גבוה | 31 | 25.8% | 25.8% | 0.0% |
| vta_vol_of_vol_20 | 14 | volatility | רגוע | 306 | 45.8% | 41.5% | 4.2% |
| vta_vol_of_vol_20 | 14 | volatility | רגיל | 278 | 42.1% | 40.9% | 1.2% |
| vta_vol_of_vol_20 | 30 | volatility | זהירות | 86 | 39.5% | 39.5% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | לחץ גבוה | 31 | 25.8% | 25.8% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | רגוע | 300 | 50.7% | 47.7% | 3.0% |
| vta_vol_of_vol_20 | 30 | volatility | רגיל | 271 | 41.7% | 41.2% | 0.5% |

## Indicator robustness by calendar year

| indicator | horizon | axis | year | n | accuracy | baseline | lift |
| --- | --- | --- | --- | --- | --- | --- | --- |
| atr_5_20_ratio | 3 | volatility | 2,023 | 81 | 54.3% | 49.9% | 4.4% |
| atr_5_20_ratio | 3 | volatility | 2,024 | 245 | 40.4% | 42.9% | -2.5% |
| atr_5_20_ratio | 3 | volatility | 2,025 | 246 | 45.9% | 41.3% | 4.6% |
| atr_5_20_ratio | 3 | volatility | 2,026 | 143 | 53.8% | 45.0% | 8.8% |
| atr_5_20_ratio | 7 | volatility | 2,023 | 81 | 58.0% | 47.3% | 10.8% |
| atr_5_20_ratio | 7 | volatility | 2,024 | 245 | 37.1% | 41.7% | -4.6% |
| atr_5_20_ratio | 7 | volatility | 2,025 | 246 | 50.4% | 42.5% | 7.9% |
| atr_5_20_ratio | 7 | volatility | 2,026 | 139 | 48.2% | 42.3% | 5.9% |
| atr_5_20_ratio | 14 | volatility | 2,023 | 81 | 51.9% | 49.5% | 2.3% |
| atr_5_20_ratio | 14 | volatility | 2,024 | 245 | 46.5% | 41.4% | 5.1% |
| atr_5_20_ratio | 14 | volatility | 2,025 | 246 | 49.2% | 41.8% | 7.3% |
| atr_5_20_ratio | 14 | volatility | 2,026 | 132 | 48.5% | 43.7% | 4.8% |
| atr_5_20_ratio | 30 | volatility | 2,023 | 81 | 51.9% | 49.3% | 2.6% |
| atr_5_20_ratio | 30 | volatility | 2,024 | 245 | 46.1% | 40.5% | 5.6% |
| atr_5_20_ratio | 30 | volatility | 2,025 | 246 | 52.4% | 42.8% | 9.6% |
| atr_5_20_ratio | 30 | volatility | 2,026 | 116 | 50.9% | 47.5% | 3.3% |
| downside_share_20 | 3 | volatility | 2,023 | 81 | 43.2% | 38.7% | 4.5% |
| downside_share_20 | 3 | volatility | 2,024 | 245 | 48.6% | 49.6% | -1.0% |
| downside_share_20 | 3 | volatility | 2,025 | 246 | 50.8% | 48.4% | 2.4% |
| downside_share_20 | 3 | volatility | 2,026 | 143 | 45.5% | 46.1% | -0.6% |
| downside_share_20 | 7 | volatility | 2,023 | 81 | 45.7% | 41.5% | 4.2% |
| downside_share_20 | 7 | volatility | 2,024 | 245 | 46.1% | 43.9% | 2.2% |
| downside_share_20 | 7 | volatility | 2,025 | 246 | 39.4% | 36.8% | 2.6% |
| downside_share_20 | 7 | volatility | 2,026 | 139 | 30.9% | 42.0% | -11.1% |
| downside_share_20 | 14 | volatility | 2,023 | 81 | 46.9% | 45.4% | 1.5% |
| downside_share_20 | 14 | volatility | 2,024 | 245 | 40.4% | 39.2% | 1.2% |
| downside_share_20 | 14 | volatility | 2,025 | 246 | 30.1% | 28.5% | 1.5% |
| downside_share_20 | 14 | volatility | 2,026 | 132 | 21.2% | 40.8% | -19.6% |
| downside_share_20 | 30 | volatility | 2,023 | 81 | 49.4% | 47.9% | 1.5% |
| downside_share_20 | 30 | volatility | 2,024 | 245 | 35.5% | 35.4% | 0.1% |
| downside_share_20 | 30 | volatility | 2,025 | 246 | 29.3% | 24.5% | 4.8% |
| downside_share_20 | 30 | volatility | 2,026 | 116 | 20.7% | 36.4% | -15.7% |
| expected_move_3d_points | 3 | volatility | 2,023 | 81 | 44.4% | 39.4% | 5.1% |
| expected_move_3d_points | 3 | volatility | 2,024 | 245 | 27.3% | 23.6% | 3.8% |
| expected_move_3d_points | 3 | volatility | 2,025 | 246 | 37.4% | 35.4% | 2.0% |
| expected_move_3d_points | 3 | volatility | 2,026 | 143 | 41.3% | 39.8% | 1.5% |
| expected_move_3d_points | 7 | volatility | 2,023 | 81 | 50.6% | 36.9% | 13.8% |
| expected_move_3d_points | 7 | volatility | 2,024 | 245 | 28.2% | 26.0% | 2.1% |
| expected_move_3d_points | 7 | volatility | 2,025 | 246 | 40.2% | 37.4% | 2.9% |
| expected_move_3d_points | 7 | volatility | 2,026 | 139 | 44.6% | 45.6% | -1.0% |
| expected_move_3d_points | 14 | volatility | 2,023 | 81 | 58.0% | 39.1% | 18.9% |
| expected_move_3d_points | 14 | volatility | 2,024 | 245 | 31.0% | 27.3% | 3.8% |
| expected_move_3d_points | 14 | volatility | 2,025 | 246 | 41.9% | 38.0% | 3.9% |
| expected_move_3d_points | 14 | volatility | 2,026 | 132 | 50.0% | 49.2% | 0.8% |
| expected_move_3d_points | 30 | volatility | 2,023 | 81 | 58.0% | 39.7% | 18.3% |
| expected_move_3d_points | 30 | volatility | 2,024 | 245 | 31.4% | 28.3% | 3.1% |
| expected_move_3d_points | 30 | volatility | 2,025 | 246 | 39.0% | 39.2% | -0.1% |
| expected_move_3d_points | 30 | volatility | 2,026 | 116 | 54.3% | 51.0% | 3.3% |
| forecast_rv_3d | 3 | volatility | 2,023 | 81 | 44.4% | 39.4% | 5.1% |
| forecast_rv_3d | 3 | volatility | 2,024 | 245 | 27.3% | 23.6% | 3.8% |
| forecast_rv_3d | 3 | volatility | 2,025 | 246 | 37.4% | 35.4% | 2.0% |
| forecast_rv_3d | 3 | volatility | 2,026 | 143 | 41.3% | 39.8% | 1.5% |
| forecast_rv_3d | 7 | volatility | 2,023 | 81 | 50.6% | 36.9% | 13.8% |
| forecast_rv_3d | 7 | volatility | 2,024 | 245 | 28.2% | 26.0% | 2.1% |
| forecast_rv_3d | 7 | volatility | 2,025 | 246 | 40.2% | 37.4% | 2.9% |
| forecast_rv_3d | 7 | volatility | 2,026 | 139 | 44.6% | 45.6% | -1.0% |
| forecast_rv_3d | 14 | volatility | 2,023 | 81 | 58.0% | 39.1% | 18.9% |
| forecast_rv_3d | 14 | volatility | 2,024 | 245 | 31.0% | 27.3% | 3.8% |
| forecast_rv_3d | 14 | volatility | 2,025 | 246 | 41.9% | 38.0% | 3.9% |
| forecast_rv_3d | 14 | volatility | 2,026 | 132 | 50.0% | 49.2% | 0.8% |
| forecast_rv_3d | 30 | volatility | 2,023 | 81 | 58.0% | 39.7% | 18.3% |
| forecast_rv_3d | 30 | volatility | 2,024 | 245 | 31.4% | 28.3% | 3.1% |
| forecast_rv_3d | 30 | volatility | 2,025 | 246 | 39.0% | 39.2% | -0.1% |
| forecast_rv_3d | 30 | volatility | 2,026 | 116 | 54.3% | 51.0% | 3.3% |
| gap_share_20 | 3 | volatility | 2,023 | 81 | 34.6% | 32.4% | 2.1% |
| gap_share_20 | 3 | volatility | 2,024 | 245 | 33.5% | 30.5% | 3.0% |
| gap_share_20 | 3 | volatility | 2,025 | 246 | 32.5% | 36.0% | -3.4% |
| gap_share_20 | 3 | volatility | 2,026 | 143 | 37.8% | 31.8% | 5.9% |
| gap_share_20 | 7 | volatility | 2,023 | 81 | 35.8% | 34.7% | 1.1% |
| gap_share_20 | 7 | volatility | 2,024 | 245 | 35.1% | 29.6% | 5.5% |
| gap_share_20 | 7 | volatility | 2,025 | 246 | 29.7% | 33.2% | -3.5% |
| gap_share_20 | 7 | volatility | 2,026 | 139 | 36.7% | 26.8% | 9.9% |
| gap_share_20 | 14 | volatility | 2,023 | 81 | 22.2% | 33.7% | -11.5% |
| gap_share_20 | 14 | volatility | 2,024 | 245 | 31.0% | 28.5% | 2.5% |
| gap_share_20 | 14 | volatility | 2,025 | 246 | 26.4% | 32.1% | -5.7% |
| gap_share_20 | 14 | volatility | 2,026 | 132 | 28.8% | 23.0% | 5.8% |
| gap_share_20 | 30 | volatility | 2,023 | 81 | 23.5% | 34.0% | -10.5% |
| gap_share_20 | 30 | volatility | 2,024 | 245 | 28.2% | 27.6% | 0.5% |
| gap_share_20 | 30 | volatility | 2,025 | 246 | 18.7% | 30.8% | -12.1% |
| gap_share_20 | 30 | volatility | 2,026 | 116 | 22.4% | 22.6% | -0.2% |
| har_rv_3d | 3 | volatility | 2,024 | 223 | 27.8% | 22.9% | 4.9% |
| har_rv_3d | 3 | volatility | 2,025 | 246 | 37.4% | 35.4% | 2.0% |
| har_rv_3d | 3 | volatility | 2,026 | 143 | 41.3% | 39.8% | 1.5% |
| har_rv_3d | 7 | volatility | 2,024 | 223 | 29.6% | 25.3% | 4.3% |
| har_rv_3d | 7 | volatility | 2,025 | 246 | 40.2% | 37.4% | 2.9% |
| har_rv_3d | 7 | volatility | 2,026 | 139 | 44.6% | 45.6% | -1.0% |
| har_rv_3d | 14 | volatility | 2,024 | 223 | 32.3% | 27.2% | 5.1% |
| har_rv_3d | 14 | volatility | 2,025 | 246 | 41.9% | 38.0% | 3.9% |
| har_rv_3d | 14 | volatility | 2,026 | 132 | 50.0% | 49.2% | 0.8% |
| har_rv_3d | 30 | volatility | 2,024 | 223 | 31.4% | 28.8% | 2.6% |
| har_rv_3d | 30 | volatility | 2,025 | 246 | 39.0% | 39.2% | -0.1% |
| har_rv_3d | 30 | volatility | 2,026 | 116 | 54.3% | 51.0% | 3.3% |
| local_global_stress_spread | 3 | volatility | 2,024 | 227 | 47.1% | 47.8% | -0.7% |
| local_global_stress_spread | 3 | volatility | 2,025 | 246 | 50.0% | 46.5% | 3.5% |
| local_global_stress_spread | 3 | volatility | 2,026 | 143 | 34.3% | 31.4% | 2.8% |
| local_global_stress_spread | 7 | volatility | 2,024 | 227 | 46.7% | 45.5% | 1.2% |
| local_global_stress_spread | 7 | volatility | 2,025 | 246 | 50.4% | 46.0% | 4.4% |
| local_global_stress_spread | 7 | volatility | 2,026 | 139 | 39.6% | 38.0% | 1.6% |
| local_global_stress_spread | 14 | volatility | 2,024 | 227 | 47.6% | 43.7% | 3.9% |
| local_global_stress_spread | 14 | volatility | 2,025 | 246 | 36.2% | 42.2% | -6.0% |
| local_global_stress_spread | 14 | volatility | 2,026 | 132 | 44.7% | 48.2% | -3.5% |
| local_global_stress_spread | 30 | volatility | 2,024 | 227 | 47.1% | 40.9% | 6.3% |
| local_global_stress_spread | 30 | volatility | 2,025 | 246 | 36.2% | 43.4% | -7.2% |
| local_global_stress_spread | 30 | volatility | 2,026 | 116 | 44.0% | 44.4% | -0.4% |
| matched_vrp_3d | 3 | volatility | 2,024 | 223 | 22.4% | 22.4% | 0.0% |
| matched_vrp_3d | 3 | volatility | 2,025 | 246 | 25.2% | 25.2% | 0.0% |
| matched_vrp_3d | 3 | volatility | 2,026 | 143 | 25.9% | 25.9% | 0.0% |
| matched_vrp_3d | 7 | volatility | 2,024 | 223 | 29.6% | 29.6% | 0.0% |
| matched_vrp_3d | 7 | volatility | 2,025 | 246 | 43.9% | 43.9% | 0.0% |
| matched_vrp_3d | 7 | volatility | 2,026 | 139 | 33.8% | 33.8% | 0.0% |
| matched_vrp_3d | 14 | volatility | 2,024 | 223 | 38.6% | 38.6% | 0.0% |
| matched_vrp_3d | 14 | volatility | 2,025 | 246 | 54.5% | 54.5% | 0.0% |
| matched_vrp_3d | 14 | volatility | 2,026 | 132 | 47.7% | 47.7% | 0.0% |
| matched_vrp_3d | 30 | volatility | 2,024 | 223 | 45.3% | 45.3% | 0.0% |
| matched_vrp_3d | 30 | volatility | 2,025 | 246 | 63.4% | 63.4% | 0.0% |
| matched_vrp_3d | 30 | volatility | 2,026 | 116 | 41.4% | 41.4% | 0.0% |
| range_position_20 | 3 | volatility | 2,023 | 81 | 4.9% | 4.9% | 0.0% |
| range_position_20 | 3 | volatility | 2,024 | 245 | 4.5% | 4.5% | 0.0% |
| range_position_20 | 3 | volatility | 2,025 | 246 | 4.5% | 4.5% | 0.0% |
| range_position_20 | 3 | volatility | 2,026 | 143 | 0.0% | 0.0% | 0.0% |
| range_position_20 | 7 | volatility | 2,023 | 81 | 7.4% | 7.4% | 0.0% |
| range_position_20 | 7 | volatility | 2,024 | 245 | 7.3% | 7.3% | 0.0% |
| range_position_20 | 7 | volatility | 2,025 | 246 | 4.1% | 4.1% | 0.0% |
| range_position_20 | 7 | volatility | 2,026 | 139 | 8.6% | 8.6% | 0.0% |
| range_position_20 | 14 | volatility | 2,023 | 81 | 2.5% | 2.5% | 0.0% |
| range_position_20 | 14 | volatility | 2,024 | 245 | 6.9% | 6.9% | 0.0% |
| range_position_20 | 14 | volatility | 2,025 | 246 | 9.3% | 9.3% | 0.0% |
| range_position_20 | 14 | volatility | 2,026 | 132 | 3.8% | 3.8% | 0.0% |
| range_position_20 | 30 | volatility | 2,023 | 81 | 3.7% | 3.7% | 0.0% |
| range_position_20 | 30 | volatility | 2,024 | 245 | 8.2% | 8.2% | 0.0% |
| range_position_20 | 30 | volatility | 2,025 | 246 | 6.9% | 6.9% | 0.0% |
| range_position_20 | 30 | volatility | 2,026 | 116 | 5.2% | 5.2% | 0.0% |
| reversal_5_vol_scaled | 3 | market | 2,023 | 36 | 50.0% | 47.0% | 3.0% |
| reversal_5_vol_scaled | 3 | market | 2,024 | 118 | 52.5% | 45.2% | 7.4% |
| reversal_5_vol_scaled | 3 | market | 2,025 | 137 | 43.8% | 43.1% | 0.7% |
| reversal_5_vol_scaled | 3 | market | 2,026 | 76 | 60.5% | 48.4% | 12.2% |
| reversal_5_vol_scaled | 3 | volatility | 2,023 | 81 | 4.9% | 4.9% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | 2,024 | 245 | 4.5% | 4.5% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | 2,025 | 246 | 4.5% | 4.5% | 0.0% |
| reversal_5_vol_scaled | 3 | volatility | 2,026 | 143 | 0.0% | 0.0% | 0.0% |
| reversal_5_vol_scaled | 7 | market | 2,023 | 36 | 50.0% | 47.4% | 2.6% |
| reversal_5_vol_scaled | 7 | market | 2,024 | 118 | 55.1% | 46.0% | 9.1% |
| reversal_5_vol_scaled | 7 | market | 2,025 | 137 | 54.0% | 43.4% | 10.6% |
| reversal_5_vol_scaled | 7 | market | 2,026 | 74 | 62.2% | 49.1% | 13.0% |
| reversal_5_vol_scaled | 7 | volatility | 2,023 | 81 | 7.4% | 7.4% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 2,024 | 245 | 7.3% | 7.3% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 2,025 | 246 | 4.1% | 4.1% | 0.0% |
| reversal_5_vol_scaled | 7 | volatility | 2,026 | 139 | 8.6% | 8.6% | 0.0% |
| reversal_5_vol_scaled | 14 | market | 2,023 | 36 | 44.4% | 46.3% | -1.9% |
| reversal_5_vol_scaled | 14 | market | 2,024 | 118 | 49.2% | 41.0% | 8.1% |
| reversal_5_vol_scaled | 14 | market | 2,025 | 137 | 40.9% | 36.7% | 4.2% |
| reversal_5_vol_scaled | 14 | market | 2,026 | 70 | 40.0% | 45.9% | -5.9% |
| reversal_5_vol_scaled | 14 | volatility | 2,023 | 81 | 2.5% | 2.5% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 2,024 | 245 | 6.9% | 6.9% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 2,025 | 246 | 9.3% | 9.3% | 0.0% |
| reversal_5_vol_scaled | 14 | volatility | 2,026 | 132 | 3.8% | 3.8% | 0.0% |
| reversal_5_vol_scaled | 30 | market | 2,023 | 36 | 50.0% | 54.1% | -4.1% |
| reversal_5_vol_scaled | 30 | market | 2,024 | 118 | 39.8% | 36.9% | 2.9% |
| reversal_5_vol_scaled | 30 | market | 2,025 | 137 | 38.0% | 35.7% | 2.3% |
| reversal_5_vol_scaled | 30 | market | 2,026 | 60 | 40.0% | 46.4% | -6.4% |
| reversal_5_vol_scaled | 30 | volatility | 2,023 | 81 | 3.7% | 3.7% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 2,024 | 245 | 8.2% | 8.2% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 2,025 | 246 | 6.9% | 6.9% | 0.0% |
| reversal_5_vol_scaled | 30 | volatility | 2,026 | 116 | 5.2% | 5.2% | 0.0% |
| rs_range_5_20 | 3 | volatility | 2,023 | 81 | 50.6% | 50.9% | -0.3% |
| rs_range_5_20 | 3 | volatility | 2,024 | 245 | 42.4% | 41.8% | 0.7% |
| rs_range_5_20 | 3 | volatility | 2,025 | 246 | 45.1% | 41.1% | 4.0% |
| rs_range_5_20 | 3 | volatility | 2,026 | 143 | 50.3% | 42.9% | 7.5% |
| rs_range_5_20 | 7 | volatility | 2,023 | 81 | 53.1% | 47.3% | 5.8% |
| rs_range_5_20 | 7 | volatility | 2,024 | 245 | 41.2% | 40.3% | 1.0% |
| rs_range_5_20 | 7 | volatility | 2,025 | 246 | 55.3% | 42.7% | 12.6% |
| rs_range_5_20 | 7 | volatility | 2,026 | 139 | 38.8% | 40.9% | -2.0% |
| rs_range_5_20 | 14 | volatility | 2,023 | 81 | 45.7% | 51.4% | -5.7% |
| rs_range_5_20 | 14 | volatility | 2,024 | 245 | 42.0% | 39.5% | 2.6% |
| rs_range_5_20 | 14 | volatility | 2,025 | 246 | 53.3% | 42.6% | 10.6% |
| rs_range_5_20 | 14 | volatility | 2,026 | 132 | 40.9% | 41.9% | -1.0% |
| rs_range_5_20 | 30 | volatility | 2,023 | 81 | 46.9% | 52.0% | -5.1% |
| rs_range_5_20 | 30 | volatility | 2,024 | 245 | 43.3% | 38.4% | 4.9% |
| rs_range_5_20 | 30 | volatility | 2,025 | 246 | 54.9% | 43.5% | 11.4% |
| rs_range_5_20 | 30 | volatility | 2,026 | 116 | 48.3% | 46.1% | 2.2% |
| rv_20_60_ratio | 3 | volatility | 2,023 | 41 | 61.0% | 62.4% | -1.4% |
| rv_20_60_ratio | 3 | volatility | 2,024 | 245 | 47.8% | 48.1% | -0.3% |
| rv_20_60_ratio | 3 | volatility | 2,025 | 246 | 44.7% | 42.0% | 2.7% |
| rv_20_60_ratio | 3 | volatility | 2,026 | 143 | 39.9% | 36.2% | 3.7% |
| rv_20_60_ratio | 7 | volatility | 2,023 | 41 | 61.0% | 62.4% | -1.4% |
| rv_20_60_ratio | 7 | volatility | 2,024 | 245 | 40.8% | 41.7% | -0.9% |
| rv_20_60_ratio | 7 | volatility | 2,025 | 246 | 36.2% | 32.2% | 3.9% |
| rv_20_60_ratio | 7 | volatility | 2,026 | 139 | 26.6% | 25.2% | 1.4% |
| rv_20_60_ratio | 14 | volatility | 2,023 | 41 | 73.2% | 73.2% | 0.0% |
| rv_20_60_ratio | 14 | volatility | 2,024 | 245 | 34.7% | 36.5% | -1.8% |
| rv_20_60_ratio | 14 | volatility | 2,025 | 246 | 28.0% | 26.7% | 1.4% |
| rv_20_60_ratio | 14 | volatility | 2,026 | 132 | 19.7% | 23.5% | -3.8% |
| rv_20_60_ratio | 30 | volatility | 2,023 | 41 | 78.0% | 78.0% | 0.0% |
| rv_20_60_ratio | 30 | volatility | 2,024 | 245 | 28.6% | 32.7% | -4.1% |
| rv_20_60_ratio | 30 | volatility | 2,025 | 246 | 19.9% | 23.0% | -3.1% |
| rv_20_60_ratio | 30 | volatility | 2,026 | 116 | 13.8% | 18.2% | -4.4% |
| rv_acceleration | 3 | volatility | 2,023 | 81 | 60.5% | 51.3% | 9.2% |
| rv_acceleration | 3 | volatility | 2,024 | 245 | 50.2% | 54.3% | -4.1% |
| rv_acceleration | 3 | volatility | 2,025 | 246 | 56.9% | 53.5% | 3.4% |
| rv_acceleration | 3 | volatility | 2,026 | 143 | 56.6% | 55.1% | 1.5% |
| rv_acceleration | 7 | volatility | 2,023 | 81 | 67.9% | 49.3% | 18.6% |
| rv_acceleration | 7 | volatility | 2,024 | 245 | 42.9% | 49.9% | -7.1% |
| rv_acceleration | 7 | volatility | 2,025 | 246 | 45.9% | 45.8% | 0.1% |
| rv_acceleration | 7 | volatility | 2,026 | 139 | 47.5% | 48.3% | -0.8% |
| rv_acceleration | 14 | volatility | 2,023 | 81 | 70.4% | 53.1% | 17.3% |
| rv_acceleration | 14 | volatility | 2,024 | 245 | 49.8% | 47.2% | 2.6% |
| rv_acceleration | 14 | volatility | 2,025 | 246 | 41.9% | 37.6% | 4.3% |
| rv_acceleration | 14 | volatility | 2,026 | 132 | 46.2% | 45.5% | 0.7% |
| rv_acceleration | 30 | volatility | 2,023 | 81 | 70.4% | 53.5% | 16.9% |
| rv_acceleration | 30 | volatility | 2,024 | 245 | 42.4% | 44.2% | -1.8% |
| rv_acceleration | 30 | volatility | 2,025 | 246 | 42.7% | 35.7% | 7.0% |
| rv_acceleration | 30 | volatility | 2,026 | 116 | 56.0% | 48.1% | 8.0% |
| trend_efficiency_20 | 3 | volatility | 2,023 | 81 | 40.7% | 28.7% | 12.0% |
| trend_efficiency_20 | 3 | volatility | 2,024 | 245 | 24.1% | 25.3% | -1.2% |
| trend_efficiency_20 | 3 | volatility | 2,025 | 246 | 32.5% | 32.0% | 0.5% |
| trend_efficiency_20 | 3 | volatility | 2,026 | 143 | 31.5% | 26.3% | 5.2% |
| trend_efficiency_20 | 7 | volatility | 2,023 | 81 | 50.6% | 32.0% | 18.6% |
| trend_efficiency_20 | 7 | volatility | 2,024 | 245 | 32.2% | 29.5% | 2.7% |
| trend_efficiency_20 | 7 | volatility | 2,025 | 246 | 30.9% | 33.2% | -2.3% |
| trend_efficiency_20 | 7 | volatility | 2,026 | 139 | 34.5% | 28.9% | 5.6% |
| trend_efficiency_20 | 14 | volatility | 2,023 | 81 | 43.2% | 29.6% | 13.7% |
| trend_efficiency_20 | 14 | volatility | 2,024 | 245 | 30.2% | 33.4% | -3.2% |
| trend_efficiency_20 | 14 | volatility | 2,025 | 246 | 34.1% | 32.9% | 1.2% |
| trend_efficiency_20 | 14 | volatility | 2,026 | 132 | 34.8% | 33.1% | 1.8% |
| trend_efficiency_20 | 30 | volatility | 2,023 | 81 | 45.7% | 29.1% | 16.6% |
| trend_efficiency_20 | 30 | volatility | 2,024 | 245 | 36.7% | 36.1% | 0.7% |
| trend_efficiency_20 | 30 | volatility | 2,025 | 246 | 42.7% | 34.6% | 8.1% |
| trend_efficiency_20 | 30 | volatility | 2,026 | 116 | 25.0% | 26.5% | -1.5% |
| usdils_change_5d | 3 | market | 2,023 | 89 | 64.0% | 55.2% | 8.9% |
| usdils_change_5d | 3 | market | 2,024 | 202 | 45.5% | 49.6% | -4.0% |
| usdils_change_5d | 3 | market | 2,025 | 213 | 53.1% | 51.2% | 1.8% |
| usdils_change_5d | 3 | market | 2,026 | 126 | 46.8% | 50.3% | -3.5% |
| usdils_change_5d | 3 | volatility | 2,023 | 81 | 54.3% | 42.3% | 12.0% |
| usdils_change_5d | 3 | volatility | 2,024 | 245 | 43.3% | 39.4% | 3.9% |
| usdils_change_5d | 3 | volatility | 2,025 | 246 | 46.7% | 44.3% | 2.4% |
| usdils_change_5d | 3 | volatility | 2,026 | 143 | 49.7% | 47.6% | 2.1% |
| usdils_change_5d | 7 | market | 2,023 | 89 | 65.2% | 55.2% | 9.9% |
| usdils_change_5d | 7 | market | 2,024 | 202 | 45.5% | 49.8% | -4.3% |
| usdils_change_5d | 7 | market | 2,025 | 213 | 48.8% | 52.4% | -3.6% |
| usdils_change_5d | 7 | market | 2,026 | 123 | 41.5% | 50.2% | -8.7% |
| usdils_change_5d | 7 | volatility | 2,023 | 81 | 53.1% | 43.0% | 10.1% |
| usdils_change_5d | 7 | volatility | 2,024 | 245 | 46.5% | 39.4% | 7.1% |
| usdils_change_5d | 7 | volatility | 2,025 | 246 | 43.1% | 40.2% | 2.9% |
| usdils_change_5d | 7 | volatility | 2,026 | 139 | 46.0% | 45.3% | 0.8% |
| usdils_change_5d | 14 | market | 2,023 | 89 | 61.8% | 51.4% | 10.4% |
| usdils_change_5d | 14 | market | 2,024 | 202 | 48.5% | 48.7% | -0.1% |
| usdils_change_5d | 14 | market | 2,025 | 213 | 55.9% | 54.5% | 1.4% |
| usdils_change_5d | 14 | market | 2,026 | 116 | 54.3% | 51.1% | 3.2% |
| usdils_change_5d | 14 | volatility | 2,023 | 81 | 56.8% | 47.4% | 9.4% |
| usdils_change_5d | 14 | volatility | 2,024 | 245 | 46.1% | 40.4% | 5.7% |
| usdils_change_5d | 14 | volatility | 2,025 | 246 | 45.5% | 35.6% | 9.9% |
| usdils_change_5d | 14 | volatility | 2,026 | 132 | 46.2% | 45.6% | 0.6% |
| usdils_change_5d | 30 | market | 2,023 | 89 | 62.9% | 47.4% | 15.6% |
| usdils_change_5d | 30 | market | 2,024 | 202 | 47.0% | 48.2% | -1.2% |
| usdils_change_5d | 30 | market | 2,025 | 213 | 53.1% | 54.7% | -1.7% |
| usdils_change_5d | 30 | market | 2,026 | 101 | 43.6% | 50.7% | -7.1% |
| usdils_change_5d | 30 | volatility | 2,023 | 81 | 58.0% | 49.3% | 8.7% |
| usdils_change_5d | 30 | volatility | 2,024 | 245 | 49.0% | 40.8% | 8.2% |
| usdils_change_5d | 30 | volatility | 2,025 | 246 | 44.3% | 34.7% | 9.6% |
| usdils_change_5d | 30 | volatility | 2,026 | 116 | 38.8% | 44.1% | -5.3% |
| vix9d_vix_ratio | 3 | market | 2,023 | 74 | 54.1% | 56.6% | -2.6% |
| vix9d_vix_ratio | 3 | market | 2,024 | 209 | 56.5% | 56.6% | -0.2% |
| vix9d_vix_ratio | 3 | market | 2,025 | 226 | 63.7% | 61.5% | 2.2% |
| vix9d_vix_ratio | 3 | market | 2,026 | 126 | 55.6% | 51.9% | 3.6% |
| vix9d_vix_ratio | 3 | volatility | 2,023 | 81 | 45.7% | 43.5% | 2.1% |
| vix9d_vix_ratio | 3 | volatility | 2,024 | 245 | 56.3% | 54.5% | 1.8% |
| vix9d_vix_ratio | 3 | volatility | 2,025 | 246 | 58.9% | 57.2% | 1.7% |
| vix9d_vix_ratio | 3 | volatility | 2,026 | 143 | 60.1% | 56.2% | 3.9% |
| vix9d_vix_ratio | 7 | market | 2,023 | 74 | 54.1% | 55.0% | -1.0% |
| vix9d_vix_ratio | 7 | market | 2,024 | 209 | 53.6% | 57.2% | -3.6% |
| vix9d_vix_ratio | 7 | market | 2,025 | 226 | 64.2% | 63.1% | 1.0% |
| vix9d_vix_ratio | 7 | market | 2,026 | 123 | 55.3% | 54.8% | 0.5% |
| vix9d_vix_ratio | 7 | volatility | 2,023 | 81 | 40.7% | 38.6% | 2.2% |
| vix9d_vix_ratio | 7 | volatility | 2,024 | 245 | 54.3% | 48.3% | 6.0% |
| vix9d_vix_ratio | 7 | volatility | 2,025 | 246 | 46.3% | 41.5% | 4.8% |
| vix9d_vix_ratio | 7 | volatility | 2,026 | 139 | 51.1% | 43.6% | 7.5% |
| vix9d_vix_ratio | 14 | market | 2,023 | 74 | 58.1% | 55.7% | 2.4% |
| vix9d_vix_ratio | 14 | market | 2,024 | 209 | 53.6% | 63.2% | -9.6% |
| vix9d_vix_ratio | 14 | market | 2,025 | 226 | 70.8% | 69.3% | 1.5% |
| vix9d_vix_ratio | 14 | market | 2,026 | 116 | 59.5% | 56.3% | 3.2% |
| vix9d_vix_ratio | 14 | volatility | 2,023 | 81 | 50.6% | 44.5% | 6.2% |
| vix9d_vix_ratio | 14 | volatility | 2,024 | 245 | 49.8% | 43.9% | 5.8% |
| vix9d_vix_ratio | 14 | volatility | 2,025 | 246 | 37.0% | 29.8% | 7.2% |
| vix9d_vix_ratio | 14 | volatility | 2,026 | 132 | 43.2% | 36.2% | 7.0% |
| vix9d_vix_ratio | 30 | market | 2,023 | 74 | 50.0% | 47.2% | 2.8% |
| vix9d_vix_ratio | 30 | market | 2,024 | 209 | 72.2% | 73.4% | -1.2% |
| vix9d_vix_ratio | 30 | market | 2,025 | 226 | 71.7% | 73.7% | -2.0% |
| vix9d_vix_ratio | 30 | market | 2,026 | 100 | 42.0% | 50.5% | -8.5% |
| vix9d_vix_ratio | 30 | volatility | 2,023 | 81 | 51.9% | 46.6% | 5.3% |
| vix9d_vix_ratio | 30 | volatility | 2,024 | 245 | 42.4% | 40.3% | 2.2% |
| vix9d_vix_ratio | 30 | volatility | 2,025 | 246 | 26.8% | 23.9% | 3.0% |
| vix9d_vix_ratio | 30 | volatility | 2,026 | 116 | 36.2% | 38.0% | -1.8% |
| vix_curve_ratio | 3 | market | 2,023 | 98 | 50.0% | 50.0% | 0.0% |
| vix_curve_ratio | 3 | market | 2,024 | 240 | 55.8% | 58.3% | -2.5% |
| vix_curve_ratio | 3 | market | 2,025 | 241 | 62.7% | 61.5% | 1.2% |
| vix_curve_ratio | 3 | market | 2,026 | 136 | 55.1% | 52.7% | 2.4% |
| vix_curve_ratio | 3 | volatility | 2,023 | 81 | 66.7% | 65.4% | 1.3% |
| vix_curve_ratio | 3 | volatility | 2,024 | 245 | 70.2% | 67.7% | 2.5% |
| vix_curve_ratio | 3 | volatility | 2,025 | 246 | 63.8% | 61.5% | 2.3% |
| vix_curve_ratio | 3 | volatility | 2,026 | 143 | 69.2% | 63.4% | 5.8% |
| vix_curve_ratio | 7 | market | 2,023 | 98 | 54.1% | 54.1% | 0.0% |
| vix_curve_ratio | 7 | market | 2,024 | 240 | 54.2% | 58.0% | -3.9% |
| vix_curve_ratio | 7 | market | 2,025 | 241 | 63.1% | 64.5% | -1.5% |
| vix_curve_ratio | 7 | market | 2,026 | 132 | 53.8% | 54.9% | -1.1% |
| vix_curve_ratio | 7 | volatility | 2,023 | 81 | 55.6% | 54.9% | 0.6% |
| vix_curve_ratio | 7 | volatility | 2,024 | 245 | 63.7% | 58.8% | 4.8% |
| vix_curve_ratio | 7 | volatility | 2,025 | 246 | 48.0% | 44.6% | 3.4% |
| vix_curve_ratio | 7 | volatility | 2,026 | 139 | 54.0% | 48.3% | 5.7% |
| vix_curve_ratio | 14 | market | 2,023 | 98 | 59.2% | 59.2% | 0.0% |
| vix_curve_ratio | 14 | market | 2,024 | 240 | 64.2% | 68.0% | -3.9% |
| vix_curve_ratio | 14 | market | 2,025 | 241 | 72.2% | 70.7% | 1.5% |
| vix_curve_ratio | 14 | market | 2,026 | 125 | 58.4% | 56.8% | 1.6% |
| vix_curve_ratio | 14 | volatility | 2,023 | 81 | 67.9% | 66.7% | 1.2% |
| vix_curve_ratio | 14 | volatility | 2,024 | 245 | 57.6% | 52.7% | 4.8% |
| vix_curve_ratio | 14 | volatility | 2,025 | 246 | 37.0% | 31.6% | 5.3% |
| vix_curve_ratio | 14 | volatility | 2,026 | 132 | 43.9% | 40.1% | 3.8% |
| vix_curve_ratio | 30 | market | 2,023 | 98 | 53.1% | 53.1% | 0.0% |
| vix_curve_ratio | 30 | market | 2,024 | 240 | 81.7% | 82.0% | -0.3% |
| vix_curve_ratio | 30 | market | 2,025 | 241 | 72.6% | 73.9% | -1.2% |
| vix_curve_ratio | 30 | market | 2,026 | 109 | 45.0% | 52.1% | -7.2% |
| vix_curve_ratio | 30 | volatility | 2,023 | 81 | 70.4% | 69.2% | 1.2% |
| vix_curve_ratio | 30 | volatility | 2,024 | 245 | 50.2% | 47.1% | 3.1% |
| vix_curve_ratio | 30 | volatility | 2,025 | 246 | 28.5% | 25.3% | 3.2% |
| vix_curve_ratio | 30 | volatility | 2,026 | 116 | 42.2% | 42.6% | -0.3% |
| vix_vix3m_ratio | 3 | market | 2,023 | 101 | 51.5% | 51.5% | 0.0% |
| vix_vix3m_ratio | 3 | market | 2,024 | 228 | 56.1% | 57.6% | -1.4% |
| vix_vix3m_ratio | 3 | market | 2,025 | 232 | 62.5% | 63.6% | -1.1% |
| vix_vix3m_ratio | 3 | market | 2,026 | 132 | 53.0% | 53.6% | -0.5% |
| vix_vix3m_ratio | 3 | volatility | 2,023 | 81 | 67.9% | 67.9% | 0.0% |
| vix_vix3m_ratio | 3 | volatility | 2,024 | 245 | 69.0% | 66.8% | 2.2% |
| vix_vix3m_ratio | 3 | volatility | 2,025 | 246 | 61.4% | 61.1% | 0.3% |
| vix_vix3m_ratio | 3 | volatility | 2,026 | 143 | 67.8% | 65.7% | 2.2% |
| vix_vix3m_ratio | 7 | market | 2,023 | 101 | 53.5% | 53.5% | 0.0% |
| vix_vix3m_ratio | 7 | market | 2,024 | 228 | 56.6% | 57.8% | -1.2% |
| vix_vix3m_ratio | 7 | market | 2,025 | 232 | 63.4% | 66.0% | -2.6% |
| vix_vix3m_ratio | 7 | market | 2,026 | 128 | 52.3% | 54.7% | -2.3% |
| vix_vix3m_ratio | 7 | volatility | 2,023 | 81 | 56.8% | 56.8% | 0.0% |
| vix_vix3m_ratio | 7 | volatility | 2,024 | 245 | 61.2% | 57.9% | 3.3% |
| vix_vix3m_ratio | 7 | volatility | 2,025 | 246 | 44.7% | 43.9% | 0.8% |
| vix_vix3m_ratio | 7 | volatility | 2,026 | 139 | 53.2% | 50.4% | 2.9% |
| vix_vix3m_ratio | 14 | market | 2,023 | 101 | 58.4% | 58.4% | 0.0% |
| vix_vix3m_ratio | 14 | market | 2,024 | 228 | 67.1% | 68.3% | -1.2% |
| vix_vix3m_ratio | 14 | market | 2,025 | 232 | 73.7% | 72.1% | 1.6% |
| vix_vix3m_ratio | 14 | market | 2,026 | 121 | 57.9% | 58.3% | -0.4% |
| vix_vix3m_ratio | 14 | volatility | 2,023 | 81 | 69.1% | 69.1% | 0.0% |
| vix_vix3m_ratio | 14 | volatility | 2,024 | 245 | 52.7% | 51.6% | 1.0% |
| vix_vix3m_ratio | 14 | volatility | 2,025 | 246 | 33.7% | 30.7% | 3.1% |
| vix_vix3m_ratio | 14 | volatility | 2,026 | 132 | 41.7% | 41.0% | 0.6% |
| vix_vix3m_ratio | 30 | market | 2,023 | 101 | 52.5% | 52.5% | 0.0% |
| vix_vix3m_ratio | 30 | market | 2,024 | 228 | 84.6% | 84.9% | -0.2% |
| vix_vix3m_ratio | 30 | market | 2,025 | 232 | 75.9% | 76.2% | -0.4% |
| vix_vix3m_ratio | 30 | market | 2,026 | 105 | 48.6% | 51.5% | -3.0% |
| vix_vix3m_ratio | 30 | volatility | 2,023 | 81 | 71.6% | 71.6% | -0.0% |
| vix_vix3m_ratio | 30 | volatility | 2,024 | 245 | 48.2% | 46.1% | 2.1% |
| vix_vix3m_ratio | 30 | volatility | 2,025 | 246 | 28.0% | 24.3% | 3.8% |
| vix_vix3m_ratio | 30 | volatility | 2,026 | 116 | 44.8% | 44.8% | 0.1% |
| vrp_spread | 3 | volatility | 2,023 | 81 | 66.7% | 49.1% | 17.6% |
| vrp_spread | 3 | volatility | 2,024 | 245 | 29.8% | 25.4% | 4.3% |
| vrp_spread | 3 | volatility | 2,025 | 246 | 48.8% | 44.4% | 4.4% |
| vrp_spread | 3 | volatility | 2,026 | 143 | 48.3% | 47.9% | 0.3% |
| vrp_spread | 7 | volatility | 2,023 | 81 | 72.8% | 46.8% | 26.1% |
| vrp_spread | 7 | volatility | 2,024 | 245 | 37.1% | 31.7% | 5.4% |
| vrp_spread | 7 | volatility | 2,025 | 246 | 61.4% | 55.1% | 6.2% |
| vrp_spread | 7 | volatility | 2,026 | 139 | 49.6% | 54.2% | -4.6% |
| vrp_spread | 14 | volatility | 2,023 | 81 | 71.6% | 45.2% | 26.4% |
| vrp_spread | 14 | volatility | 2,024 | 245 | 43.3% | 38.1% | 5.2% |
| vrp_spread | 14 | volatility | 2,025 | 246 | 59.3% | 58.0% | 1.4% |
| vrp_spread | 14 | volatility | 2,026 | 132 | 55.3% | 62.4% | -7.1% |
| vrp_spread | 30 | volatility | 2,023 | 81 | 67.9% | 41.8% | 26.1% |
| vrp_spread | 30 | volatility | 2,024 | 245 | 48.6% | 42.7% | 5.9% |
| vrp_spread | 30 | volatility | 2,025 | 246 | 61.8% | 63.9% | -2.1% |
| vrp_spread | 30 | volatility | 2,026 | 116 | 68.1% | 64.4% | 3.7% |
| vta35 | 3 | market | 2,023 | 38 | 60.5% | 63.8% | -3.3% |
| vta35 | 3 | market | 2,024 | 221 | 49.3% | 52.4% | -3.1% |
| vta35 | 3 | market | 2,025 | 212 | 49.5% | 50.0% | -0.5% |
| vta35 | 3 | market | 2,026 | 132 | 43.9% | 49.5% | -5.5% |
| vta35 | 3 | volatility | 2,023 | 42 | 50.0% | 52.1% | -2.1% |
| vta35 | 3 | volatility | 2,024 | 245 | 51.4% | 51.1% | 0.3% |
| vta35 | 3 | volatility | 2,025 | 246 | 49.2% | 40.9% | 8.3% |
| vta35 | 3 | volatility | 2,026 | 143 | 43.4% | 37.8% | 5.6% |
| vta35 | 7 | market | 2,023 | 38 | 68.4% | 67.1% | 1.3% |
| vta35 | 7 | market | 2,024 | 221 | 43.4% | 50.7% | -7.2% |
| vta35 | 7 | market | 2,025 | 212 | 42.0% | 50.2% | -8.2% |
| vta35 | 7 | market | 2,026 | 130 | 30.8% | 46.6% | -15.9% |
| vta35 | 7 | volatility | 2,023 | 42 | 50.0% | 52.1% | -2.1% |
| vta35 | 7 | volatility | 2,024 | 245 | 48.2% | 45.6% | 2.6% |
| vta35 | 7 | volatility | 2,025 | 246 | 51.2% | 38.5% | 12.7% |
| vta35 | 7 | volatility | 2,026 | 139 | 41.7% | 39.9% | 1.9% |
| vta35 | 14 | market | 2,023 | 38 | 63.2% | 67.8% | -4.6% |
| vta35 | 14 | market | 2,024 | 221 | 56.1% | 58.1% | -2.0% |
| vta35 | 14 | market | 2,025 | 212 | 42.5% | 50.5% | -8.0% |
| vta35 | 14 | market | 2,026 | 124 | 45.2% | 45.3% | -0.2% |
| vta35 | 14 | volatility | 2,023 | 42 | 61.9% | 61.9% | 0.0% |
| vta35 | 14 | volatility | 2,024 | 245 | 45.3% | 41.9% | 3.4% |
| vta35 | 14 | volatility | 2,025 | 246 | 45.5% | 35.9% | 9.6% |
| vta35 | 14 | volatility | 2,026 | 132 | 41.7% | 47.9% | -6.2% |
| vta35 | 30 | market | 2,023 | 38 | 55.3% | 55.3% | 0.0% |
| vta35 | 30 | market | 2,024 | 221 | 66.1% | 63.1% | 3.0% |
| vta35 | 30 | market | 2,025 | 212 | 52.4% | 50.1% | 2.2% |
| vta35 | 30 | market | 2,026 | 111 | 25.2% | 46.9% | -21.7% |
| vta35 | 30 | volatility | 2,023 | 42 | 66.7% | 66.7% | 0.0% |
| vta35 | 30 | volatility | 2,024 | 245 | 41.6% | 39.1% | 2.5% |
| vta35 | 30 | volatility | 2,025 | 246 | 41.1% | 35.2% | 5.8% |
| vta35 | 30 | volatility | 2,026 | 116 | 42.2% | 45.9% | -3.7% |
| vta35_change_5d | 3 | market | 2,023 | 93 | 41.9% | 50.1% | -8.2% |
| vta35_change_5d | 3 | market | 2,024 | 226 | 57.1% | 50.4% | 6.7% |
| vta35_change_5d | 3 | market | 2,025 | 225 | 50.7% | 51.5% | -0.9% |
| vta35_change_5d | 3 | market | 2,026 | 136 | 44.1% | 49.8% | -5.7% |
| vta35_change_5d | 3 | volatility | 2,023 | 81 | 49.4% | 49.1% | 0.3% |
| vta35_change_5d | 3 | volatility | 2,024 | 245 | 44.9% | 45.5% | -0.6% |
| vta35_change_5d | 3 | volatility | 2,025 | 246 | 52.4% | 47.1% | 5.3% |
| vta35_change_5d | 3 | volatility | 2,026 | 143 | 45.5% | 46.8% | -1.3% |
| vta35_change_5d | 7 | market | 2,023 | 93 | 44.1% | 49.7% | -5.6% |
| vta35_change_5d | 7 | market | 2,024 | 226 | 49.1% | 50.6% | -1.5% |
| vta35_change_5d | 7 | market | 2,025 | 225 | 52.0% | 51.7% | 0.3% |
| vta35_change_5d | 7 | market | 2,026 | 133 | 36.1% | 50.2% | -14.1% |
| vta35_change_5d | 7 | volatility | 2,023 | 81 | 46.9% | 45.1% | 1.8% |
| vta35_change_5d | 7 | volatility | 2,024 | 245 | 47.8% | 44.4% | 3.3% |
| vta35_change_5d | 7 | volatility | 2,025 | 246 | 58.5% | 48.8% | 9.8% |
| vta35_change_5d | 7 | volatility | 2,026 | 139 | 46.0% | 44.7% | 1.3% |
| vta35_change_5d | 14 | market | 2,023 | 93 | 52.7% | 50.0% | 2.7% |
| vta35_change_5d | 14 | market | 2,024 | 226 | 50.0% | 50.3% | -0.3% |
| vta35_change_5d | 14 | market | 2,025 | 225 | 49.3% | 51.4% | -2.1% |
| vta35_change_5d | 14 | market | 2,026 | 126 | 56.3% | 50.7% | 5.6% |
| vta35_change_5d | 14 | volatility | 2,023 | 81 | 51.9% | 49.5% | 2.3% |
| vta35_change_5d | 14 | volatility | 2,024 | 245 | 47.3% | 45.2% | 2.2% |
| vta35_change_5d | 14 | volatility | 2,025 | 246 | 54.5% | 46.7% | 7.8% |
| vta35_change_5d | 14 | volatility | 2,026 | 132 | 47.7% | 47.7% | 0.0% |
| vta35_change_5d | 30 | market | 2,023 | 93 | 48.4% | 49.8% | -1.4% |
| vta35_change_5d | 30 | market | 2,024 | 226 | 57.1% | 51.9% | 5.2% |
| vta35_change_5d | 30 | market | 2,025 | 225 | 53.8% | 52.5% | 1.3% |
| vta35_change_5d | 30 | market | 2,026 | 113 | 49.6% | 49.7% | -0.1% |
| vta35_change_5d | 30 | volatility | 2,023 | 81 | 51.9% | 49.5% | 2.3% |
| vta35_change_5d | 30 | volatility | 2,024 | 245 | 48.2% | 45.2% | 2.9% |
| vta35_change_5d | 30 | volatility | 2,025 | 246 | 50.8% | 48.3% | 2.5% |
| vta35_change_5d | 30 | volatility | 2,026 | 116 | 44.8% | 50.9% | -6.0% |
| vta35_zscore_60 | 3 | market | 2,023 | 38 | 60.5% | 63.8% | -3.3% |
| vta35_zscore_60 | 3 | market | 2,024 | 221 | 49.3% | 52.4% | -3.1% |
| vta35_zscore_60 | 3 | market | 2,025 | 212 | 49.5% | 50.0% | -0.5% |
| vta35_zscore_60 | 3 | market | 2,026 | 132 | 43.9% | 49.5% | -5.5% |
| vta35_zscore_60 | 3 | volatility | 2,023 | 42 | 50.0% | 52.1% | -2.1% |
| vta35_zscore_60 | 3 | volatility | 2,024 | 245 | 51.4% | 51.1% | 0.3% |
| vta35_zscore_60 | 3 | volatility | 2,025 | 246 | 49.2% | 40.9% | 8.3% |
| vta35_zscore_60 | 3 | volatility | 2,026 | 143 | 43.4% | 37.8% | 5.6% |
| vta35_zscore_60 | 7 | market | 2,023 | 38 | 68.4% | 67.1% | 1.3% |
| vta35_zscore_60 | 7 | market | 2,024 | 221 | 43.4% | 50.7% | -7.2% |
| vta35_zscore_60 | 7 | market | 2,025 | 212 | 42.0% | 50.2% | -8.2% |
| vta35_zscore_60 | 7 | market | 2,026 | 130 | 30.8% | 46.6% | -15.9% |
| vta35_zscore_60 | 7 | volatility | 2,023 | 42 | 50.0% | 52.1% | -2.1% |
| vta35_zscore_60 | 7 | volatility | 2,024 | 245 | 48.2% | 45.6% | 2.6% |
| vta35_zscore_60 | 7 | volatility | 2,025 | 246 | 51.2% | 38.5% | 12.7% |
| vta35_zscore_60 | 7 | volatility | 2,026 | 139 | 41.7% | 39.9% | 1.9% |
| vta35_zscore_60 | 14 | market | 2,023 | 38 | 63.2% | 67.8% | -4.6% |
| vta35_zscore_60 | 14 | market | 2,024 | 221 | 56.1% | 58.1% | -2.0% |
| vta35_zscore_60 | 14 | market | 2,025 | 212 | 42.5% | 50.5% | -8.0% |
| vta35_zscore_60 | 14 | market | 2,026 | 124 | 45.2% | 45.3% | -0.2% |
| vta35_zscore_60 | 14 | volatility | 2,023 | 42 | 61.9% | 61.9% | 0.0% |
| vta35_zscore_60 | 14 | volatility | 2,024 | 245 | 45.3% | 41.9% | 3.4% |
| vta35_zscore_60 | 14 | volatility | 2,025 | 246 | 45.5% | 35.9% | 9.6% |
| vta35_zscore_60 | 14 | volatility | 2,026 | 132 | 41.7% | 47.9% | -6.2% |
| vta35_zscore_60 | 30 | market | 2,023 | 38 | 55.3% | 55.3% | 0.0% |
| vta35_zscore_60 | 30 | market | 2,024 | 221 | 66.1% | 63.1% | 3.0% |
| vta35_zscore_60 | 30 | market | 2,025 | 212 | 52.4% | 50.1% | 2.2% |
| vta35_zscore_60 | 30 | market | 2,026 | 111 | 25.2% | 46.9% | -21.7% |
| vta35_zscore_60 | 30 | volatility | 2,023 | 42 | 66.7% | 66.7% | 0.0% |
| vta35_zscore_60 | 30 | volatility | 2,024 | 245 | 41.6% | 39.1% | 2.5% |
| vta35_zscore_60 | 30 | volatility | 2,025 | 246 | 41.1% | 35.2% | 5.8% |
| vta35_zscore_60 | 30 | volatility | 2,026 | 116 | 42.2% | 45.9% | -3.7% |
| vta_vol_of_vol_20 | 3 | volatility | 2,023 | 81 | 27.2% | 27.2% | 0.0% |
| vta_vol_of_vol_20 | 3 | volatility | 2,024 | 245 | 20.0% | 20.5% | -0.5% |
| vta_vol_of_vol_20 | 3 | volatility | 2,025 | 246 | 24.0% | 23.3% | 0.7% |
| vta_vol_of_vol_20 | 3 | volatility | 2,026 | 143 | 25.9% | 25.9% | 0.0% |
| vta_vol_of_vol_20 | 7 | volatility | 2,023 | 81 | 35.8% | 35.8% | -0.0% |
| vta_vol_of_vol_20 | 7 | volatility | 2,024 | 245 | 30.6% | 26.7% | 3.9% |
| vta_vol_of_vol_20 | 7 | volatility | 2,025 | 246 | 42.3% | 40.1% | 2.2% |
| vta_vol_of_vol_20 | 7 | volatility | 2,026 | 139 | 33.8% | 33.8% | 0.0% |
| vta_vol_of_vol_20 | 14 | volatility | 2,023 | 81 | 28.4% | 28.4% | 0.0% |
| vta_vol_of_vol_20 | 14 | volatility | 2,024 | 245 | 37.6% | 32.6% | 5.0% |
| vta_vol_of_vol_20 | 14 | volatility | 2,025 | 246 | 50.8% | 49.2% | 1.6% |
| vta_vol_of_vol_20 | 14 | volatility | 2,026 | 132 | 47.7% | 47.7% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 2,023 | 81 | 24.7% | 24.7% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 2,024 | 245 | 40.4% | 36.8% | 3.6% |
| vta_vol_of_vol_20 | 30 | volatility | 2,025 | 246 | 56.9% | 56.9% | 0.0% |
| vta_vol_of_vol_20 | 30 | volatility | 2,026 | 116 | 41.4% | 41.4% | 0.0% |

## Every strategy family: selected-rule performance versus unconditional baseline

| strategy | horizon | available_days | selected_n | selection_rate | successes | success_rate | unconditional_baseline | uplift | adjusted_success_rate | ci_low | ci_high | p_value | strength | mean_scenario_score | median_normalized_move | nonoverlap_n_min | n_eff | nonoverlap_success_rate_min | nonoverlap_success_rate | nonoverlap_success_rate_max | positive_years | tested_years | positive_regimes | tested_regimes | sample_quality | limitation | fdr_q |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Bear Call Spread | 3 | 730 | 62 | 8.5% | 33 | 53.2% | 58.5% | -5.3% | 54.5% | 41.0% | 65.1% | 0.6837 | 1 | 0.1804 | 0.4788 | 18 | 20 | 40.9% | 55.6% | 63.6% | 2 | 4 | 0 | 2 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Call Spread | 7 | 726 | 60 | 8.3% | 31 | 51.7% | 57.2% | -5.5% | 53.0% | 39.3% | 63.8% | 0.6233 | 1 | 0.1330 | 0.4081 | 6 | 8 | 28.6% | 54.5% | 70.0% | 1 | 4 | 0 | 2 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Call Spread | 14 | 719 | 59 | 8.2% | 31 | 52.5% | 49.9% | 2.6% | 51.9% | 40.0% | 64.7% | 0.4584 | 2 | 0.0880 | 0.4676 | 3 | 4 | 0.0% | 60.0% | 100.0% | 2 | 4 | 1 | 2 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Call Spread | 30 | 703 | 50 | 7.1% | 23 | 46.0% | 42.4% | 3.6% | 45.0% | 33.0% | 59.6% | 0.4709 | 2 | 0.2920 | 0.6828 | 1 | 1 | 0.0% | 50.0% | 100.0% | 2 | 3 | 2 | 2 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Put Spread | 3 | 730 | 45 | 6.2% | 17 | 37.8% | 40.7% | -2.9% | 38.7% | 25.1% | 52.4% | 0.5906 | 1 | -0.3912 | 0.4044 | 13 | 15 | 23.1% | 38.9% | 50.0% | 1 | 4 | 2 | 4 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Put Spread | 7 | 726 | 45 | 6.2% | 23 | 51.1% | 38.3% | 12.8% | 47.2% | 37.0% | 65.0% | 0.2592 | 3 | -0.1159 | -0.0358 | 4 | 6 | 36.4% | 50.0% | 75.0% | 3 | 4 | 3 | 4 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Put Spread | 14 | 719 | 44 | 6.1% | 22 | 50.0% | 30.7% | 19.3% | 44.0% | 35.8% | 64.2% | 0.2348 | 4 | -0.0073 | 0.0036 | 1 | 3 | 14.3% | 63.3% | 100.0% | 3 | 4 | 2 | 4 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bear Put Spread | 30 | 703 | 44 | 6.3% | 18 | 40.9% | 24.3% | 16.6% | 35.7% | 27.7% | 55.6% | 0.3495 | 4 | -0.4041 | 0.2717 | 1 | 1 | 0.0% | 50.0% | 100.0% | 2 | 4 | 3 | 4 | נמוכה | market-scenario proxy; no option P&L | 1.0000 |
| Bull Call Spread | 3 | 730 | 111 | 15.2% | 73 | 65.8% | 59.3% | 6.5% | 64.8% | 56.5% | 73.9% | 0.2122 | 4 | 0.3046 | 0.3942 | 35 | 37 | 62.2% | 64.1% | 71.4% | 3 | 4 | 3 | 4 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Call Spread | 7 | 726 | 111 | 15.3% | 73 | 65.8% | 61.7% | 4.1% | 65.1% | 56.5% | 73.9% | 0.3732 | 3 | 0.2987 | 0.3600 | 14 | 15 | 57.1% | 64.3% | 78.6% | 3 | 4 | 3 | 4 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Call Spread | 14 | 719 | 111 | 15.4% | 79 | 71.2% | 69.3% | 1.9% | 70.9% | 62.1% | 78.8% | 0.4564 | 2 | 0.6043 | 0.6709 | 3 | 7 | 40.0% | 72.7% | 83.3% | 2 | 4 | 3 | 4 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Call Spread | 30 | 703 | 111 | 15.8% | 94 | 84.7% | 75.7% | 9.0% | 83.3% | 76.8% | 90.2% | 0.3580 | 6 | 0.9136 | 0.8499 | 1 | 3 | 33.3% | 91.7% | 100.0% | 2 | 4 | 4 | 4 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Put Spread | 3 | 730 | 184 | 25.2% | 123 | 66.8% | 75.8% | -8.9% | 67.7% | 59.8% | 73.2% | 0.9477 | 1 | 0.5633 | 0.0572 | 57 | 61 | 63.2% | 67.7% | 69.4% | 1 | 4 | 1 | 2 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Put Spread | 7 | 726 | 184 | 25.3% | 134 | 72.8% | 78.8% | -6.0% | 73.4% | 66.0% | 78.7% | 0.7714 | 1 | 0.7115 | 0.2635 | 23 | 26 | 64.3% | 70.8% | 82.1% | 1 | 4 | 1 | 2 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Put Spread | 14 | 719 | 183 | 25.5% | 141 | 77.0% | 84.3% | -7.2% | 77.8% | 70.4% | 82.5% | 0.7632 | 1 | 0.9077 | 0.6721 | 10 | 13 | 50.0% | 80.6% | 100.0% | 1 | 4 | 0 | 2 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Bull Put Spread | 30 | 703 | 183 | 26.0% | 151 | 82.5% | 89.5% | -7.0% | 83.2% | 76.4% | 87.3% | 0.7107 | 1 | 1.0350 | 0.6706 | 2 | 6 | 57.1% | 81.7% | 100.0% | 1 | 4 | 1 | 2 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| Calendar / Diagonal | 3 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 7 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 14 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Calendar / Diagonal | 30 | 0 | 0 | — | 0 | — | — | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | requires two-expiry IV history | — |
| Call Ratio Backspread 1×2 | 3 | 730 | 8 | 1.1% | 1 | 12.5% | 21.8% | -9.3% | 19.1% | 2.2% | 47.1% | 0.6248 | 1 | -1.7771 | -0.7804 | 1 | 2 | 0.0% | 0.0% | 20.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Call Ratio Backspread 1×2 | 7 | 726 | 8 | 1.1% | 0 | 0.0% | 26.0% | -26.0% | 18.6% | 0.0% | 32.4% | 0.7235 | 1 | -1.5259 | -0.2048 | 1 | 1 | 0.0% | 0.0% | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Call Ratio Backspread 1×2 | 14 | 719 | 8 | 1.1% | 1 | 12.5% | 29.3% | -16.8% | 24.5% | 2.2% | 47.1% | 0.6443 | 1 | -0.7803 | 0.3085 | 1 | 0 | 0.0% | 0.0% | 33.3% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Call Ratio Backspread 1×2 | 30 | 703 | 8 | 1.1% | 0 | 0.0% | 39.1% | -39.1% | 27.9% | 0.0% | 32.4% | 0.7886 | 1 | -0.7029 | 0.4013 | 1 | 0 | 0.0% | 0.0% | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Iron Butterfly | 3 | 730 | 0 | 0.0% | 0 | — | 34.2% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 7 | 726 | 0 | 0.0% | 0 | — | 36.0% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 14 | 719 | 0 | 0.0% | 0 | — | 34.2% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Butterfly | 30 | 703 | 0 | 0.0% | 0 | — | 31.9% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| Iron Condor | 3 | 730 | 16 | 2.2% | 9 | 56.2% | 64.9% | -8.7% | 61.1% | 33.2% | 76.9% | 0.6579 | 1 | -0.0411 | -0.0459 | 4 | 5 | 40.0% | 57.1% | 75.0% | 1 | 1 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Iron Condor | 7 | 726 | 15 | 2.1% | 9 | 60.0% | 64.5% | -4.5% | 62.6% | 35.7% | 80.2% | 0.5525 | 1 | 0.1397 | 0.0200 | 1 | 2 | 0.0% | 70.8% | 100.0% | 1 | 1 | 0 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Iron Condor | 14 | 719 | 15 | 2.1% | 11 | 73.3% | 64.0% | 9.4% | 68.0% | 48.0% | 89.1% | 0.4227 | 1 | 0.1893 | 0.6865 | 1 | 1 | 0.0% | 100.0% | 100.0% | 1 | 1 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Iron Condor | 30 | 703 | 14 | 2.0% | 5 | 35.7% | 54.1% | -18.3% | 46.5% | 16.3% | 61.2% | 0.6436 | 1 | -0.0691 | 1.0908 | 1 | 0 | 0.0% | 0.0% | 100.0% | 0 | 1 | 0 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Butterfly / Condor קנוי | 3 | 730 | 16 | 2.2% | 7 | 43.8% | 34.2% | 9.5% | 38.5% | 23.1% | 66.8% | 0.3271 | 1 | -0.1492 | 0.2518 | 4 | 5 | 0.0% | 42.9% | 80.0% | 2 | 2 | 2 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Butterfly / Condor קנוי | 7 | 726 | 16 | 2.2% | 5 | 31.2% | 36.0% | -4.7% | 33.9% | 14.2% | 55.6% | 0.5551 | 1 | -0.3185 | 0.2576 | 1 | 2 | 0.0% | 33.3% | 100.0% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Butterfly / Condor קנוי | 14 | 719 | 16 | 2.2% | 4 | 25.0% | 34.2% | -9.2% | 30.1% | 10.2% | 49.5% | 0.5770 | 1 | -0.3463 | 0.7397 | 1 | 1 | 0.0% | 0.0% | 100.0% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Butterfly / Condor קנוי | 30 | 703 | 14 | 2.0% | 0 | 0.0% | 31.9% | -31.9% | 18.7% | 0.0% | 21.5% | 0.7530 | 1 | -0.6443 | 1.1104 | 1 | 0 | 0.0% | 0.0% | 0.0% | 0 | 2 | 0 | 1 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Straddle / Strangle | 3 | 730 | 5 | 0.7% | 0 | 0.0% | 35.1% | -35.1% | 28.1% | 0.0% | 43.4% | 0.7688 | 1 | -0.6693 | 0.3037 | 1 | 1 | 0.0% | 0.0% | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Straddle / Strangle | 7 | 726 | 5 | 0.7% | 0 | 0.0% | 35.5% | -35.5% | 28.4% | 0.0% | 43.4% | 0.7711 | 1 | -0.3583 | 0.7461 | 1 | 0 | 0.0% | 0.0% | 0.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Straddle / Strangle | 14 | 719 | 5 | 0.7% | 1 | 20.0% | 36.0% | -16.0% | 32.8% | 3.6% | 62.4% | 0.6307 | 1 | -0.3870 | -0.1015 | 1 | 0 | 0.0% | 0.0% | 100.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Long Straddle / Strangle | 30 | 703 | 5 | 0.7% | 1 | 20.0% | 45.9% | -25.9% | 40.8% | 3.6% | 62.4% | 0.6987 | 1 | -0.3116 | 0.5675 | 1 | 0 | 0.0% | 0.0% | 100.0% | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Put Ratio Backspread 1×2 | 3 | 730 | 25 | 3.4% | 2 | 8.0% | 13.3% | -5.3% | 10.4% | 2.2% | 25.0% | 0.6702 | 1 | -1.6151 | 0.7733 | 7 | 8 | 0.0% | 11.1% | 11.1% | 0 | 2 | 1 | 3 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Put Ratio Backspread 1×2 | 7 | 726 | 25 | 3.4% | 4 | 16.0% | 9.5% | 6.5% | 13.1% | 6.4% | 34.7% | 0.3506 | 2 | -1.6326 | 0.8733 | 1 | 3 | 0.0% | 0.0% | 33.3% | 1 | 2 | 2 | 3 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Put Ratio Backspread 1×2 | 14 | 719 | 25 | 3.5% | 1 | 4.0% | 6.7% | -2.7% | 5.2% | 0.7% | 19.5% | 0.5427 | 1 | -1.6962 | 0.9132 | 1 | 1 | 0.0% | 0.0% | 50.0% | 0 | 2 | 1 | 3 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| Put Ratio Backspread 1×2 | 30 | 703 | 25 | 3.6% | 1 | 4.0% | 6.8% | -2.8% | 5.3% | 0.7% | 19.5% | 0.5446 | 1 | -1.7536 | 0.7473 | 1 | 0 | 0.0% | 0.0% | 100.0% | 0 | 2 | 1 | 3 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 730 | 184 | 25.2% | 76 | 41.3% | 37.5% | 3.8% | 40.9% | 34.4% | 48.5% | 0.2716 | 3 | -0.2827 | 0.2432 | 58 | 61 | 37.7% | 41.5% | 44.8% | 3 | 4 | 1 | 3 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 726 | 184 | 25.3% | 70 | 38.0% | 35.7% | 2.4% | 37.8% | 31.3% | 45.2% | 0.4005 | 2 | -0.2275 | 0.3459 | 21 | 26 | 25.0% | 38.5% | 48.3% | 2 | 4 | 2 | 3 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 719 | 181 | 25.2% | 86 | 47.5% | 39.9% | 7.6% | 46.8% | 40.4% | 54.8% | 0.2955 | 5 | -0.1625 | 0.4473 | 8 | 12 | 21.4% | 46.2% | 66.7% | 4 | 4 | 2 | 3 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 703 | 180 | 25.6% | 64 | 35.6% | 36.6% | -1.0% | 35.7% | 28.9% | 42.8% | 0.5203 | 1 | -0.3106 | 0.7291 | 2 | 6 | 0.0% | 33.3% | 85.7% | 1 | 4 | 2 | 3 | בינונית | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 730 | 22 | 3.0% | 10 | 45.5% | 27.4% | 18.1% | 36.9% | 26.9% | 65.3% | 0.1420 | 2 | -0.2575 | -0.3271 | 6 | 7 | 0.0% | 42.9% | 77.8% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 726 | 22 | 3.0% | 8 | 36.4% | 28.8% | 7.6% | 32.8% | 19.7% | 57.0% | 0.3860 | 2 | -0.3469 | 0.4045 | 2 | 3 | 0.0% | 45.8% | 100.0% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 719 | 22 | 3.1% | 5 | 22.7% | 24.1% | -1.3% | 23.4% | 10.1% | 43.4% | 0.5124 | 1 | -0.4382 | 0.5329 | 1 | 1 | 0.0% | 0.0% | 66.7% | 1 | 2 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 703 | 19 | 2.7% | 3 | 15.8% | 17.5% | -1.7% | 16.7% | 5.5% | 37.6% | 0.5179 | 1 | -0.7505 | 0.5146 | 1 | 0 | 0.0% | 0.0% | 100.0% | 0 | 1 | 1 | 2 | לא מספקת | market-scenario proxy; no option P&L | 1.0000 |
| פרפר הפוך / Long Iron Condor | 3 | 730 | 0 | 0.0% | 0 | — | 35.1% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 7 | 726 | 0 | 0.0% | 0 | — | 35.5% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 14 | 719 | 0 | 0.0% | 0 | — | 36.0% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |
| פרפר הפוך / Long Iron Condor | 30 | 703 | 0 | 0.0% | 0 | — | 45.9% | — | — | — | — | — | 1 | — | — | 0 | 0 | — | — | — | 0 | 0 | 0 | 0 | לא מספקת | market-scenario proxy; no option P&L | — |

## Strategy scenario sensitivity to 0.75x / 1.00x / 1.25x volatility bands

| strategy | horizon | band_multiplier | selected_n | success_rate |
| --- | --- | --- | --- | --- |
| Bear Call Spread | 3 | 0.7500 | 62 | 43.5% |
| Bear Call Spread | 3 | 1.0000 | 62 | 53.2% |
| Bear Call Spread | 3 | 1.2500 | 62 | 59.7% |
| Bear Call Spread | 7 | 0.7500 | 60 | 48.3% |
| Bear Call Spread | 7 | 1.0000 | 60 | 51.7% |
| Bear Call Spread | 7 | 1.2500 | 60 | 56.7% |
| Bear Call Spread | 14 | 0.7500 | 59 | 40.7% |
| Bear Call Spread | 14 | 1.0000 | 59 | 52.5% |
| Bear Call Spread | 14 | 1.2500 | 59 | 57.6% |
| Bear Call Spread | 30 | 0.7500 | 50 | 40.0% |
| Bear Call Spread | 30 | 1.0000 | 50 | 46.0% |
| Bear Call Spread | 30 | 1.2500 | 50 | 48.0% |
| Bear Put Spread | 3 | 0.7500 | 45 | 37.8% |
| Bear Put Spread | 3 | 1.0000 | 45 | 37.8% |
| Bear Put Spread | 3 | 1.2500 | 45 | 37.8% |
| Bear Put Spread | 7 | 0.7500 | 45 | 51.1% |
| Bear Put Spread | 7 | 1.0000 | 45 | 51.1% |
| Bear Put Spread | 7 | 1.2500 | 45 | 51.1% |
| Bear Put Spread | 14 | 0.7500 | 44 | 50.0% |
| Bear Put Spread | 14 | 1.0000 | 44 | 50.0% |
| Bear Put Spread | 14 | 1.2500 | 44 | 50.0% |
| Bear Put Spread | 30 | 0.7500 | 44 | 40.9% |
| Bear Put Spread | 30 | 1.0000 | 44 | 40.9% |
| Bear Put Spread | 30 | 1.2500 | 44 | 40.9% |
| Bull Call Spread | 3 | 0.7500 | 111 | 65.8% |
| Bull Call Spread | 3 | 1.0000 | 111 | 65.8% |
| Bull Call Spread | 3 | 1.2500 | 111 | 65.8% |
| Bull Call Spread | 7 | 0.7500 | 111 | 65.8% |
| Bull Call Spread | 7 | 1.0000 | 111 | 65.8% |
| Bull Call Spread | 7 | 1.2500 | 111 | 65.8% |
| Bull Call Spread | 14 | 0.7500 | 111 | 71.2% |
| Bull Call Spread | 14 | 1.0000 | 111 | 71.2% |
| Bull Call Spread | 14 | 1.2500 | 111 | 71.2% |
| Bull Call Spread | 30 | 0.7500 | 111 | 84.7% |
| Bull Call Spread | 30 | 1.0000 | 111 | 84.7% |
| Bull Call Spread | 30 | 1.2500 | 111 | 84.7% |
| Bull Put Spread | 3 | 0.7500 | 184 | 63.6% |
| Bull Put Spread | 3 | 1.0000 | 184 | 66.8% |
| Bull Put Spread | 3 | 1.2500 | 184 | 70.7% |
| Bull Put Spread | 7 | 0.7500 | 184 | 71.2% |
| Bull Put Spread | 7 | 1.0000 | 184 | 72.8% |
| Bull Put Spread | 7 | 1.2500 | 184 | 78.3% |
| Bull Put Spread | 14 | 0.7500 | 183 | 74.3% |
| Bull Put Spread | 14 | 1.0000 | 183 | 77.0% |
| Bull Put Spread | 14 | 1.2500 | 183 | 83.6% |
| Bull Put Spread | 30 | 0.7500 | 183 | 80.3% |
| Bull Put Spread | 30 | 1.0000 | 183 | 82.5% |
| Bull Put Spread | 30 | 1.2500 | 183 | 84.7% |
| Call Ratio Backspread 1×2 | 3 | 0.7500 | 8 | 12.5% |
| Call Ratio Backspread 1×2 | 3 | 1.0000 | 8 | 12.5% |
| Call Ratio Backspread 1×2 | 3 | 1.2500 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 0.7500 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 1.0000 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 7 | 1.2500 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 14 | 0.7500 | 8 | 12.5% |
| Call Ratio Backspread 1×2 | 14 | 1.0000 | 8 | 12.5% |
| Call Ratio Backspread 1×2 | 14 | 1.2500 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 30 | 0.7500 | 8 | 12.5% |
| Call Ratio Backspread 1×2 | 30 | 1.0000 | 8 | 0.0% |
| Call Ratio Backspread 1×2 | 30 | 1.2500 | 8 | 0.0% |
| Iron Condor | 3 | 0.7500 | 16 | 50.0% |
| Iron Condor | 3 | 1.0000 | 16 | 56.2% |
| Iron Condor | 3 | 1.2500 | 16 | 56.2% |
| Iron Condor | 7 | 0.7500 | 15 | 60.0% |
| Iron Condor | 7 | 1.0000 | 15 | 60.0% |
| Iron Condor | 7 | 1.2500 | 15 | 66.7% |
| Iron Condor | 14 | 0.7500 | 15 | 53.3% |
| Iron Condor | 14 | 1.0000 | 15 | 73.3% |
| Iron Condor | 14 | 1.2500 | 15 | 80.0% |
| Iron Condor | 30 | 0.7500 | 14 | 35.7% |
| Iron Condor | 30 | 1.0000 | 14 | 35.7% |
| Iron Condor | 30 | 1.2500 | 14 | 64.3% |
| Long Butterfly / Condor קנוי | 3 | 0.7500 | 16 | 37.5% |
| Long Butterfly / Condor קנוי | 3 | 1.0000 | 16 | 43.8% |
| Long Butterfly / Condor קנוי | 3 | 1.2500 | 16 | 43.8% |
| Long Butterfly / Condor קנוי | 7 | 0.7500 | 16 | 25.0% |
| Long Butterfly / Condor קנוי | 7 | 1.0000 | 16 | 31.2% |
| Long Butterfly / Condor קנוי | 7 | 1.2500 | 16 | 37.5% |
| Long Butterfly / Condor קנוי | 14 | 0.7500 | 16 | 12.5% |
| Long Butterfly / Condor קנוי | 14 | 1.0000 | 16 | 25.0% |
| Long Butterfly / Condor קנוי | 14 | 1.2500 | 16 | 37.5% |
| Long Butterfly / Condor קנוי | 30 | 0.7500 | 14 | 0.0% |
| Long Butterfly / Condor קנוי | 30 | 1.0000 | 14 | 0.0% |
| Long Butterfly / Condor קנוי | 30 | 1.2500 | 14 | 7.1% |
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
| Put Ratio Backspread 1×2 | 3 | 0.7500 | 25 | 12.0% |
| Put Ratio Backspread 1×2 | 3 | 1.0000 | 25 | 8.0% |
| Put Ratio Backspread 1×2 | 3 | 1.2500 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 7 | 0.7500 | 25 | 16.0% |
| Put Ratio Backspread 1×2 | 7 | 1.0000 | 25 | 16.0% |
| Put Ratio Backspread 1×2 | 7 | 1.2500 | 25 | 0.0% |
| Put Ratio Backspread 1×2 | 14 | 0.7500 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 14 | 1.0000 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 14 | 1.2500 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 30 | 0.7500 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 30 | 1.0000 | 25 | 4.0% |
| Put Ratio Backspread 1×2 | 30 | 1.2500 | 25 | 4.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 0.7500 | 184 | 29.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 1.0000 | 184 | 41.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 1.2500 | 184 | 46.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 0.7500 | 184 | 28.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 1.0000 | 184 | 38.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 1.2500 | 184 | 46.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 0.7500 | 181 | 36.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 1.0000 | 181 | 47.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 1.2500 | 181 | 56.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 0.7500 | 180 | 25.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 1.0000 | 180 | 35.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 1.2500 | 180 | 42.2% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 0.7500 | 22 | 40.9% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 1.0000 | 22 | 45.5% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 1.2500 | 22 | 50.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 0.7500 | 22 | 27.3% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 1.0000 | 22 | 36.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 1.2500 | 22 | 36.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 0.7500 | 22 | 22.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 1.0000 | 22 | 22.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 1.2500 | 22 | 22.7% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 0.7500 | 19 | 15.8% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 1.0000 | 19 | 15.8% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 1.2500 | 19 | 21.1% |

## Strategy robustness by market regime

| strategy | horizon | regime | selected_n | success_rate | unconditional_baseline | uplift |
| --- | --- | --- | --- | --- | --- | --- |
| Bear Call Spread | 3 | רגוע | 22 | 50.0% | 60.6% | -10.6% |
| Bear Call Spread | 3 | רגיל | 40 | 55.0% | 56.7% | -1.7% |
| Bear Call Spread | 7 | רגוע | 20 | 50.0% | 60.9% | -10.9% |
| Bear Call Spread | 7 | רגיל | 40 | 52.5% | 54.2% | -1.7% |
| Bear Call Spread | 14 | רגוע | 20 | 45.0% | 50.3% | -5.3% |
| Bear Call Spread | 14 | רגיל | 39 | 56.4% | 49.1% | 7.3% |
| Bear Call Spread | 30 | רגוע | 17 | 47.1% | 44.5% | 2.5% |
| Bear Call Spread | 30 | רגיל | 33 | 45.5% | 39.1% | 6.3% |
| Bear Put Spread | 3 | זהירות | 19 | 31.6% | 46.7% | -15.1% |
| Bear Put Spread | 3 | לחץ גבוה | 8 | 62.5% | 41.9% | 20.6% |
| Bear Put Spread | 3 | רגוע | 5 | 0.0% | 42.2% | -42.2% |
| Bear Put Spread | 3 | רגיל | 13 | 46.2% | 37.0% | 9.1% |
| Bear Put Spread | 7 | זהירות | 19 | 52.6% | 34.4% | 18.2% |
| Bear Put Spread | 7 | לחץ גבוה | 8 | 62.5% | 32.3% | 30.2% |
| Bear Put Spread | 7 | רגוע | 5 | 0.0% | 41.6% | -41.6% |
| Bear Put Spread | 7 | רגיל | 13 | 61.5% | 36.5% | 25.1% |
| Bear Put Spread | 14 | זהירות | 18 | 33.3% | 33.7% | -0.4% |
| Bear Put Spread | 14 | לחץ גבוה | 8 | 87.5% | 38.7% | 48.8% |
| Bear Put Spread | 14 | רגוע | 5 | 0.0% | 29.4% | -29.4% |
| Bear Put Spread | 14 | רגיל | 13 | 69.2% | 30.4% | 38.8% |
| Bear Put Spread | 30 | זהירות | 18 | 27.8% | 19.8% | 8.0% |
| Bear Put Spread | 30 | לחץ גבוה | 8 | 62.5% | 19.4% | 43.1% |
| Bear Put Spread | 30 | רגוע | 5 | 20.0% | 28.4% | -8.4% |
| Bear Put Spread | 30 | רגיל | 13 | 53.8% | 21.7% | 32.1% |
| Bull Call Spread | 3 | זהירות | 30 | 63.3% | 53.3% | 10.0% |
| Bull Call Spread | 3 | לחץ גבוה | 7 | 57.1% | 58.1% | -0.9% |
| Bull Call Spread | 3 | רגוע | 33 | 66.7% | 57.8% | 8.9% |
| Bull Call Spread | 3 | רגיל | 41 | 68.3% | 63.0% | 5.3% |
| Bull Call Spread | 7 | זהירות | 30 | 70.0% | 65.6% | 4.4% |
| Bull Call Spread | 7 | לחץ גבוה | 7 | 71.4% | 67.7% | 3.7% |
| Bull Call Spread | 7 | רגוע | 33 | 54.5% | 58.4% | -3.8% |
| Bull Call Spread | 7 | רגיל | 41 | 70.7% | 63.5% | 7.2% |
| Bull Call Spread | 14 | זהירות | 30 | 66.7% | 66.3% | 0.4% |
| Bull Call Spread | 14 | לחץ גבוה | 7 | 57.1% | 61.3% | -4.1% |
| Bull Call Spread | 14 | רגוע | 33 | 72.7% | 70.6% | 2.2% |
| Bull Call Spread | 14 | רגיל | 41 | 75.6% | 69.6% | 6.0% |
| Bull Call Spread | 30 | זהירות | 30 | 83.3% | 80.2% | 3.1% |
| Bull Call Spread | 30 | לחץ גבוה | 7 | 85.7% | 80.6% | 5.1% |
| Bull Call Spread | 30 | רגוע | 33 | 75.8% | 71.6% | 4.1% |
| Bull Call Spread | 30 | רגיל | 41 | 92.7% | 78.3% | 14.4% |
| Bull Put Spread | 3 | רגוע | 105 | 55.2% | 73.8% | -18.5% |
| Bull Put Spread | 3 | רגיל | 79 | 82.3% | 78.9% | 3.4% |
| Bull Put Spread | 7 | רגוע | 105 | 69.5% | 80.4% | -10.9% |
| Bull Put Spread | 7 | רגיל | 79 | 77.2% | 76.4% | 0.8% |
| Bull Put Spread | 14 | רגוע | 104 | 73.1% | 84.8% | -11.7% |
| Bull Put Spread | 14 | רגיל | 79 | 82.3% | 84.1% | -1.8% |
| Bull Put Spread | 30 | רגוע | 104 | 75.0% | 85.8% | -10.8% |
| Bull Put Spread | 30 | רגיל | 79 | 92.4% | 91.7% | 0.7% |
| Iron Condor | 3 | רגוע | 11 | 63.6% | 63.1% | 0.5% |
| Iron Condor | 3 | רגיל | 5 | 40.0% | 69.9% | -29.9% |
| Iron Condor | 7 | רגוע | 10 | 60.0% | 64.0% | -4.0% |
| Iron Condor | 7 | רגיל | 5 | 60.0% | 66.3% | -6.3% |
| Iron Condor | 14 | רגוע | 10 | 60.0% | 63.3% | -3.3% |
| Iron Condor | 14 | רגיל | 5 | 100.0% | 62.9% | 37.1% |
| Iron Condor | 30 | רגוע | 9 | 33.3% | 54.2% | -20.9% |
| Iron Condor | 30 | רגיל | 5 | 40.0% | 48.9% | -8.9% |
| Long Butterfly / Condor קנוי | 3 | רגוע | 11 | 45.5% | 34.4% | 11.1% |
| Long Butterfly / Condor קנוי | 3 | רגיל | 5 | 40.0% | 35.6% | 4.4% |
| Long Butterfly / Condor קנוי | 7 | רגוע | 11 | 45.5% | 41.3% | 4.1% |
| Long Butterfly / Condor קנוי | 7 | רגיל | 5 | 0.0% | 30.6% | -30.6% |
| Long Butterfly / Condor קנוי | 14 | רגוע | 11 | 9.1% | 35.1% | -26.0% |
| Long Butterfly / Condor קנוי | 14 | רגיל | 5 | 60.0% | 33.2% | 26.8% |
| Long Butterfly / Condor קנוי | 30 | רגוע | 10 | 0.0% | 30.3% | -30.3% |
| Put Ratio Backspread 1×2 | 3 | זהירות | 9 | 11.1% | 18.9% | -7.8% |
| Put Ratio Backspread 1×2 | 3 | לחץ גבוה | 9 | 0.0% | 12.9% | -12.9% |
| Put Ratio Backspread 1×2 | 3 | רגיל | 7 | 14.3% | 9.7% | 4.6% |
| Put Ratio Backspread 1×2 | 7 | זהירות | 9 | 11.1% | 6.7% | 4.4% |
| Put Ratio Backspread 1×2 | 7 | לחץ גבוה | 9 | 11.1% | 19.4% | -8.2% |
| Put Ratio Backspread 1×2 | 7 | רגיל | 7 | 28.6% | 8.0% | 20.6% |
| Put Ratio Backspread 1×2 | 14 | זהירות | 9 | 11.1% | 4.5% | 6.6% |
| Put Ratio Backspread 1×2 | 14 | לחץ גבוה | 9 | 0.0% | 3.2% | -3.2% |
| Put Ratio Backspread 1×2 | 14 | רגיל | 7 | 0.0% | 7.1% | -7.1% |
| Put Ratio Backspread 1×2 | 30 | זהירות | 9 | 11.1% | 5.8% | 5.3% |
| Put Ratio Backspread 1×2 | 30 | לחץ גבוה | 9 | 0.0% | 0.0% | 0.0% |
| Put Ratio Backspread 1×2 | 30 | רגיל | 7 | 0.0% | 6.2% | -6.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | זהירות | 5 | 20.0% | 30.0% | -10.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | רגוע | 109 | 42.2% | 35.9% | 6.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | רגיל | 70 | 41.4% | 42.6% | -1.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | זהירות | 5 | 40.0% | 37.8% | 2.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | רגוע | 109 | 38.5% | 33.1% | 5.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | רגיל | 70 | 37.1% | 37.8% | -0.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | זהירות | 5 | 20.0% | 38.2% | -18.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | רגוע | 109 | 45.9% | 41.1% | 4.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | רגיל | 67 | 52.2% | 39.6% | 12.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | זהירות | 5 | 60.0% | 48.8% | 11.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | רגוע | 108 | 38.0% | 34.2% | 3.8% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | רגיל | 67 | 29.9% | 33.3% | -3.5% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | זהירות | 13 | 53.8% | 27.8% | 26.1% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | רגיל | 5 | 20.0% | 27.3% | -7.3% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | זהירות | 13 | 46.2% | 27.8% | 18.4% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | רגיל | 5 | 20.0% | 28.5% | -8.5% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | זהירות | 13 | 30.8% | 29.2% | 1.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | רגיל | 5 | 20.0% | 23.3% | -3.3% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | זהירות | 10 | 30.0% | 14.0% | 16.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | רגיל | 5 | 0.0% | 15.6% | -15.6% |

## Strategy robustness by calendar year

| strategy | horizon | year | selected_n | success_rate | unconditional_baseline | uplift |
| --- | --- | --- | --- | --- | --- | --- |
| Bear Call Spread | 3 | 2,023 | 12 | 75.0% | 63.5% | 11.5% |
| Bear Call Spread | 3 | 2,024 | 26 | 50.0% | 58.8% | -8.8% |
| Bear Call Spread | 3 | 2,025 | 9 | 55.6% | 52.0% | 3.5% |
| Bear Call Spread | 3 | 2,026 | 15 | 40.0% | 65.7% | -25.7% |
| Bear Call Spread | 7 | 2,023 | 12 | 83.3% | 70.8% | 12.5% |
| Bear Call Spread | 7 | 2,024 | 26 | 42.3% | 56.7% | -14.4% |
| Bear Call Spread | 7 | 2,025 | 9 | 44.4% | 49.6% | -5.1% |
| Bear Call Spread | 7 | 2,026 | 13 | 46.2% | 61.9% | -15.7% |
| Bear Call Spread | 14 | 2,023 | 12 | 91.7% | 57.3% | 34.4% |
| Bear Call Spread | 14 | 2,024 | 26 | 30.8% | 46.1% | -15.4% |
| Bear Call Spread | 14 | 2,025 | 9 | 33.3% | 43.1% | -9.8% |
| Bear Call Spread | 14 | 2,026 | 12 | 75.0% | 64.4% | 10.6% |
| Bear Call Spread | 30 | 2,023 | 12 | 91.7% | 56.2% | 35.4% |
| Bear Call Spread | 30 | 2,024 | 26 | 15.4% | 41.2% | -25.8% |
| Bear Call Spread | 30 | 2,025 | 9 | 55.6% | 31.3% | 24.3% |
| Bear Put Spread | 3 | 2,023 | 9 | 55.6% | 46.9% | 8.7% |
| Bear Put Spread | 3 | 2,024 | 5 | 0.0% | 40.0% | -40.0% |
| Bear Put Spread | 3 | 2,025 | 13 | 30.8% | 35.0% | -4.2% |
| Bear Put Spread | 3 | 2,026 | 18 | 44.4% | 47.6% | -3.1% |
| Bear Put Spread | 7 | 2,023 | 9 | 66.7% | 43.8% | 22.9% |
| Bear Put Spread | 7 | 2,024 | 5 | 40.0% | 39.6% | 0.4% |
| Bear Put Spread | 7 | 2,025 | 13 | 23.1% | 31.3% | -8.2% |
| Bear Put Spread | 7 | 2,026 | 18 | 66.7% | 44.6% | 22.1% |
| Bear Put Spread | 14 | 2,023 | 9 | 44.4% | 38.5% | 5.9% |
| Bear Put Spread | 14 | 2,024 | 5 | 0.0% | 29.0% | -29.0% |
| Bear Put Spread | 14 | 2,025 | 13 | 30.8% | 24.0% | 6.8% |
| Bear Put Spread | 14 | 2,026 | 17 | 82.4% | 40.9% | 41.4% |
| Bear Put Spread | 30 | 2,023 | 9 | 22.2% | 44.8% | -22.6% |
| Bear Put Spread | 30 | 2,024 | 5 | 20.0% | 12.7% | 7.3% |
| Bear Put Spread | 30 | 2,025 | 13 | 15.4% | 17.9% | -2.5% |
| Bear Put Spread | 30 | 2,026 | 17 | 76.5% | 45.7% | 30.8% |
| Bull Call Spread | 3 | 2,023 | 6 | 100.0% | 53.1% | 46.9% |
| Bull Call Spread | 3 | 2,024 | 30 | 63.3% | 60.0% | 3.3% |
| Bull Call Spread | 3 | 2,025 | 54 | 68.5% | 65.0% | 3.5% |
| Bull Call Spread | 3 | 2,026 | 21 | 52.4% | 52.4% | -0.1% |
| Bull Call Spread | 7 | 2,023 | 6 | 66.7% | 56.2% | 10.4% |
| Bull Call Spread | 7 | 2,024 | 30 | 66.7% | 60.4% | 6.3% |
| Bull Call Spread | 7 | 2,025 | 54 | 68.5% | 68.7% | -0.2% |
| Bull Call Spread | 7 | 2,026 | 21 | 57.1% | 55.4% | 1.7% |
| Bull Call Spread | 14 | 2,023 | 6 | 33.3% | 61.5% | -28.1% |
| Bull Call Spread | 14 | 2,024 | 30 | 56.7% | 71.0% | -14.4% |
| Bull Call Spread | 14 | 2,025 | 54 | 81.5% | 76.0% | 5.5% |
| Bull Call Spread | 14 | 2,026 | 21 | 76.2% | 59.1% | 17.1% |
| Bull Call Spread | 30 | 2,023 | 6 | 16.7% | 55.2% | -38.5% |
| Bull Call Spread | 30 | 2,024 | 30 | 86.7% | 87.3% | -0.7% |
| Bull Call Spread | 30 | 2,025 | 54 | 90.7% | 82.1% | 8.6% |
| Bull Call Spread | 30 | 2,026 | 21 | 85.7% | 54.3% | 31.4% |
| Bull Put Spread | 3 | 2,023 | 24 | 66.7% | 77.1% | -10.4% |
| Bull Put Spread | 3 | 2,024 | 79 | 68.4% | 75.9% | -7.6% |
| Bull Put Spread | 3 | 2,025 | 53 | 58.5% | 76.0% | -17.5% |
| Bull Put Spread | 3 | 2,026 | 28 | 78.6% | 74.1% | 4.4% |
| Bull Put Spread | 7 | 2,023 | 24 | 79.2% | 82.3% | -3.1% |
| Bull Put Spread | 7 | 2,024 | 79 | 70.9% | 77.1% | -6.3% |
| Bull Put Spread | 7 | 2,025 | 53 | 64.2% | 80.9% | -16.7% |
| Bull Put Spread | 7 | 2,026 | 28 | 89.3% | 75.5% | 13.7% |
| Bull Put Spread | 14 | 2,023 | 24 | 66.7% | 78.1% | -11.5% |
| Bull Put Spread | 14 | 2,024 | 79 | 73.4% | 83.7% | -10.3% |
| Bull Put Spread | 14 | 2,025 | 53 | 83.0% | 88.2% | -5.2% |
| Bull Put Spread | 14 | 2,026 | 27 | 85.2% | 82.6% | 2.6% |
| Bull Put Spread | 30 | 2,023 | 24 | 29.2% | 67.7% | -38.5% |
| Bull Put Spread | 30 | 2,024 | 79 | 94.9% | 98.0% | -3.0% |
| Bull Put Spread | 30 | 2,025 | 53 | 86.8% | 93.9% | -7.1% |
| Bull Put Spread | 30 | 2,026 | 27 | 85.2% | 80.2% | 5.0% |
| Iron Condor | 3 | 2,024 | 12 | 66.7% | 64.9% | 1.8% |
| Iron Condor | 7 | 2,024 | 12 | 66.7% | 64.9% | 1.8% |
| Iron Condor | 14 | 2,024 | 12 | 75.0% | 59.6% | 15.4% |
| Iron Condor | 30 | 2,024 | 12 | 33.3% | 62.4% | -29.1% |
| Long Butterfly / Condor קנוי | 3 | 2,023 | 7 | 42.9% | 40.6% | 2.2% |
| Long Butterfly / Condor קנוי | 3 | 2,025 | 6 | 33.3% | 28.0% | 5.3% |
| Long Butterfly / Condor קנוי | 7 | 2,023 | 7 | 71.4% | 53.1% | 18.3% |
| Long Butterfly / Condor קנוי | 7 | 2,025 | 6 | 0.0% | 30.5% | -30.5% |
| Long Butterfly / Condor קנוי | 14 | 2,023 | 7 | 0.0% | 35.4% | -35.4% |
| Long Butterfly / Condor קנוי | 14 | 2,025 | 6 | 33.3% | 31.3% | 2.0% |
| Long Butterfly / Condor קנוי | 30 | 2,023 | 7 | 0.0% | 24.0% | -24.0% |
| Long Butterfly / Condor קנוי | 30 | 2,025 | 6 | 0.0% | 25.2% | -25.2% |
| Put Ratio Backspread 1×2 | 3 | 2,024 | 7 | 14.3% | 14.3% | 0.0% |
| Put Ratio Backspread 1×2 | 3 | 2,025 | 11 | 9.1% | 13.0% | -3.9% |
| Put Ratio Backspread 1×2 | 7 | 2,024 | 7 | 0.0% | 6.9% | -6.9% |
| Put Ratio Backspread 1×2 | 7 | 2,025 | 11 | 18.2% | 11.8% | 6.4% |
| Put Ratio Backspread 1×2 | 14 | 2,024 | 7 | 0.0% | 6.1% | -6.1% |
| Put Ratio Backspread 1×2 | 14 | 2,025 | 11 | 0.0% | 3.3% | -3.3% |
| Put Ratio Backspread 1×2 | 30 | 2,024 | 7 | 0.0% | 0.0% | 0.0% |
| Put Ratio Backspread 1×2 | 30 | 2,025 | 11 | 0.0% | 1.2% | -1.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,023 | 21 | 42.9% | 34.4% | 8.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,024 | 56 | 37.5% | 39.2% | -1.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,025 | 73 | 46.6% | 39.8% | 6.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 3 | 2,026 | 34 | 35.3% | 32.9% | 2.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,023 | 21 | 57.1% | 38.5% | 18.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,024 | 56 | 39.3% | 32.2% | 7.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,025 | 73 | 34.2% | 37.0% | -2.7% |
| פרפר Call שורי / Broken-Wing Butterfly | 7 | 2,026 | 34 | 32.4% | 37.4% | -5.1% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,023 | 21 | 71.4% | 45.8% | 25.6% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,024 | 56 | 41.1% | 36.7% | 4.3% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,025 | 73 | 46.6% | 38.6% | 8.0% |
| פרפר Call שורי / Broken-Wing Butterfly | 14 | 2,026 | 31 | 45.2% | 43.9% | 1.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,023 | 21 | 66.7% | 37.5% | 29.2% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,024 | 56 | 46.4% | 49.8% | -3.4% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,025 | 73 | 24.7% | 25.2% | -0.5% |
| פרפר Call שורי / Broken-Wing Butterfly | 30 | 2,026 | 30 | 20.0% | 31.9% | -11.9% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,023 | 12 | 33.3% | 36.5% | -3.1% |
| פרפר Put דובי / Broken-Wing Butterfly | 3 | 2,026 | 7 | 57.1% | 33.6% | 23.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,023 | 12 | 33.3% | 33.3% | 0.0% |
| פרפר Put דובי / Broken-Wing Butterfly | 7 | 2,026 | 7 | 42.9% | 35.3% | 7.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,023 | 12 | 8.3% | 22.9% | -14.6% |
| פרפר Put דובי / Broken-Wing Butterfly | 14 | 2,026 | 7 | 57.1% | 33.3% | 23.8% |
| פרפר Put דובי / Broken-Wing Butterfly | 30 | 2,023 | 12 | 0.0% | 13.5% | -13.5% |

## Context-only OOS ablation: FX-equity state and TA35-VTA35 correlation

| feature | horizon | n_eff | baseline_accuracy | augmented_accuracy | lift | p_value | positive_regimes | tested_regimes | fdr_q | eligible | status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fx_equity_state | 3 | 241 | 52.7% | 51.9% | -0.8% | 0.5896 | 0 | 4 | 1.0000 | 0 | context-only |
| ta35_vta35_corr_60 | 3 | 225 | 53.3% | 48.4% | -4.9% | 0.8730 | 0 | 4 | 1.0000 | 0 | context-only |
| fx_equity_state | 7 | 103 | 50.5% | 44.7% | -5.8% | 0.8633 | 0 | 3 | 1.0000 | 0 | context-only |
| ta35_vta35_corr_60 | 7 | 96 | 51.0% | 46.9% | -4.2% | 0.7418 | 1 | 3 | 1.0000 | 0 | context-only |
| fx_equity_state | 14 | 50 | 60.0% | 68.0% | 8.0% | 0.1587 | 2 | 2 | 1.0000 | 0 | context-only |
| ta35_vta35_corr_60 | 14 | 47 | 61.7% | 44.7% | -17.0% | 0.9703 | 0 | 2 | 1.0000 | 0 | context-only |
| fx_equity_state | 30 | 23 | 60.9% | 52.2% | -8.7% | 0.7602 | 1 | 2 | 1.0000 | 0 | context-only |
| ta35_vta35_corr_60 | 30 | 22 | 63.6% | 54.5% | -9.1% | 0.7602 | 0 | 2 | 1.0000 | 0 | context-only |
