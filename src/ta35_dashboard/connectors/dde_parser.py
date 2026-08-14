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
    call_contract_id: str | None
    put_contract_id: str | None
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
        if self.call_bid is not None and self.call_ask is not None:
            return (self.call_bid + self.call_ask) / 2.0
        return self.call_last if self.call_last is not None else (self.call_bid if self.call_bid is not None else self.call_ask)

    @property
    def put_mid(self) -> float | None:
        if self.put_bid is not None and self.put_ask is not None:
            return (self.put_bid + self.put_ask) / 2.0
        return self.put_last if self.put_last is not None else (self.put_bid if self.put_bid is not None else self.put_ask)


@dataclass(frozen=True, slots=True)
class ParsedOptionChain:
    expiration_label: str
    days_to_expiration: float
    synthetic_spot: float | None
    quotes: tuple[OptionQuote, ...]
    content_hash: str | None = None

    @property
    def quotes_with_prices(self) -> int:
        return sum(1 for q in self.quotes if q.call_mid is not None or q.put_mid is not None)

    def to_dataframe(self) -> pd.DataFrame:
        records = []
        for q in self.quotes:
            records.append({
                "strike": q.strike,
                "call_contract_id": q.call_contract_id,
                "put_contract_id": q.put_contract_id,
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
        if "יומית" in fname or "daily" in fname:
            expiration_label = "יומית (Daily)"
            if days_to_expiration is None:
                days_to_expiration = 1.0
        elif "שבועית" in fname or "weekly" in fname:
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

    if not lines or len(lines) < 2:
        return ParsedOptionChain(
            expiration_label=expiration_label,
            days_to_expiration=days_to_expiration,
            synthetic_spot=None,
            quotes=(),
            content_hash=None,
        )

    header = lines[0]
    
    # Find strike index
    try:
        strike_idx = next(i for i, h in enumerate(header) if "מחיר מימוש" in h or "מימוש" in h)
    except StopIteration:
        strike_idx = 17 # fallback
        
    def find_col(name: str, side: str) -> int:
        for i, h in enumerate(header):
            if name in h:
                if side == "put" and i < strike_idx:
                    return i
                elif side == "call" and i > strike_idx:
                    return i
        return -1
        
    col_map = {
        "put_bid_sz": find_col("כ.ביקוש", "put"),
        "put_bid": find_col("ביקוש", "put"),
        "put_last": find_col("שער אחרון", "put"),
        "put_ask": find_col("היצע", "put"),
        "put_ask_sz": find_col("כ.היצע", "put"),
        "put_iv": find_col("גלום", "put"),
        "put_contract_id": find_col("מספר נייר", "put") if find_col("מספר נייר", "put") != -1 else find_col("מספר", "put"),
        "call_iv": find_col("גלום", "call"),
        "call_ask_sz": find_col("כ.היצע", "call"),
        "call_ask": find_col("היצע", "call"),
        "call_last": find_col("שער אחרון", "call"),
        "call_bid": find_col("ביקוש", "call"),
        "call_bid_sz": find_col("כ.ביקוש", "call"),
        "call_contract_id": find_col("מספר נייר", "call") if find_col("מספר נייר", "call") != -1 else find_col("מספר", "call"),
        "expiry": find_col("פקיעה", "put") if find_col("פקיעה", "put") != -1 else (find_col("פקיעה", "call") if find_col("פקיעה", "call") != -1 else find_col("תאריך", "put")),
    }
    
    # Fallback to known indices if headers are missing
    if col_map["put_bid"] == -1: col_map["put_bid"] = 11
    if col_map["put_ask"] == -1: col_map["put_ask"] = 13
    if col_map["put_last"] == -1: col_map["put_last"] = 12
    if col_map["put_bid_sz"] == -1: col_map["put_bid_sz"] = 10
    if col_map["put_ask_sz"] == -1: col_map["put_ask_sz"] = 14
    if col_map["put_iv"] == -1: col_map["put_iv"] = 16

    if col_map["call_bid"] == -1: col_map["call_bid"] = 23
    if col_map["call_ask"] == -1: col_map["call_ask"] = 21
    if col_map["call_last"] == -1: col_map["call_last"] = 22
    if col_map["call_bid_sz"] == -1: col_map["call_bid_sz"] = 24
    if col_map["call_ask_sz"] == -1: col_map["call_ask_sz"] = 20
    if col_map["call_iv"] == -1: col_map["call_iv"] = 18

    records: list[OptionQuote] = []
    synthetic_spots: list[float] = []

    for line in lines[1:]:
        if len(line) <= strike_idx:
            continue

        strike_raw = line[strike_idx].strip()
        try:
            # Handle float values like '4120.0' from Excel COM
            strike = float(strike_raw)
            if strike < 100:
                continue
        except ValueError:
            continue

        def _val(idx: int, is_price: bool = True) -> float | None:
            if idx >= 0 and idx < len(line):
                v = line[idx].strip().replace(",", "")
                if v:
                    try:
                        res = float(v)
                        if is_price:
                            res /= scale_factor
                        return res
                    except ValueError:
                        pass
            return None

        def _str_val(idx: int) -> str | None:
            if idx >= 0 and idx < len(line):
                v = line[idx].strip()
                if v:
                    return v
            return None

        put_bid = _val(col_map["put_bid"], is_price=True)
        put_ask = _val(col_map["put_ask"], is_price=True)
        put_last = _val(col_map["put_last"], is_price=True)
        put_bid_sz = _val(col_map["put_bid_sz"], is_price=False)
        put_ask_sz = _val(col_map["put_ask_sz"], is_price=False)
        put_iv = _val(col_map["put_iv"], is_price=False)
        if put_iv is not None:
            put_iv /= 100.0
        put_contract_id = _str_val(col_map.get("put_contract_id", -1))

        call_bid = _val(col_map["call_bid"], is_price=True)
        call_ask = _val(col_map["call_ask"], is_price=True)
        call_last = _val(col_map["call_last"], is_price=True)
        call_ask_sz = _val(col_map["call_ask_sz"], is_price=False)
        call_bid_sz = _val(col_map["call_bid_sz"], is_price=False)
        call_iv = _val(col_map["call_iv"], is_price=False)
        if call_iv is not None:
            call_iv /= 100.0
        call_contract_id = _str_val(col_map.get("call_contract_id", -1))

        expiry_val = _str_val(col_map.get("expiry", -1))
        if expiry_val and expiration_label == "auto":
            # Override guessed expiration label if we found a real expiry date in the row
            expiration_label = expiry_val

        call_mid = (call_bid + call_ask) / 2.0 if (call_bid is not None and call_ask is not None) else call_last
        put_mid = (put_bid + put_ask) / 2.0 if (put_bid is not None and put_ask is not None) else put_last

        if call_mid is not None and put_mid is not None:
            synth = strike + call_mid - put_mid
            if synth > 1000:
                synthetic_spots.append(synth)

        records.append(
            OptionQuote(
                strike=strike,
                call_contract_id=call_contract_id,
                put_contract_id=put_contract_id,
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

    import hashlib
    content_hash = hashlib.sha256(content.encode('utf-8', errors='ignore')).hexdigest() if content else None

    return ParsedOptionChain(
        expiration_label=expiration_label,
        days_to_expiration=days_to_expiration,
        synthetic_spot=median_synth,
        quotes=tuple(records),
        content_hash=content_hash,
    )
