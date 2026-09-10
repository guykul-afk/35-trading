"""Service for parsing and analyzing TASE Put/Call Chart and Derivatives Open Positions data."""

from __future__ import annotations

import io
import json
import math
import sqlite3
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pandas as pd


@dataclass(frozen=True, slots=True)
class PutCallStrikeRow:
    strike: float
    call_oi: float
    put_oi: float
    call_vol: float
    put_vol: float


@dataclass(frozen=True, slots=True)
class PutCallAnalysisResult:
    as_of_date: str
    expiry_label: str
    strikes: list[PutCallStrikeRow]
    total_call_oi: float
    total_put_oi: float
    pcr_oi: float
    total_call_vol: float
    total_put_vol: float
    pcr_vol: float
    max_pain_strike: float
    call_wall_strike: float
    put_wall_strike: float
    net_skew_ratio: float


@dataclass(frozen=True, slots=True)
class PutCallDeltaStrike:
    strike: float
    current_call_oi: float
    prev_call_oi: float
    delta_call_oi: float
    current_put_oi: float
    prev_put_oi: float
    delta_put_oi: float
    net_delta_oi: float


@dataclass(frozen=True, slots=True)
class OpenInterestChangeAnalysis:
    current_date: str
    prev_date: str
    delta_total_call_oi: float
    delta_total_put_oi: float
    delta_net_oi: float
    delta_pcr_oi: float
    delta_max_pain: float
    strike_deltas: list[PutCallDeltaStrike]
    top_call_accumulations: list[PutCallDeltaStrike]
    top_put_accumulations: list[PutCallDeltaStrike]
    top_closings: list[PutCallDeltaStrike]
    primary_regime_sentiment: str
    detailed_insights: list[str]


def calculate_max_pain(
    strikes: list[float], call_ois: list[float], put_ois: list[float]
) -> float:
    """Calculate the Max Pain price (strike where total option payout to buyers is minimized).
    
    Total Payout(S) = sum_i(Call_OI_i * max(0, S - K_i)) + sum_i(Put_OI_i * max(0, K_i - S))
    """
    if not strikes:
        return 0.0

    min_loss = float("inf")
    best_strike = strikes[0]

    for test_price in strikes:
        total_loss = 0.0
        for k, c_oi, p_oi in zip(strikes, call_ois, put_ois):
            if test_price > k:
                total_loss += c_oi * (test_price - k)
            if test_price < k:
                total_loss += p_oi * (k - test_price)

        if total_loss < min_loss:
            min_loss = total_loss
            best_strike = test_price

    return best_strike


def _clean_numeric(val: Any) -> float:
    """Safely convert strings or numbers with commas to float."""
    if pd.isna(val) or val is None:
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    s = str(val).strip().replace(",", "").replace(" ", "").replace("%", "")
    try:
        return float(s)
    except (ValueError, TypeError):
        return 0.0


