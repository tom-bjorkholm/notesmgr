#! /usr/local/bin/python3
"""Putting a formatted copy of a note on the clipboard of a desktop."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
from typing import Optional, Sequence
from notesmgr.clipboard_tool import RichText, run_tool
from notesmgr.errors import NotesmgrError

XCLIP = ('xclip', '-selection', 'clipboard', '-t', 'text/html')
"""What puts HTML on the clipboard of an X11 desktop."""

WL_COPY = ('wl-copy', '-t', 'text/html')
"""What puts HTML on the clipboard of a Wayland desktop."""

TOOLS = (XCLIP, WL_COPY)
"""The programs that can take a formatted copy, the first one first.

A Wayland desktop usually answers for X11 programs as well, so the
one that works on both is the one that is tried first.
"""

NO_TOOL = 'Neither xclip nor wl-copy is installed, and one of them is ' \
    'what puts formatted text on the clipboard of this desktop.'
"""What is said when the desktop has neither of the two programs."""

CHARSET = '<meta charset="utf-8">'
"""What says that the HTML of a copy is written as UTF-8."""


def html_tool() -> Optional[Sequence[str]]:
    """Return the program that takes a formatted copy, None for none."""
    return next((tool for tool in TOOLS
                 if shutil.which(tool[0]) is not None), None)


def copy_to_clipboard(payload: RichText) -> None:
    """Put a formatted copy of a note on the clipboard of a desktop.

    The clipboard of X11 and of Wayland is owned by a program rather
    than held by the system, and the program that owns it offers the
    one shape it was given, so the formatted shape is what is put
    there. That program goes on running to answer for the clipboard,
    and is therefore not waited for.

    Args:
        payload: The copy to put there.

    Raises:
        NotesmgrError: The desktop has no program that takes a
            formatted copy, or the one it has refused this copy.
    """
    tool = html_tool()
    if tool is None:
        raise NotesmgrError(NO_TOOL)
    run_tool(tool, (CHARSET + payload.html).encode('utf-8'), capture=False)
