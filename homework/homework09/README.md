# Homework 09 — Feature Engineering

This homework engineers features for a synthetic credit-default dataset and documents each one with
a rationale tied to EDA, plus a correlation check against the target.

## Files

- `homework09_feature-engineering_submission.ipynb` → main feature-engineering notebook
- `src/features.py` → reusable feature helpers

## Dataset

The notebook generates a small credit dataset in-memory (no CSV is written): `income`, `monthly_spend`,
`credit_score`, `region`, and a binary target `default_flag`. To make the correlation checks meaningful,
`default_flag` is generated with a realistic dependence on the spend-to-income ratio and credit score
(seeded for reproducibility, ~20% base rate).

## Engineered Features

| Feature | Type | Correlation with `default_flag` |
|---|---|---|
| `spend_income_ratio` | ratio (`monthly_spend / income`) | +0.37 (strongest feature) |
| `income_x_credit_score` | interaction (`income * credit_score`) | -0.30 |
| `high_spender_flag` | threshold flag (above-median spend) | +0.16 |
| `region_*` (one-hot) | categorical encoding | ≈ 0 (region does not predict default) |

## Reusable Helpers

`src/features.py` holds:

- `add_spend_income_ratio(df)`
- `add_income_credit_interaction(df)`
- `add_high_spender_flag(df)`
- `encode_region_onehot(df)`
- `create_features(df)` → runs all of the above

## Key Finding

The ratio and interaction features are *more* predictive than any raw column alone: `spend_income_ratio`
(+0.37) beats both `monthly_spend` (+0.22) and `income` (-0.27), and `income_x_credit_score` (-0.30)
beats `credit_score` (-0.20). The one-hot `region` columns are all ≈0, showing region carries no default
signal — which is itself a useful finding for feature selection.
