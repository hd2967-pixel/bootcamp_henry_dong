# Homework 07 — Outliers + Risk Assumptions

This homework implements reusable outlier detection/handling functions, runs a simple
sensitivity analysis, and documents the assumptions and risks behind each choice.

## Files

- `homework07_outliers-risk-assumptions_submission.ipynb` → main notebook
- `src/outliers.py` → reusable outlier functions
- `data/raw/outliers_homework.csv` → generated dataset (no dataset is handed out for this assignment)
- `data/processed/` → reserved for processed outputs

## Dataset

The Setup cell in the notebook generates a synthetic time series of business-day dates
(2022-01-03 to 2022-06-10) with two correlated numeric columns:

- `daily_return` — normally distributed returns with a slight pre-May downward shift and five
  large "shock" values injected in May.
- `daily_return_2` — generated as `0.6 * daily_return + noise`, so its true relationship to
  `daily_return` is a slope of about 0.6.

The data has no missing values (that was Stage 06); this stage is about outliers.

## Outlier Methods

The reusable logic lives in `src/outliers.py`:

- `detect_outliers_iqr(series, k=1.5)` → flags values outside `Q1 ± k * IQR` (Tukey's fences)
- `detect_outliers_zscore(series, threshold=3.0, ddof=0)` → flags values with `|z| > threshold`
- `winsorize_series(series, lower=0.05, upper=0.95)` → clips extreme values at quantile bounds

Each function returns a new object (never mutates input), rejects empty/non-numeric input with a
clear error, validates its parameters, and documents its NaN behavior.

## Sensitivity Analysis

The notebook compares three treatments of `daily_return`:

1. **all** — every observation kept.
2. **filtered_iqr** — rows flagged by the IQR rule removed.
3. **winsorized** — extreme values capped at the 5th/95th percentile (no rows removed).

It reports summary statistics (mean / median / std) and fits a simple least-squares regression of
`daily_return_2` on `daily_return` for each treatment, comparing slope, intercept, R², and MAE.

## Key Finding

The injected "shocks" are genuine, consistent with the true relationship, so removing them does
*not* improve the model — in-sample R² falls and the slope estimate moves slightly away from the
true 0.6. The reflection discusses why treating real events as errors is risky.
