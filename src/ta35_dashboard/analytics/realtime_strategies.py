"""Real-Time Option Strategy Engine.

Prices candidate option strategies (vertical spreads, straddles, and inter-expiration calendar spreads)
using actual live option chain Bid/Ask and Mid quotes. Uses official TASE contract multiplier of 50 NIS/point.
Calculates Risk-Neutral Density (RND) via Breeden-Litzenberger for true Probability of Profit (POP) and Expected Value (EV).
"""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np
from typing import Any

from ta35_dashboard.connectors.dde_parser import ParsedOptionChain, OptionQuote
from ta35_dashboard.analytics.implied_vol import bs_call_price, bs_put_price


@dataclass(frozen=True, slots=True)
class RealtimeLeg:
    action: str  # 'Buy' or 'Sell'
    option_type: str  # 'Call' or 'Put'
    strike: float
    bid: float | None
    ask: float | None
    mid: float | None
    exec_price: float
    label: str


@dataclass(frozen=True, slots=True)
class RealtimeStrategyProposal:
    strategy_name: str
    horizon_days: int
    net_credit_debit: float  # Positive = Net Credit, Negative = Net Debit (points)
    net_credit_debit_nis: float  # Net Credit/Debit in NIS (points * 50)
    max_profit_nis: float
    max_loss_nis: float
    risk_reward_ratio: float
    breakeven_points: tuple[float, ...]
    probability_of_profit: float
    expected_value_nis: float
    legs: tuple[RealtimeLeg, ...]
    rationale: str
    quality_label: str

    @property
    def is_credit(self) -> bool:
        return self.net_credit_debit > 0


@dataclass(frozen=True, slots=True)
class CalendarSpreadProposal:
    strategy_name: str
    strike: float
    short_expiration_days: float
    long_expiration_days: float
    option_type: str  # 'Call' or 'Put'
    short_leg_exec_price: float  # Weekly Bid (pts)
    long_leg_exec_price: float  # Monthly Ask (pts)
    net_debit_pts: float
    net_debit_nis: float
    estimated_max_profit_nis: float
    time_decay_ratio: float
    iv_diff_pct: float  # IV_weekly - IV_monthly
    rationale: str
    quality_label: str
    legs: tuple[RealtimeLeg, ...]


def _get_clean_exec_price(
    quote: OptionQuote, option_type: str, action: str
) -> float | None:
    """Extract realistic execution price taking actual Bid/Ask or Mid with slippage penalty."""
    if option_type.lower() == "put":
        bid, ask, mid = quote.put_bid, quote.put_ask, quote.put_mid
    else:
        bid, ask, mid = quote.call_bid, quote.call_ask, quote.call_mid

    if mid is None or mid <= 0:
        return None

    spread = (ask - bid) if (ask is not None and bid is not None and ask >= bid) else 0.1 * mid
    slippage = 0.25 * spread

    if action.lower() == "buy":
        if ask is not None and ask > 0:
            return ask
        return mid + slippage
    else:  # Sell
        if bid is not None and bid > 0:
            return bid
        return max(0.01, mid - slippage)


def compute_rnd_distribution(
    chain: ParsedOptionChain,
    spot_price: float,
    implied_vol: float = 0.15,
) -> tuple[np.ndarray, np.ndarray]:
    """Compute Risk-Neutral Density (RND) via Breeden-Litzenberger (2nd derivative of Call prices wrt Strike).

    Returns:
        Tuple of (strikes_grid, pdf_grid)
    """
    F = chain.synthetic_spot or spot_price
    T = max(0.001, chain.days_to_expiration / 365.0)
    std_dev = F * implied_vol * math.sqrt(T)

    # Grid covering +/- 3.5 std dev around forward price
    grid_min = max(100.0, F - 3.5 * std_dev)
    grid_max = F + 3.5 * std_dev
    grid = np.linspace(grid_min, grid_max, 200)
    dK = grid[1] - grid[0]

    # Attempt Breeden-Litzenberger from market Call quotes if at least 4 quotes exist
    valid_quotes = sorted(
        [q for q in chain.quotes if q.call_mid is not None and q.call_mid > 0],
        key=lambda q: q.strike,
    )

    if len(valid_quotes) >= 4:
        mkt_strikes = np.array([q.strike for q in valid_quotes])
        mkt_calls = np.array([q.call_mid for q in valid_quotes])

        # Interpolate call prices on fine grid
        interp_calls = np.interp(grid, mkt_strikes, mkt_calls, left=np.nan, right=0.0)
        
        # Extrapolate outside market strikes using Black-76
        left_mask = np.isnan(interp_calls)
        if np.any(left_mask):
            interp_calls[left_mask] = [bs_call_price(F, K, T, 0.0, implied_vol) for K in grid[left_mask]]

        # Second numerical derivative
        d2c = np.gradient(np.gradient(interp_calls, dK), dK)
        pdf = np.maximum(0.0, d2c)
        
        total_prob = np.sum(pdf) * dK
        if total_prob > 1e-6:
            pdf /= total_prob
            return grid, pdf

    # Fallback to Lognormal / Normal RND around Forward F
    pdf = (1.0 / (std_dev * math.sqrt(2.0 * math.pi))) * np.exp(-0.5 * ((grid - F) / std_dev) ** 2)
    pdf /= (np.sum(pdf) * dK)
    return grid, pdf


