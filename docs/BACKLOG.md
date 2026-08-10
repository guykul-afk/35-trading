# Lite backlog

1. Validate Hebrew/English TASE CSV column variants against fresh exports.
2. Add a documented Bank of Israel SDMX adapter after pinning the USD/ILS key.
3. Backtest the four-state stress score and replace heuristic thresholds with
   empirical TA35 percentiles.
4. Add scheduled daily refresh only for sources with documented automation.
5. Add empirical forward three-day ranges by historical regime.
6. Implement validation freeze: context-only tiers, no 1–10 UI scores, premium
   gate closed independently of research results.
7. Add purged walk-forward + embargo, moving-block bootstrap and dependence-safe
   multiple-testing correction.
8. Add RV-level-conditioned and expanding HAR-RV baselines with a VTA35
   incremental-value ablation.
9. Add frozen-rule metadata and forward-only evaluation.
10. Persist a daily MAOF option-chain snapshot with source and timestamp.
11. After items 6–10, add calibrated TA-35 and volatility forecast arrows and a
    0–100 confidence score using five de-duplicated factor families.
