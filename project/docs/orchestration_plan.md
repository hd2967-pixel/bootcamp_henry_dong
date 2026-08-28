# Orchestration & System Design Plan

The pipeline decomposes into six tasks that run in a straight line (a chain, not a tree).

## 1) Task list

| # | Task | Inputs | Outputs | Idempotent? |
|---|---|---|---|---|
| 1 | ingest | (none — generated) | `data/raw/factor_returns.csv` | yes — seeded generator |
| 2 | clean | `data/raw/factor_returns.csv` | `data/processed/cleaned_data.csv` | yes — deterministic impute + winsorize |
| 3 | features | `data/processed/cleaned_data.csv` | `data/processed/featured_data.csv` | yes — deterministic transforms |
| 4 | train | `data/processed/featured_data.csv` | `model/model.pkl` | yes — deterministic OLS |
| 5 | evaluate | `model/model.pkl`, cleaned data | `data/processed/scenario_results.json`, `reports/images/*.png` | yes — seeded bootstrap |
| 6 | report | `reports/images/*`, scenario results | `reports/final_report.md` | yes |

## 2) Dependencies (DAG)

```
ingest -> clean -> features -> train -> evaluate -> report
```

No task can run in parallel — each consumes the previous one's output. (In a real multi-asset project,
`ingest` for several assets could fan out in parallel; here there is a single portfolio.)

## 3) Logging & checkpoints

- Each task logs `start`, `end`, row counts in/out, and the output artifact path
  (see `src/run_step.py` for the `clean` task's implementation).
- **Checkpoint = the output artifact.** If a later task fails, re-running only needs the checkpoint, not
  the whole chain — each task is idempotent and overwrites its own output.

## 4) Failure points & retry policy

- **Transient I/O errors** (missing dir, write lock): retry up to 3 times with linear backoff
  (0.5s → 1s → 1.5s).
- **Validation failures** (wrong schema, zero-variance feature): do **not** retry — fail fast and alert,
  because retrying will not fix a data problem.

## 5) Automate now vs. keep manual

- **Automate** `ingest`, `clean`, `features`, `train`: deterministic, no human judgment, cheap to re-run.
- **Keep manual** `evaluate` and `report`: a human should review the charts and the scenario table before
  a stakeholder sees them — this is where a silent bug would do the most reputational damage.
