#! /usr/local/bin/python3
"""Putting a formatted copy of a note on the clipboard of Windows."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import ctypes
import sys
from typing import Sequence
from notesmgr.clipboard_tool import RichText
from notesmgr.errors import NotesmgrError

HEADER = 'Version:0.9\r\nStartHTML:{start:010d}\r\nEndHTML:{end:010d}\r\n' \
    'StartFragment:{first:010d}\r\nEndFragment:{last:010d}\r\n'
"""What says where the pieces of an HTML Format payload begin and end.

Every number is a count of bytes from the very start of the payload,
written with as many digits as it can ever need, so that filling the
numbers in does not move what they point at.
"""

OPENING = '<html><body>\r\n<!--StartFragment-->'
"""What stands before the piece of the payload that is pasted."""

CLOSING = '<!--EndFragment-->\r\n</body></html>'
"""What stands after the piece of the payload that is pasted."""

HTML_FORMAT = 'HTML Format'
"""What the clipboard of Windows calls the shape that keeps markup."""

UNICODE_TEXT = 13
"""What the clipboard of Windows calls plain text, as CF_UNICODETEXT."""

MOVEABLE = 0x0002
"""How memory that is handed over to the clipboard is allocated."""

NOT_WINDOWS = 'This is the clipboard of Microsoft Windows, and this is ' \
    'no Microsoft Windows.'
"""What is said when the clipboard of Windows is asked for elsewhere."""

NOT_OPENED = 'The clipboard is held by another program just now.'
"""What is said when the clipboard could not be opened at all."""

NO_MEMORY = 'There is not memory enough to copy the note.'
"""What is said when the memory for a copy could not be had."""

NOT_TAKEN = 'The clipboard did not take the copy of the note.'
"""What is said when the clipboard refused a shape of the copy."""


def byte_length(text: str) -> int:
    """Return how many bytes a text is when it is written as UTF-8."""
    return len(text.encode('utf-8'))


def cf_html(fragment: str) -> str:
    """Return the HTML Format payload that Windows takes a copy in.

    The header says where the document begins and ends and where the
    piece of it that is pasted begins and ends. All four are counted
    in bytes rather than in characters, so a note holding anything
    but plain ASCII is counted as the UTF-8 that it is written as.

    Args:
        fragment: The HTML of the note, as it goes inside a body.

    Returns:
        The payload, header and document together.
    """
    head = byte_length(HEADER.format(start=0, end=0, first=0, last=0))
    first = head + byte_length(OPENING)
    last = first + byte_length(fragment)
    return HEADER.format(start=head, end=last + byte_length(CLOSING),
                         first=first, last=last) + OPENING + fragment + \
        CLOSING


def html_bytes(fragment: str) -> bytes:
    """Return the formatted shape of a copy as Windows holds it."""
    return cf_html(fragment).encode('utf-8') + b'\0'


def text_bytes(text: str) -> bytes:
    """Return the plain shape of a copy as Windows holds it."""
    return text.encode('utf-16-le') + b'\0\0'


def declare_memory(kernel32: ctypes.CDLL) -> None:
    """Tell ctypes what the functions that hand out memory take."""
    kernel32.GlobalAlloc.restype = ctypes.c_void_p
    kernel32.GlobalAlloc.argtypes = [ctypes.c_uint, ctypes.c_size_t]
    kernel32.GlobalLock.restype = ctypes.c_void_p
    kernel32.GlobalLock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalUnlock.argtypes = [ctypes.c_void_p]
    kernel32.GlobalFree.argtypes = [ctypes.c_void_p]


def moveable_memory(kernel32: ctypes.CDLL, data: bytes) -> int:
    """Return a handle to memory holding the given bytes.

    The clipboard takes over the memory it is given, so what is
    allocated here is moveable, as the clipboard asks, and is not
    freed again by notesmgr once the clipboard has it. Memory that
    was had but could not be written to is freed here instead.

    Args:
        kernel32: The library of Windows that hands out memory.
        data: What the memory is to hold.

    Returns:
        The handle to give to the clipboard.

    Raises:
        NotesmgrError: The memory could not be had or written to.
    """
    declare_memory(kernel32)
    handle = kernel32.GlobalAlloc(MOVEABLE, len(data))
    if not handle:
        raise NotesmgrError(NO_MEMORY)
    place = kernel32.GlobalLock(handle)
    if not place:
        kernel32.GlobalFree(handle)
        raise NotesmgrError(NO_MEMORY)
    ctypes.memmove(place, data, len(data))
    kernel32.GlobalUnlock(handle)
    return int(handle)


def hand_over(user32: ctypes.CDLL, kernel32: ctypes.CDLL, named: int,
              data: bytes) -> None:
    """Give one shape of a copy to the clipboard, which then owns it.

    Memory that the clipboard did not take is still notesmgr's own,
    and is freed again rather than left behind.

    Args:
        user32: The library of Windows that owns the clipboard.
        kernel32: The library of Windows that hands out memory.
        named: What the clipboard calls the shape.
        data: What the shape holds.

    Raises:
        NotesmgrError: The memory for the shape could not be had, or
            the clipboard did not take it.
    """
    handle = moveable_memory(kernel32, data)
    if not user32.SetClipboardData(named, handle):
        kernel32.GlobalFree(handle)
        raise NotesmgrError(NOT_TAKEN)


def write_clipboard(user32: ctypes.CDLL, kernel32: ctypes.CDLL,
                    shapes: Sequence[tuple[int, bytes]]) -> None:
    """Put every shape of one copy on the clipboard in one session.

    The clipboard is emptied once and then filled with every shape,
    because opening it a second time would take away what the first
    session put there.

    Args:
        user32: The library of Windows that owns the clipboard.
        kernel32: The library of Windows that hands out memory.
        shapes: What each shape of the copy is called and holds.

    Raises:
        NotesmgrError: The clipboard could not be opened, the memory
            for a shape could not be had, or the clipboard did not
            take a shape.
    """
    user32.SetClipboardData.restype = ctypes.c_void_p
    user32.SetClipboardData.argtypes = [ctypes.c_uint, ctypes.c_void_p]
    if not user32.OpenClipboard(None):
        raise NotesmgrError(NOT_OPENED)
    try:
        user32.EmptyClipboard()
        for named, data in shapes:
            hand_over(user32, kernel32, named, data)
    finally:
        user32.CloseClipboard()


def copy_to_clipboard(payload: RichText) -> None:
    """Put a formatted copy of a note on the clipboard of Windows.

    Args:
        payload: The copy to put there.

    Raises:
        NotesmgrError: This is no Windows, or Windows did not take
            the copy.
    """
    if sys.platform != 'win32':
        raise NotesmgrError(NOT_WINDOWS)
    user32 = ctypes.windll.user32
    named = user32.RegisterClipboardFormatW(HTML_FORMAT)
    write_clipboard(user32, ctypes.windll.kernel32,
                    ((named, html_bytes(payload.html)),
                     (UNICODE_TEXT, text_bytes(payload.text))))
