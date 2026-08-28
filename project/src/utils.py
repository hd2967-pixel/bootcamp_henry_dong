"""Reusable data-generation and file-I/O utilities.

- ``generate_factor_data`` creates the project's self-contained factor/return dataset.
- ``save_dataframe`` / ``load_dataframe`` write and read CSV or Parquet by suffix.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from src import config


def generate_factor_data(n=250, seed=None):
    """Generate the synthetic factor + asset-return dataset.

    Four style factors (market, size, value, momentum) drive a portfolio's excess
    return via a factor model with a small quadratic momentum term and heteroskedastic
    noise. A few missing values (in ``value``) and two outliers (in ``momentum``) are
    injected so later cleaning / outlier stages have something to do.

    Parameters
    ----------
    n : int, default 250
        Number of business days.
    seed : int, optional
        RNG seed. Defaults to ``config.RANDOM_SEED``.

    Returns
    -------
    pandas.DataFrame
        Columns: date, mkt_excess, size, value, momentum, asset_excess.
    """
    seed = seed if seed is not None else config.RANDOM_SEED
    rng = np.random.default_rng(seed)

    dates = pd.bdate_range("2023-01-03", periods=n)
    mkt = rng.normal(0, 0.011, n)
    size = rng.normal(0, 0.008, n)
    value = rng.normal(0, 0.009, n)
    momentum = rng.normal(0, 0.006, n)

    noise_scale = 0.0035 + 0.5 * np.abs(mkt)          # heteroskedastic noise
    eps = rng.normal(0, noise_scale)
    asset = (
        0.0001 + 0.9 * mkt + 0.25 * size - 0.15 * value
        + 0.35 * momentum + 3.5 * momentum ** 2 + eps
    )

    df = pd.DataFrame({
        "date": dates,
        "mkt_excess": mkt,
        "size": size,
        "value": value,
        "momentum": momentum,
        "asset_excess": asset,
    })

    # Inject 5% missingness in `value` and two outliers in `momentum`.
    missing = rng.choice(np.arange(n), size=int(0.05 * n), replace=False)
    df.loc[missing, "value"] = np.nan
    outliers = rng.choice(np.arange(n), size=2, replace=False)
    df.loc[outliers, "momentum"] += 0.03

    return df


def save_dataframe(df, path):
    """Write a DataFrame as CSV or Parquet, choosing the format by the suffix."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.suffix == ".parquet":
        df.to_parquet(path, index=False)
    elif path.suffix == ".csv":
        df.to_csv(path, index=False)
    else:
        raise ValueError(f"Unsupported format: {path.suffix}")
    return path


def load_dataframe(path):
    """Load a CSV or Parquet file back into a DataFrame."""
    path = Path(path)
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".csv":
        return pd.read_csv(path, parse_dates=["date"])
    raise ValueError(f"Unsupported format: {path.suffix}")