def parse_putcall_data(raw: bytes, filename: str = "") -> PutCallAnalysisResult:
    """Parse Put/Call Chart or Open Positions data from CSV / Excel / text bytes."""
    df: pd.DataFrame | None = None

    if filename.lower().endswith((".xlsx", ".xls")):
        try:
            df = pd.read_excel(io.BytesIO(raw))
        except Exception:
            df = None

    if df is None:
        encodings = ("utf-8-sig", "utf-8", "windows-1255", "iso-8859-8", "latin1", "utf-16")
        separators = (",", "\t", ";")
        for enc in encodings:
            for sep in separators:
                try:
                    content = raw.decode(enc)
                    lines = [ln.strip() for ln in content.splitlines() if ln.strip()]
                    if not lines:
                        continue
                    
                    header_idx = 0
                    for idx, line in enumerate(lines[:15]):
                        line_lower = line.lower()
                        if any(k in line_lower for k in ("strike", "מימוש", "סטרייק", "קול", "פוט", "call", "put")):
                            header_idx = idx
                            break

                    parsed_csv = "\n".join(lines[header_idx:])
                    df_candidate = pd.read_csv(io.StringIO(parsed_csv), sep=sep, on_bad_lines="skip")
                    if len(df_candidate.columns) >= 2 and len(df_candidate) >= 1:
                        df = df_candidate
                        break
                except Exception:
                    continue
            if df is not None:
                break

    if df is None or df.empty:
        raise ValueError("לא ניתן היה לפענח את קובץ נתוני ה-Put/Call. ודא שהקובץ תקין וכולל עמודות שערי מימוש ופוזיציות.")

    col_map: dict[str, str] = {}
    for col in df.columns:
        c_norm = str(col).strip().lower().replace('"', "").replace("'", "").replace("_", " ")
        if any(k in c_norm for k in ("שער מימוש", "מחיר מימוש", "סטרייק", "strike", "exercise price", "k")):
            col_map[col] = "strike"
        elif any(k in c_norm for k in ("פוזיציות פתוחות קול", "פתיחות קול", "call oi", "calls oi", "call open interest", "פתוחות c")):
            col_map[col] = "call_oi"
        elif any(k in c_norm for k in ("פוזיציות פתוחות פוט", "פתיחות פוט", "put oi", "puts oi", "put open interest", "פתוחות p")):
            col_map[col] = "put_oi"
        elif any(k in c_norm for k in ("מחזור קול", "מחזורים קול", "כמות קול", "call vol", "call turnover", "מחזור c")):
            col_map[col] = "call_vol"
        elif any(k in c_norm for k in ("מחזור פוט", "מחזורים פוט", "כמות פוט", "put vol", "put turnover", "מחזור p")):
            col_map[col] = "put_vol"
        elif any(k in c_norm for k in ("פוזיציות פתוחות", "פתיחות", "open interest", "oi")):
            col_map[col] = "open_interest"
        elif any(k in c_norm for k in ("מחזור", "volume", "turnover", "vol")):
            col_map[col] = "volume"
        elif any(k in c_norm for k in ("סוג", "type", "call/put", "right")):
            col_map[col] = "right"
        elif any(k in c_norm for k in ("תאריך", "date", "session")):
            col_map[col] = "date"
        elif any(k in c_norm for k in ("פקיעה", "expiry", "expiration")):
            col_map[col] = "expiry"

    df = df.rename(columns=col_map)

    strike_rows: list[PutCallStrikeRow] = []

    if "strike" in df.columns and ("call_oi" in df.columns or "put_oi" in df.columns):
        for _, row in df.iterrows():
            k = _clean_numeric(row.get("strike"))
            if k <= 0:
                continue
            c_oi = _clean_numeric(row.get("call_oi", 0.0))
            p_oi = _clean_numeric(row.get("put_oi", 0.0))
            c_vol = _clean_numeric(row.get("call_vol", 0.0))
            p_vol = _clean_numeric(row.get("put_vol", 0.0))
            strike_rows.append(PutCallStrikeRow(
                strike=k,
                call_oi=c_oi,
                put_oi=p_oi,
                call_vol=c_vol,
                put_vol=p_vol,
            ))

    elif "strike" in df.columns and "right" in df.columns and "open_interest" in df.columns:
        grouped: dict[float, dict[str, float]] = {}
        for _, row in df.iterrows():
            k = _clean_numeric(row.get("strike"))
            if k <= 0:
                continue
            r = str(row.get("right", "")).upper().strip()
            oi = _clean_numeric(row.get("open_interest", 0.0))
            vol = _clean_numeric(row.get("volume", 0.0))
            if k not in grouped:
                grouped[k] = {"call_oi": 0.0, "put_oi": 0.0, "call_vol": 0.0, "put_vol": 0.0}
            if r.startswith("C") or "קול" in r:
                grouped[k]["call_oi"] += oi
                grouped[k]["call_vol"] += vol
            elif r.startswith("P") or "פוט" in r:
                grouped[k]["put_oi"] += oi
                grouped[k]["put_vol"] += vol

        for k in sorted(grouped.keys()):
            item = grouped[k]
            strike_rows.append(PutCallStrikeRow(
                strike=k,
                call_oi=item["call_oi"],
                put_oi=item["put_oi"],
                call_vol=item["call_vol"],
                put_vol=item["put_vol"],
            ))

    if not strike_rows:
        raise ValueError("לא זוהו שורות נתונים תקינות בקובץ ה-Put/Call. ודא שהקובץ כולל שערי מימוש ופוזיציות פתוחות.")

    strike_rows.sort(key=lambda x: x.strike)

    strikes_list = [r.strike for r in strike_rows]
    call_ois = [r.call_oi for r in strike_rows]
    put_ois = [r.put_oi for r in strike_rows]
    call_vols = [r.call_vol for r in strike_rows]
    put_vols = [r.put_vol for r in strike_rows]

    tot_call_oi = sum(call_ois)
    tot_put_oi = sum(put_ois)
    tot_call_vol = sum(call_vols)
    tot_put_vol = sum(put_vols)

    pcr_oi = (tot_put_oi / tot_call_oi) if tot_call_oi > 0 else 1.0
    pcr_vol = (tot_put_vol / tot_call_vol) if tot_call_vol > 0 else 1.0

    max_pain = calculate_max_pain(strikes_list, call_ois, put_ois)

    max_c_idx = max(range(len(call_ois)), key=lambda i: call_ois[i]) if call_ois else 0
    max_p_idx = max(range(len(put_ois)), key=lambda i: put_ois[i]) if put_ois else 0
    call_wall = strikes_list[max_c_idx] if strikes_list else 0.0
    put_wall = strikes_list[max_p_idx] if strikes_list else 0.0

    net_skew = ((tot_call_oi - tot_put_oi) / (tot_call_oi + tot_put_oi)) if (tot_call_oi + tot_put_oi) > 0 else 0.0

    as_of = datetime.now(UTC).strftime("%Y-%m-%d")
    return PutCallAnalysisResult(
        as_of_date=as_of,
        expiry_label="סדרה נוכחית",
        strikes=strike_rows,
        total_call_oi=tot_call_oi,
        total_put_oi=tot_put_oi,
        pcr_oi=round(pcr_oi, 4),
        total_call_vol=tot_call_vol,
        total_put_vol=tot_put_vol,
        pcr_vol=round(pcr_vol, 4),
        max_pain_strike=max_pain,
        call_wall_strike=call_wall,
        put_wall_strike=put_wall,
        net_skew_ratio=round(net_skew, 4),
    )


