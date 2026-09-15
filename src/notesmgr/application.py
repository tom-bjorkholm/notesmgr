#! /usr/local/bin/python3
"""Start-up of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import suppress
from notesmgr.main_window import MainWindow


def main() -> None:
    """Run the notesmgr graphical user interface until the user quits."""
    root = tkinter.Tk()
    MainWindow(root)
    root.mainloop()
    # Quitting through the menu has already destroyed the root window.
    with suppress(tkinter.TclError):
        root.destroy()
