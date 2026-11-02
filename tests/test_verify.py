import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import analyze, insights, verify


def _facts():
    return analyze.compute_facts(analyze.load("data/sample_sales.csv"))


def test_correct_text_passes():
    f = _facts()
    text = f"Total sales were {f['total_sales']:,.2f} and margin was {f['profit_margin_pct']}%."
    assert all(r["ok"] for r in verify.verify(text, analyze.flatten_numbers(f)))


def test_wrong_number_is_flagged():
    f = _facts()
    text = f"Total sales were {f['total_sales'] * 1.2:,.2f}."
    assert not all(r["ok"] for r in verify.verify(text, analyze.flatten_numbers(f)))


def test_offline_insights_all_supported():
    f = _facts()
    text = insights.offline_insights(f)
    assert all(r["ok"] for r in verify.verify(text, analyze.flatten_numbers(f)))
