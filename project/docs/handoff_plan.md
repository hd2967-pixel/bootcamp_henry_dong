# Deployment Path & Runbook — Handoff Plan

The path an on-call operator would follow to run, deploy, and respond to issues.

- **Start the API:** from the project root, `python app.py` (serves on `http://127.0.0.1:5001`).
- **Regenerate data + model:** run `notebooks/project_pipeline.ipynb` top-to-bottom, or run the clean
  step standalone via `python src/run_step.py --input data/raw/factor_returns.csv --output data/processed/cleaned_data.csv`.
- **Rebuild the environment:** `pip install -r requirements.txt`.
- **Secrets:** copy `.env.example` to `.env` and set the paths/seed (never commit `.env`).
- **Model artifact:** `model/model.pkl` — retrain and re-save it if any factor's distribution shifts.
- **Data alerts** → `docs/monitoring_plan.md` (freshness / null-rate / schema thresholds).
- **Model alerts** → `docs/monitoring_plan.md` (rolling MAE / R² / PSI thresholds).
- **System alerts** → `docs/monitoring_plan.md` (p95 latency / job success rate).
- **Rollback:** restore the previous `model/model.pkl` and re-run the last known-good pipeline commit.
- **Where it is logged:** the shared issue tracker; each alert links back to the relevant runbook row.
