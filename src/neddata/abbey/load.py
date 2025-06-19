"""Loads datasets"""

# %%

from __future__ import annotations
from dataclasses import dataclass
from importlib.resources import files, as_file
from importlib.resources.abc import Traversable
from pathlib import Path
import fnmatch
from difflib import get_close_matches

from typing import (
    Callable,
    Dict,
    Iterable,
    cast,
    Any,
    Iterator,
    Mapping,
    Sequence,
)

import neddata.utils as u

# ---------------------------------------------------------------------
# 1. Data-model
# ---------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class DataFile:
    path: Path
    loader: Callable[[Path], Any] | None = None

    @property
    def stem(self) -> str:
        return self.path.stem

    def load(self) -> Any:
        if not self.loader:
            raise ValueError(f"No loader for {self.stem}")
        return self.loader(self.path)


@dataclass(frozen=True, slots=True)
class DataDir:
    path: Path

    def list(self) -> list[str]:
        return [p.name for p in self.path.iterdir() if p.is_file()]


type Resource = DataFile | DataDir  # public alias


class Catalogue(Mapping[str, Resource]):
    """Auto-discovers files & 'directory datasets' beneath *package_root*."""

    FILE_PATTERNS = ("*.csv", "*.xlsx", "*.json", "*.txt", "*.npy", "*.pickle")
    IGNORE_PATTERNS = (".git", "__pycache__")

    def __init__(
        self, package: str, dir_patterns: Sequence[str] = ("*RAGI*",)
    ) -> None:
        root_t: Traversable = files(package)  # Traversable ✔
        with as_file(root_t) as root:  # zip-safe path
            self.dir_patterns = dir_patterns
            self._root: Path = root
            self._data: Dict[str, Resource] = {}
            self._build()

    # ---------- Mapping API ----------
    def _suggest(
        self, bad_key: str, n: int = 1, cutoff: float = 0.6
    ) -> list[str]:
        return get_close_matches(
            bad_key,
            self._data.keys(),  # possibilities
            n=n,
            cutoff=cutoff,  # 0.0 = very lenient, 1.0 = exact
        )

    def __getitem__(self, key: str) -> Resource:
        try:
            return self._data[key.lower()]
        except KeyError as exc:
            suggestions = self._suggest(key)
            hint = ", ".join(suggestions) if suggestions else "no close matches"
            raise KeyError(
                f"Resource '{key}' not found; Did you mean: '{hint}'?"
            ) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    # ---------- public helpers ----------
    def items(self) -> Iterable[tuple[str, Resource]]:
        return self._data.items()

    def keys(self) -> list[str]:
        """List all resource keys in the catalogue."""
        return list(self._data.keys())

    def get(self, key: str, default: Any = None) -> Resource | Any:
        return self._data.get(key, default)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}\n len={len(self)}\n root='{self._root}'\n dir_patterns={self.dir_patterns}>"

    def __str__(self) -> str:
        lines = []
        for key, res in self._data.items():
            kind = "Dir" if isinstance(res, DataDir) else f"{res.path.suffix}"
            lines.append(f"({kind}) {key}:\n  {res.path}")
            if isinstance(res, DataFile):
                lines.append(
                    f"  Loader: {res.loader.__name__ if res.loader else 'None'}"
                )
        return "\n".join(lines)

    # ---------- internals ----------
    def _match_any(self, name: str, globs: Iterable[str]) -> bool:
        return any(fnmatch.fnmatchcase(name, g) for g in globs)  # wildcards ✔

    def _has_dir_ancestor(self, path: Path) -> bool:
        return any(
            self._match_any(parent.name, self.dir_patterns)
            for parent in path.parents
        )

    def _build(self) -> None:
        for p in self._root.rglob("*"):  # walks files+dirs
            # > generic ignore (any part)
            if any(
                self._match_any(part, self.IGNORE_PATTERNS) for part in p.parts
            ):
                continue
            # > declare directory-dataset once
            if p.is_dir() and self._match_any(p.name, self.dir_patterns):
                key = f"{p.relative_to(self._root).as_posix()}/"
                key = key.lower()  # < make keys case-insensitive
                self._data[key] = DataDir(p)
                continue
            # > skip everything nested inside a directory-dataset
            if self._has_dir_ancestor(p):
                continue
            # > ordinary file
            if p.is_file() and self._match_any(p.name, self.FILE_PATTERNS):
                key = p.relative_to(self._root).with_suffix("").as_posix()
                key = key.lower()
                loader = lookup_registry(key) or u.fileio.get_default_loader(p)
                self._data[key] = DataFile(p, loader=loader)


if __name__ == "__main__":
    from pprint import pprint

    print(_REGISTRY)
    # create a catalogue
    cat = Catalogue("neddata.abbey")

    # %%
    # print the catalogue keys
    pprint(cat.keys())

    # %%
    cat["Regests/2_Ben-Cist_Identifizierungen"]

    # %%
    # !! Typo lower case
    cat["Regests/2_ben-Cist_Identifizierungen"]

    # %%
    # !! Big
    cat["Regests/3Cis-ben"]

    # %%
    # pretty-print the catalogue
    print(cat)

    # %%
    print(cat.__repr__())

# %%

# =====================================================================
# === For Developers: Register loaders
# =====================================================================

_REGISTRY: Dict[str, Callable[[Path], Any]] = {}


def register(
    key_or_glob: str,
) -> Callable[[Callable[[Path], Any]], Callable[[Path], Any]]:
    """
    Decorator that registers *func* as the loader for *key_or_glob*.

    >>> @register("Regests/2_Ben_Cist_Identifizierungen")
    ... def read_ben_cist(path: Path) -> pd.DataFrame: ...
    """

    def decorator(func: Callable[[Path], Any]):
        _REGISTRY[key_or_glob] = func
        return func

    return decorator


def lookup_registry(key: str) -> Callable[[Path], Any] | None:
    """Return the first loader whose pattern matches *key* (exact or glob)."""
    for pattern, loader in _REGISTRY.items():
        if fnmatch.fnmatchcase(key, pattern):  # shell-style wildcards
            return loader
    return None


# %%

import pandas as pd


@register("Regests/2_Ben-Cist_Identifizierungen")  # exact key
def read_ben_cist(path: Path) -> pd.DataFrame:
    """Import CSV file that ignores the separator in the last column."""
    # 1) Read the whole file as plain text, one Python string per line
    with open(path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    # 2) Split each line at the first 6 semicolons only
    rows = [line.split(";", 6) for line in lines]
    columns = rows[0]  # < first line is the header
    rows = rows[1:]  # < remove header from data

    # 3) Build the DataFrame and name your columns
    df = pd.DataFrame(rows, columns=columns).drop_duplicates()

    return df


if __name__ == "__main__":
    from IPython.display import display

    print(cat["Regests/2_Ben-Cist_Identifizierungen"].path)

    #  %%
    df = read_ben_cist(cat["Regests/2_Ben-Cist_Identifizierungen"].path)
    display(df)

    # %%
    ### Load from the catalogue
    # from neddata import abbey
    cat["Regests/2_Ben-Cist_Identifizierungen"].load()
