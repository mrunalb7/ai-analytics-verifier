"""Step 3: ask an LLM to write insights from the verified numbers.
Uses Gemini if GEMINI_API_KEY is set; otherwise a built-in offline writer so the project runs anywhere."""
import json
import os
from dotenv import load_dotenv

load_dotenv()
PROMPT = """You are a business analyst. Write 5 short bullet-point insights for a manager.
Use ONLY the numbers in the JSON below, copied exactly as given. Do not invent or estimate any number.
Mention at least one risk and one recommendation.

FACTS:
{facts}
"""


def offline_insights(f: dict) -> str:
    worst_cat = min(f["category_profit"], key=f["category_profit"].get)
    best_region = max(f["region_sales"], key=f["region_sales"].get)
    m = f["margin_pct_by_discount"]
    lines = [
        f"- Total sales were {f['total_sales']:,.2f} with a profit margin of {f['profit_margin_pct']}% across {f['orders']} orders.",
        f"- {best_region} is the strongest region by sales at {f['region_sales'][best_region]:,.2f}.",
        f"- Risk: {worst_cat} lost {abs(f['category_profit'][worst_cat]):,.2f} in profit.",
        f"- Discounts hurt margin: {m.get('no discount')}% with no discount versus {m.get('over 20% discount')}% above 20% discount.",
        f"- Recommendation: review pricing and discount limits for {worst_cat}; best month was {f['best_month']} ({f['best_month_sales']:,.2f}).",
    ]
    return "\n".join(lines)


def gemini_insights(facts: dict) -> str:
    from google import genai  # pip install google-genai

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    model = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
    resp = client.models.generate_content(model=model, contents=PROMPT.format(facts=json.dumps(facts, indent=2)))
    return resp.text


def generate(facts: dict) -> tuple[str, str]:
    if os.environ.get("GEMINI_API_KEY"):
        return gemini_insights(facts), "gemini"
    return offline_insights(facts), "offline"

