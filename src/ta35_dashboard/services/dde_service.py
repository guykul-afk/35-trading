import logging
from ta35_dashboard.storage.repository import SQLiteRepository

logger = logging.getLogger(__name__)


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
    chains: tuple[ParsedOptionChain, ...]


def calculate_atm_premium_sum(chain: ParsedOptionChain, spot_price: float) -> float:
    """Calculate the sum of ATM Call and Put premiums to estimate time value."""
    if not chain.quotes:
        return 0.0
    closest_quote = min(chain.quotes, key=lambda q: abs(q.strike - spot_price))
    c_val = closest_quote.call_mid or 0.0
    p_val = closest_quote.put_mid or 0.0
    return c_val + p_val


def analyze_dde_options_data(
    project_root: str | Path = PROJECT_ROOT,
    uploaded_files: Sequence[Any] | None = None,
    spot_override: float | None = None,
    prob_rise: float = 0.50,
    db_path: str | Path | None = None,
) -> DDEAnalysisResult:
    """Scan and analyze DDE options chain files from project root or user uploads."""
    root_path = Path(project_root)
    source_files: list[str] = []
    latest_mtime: float = 0.0

    raw_chains: list[tuple[float, str, ParsedOptionChain]] = []

    # 1. Handle uploaded files if provided
    if uploaded_files:
        for uf in uploaded_files:
            try:
                content = None
                for enc in ["utf-16", "utf-8", "cp1255"]:
                    try:
                        content = uf.getvalue().decode(enc)
                        if "מחיר מימוש" in content or "מימוש" in content:
                            break
                    except Exception as err:
                        logger.debug("Encoding %s failed for %s: %s", enc, uf.name, err)
                
                if content:
                    with tempfile.NamedTemporaryFile("w", encoding="utf-16", delete=False, suffix=".txt") as tmp:
                        tmp.write(content)
                        tmp_path = Path(tmp.name)

                    chain = parse_tase_dde_file(tmp_path, expiration_label="auto")
                    raw_chains.append((datetime.now().timestamp(), uf.name, chain))
                    latest_mtime = max(latest_mtime, datetime.now().timestamp())
            except Exception as e:
                logger.error("Failed parsing uploaded file %s: %s", getattr(uf, 'name', 'unknown'), e)

    # 2. Scan project root and downloads/data directories
    candidate_paths = []
    for ext in ["*.txt", "*.csv", "*.tsv"]:
        candidate_paths.extend(root_path.glob(ext))
        candidate_paths.extend((root_path / "downloads").glob(ext))
        candidate_paths.extend((root_path / "data").glob(ext))

    candidate_paths = list(set(candidate_paths))

    for p in candidate_paths:
        name_lower = p.name.lower()
        if "נגזרים" in name_lower or "option" in name_lower or "dde" in name_lower or "שבועית" in name_lower or "יומית" in name_lower or "אוגוסט" in name_lower:
            try:
                chain = parse_tase_dde_file(p, expiration_label="auto")
                if chain.quotes:
                    mtime = p.stat().st_mtime
                    raw_chains.append((mtime, p.name, chain))
                    latest_mtime = max(latest_mtime, mtime)
            except Exception as e:
                logger.warning("Error parsing candidate DDE file %s: %s", p.name, e)

    # 3. Deduplicate based on base filename (stripping '_live' suffix)
    dedup_map: dict[str, tuple[float, str, ParsedOptionChain]] = {}
    
    for mtime, name, chain in raw_chains:
        base_key = name.lower().replace("_live", "")
        for ext in [".csv", ".txt", ".tsv"]:
            base_key = base_key.replace(ext, "")
        base_key = base_key.strip()
        
        if base_key not in dedup_map or mtime > dedup_map[base_key][0]:
            dedup_map[base_key] = (mtime, name, chain)
            
    unique_chains = list(dedup_map.values())

    # Keep list of source files
    for mtime, name, chain in unique_chains:
        source_files.append(name)

    # Extract parsed chains
    parsed_chains = [item[2] for item in unique_chains]

    # Sort chains by their ATM Option Value (which corresponds to time value / days to expiration)
    temp_spot = 4150.0
    parsed_chains.sort(key=lambda c: calculate_atm_premium_sum(c, temp_spot))

    # 4. Map days to expiration and labels dynamically based on sorted ATM premium order
    final_chains: list[ParsedOptionChain] = []
    num_chains = len(parsed_chains)
    
    if num_chains == 1:
        c = parsed_chains[0]
        final_chains.append(ParsedOptionChain(
            expiration_label=c.expiration_label or "חודשית (Monthly)",
            days_to_expiration=c.days_to_expiration or 16.0,
            synthetic_spot=c.synthetic_spot,
            quotes=c.quotes
        ))
    elif num_chains >= 2:
        min_days = 2.0
        max_days = 16.0
        
        for idx, c in enumerate(parsed_chains):
            if idx == 0:
                days = min_days
                label = "שבועית 1 (Weekly)" if num_chains > 2 else "שבועית (Weekly)"
            elif idx == num_chains - 1:
                days = max_days
                label = "חודשית (Monthly)"
            else:
                days = min_days + (max_days - min_days) * (idx / (num_chains - 1))
                days = float(round(days))
                label = f"שבועית {idx + 1} (Weekly)"
                
            final_chains.append(ParsedOptionChain(
                expiration_label=label,
                days_to_expiration=days,
                synthetic_spot=c.synthetic_spot,
                quotes=c.quotes
            ))

    weekly_chain = None
    monthly_chain = None
    if final_chains:
        weekly_chain = final_chains[0]
        monthly_chain = final_chains[-1]

    # 5. Determine spot price (Live synthetic spot takes precedence over static spot override)
    synth_spot = None
    for c in final_chains:
        if c.synthetic_spot:
            synth_spot = c.synthetic_spot
            break

    spot_price = synth_spot or spot_override or 4145.35

    # 5b. Persist parsed option chains to SQLite
    try:
        repo_path = db_path or (root_path / "data" / "ta35_dashboard.db")
        repo = SQLiteRepository(repo_path)
        for (mtime, s_name, _), f_chain in zip(unique_chains, final_chains):
            repo.insert_chain_snapshots(f_chain, source_file=s_name)
    except Exception as e:
        logger.error("Failed saving chain snapshots to SQLite DB: %s", e)


    # Re-sort final chains in case their days_to_expiration changed
    final_chains.sort(key=lambda c: c.days_to_expiration)

    # 6. Term structure expectations (1d, 3d, 7d, 14d, 30d) using all final chains
    expectations = calculate_term_structure_expectations(
        weekly_chain=weekly_chain,
        monthly_chain=monthly_chain,
        spot_price=spot_price,
        target_horizons=(1, 3, 7, 14, 30),
        chains=final_chains,
    )

    # 7. Real-time strategy proposals (use the monthly chain if available, else weekly)
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

    # 8. Calendar time spreads (between shortest and longest chains)
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
        chains=tuple(final_chains),
    )
