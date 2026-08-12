"""TASE Options Chain DDE File Parser.

Parses UTF-16LE TSV options chain files exported from TASE trading platforms (e.g. FMR, Orpak, Excel DDE).
Uses official TASE contract multiplier of 50 NIS per index point (updated March 2024).
Extracts Call and Put bid/ask/last quotes, strike prices, synthetic futures, and computes clean mid-prices.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd


@dataclass(frozen=True, slots=True)
class OptionQuote:
    strike: float
    call_bid: float | None
    call_ask: float | None
    call_last: float | None
    call_bid_size: float | None
    call_ask_size: float | None
    call_iv: float | None
    put_bid: float | None
    put_ask: float | None
    put_last: float | None
    put_bid_size: float | None
    put_ask_size: float | None
    put_iv: float | None

    @property
    def call_mid(self) -> float | None:
        if self.call_bid is not None and self.call_ask is not None and self.call_bid > 0 and self.call_ask > 0:
            return (self.call_bid + self.call_ask) / 2.0
        return self.call_last or self.call_bid or self.call_ask

    @property
    def put_mid(self) -> float | None:
        if self.put_bid is not None and self.put_ask is not None and self.put_bid > 0 and self.put_ask > 0:
            return (self.put_bid + self.put_ask) / 2.0
        return self.put_last or self.put_bid or self.put_ask


@dataclass(frozen=True, slots=True)
class ParsedOptionChain:
    expiration_label: str
    days_to_expiration: float
    synthetic_spot: float | None
    quotes: tuple[OptionQuote, ...]

    def to_dataframe(self) -> pd.DataFrame:
        records = []
        for q in self.quotes:
            records.append({
                "strike": q.strike,
                "call_bid": q.call_bid,
                "call_ask": q.call_ask,
                "call_last": q.call_last,
                "call_mid": q.call_mid,
                "put_bid": q.put_bid,
                "put_ask": q.put_ask,
                "put_last": q.put_last,
                "put_mid": q.put_mid,
            })
        return pd.DataFrame(records)


def parse_tase_dde_file(
    file_path: str | Path,
    expiration_label: str = "auto",
    days_to_expiration: float | None = None,
    scale_factor: float = 50.0,  # Official TASE 50 NIS per index point
) -> ParsedOptionChain:
    """Parse a TASE option chain text/DDE export file into structured quotes.

    Args:
        file_path: Path to the UTF-16LE TSV file.
        expiration_label: Optional label for the expiration (e.g. 'weekly', 'monthly').
        days_to_expiration: Days to expiration if known (e.g. 2.0 or 16.0).
        scale_factor: Scale factor to convert NIS quotes to index points (default 50.0 NIS/pt).

    Returns:
        ParsedOptionChain dataclass.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Options file not found: {file_path}")

    fname = path.name.lower()
    if expiration_label == "auto":
        if "שבועית" in fname or "weekly" in fname:
            expiration_label = "שבועית (Weekly)"
            if days_to_expiration is None:
                days_to_expiration = 2.0
        elif "אוגוסט" in fname or "monthly" in fname or "חודשית" in fname:
            expiration_label = "חודשית (Monthly)"
            if days_to_expiration is None:
                days_to_expiration = 16.0
        else:
            expiration_label = "אופציות ת״א־35"
            if days_to_expiration is None:
                days_to_expiration = 10.0

    if days_to_expiration is None:
        days_to_expiration = 14.0

    # Detect encoding and read content
    content = ""
    for enc in ["utf-16", "utf-8-sig", "utf-8", "cp1255"]:
        try:
            with open(path, "r", encoding=enc) as f:
                content = f.read()
            if len(content) > 10 and ("מחיר מימוש" in content or "מימוש" in content):
                break
        except Exception:
            continue

    if not content:
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception:
            pass

    # Detect separator
    first_line = content.split("\n")[0] if content else ""
    separator = "\t"
    if "," in first_line:
        separator = ","
    elif ";" in first_line:
        separator = ";"

    lines = [line.split(separator) for line in content.splitlines() if line.strip()]

    if not lines:
        return ParsedOptionChain(
            expiration_label=expiration_label,
            days_to_expiration=days_to_expiration,
            synthetic_spot=None,
            quotes=(),
        )

    records: list[OptionQuote] = []
    synthetic_spots: list[float] = []

    for line in lines[1:]:
        if len(line) <= 17:
            continue

        strike_raw = line[17].strip()
        if not strike_raw.isdigit() or int(strike_raw) < 100:
            continue

        strike = float(strike_raw)

        def _val(idx: int) -> float | None:
            if idx < len(line):
                v = line[idx].strip().replace(",", "")
                if v and v != "0":
                    try:
                        res = float(v) / scale_factor
                        return res if res > 0 else None
                    except ValueError:
                        return None
            return None

        call_bid = _val(11)
        call_ask = _val(13)
        call_last = _val(12)
        call_bid_sz = _val(10)
        call_ask_sz = _val(14)
        call_iv = _val(16)

        put_bid = _val(23)
        put_ask = _val(21)
        put_last = _val(22)
        put_ask_sz = _val(20)
        put_bid_sz = _val(24)
        put_iv = _val(18)

        call_mid = (call_bid + call_ask) / 2.0 if (call_bid and call_ask) else call_last
        put_mid = (put_bid + put_ask) / 2.0 if (put_bid and put_ask) else put_last

        if call_mid is not None and put_mid is not None:
            synth = strike + call_mid - put_mid
            if 3000 <= synth <= 6000:
                synthetic_spots.append(synth)

        records.append(
            OptionQuote(
                strike=strike,
                call_bid=call_bid,
                call_ask=call_ask,
                call_last=call_last,
                call_bid_size=call_bid_sz,
                call_ask_size=call_ask_sz,
                call_iv=call_iv,
                put_bid=put_bid,
                put_ask=put_ask,
                put_last=put_last,
                put_bid_size=put_bid_sz,
                put_ask_size=put_ask_sz,
                put_iv=put_iv,
            )
        )

    median_synth = float(np.median(synthetic_spots)) if synthetic_spots else None

    return ParsedOptionChain(
        expiration_label=expiration_label,
        days_to_expiration=days_to_expiration,
        synthetic_spot=median_synth,
        quotes=tuple(records),
    )
