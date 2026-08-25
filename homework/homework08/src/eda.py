"""Reusable exploratory-data-analysis (EDA) helpers for Homework 08.

This module holds the profiling helper the lecture builds in its section 8, so the
project keeps ONE profiling function instead of pasting copies of it into every
notebook. It also adds a flagger for columns that need attention before feature
engineering.

- ``eda_summary(df)``  -> one-call numeric + categorical profile, missingness, flags
- ``flag_columns(df)`` -> flags high missingness, near-zero variance, or a dominant category
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def flag_columns(df, numeric_cols=None, missing_thresh=0.05, dominant_thresh=0.80):
    """Return a DataFrame of columns that need attention before feature engineering.

    Flags three problems:

    - **high missingness** — the share of missing values exceeds ``missing_thresh``.
    - **near-zero variance** — a numeric column is effectively constant, so it can
      carry no signal for a model.
    - **one category dominating** — a categorical column's top value covers more than
      ``dominant_thresh`` of the rows, so it is nearly useless as a feature.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to check.
    numeric_cols : list, optional
        Numeric columns to consider for the variance check. If None, all numeric columns.
    missing_thresh : float, default 0.05
        Missing fraction above which a column is flagged.
    dominant_thresh : float, default 0.80
        Top-category share above which a categorical column is flagged.

    Returns
    -------
    pandas.DataFrame
        One row per flagged column, with a 'reasons' string describing each problem.
        Empty (zero rows) when nothing trips the thresholds.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    flags = []
    for c in df.columns:
        reasons = []

        miss_frac = df[c].isna().mean()
        if miss_frac > missing_thresh:
            reasons.append("high missingness (%.1f%%)" % (miss_frac * 100))

        if c in numeric_cols:
            n_unique = df[c].nunique(dropna=True)
            std = df[c].std(ddof=0)
            if n_unique <= 1 or std < 1e-12:
                reasons.append("near-zero variance")
        else:
            non_null = df[c].notna().sum()
            if non_null > 0:
                top_share = df[c].value_counts(dropna=True).iloc[0] / non_null
                if top_share > dominant_thresh:
                    reasons.append("one category dominates (%.1f%%)" % (top_share * 100))

        if reasons:
            flags.append({
                "column": c,
                "dtype": str(df[c].dtype),
                "reasons": "; ".join(reasons),
            })

    return pd.DataFrame(flags)


def eda_summary(df, numeric_cols=None, missing_thresh=0.05, dominant_thresh=0.80):
    """Return a dict with quick profiling stats, missingness, and attention flags.

    Parameters
    ----------
    df : pandas.DataFrame
        Data to profile.
    numeric_cols : list, optional
        Numeric columns to profile. If None, all numeric columns are used.
    missing_thresh : float, default 0.05
        Forwarded to :func:`flag_columns`.
    dominant_thresh : float, default 0.80
        Forwarded to :func:`flag_columns`.

    Returns
    -------
    dict
        Keys: 'shape', 'dtypes', 'missing', 'numeric_profile',
        'categorical_profile', 'flags'.
    """
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    out = {}
    out["shape"] = df.shape
    out["dtypes"] = df.dtypes.to_dict()
    out["missing"] = df.isna().sum().to_dict()

    # Numeric profile: describe() plus skew and (excess) kurtosis.
    profile = df[numeric_cols].describe().T
    profile["skew"] = [skew(df[c].dropna()) for c in profile.index]
    profile["kurtosis"] = [kurtosis(df[c].dropna()) for c in profile.index]
    out["numeric_profile"] = profile

    # Categorical profile: one row per non-numeric column, with distinct-count and
    # the share held by its most common value.
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    cat_rows = []
    for c in cat_cols:
        vc = df[c].value_counts(dropna=False)
        top = vc.index[0] if len(vc) else None
        cat_rows.append({
            "column": c,
            "dtype": str(df[c].dtype),
            "n_unique": df[c].nunique(dropna=True),
            "missing": int(df[c].isna().sum()),
            "top_category": top,
            "top_share": float(vc.iloc[0]) / len(df) if len(vc) else np.nan,
        })
    out["categorical_profile"] = pd.DataFrame(cat_rows)

    out["flags"] = flag_columns(
        df,
        numeric_cols=numeric_cols,
        missing_thresh=missing_thresh,
        dominant_thresh=dominant_thresh,
    )
    return out
