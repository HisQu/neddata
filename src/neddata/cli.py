# neddata/cli.py
import sys
import argparse

from ._tools import register


def main() -> None:

    # =================================================================
    # === Build Parser
    # =================================================================

    ### Top-level parser
    PARSER = argparse.ArgumentParser(
        prog="neddata",
        description="CLI of neddata.",
    )

    ### Init Subparser, will be modified in place to include script-parsers
    subparsers: argparse._SubParsersAction = PARSER.add_subparsers(
        dest="cmd", required=True
    )

    ### Edit subparser in place to include script-specific parsers
    register._add_my_parser(subparsers)

    # =================================================================
    # === Handle Cases
    # =================================================================

    if len(sys.argv) == 1:  # < Only the program name was entered
        PARSER.print_help(sys.stderr)
        PARSER.exit(1)

    # =================================================================
    # === Execute
    # =================================================================

    args = PARSER.parse_args()
    # > args.func was set to _run()
    args.func(args)  # < ⚠ pass the Namespace to the handler


if __name__ == "__main__":
    main()