def price_realtime_strategies(
    chain: ParsedOptionChain,
    spot_price: float,
    prob_rise: float = 0.50,
    implied_vol: float = 0.15,
    contract_multiplier: float = 50.0,
    fee_per_leg_nis: float = 2.5,
) -> list[RealtimeStrategyProposal]:
    """Price candidate strategies on live option chain quotes with true RND-based POP and EV."""
    if not chain.quotes or spot_price <= 0:
        return []

    quote_map: dict[float, OptionQuote] = {q.strike: q for q in chain.quotes}
    strikes = sorted(quote_map.keys())

    if len(strikes) < 4:
        return []

    horizon = int(round(chain.days_to_expiration))
    effective_spot = chain.synthetic_spot or spot_price
    std_move = effective_spot * implied_vol * math.sqrt(horizon / 365.0)

    # Compute RND PDF over strike grid
    grid, pdf = compute_rnd_distribution(chain, spot_price=effective_spot, implied_vol=implied_vol)
    dK = grid[1] - grid[0]

    def find_nearest_strike(target: float, available_strikes: list[float]) -> float:
        return min(available_strikes, key=lambda s: abs(s - target))

    valid_puts = [s for s in strikes if quote_map[s].put_mid is not None]
    valid_calls = [s for s in strikes if quote_map[s].call_mid is not None]

    proposals: list[RealtimeStrategyProposal] = []

    # 1. Bull Put Spread
    if len(valid_puts) >= 2:
        sp_k = find_nearest_strike(effective_spot - 0.2 * std_move, valid_puts)
        lp_candidates = [s for s in valid_puts if s < sp_k]
        if lp_candidates:
            lp_k = find_nearest_strike(sp_k - 0.6 * std_move, lp_candidates)
            sp_q, lp_q = quote_map[sp_k], quote_map[lp_k]

            sp_price = _get_clean_exec_price(sp_q, "put", "sell")
            lp_price = _get_clean_exec_price(lp_q, "put", "buy")

            if sp_price is not None and lp_price is not None:
                net_credit = sp_price - lp_price
                width = sp_k - lp_k
                commissions_nis = 2 * fee_per_leg_nis
                max_profit_nis = net_credit * contract_multiplier - commissions_nis
                max_loss_nis = (width - net_credit) * contract_multiplier + commissions_nis

                if max_loss_nis > 0 and max_profit_nis > 0:
                    be = sp_k - net_credit
                    # Calculate true POP & EV using RND PDF integration
                    payoff_grid = np.maximum(-width, np.minimum(net_credit, grid - sp_k + net_credit)) * contract_multiplier - commissions_nis
                    ev_nis = float(np.sum(payoff_grid * pdf) * dK)
                    pop = float(np.sum(pdf[grid >= be]) * dK)

                    legs = (
                        RealtimeLeg("Sell", "Put", sp_k, sp_q.put_bid, sp_q.put_ask, sp_q.put_mid, sp_price, "Short Put (מכירת פוט)"),
                        RealtimeLeg("Buy", "Put", lp_k, lp_q.put_bid, lp_q.put_ask, lp_q.put_mid, lp_price, "Long Put (קניית הגנה)"),
                    )

                    proposals.append(
                        RealtimeStrategyProposal(
                            strategy_name="Bull Put Spread (מרווח פוט אופטימי)",
                            horizon_days=horizon,
                            net_credit_debit=net_credit,
                            net_credit_debit_nis=net_credit * contract_multiplier,
                            max_profit_nis=max_profit_nis,
                            max_loss_nis=max_loss_nis,
                            risk_reward_ratio=max_profit_nis / max_loss_nis,
                            breakeven_points=(be,),
                            probability_of_profit=pop,
                            expected_value_nis=ev_nis,
                            legs=legs,
                            rationale="איסוף פרמיה מעל קו תמיכה; מרוויח מעלייה, דשדוש או ירידה קלה מעל נקודת האיזון.",
                            quality_label="ציטוט חי (RND Breeden-Litzenberger)",
                        )
                    )

    # 2. Bear Call Spread
    if len(valid_calls) >= 2:
        sc_k = find_nearest_strike(effective_spot + 0.2 * std_move, valid_calls)
        lc_candidates = [s for s in valid_calls if s > sc_k]
        if lc_candidates:
            lc_k = find_nearest_strike(sc_k + 0.6 * std_move, lc_candidates)
            sc_q, lc_q = quote_map[sc_k], quote_map[lc_k]

            sc_price = _get_clean_exec_price(sc_q, "call", "sell")
            lc_price = _get_clean_exec_price(lc_q, "call", "buy")

            if sc_price is not None and lc_price is not None:
                net_credit = sc_price - lc_price
                width = lc_k - sc_k
                commissions_nis = 2 * fee_per_leg_nis
                max_profit_nis = net_credit * contract_multiplier - commissions_nis
                max_loss_nis = (width - net_credit) * contract_multiplier + commissions_nis

                if max_loss_nis > 0 and max_profit_nis > 0:
                    be = sc_k + net_credit
                    payoff_grid = np.maximum(-width, np.minimum(net_credit, sc_k + net_credit - grid)) * contract_multiplier - commissions_nis
                    ev_nis = float(np.sum(payoff_grid * pdf) * dK)
                    pop = float(np.sum(pdf[grid <= be]) * dK)

                    legs = (
                        RealtimeLeg("Sell", "Call", sc_k, sc_q.call_bid, sc_q.call_ask, sc_q.call_mid, sc_price, "Short Call (מכירת קול)"),
                        RealtimeLeg("Buy", "Call", lc_k, lc_q.call_bid, lc_q.call_ask, lc_q.call_mid, lc_price, "Long Call (קניית הגנה)"),
                    )

                    proposals.append(
                        RealtimeStrategyProposal(
                            strategy_name="Bear Call Spread (מרווח קול פסימי)",
                            horizon_days=horizon,
                            net_credit_debit=net_credit,
                            net_credit_debit_nis=net_credit * contract_multiplier,
                            max_profit_nis=max_profit_nis,
                            max_loss_nis=max_loss_nis,
                            risk_reward_ratio=max_profit_nis / max_loss_nis,
                            breakeven_points=(be,),
                            probability_of_profit=pop,
                            expected_value_nis=ev_nis,
                            legs=legs,
                            rationale="איסוף פרמיה מתחת לקו התנגדות; מרוויח מירידה או דשדוש מתחת לנקודת האיזון.",
                            quality_label="ציטוט חי (RND Breeden-Litzenberger)",
                        )
                    )

    # 3. Bull Call Spread
    if len(valid_calls) >= 2:
        lc_k = find_nearest_strike(effective_spot - 0.1 * std_move, valid_calls)
        sc_candidates = [s for s in valid_calls if s > lc_k]
        if sc_candidates:
            sc_k = find_nearest_strike(effective_spot + 0.5 * std_move, sc_candidates)
            lc_q, sc_q = quote_map[lc_k], quote_map[sc_k]

            lc_price = _get_clean_exec_price(lc_q, "call", "buy")
            sc_price = _get_clean_exec_price(sc_q, "call", "sell")

            if lc_price is not None and sc_price is not None:
                net_debit = lc_price - sc_price
                width = sc_k - lc_k
                commissions_nis = 2 * fee_per_leg_nis
                max_profit_nis = (width - net_debit) * contract_multiplier - commissions_nis
                max_loss_nis = net_debit * contract_multiplier + commissions_nis

                if max_loss_nis > 0 and max_profit_nis > 0:
                    be = lc_k + net_debit
                    payoff_grid = np.maximum(-net_debit, np.minimum(width - net_debit, grid - lc_k - net_debit)) * contract_multiplier - commissions_nis
                    ev_nis = float(np.sum(payoff_grid * pdf) * dK)
                    pop = float(np.sum(pdf[grid >= be]) * dK)

                    legs = (
                        RealtimeLeg("Buy", "Call", lc_k, lc_q.call_bid, lc_q.call_ask, lc_q.call_mid, lc_price, "Long Call (קניית קול)"),
                        RealtimeLeg("Sell", "Call", sc_k, sc_q.call_bid, sc_q.call_ask, sc_q.call_mid, sc_price, "Short Call (מכירת קול)"),
                    )

                    proposals.append(
                        RealtimeStrategyProposal(
                            strategy_name="Bull Call Spread (מרווח קול אופטימי בסיכון מוגבל)",
                            horizon_days=horizon,
                            net_credit_debit=-net_debit,
                            net_credit_debit_nis=-net_debit * contract_multiplier,
                            max_profit_nis=max_profit_nis,
                            max_loss_nis=max_loss_nis,
                            risk_reward_ratio=max_profit_nis / max_loss_nis,
                            breakeven_points=(be,),
                            probability_of_profit=pop,
                            expected_value_nis=ev_nis,
                            legs=legs,
                            rationale="מינוף עליית המדד בסיכון מוגדר מראש ועלות נמוכה מקניית קול ישירה.",
                            quality_label="ציטוט חי (RND Breeden-Litzenberger)",
                        )
                    )

    # 4. Long Straddle
    atm_k = find_nearest_strike(effective_spot, strikes)
    if atm_k in quote_map:
        atm_q = quote_map[atm_k]
        c_price = _get_clean_exec_price(atm_q, "call", "buy")
        p_price = _get_clean_exec_price(atm_q, "put", "buy")

        if c_price is not None and p_price is not None:
            net_debit = c_price + p_price
            commissions_nis = 2 * fee_per_leg_nis
            be_low = atm_k - net_debit
            be_high = atm_k + net_debit
            max_loss_nis = net_debit * contract_multiplier + commissions_nis

            payoff_grid = (np.abs(grid - atm_k) - net_debit) * contract_multiplier - commissions_nis
            ev_nis = float(np.sum(payoff_grid * pdf) * dK)
            pop = float(np.sum(pdf[(grid <= be_low) | (grid >= be_high)]) * dK)
            max_profit_nis = float("inf")

            legs = (
                RealtimeLeg("Buy", "Call", atm_k, atm_q.call_bid, atm_q.call_ask, atm_q.call_mid, c_price, "Long Call ATM"),
                RealtimeLeg("Buy", "Put", atm_k, atm_q.put_bid, atm_q.put_ask, atm_q.put_mid, p_price, "Long Put ATM"),
            )

            proposals.append(
                RealtimeStrategyProposal(
                    strategy_name="Long Straddle (אסטרטגיית פריצה תנודתית)",
                    horizon_days=horizon,
                    net_credit_debit=-net_debit,
                    net_credit_debit_nis=-net_debit * contract_multiplier,
                    max_profit_nis=max_profit_nis,
                    max_loss_nis=max_loss_nis,
                    risk_reward_ratio=2.0,
                    breakeven_points=(be_low, be_high),
                    probability_of_profit=pop,
                    expected_value_nis=ev_nis,
                    legs=legs,
                    rationale="מרוויח מתנועה חדה לכל כיוון (פריצת תנודתיות למעלה או למטה).",
                    quality_label="ציטוט חי (RND Breeden-Litzenberger)",
                )
            )

    # Sort proposals by risk-adjusted Expected Value (EV / Max Loss ratio - Kelly style)
    proposals.sort(key=lambda p: p.expected_value_nis / (p.max_loss_nis + 1.0) if p.max_loss_nis != float("inf") else p.expected_value_nis, reverse=True)
    return proposals


