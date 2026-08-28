# Lifecycle Framework Guide

One row per lifecycle stage, mapping it to the file or folder in this repo that holds that work, plus one
line on what was decided there.

| # | Stage | Where the work lives | What was decided |
|---|---|---|---|
| 1 | Problem Framing & Scoping | `README.md` | Frame a stakeholder-centered question: forecast a portfolio's excess return from four style factors. |
| 2 | Tooling Setup | `src/config.py`, `.gitignore`, `requirements.txt`, folder scaffold | Centralize paths/seed in `config.py`; env-driven paths; reproducible env. |
| 3 | Python Fundamentals | `src/utils.py`, `notebooks/python_fundamentals_summary.ipynb` | Data-gen + IO utilities as the first reusable functions. |
| 4 | Data Acquisition & Ingestion | `src/utils.py::generate_factor_data`, `data/raw/`, `.env.example` | Self-contained seeded generator (no external keys) as the ingestion layer. |
| 5 | Data Storage | `data/processed/`, `src/utils.py::save_dataframe/load_dataframe` | CSV for raw, Parquet+CSV for processed; env-driven paths. |
| 6 | Data Preprocessing | `src/cleaning.py` | Median-impute missing `value`; min-max scaling available. |
| 7 | Outlier Analysis | `src/outliers.py`, `docs/outliers.md` | Winsorize `momentum` at 1/99% rather than delete rows. |
| 8 | EDA | `src/eda.py`, `notebooks/eda.ipynb` | `eda_summary()` profiles numeric + categorical and flags attention. |
| 9 | Feature Engineering | `src/features.py` | Add `momentum_sq`, lag-1, rolling mean/vol (leakage-free). |
| 10a | Modeling (regression) | `notebooks/modeling_regression.ipynb` | Baseline 4-factor OLS + residual diagnostics. |
| 10b | Modeling (time series) | `notebooks/project_pipeline.ipynb` (time-aware split) | Time-ordered train/test split for the same model. |
| 11 | Evaluation & Risk | `src/evaluation.py`, `data/processed/scenario_results.json` | Bootstrap CI + scenario sensitivity (impute / outlier). |
| 12 | Delivery Design | `reports/final_report.md`, `reports/images/` | Stakeholder markdown report with charts and Δ-from-baseline. |
| 13 | Productization | `app.py`, `model/model.pkl` | Flask API with `/predict` (POST + GET) loading the model once. |
| 14 | Deployment & Monitoring | `docs/monitoring_plan.md`, `docs/handoff_plan.md` | Four-layer metrics (data/model/system/business) + runbook. |
| 15 | Orchestration | `docs/orchestration_plan.md`, `src/run_step.py` | Six-task DAG; `clean` refactored into a CLI task. |
| 16 | Lifecycle Review | this guide + `docs/project_summary.md` | Map the whole chain to the repo; polish for a stranger. |

The single thread that runs every stage end-to-end is `notebooks/project_pipeline.ipynb`.
