# Deployment & Monitoring Plan

If the factor model were deployed to predict a portfolio's daily excess return, here is what would have
to be true for it to keep working — and who would notice when it stops.

## Failure modes, metrics, and thresholds

| Layer | Failure mode | Metric | Starting threshold |
|---|---|---|---|
| **Data** | Batch stalls / feed gap | Freshness (minutes since last batch) | > 60 min |
| **Data** | Rising missingness in `value` | Null rate on `value` | > 10% (baseline 5%) |
| **Data** | Schema drift (renamed/dropped factor) | Schema hash mismatch | any change |
| **Model** | Prediction quality decay | 20-day rolling MAE vs. baseline | > 1.5× baseline MAE |
| **Model** | Loss of explanatory power | 2-week rolling R² | < 0.30 |
| **Model** | Feature distribution shift | PSI on `mkt_excess` | > 0.05 |
| **System** | Slow responses | p95 latency | > 250 ms |
| **System** | Failing jobs | Job success rate | < 99% |
| **Business** | Model tracks reality poorly | Tracking error (predicted vs realized) | > 2× historical |

## Alert recipients & first runbook step

- **Data alerts** → Data on-call. First step: check the upstream feed and re-pull the last batch.
- **Model alerts** → Analytics team. First step: re-run the pipeline on fresh data and inspect drift.
- **System alerts** → Platform on-call. First step: check the server logs and restart the API.
- **Business alerts** → Portfolio manager. First step: freeze trading on the model until reviewed.

## Retraining cadence / triggers

- Scheduled retraining **weekly** (Monday), and immediately on any **PSI > 0.05** on a key feature or
  **2-week rolling R² < 0.30**.

## Ownership

- **Who updates dashboards:** Analytics team, weekly.
- **Who approves rollbacks:** the portfolio manager, with the analytics lead as reviewer.
- **Where issues are logged:** a shared issue tracker, one ticket per alert, linked to the runbook.
