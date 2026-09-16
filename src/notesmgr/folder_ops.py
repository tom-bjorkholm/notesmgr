#! /usr/local/bin/python3
"""Making, renaming and taking away the folders of a project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import checked_name, is_template, template_name
from notesmgr.note_ops import free_path, resync_order, template_text
from notesmgr.order_file import ORDER_NAME
from notesmgr.project import folder_entries, is_project
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
    it holds anything or not. The root folder is the project itself
    rather than a folder in it, and is renamed from the outside.

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
    wanted = free_path(folder.parent, name)
    try:
        folder.rename(wanted)
    except OSError as error:
        raise NotesmgrError(NOT_RENAMED.format(path=folder,
                                               reason=error)) from error
    return wanted


def is_empty(folder: Path) -> bool:
    """Return whether a folder holds nothing but notesmgr's own files.

    The template of a folder and its note order file are notesmgr's
    doing rather than anything the user put there, so a folder that
    holds only those is empty to the user who is looking at it.

    Args:
        folder: The folder to look into.

    Returns:
        Whether nothing of the user's would be taken away with it.

    Raises:
        NotesmgrError: The folder cannot be read.
    """
    return all(path.is_file() and (path.name == ORDER_NAME
                                   or is_template(path.name))
               for path in folder_entries(folder))


def delete_folder(folder: Path) -> None:
    """Move a folder that holds nothing of the user's to the trash.

    Args:
        folder: The folder to take away.

    Raises:
        NotesmgrError: The folder is the root folder of the project,
            it holds notes or folders of its own, or the trash would
            not take it.
    """
    if is_project(folder):
        raise NotesmgrError(IS_PROJECT.format(folder=folder))
    if not is_empty(folder):
        raise NotesmgrError(NOT_EMPTY.format(folder=folder))
    send_to_trash(folder, NOT_TRASHED)