def init_putcall_table(conn: sqlite3.Connection) -> None:
    """Ensure the putcall_snapshots table exists in the database."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS putcall_snapshots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            as_of_date TEXT NOT NULL,
            uploaded_at_utc TEXT NOT NULL,
            expiry_label TEXT NOT NULL,
            total_call_oi REAL NOT NULL,
            total_put_oi REAL NOT NULL,
            pcr_oi REAL NOT NULL,
            total_call_vol REAL NOT NULL,
            total_put_vol REAL NOT NULL,
            pcr_vol REAL NOT NULL,
            max_pain_strike REAL NOT NULL,
            call_wall_strike REAL NOT NULL,
            put_wall_strike REAL NOT NULL,
            net_skew_ratio REAL NOT NULL,
            raw_strikes_json TEXT NOT NULL
        );
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_putcall_date ON putcall_snapshots(as_of_date DESC);"
    )


def save_putcall_snapshot(db_path: Path, result: PutCallAnalysisResult) -> int:
    """Save parsed Put/Call analysis to SQLite database."""
    conn = sqlite3.connect(db_path)
    try:
        init_putcall_table(conn)
        strikes_payload = json.dumps([asdict(r) for r in result.strikes])
        now_utc = datetime.now(UTC).isoformat()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO putcall_snapshots (
                as_of_date, uploaded_at_utc, expiry_label,
                total_call_oi, total_put_oi, pcr_oi,
                total_call_vol, total_put_vol, pcr_vol,
                max_pain_strike, call_wall_strike, put_wall_strike,
                net_skew_ratio, raw_strikes_json
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                result.as_of_date,
                now_utc,
                result.expiry_label,
                result.total_call_oi,
                result.total_put_oi,
                result.pcr_oi,
                result.total_call_vol,
                result.total_put_vol,
                result.pcr_vol,
                result.max_pain_strike,
                result.call_wall_strike,
                result.put_wall_strike,
                result.net_skew_ratio,
                strikes_payload,
            ),
        )
        conn.commit()
        return cur.lastrowid or 0
    finally:
        conn.close()


def load_latest_putcall_snapshot(db_path: Path) -> PutCallAnalysisResult | None:
    """Load the most recent Put/Call snapshot from the database."""
    if not Path(db_path).exists():
        return None

    conn = sqlite3.connect(db_path)
    try:
        init_putcall_table(conn)
        conn.row_factory = sqlite3.Row
        row = conn.execute(
            """
            SELECT * FROM putcall_snapshots
            ORDER BY id DESC LIMIT 1
            """
        ).fetchone()
        if not row:
            return None

        strikes_data = json.loads(row["raw_strikes_json"])
        strikes = [
            PutCallStrikeRow(
                strike=float(s["strike"]),
                call_oi=float(s.get("call_oi", 0.0)),
                put_oi=float(s.get("put_oi", 0.0)),
                call_vol=float(s.get("call_vol", 0.0)),
                put_vol=float(s.get("put_vol", 0.0)),
            )
            for s in strikes_data
        ]

        return PutCallAnalysisResult(
            as_of_date=row["as_of_date"],
            expiry_label=row["expiry_label"],
            strikes=strikes,
            total_call_oi=float(row["total_call_oi"]),
            total_put_oi=float(row["total_put_oi"]),
            pcr_oi=float(row["pcr_oi"]),
            total_call_vol=float(row["total_call_vol"]),
            total_put_vol=float(row["total_put_vol"]),
            pcr_vol=float(row["pcr_vol"]),
            max_pain_strike=float(row["max_pain_strike"]),
            call_wall_strike=float(row["call_wall_strike"]),
            put_wall_strike=float(row["put_wall_strike"]),
            net_skew_ratio=float(row["net_skew_ratio"]),
        )
    finally:
        conn.close()


def load_historical_putcall_snapshots(db_path: Path, limit: int = 5) -> list[PutCallAnalysisResult]:
    """Load historical Put/Call snapshots in descending order (newest first)."""
    if not Path(db_path).exists():
        return []

    conn = sqlite3.connect(db_path)
    try:
        init_putcall_table(conn)
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT * FROM putcall_snapshots
            ORDER BY id DESC LIMIT ?
            """,
            (limit,),
        ).fetchall()
        
        results: list[PutCallAnalysisResult] = []
        for row in rows:
            strikes_data = json.loads(row["raw_strikes_json"])
            strikes = [
                PutCallStrikeRow(
                    strike=float(s["strike"]),
                    call_oi=float(s.get("call_oi", 0.0)),
                    put_oi=float(s.get("put_oi", 0.0)),
                    call_vol=float(s.get("call_vol", 0.0)),
                    put_vol=float(s.get("put_vol", 0.0)),
                )
                for s in strikes_data
            ]
            results.append(
                PutCallAnalysisResult(
                    as_of_date=row["as_of_date"],
                    expiry_label=row["expiry_label"],
                    strikes=strikes,
                    total_call_oi=float(row["total_call_oi"]),
                    total_put_oi=float(row["total_put_oi"]),
                    pcr_oi=float(row["pcr_oi"]),
                    total_call_vol=float(row["total_call_vol"]),
                    total_put_vol=float(row["total_put_vol"]),
                    pcr_vol=float(row["pcr_vol"]),
                    max_pain_strike=float(row["max_pain_strike"]),
                    call_wall_strike=float(row["call_wall_strike"]),
                    put_wall_strike=float(row["put_wall_strike"]),
                    net_skew_ratio=float(row["net_skew_ratio"]),
                )
            )
        return results
    finally:
        conn.close()


