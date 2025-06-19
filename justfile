# Template from buildben copied to neddata/justfile
# This is a collection of recipes callable from the CLI
# Helpful links for just:
# - Documentation: https://just.systems/man/en/
# - Cheat Sheet: https://cheatography.com/linux-china/cheat-sheets/justfile/
# Dependencies: python3, direnv

# Allow `just deps-sync --upgrade --dry-run` pattern
set shell := ["bash", "-cu"]



# === Shortcuts / CI entrypoint =======================================

# Runs when you type just
default: 
    just --list


# =====================================================================
# === Virtual-environment 
# =====================================================================

### Store python executable from virtual environment
PY := "${VIRTUAL_ENV-}/bin/python"

# Hidden helper that must succeed first
[private]
_venv-guard:
    @test -n "${VIRTUAL_ENV-}" || { \
        echo "✗ VIRTUAL_ENV is not set, Virtual environment inactive — run 'direnv reload' first" >&2; \
        exit 1; \
    }
    
# Deletes .direnv, recreates it, installs all requirements and neddata (editable)
reset-venv:
    rm -rf .direnv        
    direnv reload   # direnv will rebuild on reload
    direnv exec . just install-recompile  # Make requirements.txt & install deps
alias resve := reset-venv

# =====================================================================
# === Installations
# =====================================================================

# Resolves dependency versions and creates requirements.txt + dev-requirements.txt
compile-requirements *ARGS:
    pip-compile pyproject.toml -o requirements.txt {{ARGS}}
    pip-compile --extra dev pyproject.toml -o dev-requirements.txt {{ARGS}}
alias comre:= compile-requirements

# Compiles all requirements & installs neddata in editable mode
install-compile *ARGS:
    just _venv-guard
    just compile-requirements {{ARGS}}
    just install
alias insco := install-compile

# Only Installs: requirements.txt & neddata in editable mode
install:
    just _venv-guard
    if ! [[ -e requirements.txt ]]; then echo "✗ Didn't find requirements.txt! Run 'just install-recompile'!" >&2; exit 1; fi
    pip-sync requirements.txt dev-requirements.txt  
    {{PY}} -m pip install -e .[dev]
alias ins := install

# Uninstalls neddata, and installs it in editable mode
reinstall:
    just _venv-guard
    {{PY}} -m pip uninstall -y "${PROJECT_NAME}"
    {{PY}} -m pip install -e .[dev]
alias reins := reinstall

# Upgrade all pins in-place
upgrade:                        
    just install-recompile --upgrade


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# === Add custom recipes below!
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%