#! /usr/local/bin/python3
"""The text tags that the pieces of a formatted note are drawn with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Optional
from notesmgr.note_blocks import Block, BlockKind, Span, SpanStyle
from notesmgr.note_fonts import BODY_KEY, HEADING_SCALES, FontKey, \
    NoteFonts, font_key, font_tag

CODE_BACKGROUND = '#f0f0f0'
"""Colour behind code, which is what sets it off from the prose."""

QUOTE_COLOUR = '#4a4a4a'
"""Colour of a quoted piece, a grey that is read as quieter text."""

LINK_COLOUR = '#1a5fb4'
"""Colour of the text of a link, the blue that a link is known by."""

RULE_COLOUR = '#9a9a9a'
"""Colour of a line drawn across the note."""

LINK_TAG = 'link'
"""Tag of the text of a link, which is underlined and coloured."""

CODE_SPAN_TAG = 'codespan'
"""Tag of code inside a line of prose, which is set off behind."""

STRIKE_TAG = 'strike'
"""Tag of text that is struck through, which Tk draws a line over."""

IMAGE_TAG = 'image'
"""Tag of an image that is named rather than drawn."""

GAP_TAG = 'gap'
"""Tag of the blank line that is left between two pieces of a note."""

INDENT_TAG = 'indent{depth}'
"""Tag that writes a piece of a note so many steps from the left."""

ITEM_TAG = 'item{depth}'
"""Tag that writes a list item, its bullet standing out to the left.

What the bullet takes up is left free on the lines after the first
one, so that a list item that is broken over several lines reads as
one item rather than as the beginning of another.
"""

MAX_INDENT = 8
"""Most steps from the left that a piece of a note is written at.

A note nested deeper than this is written at this depth, which
keeps a note that is nothing but nested lists readable in a narrow
window.
"""

RAW_KEY = FontKey(fixed=True)
"""The font of a note that is shown as it is written.

A note that is no markdown is shown as the file holds it, so it is
drawn with one width per letter, which is what keeps a table that
was lined up by hand lined up. It is the font of the area itself
rather than of a tag, so that it follows the size of the note the
way every other font of it does.
"""

GAP_KEY = FontKey(scale=0.4)
"""The font of the blank line that is left between two pieces.

