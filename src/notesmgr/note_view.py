#! /usr/local/bin/python3
"""The area of the main window that a note is read in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import contextmanager
from pathlib import Path
from tkinter import ttk
from typing import Iterator, Optional, Sequence
from notesmgr.note_blocks import Block, BlockKind, Span, SpanStyle, \
    markdown_blocks
from notesmgr.note_image import image_path, shrink_factor
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


def block_spans(block: Block) -> tuple[Span, ...]:
    """Return everything that is written for one piece of a note.

    The bullet or the number of a list item and the line of a rule
    are drawn rather than read, so they are written here and are no
    part of what the note holds.

    Args:
        block: The piece of the note that is to be written.

    Returns:
        The runs of text to write, in the order they are written in.
    """
    if block.kind is BlockKind.RULE:
        return (Span(RULE_TEXT),)
    if block.prefix:
        return (Span(block.prefix), *block.spans)
    return block.spans


def image_text(span: Span) -> str:
    """Return how an image is named where the image is not drawn."""
    return IMAGE_TEXT.format(alt=span.text or MISSING_ALT)


class NoteView:
    """Shows the text of one note, with any warning above it.

    The warning is what could not be shown and why, and it is left
    out of the way whenever there is nothing to warn about. A note
    written in markdown is shown formatted for reading, and every
    other note is shown as it is written.
    """

    def __init__(self, parent: tkinter.Misc) -> None:
        """Build the area in a frame of its own inside a parent widget."""
        self.frame = ttk.Frame(parent)
        self.warning = ttk.Label(self.frame, foreground=WARNING_COLOUR,
                                 font=WARNING_FONT, justify=tkinter.LEFT,
                                 wraplength=WRAP_WIDTH)
        self.area = tkinter.Text(self.frame, wrap=tkinter.WORD,
                                 state=tkinter.DISABLED)
        self.tags = NoteTags(self.area)
        self.note = EMPTY_NOTE
        self.folder: Optional[Path] = None
        self.pictures: list[tkinter.PhotoImage] = []
        self._lay_out()

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
        self.folder = folder
        self.pictures = []
        previous: Optional[Block] = None
        with self._writing():
            for block in blocks:
                self._write_gap(block, previous)
                self._write_block(block)
                previous = block

    def _write_gap(self, block: Block, previous: Optional[Block]) -> None:
        """Leave room above a piece of a note that follows another."""
        lines = '\n' * gap_lines(block, previous)
        if lines:
            self.area.insert(tkinter.END, lines, GAP_TAG)

    def _write_block(self, block: Block) -> None:
        """Write one piece of a note with the tags it is drawn with."""
        indent = indent_tag(block)
        for span in block_spans(block):
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
        path = image_path(self.folder, span.target)
        if path is None:
            return None
        try:
            picture = tkinter.PhotoImage(master=self.area, file=path)
        except tkinter.TclError:
            return None
        drawn = self._fitted(picture)
        self.pictures.append(drawn)
        return drawn

    def _fitted(self, picture: tkinter.PhotoImage) -> tkinter.PhotoImage:
        """Return a picture drawn small enough to be read in the panel."""
        factor = shrink_factor(picture.width())
        return picture if factor == 1 else picture.subsample(factor)

    def zoom(self, step: int) -> None:
        """Draw the note so many steps larger, or smaller below zero."""
        self.tags.zoom(step)

    def zoom_normal(self) -> None:
        """Draw the note in the size that it started out in."""
        self.tags.normal_size()

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

    def warning_shown(self) -> bool:
        """Return whether a warning is on the screen above the note."""
        return bool(self.warning.winfo_manager())
