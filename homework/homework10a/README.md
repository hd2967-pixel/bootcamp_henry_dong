# Homework 10a — Modeling: Linear Regression

This homework fits a baseline linear regression on a synthetic asset-return dataset, diagnoses the four
regression assumptions from its residuals, adds a squared (transformed) feature, and concludes with a
trust assessment that separates prediction from explanation.

## Files

- `homework10a_modeling-linear-regression_submission.ipynb` → main modeling notebook
- `data/` → not used; the dataset is generated in-memory (seeded for reproducibility)

## Dataset

A synthetic 200-day asset-return series generated from four style factors (`mkt_excess`, `size`, `value`,
`momentum`). The true data-generating process deliberately includes:

- a quadratic term `+3.5 * momentum^2` that the baseline model omits, and
- heteroskedastic noise whose standard deviation grows with `|mkt_excess|`.

So the residual diagnostics have two real violations to find.

## Model & Diagnostics

- **Fit**: `sklearn.linear_model.LinearRegression`, time-ordered 80/20 split (`shuffle=False`).
- **Metrics**: out-of-sample R² ≈ 0.37, RMSE ≈ 0.0085 (vs. outcome std ≈ 0.011).
- **Diagnostics**: residuals vs fitted, vs `momentum` and vs `mkt_excess`, histogram + QQ, and a lag-1
  residual plot.

## Key Findings

| Assumption | Verdict | Evidence |
|---|---|---|
| Linearity | mildly violated, negligible effect | `corr(residual, momentum²) = +0.34`, but the term contributes ~0.0001 vs noise ~0.008 |
| Homoscedasticity | **clearly violated** | `corr(\|residual\|, \|mkt_excess\|) = +0.57`, funnel-shaped spread |
| Normality | roughly OK, heavy tails | skew +0.51, kurtosis +1.22, Shapiro p=0.24 |
| Independence | satisfied | lag-1 autocorrelation +0.26, inside ±0.31 band |

## Conclusion

Trustworthy for **prediction** (beats a mean-only baseline, out-of-sample), but **not for explanation**:
the coefficients are biased by the omitted quadratic term and the heteroscedasticity. Adding `momentum^2`
barely changes R² (0.3677 → 0.3681), because the nonlinearity is tiny relative to the noise — and it does
nothing for the heteroscedasticity, which is the real issue.
