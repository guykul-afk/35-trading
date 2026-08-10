# TA-35 Volatility Dashboard — Lite

Local, read-only, end-of-day volatility dashboard built only from free public
data. The Lite line intentionally contains no option chain, DDE, IBKR, account,
credential, order-entry or real-time code.

## What it shows

- VTA35 level and one-year percentile.
- TA35 realized volatility: 5/10/20-day, EWMA, Parkinson and Yang–Zhang.
- Volatility acceleration, overnight-gap share and a 3-day statistical move.
- An independently selectable 3/7/14/30-day probability fan at 0.5, 1, 1.5
  and 2 standard deviations.
- IV–RV spread/ratio when VTA35 is available.
- USD/ILS pressure and the VIX9D/VIX3M global volatility curve.
- RV20/RV60 structure, normalized ATR5/ATR20 range pressure and VTA35 momentum.
- Nine frozen research candidates: downside-variance share, VTA35 vol-of-vol,
  Rogers-Satchell acceleration, local-global stress spread, trend efficiency,
  range position, volatility-scaled reversal, HAR-EOD and horizon-matched VRP.
- Strict non-overlapping expanding OOS comparison of RV20, the combined forecast,
  VTA35, fixed-parameter GJR, HAR and HAR-X using QLIKE and variance MSE.
- A five-family L2-shrunk probability model for `P(RV rises)` and `P(TA35 rises)`,
  with label purge, Brier/log loss, calibration bins and family ablation.
- Separate VIX9D/VIX and VIX/VIX3M curve segments.
- Per-indicator volatility and conservative TA-35 direction arrows. Historical
  diagnostics are shown as `Research/Context`; 1–10 deployment scores and all
  automatic evidence gates remain disabled until a new frozen forward sample
  passes review.
- Full-history indicator and strategy-scenario backtest tables for 3/7/14/30
  trading days, including hit rates, sample sizes and sample-quality labels.
- A reproducible comprehensive research report (`scripts/generate_backtest_research.py`)
  covering direction, every non-overlapping offset, calibration, QLIKE/MSE,
  moving-block bootstrap, family ablation, year/regime stability,
  multiple-testing control and strategy-band sensitivity.
- A general option-strategy family, selectable 3/7/14/30-day scenario range and
  bounded-risk alternatives; no strikes, option prices or orders are selected.
- A transparent four-state stress regime and per-series data health.
- In-dashboard links and a validated upload flow for official TA35/VTA35 CSV exports.

## Quick start

The distributed Lite bundle already contains the imported database in
`data/ta35_lite.sqlite3`. On Windows, double-click `start_dashboard.bat`, or run
the following commands from the extracted project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e .
.\.venv\Scripts\python.exe -m streamlit run app\Home.py
```

The application always resolves the database relative to the project itself,
so it does not depend on the PowerShell working directory.

For a manual installation on Linux/macOS:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
streamlit run app/Home.py
```

`scripts/seed_demo.py` is only for creating synthetic demo data in a separate
database. It is not required when using the bundled public-data database.

To regenerate the complete backtest knowledge base after a data update:

```bash
python scripts/generate_backtest_research.py
```

The command writes all 3/7/14/30-day indicator, forecast and strategy-scenario
results to `docs/backtest-research-report.md`.

`frozen_rules.json` fixes the candidate formulas before the forward evaluation
beginning 2026-08-11. It explicitly grants no deployment authority: the entire
earlier history remains a discovery sample.

## Import free official data

### Direct download links

| Series | Official download | Save as | What to do |
|---|---|---|---|
| TA35 | [TASE TA-35 — End of Day](https://market.tase.co.il/en/market_data/index/142/historical_data/eod) | `downloads/ta35.csv` | Select **3 Years**, apply the filter, then click **CSV**. |
| VTA35 | [TASE VTA35 — End of Day](https://market.tase.co.il/en/market_data/index/598/historical_data/eod) | `downloads/vta35.csv` | Select **3 Years**, apply the filter, then click **CSV**. |
| USD/ILS | [Bank of Israel — direct CSV](https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS?format=csv) | `downloads/usdils.csv` | The link downloads the complete official daily series. This input is optional but recommended. |
| VIX9D | [Cboe — direct CSV](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX9D_History.csv) | automatic | Downloaded by `--cboe`; no manual save is needed. |
| VIX | [Cboe — direct CSV](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv) | automatic | Downloaded by `--cboe`; no manual save is needed. |
| VIX3M | [Cboe — direct CSV](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv) | automatic | Downloaded by `--cboe`; no manual save is needed. |

TASE does not publish a stable direct file URL: the **CSV** button creates the
export for the selected date range. The links above therefore open the exact
end-of-day download screens, not the intraday tables.

The same links and upload fields are available inside **עדכון נתוני ת״א־35
מהבורסה** on the main dashboard. Uploading TA35 is required; VTA35 is optional.
The dashboard validates the export, imports into a staged database, keeps a
backup and activates the new database only after all checks succeed.

After saving the TASE files (and optionally the Bank of Israel file), run:

PowerShell on Windows (from the project directory):

```powershell
py scripts/import_public_data.py --ta35 downloads/ta35.csv --vta35 downloads/vta35.csv --usdils downloads/usdils.csv --cboe
```

If `usdils.csv` was not downloaded, omit `--usdils downloads/usdils.csv`.

Linux/macOS:

```bash
python scripts/import_public_data.py \
  --ta35 downloads/ta35.csv \
  --vta35 downloads/vta35.csv \
  --usdils downloads/usdils.csv \
  --cboe
```

`--cboe` downloads official VIX9D, VIX and VIX3M histories directly from Cboe.
TASE remains a manual CSV step because its website does not expose a stable,
documented public API and may reject automated requests. Re-running an import
is safe: run IDs are content-derived and SQLite writes are idempotent.

## Checks

```bash
python scripts/run_checks.py
```

The system never silently substitutes missing data. OHLC-dependent estimators
remain null when only closes are available, and the health page exposes the
last date, source and observation count for every series.
