#! /usr/local/bin/python3
"""Making, renaming and taking away the folders of a project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Iterator, NamedTuple
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import checked_name, is_plain_note, template_name
from notesmgr.note_ops import free_path, resync_order, template_text
from notesmgr.order_file import ORDER_NAME
from notesmgr.project import folder_entries, is_project, is_shown_folder
from notesmgr.trash import send_to_trash

IS_PROJECT = 'The folder {folder} is the project itself.'
"""What is said about the root folder, which is no folder to change."""

NOT_EMPTY = 'The folder {folder} holds notes or folders of its own.'
"""What is said about a folder that is not to be taken away yet."""

NOT_MADE = 'The folder {path} cannot be made.\n{reason}'
"""What is said about a folder that the file system would not take."""

NOT_RENAMED = 'The folder {path} cannot be renamed.\n{reason}'
"""What is said about a folder that could not be given its new name."""

NOT_TRASHED = 'The folder {path} cannot be moved to the trash.\n{reason}'
"""What is said about a folder that the trash would not take."""

NOT_MOVED = 'The folder {path} cannot be moved.\n{reason}'
"""What is said about a folder that could not be moved."""

INTO_ITSELF = 'The folder {folder} cannot be moved into itself.'
"""What is said about a folder that would be put inside its own tree."""

FILE_MANAGER_NAMES = ('.DS_Store', '.localized', 'Thumbs.db', 'desktop.ini',
                      '.directory')
"""Files that macOS, Windows and KDE file managers put into folders."""

IGNORED_NAMES = frozenset(name.casefold() for name in (
    ORDER_NAME, *FILE_MANAGER_NAMES, *map(template_name, NoteExtension)))
"""Casefolded names of the files that do not make a folder non-empty.

They are notesmgr's own note order file, the template of a folder
whatever extension the project has, and the files that file managers
put there on their own, none of which the user wrote.
"""


class Tally(NamedTuple):
    """How much of the user's a folder holds, all the way down.

    The files named in IGNORED_NAMES are not the user's, so they are
    not counted.
    """

    notes: int = 0
    folders: int = 0
    others: int = 0

    @property
    def empty(self) -> bool:
        """Whether nothing of the user's is held at all."""
        return self == Tally()


def new_folder(parent: Path, typed: str, extension: NoteExtension) -> Path:
    """Make a folder in a folder of the project.

    The new folder starts out as the folder above it: it is given a
    copy of that folder's template and a note order file of its own,
    so that opening the project again finds nothing to repair.

    Args:
        parent: The folder that the new folder is made in.
        typed: What the user typed as the name of the new folder.
        extension: The extension that the notes of the project have.

    Returns:
        The folder that was made.

    Raises:
        NotesmgrError: The name names no folder that can be made
            here, or the folder cannot be made.
    """
    path = free_path(parent, checked_name(typed))
    template = path / template_name(extension)
    try:
        path.mkdir()
        template.write_text(template_text(parent, extension), encoding='utf-8')
    except OSError as error:
        raise NotesmgrError(NOT_MADE.format(path=path,
                                            reason=error)) from error
    resync_order(path)
    return path


def rename_folder(folder: Path, typed: str) -> Path:
    """Give a folder of the project another name.

    Nothing outside a folder names it, so a folder is renamed whether
    it holds anything or not, and a name that differs from its own
    only in case is a name it can have. The root folder is the project
    itself rather than a folder in it, and is renamed from the outside.

    Args:
        folder: The folder to rename.
        typed: What the user typed as its new name.

    Returns:
        The folder under the name it now has.

    Raises:
        NotesmgrError: The folder is the root folder of the project,
            the name names no folder, the name is taken already, or
            the folder cannot be renamed.
    """
    if is_project(folder):
        raise NotesmgrError(IS_PROJECT.format(folder=folder))
    name = checked_name(typed)
    if name == folder.name:
        return folder
    wanted = free_path(folder.parent, name, folder.name)
    try:
        folder.rename(wanted)
    except OSError as error:
        raise NotesmgrError(NOT_RENAMED.format(path=folder,
                                               reason=error)) from error
    return wanted


def is_ignored(path: Path) -> bool:
    """Return whether a path is a file that IGNORED_NAMES names.

    Names are compared whatever their case, as the file systems of
    macOS and Windows compare them.
    """
    return path.is_file() and path.name.casefold() in IGNORED_NAMES


def is_empty(folder: Path) -> bool:
    """Return whether a folder holds nothing but files that are ignored.

    A folder that holds only its template, its note order file and
    what file managers put there is empty to the user looking at it.

    Args:
        folder: The folder to look into.

    Returns:
        Whether nothing of the user's would be taken away with it.

    Raises:
        NotesmgrError: The folder cannot be read.
    """
    return all(is_ignored(path) for path in folder_entries(folder))


def all_entries(folder: Path) -> Iterator[Path]:
    """Yield everything below a folder, going down into shown folders.

    Hidden folders and folders reached through a symbolic link are
    yielded themselves, but not gone into, just as the tree does not
    show them.

    Raises:
        NotesmgrError: A folder cannot be read.
    """
    for path in folder_entries(folder):
        yield path
        if is_shown_folder(path):
            yield from all_entries(path)


def tally_folder(folder: Path) -> Tally:
    """Return how much of the user's a folder holds, all the way down.

    Args:
        folder: The folder to look into.

    Returns:
        The notes and the shown folders below it, and everything else
        of the user's, such as pictures or hidden folders.

    Raises:
        NotesmgrError: A folder below it cannot be read.
    """
    entries = [path for path in all_entries(folder)
               if not is_ignored(path)]
    folders = sum(1 for path in entries if is_shown_folder(path))
    notes = sum(1 for path in entries
                if path.is_file() and is_plain_note(path.name))
    return Tally(notes=notes, folders=folders,
                 others=len(entries) - notes - folders)


def delete_folder(folder: Path, with_content: bool = False) -> None:
    """Move a folder of the project to the trash.

    Args:
        folder: The folder to take away.
        with_content: Whether the folder may be taken away with things
            of the user's in it, which only the user is to decide.

    Raises:
        NotesmgrError: The folder is the root folder of the project,
            it holds things of the user's that it is not to be taken
            away with, or the trash would not take it.
    """
    if is_project(folder):
        raise NotesmgrError(IS_PROJECT.format(folder=folder))
    if not with_content and not is_empty(folder):
        raise NotesmgrError(NOT_EMPTY.format(folder=folder))
    send_to_trash(folder, NOT_TRASHED)


def move_folder(folder: Path, parent: Path) -> Path:
    """Move a folder of the project into another folder of it.

    Everything the folder holds goes along with it, and no note order
    is touched: a note order lists the notes of one folder and knows
    nothing of the folders beside them.

    Args:
        folder: The folder to move.
        parent: The folder it is to be in.

    Returns:
        The folder where it now is, which is where it was when it is
        in that folder already.

    Raises:
        NotesmgrError: The folder is the root folder of the project,
            it would be put inside its own tree, the name is taken in
            the other folder already, or the folder cannot be moved.
    """
    if is_project(folder):
        raise NotesmgrError(IS_PROJECT.format(folder=folder))
    if parent == folder or folder in parent.parents:
        raise NotesmgrError(INTO_ITSELF.format(folder=folder))
    if parent == folder.parent:
        return folder
    wanted = free_path(parent, folder.name)
    try:
        folder.rename(wanted)
    except OSError as error:
        raise NotesmgrError(NOT_MOVED.format(path=folder,
                                             reason=error)) from error
    return wanted
