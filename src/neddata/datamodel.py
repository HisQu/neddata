"""Loads datasets"""

# %%

from __future__ import annotations

from importlib.resources import files, as_file
from importlib.resources.abc import Traversable
from pathlib import Path
import fnmatch
import difflib

import pooch
from rapidfuzz import fuzz

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

import neddata._utils as u
from neddata.datamodel_classes import Resource, DataFile, DataDir

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


FILE_PATTERNS = (
    "*.tsv",
    "*.csv",
    "*.xlsx",
    "*.json",
    "*.txt",
    "*.npy",
    "*.pickle",
)
IGNORE_PATTERNS = (
    ".git",
    "*__pycache__*",
    ".DS_Store",
    "Thumbs.db",
    "~$*",  # < Excel temp files (not working on MacOS)
    ".old",
    "*.IGNORE*",
    "*.py",
    "*.pyc",
    "pooch_registry.txt",  # < The registry itself
)


# %%
# =====================================================================
# === MAIN PUBLIC API
# =====================================================================


def make_catalog(
    dataset: str,
    base_url: str,
    datadir_patterns: list[str],
) -> Catalog:
    """Mages pooch-registry.txt, builds a Pooch, puts pooch into a Catalog."""
    pooch = make_pooch(
        package=dataset,
        base_url=f"{base_url}/{dataset.replace('.', '/')}",
    )
    return Catalog(
        package=dataset,
        dir_patterns=datadir_patterns,
        pooch=pooch,
    )


def make_pooch(package: str, base_url: str) -> pooch.Pooch:
    """Create a :class:`pooch.Pooch` for *package* using the shipped registry."""
    poochy = pooch.create(
        path=pooch.os_cache(package),
        base_url=base_url,
        registry=None,  # < Loaded after creation
        retry_if_failed=2,
    )
    registry_fp: Traversable = files(package) / "pooch_registry.txt"
    with as_file(registry_fp) as path_obj:
        if path_obj.exists():
            # > Load the registry from the package
            poochy.load_registry(registry_fp)
        else:
            # > Write one if it's not there
            write_pooch_registry(package, verbose=False)
    return poochy


def write_pooch_registry(
    dataset: str | Path | Traversable, verbose: bool = True
) -> None:
    """Generate (or overwrite) *pooch_registry.txt* for *dataset*."""
    ### Resolve real on-disk path to package directory & register
    traversable = _cast_traversable(dataset)
    with as_file(traversable) as tmp_path:
        pkg_dir: Path = tmp_path
        _write_registry(pkg_dir, verbose=verbose)


# %%
# =====================================================================
# === Pooch Implementation
# =====================================================================


def _write_registry(
    pkg_dir: Path, verbose: bool = True, cleanup: bool = True
) -> None:
    ### Register
    registry_fp = pkg_dir / "pooch_registry.txt"
    pooch.make_registry(pkg_dir, registry_fp)  # < recursive=True by default
    ### Remove ignored entries
    if cleanup:
        removed = _clean_registry(registry_fp, ignore=IGNORE_PATTERNS)
        if verbose:
            print(
                f"Ignored {len(removed)} entries from the registry: {', '.join(removed)}"
            )
    ### Print summary
    with registry_fp.open() as fh:
        n_entries = sum(1 for _ in fh)
    # > Try to make it relative to CWD, if possible
    try:
        rel = registry_fp.relative_to(Path.cwd())
    except ValueError:
        rel = registry_fp
    if verbose:  # < Print the registry content
        with open(registry_fp, "r") as f:
            print(f.read())
    print(
        f"Pooch-registry written to {rel}"
        f"\nContains {n_entries} entries."
        f"\nYou can now upload {pkg_dir} to your object store and commit the new registry."
    )


def _clean_registry(registry_fp: Path, ignore=IGNORE_PATTERNS) -> list[str]:
    keep = []
    removed = []
    for line in registry_fp.read_text().splitlines():
        fname, *_ = line.split()
        if any(fnmatch.fnmatch(fname, pat) for pat in ignore):
            removed.append(fname)
            continue  # < Drop unwanted entry
        keep.append(line)
    registry_fp.write_text("\n".join(keep) + "\n")
    return removed


def _cast_traversable(dataset: str | Path | Traversable) -> Traversable:
    """Cast input to a Traversable.
    :param dataset:
        · Dotted package name  (e.g. ``'neddata.abbey'``) **or**
        · Directory ``Path``/``Traversable`` pointing at the raw-data folder.
    """
    if isinstance(dataset, str):
        return files(dataset)
    return cast(Traversable, dataset)


# !! The GitHub repo must be public, otherwise pooch needs authentication.
# def fetch_github_data(poochy: pooch.Pooch) -> Any:
#     """
#     Fetch a file from a server that requires authentication
#     """
#     username = os.environ.get("SOMESITE_USERNAME")
#     password = os.environ.get("SOMESITE_PASSWORD")
#     download_auth = pooch.HTTPDownloader(auth=(username, password))
#     return poochy.fetch("some-data.csv", downloader=download_auth)


