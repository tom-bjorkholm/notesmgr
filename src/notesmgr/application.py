#! /usr/local/bin/python3
"""Start-up of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
from contextlib import suppress
from functools import partial
from pathlib import Path
from typing import Optional
from notesmgr.cmd_line import parse_command_line
from notesmgr.console import console_or_window
from notesmgr.errors import NotesmgrError
from notesmgr.failure_report import report_failures
from notesmgr.main_window import MainWindow
from notesmgr.version_info import version_report

NO_WINDOW = 'notesmgr cannot open a window: {error}'
"""What is said when there is no display to show a window on."""


def main(argv: Optional[list[str]] = None) -> None:
    """Run the notesmgr graphical user interface until the user quits.

    A command line asking for version information is answered on the
    standard output stream, and no window is opened for it. A command
    line naming a project folder opens that project, and says in a
    window of its own when the folder holds no project. What the
    command line has to say is shown in a window where there is no
    console to say it on.

    Args:
        argv: Command line arguments, or None for the ones this
            program was started with.
    """
    with console_or_window():
        command_line = parse_command_line(argv)
        if command_line.show_version:
            report_versions()
            return
    run_window(command_line.project)


def report_versions() -> None:
    """Write the version report on the standard output stream.

    Raises:
        SystemExit: The report cannot be made, which is said on the
            standard error stream in words rather than as a traceback,
            and is said before leaving, as a command line error is, so
            that a window can show it where there is no console.
    """
    try:
        version_report(sys.stdout)
    except NotesmgrError as error:
        print(error, file=sys.stderr)
        sys.exit(1)


def new_root() -> tkinter.Tk:
    """Return the root window, or leave saying why there can be none.

    Raises:
        SystemExit: There is no display, which a program started from
            a terminal with no display is told in one line.
    """
    try:
        return tkinter.Tk()
    except tkinter.TclError as error:
        sys.exit(NO_WINDOW.format(error=error))


def open_window(root: tkinter.Tk, project: Optional[Path]) -> None:
    """Fill the root window, and open the named project in it, if any."""
    window = MainWindow(root)
    if project is not None:
        window.load_project(project)


def run_window(project: Optional[Path]) -> None:
    """Show the main window until the user quits.

    Args:
        project: The project to open at start, None for none at all.
    """
    root = new_root()
    report_failures(root).run(partial(open_window, root, project))
    root.mainloop()
    # Quitting through the menu has already destroyed the root window.
    with suppress(tkinter.TclError):
        root.destroy()
