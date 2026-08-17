def get_summary_stats(df):
    """
    Return descriptive statistics for numeric columns.
    """
    return df.describe()


def get_grouped_summary(df):
    """
    Aggregate value statistics by category.
    """
    return (
        df.groupby("category")["value"]
        .agg(["count", "mean", "sum", "min", "max"])
        .reset_index()
    )