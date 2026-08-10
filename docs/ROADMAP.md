# Lite roadmap

## 1.0 — complete

Public CSV contracts, EOD storage, volatility analytics, market-regime UI,
data-health view, deterministic demo and automated tests.

## 1.1

Real-source sample fixtures, Bank of Israel SDMX adapter and a trading-calendar
freshness policy.

## 1.2

Walk-forward calibration of the stress score and empirical 1–3 day ranges.

## 1.7 — validation rebuild (blocking)

1. Keep every research result at `context only`, remove A-tier and 1–10 product
   scores, and keep the premium-sale deployment gate forcibly closed.
2. Use point-in-time US-series alignment, bias-consistent realized volatility,
   purged walk-forward folds with horizon embargo, block bootstrap inference and
   dependence-safe family-wise multiple-testing correction.
3. Compare every volatility signal with an RV-level-conditioned baseline and an
   expanding HAR-RV benchmark; measure whether VTA35 adds incremental OOS value.
4. Evaluate premium-sale candidates with the research flag enabled while keeping
   research selection separate from deployment eligibility.
5. Freeze candidate rules in `frozen_rules.json` with commit hash and evaluation
   start date before any forward-only assessment.
6. Start daily MAOF option-chain snapshots. Add Black-76 proxy P&L only as a
   research diagnostic until calibrated against real chain history.

## 1.8 — combined directional forecast (after validation rebuild)

Display separate TA-35 and volatility arrows (`↑`, `↓`, `↔`) plus a calibrated
0–100 confidence number. Combine five non-overlapping factor families exactly
once, use OOS reliability weights with shrinkage and correlation penalties, and
abstain (`↔`) when coverage, stability or confidence gates fail. A neutral arrow
is never scored as a successful directional prediction.
