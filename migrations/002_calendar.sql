PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS trading_session (
    session_date          TEXT PRIMARY KEY,          -- YYYY-MM-DD
    venue                 TEXT NOT NULL DEFAULT 'TASE',
    is_trading            INTEGER NOT NULL,          -- 0/1
    session_type          TEXT NOT NULL,             -- full | sunday_short | erev_chag | closed
    equity_open_local     TEXT,                      -- HH:MM, Asia/Jerusalem
    equity_close_local    TEXT,
    maof_open_local       TEXT,                      -- Derivatives trading hours
    maof_close_local      TEXT,
    closing_auction_local TEXT,
    trading_day_index     INTEGER,                   -- Sequential index for trading days
    prior_us_sessions     INTEGER,                   -- Number of US sessions since prior TASE close (Sunday = 2)
    calendar_gap_days     REAL,                      -- Calendar days since prior TASE session
    source                TEXT NOT NULL,
    note                  TEXT
);
CREATE INDEX IF NOT EXISTS idx_session_trading ON trading_session(is_trading, session_date);

CREATE TABLE IF NOT EXISTS contract_expiry (
    expiry_id             TEXT PRIMARY KEY,          -- e.g. 'TA35-O-2026-08-27'
    underlying            TEXT NOT NULL,             -- 'TA35'
    expiry_kind           TEXT NOT NULL,             -- weekly | monthly
    expiry_date           TEXT NOT NULL,
    last_trading_date     TEXT NOT NULL,
    settlement_time_local TEXT,
    settlement_rule       TEXT NOT NULL,             -- Description of settlement mechanism
    multiplier_nis        REAL NOT NULL DEFAULT 50.0,
    strike_step           REAL DEFAULT 10.0,
    source                TEXT NOT NULL
);
