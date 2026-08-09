# Lite runbook

## Install and preview

```bash
python -m pip install -e ".[dev]"
python scripts/seed_demo.py
streamlit run app/Home.py
```

## Production-style public import

Download the official files using these links:

- [TA35 End of Day](https://market.tase.co.il/en/market_data/index/142/historical_data/eod): choose **3 Years**, then **CSV**.
- [VTA35 End of Day](https://market.tase.co.il/en/market_data/index/598/historical_data/eod): choose **3 Years**, then **CSV**.
- [USD/ILS direct CSV](https://edge.boi.gov.il/FusionEdgeServer/sdmx/v2/data/dataflow/BOI.STATISTICS/EXR/1.0/RER_USD_ILS?format=csv) (optional but recommended).
- Cboe files are downloaded automatically with `--cboe`: [VIX9D](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX9D_History.csv), [VIX](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv), and [VIX3M](https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX3M_History.csv).

Save the manual files as `downloads/ta35.csv`, `downloads/vta35.csv`, and
`downloads/usdils.csv`, then run `scripts/import_public_data.py` as shown in
README. Use a new `data/ta35_lite.sqlite3`; the old options database is not read.

## Daily checks

- Confirm the UI does not show the DEMO warning.
- Confirm TA35 and VTA35 dates on Data Health match the last TASE session.
- For an in-dashboard refresh, expand **עדכון נתוני ת״א־35 מהבורסה**, use the
  official page buttons, upload TA35 and optionally VTA35, then press the update
  button. A failed validation leaves the active database unchanged.
- Treat OHLC estimators as unavailable when the export contains closes only.
- Never present a stale value as current; the header warns after three days.

## Verification

Run `python scripts/run_checks.py`. Imports are replay-safe, so the same CSV can
be imported again without duplicating a daily series/run combination.