# =====================================================================
# === Catalogue
# =====================================================================


# ---------------------------------------------------------------------
# --- Catalogue Helpers
# ---------------------------------------------------------------------


def _format_key(key: str) -> str:
    """Normalise keys so look‑ups are case‑insensitive and whitespace tolerant."""
    return key.lower().strip().replace(" ", "_").replace("-", "_")


def _match_any_globs(name: str, patterns: Iterable[str]) -> bool:
    """Return *True* if *name* matches at least one shell‑style glob."""
    return any(fnmatch.fnmatchcase(name, g) for g in patterns)


class Catalog(Mapping[str, Resource]):
    """Auto-discovers files & 'directory datasets' beneath *package_root*."""

    def __init__(
        self,
        package: str,
        pooch: pooch.Pooch,
        dir_patterns: Sequence[str] = ("*RAGI*",),
    ) -> None:
        self.package = package
        self.pooch = pooch
        self.dir_patterns = dir_patterns

        self._root = files(package)
        ###
        self._data: Dict[str, Resource] = {}
        self._loaders: Dict[str, Callable[[Path], Any]] = {}

        ### Build
        self._build()

    # =================================================================
    # === Build

    def _build(self) -> None:
        """Populate ``self._data`` from *pooch* registry entries."""
        for p in self.pooch.registry.keys():
            p = Path(p)
            if self._is_ignored(p):
                continue
            key, key_dir = self._construct_keys(p)
            ### DataDir
            if self._is_datadir(p):
                self._data[key_dir] = DataDir(p.parent, self.pooch)
            elif self._is_inside_datadir(p):
                continue  # > Skip everything nested inside a DataDir
            ### DataFile
            elif _match_any_globs(p.name, FILE_PATTERNS):
                loader = self._get_customloader(
                    key
                ) or u.fileio.get_default_loader(p)
                self._data[key] = DataFile(p, self.pooch, loader)

    def _construct_keys(self, path: Path) -> tuple[str, str]:
        """Create a key from the path, normalised for case and whitespace."""
        _p: Path = Path(path.as_posix())
        key: str = _format_key(f"{_p.parent}/{_p.name}")
        key_dir: str = _format_key(f"{_p.parent}/")

        return key, key_dir

    def _is_ignored(self, path: Path) -> bool:
        return any(
            _match_any_globs(part, IGNORE_PATTERNS) for part in path.parts
        )

    def _is_datadir(self, path: Path) -> bool:
        return any(
            _match_any_globs(part, self.dir_patterns) for part in path.parts
        )

    def _is_inside_datadir(self, path: Path) -> bool:
        return path.is_file() and any(
            _match_any_globs(parent.name, self.dir_patterns)
            for parent in path.parents
        )

    # =================================================================
    # === Load

    def load(self, key: str) -> Any:
        """
        Load a resource by its key. If the resource is a DataFile, it will
        be loaded using its loader function.
        """
        key = _format_key(key)
        if not key in self._data:
            self._raise_key_error(bad_key=key)
        return self._data[key].load()

    # =================================================================
    # === Custom Loader

    def set_loader(
        self, pattern: str
    ) -> Callable[[Callable[[Path], Any]], Callable[[Path], Any]]:
        """
        Decorator: register a custom *loader* for every key that matches *pattern*
        (shell-style glob, case-insensitive). Raises KeyError if no key matches.
        """

        def decorator(
            func: Callable[[Path]], pattern: str = pattern
        ) -> Callable[[Path], Any]:
            pattern = _format_key(pattern)
            matches = self.glob(pattern)
            if not matches:
                self._raise_key_error(bad_key=pattern)
            for key in matches:
                _resource = self._data.get(key)
                if isinstance(_resource, DataFile):
                    self._data[key] = DataFile(  # < Replace loader
                        path=_resource.path,
                        pooch=self.pooch,
                        loader=func,
                    )
            self._loaders[pattern] = func  # < Store the loader
            return func

        return decorator

    def _get_customloader(self, key: str) -> Callable[[Path], Any] | None:
        """Return the first loader whose pattern matches *key* (exact or
        glob)."""
        key = _format_key(key)
        for pattern, loader in self._loaders.items():
            if fnmatch.fnmatchcase(key, pattern):  # shell-style wildcards
                return loader
        return None

    # =================================================================
    # === Search & Glob

    def search(self, query: str, cutoff: int = 80) -> list[str]:
        """Searches keys based on fuzzy matching against the query."""
        query = _format_key(query)
        matches = []
        for key in self.keys():
            if fuzz.partial_ratio(key, query) > cutoff:
                matches.append(key)
        return matches

    def glob(self, pattern: str) -> list[str]:
        """Searches keys based on shell-style glob patterns."""
        pattern = _format_key(pattern)
        matches = []
        for key in self.keys():
            if fnmatch.fnmatchcase(key, pattern):
                matches.append(key)
        return matches

    # =================================================================
    # === Public: Helpers

    def items(self) -> Iterable[tuple[str, Resource]]:
        return self._data.items()

    def keys(self) -> list[str]:
        """List all resource keys in the catalogue."""
        return sorted(self._data.keys())

    def get(self, key: str, default: Any = None) -> Resource | Any:
        key = _format_key(key)
        return self._data.get(key, default)

    @property
    def datadirs(self) -> list[str]:
        """List all DataDir keys in the catalogue."""
        return [
            key for key, res in self._data.items() if isinstance(res, DataDir)
        ]

    # =================================================================
    # === Representation

    def __repr__(self) -> str:
        loaders_repr = [
            f"{name} = {loader.__name__ if loader else 'None'}"
            for name, loader in self._loaders.items()
        ]
        s = "\n    "

        return (
            f"<{self.__class__.__name__}(package='{self.package}', dir_patterns={self.dir_patterns}, pooch={self.pooch})>\n"
            f" ._root = {s}'{self._root}'\n"
            f" .pooch.base_url = {s}'{self.pooch.base_url}'\n"
            f" .datadirs = {s}- {f"{s}- ".join(self.datadirs)}\n"
            f" ._loaders = {s}- {f"{s}- ".join(loaders_repr)}\n"
            f" len = {len(self)}\n"
            f" .keys() = {s}- {f"{s}- ".join(self.keys())}\n"
        )

    # =================================================================
    # === Mapping API

    def __getitem__(self, key: str) -> Resource:
        """Catalogue[key] -> Resource"""
        key = _format_key(key)
        if not key in self._data:
            self._raise_key_error(bad_key=key)
        return self._data[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: str) -> bool:
        key = _format_key(key)
        return key in self._data

    def _suggest_alternative_keys(
        self, bad_key: str, n: int = 2, cutoff: float = 0.6
    ) -> str:
        close_matches: list[str] = difflib.get_close_matches(
            bad_key,
            self._data.keys(),  # possibilities
            n=n,
            cutoff=cutoff,  # 0.0 = very lenient, 1.0 = exact
        )
        if close_matches:
            return (
                f"\n Did you meanany of these:\n{'\n -'.join(close_matches)}?"
            )
        else:
            return "(No close matches found.)"

    def _raise_key_error(self, bad_key: str) -> None:
        """Raise a KeyError with a custom message."""
        suggestions = self._suggest_alternative_keys(bad_key)
        raise KeyError(f"Resource '{bad_key}' not found. {suggestions}")


