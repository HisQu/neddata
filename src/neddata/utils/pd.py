"""Utility functions for everything related to pandas."""

# %%
import re
from io import StringIO
import pandas as pd
from contextlib import contextmanager
from warnings import warn

from IPython.display import display
from tabulate import tabulate

from typing import Sequence, Mapping, Callable, Iterable, Optional

# from neddata.utils.stdlib import infer_caller


# %%
# =====================================================================
# === Internal Helpers
# =====================================================================


def _check_columns(
    user_columns: Sequence[str] | Mapping[str, object],
    target_columns: Optional[Sequence[str]] = None,
    df: Optional[pd.DataFrame] = None,
) -> None:
    """Check if the columns are in the DataFrame

    :param user_columns: columns to check, can be a list or a dict-like object.
    :param target_columns: columns in the DataFrame. This overrides the df, if both are provided.
    :param df: DataFrame to check against.
    :raises KeyError: if any of the user_columns are not in the target_columns.
    :raises TypeError: if user_columns or target_columns are not hashable.
    """
    ### Assert target_columns is provided, fall back to df if not
    assert (
        df is not None or target_columns is not None
    ), "Either 'df' or 'target_columns' must be provided."
    if target_columns is None:
        if df is None:
            raise ValueError(
                "Either 'df' or 'target_columns' must be provided."
            )
        target_columns = df.columns.tolist()
    ### Check Columns:
    try:
        missing = set(user_columns) - set(target_columns)
    except TypeError as e:
        raise TypeError(
            f"All elements in 'user_columns' and 'target_columns' must be hashable, but got {type(user_columns)} and {type(target_columns)}."
        ) from e
    if missing:
        raise KeyError(
            f"Columns {missing} not found in DataFrame. Available columns are: \n {target_columns}"
        )


if __name__ == "__main__":
    df = pd.DataFrame({"A": [1, 2], "B": [3, 4]})
    # > Should pass without error
    _check_columns(["A", "B"], target_columns=["A", "B", "C"])
    _check_columns(["A", "B"], df=df)
    # %%
    # > Should raise
    try:
        _check_columns(["A", "C"], df=df)
    except KeyError as e:
        print(e)  # < Should raise KeyError for missing column 'C'
    try:
        _check_columns(["A", "B"], target_columns=["C", "D"])
    except KeyError as e:
        print(e)
    try:
        _check_columns(["A", "B"], target_columns=["C", "D"], df=df)
    except KeyError as e:
        print("target_column correctly overrides df:", e)
    try:
        _check_columns(["A", "B"])
    except AssertionError as e:
        print(e)


# %%
# =====================================================================
# === Public Helpers
# =====================================================================


def drop_columns(
    df: pd.DataFrame,
    columns: Sequence[str],
) -> pd.DataFrame:
    """A wrapper with improved error message"""
    _check_columns(columns, df=df)
    return df.drop(columns, axis=1)


# %%


def _nan_summary_table(
    increased: pd.Series,
    new_nan_mask: pd.DataFrame,
    df: pd.DataFrame,
    max_rows=10,
    show_all=False,
) -> str:
    ### Get Indices of newly NaN rows
    table_rows = []
    for col, n_new in increased.items():
        if show_all:
            idxs = df.index[new_nan_mask[col]].tolist()
        else:
            idxs_full = df.index[new_nan_mask[col]].tolist()
            if len(idxs_full) <= max_rows:
                idxs = idxs_full
            else:
                head = idxs_full[:max_rows]
                idxs = head + [
                    "... ({} more)".format(len(idxs_full) - max_rows)
                ]
        table_rows.append((col, n_new, idxs))
    ### Produce nicer table; flatten indices to string
    tab_data = [
        [
            col,
            n_new,
            (", ".join(map(str, idxs)) if isinstance(idxs, list) else idxs),
        ]
        for col, n_new, idxs in table_rows
    ]
    table_str = tabulate(
        tab_data,
        headers=["Column", "+NaNs", "Row indices newly NaN"],
        tablefmt="github",
        colalign=("left", "right", "left"),
    )
    return table_str


