# AI Analytics Verifier

An analytics workflow where **AI writes the insights but every number it uses is checked against the source data**.

## How it works
1. `analyze.py` computes all KPIs in pandas (sales, profit, margin, regions, categories, monthly trend, discount vs margin).
2. `sql_checks.py` recomputes key figures in SQL (SQLite, including a `RANK() OVER (PARTITION BY ...)` window function) and compares them with pandas.
3. `insights.py` sends the verified numbers to the Gemini API and asks for business insights. With no API key it uses an offline writer so the project still runs.
4. `verify.py` pulls every number out of the AI text and flags any that does not match a computed fact.
5. `main.py` writes `reports/report.md` and exits with an error if any number is unsupported.

## Run it
```bash
pip install -r requirements.txt
python make_sample_data.py                 # synthetic data; or use your own CSV with the same columns
python main.py data/sample_sales.csv       # offline writer
export GEMINI_API_KEY=your_key             # then use the real LLM
python main.py data/sample_sales.csv
python main.py data/sample_sales.csv --inject-error   # simulates an AI mistake; the verifier catches it
pytest
```
CSV columns: `order_id, order_date, region, category, discount, sales, profit`.

## Tools used
Python, pandas, SQL (SQLite), Gemini API, pytest.

## AI mistakes I caught
See `AI_MISTAKES.md` (log each real mistake: what the AI said, what the data said, how I fixed it).

## Limitations
The verifier checks that numbers match the data, not that the interpretation is sound. It can accept a correct number attached to the wrong claim, so a human still reads the insights.
