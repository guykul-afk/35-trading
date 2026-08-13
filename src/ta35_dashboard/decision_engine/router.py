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
    max_quote_age_seconds: float = 86400.0,
) -> tuple[EngineMode, list[str]]:
    """Inspects parsed option chains to route the engine execution mode.
    
    Returns:
        tuple[EngineMode, list[str]]: The mode and any warnings/reasons.
    """
    import time
    
    warnings: list[str] = []
    
    if not parsed_chains:
        warnings.append("No options chain data available (DDE status: UNAVAILABLE). Switching to EOD Strategy Mode.")
        return EngineMode.EOD_GENERAL, warnings

    valid_chains = 0
    static_chains = 0
    now = time.time()
    
    for chain in parsed_chains:
        quotes = getattr(chain, "quotes", None)
        if quotes and len(quotes) > 0:
            two_sided_live = 0
            has_price_count = 0
            
            for q in quotes:
                # Check quote freshness if timestamp is available
                q_time = getattr(q, "timestamp", None)
                if q_time is not None:
                    try:
                        age = now - q_time.timestamp()
                        if age > max_quote_age_seconds:
                            continue
                    except Exception:
                        pass
                
                c_bid = getattr(q, "call_bid", 0) or 0
                c_ask = getattr(q, "call_ask", 0) or 0
                c_mid = getattr(q, "call_mid", 0) or 0
                p_bid = getattr(q, "put_bid", 0) or 0
                p_ask = getattr(q, "put_ask", 0) or 0
                p_mid = getattr(q, "put_mid", 0) or 0
                
                has_live_call = c_bid > 0 and c_ask > c_bid and ((c_ask - c_bid) / c_bid) < 0.50
                has_live_put = p_bid > 0 and p_ask > p_bid and ((p_ask - p_bid) / p_bid) < 0.50
                
                if has_live_call or has_live_put:
                    two_sided_live += 1
                
                if c_mid > 0 or p_mid > 0 or c_bid > 0 or p_bid > 0:
                    has_price_count += 1
            
            if two_sided_live >= 4:
                valid_chains += 1
            elif has_price_count >= 4:
                static_chains += 1

    if valid_chains > 0:
        logger.info("Validated %d active live option chain(s). Mode: FULL_DDE", valid_chains)
        return EngineMode.FULL_DDE, warnings

    if static_chains > 0:
        logger.info("Validated %d static/pre-market option chain(s). Mode: FULL_DDE (Pre-Market / Mid Prices)", static_chains)
        warnings.append("DDE קבצים נטענו (טרום מסחר / ציטוטים סטטיים) — תמחור הרגליים מבוסס על מחירי אמצע/סגירה.")
        return EngineMode.FULL_DDE, warnings

    warnings.append("Options chain files found but contain no usable strike price quotes. Switching to EOD Strategy Mode.")
    return EngineMode.EOD_GENERAL, warnings
