"""Environment Variables Management:
- setup(): Retrieve environment variables from .envrc for developer tasks
- Initialize environs.Env() as a handle for connecting to the environment at runtime
"""

# %%
import sys
import os
import subprocess
from pathlib import Path
import json

from environs import Env, EnvError

from typing import Sequence


# %%
# =====================================================================
# === Public Helper "env" for connecting to the environment
# =====================================================================

env: Env = Env()  # < Create a global Env Wrapper (copies available variables)

def import_vars(*names: str, allow_blank: bool = False) -> tuple[str, ...]:
    """
    Return the requested environment variables **in order**.
    * Raises RuntimeError if one or more are missing (or blank when allow_blank=False)
      and prints a friendly summary to stderr first.
    * If allow_blank=True, empty strings are accepted.
    """
    validate = (lambda s: True) if allow_blank else None
    missing: list[str] = []
    values: list[str] = []

    for name in names:
        try:
            # > Accept empty strings if allow_blank is True
            val = env.str(name, validate=validate)  # < raises EnvError
            if not allow_blank and val == "":
                raise EnvError(f"{name} may not be blank")
            values.append(val)
        except EnvError as exc:  # < collect but don't abort yet
            missing.append(f"{name}: {exc}")

    if missing:
        msg = "Missing or invalid environment variables:\n  " + "\n  ".join(
            missing
        )
        print(msg, file=sys.stderr)  # visible hint for CLI users
        raise RuntimeError(msg)

    return tuple(values)


if __name__ == "__main__":
    a, b = import_vars("PROJECT_NAME", "BASE_URL")
    print(a, b)
    # %%
    # !! Throws error
    # import_vars("PROJECT_name", "BASE_URL")


# %%
# =====================================================================
# === For Developers: Import .envrc
# =====================================================================
# !!! Only editable pip-installs will retain a .envrc !!!


# --- Public API ------------------------------------------------------
def setup(quiet: bool = False):
    PROJECT_ROOT = _find_project_root()
    if PROJECT_ROOT is None:
        raise RuntimeError("Could not find project root directory.")
    _load_direnv_envrc(cwd=PROJECT_ROOT, quiet=quiet)


# --- Private Helpers -------------------------------------------------
def _find_project_root(
    start: Path | None = None,
    sentinels: Sequence[str] = (".git", "pyproject.toml", "setup.py"),
    raise_error: bool = False,
) -> Path | None:
    """
    Returns environment variable "PROJECT_ROOT". Otherwise, falls back
    to Walk upward from *start* (or cwd) until we find a sentinel that
    marks the project root. Raises RuntimeError if none found.
    """
    env_root = os.getenv("PROJECT_ROOT")
    if env_root:
        return Path(env_root).resolve()  # !! Early exit

    here = (start or Path.cwd()).resolve()
    for candidate in [here, *here.parents]:
        if any((candidate / s).exists() for s in sentinels):
            return candidate  # < Found!

    m = f"Not inside a project; looked for {sentinels} starting at {here}"
    if raise_error:
        raise RuntimeError(m)
    else:
        print(m)


if __name__ == "__main__":
    print(_find_project_root(Path(".")))
    print(_find_project_root(None))


# %%
def _load_direnv_envrc(cwd: str | Path = ".", quiet: bool = False) -> None:
    """Merge the official .envrc into the current environment"""

    ### Skip if we already ran inside a direnv session
    if "DIRENV_DIR" in os.environ:
        return  # !! Early exit; 2nd Call causes JSONDecodeError

    ### Prepare child-process environment
    child_env = os.environ.copy()  # < Lives only until child process spawns
    if quiet:
        # > Empty string silences *all* log lines from direnv
        child_env.setdefault("DIRENV_LOG_FORMAT", "")

    ### Run direnv .envrc
    try:
        payload = subprocess.check_output(
            ["direnv", "export", "json"],
            cwd=cwd,
            text=True,
            env=child_env,  # < Use our modified environment
            stderr=subprocess.DEVNULL if quiet else None,
        )
        os.environ.update(json.loads(payload))  # idempotent; no new venv
    except (FileNotFoundError, subprocess.CalledProcessError):
        # > direnv binary missing
        # > .envrc not yet allowed
        # > export produced non-JSON because of an unexpected message
        pass


if __name__ == "__main__":
    root = _find_project_root()
    if root:
        _load_direnv_envrc(cwd=root)
    print(os.getenv("PROJECT_ROOT"))
    print(os.getenv("BASE_URL"))
