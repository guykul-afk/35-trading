# Lite service interfaces

`SnapshotProvider.fetch_history(start, end)` returns ascending, replay-safe EOD
snapshots. `fetch_snapshot(as_of)` returns the latest available session.

Providers are read-only and deal only with public market series. The core has no
concept of contracts, option quotes, accounts or orders.

`SQLiteRepository` persists `lite_runs`, `eod_bars` and `lite_metrics`.
Missing observations and metrics are stored as null or explicit quality flags.
