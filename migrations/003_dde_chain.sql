PRAGMA foreign_keys = ON;

-- Layer 1: Raw immutable compressed payload
CREATE TABLE IF NOT EXISTS chain_payload (
    payload_sha256  TEXT PRIMARY KEY,
    raw_gzip        BLOB NOT NULL,
    raw_bytes       INTEGER NOT NULL,
    encoding        TEXT,
    first_seen_utc  TEXT NOT NULL
);

-- Layer 2: Normalized chain snapshot
CREATE TABLE IF NOT EXISTS chain_snapshot (
    snapshot_id           TEXT PRIMARY KEY,
    captured_at_utc       TEXT NOT NULL,
    quote_ts_utc          TEXT,
    session_date          TEXT NOT NULL REFERENCES trading_session(session_date),
    seconds_into_session  REAL,
    session_progress      REAL,
    expiry_id             TEXT REFERENCES contract_expiry(expiry_id),
    payload_sha256        TEXT NOT NULL REFERENCES chain_payload(payload_sha256),
    source_file           TEXT NOT NULL,
    source_mtime_utc      TEXT,
    parser_version        TEXT NOT NULL,
    layout_id             TEXT NOT NULL,
    price_unit            TEXT NOT NULL,
    scale_factor_applied  REAL NOT NULL,
    n_strikes             INTEGER NOT NULL,
    n_two_sided           INTEGER NOT NULL,
    synthetic_forward     REAL,
    forward_method        TEXT,
    forward_ci_width      REAL,
    atm_spread_pct        REAL,
    coverage_score        REAL,
    is_usable             INTEGER NOT NULL,
    quality_flags_json    TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_snap_session ON chain_snapshot(session_date, expiry_id, captured_at_utc);
CREATE INDEX IF NOT EXISTS idx_snap_usable  ON chain_snapshot(is_usable, captured_at_utc);

-- Layer 2b: Normalized quotes per strike/right
CREATE TABLE IF NOT EXISTS chain_quote (
    snapshot_id          TEXT NOT NULL REFERENCES chain_snapshot(snapshot_id) ON DELETE CASCADE,
    strike               REAL NOT NULL,
    right                TEXT NOT NULL CHECK (right IN ('C','P')),
    bid                  REAL,
    ask                  REAL,
    last                 REAL,
    bid_size             REAL,
    ask_size             REAL,
    volume               REAL,
    open_interest        REAL,
    vendor_iv            REAL,
    unchanged_since_utc  TEXT,
    stale_seconds        REAL,
    quality_flags_json   TEXT NOT NULL,
    PRIMARY KEY (snapshot_id, strike, right)
);

-- Layer 3: Derived snapshot metrics
CREATE TABLE IF NOT EXISTS chain_metric (
    snapshot_id          TEXT NOT NULL REFERENCES chain_snapshot(snapshot_id) ON DELETE CASCADE,
    metric_name          TEXT NOT NULL,
    value                REAL,
    model_version        TEXT NOT NULL,
    quality_flags_json   TEXT NOT NULL,
    PRIMARY KEY (snapshot_id, metric_name, model_version)
);
