"""Reusable exploratory-data-analysis helper.

- ``eda_summary(df)`` returns a one-call profile: shape, dtypes, missingness,
  a numeric profile (describe + skew + kurtosis), a categorical profile, and a
  list of columns needing attention.
- ``flag_columns(df)`` flags high missingness, near-zero variance, and columns
  where one category dominates.
"""

import numpy as np
import pandas as pd
from scipy.stats import skew, kurtosis


def flag_columns(df, numeric_cols=None, missing_thresh=0.05, dominant_thresh=0.80):
    """Return a DataFrame of columns needing attention before feature engineering."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    flags = []
    for c in df.columns:
        reasons = []
        miss_frac = df[c].isna().mean()
        if miss_frac > missing_thresh:
            reasons.append("high missingness (%.1f%%)" % (miss_frac * 100))
        if c in numeric_cols:
            if df[c].nunique(dropna=True) <= 1 or df[c].std(ddof=0) < 1e-12:
                reasons.append("near-zero variance")
        else:
            non_null = df[c].notna().sum()
            if non_null > 0:
                top_share = df[c].value_counts(dropna=True).iloc[0] / non_null
                if top_share > dominant_thresh:
                    reasons.append("one category dominates (%.1f%%)" % (top_share * 100))
        if reasons:
            flags.append({"column": c, "dtype": str(df[c].dtype),
                          "reasons": "; ".join(reasons)})
    return pd.DataFrame(flags)


def eda_summary(df, numeric_cols=None, missing_thresh=0.05, dominant_thresh=0.80):
    """Return a dict with quick profiling stats, missingness, and attention flags."""
    if numeric_cols is None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    out = {}
    out["shape"] = df.shape
    out["dtypes"] = df.dtypes.to_dict()
    out["missing"] = df.isna().sum().to_dict()

    profile = df[numeric_cols].describe().T
    profile["skew"] = [skew(df[c].dropna()) for c in profile.index]
    profile["kurtosis"] = [kurtosis(df[c].dropna()) for c in profile.index]
    out["numeric_profile"] = profile

    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    cat_rows = []
    for c in cat_cols:
        vc = df[c].value_counts(dropna=False)
        top = vc.index[0] if len(vc) else None
        cat_rows.append({
            "column": c, "dtype": str(df[c].dtype),
            "n_unique": df[c].nunique(dropna=True),
            "missing": int(df[c].isna().sum()),
            "top_category": top,
            "top_share": float(vc.iloc[0]) / len(df) if len(vc) else np.nan,
        })
    out["categorical_profile"] = pd.DataFrame(cat_rows)

    out["flags"] = flag_columns(df, numeric_cols=numeric_cols,
                                missing_thresh=missing_thresh,
                                dominant_thresh=dominant_thresh)
    return out
