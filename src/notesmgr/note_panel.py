#! /usr/local/bin/python3
"""The panel at the right of the main window, showing a note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Optional

PADDING = 8
"""Space in pixels left around what the panel shows."""


class NotePanel:
    """Shows what is selected in the explorer.

    So far that is the path of the selected file or folder. The note
    itself, formatted for reading, and the row of buttons above it,
    are what this panel grows into.
    """

    def __init__(self, parent: tkinter.Misc) -> None:
        """Build the panel in a frame of its own inside a parent widget."""
        self.frame = ttk.Frame(parent)
        self.path_label = ttk.Label(self.frame, anchor=tkinter.W)
        self.path_label.pack(side=tkinter.TOP, fill=tkinter.X, padx=PADDING,
                             pady=PADDING)

    def show_path(self, path: Optional[Path]) -> None:
        """Show the path of what is selected, nothing for nothing.

        Args:
            path: What is selected in the explorer, None for nothing.
        """
        self.path_label.configure(text='' if path is None else str(path))

    def shown_path(self) -> str:
        """Return the path the panel is showing, empty for none."""
        return str(self.path_label.cget('text'))
