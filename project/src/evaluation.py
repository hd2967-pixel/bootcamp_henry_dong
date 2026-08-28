"""Reusable evaluation & uncertainty helpers.

- ``bootstrap_metric`` — bootstrap a metric's mean and percentile CI.
- ``bootstrap_predictions`` — bootstrap the fitted line to build a prediction band.
- ``bootstrap_scenario_mae`` — bootstrap the full impute->fit->predict pipeline.
"""

import numpy as np
from sklearn.linear_model import LinearRegression


def mae(y_true, y_pred):
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def rmse(y_true, y_pred):
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


def bootstrap_metric(y_true, y_pred, fn, n_boot=500, seed=42, alpha=0.05):
    """Bootstrap ``fn(y_true, y_pred)`` and return its mean and percentile CI."""
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    idx = np.arange(len(y_true))
    stats = [fn(y_true[b], y_pred[b])
             for b in (rng.choice(idx, size=len(idx), replace=True) for _ in range(n_boot))]
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"mean": float(np.mean(stats)), "lo": float(lo), "hi": float(hi)}


def bootstrap_predictions(X, y, x_grid, n_boot=500, seed=42, alpha=0.05):
    """Return (mean, lo, hi) prediction bands by resampling rows and refitting."""
    rng = np.random.default_rng(seed)
    X = np.asarray(X, dtype=float).reshape(-1, 1)
    y = np.asarray(y, dtype=float)
    xg = np.asarray(x_grid, dtype=float).reshape(-1, 1)
    idx = np.arange(len(y))
    preds = []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        m = LinearRegression().fit(X[b], y[b])
        preds.append(m.predict(xg))
    P = np.vstack(preds)
    return (P.mean(axis=0),
            np.percentile(P, 100 * alpha / 2, axis=0),
            np.percentile(P, 100 * (1 - alpha / 2), axis=0))


def bootstrap_scenario_mae(X_raw, y, process_fn, n_boot=500, seed=42, alpha=0.05):
    """Bootstrap the full scenario pipeline (process -> fit -> predict -> MAE)."""
    rng = np.random.default_rng(seed)
    X_raw = np.asarray(X_raw, dtype=float)
    y = np.asarray(y, dtype=float)
    idx = np.arange(len(y))
    maes = []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        Xp, yp = process_fn(X_raw[b], y[b])
        m = LinearRegression().fit(Xp.reshape(-1, 1), yp)
        yh = m.predict(Xp.reshape(-1, 1))
        maes.append(mae(yp, yh))
    return {"mean": float(np.mean(maes)),
            "lo": float(np.percentile(maes, 100 * alpha / 2)),
            "hi": float(np.percentile(maes, 100 * (1 - alpha / 2)))}
