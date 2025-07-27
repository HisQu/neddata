import json
from pathlib import Path

import numpy as np
import pandas as pd

from typing import Callable, Any, Optional


# =====================================================================
# === Default Loaders
# =====================================================================


def defaultload_json(filep: Path) -> dict:
    """Read a JSON file and return its contents as a dictionary."""
    with open(filep, "r") as f:
        return json.load(f)


def defaultload_text(filep: Path) -> str:
    """Read a text file and return its contents as a string."""
    with open(filep, "r") as f:
        return f.read()


def defaultload_csv(filep: Path) -> pd.DataFrame:
    """Read a CSV file and return its contents as a pandas DataFrame."""
    return pd.read_csv(filep)


def defaultload_tsv(filep: Path) -> pd.DataFrame:
    """Read a TSV file and return its contents as a pandas DataFrame."""
    return pd.read_csv(filep, sep="\t")


def defaultload_excel(filep: Path) -> pd.DataFrame:
    """Read an Excel file and return its contents as a pandas DataFrame."""
    return pd.read_excel(filep)


def defaultload_npy(filep: Path) -> np.ndarray:
    """Read a NumPy file and return its contents as a NumPy array."""
    return np.load(filep)


DEFAULT_LOADERS: dict[str, Callable[[Path], Any]] = {
    "json": defaultload_json,
    "txt": defaultload_text,
    "csv": defaultload_csv,
    "tsv": defaultload_tsv,
    "xlsx": defaultload_excel,
    "npy": defaultload_npy,
}


def get_default_loader(filep: Path) -> Callable[[Path], Any] | None:
    """Return the default loader function for a given file type."""
    ext = filep.suffix[1:]
    return DEFAULT_LOADERS.get(ext)


# =====================================================================
# === Special Loaders
# =====================================================================


def load_json_records(filep: Path | str) -> pd.DataFrame:
    """Load a DataFrame from a JSON records file."""
    df = pd.read_json(
        Path(filep),
        orient="records",
        lines=False,
        encoding="utf-8",
    )
    return df


# =====================================================================
# === Save
# =====================================================================


def save_json_records(df: pd.DataFrame, filep: Path | str) -> None:
    """Save a DataFrame as a JSON file with records format."""
    df.to_json(
        Path(filep).with_suffix(".json"),
        index=False,
        orient="records",
        indent=2,
        force_ascii=False,
    )


# =====================================================================
# === Checkers
# =====================================================================
WEIRD_CHARS = ["&w&w", "&w&", "&w", "&y"]


import re
import pandas as pd
from typing import Iterable, Sequence, Optional

WEIRD_CHARS: Sequence[str] = ["&w&w", "&w&", "&w", "&y"]


def find_weird_tokens(
    df: pd.DataFrame,
    weird_tokens: Optional[Iterable[str]] = None,
    columns: Optional[Sequence[str]] = None,
    case: bool = True,
) -> pd.DataFrame | None:
    """
    Return a DataFrame listing every cell that contains one of *weird_tokens*.

    Columns of the result:
    ┌ row  – original row label
    ├ column – column name
    ├ weird_token – the first matching token
    └ value – the full original cell value
    """
    tokens = list(weird_tokens or WEIRD_CHARS)
    # Build a single alternation pattern, escaping any regex meta-chars
    pattern = re.compile(
        "|".join(map(re.escape, tokens)), flags=0 if case else re.I
    )

    # If not provided, scan every column that has string-compatible dtype
    if columns is None:
        columns = df.select_dtypes(include=["object", "string"]).columns

    # 1️⃣ Boolean mask of matches (DataFrame shape identical to *columns*)
    mask: pd.DataFrame = df[columns].apply(
        lambda s: s.astype("string").str.contains(pattern, na=False, regex=True)
    )  
    if not mask.any().any():  # short-circuit when nothing found
        return None

    # 2️⃣ Reshape to long format: each True becomes one row
    hits = (
        mask.stack()  # MultiIndex (row-label, column-name) → bool
        .loc[lambda x: x]  # keep only True values
        .reset_index()
        .rename(columns={"level_0": "row", "level_1": "column"})
    )  # stack is faster than nested Python loops
    # 3️⃣ Capture which token triggered the hit (vectorised extract)
    long_vals = df.reindex(columns=columns).stack()  # align with hits
    hits["value"] = long_vals.loc[mask.stack()].values
    hits["weird_token"] = hits["value"].str.extract(
        f"({'|'.join(map(re.escape, tokens))})", expand=False
    )  # str.extract returns the matching group
    
    # if not hits.empty:
    #     print(f"Found {len(hits)} hits in {len(df)} rows and {len(columns)} columns.")
    # else:
    #     print("No weird tokens found in the DataFrame.")
    return hits
