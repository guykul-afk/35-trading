"""Generate live/simulated DDE market pricing for TA-35 options CSV files in DDE folder.

Computes Black-Scholes pricing, bid-ask spreads, and IVs for each strike in the existing CSVs.
Supports single-run and continuous live-updating loop mode (--loop).
"""
from __future__ import annotations

import argparse
import math
from pathlib import Path
import random
import sys
import time

# Ensure src is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT / "src") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "src"))

from ta35_dashboard.services.dde_service import analyze_dde_options_data, save_dde_analysis_cache


def norm_cdf(x: float) -> float:
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def bs_price(spot: float, strike: float, t_years: float, vol: float, r: float = 0.045, option_type: str = "CALL") -> float:
    if t_years <= 0.0001:
        if option_type == "CALL":
            return max(0.0, spot - strike)
        return max(0.0, strike - spot)

    d1 = (math.log(spot / strike) + (r + 0.5 * vol**2) * t_years) / (vol * math.sqrt(t_years))
    d2 = d1 - vol * math.sqrt(t_years)

    if option_type == "CALL":
        return spot * norm_cdf(d1) - strike * math.exp(-r * t_years) * norm_cdf(d2)
    else:
        return strike * math.exp(-r * t_years) * norm_cdf(-d2) - spot * norm_cdf(-d1)


def populate_dde_files(spot: float = 4145.35, base_vol: float = 0.142) -> None:
    dde_dir = PROJECT_ROOT / "DDE"
    if not dde_dir.exists():
        print(f"DDE directory {dde_dir} does not exist.")
        return

    csv_files = list(dde_dir.glob("*.csv"))
    if not csv_files:
        print("No CSV files found in DDE directory.")
        return

    for file_path in csv_files:
        name_lower = file_path.name.lower()
        if "שבועית 18" in name_lower:
            days = 2.0
            vol = base_vol + 0.015
        elif "שבועית" in name_lower:
            days = 5.0
            vol = base_vol + 0.008
        else:
            days = 14.0
            vol = base_vol

        t_years = days / 365.0

        with open(file_path, "r", encoding="utf-8-sig", errors="ignore") as f:
            lines = [l.strip() for l in f.readlines() if l.strip()]

        if not lines:
            continue

        header_line = lines[0]
        new_lines = [header_line]

        for line in lines[1:]:
            parts = [p.strip() for p in line.split(",")]
            if len(parts) < 18:
                continue

            strike_str = parts[17]
            try:
                strike = float(strike_str)
            except ValueError:
                continue

            # Black-Scholes in index points
            call_pts = bs_price(spot, strike, t_years, vol, option_type="CALL")
            put_pts = bs_price(spot, strike, t_years, vol, option_type="PUT")

            # Scale to NIS (multiplier = 50 NIS per index point)
            scale = 50.0
            call_nis = call_pts * scale
            put_nis = put_pts * scale

            # Bid/Ask spread in NIS (e.g. 20-50 NIS)
            spread_call = max(20.0, round(call_nis * 0.02, 0))
            spread_put = max(20.0, round(put_nis * 0.02, 0))

            call_bid_nis = max(10.0, round(call_nis - spread_call / 2.0, 0))
            call_ask_nis = round(call_nis + spread_call / 2.0, 0)
            call_last_nis = round(call_nis, 0)

            put_bid_nis = max(10.0, round(put_nis - spread_put / 2.0, 0))
            put_ask_nis = round(put_nis + spread_put / 2.0, 0)
            put_last_nis = round(put_nis, 0)

            iv_pct = round(vol * 100.0, 1)

            # Build line according to TASE CSV schema
            row = ["" for _ in range(35)]
            row[10] = "15"  # call bid sz
            row[11] = f"{int(call_bid_nis)}"
            row[12] = f"{int(call_last_nis)}"
            row[13] = f"{int(call_ask_nis)}"
            row[14] = "20"  # call ask sz
            row[15] = f"{spot:.1f}"
            row[16] = f"{iv_pct}"
            row[17] = f"{int(strike)}"
            row[18] = f"{iv_pct}"
            row[19] = f"{spot:.1f}"
            row[20] = "25"  # put ask sz
            row[21] = f"{int(put_ask_nis)}"
            row[22] = f"{int(put_last_nis)}"
            row[23] = f"{int(put_bid_nis)}"
            row[24] = "18"  # put bid sz

            new_lines.append(",".join(row))

        with open(file_path, "w", encoding="utf-8-sig") as f:
            f.write("\n".join(new_lines) + "\n")

    # Re-run analysis and save cache
    res = analyze_dde_options_data(project_root=PROJECT_ROOT, spot_override=spot)
    save_dde_analysis_cache(res, project_root=PROJECT_ROOT)
    print(f"[{time.strftime('%H:%M:%S')}] DDE updated. Status: {res.status_message} (Chains: {len(res.chains)}, Active quotes: {sum(c.quotes_with_prices for c in res.chains)})")


def main() -> None:
    parser = argparse.ArgumentParser(description="Populate DDE files with live option data.")
    parser.add_argument("--loop", action="store_true", help="Run continuously in a loop simulating live ticking market")
    parser.add_argument("--interval", type=float, default=5.0, help="Interval in seconds between updates in loop mode")
    parser.add_argument("--spot", type=float, default=4145.35, help="Base spot index level")
    parser.add_argument("--vol", type=float, default=0.142, help="Base implied volatility decimal")
    args = parser.parse_args()

    current_spot = args.spot
    if args.loop:
        print(f"Starting continuous DDE live generator every {args.interval}s...")
        while True:
            # Small random walk on spot
            drift = random.gauss(0, 0.4)
            current_spot = round(max(3800.0, min(4500.0, current_spot + drift)), 2)
            populate_dde_files(spot=current_spot, base_vol=args.vol)
            time.sleep(args.interval)
    else:
        populate_dde_files(spot=args.spot, base_vol=args.vol)


if __name__ == "__main__":
    main()
