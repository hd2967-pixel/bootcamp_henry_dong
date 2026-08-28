"""Reusable outlier detection and handling functions.

- ``detect_outliers_iqr`` — Tukey's-fences rule (robust to skew).
- ``detect_outliers_zscore`` — Z-score rule (assumes a roughly normal shape).
- ``winsorize_series`` — clip extreme values at quantile boundaries.

Every function returns a new object and never mutates its input. NaN values are left
in place and not flagged (missingness is handled in the cleaning stage).
"""

import pandas as pd


def _validate_series(series):
    """Return a copy of ``series`` after checking it is a non-empty numeric Series."""
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas.Series")
    if series.empty:
        raise ValueError("series must not be empty")
    if not pd.api.types.is_numeric_dtype(series.dtype):
        raise ValueError("series must be numeric")
    return series.copy()


def detect_outliers_iqr(series, k=1.5):
    """Return a boolean mask flagging IQR-based (Tukey's-fences) outliers.

    A value is flagged when it falls below ``Q1 - k*IQR`` or above ``Q3 + k*IQR``.
    """
    series = _validate_series(series)
    if not isinstance(k, (int, float)) or k <= 0:
        raise ValueError("k must be a positive number")
    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    return (series < q1 - k * iqr) | (series > q3 + k * iqr)


def detect_outliers_zscore(series, threshold=3.0, ddof=0):
    """Return a boolean mask flagging Z-score outliers where ``|z| > threshold``.

    ``ddof=0`` treats the observed data as the full population (the conventional
    choice for this rule); a constant series returns an all-False mask.
    """
    series = _validate_series(series)
    if not isinstance(threshold, (int, float)) or threshold <= 0:
        raise ValueError("threshold must be a positive number")
    mu = series.mean()
    sigma = series.std(ddof=ddof)
    if sigma == 0:
        return pd.Series(False, index=series.index)
    z = (series - mu) / sigma
    return z.abs() > threshold


def winsorize_series(series, lower=0.05, upper=0.95):
    """Clip values outside the ``[lower, upper]`` quantile range.

    Values below the ``lower`` quantile are raised to it and values above the
    ``upper`` quantile are lowered to it, capping extremes without deleting rows.
    """
    series = _validate_series(series)
    if not (isinstance(lower, (int, float)) and isinstance(upper, (int, float))
            and 0 <= lower < upper <= 1):
        raise ValueError("lower and upper must satisfy 0 <= lower < upper <= 1")
    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)
