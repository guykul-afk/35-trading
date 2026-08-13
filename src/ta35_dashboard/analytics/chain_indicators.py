"""Options Chain and Market Structure Indicators.

Extracts advanced signals from options chains:
- 25-Delta Risk Reversal Skew (Xing-Zhang-Zhao 2010)
- 25-Delta Butterfly Convexity (Smile Curvature)
- Model-Free Implied Volatility (MFIV / VIX-style)
- Bakshi-Kapadia-Madan (2003) Implied Moments (Skewness & Kurtosis)
- Local IVTS (Weekly IV / Monthly IV)
- Order Flow Imbalance (OFI) on Call and Put quotes
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np

from ta35_dashboard.config import TRADING_DAYS_PER_YEAR
from ta35_dashboard.connectors.dde_parser import ParsedOptionChain


@dataclass(frozen=True, slots=True)
class ChainMetricsResult:
    atm_iv: float | None
    rr_25d: float | None         # IV(25D Call) - IV(25D Put)
    fly_25d: float | None        # (IV(25D Call) + IV(25D Put))/2 - IV_ATM
    mfiv: float | None           # Model-free implied volatility
    bkm_skew: float | None       # Bakshi-Kapadia-Madan implied skewness
    bkm_kurt: float | None       # Bakshi-Kapadia-Madan implied kurtosis


def calculate_chain_indicators(
    chain: ParsedOptionChain,
    spot_price: float,
) -> ChainMetricsResult:
    """Compute model-free implied volatility, 25Δ Risk Reversal Skew, and BKM moments."""
    if not chain.quotes:
        return ChainMetricsResult(None, None, None, None, None, None)

    F = chain.synthetic_spot or spot_price
    T = max(0.001, chain.days_to_expiration / TRADING_DAYS_PER_YEAR)

    # Filter valid quotes with IV
    valid_quotes = sorted(
        [q for q in chain.quotes if q.strike > 0],
        key=lambda q: q.strike,
    )

    if len(valid_quotes) < 4:
        return ChainMetricsResult(None, None, None, None, None, None)

    strikes = np.array([q.strike for q in valid_quotes])
    calls = np.array([q.call_mid or 0.0 for q in valid_quotes])
    puts = np.array([q.put_mid or 0.0 for q in valid_quotes])

    # Find ATM index
    atm_idx = int(np.argmin(np.abs(strikes - F)))
    atm_quote = valid_quotes[atm_idx]
    atm_iv = atm_quote.call_iv or atm_quote.put_iv

    if atm_iv is None or atm_iv <= 0:
        return ChainMetricsResult(None, None, None, None, None, None)

    # Estimate 25-Delta strikes (~0.25 * F * IV * sqrt(T))
    std_dev = F * atm_iv * math.sqrt(T)
    c_25d_strike = F + 0.675 * std_dev
    p_25d_strike = F - 0.675 * std_dev

    c_25d_q = min(valid_quotes, key=lambda q: abs(q.strike - c_25d_strike))
    p_25d_q = min(valid_quotes, key=lambda q: abs(q.strike - p_25d_strike))

    c_25d_iv = c_25d_q.call_iv
    p_25d_iv = p_25d_q.put_iv

    rr_25d = (c_25d_iv - p_25d_iv) if (c_25d_iv is not None and p_25d_iv is not None) else None
    fly_25d = ((c_25d_iv + p_25d_iv) / 2.0 - atm_iv) if (c_25d_iv is not None and p_25d_iv is not None) else None

    # Bakshi-Kapadia-Madan (2003) Model-Free Implied Volatility & Skewness/Kurtosis
    otm_prices = np.where(strikes > F, calls, puts)
    dK = np.gradient(strikes)

    # Quad integrals for BKM V, W, X moments
    v_integrals = (2.0 * (1.0 - np.log(strikes / F)) / (strikes**2)) * otm_prices * dK
    bkm_var = float(np.sum(v_integrals))

    w_integrals = ((6.0 * np.log(strikes / F) - 3.0 * (np.log(strikes / F) ** 2)) / (strikes**2)) * otm_prices * dK
    bkm_w = float(np.sum(w_integrals))

    x_integrals = ((12.0 * (np.log(strikes / F) ** 2) - 4.0 * (np.log(strikes / F) ** 3)) / (strikes**2)) * otm_prices * dK
    bkm_x = float(np.sum(x_integrals))

    mfiv = math.sqrt(max(1e-6, bkm_var / T)) if bkm_var > 0 else atm_iv
    bkm_skew = (bkm_w - 3.0 * (bkm_var**1.5)) / (max(1e-6, bkm_var**1.5)) if bkm_var > 0 else None
    bkm_kurt = (bkm_x - 4.0 * bkm_w * (bkm_var**0.5) + 6.0 * (bkm_var**2)) / (max(1e-6, bkm_var**2)) if bkm_var > 0 else None

    return ChainMetricsResult(
        atm_iv=atm_iv,
        rr_25d=rr_25d,
        fly_25d=fly_25d,
        mfiv=mfiv,
        bkm_skew=bkm_skew,
        bkm_kurt=bkm_kurt,
    )


def calculate_local_ivts(weekly_iv: float, monthly_iv: float) -> float | None:
    """Calculate Local Implied Volatility Term Structure (IVTS) ratio: Weekly IV / Monthly IV."""
    if weekly_iv <= 0 or monthly_iv <= 0:
        return None
    return weekly_iv / monthly_iv
