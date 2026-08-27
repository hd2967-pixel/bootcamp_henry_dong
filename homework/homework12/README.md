# Homework 12 — Results Reporting & Delivery Design

This homework turns a synthetic risk-return analysis into a stakeholder-ready deliverable: polished charts,
a sensitivity/tornado analysis, and plain-language assumptions, risks, and decision implications.

## Files

- `homework12_results-reporting-delivery-design_submission.ipynb` → analysis + chart-generation notebook
- `reports/final_report.md` → the assembled stakeholder deliverable (charts embedded)
- `reports/images/*.png` → exported figures
- `reports/README.md` → chosen audience and format rationale

## Deliverable

The notebook generates four scenarios of the same strategy (Baseline / Mean impute / Keep outliers /
Winsorize 5–95%) and produces:

1. a risk–return scatter,
2. a return-by-scenario bar chart,
3. a 24-month cumulative-return line chart, and
4. a tornado chart of Δ-return vs. baseline.

The key finding: the strategy's reported return is more sensitive to the **outlier rule** (up to +1.5 pp
return, +3.5 pp volatility) than to the imputation choice, so the conservative baseline is the right number
to quote.
