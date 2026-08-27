# Homework 10b — Time Series & Classification

This homework builds leakage-free lag and rolling features on a synthetic regime-switching return
series, then fits `sklearn` pipelines for both a next-return forecast and a next-day direction
classifier, with a time-aware split and appropriate metrics.

## Files

- `homework10b_modeling-time-series-and-classification_submission.ipynb` → main notebook

## Dataset

A synthetic 500-day log-scale random walk with:

- a regime shift halfway through (mean and volatility both change), and
- five ~5% jumps for heavy tails.

The data is generated in-memory, seeded for reproducibility.

## Features (all leakage-free, `.shift(1)`-ed)

- `lag_1`, `lag_5`
- `roll_mean_5`, `roll_std_20`
- `momentum_10`, `zscore_20`

## Models & Results

| Track | Model | Result |
|---|---|---|
| Forecast | `StandardScaler` → `LinearRegression` | RMSE 0.0144 ≈ naive baseline 0.0145; R² ≈ 0.02 |
| Classify | `StandardScaler` → `LogisticRegression` | accuracy 0.53 (below majority baseline 0.55); recall for "up" 0.30 |
| Classify (cmp) | `StandardScaler` → `DecisionTreeClassifier` | accuracy 0.52 |

## Key Finding

The methodology (leakage-free features, time-aware split, pipelines, right metrics) is correct, but the
models cannot beat a naive baseline — the series is a (near-)random walk with no predictable structure.
The time-aware split also exposes a regime shift between train and test, which a shuffled split would
hide. The honest, risk-aware conclusion is that variance is more predictable than returns, so the next
step would be to forecast volatility (or add exogenous predictors) rather than chase a higher R².
