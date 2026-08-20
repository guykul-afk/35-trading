"""Options Chain and Market Structure Indicators.

Provides standard quantitative metrics for implied volatility term structure and skew.
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


@dataclass(frozen=True, slots=True)
class ChainMetricsResult:
    atm_iv: float | None
    rr_25d: float | None         # IV(25D Call) - IV(25D Put)
    fly_25d: float | None        # (IV(25D Call) + IV(25D Put))/2 - IV_ATM
    mfiv: float | None           # Model-free implied volatility
    bkm_skew: float | None       # Bakshi-Kapadia-Madan implied skewness
    bkm_kurt: float | None       # Bakshi-Kapadia-Madan implied kurtosis


def calculate_local_ivts(weekly_iv: float, monthly_iv: float) -> float | None:
    """Calculate Local Implied Volatility Term Structure (IVTS) ratio: Weekly IV / Monthly IV."""
    if weekly_iv <= 0 or monthly_iv <= 0:
        return None
    return weekly_iv / monthly_iv
