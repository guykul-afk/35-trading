# Model card — TA35 Lite 1.0

All volatility outputs are annual decimal values using 252 sessions per year;
VTA35 inputs are published percentage points and are divided by 100 only when
compared with realized volatility.

The 3-day forecast is the median of available RV5, RV20, EWMA and Yang–Zhang
estimates. The displayed move is one standard deviation under square-root time,
not an option-implied expected move or a confidence guarantee.

The stress regime is transparent and heuristic. It adds points for elevated
VTA35 percentile, RV acceleration, gap share, inverted short VIX curve and a
sharp USD/ILS move. It is decision support, not a trading signal. Sparse or
missing inputs remain null.
