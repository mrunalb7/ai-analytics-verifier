"""Run: python main.py data/sample_sales.csv   (add --inject-error to see the verifier catch a bad number)"""
import argparse
import re

from pathlib import Path

import analyze, sql_checks, insights, verify


def inject_error(text: str) -> str:
    """Simulate an AI hallucination: change the first big number in the text."""
    m = re.search(r"D:\\ai-analytics-verifier\\data\\sample_sales.csv", text)
    return text[: m.start()] + "9,999,999.99" + text[m.end():] if m else text


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--inject-error", action="store_true")
    a = ap.parse_args()

    df = analyze.load(a.csv)
    facts = analyze.compute_facts(df)
    sql = sql_checks.sql_cross_check(df, facts)
    text, source = insights.generate(facts)
    if a.inject_error:
        text = inject_error(text)
    checks = verify.verify(text, analyze.flatten_numbers(facts))

    bad = [c for c in checks if not c["ok"]]
    out = ["# AI insights with verification", "", f"Insight writer: **{source}**", "", "## Insights", text, "",
           "## SQL vs pandas cross-check", "", "| check | pandas | sql | match |", "|---|---|---|---|"]
    out += [f"| {c['check']} | {c['pandas']} | {c['sql']} | {'yes' if c['match'] else 'NO'} |" for c in sql]
    out += ["", "## Number verification", "",
            f"{len(checks) - len(bad)} of {len(checks)} numbers in the AI text match the computed data.", ""]
    if bad:
        out += ["**Unsupported numbers (do not send to stakeholders):**"] + [f"- {c['number']}" for c in bad]
    Path("reports").mkdir(exist_ok=True)
    Path("reports/report.md").write_text("\n".join(out))
    print("\n".join(out))
    raise SystemExit(1 if bad else 0)


if __name__ == "__main__":
    main()
