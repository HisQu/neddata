# neddata/_tools/assert_editable.py
from __future__ import annotations

import json
import sys
from importlib import metadata
from pathlib import Path
import site

def _is_editable_via_direct_url(dist: metadata.Distribution) -> bool:
    txt = dist.read_text("direct_url.json")
    if txt:
        try:
            info = json.loads(txt)
        except ValueError:
            return False
        return info.get("dir_info", {}).get("editable", False)
    return False

def _has_egg_link(pkg_name: str) -> bool:
    sp_dirs = site.getsitepackages() + [site.getusersitepackages()]
    return any(Path(d, f"{pkg_name}.egg-link").is_file() for d in sp_dirs)

def assert_editable(pkg_name: str = "neddata") -> None:
    """Abort if *pkg_name* is not installed in editable/develop mode."""
    try:
        dist = metadata.distribution(pkg_name)
    except metadata.PackageNotFoundError:
        raise RuntimeError(f"{pkg_name} is not installed at all") from None

    if _is_editable_via_direct_url(dist) or _has_egg_link(pkg_name):
        return

    raise RuntimeError(
        f"{pkg_name} must be installed editably (`pip install -e .`) "
        "to run registry-maintenance commands."
    )
