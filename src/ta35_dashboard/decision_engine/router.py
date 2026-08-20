"""EOD Data Validation and Mode Router.

Validates that end-of-day statistical inputs are present and determines engine readiness.
"""

from __future__ import annotations

import logging
from typing import Sequence

from ta35_dashboard.decision_engine.models import EngineMode

logger = logging.getLogger(__name__)


def determine_engine_mode(
    spot_price: float | None = None,
    prob_up: float | None = None,
    forecast_rv: float | None = None,
) -> tuple[EngineMode, list[str]]:
    """Validates EOD parameters to determine engine readiness.
    
    Returns:
        tuple[EngineMode, list[str]]: The engine mode and any warnings.
    """
    warnings: list[str] = []
    
    if spot_price is None or spot_price <= 0:
        warnings.append("Spot price is unavailable or invalid.")
        return EngineMode.RESEARCH_ONLY, warnings
        
    if forecast_rv is None or forecast_rv <= 0:
        warnings.append("Forecast volatility is unavailable.")
        return EngineMode.RESEARCH_ONLY, warnings

    return EngineMode.EOD_GENERAL, warnings