def analyze_open_interest_changes(
    current: PutCallAnalysisResult,
    prev: PutCallAnalysisResult,
    spot_price: float = 0.0,
) -> OpenInterestChangeAnalysis:
    """Analyze the strike-by-strike and aggregate changes between two open interest snapshots,
    and generate expert quantitative market microstructure insights on institutional positioning.
    """
    curr_map = {r.strike: r for r in current.strikes}
    prev_map = {r.strike: r for r in prev.strikes}
    all_strikes = sorted(set(curr_map.keys()) | set(prev_map.keys()))

    strike_deltas: list[PutCallDeltaStrike] = []
    otm_put_delta = 0.0
    atm_put_delta = 0.0
    otm_call_delta = 0.0
    atm_call_delta = 0.0

    ref_spot = spot_price if spot_price > 0 else current.max_pain_strike

    for k in all_strikes:
        c_curr = curr_map[k].call_oi if k in curr_map else 0.0
        c_prev = prev_map[k].call_oi if k in prev_map else 0.0
        d_c = c_curr - c_prev

        p_curr = curr_map[k].put_oi if k in curr_map else 0.0
        p_prev = prev_map[k].put_oi if k in prev_map else 0.0
        d_p = p_curr - p_prev

        strike_deltas.append(
            PutCallDeltaStrike(
                strike=k,
                current_call_oi=c_curr,
                prev_call_oi=c_prev,
                delta_call_oi=d_c,
                current_put_oi=p_curr,
                prev_put_oi=p_prev,
                delta_put_oi=d_p,
                net_delta_oi=d_c - d_p,
            )
        )

        if ref_spot > 0:
            if k < 0.985 * ref_spot:
                otm_put_delta += d_p
            elif k > 1.015 * ref_spot:
                otm_call_delta += d_c
            else:
                atm_put_delta += d_p
                atm_call_delta += d_c

    delta_c_tot = current.total_call_oi - prev.total_call_oi
    delta_p_tot = current.total_put_oi - prev.total_put_oi
    delta_pcr = current.pcr_oi - prev.pcr_oi
    delta_pain = current.max_pain_strike - prev.max_pain_strike

    top_calls = sorted([s for s in strike_deltas if s.delta_call_oi > 0], key=lambda x: x.delta_call_oi, reverse=True)[:5]
    top_puts = sorted([s for s in strike_deltas if s.delta_put_oi > 0], key=lambda x: x.delta_put_oi, reverse=True)[:5]
    top_closings = sorted([s for s in strike_deltas if (s.delta_call_oi < 0 or s.delta_put_oi < 0)], key=lambda x: min(x.delta_call_oi, x.delta_put_oi))[:5]

    insights: list[str] = []

    # 1. Primary classification of net change
    if delta_p_tot > 0 and delta_p_tot > 1.35 * max(0.0, delta_c_tot):
        if otm_put_delta > 0.40 * delta_p_tot:
            regime = "🛡️ הצטברות ביטוחי אסון (Tail-Risk Hedging) – זהירות מוסדית"
            insights.append(
                f"עיקר תוספת החוזים החדשים התרכזה ברכישת פוטים מחוץ לכסף (תוספת של {otm_put_delta:,.0f} חוזי OTM Puts). "
                "דפוס זה מאפיין קרנות גידור וגופים מוסדיים הרוכשים ביטוח מפני נפילה חדה, ומעיד על נקיטת משנה זהירות."
            )
        else:
            regime = "🐻 גידור אגרסיבי / לחץ פוטים (Downside Hedging)"
            insights.append(
                f"פתיחה מסיבית של {delta_p_tot:,.0f} חוזי פוט חדשים סביב הכסף (ATM), לעומת שינוי של {delta_c_tot:+,.0f} בקולים בלבד. "
                "משקף עלייה ברורה בחשש מירידות מחירים בטווח הקצר."
            )
    elif delta_c_tot > 0 and delta_c_tot > 1.35 * max(0.0, delta_p_tot):
        regime = "🚀 איסוף חוזי Call – מומנטום שורי וציפייה לעליות"
        insights.append(
            f"השוק רשם הצטברות בולטת של {delta_c_tot:,.0f} חוזי קול חדשים (מול {delta_p_tot:+,.0f} פוטים בלבד). "
            "זרימת פקודות זו מעידה על פעילות קניות שורית וציפייה להמשך עליות שערים במדד ת״א-35."
        )
    elif delta_p_tot < 0 and delta_c_tot >= 0:
        regime = "☀️ שחרור הגנות (De-hedging / Unwinding) – הקלה בלחץ המכירות"
        insights.append(
            f"נסגרו {abs(delta_p_tot):,.0f} חוזי פוט פתוחים במקביל ליציבות בקולים. "
            "פדיון הגנות מוסדיות מעיד על ירידה במפלס הפחד של השחקנים הגדולים, ומספק רוח גבית לעליות."
        )
    elif delta_c_tot < 0 and delta_p_tot < 0:
        regime = "📦 סגירת פוזיציות דו-צדדית לקראת פקיעה (Position Squaring)"
        insights.append(
            f"נרשמה סגירת חוזים בשני צדי השוק ({delta_c_tot:,.0f} קולים, {delta_p_tot:,.0f} פוטים). "
            "דפוס זה אופייני לשלבי סיום סדרה לקראת פקיעה, כאשר כותבים נועלים רווחים ומצמצמים חשיפות."
        )
    else:
        regime = "⚖️ הרחבת פוזיציות מאוזנת (Two-Sided Expansion)"
        insights.append(
            f"התווספו חוזים בשני צדי השוק באופן מאוזן ({delta_c_tot:+,.0f} קולים, {delta_p_tot:+,.0f} פוטים). "
            "השוק שומר על שיווי משקל, ועושי השוק מרחיבים כתיבות מתוך ציפייה למסחר בתוך טווח מוגדר."
        )

    # 2. Max Pain dynamics
    if delta_pain > 0:
        insights.append(
            f"שער הכאב המקסימלי (Max Pain) עלה ב-+{delta_pain:,.0f} נקודות ל-{current.max_pain_strike:,.0f}. "
            "עליית ה-Max Pain מעידה שהכותבים מושכים את שער היעד לפקיעה כלפי מעלה (Bullish Drift)."
        )
    elif delta_pain < 0:
        insights.append(
            f"שער הכאב המקסימלי (Max Pain) ירד ב-{delta_pain:,.0f} נקודות ל-{current.max_pain_strike:,.0f}. "
            "ירידת ה-Max Pain משקפת הסטת שער הפדיונות של הכותבים כלפי מטה (Bearish Drift)."
        )

    # 3. Wall shifts
    if current.call_wall_strike != prev.call_wall_strike:
        insights.append(
            f"תקרת ההתנגדות המרכזית (Call Wall) הוסטה מ-{prev.call_wall_strike:,.0f} ל-{current.call_wall_strike:,.0f} "
            f"({'הרחבת טווח עליון' if current.call_wall_strike > prev.call_wall_strike else 'הנמכת תקרת התנגדות'})."
        )
    if current.put_wall_strike != prev.put_wall_strike:
        insights.append(
            f"רצפת התמיכה המרכזית (Put Wall) הוסטה מ-{prev.put_wall_strike:,.0f} ל-{current.put_wall_strike:,.0f} "
            f"({'העלאת רצפת תמיכה' if current.put_wall_strike > prev.put_wall_strike else 'הנמכת תמיכה / סיכון לירידות'})."
        )

    # 4. PCR OI trajectory
    if abs(delta_pcr) >= 0.05:
        pcr_trend = "עלייה" if delta_pcr > 0 else "ירידה"
        insights.append(
            f"יחס הפוט/קול שינה כיוון ({pcr_trend} של {delta_pcr:+.2f} ל-{current.pcr_oi:.2f}). "
            f"{'השוק מוטה פסימיות יתר (פוטנציאל לאיתות קונטרריאני)' if current.pcr_oi > 1.25 else 'השוק מוטה שאננות יתר' if current.pcr_oi < 0.70 else 'שיווי משקל ניטרלי'}."
        )

    return OpenInterestChangeAnalysis(
        current_date=current.as_of_date,
        prev_date=prev.as_of_date,
        delta_total_call_oi=delta_c_tot,
        delta_total_put_oi=delta_p_tot,
        delta_net_oi=delta_c_tot - delta_p_tot,
        delta_pcr_oi=round(delta_pcr, 4),
        delta_max_pain=delta_pain,
        strike_deltas=strike_deltas,
        top_call_accumulations=top_calls,
        top_put_accumulations=top_puts,
        top_closings=top_closings,
        primary_regime_sentiment=regime,
        detailed_insights=insights,
    )
