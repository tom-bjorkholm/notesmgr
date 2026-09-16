#! /usr/local/bin/python3
"""Putting a formatted copy of a note on the pasteboard of macOS."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from tempfile import TemporaryDirectory
from notesmgr.clipboard_tool import RichText, run_tool

TEXTUTIL = ('textutil', '-stdin', '-format', 'html', '-inputencoding',
            'UTF-8', '-convert', 'rtf', '-stdout')
"""What turns the HTML of a note into the rich text that macOS pastes.

It is part of macOS itself, so a formatted copy costs notesmgr no
dependency of its own.
"""

SCRIPT = """on run argv
set rtf_path to POSIX file (item 1 of argv)
set txt_path to POSIX file (item 2 of argv)
set rtf_data to read rtf_path as «class RTF »
set plain_text to read txt_path as «class utf8»
set the clipboard to {«class RTF »:rtf_data, string:plain_text}
end run"""
"""What puts both shapes of a copy on the pasteboard in one write.

A second write would replace the first, so the rich text and the
plain text are given to the pasteboard together. They are read from
files rather than written into the script itself, because a note is
longer than a command line may be.

The names here are of two words each because AppleScript knows a
great many words of one: a variable called plain, for one, is a
term of the language already, and setting it is refused.
"""

OSASCRIPT = ('osascript', '-e', SCRIPT)
"""What runs that script, with the two files as its arguments."""

RTF_NAME = 'note.rtf'
"""What the file holding the rich text of a copy is called."""

TEXT_NAME = 'note.txt'
"""What the file holding the plain text of a copy is called."""


def written(folder: Path, name: str, data: bytes) -> str:
    """Write one shape of a copy into a folder, and name the file.

    Args:
        folder: The folder that the file is written into.
        name: What the file is to be called.
        data: What the file is to hold.

    Returns:
        The file, named as the script that reads it names it.
    """
    path = folder / name
    path.write_bytes(data)
    return str(path)


def copy_to_clipboard(payload: RichText) -> None:
    """Put a formatted copy of a note on the pasteboard of macOS.

    Args:
        payload: The copy to put there.

    Raises:
        NotesmgrError: macOS did not take the copy.
    """
    rich = run_tool(TEXTUTIL, payload.html.encode('utf-8'))
    with TemporaryDirectory() as made:
        folder = Path(made)
        argv = (*OSASCRIPT, written(folder, RTF_NAME, rich),
                written(folder, TEXT_NAME, payload.text.encode('utf-8')))
        run_tool(argv, b'')
