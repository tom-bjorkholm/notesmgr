#! /usr/local/bin/python3
"""The command line of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
from typing import NamedTuple, Optional
import argcomplete

PROGRAM_NAME = 'notesmgr'
"""Name that the command line help calls this program."""

DESCRIPTION = 'Manage small notes and AI prompts.'
"""What the command line help says this program is for."""

FOLDER_HELP = 'Project folder to open at start up.'
"""What the command line help says about the project folder."""

VERSION_HELP = 'Report the versions of notesmgr and of what it uses.'
"""What the command line help says about the version flag."""


class CommandLine(NamedTuple):
    """What the command line asked notesmgr to do."""

    project: Optional[Path]
    show_version: bool


def argument_parser() -> argparse.ArgumentParser:
    """Return the parser that reads the notesmgr command line."""
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME,
                                     description=DESCRIPTION)
    parser.add_argument('project', nargs='?', default=None, type=Path,
                        metavar='PROJECT_FOLDER', help=FOLDER_HELP)
    parser.add_argument('--version', dest='show_version', default=False,
                        action='store_true', help=VERSION_HELP)
    return parser


def parse_command_line(argv: Optional[list[str]] = None) -> CommandLine:
    """Return what the given command line, or sys.argv, asked for.

    Whether the named folder holds a project is not decided here. A
    graphical application says that in a window of its own, and not on
    an error stream that a program started from a desktop has not got.

    Args:
        argv: Command line arguments, or None for the ones this
            program was started with.

    Returns:
        What was asked for.
    """
    parser = argument_parser()
    argcomplete.autocomplete(parser)
    parsed = parser.parse_args(argv)
    assert isinstance(parsed.project, (Path, type(None)))
    assert isinstance(parsed.show_version, bool)
    return CommandLine(project=parsed.project,
                       show_version=parsed.show_version)
