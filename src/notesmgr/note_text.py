#! /usr/local/bin/python3
"""Reading the text of a note, and what cannot be read of it."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple

NOT_UTF8 = 'This note is not UTF-8 text, and is therefore not shown.\n' \
    'Editing it in an editor that writes UTF-8 makes it readable here.'
"""What is said about a note that holds bytes that are no text."""

NOT_READ = 'This note cannot be read.\n{reason}'
"""What is said about a note that the file system does not give."""

TOO_LONG = 'Only the first {limit} characters of this note are shown.\n' \
    'The configuration member max_note_size says how many that is.'
"""What is said about a note that is longer than may be shown."""


class NoteText(NamedTuple):
    """The text of a note, and what is to be said about it.

    The warning is what the user is told above the text, and it is
    empty when there is nothing to tell. A note that cannot be shown
    at all has a warning and no text.
    """

    text: str
    warning: str = ''


EMPTY_NOTE = NoteText('')
"""What is shown when nothing at all is selected."""


def read_note_text(path: Path, limit: int) -> NoteText:
    """Return the text of a note, as much of it as may be shown.

    One character more than the limit is read, which is what tells a
    note that fits from one that has to be cut, without reading a
    note of any size into memory. Reading characters rather than
    bytes is also what keeps the cut from falling inside a character.

    Args:
        path: The note to read.
        limit: The most characters of it that may be shown.

    Returns:
        The text to show and the warning to show above it.
    """
    try:
        with path.open(encoding='utf-8') as note:
            read = note.read(limit + 1)
    except UnicodeDecodeError:
        return NoteText('', NOT_UTF8)
    except OSError as error:
        return NoteText('', NOT_READ.format(reason=error))
    if len(read) > limit:
        return NoteText(read[:limit], TOO_LONG.format(limit=limit))
    return NoteText(read)
