import argparse
import importlib.resources as ir

from neddata._tools.assert_editable import assert_editable
from neddata.datamodel import make_pooch_registry


# ================================================================== #
# === CLI wiring                                                     #
# ================================================================== #

CMD_NAME = "register"  # < Name of the command, used in CLI
CMD_ALIASES = ["reg"]  # < Alias shortcut of the command
DOC = f"Make or update the `pooch_registry.txt` file for a dataset package. !! Requires full clone & editable install !! Aliases: {CMD_ALIASES} "


def _add_my_parser(subparsers: argparse._SubParsersAction) -> None:
    p: argparse.ArgumentParser = subparsers.add_parser(
        name=CMD_NAME,
        aliases=CMD_ALIASES,
        description=DOC,
        help=DOC,
    )
    p.add_argument("package", help="Dataset package, e.g. neddata.abbey")
    # > Entrypoint, retrieved as args.func in cli.py
    p.set_defaults(func=_run)


def _run(args: argparse.Namespace) -> None:

    ### Add "neddata." prefix if not present
    if not args.package.startswith("neddata."):
        args.package = "neddata." + args.package
    pkg_path = ir.files(args.package)

    ### Assertions
    assert_editable("neddata")

    ### Register
    make_pooch_registry(pkg_path)
