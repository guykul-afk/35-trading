PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS recommendation_log (
    rec_id             TEXT PRIMARY KEY,
    created_at_utc     TEXT NOT NULL,
    snapshot_id        TEXT NOT NULL REFERENCES chain_snapshot(snapshot_id),
    engine_version     TEXT NOT NULL,
    strategy_name      TEXT NOT NULL,
    legs_json          TEXT NOT NULL,
    entry_convention   TEXT NOT NULL,   -- 'bid_ask' | 'mid_plus_slippage'
    entry_price_pts    REAL NOT NULL,
    assumed_cost_pts   REAL NOT NULL,
    pop_model          TEXT NOT NULL,   -- 'rnd_bl' | 'blend'
    pop_value          REAL NOT NULL,
    ev_pts             REAL NOT NULL,
    horizon_expiry_id  TEXT NOT NULL,
    was_recommended    INTEGER NOT NULL, -- 1 = Top displayed, 0 = Evaluated and rejected
    resolved_at_utc    TEXT,
    exit_price_pts     REAL,
    realized_pnl_pts   REAL,
    resolution_method  TEXT,             -- 'expiry_settlement' | 'chain_reprice' | 'unresolved'
    status             TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_rec_log_snap ON recommendation_log(snapshot_id);
CREATE INDEX IF NOT EXISTS idx_rec_log_status ON recommendation_log(status, created_at_utc DESC);
