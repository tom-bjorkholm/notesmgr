#! /usr/local/bin/python3
"""Making, copying, moving and taking away the notes of a project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
from pathlib import Path
from typing import Sequence
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import note_file_name, template_name
from notesmgr.order_file import order_text, repair_order_file, write_order
from notesmgr.project import folder_content, folder_entries
from notesmgr.trash import send_to_trash

NAME_TAKEN = 'The folder {folder} holds a file called {name} already.'
"""What is said about a name that is another file's name already."""

NOT_WRITTEN = 'The note {path} cannot be written.\n{reason}'
"""What is said about a note that the file system would not take."""

NOT_COPIED = 'The note {path} cannot be copied.\n{reason}'
"""What is said about a note that could not be copied."""

NOT_TRASHED = 'The note {path} cannot be moved to the trash.\n{reason}'
"""What is said about a note that the trash would not take."""


def resync_order(folder: Path) -> list[str]:
    """Return the notes of a folder, bringing its order file in line.

    The notes of a folder change under its order file whenever one is
    made, copied or taken away, and the repair that opening a project
    does is exactly what is wanted then, so it is done here as well.

    Args:
        folder: The folder whose notes have changed.

    Returns:
        The notes of the folder, in the order they are shown in.

    Raises:
        NotesmgrError: The folder or its order file cannot be read,
            or the order file cannot be written.
    """
    return repair_order_file(folder, folder_content(folder).notes)


def free_path(folder: Path, name: str) -> Path:
    """Return the file that a name asks for, refusing a taken name.

    Two names that differ only in case are one file on macOS and on
    Windows, so a name is taken when the folder holds any name equal
    to it but for its case, whatever this file system makes of it.

    Args:
        folder: The folder that the file is to be in.
        name: The name of the file, extension and all.

    Returns:
        The file to write, which is not there yet.

    Raises:
        NotesmgrError: The folder holds a file of that name already,
            or the folder cannot be read.
    """
    taken = {path.name.casefold() for path in folder_entries(folder)}
    if name.casefold() in taken:
        raise NotesmgrError(NAME_TAKEN.format(folder=folder, name=name))
    return folder / name


def new_path(folder: Path, typed: str, extension: NoteExtension) -> Path:
    """Return the note file that a typed name asks for in a folder.

    Args:
        folder: The folder that the note is to be in.
        typed: What the user typed as the name of the note.
        extension: The extension that the notes of the project have.

    Returns:
        The note file to write, which is not there yet.

    Raises:
        NotesmgrError: The name names no note of this project, or it
            is the name of a file that is there already.
    """
    return free_path(folder, note_file_name(typed, extension))


def template_text(folder: Path, extension: NoteExtension) -> str:
    """Return what a new note in a folder starts out holding.

    That is the template of the folder, and nothing at all when the
    folder holds no template that can be read, which is no reason to
    refuse to make the note.

    Args:
        folder: The folder that the new note is made in.
        extension: The extension that the notes of the project have.

    Returns:
        The text that the new note starts out holding.
    """
    template = folder / template_name(extension)
    try:
        return template.read_text(encoding='utf-8')
    except (OSError, UnicodeDecodeError):
        return ''


def new_note(folder: Path, typed: str, extension: NoteExtension) -> Path:
    """Make a note in a folder, holding what its template holds.

    Args:
        folder: The folder that the note is made in.
        typed: What the user typed as the name of the note.
        extension: The extension that the notes of the project have.

    Returns:
        The note that was made.

    Raises:
        NotesmgrError: The name names no note that can be made here,
            or the note or the note order cannot be written.
    """
    path = new_path(folder, typed, extension)
    try:
        path.write_text(template_text(folder, extension), encoding='utf-8')
    except OSError as error:
        raise NotesmgrError(NOT_WRITTEN.format(path=path,
                                               reason=error)) from error
    resync_order(folder)
    return path


def duplicate_note(note: Path, folder: Path, typed: str,
                   extension: NoteExtension) -> Path:
    """Copy a note into a folder of the project under another name.

    Args:
        note: The note to copy.
        folder: The folder that the copy is made in, which is any
            folder of the project and not only the note's own.
        typed: What the user typed as the name of the copy.
        extension: The extension that the notes of the project have.

    Returns:
        The copy that was made.

    Raises:
        NotesmgrError: The name names no note that can be made here,
            or the copy or the note order cannot be written.
    """
    path = new_path(folder, typed, extension)
    try:
        shutil.copyfile(note, path)
    except OSError as error:
        raise NotesmgrError(NOT_COPIED.format(path=note,
                                              reason=error)) from error
    resync_order(folder)
    return path


def delete_note(note: Path) -> None:
    """Move a note to the trash, and out of the order of its folder.

    Args:
        note: The note to take away.

    Raises:
        NotesmgrError: The trash would not take the note, or the note
            order cannot be written.
    """
    send_to_trash(note, NOT_TRASHED)
    resync_order(note.parent)


def moved_order(names: Sequence[str], name: str, offset: int) -> list[str]:
    """Return an order with one of its notes moved so many places.

    A note at the first place cannot be moved further up and one at
    the last place cannot be moved further down, so it stays where it
    is rather than moving round the end of the folder.

    Args:
        names: The notes of a folder, in the order they are shown in.
        name: The note to move, which may be none of them.
        offset: How many places to move it, up being negative.

    Returns:
        The order as it is after the move.
    """
    moved = list(names)
    if name not in moved:
        return moved
    was = moved.index(name)
    now = min(max(was + offset, 0), len(moved) - 1)
    moved.insert(now, moved.pop(was))
    return moved


def move_note(note: Path, offset: int) -> Path:
    """Move a note so many places in the order of its folder.

    Args:
        note: The note to move.
        offset: How many places to move it, up being negative.

    Returns:
        The note, which is where it now stands in its folder.

    Raises:
        NotesmgrError: The folder or its order file cannot be read,
            or the order file cannot be written.
    """
    folder = note.parent
    order = resync_order(folder)
    moved = moved_order(order, note.name, offset)
    if moved != order:
        write_order(folder, order_text(moved))
    return note
