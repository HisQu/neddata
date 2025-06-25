"""Loads datasets"""

# %%

from __future__ import annotations
from dataclasses import dataclass
from importlib.resources import files, as_file, path
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


# =====================================================================
# === Data-model
# =====================================================================

"""
Terminology:
- database: = The Git-Repository, 1 pyproject.toml (Project root)
- dataset: A directory inside ./src/<my_project>)
- catalog.py: A python module inside each dataset, creating the Catalog instance
- Catalog: An instance assigning keys to resources + other utilities (file loaders, etc.)
- Resource: A DataFile or DataDir.
    - DataFile: Catalogued Files (csv, json, etc.)
    - DataDir: Catalogued Directories, but files within are NOT catalogued.


example tree structure:
```
./database-name (<my_project>)
├── src
│   └── <database-name> (<my_project>) # = Project name (src layout PEP 517)
│       ├── __init__.py
│       ├── env.py
│       ├── datamodel.py
│       ├── <dataset-1>
│       │   ├── __init__.py
│       │   ├── catalog.py
│       │   ├── Subset-folder_a
│       │   │   ├── <DataFile>.csv  
│       │   │   └── <DataFile>.json
│       │   ├── Subset-folder_b
│       │   │   ├── <DataFile>.txt
│       │   │   └── <DataFile>.json
│       │   ├── <DataDir>
│       │   │   ├── some_uncatalogued_file.npy
│       │   │   ├── some_uncatalogued_file.json
│       │   │   └── some_uncatalogued_file.zip
│       ├── <dataset-2>
│       │   ├── __init__.py
│       │   ├── catalog.py
│       │   ├── Subset-folder_a
│       │   │   ├── <DataFile>.csv
│       │   │   └── <DataFile>.json
```
"""
### ./src/<my_project>/<dataset>


# =====================================================================
# === Resources (DataFile | DataDir)
# =====================================================================


@dataclass(frozen=True, slots=True)
class DataFile:
    path: Path
    loader: Callable[[Path], Any] | None = None

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def name(self) -> str:
        return self.path.name

    def load(self) -> Any:
        if not self.loader:
            raise ValueError(f"No loader for {self.stem}")
        try:
            return self.loader(self.path)
        except Exception as e:
            raise ValueError(
                f"Failed to load '{self.name}' with loader '{self.loader.__name__ if self.loader else 'unknown loader'}'"
            ) from e


@dataclass(frozen=True, slots=True)
class DataDir:
    path: Path

    def list(self) -> list[str]:
        return [p.name for p in self.path.iterdir() if p.is_file()]


type Resource = DataFile | DataDir


# =====================================================================
# === Catalogue
# =====================================================================


