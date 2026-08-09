# ADR-001: Lite-only public EOD boundary

## Decision

The system is an end-of-day, read-only volatility dashboard. It ingests only
free public time series and contains no derivative chain, broker, DDE, account,
credential, position or order abstractions.

TASE data uses manual official CSV exports until a documented stable public API
exists. Cboe CSV history may be fetched automatically. SQLite stores immutable,
content-addressed daily runs and nullable analytics with quality flags.

## Consequences

The dashboard is robust enough for regime context but is not real-time and
cannot reproduce skew, option expected move or contract-level positioning.
