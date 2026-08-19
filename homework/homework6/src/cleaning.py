import pandas as pd


def fill_missing_median(df, columns=None):
    """
    Fill missing values in numeric columns with the column median.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    columns : list, optional
        Numeric columns to fill. If None, all numeric columns are used.

    Returns
    -------
    pandas.DataFrame
        A copy of the DataFrame with missing numeric values filled.
    """
    result = df.copy()

    if columns is None:
        columns = result.select_dtypes(include="number").columns

    for col in columns:
        result[col] = result[col].fillna(result[col].median())

    return result


def drop_missing(df, threshold=0.5):
    result = df.copy()

    missing_ratio = result.isna().mean()
    columns_to_drop = missing_ratio[missing_ratio > threshold].index

    return result.drop(columns=columns_to_drop)


def normalize_data(df, columns=None):
    """
    Normalize numeric columns to the range [0, 1] using min-max scaling.

    Parameters
    ----------
    df : pandas.DataFrame
        Input DataFrame.
    columns : list, optional
        Numeric columns to normalize. If None, all numeric columns are used.

    Returns
    -------
    pandas.DataFrame
        A copy of the DataFrame with normalized numeric columns.
    """
    result = df.copy()

    if columns is None:
        columns = result.select_dtypes(include="number").columns

    for col in columns:
        min_value = result[col].min()
        max_value = result[col].max()

        if max_value != min_value:
            result[col] = (
                result[col] - min_value
            ) / (
                max_value - min_value
            )

    return result