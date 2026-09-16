#! /usr/local/bin/python3
"""The fonts that a note is drawn with, and how large they are."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from tkinter.font import Font, nametofont
from typing import AbstractSet, Mapping, NamedTuple, Optional
from notesmgr.note_blocks import BlockKind, SpanStyle

MIN_SIZE = 6
"""Smallest size that a note is drawn in, however small it is asked."""

MAX_SIZE = 40
"""Largest size that a note is drawn in, however large it is asked."""

FALLBACK_SIZE = 12
"""Size used where Tk names no size for the text that it draws."""

TEXT_FONT = 'TkTextFont'
"""The font that Tk draws ordinary text with on this system."""

FIXED_FONT = 'TkFixedFont'
"""The font that Tk draws text of one width per letter with."""

BODY_SCALE = 1.0
"""How large the ordinary text of a note is drawn, which is as given."""

FIXED_KINDS = (BlockKind.CODE, BlockKind.TABLE, BlockKind.RULE)
"""The pieces of a note that are drawn with one width per letter.

Code is written in such a font to be read in one, a table is lined
up in columns that only such a font keeps lined up, and a line
across the note is a row of letters that only such a font joins.
"""

HEADING_SCALES: Mapping[BlockKind, float] = {
    BlockKind.HEADING1: 1.8, BlockKind.HEADING2: 1.5,
    BlockKind.HEADING3: 1.3, BlockKind.HEADING4: 1.15,
    BlockKind.HEADING5: 1.05, BlockKind.HEADING6: 1.0}
"""How much larger than the text of a note each heading is drawn."""


def note_size(size: int) -> int:
    """Return a size that a note can be read at.

    Args:
        size: The size that is asked for, from wherever it came.

    Returns:
        That size, kept within what can be read, so that holding a
        key down can neither make a note vanish nor fill the window
        with a single word.
    """
    return max(MIN_SIZE, min(MAX_SIZE, size))


def default_size(widget: tkinter.Misc) -> int:
    """Return the size that Tk draws ordinary text in on this system.

    Tk gives a size in points, or in pixels written as a negative
    number, and either way how large it is, is where a note starts.
    """
    named = nametofont(TEXT_FONT, root=widget)
    return abs(int(named.actual('size'))) or FALLBACK_SIZE


def family_of(name: str, widget: tkinter.Misc) -> str:
    """Return the family of one of the fonts that Tk names itself."""
    return str(nametofont(name, root=widget).actual('family'))


class FontKey(NamedTuple):
    """What tells one of the fonts that a note is drawn with from another.

    The scale is how large the font is against the size that the
    note is drawn in, so that making the note larger or smaller is
    one size that every font of it follows.
    """

    scale: float = BODY_SCALE
    fixed: bool = False
    bold: bool = False
    italic: bool = False


BODY_KEY = FontKey()
"""The font that the ordinary text of a note is drawn with."""


def font_key(kind: BlockKind,
             styles: AbstractSet[SpanStyle] = frozenset()) -> FontKey:
    """Return the font that one run of text of a piece is drawn with.

    A heading is drawn larger and bold, a quote in italics, and
    code and a table in the font of one width per letter. What is
    said about the run of text itself is added to that, so that
    code inside a heading is drawn as large as the heading is.

    Args:
        kind: What the piece of the note holding the run of text is.
        styles: What is said about that run of text.

    Returns:
        The font to draw it with.
    """
    fixed = kind in FIXED_KINDS or SpanStyle.CODE in styles
    bold = kind in HEADING_SCALES or SpanStyle.BOLD in styles
    italic = kind is BlockKind.QUOTE or SpanStyle.ITALIC in styles
    scale = HEADING_SCALES.get(kind, BODY_SCALE)
    return FontKey(scale, fixed, bold, italic)


def font_tag(key: FontKey) -> str:
    """Return the name of the text tag that carries one of the fonts."""
    return f'font{key.scale}{key.fixed:d}{key.bold:d}{key.italic:d}'


class NoteFonts:
    """The fonts that a note is drawn with, made larger all together.

    A font is made when a note first needs it and is then kept, so
    that a note of headings and code brings its fonts along while a
    note of plain text needs one. Changing the size configures every
    font that was made, and the text tags that carry them draw with
    the new size from then on without being touched.
    """

    def __init__(self, widget: tkinter.Misc,
                 size: Optional[int] = None) -> None:
        """Get ready to draw a note with fonts of a size.

        Args:
            widget: The widget that the fonts belong to, which is
                what Tk is asked about the system's own fonts over.
            size: The size to draw the ordinary text of a note in,
                None for the size that Tk draws text in.
        """
        self.widget = widget
        self.normal = default_size(widget) if size is None else size
        self.size = note_size(self.normal)
        self.body_family = family_of(TEXT_FONT, widget)
        self.fixed_family = family_of(FIXED_FONT, widget)
        self.fonts: dict[FontKey, Font] = {}

    def font(self, key: FontKey) -> Font:
        """Return the font of a key, made the first time it is asked for."""
        if key not in self.fonts:
            self.fonts[key] = self._make(key)
        return self.fonts[key]

    def _make(self, key: FontKey) -> Font:
        """Make the font of a key, in the size that is drawn in now."""
        family = self.fixed_family if key.fixed else self.body_family
        return Font(self.widget, family=family, size=self.scaled(key),
                    weight='bold' if key.bold else 'normal',
                    slant='italic' if key.italic else 'roman')

    def scaled(self, key: FontKey) -> int:
        """Return how large the font of a key is at the size drawn in."""
        return max(1, round(self.size * key.scale))

    def resize(self, size: int) -> int:
        """Draw with fonts of another size from now on.

        Args:
            size: The size to draw the ordinary text of a note in.

        Returns:
            The size that is drawn in, which is as near the one
            asked for as a note can be read at.
        """
        self.size = note_size(size)
        for key, made in self.fonts.items():
            made.configure(size=self.scaled(key))
        return self.size

    def zoom(self, step: int) -> int:
        """Draw so many steps larger, or smaller for a step below zero."""
        return self.resize(self.size + step)

    def normal_size(self) -> int:
        """Draw in the size that the note started out in."""
        return self.resize(self.normal)

    def indent_step(self) -> int:
        """Return how far one step of indentation is, in pixels."""
        return self.font(BODY_KEY).measure('    ')
