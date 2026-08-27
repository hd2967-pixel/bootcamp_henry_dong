"""Reusable feature-engineering helpers for Homework 09.

Each helper adds one engineered feature; ``create_features`` runs them all and returns
the augmented DataFrame. Every function returns a *new* object and never mutates its
input, so the helpers can be used standalone or chained.

- ``add_spend_income_ratio``      -> debt-to-income style ratio
- ``add_income_credit_interaction`` -> earning capacity x creditworthiness
- ``add_high_spender_flag``       -> binary flag for above-median spenders
- ``encode_region_onehot``        -> one-hot encoding of the nominal 'region' column
- ``create_features``             -> run all of the above at once
"""

import pandas as pd


def add_spend_income_ratio(df, income="income", spend="monthly_spend",
                           out="spend_income_ratio"):
    """Return a copy of ``df`` with a spend-to-income ratio column.

    Rationale: captures how much of one's income is consumed each month, a
    debt-to-income analogue. EDA showed that the ratio is more informative about the
    target than either raw component, because it normalizes spending by earning
    capacity instead of leaving the two numbers separate.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with an income column and a monthly spend column.
    income, spend, out : str
        Column names for the inputs and the new ratio column.
    """
    result = df.copy()
    result[out] = result[spend] / result[income]
    return result


def add_income_credit_interaction(df, income="income", credit="credit_score",
                                  out="income_x_credit_score"):
    """Return a copy of ``df`` with an income * credit_score interaction column.

    Rationale: the same income is riskier at a lower credit score, so earning
    capacity and creditworthiness should act *together*. Multiplying them lets a
    linear model capture that joint effect instead of treating the two additively.
    """
    result = df.copy()
    result[out] = result[income] * result[credit]
    return result


def add_high_spender_flag(df, spend="monthly_spend", threshold=None,
                          out="high_spender_flag"):
    """Return a copy of ``df`` with a binary flag for above-median spenders.

    Rationale: a coarse "high burn rate" indicator. The flag trades away the
    continuous information in ``monthly_spend``, which is useful to compare against
    the ratio feature that keeps it.

    Parameters
    ----------
    threshold : float, optional
        Spend cutoff for the flag. Defaults to the column median.
    """
    result = df.copy()
    if threshold is None:
        threshold = result[spend].median()
    result[out] = (result[spend] > threshold).astype(int)
    return result


def encode_region_onehot(df, col="region", prefix="region"):
    """Return a copy of ``df`` with the nominal ``region`` column one-hot encoded.

    One-hot is chosen over label encoding (which would impose a false ordering on
    North/South/East/West) and over frequency encoding (which collapses four
    categories to one number and discards per-category signal). With only four levels
    there is no dimensionality concern, so one dummy column per region is clean.
    """
    return pd.get_dummies(df, columns=[col], prefix=prefix)


def create_features(df):
    """Engineer all Homework 09 features and return the augmented DataFrame.

    Applies, in order: the spend-to-income ratio, the income x credit_score
    interaction, the high-spender flag, and one-hot encoding of ``region``.

    Parameters
    ----------
    df : pandas.DataFrame
        Raw data. Expected columns: ``income``, ``monthly_spend``,
        ``credit_score``, ``region``.

    Returns
    -------
    pandas.DataFrame
        A new DataFrame with the engineered columns added.
    """
    result = add_spend_income_ratio(df)
    result = add_income_credit_interaction(result)
    result = add_high_spender_flag(result)
    result = encode_region_onehot(result)
    return result
