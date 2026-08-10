# Release 2.0.0 — additional indicators and strict forecast validation

- Added nine frozen `Research/Context` candidates derived only from existing
  Lite EOD data, without adding duplicate technical-indicator votes.
- Added live HAR-EOD, fixed-parameter GJR and horizon-matched variance-premium
  metrics, plus downside share, VTA35 vol-of-vol, Rogers-Satchell acceleration,
  local-global stress, trend efficiency, range position and scaled reversal.
- Rebuilt volatility-model evaluation around purged expanding OOS predictions,
  one non-overlapping offset, QLIKE, variance MSE and moving-block bootstrap.
- Added HAR-X with only downside share, VTA35 and local-global stress, plus an
  L2-shrunk five-family probability model, calibration and OOS ablation.
- Added every non-overlapping offset as a separate report table and froze the
  formulas for forward-only evaluation from 2026-08-11.
- Kept every new output context-only; premium-sale eligibility, strength scores
  and automated deployment remain hard-closed.

# Release 1.5.0 — comprehensive backtest research

- Standardized dashboard and research horizons on 3, 7, 14 and 30 trading days.
- Added a reproducible single-file research report for every indicator output
  and every strategy family across the complete local history.
- Added direction accuracy, empirical baselines, lift, Wilson intervals,
  delayed walk-forward Brier scores, rank IC, intensity subsets, non-overlapping
  robustness, calendar-year and market-regime stability.
- Added forecast bias/MAE/RMSE and empirical probability-band coverage tests.
- Added selected-strategy uplift against unconditional scenario frequency and
  sensitivity to 0.75x, 1.00x and 1.25x volatility-band definitions.
- Added one-sided inference with Benjamini-Hochberg FDR adjustment and explicit
  sample-quality gates.
- Strategy results remain market-scenario proxies rather than option P&L because
  the Lite database has no historical chain, premiums, skew or transaction costs.

# Release 1.4.0 — empirical signal and strategy strength

- Added walk-forward backtests across the full local TA-35 history for 3, 7,
  14 and 30 trading-day horizons without using future observations in features.
- Added a separate empirical 1–10 strength score beside every volatility arrow,
  based on prior matching signals versus subsequently realized volatility.
- Recalibrated directional TA-35 arrow strength from historical hit rates when
  the indicator has a directional market claim, net of the outcome's historical
  base rate so a broadly rising market is not mistaken for indicator skill.
- Added per-indicator hit rates, sample sizes and per-strategy scenario success
  tables inside the dashboard.
- Strategy results are explicitly labelled market-scenario proxies, not option
  P&L; Calendar/Diagonal remains untestable without two-expiry IV history.

# Release 1.3.0 — selectable fan and indicator signals

- Decoupled the probability-fan horizon from the strategy horizon and added a
  dedicated 3/7/14/30-trading-day control.
- Added a volatility arrow and a TA-35 direction arrow with a 1–10 heuristic
  intensity score beside every indicator.
- Kept range-only indicators explicitly neutral instead of manufacturing a
  market-direction claim.

# Release 1.2.0 — general option-strategy recommendations

- Added transparent strategy-family recommendations using the existing trend,
  volatility-state and relative-pricing inputs.
- Added bullish/bearish spreads, butterflies, ratio backspreads, volatility
  structures, condors and calendar/diagonal candidates.
- Added selectable 3/7/14/30-day core, base and strategy-focus ranges without
  selecting strikes, premiums or executable orders.
- Kept "no preferred trade" as an explicit output when inputs conflict.

# Release 1.1.0 — volatility direction and market trend state

- Added RV20/RV60 structure, ATR5/ATR20 range pressure, five-day VTA35
  momentum, 60-day VTA35 z-score, VIX9D/VIX and VIX/VIX3M cards.
- Added separate, transparent state summaries for volatility direction and
  TA-35 market trend; neither is presented as a trading signal.
- Expanded every card's help text with construction, interpretation and limits.
- Added explicit regression coverage for all new metrics and score bounds.

# Release 1.0.3 — TASE upload

- Added direct buttons to the official TA35 and VTA35 end-of-day download pages.
- Added manual download guidance and in-dashboard CSV upload controls.
- Uploaded TASE exports are validated and imported through a staged database;
  the active database is replaced only after the import succeeds.
- Raw TASE CSV exports with informational rows before the header are supported.

# Release 1.0.2 — Probability fan

- Added an interactive TA-35 probability fan for 3, 7, 14 and 30 trading days.
- Added 0.5, 1, 1.5 and 2 standard-deviation ranges
  (38.3%, 68.3%, 86.6% and 95.4%).
- The fan uses the dashboard's combined annualized volatility forecast and 252 sessions.

# Release 1.0.0 — Lite conversion

- Replaced option-chain snapshots with validated public EOD bars.
- Removed pricing, Greeks, IV solvers, DDE/IBKR plans and option-surface UI.
- Added TA35 close/range volatility, Yang–Zhang, Parkinson, EWMA, gap share,
  VTA35 percentile, IV–RV spread, USD/ILS pressure and the VIX curve.
- Added official-public CSV ingestion, idempotent SQLite persistence and a
  compact market-regime dashboard with explicit data-health status.
- TASE ingestion is a manual official CSV import; Cboe histories can refresh
  directly. Missing data never receives an invented fallback.
# 1.6.0

- Collapsed VTA35 level, change and IV-RV spread into one local-IV family vote.
- Added a 3×3 market-direction × volatility-regime matrix.
- Added an evidence card and hard eligibility gates for short-premium strategies.
- Replaced pseudo-payoff ranges with a clearly labelled scenario-fit map.
- Added non-overlapping OOS ablation with FDR for FX-equity state and rolling
  TA35-VTA35 correlation; both remain context-only until every gate passes.
