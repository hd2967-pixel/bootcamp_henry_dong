# Project Summary — Factor-Based Asset Return Model

## The problem

A portfolio manager wants to understand what drives a portfolio's daily excess return and how much to
trust the estimate. Rather than a single number, they need a model that names the exposures — to the
market, and to the size, value, and momentum factors — and a clear statement of how sensitive the answer
is to data-handling choices.

## What we did

We built a self-contained, end-to-end pipeline on a synthetic dataset of 250 business days:

1. **Generated** daily factor returns (market, size, value, momentum) and a portfolio excess return that
   depends on them (plus a small momentum-squared effect and heteroskedastic noise).
2. **Cleaned** it — filled 5% missing values and capped two injected momentum outliers.
3. **Profiled** it with an EDA summary and **engineered** features (momentum², lag, rolling volatility).
4. **Modeled** it with linear regression, using a time-ordered train/test split.
5. **Evaluated** it with bootstrap confidence intervals and scenario sensitivity.
6. **Packaged** it into a Flask API that serves predictions, and documented monitoring, handoff, and
   orchestration plans.

## What we found

- The market factor is by far the dominant driver (`mkt_excess` correlates with the return at ~0.73), and
  the model recovers the factor exposures reasonably well.
- The estimate is **more sensitive to the outlier treatment than to imputation** — capping outliers keeps
  the fitted relationship nearly unchanged, while the reported error can look better or worse depending on
  which rows are scored.
- Bootstrap confidence intervals are wider than Gaussian ones, because the return noise is heavy-tailed.

## What I would not rely on

- **The point estimate alone.** The uncertainty bands and the scenario table matter more than a single
  number.
- **The coefficients as clean economic quantities.** Heteroskedastic noise and a small omitted quadratic
  effect bias them slightly, so they are useful for prediction, not for precise inference.
- **Out-of-sample performance under a regime change.** The model is fit on one market regime; the
  monitoring plan exists precisely because that assumption can break.

## What I would do next

- Collect a longer history and add a formal regime check before trusting the model live.
- Predict **volatility** as well as the mean, since the risk side is at least as decision-relevant.
- Wire the API to the monitoring metrics in `docs/monitoring_plan.md` so drift triggers an alert instead of
  a surprise.
