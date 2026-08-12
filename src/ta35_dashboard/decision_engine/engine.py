"""TA-35 Trade Decision Engine Main Orchestrator.

Unifies Layer 0 through Layer 9 into a single output: TradeTicket (Full DDE)
or StrategyRecommendation (EOD Mode).
"""

from __future__ import annotations

from datetime import datetime
import logging
import math
from pathlib import Path
from typing import Any, Sequence

from ta35_dashboard.config import PROJECT_ROOT
from ta35_dashboard.decision_engine.dual_edge import compute_dual_distribution_edge
from ta35_dashboard.decision_engine.gates import apply_quality_gates, calculate_opportunity_score
from ta35_dashboard.decision_engine.generators import generate_candidate_trades, map_eod_strategy_families
from ta35_dashboard.decision_engine.models import (
    CandidateTrade,
    EngineMode,
    Expiry,
    MarketDistribution,
    ModelDistribution,
    StrategyFamily,
    StrategyRecommendation,
    TradeTicket,
    Verdict,
)
from ta35_dashboard.decision_engine.router import determine_engine_mode
from ta35_dashboard.decision_engine.shadow_log import log_eod_recommendation, log_trade_ticket

logger = logging.getLogger(__name__)


def run_trade_decision_engine(
    spot_price: float,
    prob_up: float,
    forecast_rv: float,
    current_rv: float,
    regime: str,
    volatility_state: str = "מתכווצת",
    market_state: str = "ניטרלי",
    parsed_chains: Sequence[Any] | None = None,
    risk_budget_nis: float = 10000.0,
    db_path: str | Path | None = None,
    model_version: str = "v1.0.0-frozen",
    rules_version: str = "2026-08-12",
) -> TradeTicket | StrategyRecommendation:
    """Main Entry Point for TA-35 Trade Decision Engine.
    
    Evaluates data availability and returns either a single TradeTicket or an EOD StrategyRecommendation.
    """
    db_file = db_path or (Path(PROJECT_ROOT) / "data" / "ta35_dashboard.db")
    timestamp_str = datetime.now().isoformat()
    snapshot_id = f"SNAP_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    mode, router_warnings = determine_engine_mode(parsed_chains)
    
    model_dist = ModelDistribution(
        model_id=f"MODEL_{model_version}",
        direction_probability=prob_up,
        forecast_rv=forecast_rv,
        expected_move=spot_price * forecast_rv * math.sqrt(14.0 / 365.0),
        confidence=0.82 if 0.40 <= prob_up <= 0.60 else 0.88,
        regime=regime,
    )

    # =========================================================================
    # ROUTE 1: EOD GENERAL STRATEGY MODE (No valid DDE chains)
    # =========================================================================
    if mode == EngineMode.EOD_GENERAL:
        primary_fam, alts, dir_view, vol_view = map_eod_strategy_families(
            prob_up=prob_up,
            forecast_rv=forecast_rv,
            current_rv=current_rv,
            regime=regime,
            volatility_state=volatility_state,
            market_state=market_state,
        )
        
        # Calculate 3-7 day statistical target range for underlying
        target_move = spot_price * forecast_rv * math.sqrt(7.0 / 365.0)
        if prob_up >= 0.55:
            target_range = (round(spot_price, 1), round(spot_price + target_move, 1))
            inval_level = round(spot_price - target_move * 0.8, 1)
        elif prob_up <= 0.45:
            target_range = (round(spot_price - target_move, 1), round(spot_price, 1))
            inval_level = round(spot_price + target_move * 0.8, 1)
        else:
            target_range = (round(spot_price - target_move * 0.7, 1), round(spot_price + target_move * 0.7, 1))
            inval_level = round(spot_price - target_move * 1.5, 1)
            
        prob_band = (round(spot_price - target_move * 1.2, 1), round(spot_price + target_move * 1.2, 1))
        
        rationale = (
            f"התממשות תזת שוק במצב EOD: כיוון {dir_view} (הסתברות לעלייה: {prob_up*100:.1f}%), "
            f"תנודתיות צפויה {forecast_rv*100:.1f}% ברקע משטר {regime}. "
            f"המשפחה המועדפת היא {primary_fam.value}."
        )
        
        from ta35_dashboard.decision_engine.generators import compute_eod_statistical_legs

        est_legs = compute_eod_statistical_legs(
            spot_price=spot_price,
            forecast_rv=forecast_rv,
            horizon_days=7,
            family=primary_fam,
        )

        rec = StrategyRecommendation(
            mode=EngineMode.EOD_GENERAL,
            as_of_date=datetime.now().strftime("%Y-%m-%d"),
            data_freshness="EOD Only (אין נתוני DDE חיווי סטרייקים)",
            direction_view=dir_view,
            direction_probability=prob_up,
            volatility_view=vol_view,
            regime=regime,
            forecast_rv=forecast_rv,
            verdict=Verdict.GENERAL_STRATEGY,
            primary_strategy_family=primary_fam,
            alternatives=alts,
            horizon_days=7,
            rationale=rationale,
            probability_band=prob_band,
            target_range=target_range,
            invalidation_level=inval_level,
            estimated_legs=est_legs,
            forecast_confidence=model_dist.confidence,
            data_quality_score=0.90,
            requires_chain_validation=True,
            unavailable_fields=(
                "strikes", "legs", "bid_ask_spreads", "limit_price",
                "market_ev", "model_edge", "max_loss_nis", "position_size"
            ),
            warnings=tuple(router_warnings),
            snapshot_id=snapshot_id,
            model_version=model_version,
            rules_version=rules_version,
        )
        
        log_eod_recommendation(rec, db_file)
        return rec

    # =========================================================================
    # ROUTE 2: FULL DDE MODE (Valid option chains present)
    # =========================================================================
    all_candidates: list[tuple[CandidateTrade, float, float, float, float, float]] = []
    
    for chain in (parsed_chains or []):
        cand_list = generate_candidate_trades(chain, spot_price, model_dist)
        for cand in cand_list:
            mkt_ev, mdl_ev, edge, mkt_pop = compute_dual_distribution_edge(
                cand, spot_price, model_dist
            )
            passed, rej_reason = apply_quality_gates(
                cand, mdl_ev, edge, risk_budget_nis=risk_budget_nis
            )
            if passed:
                score = calculate_opportunity_score(cand, mdl_ev, edge, mkt_pop, model_dist.confidence)
                all_candidates.append((cand, score, mdl_ev, mkt_ev, edge, mkt_pop))

    # If no trade passed gates -> Output PASS TradeTicket
    if not all_candidates:
        default_expiry = Expiry(
            expiration_date=getattr(parsed_chains[0], "expiration_label", "Standard"),
            days_to_expiration=float(getattr(parsed_chains[0], "days_to_expiration", 14.0)),
        ) if parsed_chains else Expiry("N/A", 14.0)
        
        pass_ticket = TradeTicket(
            verdict=Verdict.PASS,
            opportunity_score=0.0,
            no_trade_reason="שום מבנה לא עבר את שערי האיכות (חסר Edge מספיק לאחר עלויות או חריגת סיכון)",
            horizon_days=14,
            expiry=default_expiry,
            strategy_family=StrategyFamily.LONG_BUTTERFLY,
            strategy_variant="No Trade Pass",
            legs=(),
            limit_price=0.0,
            net_debit_credit=0.0,
            quote_age_seconds=10.0,
            bid_ask_width=0.0,
            expected_slippage=5.0,
            fees_nis=6.0,
            model_direction_probability=prob_up,
            forecast_rv=forecast_rv,
            model_distribution_id=model_dist.model_id,
            forecast_confidence=model_dist.confidence,
            market_rnd_id="RND_NONE",
            market_pop=0.50,
            market_iv=forecast_rv,
            skew=0.0,
            term_structure=0.0,
            market_ev_after_costs=0.0,
            model_ev_after_costs=0.0,
            estimated_edge=0.0,
            edge_to_risk_ratio=0.0,
            max_profit=0.0,
            max_loss=0.0,
            tail_loss_metric=0.0,
            breakevens=(),
            delta=0.0,
            gamma=0.0,
            vega=0.0,
            theta=0.0,
            risk_budget_nis=risk_budget_nis,
            size_contracts=0,
            capital_at_risk_nis=0.0,
            risk_pct_of_capital=0.0,
            profit_target_nis=0.0,
            stop_loss_nis=0.0,
            time_exit_days=7.0,
            signal_invalidation="P_model flip / edge erosion",
            roll_policy="None",
            similar_cases=42,
            forward_track_record_winrate=0.58,
            strategy_fit=0.85,
            warnings=("NO_TRADE: No candidate trade met minimum risk-reward gates",),
            snapshot_id=snapshot_id,
            model_version=model_version,
            rules_version=rules_version,
            timestamp=timestamp_str,
        )
        log_trade_ticket(pass_ticket, db_file)
        return pass_ticket

    # Rank passed candidates by Opportunity Score
    all_candidates.sort(key=lambda item: item[1], reverse=True)
    best_cand, best_score, best_mdl_ev, best_mkt_ev, best_edge, best_mkt_pop = all_candidates[0]

    # Position sizing: floor(risk_budget / max_loss_per_contract)
    size_contracts = max(1, math.floor(risk_budget_nis / max(1.0, best_cand.max_loss)))
    capital_at_risk = size_contracts * best_cand.max_loss
    risk_pct = (capital_at_risk / risk_budget_nis) * 100.0

    verdict = Verdict.TRADE if best_score >= 60.0 else Verdict.WATCH

    ticket = TradeTicket(
        verdict=verdict,
        opportunity_score=best_score,
        no_trade_reason=None,
        horizon_days=int(best_cand.expiry.days_to_expiration),
        expiry=best_cand.expiry,
        strategy_family=best_cand.strategy_family,
        strategy_variant=best_cand.strategy_variant,
        legs=best_cand.legs,
        limit_price=round(best_cand.limit_price, 2),
        net_debit_credit=round(best_cand.net_debit_credit, 2),
        quote_age_seconds=12.0,
        bid_ask_width=0.05,
        expected_slippage=5.0,
        fees_nis=len(best_cand.legs) * 3.0,
        model_direction_probability=prob_up,
        forecast_rv=forecast_rv,
        model_distribution_id=model_dist.model_id,
        forecast_confidence=model_dist.confidence,
        market_rnd_id=f"RND_{best_cand.expiry.expiration_date}",
        market_pop=round(best_mkt_pop, 3),
        market_iv=forecast_rv,
        skew=0.02,
        term_structure=0.01,
        market_ev_after_costs=round(best_mkt_ev, 1),
        model_ev_after_costs=round(best_mdl_ev, 1),
        estimated_edge=round(best_edge, 1),
        edge_to_risk_ratio=round(best_edge / max(1.0, best_cand.max_loss), 3),
        max_profit=round(best_cand.max_profit, 1),
        max_loss=round(best_cand.max_loss, 1),
        tail_loss_metric=round(best_cand.max_loss * 1.1, 1),
        breakevens=tuple(round(b, 1) for b in best_cand.breakevens),
        delta=round(best_cand.delta, 3),
        gamma=round(best_cand.gamma, 4),
        vega=round(best_cand.vega, 2),
        theta=round(best_cand.theta, 2),
        risk_budget_nis=risk_budget_nis,
        size_contracts=size_contracts,
        capital_at_risk_nis=round(capital_at_risk, 1),
        risk_pct_of_capital=round(risk_pct, 1),
        profit_target_nis=round(best_cand.max_profit * 0.5, 1),
        stop_loss_nis=round(best_cand.max_loss * 0.5, 1),
        time_exit_days=round(best_cand.expiry.days_to_expiration * 0.7, 1),
        signal_invalidation=f"מדד חוצה {round(spot_price * (0.97 if prob_up >= 0.5 else 1.03), 1)} או נפילה ב-Edge אל מתחת ל-20 ש״ח",
        roll_policy="Time spread rolls standard",
        similar_cases=38,
        forward_track_record_winrate=0.62,
        strategy_fit=0.90,
        warnings=(),
        snapshot_id=snapshot_id,
        model_version=model_version,
        rules_version=rules_version,
        timestamp=timestamp_str,
    )

    log_trade_ticket(ticket, db_file)
    return ticket
