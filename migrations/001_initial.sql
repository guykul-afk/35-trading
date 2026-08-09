PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS lite_runs (
    run_id TEXT PRIMARY KEY,
    schema_version TEXT NOT NULL,
    source TEXT NOT NULL,
    source_timestamp TEXT NOT NULL,
    received_timestamp TEXT NOT NULL,
    market_data_type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS eod_bars (
    run_id TEXT NOT NULL REFERENCES lite_runs(run_id) ON DELETE CASCADE,
    symbol TEXT NOT NULL,
    session_date TEXT NOT NULL,
    open REAL,
    high REAL,
    low REAL,
    close REAL NOT NULL,
    source TEXT NOT NULL,
    quality_flags_json TEXT NOT NULL,
    PRIMARY KEY (run_id, symbol)
);
CREATE INDEX IF NOT EXISTS idx_eod_bars_symbol_date ON eod_bars(symbol, session_date DESC);

CREATE TABLE IF NOT EXISTS lite_metrics (
    run_id TEXT NOT NULL REFERENCES lite_runs(run_id) ON DELETE CASCADE,
    metric_name TEXT NOT NULL,
    value REAL,
    as_of TEXT NOT NULL,
    model_version TEXT NOT NULL,
    quality_flags_json TEXT NOT NULL,
    dimensions_json TEXT NOT NULL,
    PRIMARY KEY (run_id, metric_name, dimensions_json)
);
CREATE INDEX IF NOT EXISTS idx_lite_metrics_name_date ON lite_metrics(metric_name, as_of DESC);
