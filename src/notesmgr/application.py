#! /usr/local/bin/python3
"""Start-up of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
from contextlib import suppress
from typing import Optional
from notesmgr.cmd_line import parse_command_line
from notesmgr.main_window import MainWindow
from notesmgr.version_info import version_report


def main(argv: Optional[list[str]] = None) -> None:
    """Run the notesmgr graphical user interface until the user quits.

    A command line asking for version information is answered on the
    standard output stream, and no window is opened for it.

    Args:
        argv: Command line arguments, or None for the ones this
            program was started with.
    """
    command_line = parse_command_line(argv)
    if command_line.show_version:
        version_report(sys.stdout)
        return
    root = tkinter.Tk()
    MainWindow(root)
    root.mainloop()
    # Quitting through the menu has already destroyed the root window.
    with suppress(tkinter.TclError):
        root.destroy()
