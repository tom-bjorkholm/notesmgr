#! /usr/local/bin/python3
"""The area of the main window that a note is read in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path
from tkinter import ttk
from typing import Iterator, Optional, Sequence
from notesmgr.note_blocks import Block, BlockKind, Span, SpanStyle, \
    markdown_blocks
from notesmgr.note_image import image_path, shrink_factor
from notesmgr.note_table import table_text
from notesmgr.note_tags import GAP_TAG, NoteTags, gap_lines, indent_tag
from notesmgr.note_text import EMPTY_NOTE, NoteText

WARNING_COLOUR = '#b00020'
"""Colour of a warning above a note, a red that is hard to miss."""

WARNING_FONT = 'TkHeadingFont'
"""Font of a warning above a note, heavier than the note itself."""

WRAP_WIDTH = 600
"""Pixels after which a long warning is broken into another line."""

PADDING = 8
"""Space in pixels left around what the area shows."""

TEXT_ROW = 1
"""Row of the area that the note itself is shown in."""

RULE_TEXT = '─' * 200
"""What a line across the note is drawn with.

The line is drawn long and is not broken where the window ends, so
that it reaches across however wide the window is made.
"""

IMAGE_TEXT = '[{alt}]'
"""How an image of a note is named where it is not drawn."""

MISSING_ALT = 'image'
"""What an image that the note gives no description of is called."""

IMAGE_PADDING = 4
"""Space in pixels left around an image that is drawn in a note."""

EDGE_OPTIONS = ('borderwidth', 'highlightthickness', 'padx')
"""Options of a text area that leave room on both sides of its text."""


def block_spans(block: Block, columns: int) -> tuple[Span, ...]:
    """Return everything that is written for one piece of a note.

    The bullet or the number of a list item and the line of a rule
    are drawn rather than read, so they are written here and are no
    part of what the note holds. A table is laid out in columns
    here, as wide as the area it is drawn in lets it be.

    Args:
        block: The piece of the note that is to be written.
        columns: How many letters of a table fit across the area,
            once the piece is indented.

    Returns:
        The runs of text to write, in the order they are written in.
    """
    if block.table is not None:
        return (Span(table_text(block.table, columns)),)
    if block.kind is BlockKind.RULE:
        return (Span(RULE_TEXT),)
    if block.prefix:
        return (Span(block.prefix), *block.spans)
    return block.spans


def image_text(span: Span) -> str:
    """Return how an image is named where the image is not drawn."""
    return IMAGE_TEXT.format(alt=span.text or MISSING_ALT)


@dataclass
class Drawn:
    """What a note formatted for reading was last drawn from and in.

    The pieces are kept so that the note can be drawn again when its
    tables are to be laid out to another width, which is how many
    letters of a table fit across the area, and the pictures are
    kept because Tk draws a picture that is no longer kept as
    nothing at all. A note shown as it is written has no pieces.
    """

    blocks: Sequence[Block] = ()
    folder: Optional[Path] = None
    columns: int = 0
    pictures: list[tkinter.PhotoImage] = field(default_factory=list)


class NoteView:
    """Shows the text of one note, with any warning above it.

    The warning is what could not be shown and why, and it is left
    out of the way whenever there is nothing to warn about. A note
    written in markdown is shown formatted for reading, and every
    other note is shown as it is written.
    """

    def __init__(self, parent: tkinter.Misc) -> None:
        """Build the area in a frame of its own inside a parent widget.

        The note is read here and edited elsewhere, so the area cannot
        be written in. Tk leaves such an area out when Tab goes from
        widget to widget, so it is asked to take the focus all the
        same, which lets the note be scrolled and selected with keys.
        """
        self.frame = ttk.Frame(parent)
        self.warning = ttk.Label(self.frame, foreground=WARNING_COLOUR,
                                 font=WARNING_FONT, justify=tkinter.LEFT,
                                 wraplength=WRAP_WIDTH)
        self.area = tkinter.Text(self.frame, wrap=tkinter.WORD,
                                 state=tkinter.DISABLED, takefocus=True)
        self.tags = NoteTags(self.area)
        self.note = EMPTY_NOTE
        self.drawn = Drawn()
        self._lay_out()
        self.area.bind('<Configure>', self._resized, add=True)

    def _lay_out(self) -> None:
        """Put the warning above the note and let the note have the room."""
        scroll = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL,
                               command=self.area.yview)
        self.area.configure(yscrollcommand=scroll.set)
        self.frame.rowconfigure(TEXT_ROW, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.warning.grid(row=0, column=0, columnspan=2, sticky=tkinter.EW,
                          pady=PADDING)
        self.area.grid(row=TEXT_ROW, column=0, sticky=tkinter.NSEW)
        scroll.grid(row=TEXT_ROW, column=1, sticky=tkinter.NS)
        self.warning.grid_remove()

    def show(self, note: NoteText, formatted: bool = False,
             folder: Optional[Path] = None) -> None:
        """Show a note that was read, warning and all.

        Args:
            note: The text to show and the warning to show above it.
            formatted: Whether the note is written in markdown and
                is therefore shown formatted for reading rather than
                as it is written.
            folder: The folder that holds the note, which is where
                an image that the note shows is looked for.
        """
        self.note = note
        self.show_warning(note.warning)
        if formatted:
            self.show_blocks(markdown_blocks(note.text), folder)
        else:
            self.show_text(note.text)

    def show_warning(self, warning: str) -> None:
        """Show a warning above the note, and none when there is none."""
        self.warning.configure(text=warning)
        if warning:
            self.warning.grid()
        else:
            self.warning.grid_remove()

    @contextmanager
    def _writing(self) -> Iterator[None]:
        """Empty the area and let it be written to, and no longer."""
        self.area.configure(state=tkinter.NORMAL)
        self.area.delete('1.0', tkinter.END)
        yield
        self.area.configure(state=tkinter.DISABLED)

    def show_text(self, text: str) -> None:
        """Show a text in an area that the user cannot type in."""
        self.drawn = Drawn()
        with self._writing():
            self.area.insert('1.0', text)

    def show_blocks(self, blocks: Sequence[Block],
                    folder: Optional[Path] = None) -> None:
        """Show the pieces that a note formatted for reading is drawn in.

        Args:
            blocks: The pieces of the note, in the order they are
                drawn in.
            folder: The folder that holds the note, which is where
                an image that the note shows is looked for.
        """
        self.drawn = Drawn(blocks, folder)
        self._draw_blocks()

    def _draw_blocks(self) -> None:
        """Draw the pieces of the note, tables as wide as they fit."""
        self.drawn.pictures = []
        self.drawn.columns = self.table_columns(0)
        previous: Optional[Block] = None
        with self._writing():
            for block in self.drawn.blocks:
                self._write_gap(block, previous)
                self._write_block(block)
                previous = block

    def table_columns(self, depth: int) -> int:
        """Return how many letters of a table fit across the area.

        An area that Tk has not laid out yet is 1 pixel wide, so the
        width it asks for is taken instead, which is what it is given
        when it is shown in a window of its natural size. Whether it
        is on the screen does not matter: a window is laid out to the
        size it is given before it is shown, and is not told again.

        Args:
            depth: How many steps from the left the table is written.

        Returns:
            How many letters fit, at least 1.
        """
        width = self.area.winfo_width()
        if width <= 1:
            width = self.area.winfo_reqwidth()
        edges = sum(self.area.winfo_pixels(self.area.cget(option))
                    for option in EDGE_OPTIONS)
        return self.tags.table_columns(width - 2 * edges, depth)

    def relayout(self) -> None:
        """Lay the tables of the note out again, if the room has changed.

        A note without tables is left alone, as are tables that fit
        as many letters as they did, because drawing a note again
        reads its images again. The note is scrolled to where it was.
        """
        has_table = any(block.table is not None
                        for block in self.drawn.blocks)
        if not has_table or self.table_columns(0) == self.drawn.columns:
            return
        top = self.area.yview()[0]
        self._draw_blocks()
        self.area.yview_moveto(top)

    def _resized(self, _event: 'tkinter.Event[tkinter.Text]') -> None:
        """Fit the tables of the note to the area as it is now sized."""
        self.relayout()

    def _write_gap(self, block: Block, previous: Optional[Block]) -> None:
        """Leave room above a piece of a note that follows another."""
        lines = '\n' * gap_lines(block, previous)
        if lines:
            self.area.insert(tkinter.END, lines, GAP_TAG)

    def _write_block(self, block: Block) -> None:
        """Write one piece of a note with the tags it is drawn with."""
        indent = indent_tag(block)
        columns = self.table_columns(block.indent)
        for span in block_spans(block, columns):
            self._write_span(block.kind, span, indent)
        self.area.insert(tkinter.END, '\n', (str(block.kind), indent))

    def _write_span(self, kind: BlockKind, span: Span, indent: str) \
            -> None:
        """Write one run of text of a piece of a note.

        An image is drawn where its file can be drawn, and is named
        by its description where it cannot, so that a note always
        says what belongs where the image is.
        """
        picture = self._picture(span) if SpanStyle.IMAGE in span.styles \
            else None
        if picture is not None:
            self._draw_picture(picture, indent)
        else:
            self._write_text(kind, span, indent)

    def _write_text(self, kind: BlockKind, span: Span, indent: str) \
            -> None:
        """Write the text of one run of text, image and all."""
        text = image_text(span) if SpanStyle.IMAGE in span.styles \
            else span.text
        tags = self.tags.span_tags(kind, span, indent)
        self.area.insert(tkinter.END, text, tags)

    def _draw_picture(self, picture: tkinter.PhotoImage, indent: str) \
            -> None:
        """Draw a picture where the note shows it, indented as it is."""
        start = self.area.index(tkinter.END)
        self.area.image_create(tkinter.END, image=picture, padx=IMAGE_PADDING,
                               pady=IMAGE_PADDING)
        self.area.tag_add(indent, start, tkinter.END)

    def _picture(self, span: Span) -> Optional[tkinter.PhotoImage]:
        """Return the picture of an image of the note, None for none.

        Tk reads PNG and GIF files of its own, and every other file
        is named rather than drawn. The pictures of the note are
        kept while it is shown, because Tk draws a picture that is
        nothing but the tag of an image no longer.
        """
        path = image_path(self.drawn.folder, span.target)
        if path is None:
            return None
        try:
            picture = tkinter.PhotoImage(master=self.area, file=path)
        except tkinter.TclError:
            return None
        fitted = self._fitted(picture)
        self.drawn.pictures.append(fitted)
        return fitted

    def _fitted(self, picture: tkinter.PhotoImage) -> tkinter.PhotoImage:
        """Return a picture drawn small enough to be read in the panel."""
        factor = shrink_factor(picture.width())
        return picture if factor == 1 else picture.subsample(factor)

    def zoom(self, step: int) -> None:
        """Draw the note so many steps larger, or smaller below zero."""
        self.tags.zoom(step)
        self.relayout()

    def zoom_normal(self) -> None:
        """Draw the note in the size that it started out in."""
        self.tags.normal_size()
        self.relayout()

    def shown_note(self) -> NoteText:
        """Return the note that is shown, warning and all."""
        return self.note

    def area_text(self) -> str:
        """Return the text that the area holds, as the user sees it.

        Tk keeps a newline of its own at the end of a text area,
        which is left out here, so that what is returned is what was
        put in.
        """
        return str(self.area.get('1.0', 'end-1c'))

    def selected_text(self) -> str:
        """Return what the user has selected of the note, empty for none."""
        if not self.area.tag_ranges(tkinter.SEL):
            return ''
        return str(self.area.get(tkinter.SEL_FIRST, tkinter.SEL_LAST))

    def warning_shown(self) -> bool:
        """Return whether a warning is on the screen above the note."""
        return bool(self.warning.winfo_manager())
