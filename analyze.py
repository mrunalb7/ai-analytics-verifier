"""Step 1: compute every KPI in pandas. These numbers are the single source of truth."""
import pandas as pd

REQUIRED = {"order_id", "order_date", "region", "category", "discount", "sales", "profit"}


def load(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"CSV is missing columns: {sorted(missing)}")
    return df


def compute_facts(df: pd.DataFrame) -> dict:
    total_sales = df["sales"].sum()
    total_profit = df["profit"].sum()
    orders = df["order_id"].nunique()

    facts = {
        "total_sales": round(total_sales, 2),
        "total_profit": round(total_profit, 2),
        "profit_margin_pct": round(100 * total_profit / total_sales, 2),
        "orders": int(orders),
        "avg_order_value": round(total_sales / orders, 2),
    }

    by_region = df.groupby("region")[["sales", "profit"]].sum().round(2)
    facts["region_sales"] = by_region["sales"].to_dict()
    facts["region_profit"] = by_region["profit"].to_dict()

    by_cat = df.groupby("category")[["sales", "profit"]].sum().round(2)
    facts["category_sales"] = by_cat["sales"].to_dict()
    facts["category_profit"] = by_cat["profit"].to_dict()
    facts["loss_making_categories"] = sorted(by_cat.index[by_cat["profit"] < 0])

    monthly = df.set_index("order_date").resample("MS")["sales"].sum().round(2)
    facts["best_month"] = monthly.idxmax().strftime("%B %Y")
    facts["best_month_sales"] = float(monthly.max())
    facts["worst_month"] = monthly.idxmin().strftime("%B %Y")
    facts["worst_month_sales"] = float(monthly.min())

    bins = pd.cut(df["discount"], [-0.001, 0.0, 0.2, 1.0], labels=["no discount", "1-20% discount", "over 20% discount"])
    g = df.groupby(bins, observed=True)[["sales", "profit"]].sum()
    facts["discount_threshold_pct"] = 20
    facts["margin_pct_by_discount"] = {str(k): round(100 * v.profit / v.sales, 2) for k, v in g.iterrows()}
    return facts


def flatten_numbers(facts: dict) -> list[tuple[str, float]]:
    """Every numeric fact as (label, value). Used by the verifier."""
    out = []
    for k, v in facts.items():
        if isinstance(v, dict):
            out += [(f"{k}[{kk}]", float(vv)) for kk, vv in v.items() if isinstance(vv, (int, float))]
        elif isinstance(v, (int, float)):
            out.append((k, float(v)))
    return out
