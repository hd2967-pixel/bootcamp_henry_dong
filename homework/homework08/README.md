# Homework 08 — Exploratory Data Analysis (EDA)

This homework profiles a synthetic financial-behavior dataset end to end: numeric and categorical
summaries, distribution and relationship plots, a time-axis read, and a written "so what" that feeds
the next two stages (feature engineering and time-series modeling).

## Files

- `homework08_exploratory-data-analysis_submission.ipynb` → main EDA notebook
- `src/eda.py` → reusable profiling helpers

## Dataset

The notebook generates the data in-memory (no CSV is written for this assignment) with the starter's
synthetic generator, seeded for reproducibility. Six columns:

- `date` (datetime), `region` (categorical), `age`, `income`, `transactions`, `spend`
- `spend` is generated as `income * 0.0015 + transactions * 18 + noise`
- 5 missing values injected in `income`, 3 in `spend`, and two extreme `transactions` spikes (20 vs. a median of 3)

## Reusable Helpers

`src/eda.py` holds:

- `eda_summary(df)` → one-call numeric + categorical profile, missingness, and attention flags
- `flag_columns(df)` → flags high missingness, near-zero variance, and one-category-dominates columns

## Key Findings

1. `transactions` (r ≈ 0.48) and `income` (r ≈ 0.31) drive `spend`; `age` is unrelated (r ≈ 0).
2. Two `transactions` spikes are outliers whose `spend` is unremarkable — a data-quality flag.
3. The time axis is stationary noise: no trend, seasonality, level shift, or gaps.

These findings determine what stage 09 should clean/engineer (impute, winsorize, log-transform income,
drop age) and what stage 10b should expect (a level model, not a trend model).
