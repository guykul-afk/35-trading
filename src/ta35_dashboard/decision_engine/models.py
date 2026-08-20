"""Data Contracts (DTOs) for TA-35 Trade Decision Engine.

Defines the single source of truth contracts for EOD quantitative decision modeling.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence


class EngineMode(str, Enum):
    EOD_GENERAL = "EOD_GENERAL"
    RESEARCH_ONLY = "RESEARCH_ONLY"


class Verdict(str, Enum):
    TRADE = "TRADE"
    WATCH = "WATCH"
    PASS = "PASS"
    GENERAL_STRATEGY = "GENERAL_STRATEGY"
    NO_STRATEGY = "NO_STRATEGY"


class StrategyFamily(str, Enum):
    # Core Directional
    BULL_CALL_DEBIT = "Bull Call Spread"
    BULL_PUT_CREDIT = "Bull Put Spread"
    BEAR_PUT_DEBIT = "Bear Put Spread"
    BEAR_CALL_CREDIT = "Bear Call Spread"
    
    # Target / Range
    LONG_BUTTERFLY = "Long Butterfly"
    DIRECTIONAL_BUTTERFLY = "Directional Butterfly"
    BROKEN_WING_BUTTERFLY = "Broken-Wing Butterfly"
    IRON_BUTTERFLY = "Iron Butterfly"
    IRON_CONDOR = "Iron Condor"
    DEBIT_CONDOR = "Debit Condor"
    
    # Volatility
    LONG_STRADDLE = "Long Straddle"
    LONG_STRANGLE = "Long Strangle"
    LONG_IRON_BUTTERFLY = "Long Iron Butterfly (Reverse Fly)"
    LONG_REVERSE_IRON_CONDOR = "Long Reverse Iron Condor"
    
    # Time / Term Structure
    CALL_CALENDAR = "Call Calendar"
    PUT_CALENDAR = "Put Calendar"
    DOUBLE_CALENDAR = "Double Calendar"
    CALL_DIAGONAL = "Call Diagonal"
    PUT_DIAGONAL = "Put Diagonal"
    DOUBLE_DIAGONAL = "Double Diagonal"
    
    # Advanced / Conditional Tier C
    CALL_RATIO_BACKSPREAD = "Call Ratio Backspread"
    PUT_RATIO_BACKSPREAD = "Put Ratio Backspread"
    WINGED_RISK_REVERSAL = "Winged Risk Reversal"
    TIME_BUTTERFLY = "Time Butterfly"


@dataclass(frozen=True, slots=True)
class Expiry:
    expiration_date: str
    days_to_expiration: float
    last_trading_date: str | None = None
    settlement_reference: str = "TASE_TA35"
    is_weekly: bool = False
    source: str = "TASE"


@dataclass(frozen=True, slots=True)
class LegQuote:
    option_type: str  # "CALL" or "PUT"
    strike: float
    action: str  # "BUY" or "SELL"
    ratio: int = 1
    bid: float = 0.0
    ask: float = 0.0
    executable_price: float = 0.0
    contract_multiplier: float = 50.0  # TASE TA-35 standard multiplier (NIS)


@dataclass(frozen=True, slots=True)
class ModelDistribution:
    model_id: str
    direction_probability: float  # P(up)
    forecast_rv: float  # Forecast annualized realized volatility
    expected_move: float
    quantiles: dict[float, float] = field(default_factory=dict)
    confidence: float = 0.8
    regime: str = "NORMAL"


@dataclass(frozen=True, slots=True)
class StrategyRecommendation:
    # Mode & Freshness
    mode: EngineMode
    as_of_date: str
    data_freshness: str
    
    # Market View
    direction_view: str  # e.g., "שורי (Bullish)", "דובי (Bearish)", "נייטרלי"
    direction_probability: float
    volatility_view: str  # e.g., "ציפייה לירידת תנודתיות", "ציפייה לעליית תנודתיות"
    regime: str
    forecast_rv: float
    
    # Recommendation
    verdict: Verdict
    primary_strategy_family: StrategyFamily
    alternatives: tuple[StrategyFamily, ...]
    horizon_days: int
    rationale: str
    
    # Scenario
    probability_band: tuple[float, float]
    target_range: tuple[float, float]
    invalidation_level: float
    
    # Confidence & Execution
    forecast_confidence: float
    data_quality_score: float
    warnings: tuple[str, ...]
    
    # Audit
    snapshot_id: str
    model_version: str
    rules_version: str
    estimated_legs: tuple[dict[str, Any], ...] = ()


@dataclass(frozen=True, slots=True)
class CandidateTrade:
    candidate_id: str
    strategy_family: StrategyFamily
    strategy_variant: str
    expiry: Expiry
    legs: tuple[LegQuote, ...]
    net_debit_credit: float
    limit_price: float
    max_profit: float
    max_loss: float
    breakevens: tuple[float, ...]
    delta: float = 0.0
    gamma: float = 0.0
    vega: float = 0.0
    theta: float = 0.0
    margin_required: float = 0.0
    has_defined_risk: bool = True


@dataclass(frozen=True, slots=True)
class MarketDistribution:
    market_rnd_id: str
    market_pop: float
    implied_volatility: float
    skew_metric: float = 0.0
    term_structure_slope: float = 0.0


TradeTicket = StrategyRecommendation


