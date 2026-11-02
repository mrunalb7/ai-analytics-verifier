"""Step 4: the key step. Every number in the AI text must match a computed fact, or it is flagged."""
import re

NUM = re.compile(r"-?\d[\d,]*\.?\d*")


def extract_numbers(text: str) -> list[float]:
    out = []
    for m in NUM.findall(text):
        s = m.replace(",", "").rstrip(".")
        try:
            out.append(float(s))
        except ValueError:
            pass
    return out


def _close(a: float, b: float) -> bool:
    # allow rounding: 0.05 on small values, 0.1% on large ones
    return abs(a - b) <= max(0.051, 0.001 * abs(b))


def verify(text: str, fact_numbers: list[tuple[str, float]]) -> list[dict]:
    results = []
    for n in extract_numbers(text):
        if 1990 <= n <= 2100 and float(n).is_integer():  # years in month names
            continue
        match = next((label for label, v in fact_numbers if _close(abs(n), abs(v))), None)
        results.append({"number": n, "supported_by": match, "ok": match is not None})
    return results