class Catalog(Mapping[str, Resource]):
    """Auto-discovers files & 'directory datasets' beneath *package_root*."""

    FILE_PATTERNS = ("*.csv", "*.xlsx", "*.json", "*.txt", "*.npy", "*.pickle")
    IGNORE_PATTERNS = (
        ".git",
        "__pycache__",
        ".DS_Store",
        "Thumbs.db",
        "~$*",
        ".old",
        "*.IGNORE*",
    )

    def __init__(
        self, package: str, dir_patterns: Sequence[str] = ("*RAGI*",)
    ) -> None:
        self.package = package
        self.dir_patterns = dir_patterns

        _root: Traversable = files(package)  # < Traversable ✔
        with as_file(_root) as r:  # < zip-safe path
            self._root: Path = r
            self._data: Dict[str, Resource] = {}
            self._loaders: Dict[str, Callable[[Path], Any]] = {}
            self._build()

    # =================================================================
    # === Public Helpers
    # =================================================================

    def load(self, key: str) -> Any | Path:
        """
        Load a resource by its key. If the resource is a DataFile, it will
        be loaded using its loader function.
        """
        resource = self[key]
        if isinstance(resource, DataFile):
            return resource.load()
        elif isinstance(resource, DataDir):
            return resource.path
        else:
            raise TypeError(f"Unknown resource type: {type(resource)}")

    def items(self) -> Iterable[tuple[str, Resource]]:
        return self._data.items()

    def keys(self) -> list[str]:
        """List all resource keys in the catalogue."""
        return sorted(self._data.keys())

    def get(self, key: str, default: Any = None) -> Resource | Any:
        key = self._format_key(key)
        return self._data.get(key, default)

    # =================================================================
    # === Representation
    # =================================================================

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}(package='{self.package}', dir_patterns={self.dir_patterns})>\n"
            f"  root='{self._root}'\n"
            f"  len={len(self)}\n"
            f"  keys=\n   - {"\n   - ".join(self.keys())}\n"
        )

    def __str__(self) -> str:
        lines = []
        for key, res in self._data.items():
            kind = "Dir" if isinstance(res, DataDir) else f"{res.path.suffix}"
            lines.append(f"({kind}) {key}:\n  Path:\t{res.path}")
            if isinstance(res, DataFile):
                lines.append(
                    f"  Loader:\t{res.loader.__name__ if res.loader else 'None'}"
                )
            lines.append("\n")
        return "\n".join(lines)

    # =================================================================
    # === Mapping API
    # =================================================================

    @staticmethod
    def _format_key(key: str) -> str:
        """Format the key to simplify it:
        - Lowercase the key to make it case-insensitive.
        - Remove leading/trailing whitespace.
        - Replace whitespace, dashes, and underscores with underscores.
        """
        return key.lower().strip().replace(" ", "_").replace("-", "_")

    def __getitem__(self, key: str) -> Resource:
        """Catalogue[key] -> Resource"""
        key = self._format_key(key)
        try:
            resource = self._data[key]
        except:
            self._raise_key_error(bad_key=key)
        return resource

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def _suggest(
        self, bad_key: str, n: int = 2, cutoff: float = 0.6
    ) -> list[str]:
        return get_close_matches(
            bad_key,
            self._data.keys(),  # possibilities
            n=n,
            cutoff=cutoff,  # 0.0 = very lenient, 1.0 = exact
        )

    def _raise_key_error(self, bad_key: str) -> None:
        """Raise a KeyError with a custom message."""
        suggestions = self._suggest(bad_key)
        hint = ", ".join(suggestions) if suggestions else "no close matches"
        raise KeyError(
            f"Resource '{bad_key}' not found; Did you mean: '{hint}'?"
        )

    # =================================================================
    # === Set Custom Loaders
    # =================================================================

    def set_loader(
        self, pattern: str
    ) -> Callable[[Callable[[Path], Any]], Callable[[Path], Any]]:
        """
        Decorator: register a custom *loader* for every key that matches *pattern*
        (shell-style glob, case-insensitive). Raises KeyError if no key matches.
        """

        def decorator(
            func: Callable[[Path], Any], pattern: str = pattern
        ) -> Callable[[Path], Any]:
            matched = False
            for key, res in self._data.items():
                key = self._format_key(key)
                pattern = self._format_key(pattern)
                if fnmatch.fnmatchcase(key, pattern):
                    if isinstance(res, DataFile):
                        # > Replace loader immediately
                        self._data[key] = DataFile(res.path, loader=func)
                        matched = True
            if not matched:
                self._raise_key_error(bad_key=key)

            self._loaders[pattern] = (
                func  # keep for lookup() if you still need it
            )
            return func

        return decorator

    def _lookup_loaders(self, key: str) -> Callable[[Path], Any] | None:
        """Return the first loader whose pattern matches *key* (exact or
        glob)."""
        key = self._format_key(key)
        for pattern, loader in self._loaders.items():
            if fnmatch.fnmatchcase(key, pattern):  # shell-style wildcards
                return loader
        return None

    # =================================================================
    # === Build
    # =================================================================

    def _match_any(self, name: str, globs: Iterable[str]) -> bool:
        return any(fnmatch.fnmatchcase(name, g) for g in globs)  # wildcards ✔

    def _has_dir_ancestor(self, path: Path) -> bool:
        return any(
            self._match_any(parent.name, self.dir_patterns)
            for parent in path.parents
        )

    def _build(self) -> None:
        for p in self._root.rglob("*"):  # walks files+dirs
            key = p.relative_to(self._root).as_posix()
            key = self._format_key(key)
            # > Generic ignore (any part)
            _ignored: bool = any(
                self._match_any(part, self.IGNORE_PATTERNS) for part in p.parts
            )
            if _ignored:
                continue
            elif p.is_dir() and self._match_any(p.name, self.dir_patterns):
                self._data[key + "/"] = DataDir(p)
            elif self._has_dir_ancestor(p):
                continue  # > Skip everything nested inside a DataDir
            elif p.is_file() and self._match_any(p.name, self.FILE_PATTERNS):
                loader = self._lookup_loaders(
                    key
                ) or u.fileio.get_default_loader(p)
                self._data[key] = DataFile(p, loader=loader)


if __name__ == "__main__":
    from pprint import pprint

    # print(_REGISTRY)
    # create a catalogue
    cat = Catalog("neddata.abbey")

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
    cat["Regests/2"]

    # %%
    # pretty-print the catalogue
    print(cat)

    # %%
    print(cat.__repr__())
