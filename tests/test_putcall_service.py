from pathlib import Path
import pytest
from ta35_dashboard.analytics.putcall_service import (
    calculate_max_pain,
    calculate_max_pain_curve,
    build_putcall_research_product,
    parse_putcall_data,
    save_putcall_snapshot,
    load_latest_putcall_snapshot,
)
from ta35_dashboard.services.tase_upload import auto_detect_series, import_tase_uploads

def test_calculate_max_pain():
    strikes = [2000.0, 2020.0, 2040.0, 2060.0]
    call_ois = [100.0, 300.0, 500.0, 700.0]
    put_ois = [500.0, 400.0, 200.0, 50.0]
    pain = calculate_max_pain(strikes, call_ois, put_ois)
    assert pain == 2020.0

def test_parse_putcall_hebrew_csv():
    raw = """
    שער מימוש,פוזיציות פתוחות קול,פוזיציות פתוחות פוט,מחזור קול,מחזור פוט
    2000,100,500,10,50
    2020,300,400,25,30
    2040,500,200,40,15
    2060,700,50,60,5
    """.strip().encode("utf-8")
    
    res = parse_putcall_data(raw, "putcallchart.csv")
    assert res.total_call_oi == 1600.0
    assert res.total_put_oi == 1150.0
    assert abs(res.pcr_oi - 0.7188) < 0.001
    assert res.max_pain_strike == 2020.0
    assert res.call_wall_strike == 2060.0
    assert res.put_wall_strike == 2000.0

def test_parse_putcall_english_csv():
    raw = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    4200,1500,800,200,100
    4250,2000,1200,300,150
    4300,2500,400,500,50
    """.strip().encode("utf-8")
    
    res = parse_putcall_data(raw, "options_summary.csv")
    assert res.total_call_oi == 6000.0
    assert res.total_put_oi == 2400.0
    assert abs(res.pcr_oi - 0.40) < 0.001
    assert res.call_wall_strike == 4300.0
    assert res.put_wall_strike == 4250.0

def test_auto_detect_putcall():
    raw = "שער מימוש,פוזיציות פתוחות קול,פוזיציות פתוחות פוט".encode("utf-8")
    assert auto_detect_series(raw, "putcallchart.csv") == "PUTCALL_CHART"

def test_save_and_load_putcall(tmp_path):
    db_file = tmp_path / "test.sqlite3"
    raw = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    4200,1000,1000,100,100
    """.strip().encode("utf-8")
    res = parse_putcall_data(raw)
    row_id = save_putcall_snapshot(db_file, res)
    assert row_id > 0
    loaded = load_latest_putcall_snapshot(db_file)
    assert loaded is not None
    assert loaded.total_call_oi == 1000.0


def test_analyze_open_interest_changes():
    from ta35_dashboard.analytics.putcall_service import analyze_open_interest_changes
    raw1 = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    2000,100,500,10,50
    2020,300,400,25,30
    """.strip().encode("utf-8")
    raw2 = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    2000,120,800,10,50
    2020,310,600,25,30
    """.strip().encode("utf-8")
    s1 = parse_putcall_data(raw1)
    s2 = parse_putcall_data(raw2)
    res = analyze_open_interest_changes(s2, s1, spot_price=2015.0)
    assert res.delta_total_call_oi == 30.0
    assert res.delta_total_put_oi == 500.0
    assert "גידור" in res.primary_regime_sentiment or "ביטוחי אסון" in res.primary_regime_sentiment
    assert len(res.detailed_insights) >= 1


def test_parse_tase_putvscall_chart_export():
    raw = """
מחזור ביחידות לפי מחיר מימוש - סוג עדכון:  חודשי -  תאריך פקיעה: 27/09/2026,,,
נכון ל- 09/09/2026
מחיר מימוש (Call),מחיר מימוש (Put),מחזור ביחידות  (Call),מחזור ביחידות  (Put)
4100.00,4100.00,20,100
4120.00,4120.00,50,80
4140.00,4140.00,100,30
4160.00,4160.00,150,10
""".strip().encode("utf-8-sig")

    assert auto_detect_series(raw, "PutVsCallChartData.csv") == "PUTCALL_CHART"
    res = parse_putcall_data(raw, "PutVsCallChartData.csv")
    assert len(res.strikes) == 4
    assert res.as_of_date == "2026-09-09"
    assert "27/09/2026" in res.expiry_label
    assert res.total_call_vol == 320.0
    assert res.total_put_vol == 220.0
    assert abs(res.pcr_vol - (220.0 / 320.0)) < 0.001
    assert res.call_wall_strike == 4160.0
    assert res.put_wall_strike == 4100.0


def test_calculate_max_pain_curve():
    strikes = [2000.0, 2020.0, 2040.0]
    call_ois = [100.0, 300.0, 500.0]
    put_ois = [500.0, 400.0, 100.0]
    curve = calculate_max_pain_curve(strikes, call_ois, put_ois)
    assert len(curve) == 3
    # At strike 2020, total loss should be the minimum among the 3 strikes
    pain_loss = [loss for s, loss in curve if s == 2020.0][0]
    for s, loss in curve:
        assert pain_loss <= loss


def test_build_putcall_research_product():
    raw1 = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    2000,100,500,10,50
    2020,300,400,25,30
    2040,500,200,40,15
    """.strip().encode("utf-8")
    raw2 = """
    Strike,Call OI,Put OI,Call Vol,Put Vol
    2000,120,800,10,50
    2020,310,600,25,30
    2040,550,150,40,15
    """.strip().encode("utf-8")
    s1 = parse_putcall_data(raw1)
    s2 = parse_putcall_data(raw2)

    product = build_putcall_research_product(s2, s1, spot_price=2025.0)
    assert product is not None
    assert product.has_data is True
    assert product.spot_price == 2025.0
    assert len(product.payout_curve) == 3
    assert product.has_delta is True
    assert product.oi_change is not None
    assert len(product.empirical_table) == 4
    assert len(product.strategic_takeaways) >= 2


