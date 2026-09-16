#! /usr/local/bin/python3
"""The formatted copy of a note, and where each platform puts it."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import re
import sys
from functools import partial
from html import escape, unescape
from pathlib import Path
from typing import Callable, Mapping, Optional
from notesmgr import clipboard_linux, clipboard_macos, clipboard_windows
from notesmgr.clipboard_tool import RichText
from notesmgr.markdown_render import note_html
from notesmgr.note_image import image_path

PLAIN = '<pre>{text}</pre>'
"""How a note that is no markdown is written for a formatted copy.

Such a note is shown in the fixed width font and exactly as it is
written, so the copy of it keeps its own line breaks and the columns
of a table that was lined up by hand.
"""

IMAGE_SOURCE = re.compile(r'(<img[^>]*\ssrc=")([^"]*)(")')
"""What names the file of an image in the HTML of a note."""

BACKENDS: Mapping[str, Callable[[RichText], None]] = {
    'darwin': clipboard_macos.copy_to_clipboard,
    'win32': clipboard_windows.copy_to_clipboard}
"""What puts a formatted copy on the clipboard of each platform.

Every other platform is taken to be a desktop of X11 or of Wayland,
which is what Linux and the BSDs have.
"""


def absolute_source(folder: Optional[Path], match: re.Match[str]) -> str:
    """Return one image of a note naming its file wherever it is read.

    A copy is pasted somewhere else than into the folder of the note,
    so an image that the note names beside itself is named by its
    whole path instead. An image that is on the network, or that
    names no file that can be found from where the note stands, is
    left exactly as the note wrote it.

    Args:
        folder: The folder that holds the note, None when the note
            is copied from nowhere in particular.
        match: The image of the HTML that is being named again.

    Returns:
        The image as the copy of the note is to hold it.
    """
    path = image_path(folder, unescape(match.group(2)))
    if path is None or not path.is_absolute():
        return match.group(0)
    return match.group(1) + escape(path.as_uri()) + match.group(3)


def local_images(html: str, folder: Optional[Path]) -> str:
    """Return HTML in which every image beside the note names its file."""
    return IMAGE_SOURCE.sub(partial(absolute_source, folder), html)


def note_fragment(text: str, markdown: bool,
                  folder: Optional[Path] = None) -> str:
    """Return the HTML that a formatted copy of a note is made of.

    Args:
        text: The note, as much of it as is shown.
        markdown: Whether the note is written in markdown, and is
            therefore formatted rather than kept as it is written.
        folder: The folder that holds the note, which is what an
            image that the note shows is named from.

    Returns:
        The HTML of the note, as it goes inside a body.
    """
    if not markdown:
        return PLAIN.format(text=escape(text))
    return local_images(note_html(text), folder)


def note_rich_text(text: str, markdown: bool,
                   folder: Optional[Path] = None) -> RichText:
    """Return a copy of a note in the shapes a clipboard takes it in."""
    return RichText(note_fragment(text, markdown, folder), text)


def backend() -> Callable[[RichText], None]:
    """Return what puts a formatted copy on the clipboard here."""
    return BACKENDS.get(sys.platform, clipboard_linux.copy_to_clipboard)


def copy_rich(payload: RichText) -> None:
    """Put a formatted copy of a note on the clipboard of the system.

    Args:
        payload: The copy to put there.

    Raises:
        NotesmgrError: The system has no way of taking a formatted
            copy, or the way it has did not take this one.
    """
    backend()(payload)
