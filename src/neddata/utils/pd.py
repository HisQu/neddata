"""Utility functions for everything related to pandas."""

# %%
from io import StringIO
import pandas as pd

from IPython.display import display

from typing import Sequence, Mapping, Callable


# %%
# =====================================================================
# === Helpers
# =====================================================================


def _check_columns(
    user_columns: Sequence[str] | Mapping[str, object],
    target_columns: Sequence[str],
) -> None:
    """Check if the columns are in the DataFrame"""
    try:
        missing = set(user_columns) - set(target_columns)
    except TypeError as e:
        raise TypeError(
            "All elements in 'user_columns' and 'target_columns' must be hashable."
        ) from e
    if missing:
        raise KeyError(
            f"Columns {missing} not found in DataFrame. Available columns are: \n {target_columns}"
        )


def drop_columns(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """A wrapper with improved error message"""
    _check_columns(columns, df.columns.tolist())
    return df.drop(columns, axis=1)


# %%
# =====================================================================
# === Initialise DataFrames
# =====================================================================


def construct_row_df(
    columns: Sequence[str],
    fills: Mapping[str, object],
    default_missing=pd.NA,
    strict: bool = False,
) -> pd.DataFrame:
    """
    Initialize a one-row DataFrame and fills it with vaules. Useful for loops.

    :param columns: ordered list/tuple of column names that must appear.
    :param fills: dict-like {column_name: value}. Only these columns get values.
    :param default_missing: what to put in the untouched cells (pd.NA by default).
    :param strict: if True, raise if *fills* contains keys not present in *columns*.
    :return: pd.DataFrame with exactly one row.
    """
    if strict:
        _check_columns(fills, columns)

    row = {col: fills.get(col, default_missing) for col in columns}
    return pd.DataFrame([row], columns=list(columns))


if __name__ == "__main__":
    # Test the function
    columns = ["A", "B", "C"]
    fills = {"A": 1, "B": 2}
    df = construct_row_df(columns, fills)
    display(df)


# %%
# =====================================================================
# === Aggregate
# =====================================================================


def implode(
    df: pd.DataFrame,
    groupby_col: str,
    agg_dict: Mapping[str, Callable] | None = None,
    as_index: bool = False,
) -> pd.DataFrame:
    """
    Group by one or more columns and aggregate the rest.

    :param df: DataFrame to group.
    :param groupby_col: column to group by.
    :param agg_dict: dict of {column_name: aggregation_function} to apply.
        If None, will implode all other columns with `", ".join`.
    :param as_index: if True, return a DataFrame with the grouped columns as index.
    :return: grouped DataFrame.
    """
    ### Assert that groupby_col is in the DataFrame
    if groupby_col not in df.columns:
        raise ValueError(f"Invalid columns: {groupby_col}")
    ### All columns except the groupby column(s) will be aggregated
    columns_to_agg = [col for col in df.columns if col != groupby_col]
    ### Assign the aggregation function to each column
    if agg_dict is None:
        agg_dict = {
            col: lambda x: ", ".join(sorted(set(x))) for col in columns_to_agg
        }
    ### Implode
    return df.groupby(groupby_col, as_index=as_index).agg(agg_dict)


if __name__ == "__main__":
    ### Load a sample DataFrame
    from neddata import abbey_catalog

    df: pd.DataFrame = abbey_catalog.load(
        "regests/2_ben_cist_identifizierungen.csv"
    )
    df_imploded = implode(
        df,
        groupby_col="complete_no_tags",
        agg_dict=None,  # Use default aggregation
        as_index=False,  # Keep the groupby column as a regular column
    )
    print(f"Number of regests (before implode): {len(df)}")
    print(f"Number of unique regests: {len(df_imploded)}")
    display(df_imploded)
