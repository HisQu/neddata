"""Loads datasets"""

# %%

from __future__ import annotations
from dataclasses import dataclass, field
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
    pooch: pooch.Pooch = field(repr=False, compare=False)
    loader: Callable[[Path], Any] | None = None

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def name(self) -> str:
        return self.path.name

    def load(self) -> Any:
        if self.loader is None:
            raise ValueError(f"No loader for {self.stem}")

        local = Path(self.pooch.fetch(self.path.as_posix()))

        try:
            return self.loader(local)
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
# === Pooch Registry
# =====================================================================

import os
import sys, pooch, pathlib, textwrap
from pooch import HTTPDownloader


def make_pooch_registry(dir: Path) -> None:

    raw_dir = pathlib.Path(dir).expanduser()
    manifest = raw_dir / "pooch_registry.txt"

    if not manifest.is_file():  # < Create empty .txt
        manifest.touch()

    pooch.make_registry(raw_dir, manifest)

    print(
        textwrap.dedent(
            f"""
    Manifest written to {manifest.relative_to(pathlib.Path.cwd())}
    Contains {sum(1 for _ in manifest.open())} entries.
    You can now upload {raw_dir} to your object store and commit the manifest.
    """
        )
    )


def make_pooch(package: str, base_url: str) -> pooch.Pooch:
    """Create a :class:`pooch.Pooch` for *package* using the shipped registry."""
    poochy = pooch.create(
        path=pooch.os_cache(package),
        base_url=base_url,
        registry=None,  # < will be loaded later
        retry_if_failed=2,
    )
    poochy.load_registry(files(package) / "pooch_registry.txt")
    return poochy


# !! The GitHub repo must be public, otherwise pooch needs authentication.
# def fetch_github_data(poochy: pooch.Pooch) -> Any:
#     """
#     Fetch a file from a server that requires authentication
#     """
#     username = os.environ.get("SOMESITE_USERNAME")
#     password = os.environ.get("SOMESITE_PASSWORD")
#     download_auth = HTTPDownloader(auth=(username, password))
#     return poochy.fetch("some-data.csv", downloader=download_auth)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _format_key(key: str) -> str:
    """Normalise keys so look‑ups are case‑insensitive and whitespace tolerant."""
    return key.lower().strip().replace(" ", "_").replace("-", "_")


def _match_any(name: str, globs: Iterable[str]) -> bool:
    """Return *True* if *name* matches at least one shell‑style glob."""
    return any(fnmatch.fnmatchcase(name, g) for g in globs)


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
        self,
        package: str,
        pooch: pooch.Pooch,
        dir_patterns: Sequence[str] = ("*RAGI*",),
    ) -> None:
        self.package = package
        self._pooch = pooch
        self.dir_patterns = dir_patterns

        ###
        self._root = files(package)
        self._data: Dict[str, Resource] = {}
        self._loaders: Dict[str, Callable[[Path], Any]] = {}

        ### Build
        self._build()

    # =================================================================
    # === Build
    # =================================================================

    # def _has_dir_ancestor(self, path: Path) -> bool:
    #     return any(
    #         _match_any(parent.name, self.dir_patterns)
    #         for parent in path.parents
    #     )

    # def _build(self) -> None:
    #     for p in self._root.rglob("*"):  # walks files+dirs
    #         key = p.relative_to(self._root).as_posix()
    #         key = self._format_key(key)
    #         # > Generic ignore (any part)
    #         _ignored: bool = any(
    #             self._match_any(part, self.IGNORE_PATTERNS) for part in p.parts
    #         )
    #         if _ignored:
    #             continue
    #         elif p.is_dir() and self._match_any(p.name, self.dir_patterns):
    #             self._data[key + "/"] = DataDir(p)
    #         elif self._has_dir_ancestor(p):
    #             continue  # > Skip everything nested inside a DataDir
    #         elif p.is_file() and self._match_any(p.name, self.FILE_PATTERNS):
    #             loader = self._lookup_loaders(
    #                 key
    #             ) or u.fileio.get_default_loader(p)
    #             self._data[key] = DataFile(p, loader=loader)

    def _build(self) -> None:
        """Populate ``self._data`` from *pooch* registry entries."""
        for p in self._pooch.registry.keys():

            if _match_any(p, self.IGNORE_PATTERNS):
                continue

            key = _format_key(p)
            _p = Path(p)

            if _match_any(_p.name, self.dir_patterns):
                self._data[key + "/"] = DataDir(path=_p)
            elif _match_any(_p.name, self.FILE_PATTERNS):
                loader = self._lookup_loaders(
                    key
                ) or u.fileio.get_default_loader(_p)
                self._data[key] = DataFile(_p, self._pooch, loader)

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
                        self._data[key] = DataFile(
                            res.path,
                            pooch=self._pooch,
                            loader=func,
                        )
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


if __name__ == "__main__":
    from pprint import pprint

    # print(_REGISTRY)
    # create a catalogue
    DATASET = "neddata.abbey"  # < Package name of the dataset
    DB_URL = (
        "https://raw.githubusercontent.com/HisQu/neddata/refs/heads/main/src"
    )
    BASE_URL = f"{DB_URL}/{DATASET.replace('.', '/')}"
    poochy = make_pooch(DATASET, BASE_URL)

    cat = Catalog("neddata.abbey", pooch=poochy)

    # %%
    # print the catalogue keys
    pprint(cat.keys())

    # %%
    cat["Regests/2_Ben-Cist_Identifizierungen.csv"]

    # %%
    # !! Typo lower case
    cat["Regests/2_ben-Cist_Identifizierungen.csv"]

    # %%
    # !! Big
    cat["Regests/2"]

    # %%
    # pretty-print the catalogue
    print(cat)

    # %%
    print(cat.__repr__())
