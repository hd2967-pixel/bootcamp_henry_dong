"""Reusable feature-engineering functions.

Each helper adds one engineered feature and returns a *new* DataFrame.
- ``add_quadratic`` — a squared term (captures the known nonlinear momentum effect).
- ``add_lag`` — lagged returns.
- ``add_rolling`` — rolling mean / std (volatility).
- ``create_features`` — run all of the above.
"""

import numpy as np
import pandas as pd


def add_quadratic(df, col="momentum", out="momentum_sq"):
    """Add a squared term for ``col``.

    Rationale: the true return model has a small quadratic momentum effect, so the
    squared term lets a linear model capture that curvature without changing its
    linear-in-parameters form.
    """
    result = df.copy()
    result[out] = result[col] ** 2
    return result


def add_lag(df, col="asset_excess", k=1, out=None):
    """Add a lag-``k`` column (only past information — no leakage)."""
    result = df.copy()
    name = out or f"{col}_lag{k}"
    result[name] = result[col].shift(k)
    return result


def add_rolling(df, col="asset_excess", window=5, stat="mean", out=None):
    """Add a rolling statistic (mean or std) of ``col``, shifted by 1 to avoid leakage."""
    result = df.copy()
    name = out or f"{col}_roll{stat}_{window}"
    roll = result[col].rolling(window)
    result[name] = (roll.mean() if stat == "mean" else roll.std()).shift(1)
    return result


def create_features(df):
    """Engineer the project's feature set and return the augmented DataFrame."""
    result = add_quadratic(df)
    result = add_lag(result, col="asset_excess", k=1)
    result = add_rolling(result, col="asset_excess", window=5, stat="mean")
    result = add_rolling(result, col="asset_excess", window=20, stat="std")
    return result
