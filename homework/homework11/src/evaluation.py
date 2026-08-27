"""Reusable evaluation & risk-communication helpers for Homework 11.

These functions power the notebook's baseline fit, bootstrap confidence intervals,
scenario sensitivity, and metric bootstrapping. They are deliberately small and
dependency-light so each can be reused or unit-tested in isolation.

Deviations from the starter: the starter's hand-rolled ``SimpleLinReg`` is replaced by
``sklearn.linear_model.LinearRegression`` (identical least-squares result, but the
standard, tested implementation).
"""

import numpy as np
from sklearn.linear_model import LinearRegression


# --- Imputation -------------------------------------------------------------

def mean_impute(a):
    """Return a copy of ``a`` with NaN replaced by the mean of the observed values."""
    m = np.nanmean(a)
    out = np.asarray(a, dtype=float).copy()
    out[np.isnan(out)] = m
    return out


def median_impute(a):
    """Return a copy of ``a`` with NaN replaced by the median of the observed values."""
    m = np.nanmedian(a)
    out = np.asarray(a, dtype=float).copy()
    out[np.isnan(out)] = m
    return out


# --- Model / metrics --------------------------------------------------------

def fit_ols(X, y):
    """Fit simple least-squares ``y ~ 1 + X`` and return the fitted model."""
    X = np.asarray(X, dtype=float).reshape(-1, 1)
    return LinearRegression().fit(X, y)


def predict(model, X):
    """Return predictions for ``X`` from a fitted model."""
    return model.predict(np.asarray(X, dtype=float).reshape(-1, 1))


def mae(y_true, y_pred):
    """Mean absolute error."""
    return float(np.mean(np.abs(np.asarray(y_true) - np.asarray(y_pred))))


def rmse(y_true, y_pred):
    """Root mean squared error."""
    return float(np.sqrt(np.mean((np.asarray(y_true) - np.asarray(y_pred)) ** 2)))


# --- Bootstrap --------------------------------------------------------------

def bootstrap_metric(y_true, y_pred, fn, n_boot=500, seed=111, alpha=0.05):
    """Bootstrap a metric ``fn(y_true, y_pred)`` and return its mean and percentile CI.

    Resamples the *paired* observations with replacement and recomputes the metric on
    each resample. This captures the sampling uncertainty of the metric itself.
    """
    rng = np.random.default_rng(seed)
    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    idx = np.arange(len(y_true))
    stats = [
        fn(y_true[b], y_pred[b])
        for b in (rng.choice(idx, size=len(idx), replace=True) for _ in range(n_boot))
    ]
    lo, hi = np.percentile(stats, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return {"mean": float(np.mean(stats)), "lo": float(lo), "hi": float(hi)}


def bootstrap_predictions(X, y, x_grid, n_boot=500, seed=111, alpha=0.05):
    """Return (mean, lo, hi) prediction bands by resampling rows, refitting, predicting.

    This is a non-parametric bootstrap of the fitted regression line: each resample
    refits the model, and the band is the percentile of the refitted predictions at
    each grid point. Unlike the Gaussian band, it does not assume normal errors.
    """
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
    lo = np.percentile(P, 100 * alpha / 2, axis=0)
    hi = np.percentile(P, 100 * (1 - alpha / 2), axis=0)
    return P.mean(axis=0), lo, hi


def bootstrap_scenario_mae(X_raw, y, process_fn, n_boot=500, seed=111, alpha=0.05):
    """Bootstrap the full *scenario* pipeline and return MAE (and slope) with CIs.

    ``process_fn(X, y)`` returns ``(X_processed, y_processed)`` for one scenario —
    e.g. mean imputation, median imputation, or dropping missing rows. Each bootstrap
    resample is pushed through the whole pipeline (process -> fit -> predict -> MAE),
    so the CI reflects the uncertainty of the *scenario decision*, not just the metric.
    """
    rng = np.random.default_rng(seed)
    X_raw = np.asarray(X_raw, dtype=float)
    y = np.asarray(y, dtype=float)
    idx = np.arange(len(y))
    maes, slopes = [], []
    for _ in range(n_boot):
        b = rng.choice(idx, size=len(idx), replace=True)
        Xp, yp = process_fn(X_raw[b], y[b])
        m = fit_ols(Xp, yp)
        yh = predict(m, Xp)
        maes.append(mae(yp, yh))
        slopes.append(float(m.coef_[0]))
    return {
        "mae_mean": float(np.mean(maes)),
        "mae_lo": float(np.percentile(maes, 100 * alpha / 2)),
        "mae_hi": float(np.percentile(maes, 100 * (1 - alpha / 2))),
        "slope_mean": float(np.mean(slopes)),
        "slope_lo": float(np.percentile(slopes, 100 * alpha / 2)),
        "slope_hi": float(np.percentile(slopes, 100 * (1 - alpha / 2))),
    }
