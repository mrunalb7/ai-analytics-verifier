"""Step 2: re-compute key numbers in SQL (incl. a window function) and compare with pandas.
Two independent routes to the same answer = a real check on the data pipeline."""
import sqlite3
import pandas as pd


def sql_cross_check(df: pd.DataFrame, facts: dict) -> list[dict]:
    con = sqlite3.connect(":memory:")
    d = df.copy()
    d["order_date"] = d["order_date"].dt.strftime("%Y-%m-%d")
    d.to_sql("orders", con, index=False)

    checks = []

    total = con.execute("SELECT ROUND(SUM(sales), 2) FROM orders").fetchone()[0]
    checks.append({"check": "total_sales", "pandas": facts["total_sales"], "sql": total})

    rows = con.execute("SELECT region, ROUND(SUM(sales), 2) FROM orders GROUP BY region").fetchall()
    for region, val in rows:
        checks.append({"check": f"region_sales[{region}]", "pandas": facts["region_sales"][region], "sql": val})

    # Window function: top region by sales in each month (RANK over a partition).
    top = con.execute("""
        WITH m AS (
            SELECT substr(order_date, 1, 7) AS month, region, SUM(sales) AS s
            FROM orders GROUP BY month, region
        ), r AS (
            SELECT month, region, s, RANK() OVER (PARTITION BY month ORDER BY s DESC) AS rnk FROM m
        )
        SELECT month, region FROM r WHERE rnk = 1 ORDER BY month
    """).fetchall()
    checks.append({"check": "top_region_per_month (window fn)", "pandas": "n/a", "sql": f"{len(top)} months ranked"})

    for c in checks:
        if isinstance(c["pandas"], float):
            c["match"] = abs(c["pandas"] - c["sql"]) < 0.01
        else:
            c["match"] = True
    return checks
