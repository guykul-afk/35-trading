"""DDE Options Chain Service.

Scans project directories for live updating DDE option chain files, computes term structure
implied volatility across 1/3/7/14 days, and generates real-time option strategy and calendar spread proposals.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tempfile
from typing import Sequence, Any

from ta35_dashboard.analytics.implied_vol import (
    HorizonExpectation,
    calculate_term_structure_expectations,
)
from ta35_dashboard.analytics.realtime_strategies import (
    CalendarSpreadProposal,
    RealtimeStrategyProposal,
    price_calendar_time_spreads,
    price_realtime_strategies,
)
from ta35_dashboard.config import PROJECT_ROOT
from ta35_dashboard.connectors.dde_parser import ParsedOptionChain, parse_tase_dde_file


@dataclass(frozen=True, slots=True)
class DDEAnalysisResult:
    weekly_chain: ParsedOptionChain | None
    monthly_chain: ParsedOptionChain | None
    spot_price: float
    synthetic_spot: float | None
    expectations: dict[int, HorizonExpectation]
    realtime_proposals: tuple[RealtimeStrategyProposal, ...]
    calendar_proposals: tuple[CalendarSpreadProposal, ...]
    source_files: tuple[str, ...]
    status_message: str
    last_modified_str: str


def analyze_dde_options_data(
    project_root: str | Path = PROJECT_ROOT,
    uploaded_files: Sequence[Any] | None = None,
    spot_override: float | None = None,
    prob_rise: float = 0.50,
) -> DDEAnalysisResult:
    """Scan and analyze DDE options chain files from project root or user uploads."""
    root_path = Path(project_root)
    source_files: list[str] = []
    weekly_chain: ParsedOptionChain | None = None
    monthly_chain: ParsedOptionChain | None = None
    latest_mtime: float = 0.0

    # 1. Handle uploaded files if provided
    if uploaded_files:
        for uf in uploaded_files:
            try:
                content = uf.getvalue().decode("utf-16")
                with tempfile.NamedTemporaryFile("w", encoding="utf-16", delete=False, suffix=".txt") as tmp:
                    tmp.write(content)
                    tmp_path = Path(tmp.name)

                chain = parse_tase_dde_file(tmp_path, expiration_label="auto")
                source_files.append(uf.name)
                latest_mtime = max(latest_mtime, datetime.now().timestamp())
                if "שבועית" in chain.expiration_label or chain.days_to_expiration <= 5:
                    weekly_chain = chain
                else:
                    monthly_chain = chain
            except Exception:
                pass

    # 2. If no uploaded files or missing chains, scan project root and downloads directory
    if weekly_chain is None or monthly_chain is None:
        candidate_paths = []
        for ext in ["*.txt", "*.csv", "*.tsv"]:
            candidate_paths.extend(root_path.glob(ext))
            candidate_paths.extend((root_path / "downloads").glob(ext))
            candidate_paths.extend((root_path / "data").glob(ext))

        for p in candidate_paths:
            name_lower = p.name.lower()
            if "נגזרים" in name_lower or "option" in name_lower or "dde" in name_lower:
                try:
                    chain = parse_tase_dde_file(p, expiration_label="auto")
                    if chain.quotes:
                        source_files.append(p.name)
                        latest_mtime = max(latest_mtime, p.stat().st_mtime)
                        if ("שבועית" in chain.expiration_label or chain.days_to_expiration <= 5) and weekly_chain is None:
                            weekly_chain = chain
                        elif monthly_chain is None:
                            monthly_chain = chain
                except Exception:
                    pass

    # 3. Determine spot price
    synth_spot = None
    if monthly_chain and monthly_chain.synthetic_spot:
        synth_spot = monthly_chain.synthetic_spot
    elif weekly_chain and weekly_chain.synthetic_spot:
        synth_spot = weekly_chain.synthetic_spot

    spot_price = spot_override or synth_spot or 4145.35

    # 4. Term structure expectations (1d, 3d, 7d, 14d)
    expectations = calculate_term_structure_expectations(
        weekly_chain, monthly_chain, spot_price, target_horizons=(1, 3, 7, 14)
    )

    # 5. Real-time strategy proposals
    proposals: list[RealtimeStrategyProposal] = []
    active_chain = monthly_chain or weekly_chain
    if active_chain:
        exp_14d = expectations.get(14)
        iv = exp_14d.implied_volatility if exp_14d else 0.15
        proposals = price_realtime_strategies(
            chain=active_chain,
            spot_price=spot_price,
            prob_rise=prob_rise,
            implied_vol=iv,
        )

    # 6. Calendar time spreads (Weekly vs Monthly)
    calendar_proposals = price_calendar_time_spreads(
        weekly_chain=weekly_chain,
        monthly_chain=monthly_chain,
        spot_price=spot_price,
        contract_multiplier=50.0,
    )

    if not source_files:
        status_msg = "לא נמצאו קבצי DDE בתיקייה. ניתן להעלות קבצים או לשמור קבצי DDE בתיקיית הפרויקט."
        last_mod_str = "לא זמין"
    else:
        status_msg = f"פוענחו בהצלחה {len(source_files)} קבצי DDE מתעדכנים ({', '.join(set(source_files))})."
        last_mod_dt = datetime.fromtimestamp(latest_mtime)
        last_mod_str = last_mod_dt.strftime("%H:%M:%S (%d/%m/%Y)")

    return DDEAnalysisResult(
        weekly_chain=weekly_chain,
        monthly_chain=monthly_chain,
        spot_price=spot_price,
        synthetic_spot=synth_spot,
        expectations=expectations,
        realtime_proposals=tuple(proposals),
        calendar_proposals=tuple(calendar_proposals),
        source_files=tuple(source_files),
        status_message=status_msg,
        last_modified_str=last_mod_str,
    )
