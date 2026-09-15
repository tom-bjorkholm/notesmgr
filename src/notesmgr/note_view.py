#! /usr/local/bin/python3
"""The area of the main window that a note is read in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from tkinter import ttk
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


class NoteView:
    """Shows the text of one note, with any warning above it.

    The warning is what could not be shown and why, and it is left
    out of the way whenever there is nothing to warn about. The text
    is shown as it is read, because what a note looks like formatted
    is what step 7 of the plan adds.
    """

    def __init__(self, parent: tkinter.Misc) -> None:
        """Build the area in a frame of its own inside a parent widget."""
        self.frame = ttk.Frame(parent)
        self.warning = ttk.Label(self.frame, foreground=WARNING_COLOUR,
                                 font=WARNING_FONT, justify=tkinter.LEFT,
                                 wraplength=WRAP_WIDTH)
        self.area = tkinter.Text(self.frame, wrap=tkinter.WORD,
                                 state=tkinter.DISABLED)
        self.note = EMPTY_NOTE
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

    def show(self, note: NoteText) -> None:
        """Show a note that was read, warning and all.

        Args:
            note: The text to show and the warning to show above it.
        """
        self.note = note
        self.show_warning(note.warning)
        self.show_text(note.text)

    def show_warning(self, warning: str) -> None:
        """Show a warning above the note, and none when there is none."""
        self.warning.configure(text=warning)
        if warning:
            self.warning.grid()
        else:
            self.warning.grid_remove()

    def show_text(self, text: str) -> None:
        """Show a text in an area that the user cannot type in."""
        self.area.configure(state=tkinter.NORMAL)
        self.area.delete('1.0', tkinter.END)
        self.area.insert('1.0', text)
        self.area.configure(state=tkinter.DISABLED)

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
