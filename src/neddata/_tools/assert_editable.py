import json
from pathlib import Path
import site, pkg_resources
from importlib.metadata import PackageNotFoundError, distribution


def is_editable(pkg_name: str = "neddata") -> bool:
    try:
        dist = distribution(pkg_name)
    except PackageNotFoundError:
        return False  # not installed at all

    direct_url = dist.read_text("direct_url.json")
    if direct_url:
        data = json.loads(direct_url)
        return data.get("dir_info", {}).get("editable", False)
    return False


def _has_egg_link(pkg_name: str = "neddata") -> bool:
    sp_dirs = site.getsitepackages() + [site.getusersitepackages()]
    for sp in sp_dirs:
        link = Path(sp, f"{pkg_name}.egg-link")
        if link.is_file():
            return True
    return False


def assert_editable(pkg="neddata") -> None:
    if is_editable(pkg) or _has_egg_link(pkg):
        return
    raise RuntimeError(
        f"{pkg} must be installed in editable mode (`pip install -e .`)."
    )
