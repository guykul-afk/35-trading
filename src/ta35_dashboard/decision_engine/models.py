"""Data Contracts (DTOs) for TA-35 Trade Decision Engine.

Defines the single source of truth contracts for Layer 0 through Layer 9,
including TradeTicket (Full DDE) and StrategyRecommendation (EOD Mode).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Sequence


class EngineMode(str, Enum):
    FULL_DDE = "FULL_DDE"
    EOD_GENERAL = "EOD_GENERAL"


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
    quantiles: dict[float, float] = field(default_factory=dict)  # e.g., {0.1: price, 0.5: price, 0.9: price}
    confidence: float = 0.8
    regime: str = "NORMAL"


@dataclass(frozen=True, slots=True)
class MarketDistribution:
    market_rnd_id: str
    market_pop: float  # Risk-neutral Probability of Profit
    implied_volatility: float
    skew_metric: float = 0.0
    term_structure_slope: float = 0.0


@dataclass(frozen=True, slots=True)
class CandidateTrade:
    candidate_id: str
    strategy_family: StrategyFamily
    strategy_variant: str
    expiry: Expiry
    legs: tuple[LegQuote, ...]
    net_debit_credit: float  # Positive = Debit, Negative = Credit
    limit_price: float
    max_profit: float
    max_loss: float  # Must be finite for production defined-risk
    breakevens: tuple[float, ...]
    delta: float = 0.0
    gamma: float = 0.0
    vega: float = 0.0
    theta: float = 0.0
    margin_required: float = 0.0
    has_defined_risk: bool = True


@dataclass(frozen=True, slots=True, kw_only=True)
class TradeTicket:
    # 1. Decision
    verdict: Verdict
    opportunity_score: float
    no_trade_reason: str | None
    horizon_days: int
    expiry: Expiry
    
    # 2. Structure
    strategy_family: StrategyFamily
    strategy_variant: str
    legs: tuple[LegQuote, ...]
    
    # 3. Execution
    limit_price: float
    net_debit_credit: float
    quote_age_seconds: float | None = None
    bid_ask_width: float | None = None
    expected_slippage: float = 5.0
    fees_nis: float = 0.0
    
    # 4. Forecast
    model_direction_probability: float
    forecast_rv: float
    model_distribution_id: str
    forecast_confidence: float
    
    # 5. Market
    market_rnd_id: str
    market_pop: float
    market_iv: float
    skew: float | None = None
    term_structure: float | None = None
    
    # 6. Edge
    market_ev_after_costs: float
    model_ev_after_costs: float
    estimated_edge: float
    edge_to_risk_ratio: float
    
    # 7. Risk
    max_profit: float
    max_loss: float
    tail_loss_metric: float
    breakevens: tuple[float, ...]
    delta: float
    gamma: float
    vega: float
    theta: float
    
    # 8. Sizing
    risk_budget_nis: float
    size_contracts: int
    capital_at_risk_nis: float
    risk_pct_of_capital: float
    
    # 9. Lifecycle
    profit_target_nis: float
    stop_loss_nis: float
    time_exit_days: float
    signal_invalidation: str
    roll_policy: str
    
    # 10. Evidence & Audit
    similar_cases: int | None = None
    forward_track_record_winrate: float | None = None
    strategy_fit: float | None = None
    warnings: tuple[str, ...] = ()
    snapshot_id: str = ""
    model_version: str = ""
    rules_version: str = ""
    timestamp: str = ""


@dataclass(frozen=True, slots=True)
class StrategyRecommendation:
    # Mode & Freshness
    mode: EngineMode  # Always EOD_GENERAL
    as_of_date: str
    data_freshness: str
    
    # Market View
    direction_view: str  # e.g., "BULLISH", "BEARISH", "NEUTRAL"
    direction_probability: float
    volatility_view: str  # e.g., "HIGH_VOL", "LOW_VOL", "STABLE"
    regime: str
    forecast_rv: float
    
    # Recommendation
    verdict: Verdict  # GENERAL_STRATEGY, WATCH, NO_STRATEGY
    primary_strategy_family: StrategyFamily
    alternatives: tuple[StrategyFamily, ...]
    horizon_days: int
    rationale: str
    
    # Scenario
    probability_band: tuple[float, float]
    target_range: tuple[float, float]
    invalidation_level: float
    
    # Confidence & Restrictions
    forecast_confidence: float
    data_quality_score: float
    requires_chain_validation: bool  # Always True
    unavailable_fields: tuple[str, ...]
    warnings: tuple[str, ...]
    
    # Audit
    snapshot_id: str
    model_version: str
    rules_version: str
    estimated_legs: tuple[dict[str, Any], ...] = ()
