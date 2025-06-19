import json
from pathlib import Path

import numpy as np
import pandas as pd

from typing import Callable, Any, Optional


def read_json(file_path: Path) -> dict:
    """Read a JSON file and return its contents as a dictionary."""
    with open(file_path, "r") as f:
        return json.load(f)


def read_text(file_path: Path) -> str:
    """Read a text file and return its contents as a string."""
    with open(file_path, "r") as f:
        return f.read()


def read_csv(file_path: Path) -> pd.DataFrame:
    """Read a CSV file and return its contents as a pandas DataFrame."""
    return pd.read_csv(file_path)


def read_excel(file_path: Path) -> pd.DataFrame:
    """Read an Excel file and return its contents as a pandas DataFrame."""
    return pd.read_excel(file_path)


def read_npy(file_path: Path) -> np.ndarray:
    """Read a NumPy file and return its contents as a NumPy array."""
    return np.load(file_path)


DEFAULT_LOADERS: dict[str, Callable[[Path], Any]] = {
    "json": read_json,
    "txt": read_text,
    "csv": read_csv,
    "xlsx": read_excel,
    "npy": read_npy,
}


def get_default_loader(file_path: Path) -> Callable[[Path], Any] | None:
    """Return the default loader function for a given file type."""
    ext = file_path.suffix[1:]
    return DEFAULT_LOADERS.get(ext)
