# Outlier Analysis — Assumptions & Risks

## What counts as an outlier here

The project dataset injects two extreme values into `momentum` (each `+0.03`, roughly 5 standard
deviations above the mean). We flag outliers with two rules from `src/outliers.py`:

- **IQR / Tukey's fences** — a value outside `Q1 ± 1.5·IQR`. Robust to the very extremes it flags.
- **Z-score** — a value with `|z| > 3`. Assumes a roughly normal distribution.

## What we do with them

We **winsorize** `momentum` at the 1st/99th percentiles (cap, don't delete) rather than removing rows.
Capping keeps every observation while limiting the influence of the two spikes.

## Assumptions

1. The two injected spikes are **data errors / extreme noise**, not genuine events. If they were real,
   capping them would understate tail risk.
2. `momentum` is otherwise roughly normal, so the 1st/99th percentile cutoff captures the right amount
   of tail.

## Risks if these assumptions are wrong

- If the spikes are **real** (a genuine momentum shock), winsorizing hides the exact risk we should be
  pricing, and the fitted model will look more stable than it is.
- The Z-score rule can **mask** moderate outliers when a few large values inflate the standard
  deviation, which is why the IQR rule is the primary detector here.
