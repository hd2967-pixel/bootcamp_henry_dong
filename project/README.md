# Factor-Based Asset Return Model

## Summary

This project builds an end-to-end model of a portfolio's daily **excess return** from four style-factor
exposures — **market, size, value, and momentum**. It matters because a portfolio manager needs to know
not just *what* the expected return is, but *which factor exposures drive it* and *how much to trust the
estimate* under different data-handling assumptions.

The project is self-contained: it generates its own dataset (no external keys or files), so anyone can
reproduce it from a fresh clone.

## Stakeholder

**Portfolio manager / investment committee** (non-technical). They care about: (1) what drives the return,
(2) how confident we are in the estimate, and (3) what breaks the model. They want decision-oriented
headlines and a clear range, not a single point estimate.

## Goals → lifecycle → deliverables

| Goal | Lifecycle stage | Deliverable |
|---|---|---|
| Frame the question and audience | 1. Problem Framing | this README |
| Reproducible environment & structure | 2. Tooling Setup | `src/config.py`, `requirements.txt`, `.gitignore` |
| Foundational Python + reusable utils | 3. Python Fundamentals | `src/utils.py`, `notebooks/python_fundamentals_summary.ipynb` |
| Generate/acquire data | 4. Data Acquisition | `src/utils.py::generate_factor_data`, `data/raw/` |
| Reproducible storage | 5. Data Storage | `data/processed/`, `src/utils.py` save/load |
| Clean the data | 6. Preprocessing | `src/cleaning.py` |
| Handle outliers | 7. Outlier Analysis | `src/outliers.py`, `docs/outliers.md` |
| Understand the data | 8. EDA | `src/eda.py`, `notebooks/eda.ipynb` |
| Create features | 9. Feature Engineering | `src/features.py` |
| Fit a model | 10a/10b. Modeling | `notebooks/modeling_regression.ipynb` |
| Evaluate & communicate risk | 11. Evaluation | `src/evaluation.py`, `data/processed/scenario_results.json` |
| Stakeholder deliverable | 12. Delivery | `reports/final_report.md`, `reports/images/` |
| Package for reuse | 13. Productization | `app.py`, `model/model.pkl` |
| Monitor & hand off | 14. Deployment/Monitoring | `docs/monitoring_plan.md`, `docs/handoff_plan.md` |
| Orchestrate the pipeline | 15. Orchestration | `docs/orchestration_plan.md`, `src/run_step.py` |
| Review the whole lifecycle | 16. Lifecycle Review | `docs/lifecycle_framework_guide.md`, `docs/project_summary.md` |

The single thread that runs every stage end-to-end is `notebooks/project_pipeline.ipynb`.

## Folder structure

```
project/
├── data/
│   ├── raw/          # generated raw dataset (factor_returns.csv)
│   └── processed/    # cleaned + featured data, scenario results
├── notebooks/        # pipeline + EDA + modeling + fundamentals notebooks
├── src/              # reusable modules (config, utils, cleaning, outliers, eda, features, evaluation, run_step)
├── docs/             # outlier, monitoring, handoff, orchestration, lifecycle, summary docs
├── reports/          # stakeholder report + exported charts
├── model/            # saved model (model.pkl)
├── app.py            # Flask API
├── requirements.txt
└── README.md
```

## Setup & running from a fresh clone

```bash
git clone <repo-url>
cd project
pip install -r requirements.txt
cp .env.example .env        # set paths / seed (never commit .env)
```

Run the full analysis top-to-bottom:

```bash
jupyter nbconvert --to notebook --execute notebooks/project_pipeline.ipynb
```

Or run one task standalone (the clean step, with logging):

```bash
python src/run_step.py --input data/raw/factor_returns.csv --output data/processed/cleaned_data.csv
```

## Data storage

- **`data/raw/`** — the generated `factor_returns.csv` (human-readable, easy to inspect).
- **`data/processed/`** — `cleaned_data.csv` (and `.parquet`) plus `scenario_results.json`.
- Code reads and writes through `src/utils.py::save_dataframe` / `load_dataframe`, which pick CSV or
  Parquet by suffix. Paths come from environment variables set in `.env` (defaults in `src/config.py`).

## Engineered features (stage 9)

- `momentum_sq` — squared momentum, so the linear model can capture the known small quadratic effect.
- `asset_excess_lag1` — yesterday's return (past info only).
- `asset_excess_rollmean_5` — 5-day rolling mean, shifted by 1 (no leakage).
- `asset_excess_rollstd_20` — 20-day rolling volatility, shifted by 1.

## API usage (stage 13)

Start the server (runs on `http://127.0.0.1:5001`):

```bash
python app.py
```

Predict from the four factor exposures:

```bash
curl -X POST http://127.0.0.1:5001/predict \
     -H "Content-Type: application/json" \
     -d '{"features": [0.01, 0.0, 0.0, 0.0]}'
# -> {"prediction": 0.009...}
```

```bash
curl http://127.0.0.1:5001/predict/0.01/0.0/0.0/0.0
```

Bad input returns a JSON error with HTTP 400 (missing/wrong feature count, or non-numeric values).

## Assumptions, risks, next steps

See `docs/outliers.md`, `docs/monitoring_plan.md`, `docs/handoff_plan.md`,
`docs/orchestration_plan.md`, and `docs/project_summary.md` for the full write-up. In one line: **the model
is useful for prediction but not for precise inference**, its estimate is most sensitive to the outlier
rule, and it should be monitored for drift before any live use.
