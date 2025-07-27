"""Base Classes for Data Model Resources"""

from __future__ import annotations
from pathlib import Path

import pooch

from typing import Callable, Any


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
