"""Reusable outlier detection and handling functions for Homework 07.

This module wraps three common, distribution-based outlier rules so they can be
reused across columns and experiments:

- ``detect_outliers_iqr``     -> IQR / Tukey's-fences rule (robust to skew)
- ``detect_outliers_zscore``  -> Z-score rule (assumes a roughly normal shape)
- ``winsorize_series``        -> clip extreme values at quantile boundaries

Every function returns a *new* object and never mutates its input, so the calls
can be chained safely. NaN handling is documented on each function: missing
values were the subject of Stage 06, so these functions deliberately leave NaN
in place and do not flag it as an outlier.
"""

import pandas as pd


def _validate_series(series):
    """Return a copy of ``series`` after checking it is a non-empty numeric Series.

    Raises
    ------
    TypeError
        If ``series`` is not a pandas Series.
    ValueError
        If ``series`` is empty or not numeric.
    """
    if not isinstance(series, pd.Series):
        raise TypeError("series must be a pandas.Series")

    if series.empty:
        raise ValueError("series must not be empty")

    if not pd.api.types.is_numeric_dtype(series.dtype):
        raise ValueError("series must be numeric")

    return series.copy()


def detect_outliers_iqr(series, k=1.5):
    """Return a boolean mask flagging IQR-based (Tukey's-fences) outliers.

    A value is flagged when it falls below ``Q1 - k * IQR`` or above
    ``Q3 + k * IQR``, where ``Q1``/``Q3`` are the 25th/75th percentiles and
    ``IQR = Q3 - Q1``. ``k=1.5`` flags "far out" points (the conventional
    Tukey fence); ``k=3`` flags only "far far out" points.

    Parameters
    ----------
    series : pandas.Series
        Numeric data to test. Must be non-empty and numeric.
    k : float, default 1.5
        Fence multiplier. Must be > 0.

    Returns
    -------
    pandas.Series
        Boolean Series with the same index as ``series``; True marks an outlier.

    Notes
    -----
    NaN values are not flagged as outliers (their comparisons evaluate to
    False) because missingness was handled separately in Stage 06. This rule
    assumes the bulk of the data is reasonably summarized by its quartiles; it
    is robust to skew, but it will flag a fixed fraction of points in any
    heavy-tailed distribution, which can be either a feature or a problem
    depending on the context.
    """
    series = _validate_series(series)

    if not isinstance(k, (int, float)) or k <= 0:
        raise ValueError("k must be a positive number")

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1
    lower = q1 - k * iqr
    upper = q3 + k * iqr

    return (series < lower) | (series > upper)


def detect_outliers_zscore(series, threshold=3.0, ddof=0):
    """Return a boolean mask flagging Z-score outliers where ``|z| > threshold``.

    The Z-score is ``(x - mean) / std``. ``ddof=0`` treats the observed data as
    the full population (the conventional choice for this rule); pass ``ddof=1``
    to use the sample standard deviation, which makes the test slightly more
    conservative.

    Parameters
    ----------
    series : pandas.Series
        Numeric data to test. Must be non-empty and numeric.
    threshold : float, default 3.0
        Minimum absolute Z-score to flag. Must be > 0.
    ddof : int, default 0
        Delta degrees of freedom for the standard deviation (0 = population,
        1 = sample).

    Returns
    -------
    pandas.Series
        Boolean Series with the same index as ``series``; True marks an outlier.

    Notes
    -----
    NaN values are not flagged (``abs(NaN) > threshold`` is False). A constant
    series has zero spread and therefore contains no Z-score outliers, so an
    all-False mask is returned rather than dividing by zero. This rule assumes a
    roughly normal distribution, and it is itself sensitive to the very outliers
    it is trying to find: extreme values inflate both the mean and the standard
    deviation, which can "mask" moderate outliers.
    """
    series = _validate_series(series)

    if not isinstance(threshold, (int, float)) or threshold <= 0:
        raise ValueError("threshold must be a positive number")

    mu = series.mean()
    sigma = series.std(ddof=ddof)

    if sigma == 0:
        # Constant series: no spread, so nothing can be an outlier.
        return pd.Series(False, index=series.index)

    z = (series - mu) / sigma
    return z.abs() > threshold


def winsorize_series(series, lower=0.05, upper=0.95):
    """Clip values outside the ``[lower, upper]`` quantile range.

    Values below the ``lower`` quantile are raised to that quantile and values
    above the ``upper`` quantile are lowered to it. This caps extreme values
    without deleting any observations, which is useful when the outliers are
    believed to be genuine observations rather than errors.

    Parameters
    ----------
    series : pandas.Series
        Numeric data to clip. Must be non-empty and numeric.
    lower : float, default 0.05
        Lower quantile boundary. Must satisfy ``0 <= lower < upper``.
    upper : float, default 0.95
        Upper quantile boundary. Must satisfy ``lower < upper <= 1``.

    Returns
    -------
    pandas.Series
        A copy of ``series`` with extreme values clipped to the quantile bounds.

    Notes
    -----
    NaN values are left in place (``clip`` does not touch them). The default
    ``lower=0.05, upper=0.95`` caps the most extreme 10% of values while
    retaining every row.
    """
    series = _validate_series(series)

    if (
        not isinstance(lower, (int, float))
        or not isinstance(upper, (int, float))
        or not (0 <= lower < upper <= 1)
    ):
        raise ValueError("lower and upper must satisfy 0 <= lower < upper <= 1")

    lo = series.quantile(lower)
    hi = series.quantile(upper)
    return series.clip(lower=lo, upper=hi)
