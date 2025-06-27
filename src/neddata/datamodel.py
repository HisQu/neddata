"""Loads datasets"""

# %%

from __future__ import annotations

from importlib.resources import files
from pathlib import Path
import fnmatch
from difflib import get_close_matches
import textwrap

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
# === Resource, DataFile, DataDir
# =====================================================================


class Resource:

    def __init__(self, path: Path, pooch: pooch.Pooch) -> None:
        self.path = path  # < Path relative to the package root
        self.pooch = pooch

        if path.is_absolute():
            raise ValueError(
                f"Resource path must be relative, not absolute: {path}"
            )

    def load(self) -> Path:
        """Placeholder, every Resource requires a load() method."""
        return self.path

    @property
    def path_local(self) -> Path:
        cache_root = self.pooch.abspath
        return cache_root / self.path

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def name(self) -> str:
        return self.path.name


# === DataFile ========================================================


class DataFile(Resource):
    """A DataFile is a file that is catalogued and can be loaded using a loader function."""

    def __init__(
        self,
        path: Path,
        pooch: pooch.Pooch,
        loader: Callable[[Path], Any] | None = None,
    ) -> None:
        super().__init__(path, pooch)
        self.loader = loader

    def load(self) -> Any:
        if self.loader is None:
            raise ValueError(f"No loader for {self.stem}")
        ### (Download and) Resolve Local Filepath (default is OS cache)
        local_fp = Path(self.pooch.fetch(self.path.as_posix()))
        try:
            return self.loader(local_fp)  # < Load file
        except Exception as e:
            raise ValueError(
                f"Failed to load '{self.name}' with loader '{self.loader.__name__ if self.loader else 'unknown loader'}'"
            ) from e


# === DataDir ========================================================


class DataDir(Resource):
    """
    A DataDir is a directory (or compressed archive) that contains
    files, but those files are not catalogued individually. Instead, the
    directory itself is catalogued.
    """

    def __init__(self, path: Path, pooch: pooch.Pooch) -> None:
        super().__init__(path, pooch)
        self._unpacked = False  # < Whether the archive has been extracted
        # self._ensure_downloaded()

    def load(self) -> Path:
        """DataDir does not load anything, it is a directory."""
        self._ensure_downloaded()  # < Ensure all files are downloaded
        return self.path_local
        # local_fp = Path(self.pooch.fetch(self.path.as_posix()))

    def list(self) -> list[str]:
        self._ensure_downloaded()
        return [p.name for p in self.path_local.iterdir() if p.is_file()]

    @property
    def is_archive(self) -> bool:
        """Check if the directory is an archive (e.g., a zip file)."""
        return self.path.suffix in {".zip", ".tar", ".tar.gz", ".tgz"}

    def _ensure_downloaded(self) -> None:
        """
        Fetch all required files **once**. Idempotent and safe
        under multiprocessing thanks to Pooch's file lock.
        """

        if self.path_local.exists():
            return  # !! already cached
        if self.is_archive:
            self._fetch_archive()
        else:
            self._fetch_piecewise()

    def _fetch_archive(self) -> None:
        """Unpack the directory if it is an archive.
        This is a no-op if the directory is not an archive.
        """
        ### Assertions
        if not self.is_archive:
            raise ValueError(
                f"Cannot unpack {self.name}: Not an archive (zip/tar)."
            )
        if self._unpacked:
            return  # !! already unpacked

        ### Unpack
        processor = (
            pooch.Untar(extract_dir=str(self.path))
            if self.name.endswith((".tar.gz", ".tgz", ".tar"))
            else pooch.Unzip(extract_dir=str(self.path))  # zip variant
        )
        self.pooch.fetch(self.path.as_posix(), processor=processor)
        self._unpacked = True  # < Mark as unpacked

    def _fetch_piecewise(self) -> None:
        """Fetch all files in the directory piece-wise.
        This is a no-op if the directory is not an archive.
        """
        if self.is_archive:
            raise ValueError(
                f"Cannot fetch piecewise {self.name}: Is an archive (zip/tar)."
            )
        prefix = f"{self.path.as_posix()}/"
        for fname in self.pooch.registry:
            fname: str
            if fname.startswith(prefix):
                self.pooch.fetch(fname)


