"""Generate a small synthetic retail dataset so the project runs without any download.
Swap in your own CSV (same columns) such as your 9,994-row retail dataset."""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
n = 2000
regions = ["West", "East", "Central", "South"]
categories = {"Furniture": 0.04, "Technology": 0.22, "Office Supplies": 0.14, "Tables": -0.08}

rows = []
for i in range(n):
    cat = rng.choice(list(categories))
    discount = float(rng.choice([0, 0, 0, 0.1, 0.2, 0.3, 0.4]))
    sales = float(round(rng.gamma(2.0, 180), 2))
    base_margin = categories[cat] - discount * 0.6
    profit = round(sales * (base_margin + rng.normal(0, 0.03)), 2)
    rows.append({
        "order_id": f"ORD-{i // 2:05d}",
        "order_date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(rng.integers(0, 365))),
        "region": rng.choice(regions),
        "category": cat,
        "discount": discount,
        "sales": sales,
        "profit": profit,
    })
pd.DataFrame(rows).to_csv("data/sample_sales.csv", index=False)
print("wrote data/sample_sales.csv", n, "rows")