def price_calendar_time_spreads(
    weekly_chain: ParsedOptionChain | None,
    monthly_chain: ParsedOptionChain | None,
    spot_price: float,
    contract_multiplier: float = 50.0,
    fee_per_leg_nis: float = 2.5,
) -> list[CalendarSpreadProposal]:
    """Scan and price inter-expiration Calendar Time Spreads (Weekly vs Monthly)."""
    if not weekly_chain or not monthly_chain or spot_price <= 0:
        return []

    w_map = {q.strike: q for q in weekly_chain.quotes}
    m_map = {q.strike: q for q in monthly_chain.quotes}
    common_strikes = sorted(set(w_map.keys()).intersection(set(m_map.keys())))

    if not common_strikes:
        return []

    short_days = weekly_chain.days_to_expiration
    long_days = monthly_chain.days_to_expiration
    decay_ratio = math.sqrt(long_days / max(0.5, short_days))

    proposals: list[CalendarSpreadProposal] = []
    near_strikes = [s for s in common_strikes if abs(s - spot_price) / spot_price <= 0.03]

    for strike in near_strikes:
        wq, mq = w_map[strike], m_map[strike]

        # 1. Calendar Call Spread
        w_c_bid = _get_clean_exec_price(wq, "call", "sell")
        m_c_ask = _get_clean_exec_price(mq, "call", "buy")

        if w_c_bid is not None and m_c_ask is not None and m_c_ask > w_c_bid > 0:
            net_debit_pts = m_c_ask - w_c_bid
            net_debit_nis = net_debit_pts * contract_multiplier + 2 * fee_per_leg_nis

            # Reprice long leg at short expiration using Black-76
            m_iv = mq.call_iv or 0.18
            rem_time = max(0.001, (long_days - short_days) / 365.0)
            repriced_long = bs_call_price(S=strike, K=strike, T=rem_time, r=0.0, sigma=m_iv)
            est_max_profit_nis = max(0.0, (repriced_long * contract_multiplier) - net_debit_nis)

            w_iv = wq.call_iv or 0.15
            iv_diff = w_iv - m_iv

            legs = (
                RealtimeLeg("Sell", "Call", strike, wq.call_bid, wq.call_ask, wq.call_mid, w_c_bid, f"Short Weekly Call ({short_days:.0f}d)"),
                RealtimeLeg("Buy", "Call", strike, mq.call_bid, mq.call_ask, mq.call_mid, m_c_ask, f"Long Monthly Call ({long_days:.0f}d)"),
            )

            proposals.append(
                CalendarSpreadProposal(
                    strategy_name=f"מרווח זמן קול (Calendar Call Spread {strike:.0f})",
                    strike=strike,
                    short_expiration_days=short_days,
                    long_expiration_days=long_days,
                    option_type="Call",
                    short_leg_exec_price=w_c_bid,
                    long_leg_exec_price=m_c_ask,
                    net_debit_pts=net_debit_pts,
                    net_debit_nis=net_debit_nis,
                    estimated_max_profit_nis=est_max_profit_nis,
                    time_decay_ratio=decay_ratio,
                    iv_diff_pct=iv_diff,
                    rationale=f"שחיקת זמן מואצת (Theta) על הקול השבועי ל-{short_days:.0f} ימים כנגד הגנת קול חודשי ל-{long_days:.0f} ימים.",
                    quality_label="הזדמנות תמחור מרווח זמן (Live DDE)",
                    legs=legs,
                )
            )

        # 2. Calendar Put Spread
        w_p_bid = _get_clean_exec_price(wq, "put", "sell")
        m_p_ask = _get_clean_exec_price(mq, "put", "buy")

        if w_p_bid is not None and m_p_ask is not None and m_p_ask > w_p_bid > 0:
            net_debit_pts = m_p_ask - w_p_bid
            net_debit_nis = net_debit_pts * contract_multiplier + 2 * fee_per_leg_nis

            m_iv = mq.put_iv or 0.18
            rem_time = max(0.001, (long_days - short_days) / 365.0)
            repriced_long = bs_put_price(S=strike, K=strike, T=rem_time, r=0.0, sigma=m_iv)
            est_max_profit_nis = max(0.0, (repriced_long * contract_multiplier) - net_debit_nis)

            w_iv = wq.put_iv or 0.15
            iv_diff = w_iv - m_iv

            legs = (
                RealtimeLeg("Sell", "Put", strike, wq.put_bid, wq.put_ask, wq.put_mid, w_p_bid, f"Short Weekly Put ({short_days:.0f}d)"),
                RealtimeLeg("Buy", "Put", strike, mq.put_bid, mq.put_ask, mq.put_mid, m_p_ask, f"Long Monthly Put ({long_days:.0f}d)"),
            )

            proposals.append(
                CalendarSpreadProposal(
                    strategy_name=f"מרווח זמן פוט (Calendar Put Spread {strike:.0f})",
                    strike=strike,
                    short_expiration_days=short_days,
                    long_expiration_days=long_days,
                    option_type="Put",
                    short_leg_exec_price=w_p_bid,
                    long_leg_exec_price=m_p_ask,
                    net_debit_pts=net_debit_pts,
                    net_debit_nis=net_debit_nis,
                    estimated_max_profit_nis=est_max_profit_nis,
                    time_decay_ratio=decay_ratio,
                    iv_diff_pct=iv_diff,
                    rationale=f"שחיקת זמן מואצת על הפוט השבועי ל-{short_days:.0f} ימים כנגד הגנת פוט חודשי ל-{long_days:.0f} ימים.",
                    quality_label="הזדמנות תמחור מרווח זמן (Live DDE)",
                    legs=legs,
                )
            )

    # Sort calendar proposals by highest ROI: (estimated_max_profit_nis - net_debit_nis) / net_debit_nis
    proposals.sort(key=lambda p: (p.estimated_max_profit_nis - p.net_debit_nis) / max(1.0, p.net_debit_nis), reverse=True)
    return proposals
