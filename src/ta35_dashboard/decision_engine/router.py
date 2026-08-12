"""Data Availability Router.

Determines whether the engine operates in FULL_DDE mode (valid option chain with quotes)
or EOD_GENERAL mode (graceful degradation using EOD indicators only).
"""

from __future__ import annotations

import logging
from typing import Any, Sequence

from ta35_dashboard.decision_engine.models import EngineMode

logger = logging.getLogger(__name__)


def determine_engine_mode(
    parsed_chains: Sequence[Any] | None,
    max_quote_age_seconds: float = 3600.0,
) -> tuple[EngineMode, list[str]]:
    """Inspects parsed option chains to route the engine execution mode.
    
    Returns:
        tuple[EngineMode, list[str]]: The mode and any warnings/reasons.
    """
    warnings: list[str] = []
    
    if not parsed_chains:
        warnings.append("No options chain data available (DDE status: UNAVAILABLE). Switching to EOD Strategy Mode.")
        return EngineMode.EOD_GENERAL, warnings

    valid_chains = 0
    for chain in parsed_chains:
        quotes = getattr(chain, "quotes", None)
        if quotes and len(quotes) > 0:
            # Check if quotes have two-sided market (bid/ask)
            two_sided = sum(1 for q in quotes if (getattr(q, "call_bid", 0) or 0) > 0 or (getattr(q, "put_bid", 0) or 0) > 0)
            if two_sided > 0:
                valid_chains += 1

    if valid_chains == 0:
        warnings.append("Options chain files found but contain no valid two-sided quotes. Switching to EOD Strategy Mode.")
        return EngineMode.EOD_GENERAL, warnings

    logger.info("Validated %d active option chain(s). Mode: FULL_DDE", valid_chains)
    return EngineMode.FULL_DDE, warnings
