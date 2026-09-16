#! /usr/local/bin/python3
"""The font that the explorer draws with, and how large it is."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import itertools
import tkinter
from tkinter import ttk
from tkinter.font import Font
from notesmgr.note_fonts import TEXT_FONT, default_size, family_of, note_size

ROW_PADDING = 6
"""Space in pixels that a row of the tree has beyond its text."""

STYLE_KIND = 'Treeview'
"""What a style of a tree must be called for the tree to take it."""

STYLE_NUMBERS = itertools.count()
"""Numbers that tell the style of one tree from the style of another."""


class TreeFont:
    """The font of one tree, and the style that the tree takes it from.

    A ttk widget is drawn with the font of its style rather than with
    a font of its own, so the tree is given a style of its own here,
    and drawing it larger or smaller is that one font being resized.
    The rows are made as high as the font needs, so that a name is
    not cut off by a row that stayed as high as it was.

    The font is the one that Tk draws text with on this system, which
    is where a note starts out as well, so that the tree and the note
    beside it are read in one size.
    """

    def __init__(self, widget: tkinter.Misc) -> None:
        """Make the style of one tree, in the size the system gives.

        Args:
            widget: The widget that the font and the style belong to.
        """
        self.style = ttk.Style(widget)
        self.name = f'Notes{next(STYLE_NUMBERS)}.{STYLE_KIND}'
        self.normal = default_size(widget)
        self.size = self.normal
        self.font = Font(widget, family=family_of(TEXT_FONT, widget),
                         size=self.size)
        self.apply()

    def apply(self) -> None:
        """Let the tree be drawn with the font as it now stands."""
        self.style.configure(self.name, font=self.font,
                             rowheight=self.row_height())

    def row_height(self) -> int:
        """Return how high a row is, which the font says."""
        return int(self.font.metrics('linespace')) + ROW_PADDING

    def resize(self, size: int) -> int:
        """Draw with a font of another size from now on.

        Args:
            size: The size to draw the tree in.

        Returns:
            The size that is drawn in, which is as near the one asked
            for as a tree can be read at.
        """
        self.size = note_size(size)
        self.font.configure(size=self.size)
        self.apply()
        return self.size

    def zoom(self, step: int) -> int:
        """Draw so many steps larger, or smaller for a step below zero."""
        return self.resize(self.size + step)

    def normal_size(self) -> int:
        """Draw in the size that the tree started out in."""
        return self.resize(self.normal)
