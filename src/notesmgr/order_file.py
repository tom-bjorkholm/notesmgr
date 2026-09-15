#! /usr/local/bin/python3
"""The file that keeps the notes of a folder in their order."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, Sequence
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import SEPARATORS, sorted_names

ORDER_NAME = '.notes_order.txt'
"""Name of the hidden file that orders the notes of a folder."""

WRITING_NAME = ORDER_NAME + '.new'
"""Name a new note order is written under until it is whole."""

NOT_READ = 'The note order of {folder} cannot be read.\n{reason}'
"""What is said about a note order file that cannot be read."""

NOT_WRITTEN = 'The note order of {folder} cannot be written.\n{reason}'
"""What is said about a note order file that cannot be written."""


def order_path(folder: Path) -> Path:
    """Return the file that holds the note order of a folder."""
    return folder / ORDER_NAME


def read_order_text(folder: Path) -> Optional[str]:
    """Return the note order file of a folder, None when it has none.

    Args:
        folder: Folder of a project.

    Returns:
        The text of the order file, None when there is no order file.

    Raises:
        NotesmgrError: There is an order file, and it cannot be read.
    """
    path = order_path(folder)
    if not path.is_file():
        return None
    try:
        return path.read_text(encoding='utf-8-sig', errors='replace')
    except OSError as error:
        raise NotesmgrError(NOT_READ.format(folder=folder,
                                            reason=error)) from error


def names_a_file(name: str) -> bool:
    """Return whether a line of an order file can name a file at all."""
    return name not in ('.', '..') and \
        not any(separator in name for separator in SEPARATORS)


def parse_order(text: str) -> list[str]:
    """Return the file names that a note order file holds, in its order.

    The file is written by hand as often as by notesmgr, so a byte
    order mark, line endings of any kind, blank lines, blanks around a
    name and a name given twice are all taken for what they meant.
    A line that can name no file in the folder is left out.

    Args:
        text: The text of the order file.

    Returns:
        The names it holds, each of them once.
    """
    names: list[str] = []
    for line in text.splitlines():
        name = line.strip()
        if name and names_a_file(name) and name not in names:
            names.append(name)
    return names


def repair_order(listed: Sequence[str], existing: Sequence[str]) -> list[str]:
    """Return the order in which the notes of a folder are shown.

    Notes that are gone are dropped, and notes that the order file
    does not mention are added at the end in alphabetical order, so
    that what another program did to the folder is taken up rather
    than making the order file worth nothing.

    Args:
        listed: The names that the order file holds, in its order.
        existing: The names of the notes really in the folder.

    Returns:
        Every existing note once, in the order it is shown in.
    """
    present = set(existing)
    kept = [name for name in listed if name in present]
    return kept + sorted_names(present.difference(kept))


def order_text(names: Sequence[str]) -> str:
    """Return what a note order file holding these names looks like."""
    return ''.join(f'{name}\n' for name in names)


def write_order(folder: Path, text: str) -> None:
    """Write the note order file of a folder, replacing the old one.

    The text is written to a file of its own and put in the place of
    the order file only once it is whole, so that a program that stops
    in the middle leaves the old order rather than half of a new one.

    Args:
        folder: Folder of a project.
        text: What the order file is to hold.

    Raises:
        NotesmgrError: The order file cannot be written.
    """
    written = folder / WRITING_NAME
    try:
        written.write_text(text, encoding='utf-8', newline='\n')
        written.replace(order_path(folder))
    except OSError as error:
        raise NotesmgrError(NOT_WRITTEN.format(folder=folder,
                                               reason=error)) from error


def repair_order_file(folder: Path, existing: Sequence[str]) -> list[str]:
    """Return the note order of a folder, repairing what needs repair.

    The file is written only when the repair changed something, so
    that opening a project leaves the folders that were in order as
    untouched as it found them.

    Args:
        folder: Folder of a project.
        existing: The names of the notes really in the folder.

    Returns:
        Every existing note once, in the order it is shown in.

    Raises:
        NotesmgrError: The order file cannot be read or written.
    """
    found = read_order_text(folder)
    order = repair_order(parse_order(found or ''), existing)
    text = order_text(order)
    if found != text:
        write_order(folder, text)
    return order
