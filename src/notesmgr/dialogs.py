#! /usr/local/bin/python3
"""Windows that notesmgr shows over a window of its own."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import contextmanager
from tkinter import messagebox, ttk
from typing import Iterator, Union

MIN_TEXT_WIDTH = 40
"""Narrowest that a window showing a text is made, in characters."""

MAX_TEXT_WIDTH = 100
"""Widest that a window showing a text is made, in characters."""

MAX_TEXT_HEIGHT = 30
"""Tallest that a window showing a text is made, in lines."""

CLOSE_LABEL = 'Close'
"""What the button that closes a shown text says."""

PADDING = 8
"""Space in pixels left around the button of a shown text."""

BUSY_CURSOR = 'watch'
"""Mouse cursor shown while an answer is being gathered."""


def text_size(text: str) -> tuple[int, int]:
    """Return the width and height in characters that a text needs.

    A window is never made narrower than a short line nor wider or
    taller than a screen comfortably holds, so a very long line or a
    very long text is scrolled to instead of being shown whole.

    Args:
        text: The text that is going to be shown.

    Returns:
        The width in characters and the height in lines.
    """
    lines = text.splitlines() or ['']
    widest = max(len(line) for line in lines)
    width = min(max(widest, MIN_TEXT_WIDTH), MAX_TEXT_WIDTH)
    return width, min(len(lines), MAX_TEXT_HEIGHT)


def show_text(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              text: str) -> tkinter.Toplevel:
    """Show a text that cannot be edited, over another window.

    Args:
        parent: The window that the new window is shown over.
        title: What the new window is called.
        text: What the new window shows.

    Returns:
        The window that was made, which its own button destroys.
    """
    window = tkinter.Toplevel(parent)
    window.title(title)
    window.transient(parent)
    _fill_with_text(window, text)
    return window


def _fill_with_text(window: tkinter.Toplevel, text: str) -> None:
    """Fill a window with a text, a scroll bar and a close button."""
    width, height = text_size(text)
    area = tkinter.Text(window, width=width, height=height, wrap='none',
                        font='TkFixedFont')
    scroll = ttk.Scrollbar(window, orient=tkinter.VERTICAL, command=area.yview)
    area.configure(yscrollcommand=scroll.set)
    area.insert('1.0', text)
    area.configure(state=tkinter.DISABLED)
    button = ttk.Button(window, text=CLOSE_LABEL, command=window.destroy)
    button.pack(side=tkinter.BOTTOM, pady=PADDING)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    area.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)


def show_error(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               message: str) -> None:
    """Tell the user what went wrong, in a window of its own.

    Args:
        parent: The window that the message is shown over.
        title: What the message window is called.
        message: What went wrong.
    """
    messagebox.showerror(title=title, message=message, parent=parent)


@contextmanager
def busy_cursor(window: Union[tkinter.Tk, tkinter.Toplevel]) -> Iterator[None]:
    """Show the waiting cursor while something slow is being done.

    Args:
        window: The window that is going to be busy.

    Yields:
        Nothing. The cursor is put back when the block has ended,
        whether it ended by finishing or by raising.
    """
    window.configure(cursor=BUSY_CURSOR)
    window.update_idletasks()
    try:
        yield
    finally:
        window.configure(cursor='')
