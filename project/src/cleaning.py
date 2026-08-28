"""Reusable data-cleaning functions.

- ``drop_missing`` removes columns whose missing fraction exceeds a threshold.
- ``fill_missing_median`` imputes missing numeric values with the column median.
- ``normalize_data`` applies min-max scaling to selected numeric columns.
"""

import pandas as pd


def drop_missing(df, threshold=0.5):
    """Drop columns whose share of missing values exceeds ``threshold``.

    Parameters
    ----------
    df : pandas.DataFrame
    threshold : float, default 0.5

    Returns
    -------
    pandas.DataFrame
        A copy with high-missingness columns removed.
    """
    result = df.copy()
    missing_ratio = result.isna().mean()
    to_drop = missing_ratio[missing_ratio > threshold].index
    return result.drop(columns=to_drop)


def fill_missing_median(df, columns=None):
    """Fill missing values in numeric columns with the column median.

    Median imputation is used because it is less sensitive to extreme values than the
    mean — the dataset contains outliers, which is exactly when the median wins.

    Parameters
    ----------
    df : pandas.DataFrame
    columns : list, optional
        Numeric columns to fill. If None, all numeric columns are used.

    Returns
    -------
    pandas.DataFrame
        A copy with missing numeric values filled.
    """
    result = df.copy()
    if columns is None:
        columns = result.select_dtypes(include="number").columns
    for col in columns:
        result[col] = result[col].fillna(result[col].median())
    return result


def normalize_data(df, columns=None):
    """Min-max scale numeric columns to [0, 1].

    Parameters
    ----------
    df : pandas.DataFrame
    columns : list, optional
        Numeric columns to normalize. If None, all numeric columns are used.

    Returns
    -------
    pandas.DataFrame
        A copy with the selected columns scaled to [0, 1].
    """
    result = df.copy()
    if columns is None:
        columns = result.select_dtypes(include="number").columns
    for col in columns:
        lo = result[col].min()
        hi = result[col].max()
        if hi != lo:
            result[col] = (result[col] - lo) / (hi - lo)
    return result