A blank line is as tall as the font of it, which is how the room
between two pieces of a note is left. Tk would space the lines
inside a code block and a table as well.
"""

HEADING_GAPS = 2
"""Blank lines above a heading, which is what sets a part apart."""

BULLET_ROOM = '•   '
"""What a bullet is taken to take up on the line that carries it."""


def indent_tag(block: Block) -> str:
    """Return the tag that writes a piece of a note where it belongs.

    Args:
        block: The piece of the note that is to be written.

    Returns:
        The name of the tag that indents it, which leaves room for
        the bullet of a list item and none for anything else.
    """
    depth = min(block.indent, MAX_INDENT)
    pattern = ITEM_TAG if block.prefix else INDENT_TAG
    return pattern.format(depth=depth)


def gap_lines(block: Block, previous: Optional[Block]) -> int:
    """Return how many blank lines are left above a piece of a note.

    A heading is set off from the part above it by a wider gap, and
    the items of one list follow one another with no gap at all, the
    way the note was written. Nothing is left above the first piece
    of a note, which begins at the top of the area.

    Args:
        block: The piece of the note that is to be written.
        previous: The piece written above it, None for the first one.

    Returns:
        How many blank lines to write above it.
    """
    if previous is None:
        return 0
    if block.kind in HEADING_SCALES:
        return HEADING_GAPS
    if block.prefix and previous.prefix:
        return 0
    return 1


def span_styles(span: Span) -> tuple[str, ...]:
    """Return the tags that say how one run of text looks.

    The font of a run of text is a tag of its own, and these are
    what is drawn on top of it: the colour of a link, the shading
    of code inside a line of prose, the line over text that is
    struck through, and how an image is named.
    """
    tags = {SpanStyle.LINK: LINK_TAG, SpanStyle.CODE: CODE_SPAN_TAG,
            SpanStyle.STRIKE: STRIKE_TAG, SpanStyle.IMAGE: IMAGE_TAG}
    return tuple(tag for style, tag in tags.items() if style in span.styles)


class NoteTags:
    """Defines and hands out the tags that a note is drawn with.

    The tag that carries a font is made the first time a note needs
    it, and every tag that is measured in pixels is given afresh
    whenever the note is drawn in another size, so that the space
    between the pieces and the indentation of a list follow the text.
    """

    def __init__(self, area: tkinter.Text, size: Optional[int] = None) \
            -> None:
        """Define the tags of a text area that a note is drawn in.

        Args:
            area: The text area that the tags belong to.
            size: The size to draw the ordinary text of a note in,
                None for the size that Tk draws text in.
        """
        self.area = area
        self.fonts = NoteFonts(area, size)
        self.made: set[str] = set()
        self.area.configure(font=self.fonts.font(RAW_KEY))
        self._colour_tags()
        self._sized_tags()

    def _colour_tags(self) -> None:
        """Define the tags that say nothing about how large the text is."""
        self.area.tag_configure(BlockKind.CODE, background=CODE_BACKGROUND)
        self.area.tag_configure(BlockKind.QUOTE, foreground=QUOTE_COLOUR)
        self.area.tag_configure(BlockKind.RULE, foreground=RULE_COLOUR,
                                wrap=tkinter.NONE)
        self.area.tag_configure(BlockKind.TABLE, wrap=tkinter.NONE)
        self.area.tag_configure(CODE_SPAN_TAG, background=CODE_BACKGROUND)
        self.area.tag_configure(STRIKE_TAG, overstrike=True)
        self.area.tag_configure(LINK_TAG, foreground=LINK_COLOUR,
                                underline=True)

    def _sized_tags(self) -> None:
        """Define the tags that are measured in the size drawn in.

        The room between two pieces of a note is left by the blank
        line between them, and the indentation of a list is measured
        in what the text of the note takes up, so both of them are
        given again whenever the note is drawn in another size.
        """
        self.area.tag_configure(GAP_TAG, font=self.fonts.font(GAP_KEY))
        step = self.fonts.indent_step()
        room = self.fonts.font(BODY_KEY).measure(BULLET_ROOM)
        for depth in range(MAX_INDENT + 1):
            self.area.tag_configure(INDENT_TAG.format(depth=depth),
                                    lmargin1=depth * step,
                                    lmargin2=depth * step)
            self.area.tag_configure(ITEM_TAG.format(depth=depth),
                                    lmargin1=depth * step,
                                    lmargin2=depth * step + room)

    def font_tag_of(self, kind: BlockKind, span: Span) -> str:
        """Return the tag that draws a run of text in its own font.

        The tag is defined the first time a note needs it, and from
        then on it follows the size that the note is drawn in,
        because it is the font itself that the size is changed on.

        Args:
            kind: What the piece of the note holding the run of text is.
            span: The run of text that is to be drawn.

        Returns:
            The name of the tag that carries its font.
        """
        key = font_key(kind, span.styles)
        name = font_tag(key)
        if name not in self.made:
            self.area.tag_configure(name, font=self.fonts.font(key))
            self.made.add(name)
        return name

    def span_tags(self, kind: BlockKind, span: Span,
                  indent: str) -> tuple[str, ...]:
        """Return every tag that one run of text of a piece is drawn with.

        Args:
            kind: What the piece of the note holding the run of text is.
            span: The run of text that is to be drawn.
            indent: The tag that writes the piece where it belongs.

        Returns:
            The tags to give the text, the piece it belongs to first
            and what is said about the run of text itself last.
        """
        return (str(kind), indent, self.font_tag_of(kind, span),
                *span_styles(span))

    def resize(self, size: int) -> int:
        """Draw the note in another size from now on."""
        drawn = self.fonts.resize(size)
        self._sized_tags()
        return drawn

    def zoom(self, step: int) -> int:
        """Draw so many steps larger, or smaller for a step below zero."""
        return self.resize(self.fonts.size + step)

    def normal_size(self) -> int:
        """Draw the note in the size that it started out in."""
        return self.resize(self.fonts.normal)