@contextmanager
def warn_if_nan_increases(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    label: Optional[str] = "",
    *,
    max_rows: int = 10,  # < how many indices to show per column before truncating
    show_all: bool = False,
    warn_category=UserWarning,
    stacklevel: int = 4,
):
    """
    Warn when NaN count rises inside the `with` block and show row indices
    where fresh NaNs appeared.

    :param df: DataFrame to monitor.
    :param columns: Columns to monitor; None -> all columns.
    :param label: Extra label text for the warning message.
    :param max_rows: Maximum number of row indices to display per column in the warning.
        Ignored if show_all=True.
    :param show_all: If True, display *all* row indices for each column (careful with big data).
    :param warn_category: Warning category passed to `warnings.warn`.
    :param stacklevel: Forwarded to `warnings.warn` to help point at user code.
    :return: Yields control to the block, then checks for NaN increases.
    """
    cols = list(columns) if columns is not None else df.columns.tolist()
    _check_columns(cols, df=df)
    ### Snapshot missingness mask before.
    before_mask = df[cols].isna()
    try:
        yield
    finally:
        after_mask = df[cols].isna()
        ### Rows that changed from non-missing -> missing
        new_nan_mask: pd.DataFrame = (~before_mask) & after_mask
        ### Count per column
        new_counts: pd.Series = new_nan_mask.sum(axis=0)
        increased: pd.Series = new_counts[new_counts > 0]
        if not increased.empty:
            ### Build rows for tabular display
            table_str = _nan_summary_table(
                increased=increased,
                new_nan_mask=new_nan_mask,
                df=df,
                max_rows=max_rows,
                show_all=show_all,
            )
            msg = f"\n⚠️  NaN-count increased by {increased.sum()}!{(' ' + label) if label else ''}\n{table_str}"
            warn(msg, category=warn_category, stacklevel=stacklevel)


if __name__ == "__main__":
    df = pd.DataFrame(
        {"Aaa": [1, 2, "hä"], "B": ["was?", 4, 5], "C": [6, "ui", "uff"]}
    )
    print("Before context manager:")
    display(df)
    with warn_if_nan_increases(df, columns=["Aaa", "B"]):
        df.loc[0, "Aaa"] = None  # < This will trigger the warning
        df.loc[1, "Aaa"] = None  # < This will trigger the warning
    print("After context manager:")
    display(df)

    # %%
    with warn_if_nan_increases(df):
        df.loc[0, "C"] = None  # < This will also trigger the warning


# %%
# =====================================================================
# === Type Converters
# =====================================================================
_num_chars_re = re.compile(r"[^0-9,.\-+]")  # remove everything else


def _clean_coord_value(val: object) -> str | None:
    """Normalize a coordinate-ish string to a float-friendly string or None."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    if not s:
        return None
    # > remove any stray chars (currency symbols etc.)
    s = _num_chars_re.sub("", s)
    # > normalize decimal comma -> dot
    s = s.replace(",", ".")
    # > if more than one dot, assume *thousands* separators after first dot:
    # > keep the first dot, drop all subsequent.
    if s.count(".") > 1:
        first = s.find(".")
        s = s[: first + 1] + s[first + 1 :].replace(".", "")
    return s or None


def _to_float_or_nan(s: str | None) -> float:
    if s is None:
        return float("nan")
    try:
        return float(s)
    except ValueError:
        return float("nan")


def _clean_coord_series(ser: pd.Series) -> pd.Series:
    return ser.map(_clean_coord_value).map(_to_float_or_nan)


def lon_lat_to_numeric(
    df: pd.DataFrame, columns: Sequence[str] = ["Lon", "Lat"]
) -> pd.DataFrame:
    """Convert columns with weird number strings like "5.175.792" to numeric."""
    with warn_if_nan_increases(df, columns=columns, stacklevel=4):
        for c in columns:
            cleaned = _clean_coord_series(df[c])
            df[c] = cleaned
    return df


if __name__ == "__main__":
    data = StringIO(
        "Lon;Lat\n"
        "12.34;56.78\n"
        "invalid;90.12\n"
        "34.56;invalid\n"
        "11.385.517.768.465.600;5.175.792.668.808.910\n"
        "NaN;NaN\n"
    )
    df: pd.DataFrame = pd.read_csv(data, sep=";")
    print("Before conversion:")
    display(df)
    print(df.info())
    # %%
    df = lon_lat_to_numeric(df, columns=["Lon", "Lat"])
    print("After conversion:")
    display(df)
    print(df.info())


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