# => ==================================================================
# => Example Usage
# => ==================================================================

if __name__ == "__main__":
    from pprint import pprint
    from IPython.display import display

    import pandas as pd

    ### Import test catalogue
    from neddata.abbey.catalog import abbey_catalog

    # %% Repr
    abbey_catalog
    # %%
    abbey_catalog.keys()
    # %%
    # === key typos ===
    # !! Typo lower case
    abbey_catalog["Regests/2_ben-Cist_Identifizierungen.csv"]

    # %%
    # cat["Regästs/2_ben-Cist_Identifizierungen.csv"] # !! raises

    # %%
    # =========================
    # === Search & glob
    # =========================
    # %%
    abbey_catalog.glob("*kdb_ben cist*")  # < Search for files in the catalogue
    # %%
    abbey_catalog.search(
        "kdb_ben-cist", cutoff=75
    )  # < Search for files wit fuzzy matching
    # %%
    abbey_catalog.search("RAGI")
    # %%
    # =========================
    # === pooch
    # =========================
    dir(abbey_catalog.pooch)  # < Show all attributes of the pooch object
    # %%
    abbey_catalog.pooch.registry  # < List all files in the dataset
    # %%
    abbey_catalog.pooch.get_url("KDB/KDB_Ben-Cist.csv")
    # %%
    abbey_catalog.pooch.is_available("KDB/KDB_Ben-Cist.csv")
    # %%
    abbey_catalog.pooch.fetch("KDB/KDB_Ben-Cist.csv")

    # %%
    print(type(abbey_catalog.pooch.registry))
    abbey_catalog.pooch.registry

    # %%
    # =========================
    # === load DataFiles
    # =========================
    df: pd.DataFrame = abbey_catalog.load(
        "Regests/2_ben-Cist Identifizierungen.csv"
    )
    display(df.head())  # < Display the first few rows of the DataFrame

    # %%
    # =========================
    # === load DataDirs
    # =========================
    abbey_catalog
    # %%
    # _key = "kdb/kdb_complete_ragi/"
    # print(abbey_catalog[_key].name)
    # print(abbey_catalog[_key].path)
    # %%
    # r = abbey_catalog.load(_key)
    # print(r)
