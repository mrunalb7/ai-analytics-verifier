# AI insights with verification

Insight writer: **gemini**

## Insights
* **Overall Performance & Sales:** Total sales reached 720883.28 across 1000 orders, with an avg_order_value of 720.88, leading to a total_profit of 2026.58 and a profit_margin_pct of 0.28.
* **Monthly Highs and Lows:** Sales peaked in July 2024 with best_month_sales of 66322.38, while the weakest period occurred in April 2024 with worst_month_sales of 47947.8.
* **Regional Disparities:** The West region generated 186626.68 in sales but represents a critical risk by posting a regional loss of -1451.77, contrasting with the South region's regional profit of 2456.65 (on 173411.84 in sales).
* **Category Profitability Risk:** Furniture (category_sales of 184881.33 and category_profit of -5637.29) and Tables (category_sales of 174153.73 and category_profit of -27988.22) are both loss_making_categories, dragging down overall profitability despite strong Technology profits of 25718.75.
* **Recommendation on Discounting:** Given that margins drop into negative territory as discounts exceed the discount_threshold_pct of 20 (resulting in margin_pct_by_discount of -1.08 for 1-20% and -13.06 for over 20%), management must restrict deep discounting to protect the baseline margin of 8.27 achieved with no discount.

## SQL vs pandas cross-check

| check | pandas | sql | match |
|---|---|---|---|
| total_sales | 720883.28 | 720883.28 | yes |
| region_sales[Central] | 173405.03 | 173405.03 | yes |
| region_sales[East] | 187439.73 | 187439.73 | yes |
| region_sales[South] | 173411.84 | 173411.84 | yes |
| region_sales[West] | 186626.68 | 186626.68 | yes |
| top_region_per_month (window fn) | n/a | 12 months ranked | yes |

## Number verification

22 of 23 numbers in the AI text match the computed data.

**Unsupported numbers (do not send to stakeholders):**
- 1.0