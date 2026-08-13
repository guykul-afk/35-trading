"""Unit tests for TA-35 Trade Decision Engine."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from ta35_dashboard.connectors.dde_parser import OptionQuote, ParsedOptionChain
from ta35_dashboard.decision_engine import (
    EngineMode,
    StrategyFamily,
    StrategyRecommendation,
    TradeTicket,
    Verdict,
)
from ta35_dashboard.decision_engine.engine import run_trade_decision_engine


class DecisionEngineTests(unittest.TestCase):
    def test_eod_mode_when_no_chains_provided(self):
        """Verify that when no DDE chains are provided, the engine gracefully degrades to EOD Strategy Mode."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_db.sqlite3"
            result = run_trade_decision_engine(
                spot_price=4150.0,
                prob_up=0.60,
                forecast_rv=0.15,
                current_rv=0.14,
                regime="NORMAL",
                volatility_state="מתכווצת",
                parsed_chains=None,
                db_path=db_path,
            )

            self.assertIsInstance(result, StrategyRecommendation)
            self.assertEqual(result.mode, EngineMode.EOD_GENERAL)
            self.assertEqual(result.verdict, Verdict.GENERAL_STRATEGY)
            self.assertIn(result.primary_strategy_family, (StrategyFamily.BULL_PUT_CREDIT, StrategyFamily.BULL_CALL_DEBIT))
            self.assertTrue(result.requires_chain_validation)
            self.assertIn("strikes", result.unavailable_fields)
            self.assertIn("bid_ask_spreads", result.unavailable_fields)

    def test_full_dde_mode_with_valid_option_chain(self):
        """Verify that when valid DDE chains with quotes are provided, the engine runs FULL_DDE and outputs a TradeTicket."""
        def make_quote(strike: float, cb: float, ca: float, pb: float, pa: float) -> OptionQuote:
            return OptionQuote(
                strike=strike,
                call_bid=cb,
                call_ask=ca,
                call_last=(cb + ca) / 2.0,
                call_bid_size=10.0,
                call_ask_size=10.0,
                call_iv=0.15,
                put_bid=pb,
                put_ask=pa,
                put_last=(pb + pa) / 2.0,
                put_bid_size=10.0,
                put_ask_size=10.0,
                put_iv=0.15,
            )

        quotes = [
            make_quote(4100.0, 60.0, 62.0, 10.0, 12.0),
            make_quote(4110.0, 52.0, 54.0, 15.0, 17.0),
            make_quote(4120.0, 44.0, 46.0, 22.0, 24.0),
            make_quote(4130.0, 36.0, 38.0, 30.0, 32.0),
            make_quote(4140.0, 28.0, 30.0, 40.0, 42.0),
            make_quote(4150.0, 20.0, 22.0, 50.0, 52.0),
            make_quote(4160.0, 14.0, 16.0, 62.0, 64.0),
            make_quote(4170.0, 9.0, 11.0, 75.0, 77.0),
            make_quote(4180.0, 5.0, 7.0, 90.0, 92.0),
        ]
        chain = ParsedOptionChain(
            expiration_label="חודשית (Monthly)",
            days_to_expiration=14.0,
            synthetic_spot=4150.0,
            quotes=quotes,
        )

        with tempfile.TemporaryDirectory() as tmp_dir:
            db_path = Path(tmp_dir) / "test_db.sqlite3"
            result = run_trade_decision_engine(
                spot_price=4150.0,
                prob_up=0.62,
                forecast_rv=0.16,
                current_rv=0.15,
                regime="NORMAL",
                volatility_state="מתכווצת",
                parsed_chains=[chain],
                risk_budget_nis=10000.0,
                db_path=db_path,
            )

            self.assertIsInstance(result, TradeTicket)
            self.assertIn(result.verdict, (Verdict.TRADE, Verdict.WATCH, Verdict.PASS))
            if result.verdict != Verdict.PASS:
                self.assertNotEqual(result.limit_price, 0)
                self.assertGreater(result.max_loss, 0)
                self.assertGreaterEqual(result.size_contracts, 1)
                self.assertGreaterEqual(len(result.legs), 2)

    def test_explicit_engine_modes(self):
        """Verify determine_engine_mode produces explicit statuses."""
        from ta35_dashboard.decision_engine.router import determine_engine_mode
        
        # 1. No chains -> EOD_GENERAL
        mode, warnings = determine_engine_mode(None)
        self.assertEqual(mode, EngineMode.EOD_GENERAL)
        
        # 2. Live executable quotes -> LIVE_EXECUTABLE
        def make_quote(strike: float, cb: float, ca: float, pb: float, pa: float) -> OptionQuote:
            return OptionQuote(
                strike=strike, call_bid=cb, call_ask=ca, call_last=(cb+ca)/2,
                call_bid_size=10, call_ask_size=10, call_iv=0.15,
                put_bid=pb, put_ask=pa, put_last=(pb+pa)/2,
                put_bid_size=10, put_ask_size=10, put_iv=0.15
            )
        quotes_live = [
            make_quote(4100+i*10, 50-i*5, 52-i*5, 10+i*5, 12+i*5) for i in range(5)
        ]
        chain_live = ParsedOptionChain("Monthly", 14.0, 4150.0, quotes_live)
        mode_live, _ = determine_engine_mode([chain_live])
        self.assertEqual(mode_live, EngineMode.LIVE_EXECUTABLE)

        # 3. Static quotes (mid price only, bid=0) -> STATIC_CHAIN_RESEARCH
        def make_static_quote(strike: float, last_p: float) -> OptionQuote:
            return OptionQuote(
                strike=strike, call_bid=0.0, call_ask=0.0, call_last=last_p,
                call_bid_size=0, call_ask_size=0, call_iv=0.15,
                put_bid=0.0, put_ask=0.0, put_last=last_p,
                put_bid_size=0, put_ask_size=0, put_iv=0.15
            )
        quotes_static = [
            make_static_quote(4100+i*10, 25.0) for i in range(5)
        ]
        chain_static = ParsedOptionChain("Monthly", 14.0, 4150.0, quotes_static)
        mode_static, _ = determine_engine_mode([chain_static])
        self.assertEqual(mode_static, EngineMode.STATIC_CHAIN_RESEARCH)

        # 4. Empty quotes list in chain -> RESEARCH_ONLY
        chain_empty = ParsedOptionChain("Monthly", 14.0, 4150.0, [])
        mode_empty, _ = determine_engine_mode([chain_empty])
        self.assertEqual(mode_empty, EngineMode.RESEARCH_ONLY)

    def test_predict_live_direction_zero_confidence(self):
        """Verify predict_live_direction returns 0.50 probability with 0.0 confidence."""
        from ta35_dashboard.analytics.forecasting import predict_live_direction
        prob, conf = predict_live_direction(horizon_days=7)
        self.assertEqual(prob, 0.50)
        self.assertEqual(conf, 0.0)

    def test_opportunity_score_coverage_gate(self):
        """Verify calculate_opportunity_score achieves 100% (1.0) coverage."""
        from ta35_dashboard.decision_engine.gates import calculate_opportunity_score
        from ta35_dashboard.decision_engine.models import CandidateTrade, Expiry, LegQuote
        
        leg1 = LegQuote("CALL", 4100, "BUY", 1, 10.0, 11.0, 11.0, 50.0)
        leg2 = LegQuote("CALL", 4150, "SELL", 1, 5.0, 6.0, 5.0, 50.0)
        cand = CandidateTrade(
            candidate_id="CAND_1",
            strategy_family=StrategyFamily.BULL_CALL_DEBIT,
            strategy_variant="Spread",
            expiry=Expiry("2026-09-01", 14.0),
            legs=(leg1, leg2),
            net_debit_credit=6.0,
            limit_price=6.0,
            max_profit=44.0 * 50,
            max_loss=6.0 * 50,
            breakevens=(4106.0,),
        )
        score, coverage = calculate_opportunity_score(cand, model_ev_after_costs=150.0, estimated_edge=200.0, market_pop=0.55)
        self.assertEqual(coverage, 1.0)


if __name__ == "__main__":
    unittest.main()
