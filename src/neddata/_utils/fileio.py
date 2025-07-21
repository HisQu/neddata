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