# =====================================================================
# === Pooch Registry
# =====================================================================


def make_pooch_registry(dir: Path) -> None:

    raw_dir = Path(dir).expanduser()
    manifest = raw_dir / "pooch_registry.txt"

    if not manifest.is_file():  # < Create empty .txt
        manifest.touch()

    pooch.make_registry(raw_dir, manifest)

    print(
        textwrap.dedent(
            f"""
    Manifest written to {manifest.relative_to(Path.cwd())}
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
        registry=None,  # < Loaded after creation
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
#     download_auth = pooch.HTTPDownloader(auth=(username, password))
#     return poochy.fetch("some-data.csv", downloader=download_auth)


# =====================================================================
# === Catalogue
# =====================================================================


# ---------------------------------------------------------------------------
# --- Helpers
# ---------------------------------------------------------------------------


def _format_key(key: str) -> str:
    """Normalise keys so look‑ups are case‑insensitive and whitespace tolerant."""
    return key.lower().strip().replace(" ", "_").replace("-", "_")


def _match_any_globs(name: str, patterns: Iterable[str]) -> bool:
    """Return *True* if *name* matches at least one shell‑style glob."""
    return any(fnmatch.fnmatchcase(name, g) for g in patterns)


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
    # =================================================================

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
            elif _match_any_globs(p.name, self.FILE_PATTERNS):
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
            _match_any_globs(part, self.IGNORE_PATTERNS) for part in path.parts
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
    # =================================================================

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
    # =================================================================

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
    # =================================================================

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
    # =================================================================

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
    # =================================================================

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
    # =================================================================

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
    ) -> list[str]:
        return get_close_matches(
            bad_key,
            self._data.keys(),  # possibilities
            n=n,
            cutoff=cutoff,  # 0.0 = very lenient, 1.0 = exact
        )

    def _raise_key_error(self, bad_key: str) -> None:
        """Raise a KeyError with a custom message."""
        suggestions = self._suggest_alternative_keys(bad_key)
        hint = ", ".join(suggestions) if suggestions else "no close matches"
        raise KeyError(
            f"Resource '{bad_key}' not found; Did you mean: '{hint}'?"
        )


# => ==================================================================
# => Example Usage
# => ==================================================================

if __name__ == "__main__":
    from pprint import pprint
    from IPython.display import display

    import pandas as pd

    ### Import test catalogue
    from neddata.abbey.catalog import cat

    # %% Repr
    cat
    # %%
    cat.keys()
    # %%
    # === key typos ===
    # !! Typo lower case
    cat["Regests/2_ben-Cist_Identifizierungen.csv"]

    # %%
    # cat["Regästs/2_ben-Cist_Identifizierungen.csv"] # !! raises

    # %%
    # =========================
    # === Search & glob
    # =========================
    # %%
    cat.glob("*kdb_ben cist*")  # < Search for files in the catalogue
    # %%
    cat.search(
        "kdb_ben-cist", cutoff=75
    )  # < Search for files wit fuzzy matching
    # %%
    cat.search("RAGI")
    # %%
    # =========================
    # === pooch
    # =========================
    dir(cat.pooch)  # < Show all attributes of the pooch object
    # %%
    cat.pooch.registry  # < List all files in the dataset
    # %%
    cat.pooch.get_url("KDB/KDB_Ben-Cist.csv")
    # %%
    cat.pooch.is_available("KDB/KDB_Ben-Cist.csv")
    # %%
    cat.pooch.fetch("KDB/KDB_Ben-Cist.csv")

    # %%
    print(type(cat.pooch.registry))
    cat.pooch.registry

    # %%
    # =========================
    # === load DataFiles
    # =========================
    df: pd.DataFrame = cat.load("Regests/2_ben-Cist Identifizierungen.csv")
    display(df.head())  # < Display the first few rows of the DataFrame

    # %%
    # =========================
    # === load DataDirs
    # =========================
    cat
    # %%
    _key = "kdb/kdb_complete_ragi/"
    print(cat[_key].name)
    print(cat[_key].path)
    # %%
    r = cat.load(_key)
    print(r)

    # %%
