import argparse
import importlib.resources as ir

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
    
    ### Register
    try:
        make_pooch_registry(pkg_path)
    # > If not editable full clone, key error is likely during import process
    except KeyError as e:
        print(f"Error: {e}")
        print(
            "This command requires a full clone of the dataset package and an editable install."
        )
        return
