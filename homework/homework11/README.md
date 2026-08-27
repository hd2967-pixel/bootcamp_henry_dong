# Homework 11 — Evaluation & Risk Communication

This homework quantifies uncertainty with bootstrap confidence intervals, compares three "what-if"
scenarios, checks stability across subgroups, and closes with a plain-language stakeholder summary.

## Files

- `homework11_evaluation-risk-communication_submission.ipynb` → main notebook
- `src/evaluation.py` → reusable evaluation & bootstrap helpers
- `data/raw/data_stage11_eval_risk.csv` → auto-generated dataset (fat-tailed errors, 5% missingness)
- `data/processed/scenario_results.csv` → scenario sensitivity table

## Dataset

Synthetic `y = 2.1 * x + 0.8 + t(3) * 1.1` with 5% missingness in `x_feature` and a random categorical
`segment`. The t-distributed errors make Gaussian confidence intervals overconfident and make the metric
reads worth checking.

## Methods

- **Bootstrap CI** — resample rows, refit, and take percentiles (≥600 resamples, seeded).
- **Gaussian vs bootstrap** prediction bands.
- **Scenario sensitivity** — mean vs median imputation vs dropping missing rows, each with a bootstrap CI
  on MAE and a fair shared-rows comparison.
- **Subgroup diagnostic** — residuals by segment.

## Key Findings

- The model recovers the true slope (≈2.13 vs true 2.1) under every scenario.
- Mean, median, and drop all give the same fit; **drop's lower MAE (1.06 vs 1.28) is an evaluation
  artifact** — it skips the 9 hard-to-predict missing rows (MAE ≈5.2 on those alone). On shared rows all
  three agree (≈1.07).
- The bootstrap CI for MAE is [1.06, 1.53], and the bootstrap prediction band is wider than the Gaussian
  band because the errors are fat-tailed.
- Segment C shows a wider residual spread (std 2.8 vs 1.8), but segments were assigned randomly, so this
  is heavy-tail noise in a small subgroup rather than a confirmed effect.
