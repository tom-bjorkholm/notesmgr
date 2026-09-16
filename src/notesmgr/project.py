#! /usr/local/bin/python3
"""What a notesmgr project is and what the folders of it hold."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple, Optional, Sequence
from notesmgr.config import NotesmgrConfig
from notesmgr.config_files import read_config_file
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import is_plain_note, is_template, name_key

PROJECT_CONFIG = 'notesmgr.cfg'
"""Name of the configuration file in the root folder of a project."""

NO_PROJECT = 'The folder {folder} is no notesmgr project.'
"""What is said about a folder that holds no configuration file."""

NOT_LISTED = 'The folder {folder} cannot be read.\n{reason}'
"""What is said about a folder whose content cannot be listed."""


class FolderContent(NamedTuple):
    """What one folder holds, before anything about it is repaired."""

    folders: Sequence[Path]
    templates: Sequence[Path]
    notes: Sequence[str]


class Folder(NamedTuple):
    """One folder of a project, holding what it holds in shown order."""

    path: Path
    folders: Sequence['Folder']
    template: Optional[Path]
    notes: Sequence[Path]


class Project(NamedTuple):
    """An open project: where it is, how it behaves, what it holds."""

    root: Path
    config: NotesmgrConfig
    tree: Folder


def config_path(root: Path) -> Path:
    """Return the configuration file of the project in a folder."""
    return root / PROJECT_CONFIG


def is_project(root: Path) -> bool:
    """Return whether a folder is the root folder of a project."""
    return config_path(root).is_file()


def read_config(root: Path) -> NotesmgrConfig:
    """Return the configuration of the project in a folder.

    Args:
        root: The root folder of the project.

    Returns:
        The configuration that the project is used with.

    Raises:
        NotesmgrError: The folder is no project, or its configuration
            file holds nothing that notesmgr can use.
    """
    if not is_project(root):
        raise NotesmgrError(NO_PROJECT.format(folder=root))
    return read_config_file(config_path(root))


def is_shown_folder(path: Path) -> bool:
    """Return whether a folder of a project is shown in the tree.

    A folder whose name starts with a dot is hidden, and a folder
    reached through a symbolic link is passed over, so that a link
    leading back into the project cannot make reading it go on
    for ever.
    """
    if path.name.startswith('.') or path.is_symlink():
        return False
    return path.is_dir()


def folder_entries(folder: Path) -> list[Path]:
    """Return everything a folder holds, in alphabetical order.

    Args:
        folder: Folder of a project.

    Returns:
        Every file and folder in it, hidden ones and all, because
        what is shown is one question and what a name would collide
        with is another.

    Raises:
        NotesmgrError: The folder cannot be read.
    """
    try:
        return sorted(folder.iterdir(), key=lambda path: name_key(path.name))
    except OSError as error:
        raise NotesmgrError(NOT_LISTED.format(folder=folder,
                                              reason=error)) from error


def folder_content(folder: Path) -> FolderContent:
    """Return what a folder holds, in the order it is shown in.

    Args:
        folder: Folder of a project.

    Returns:
        The subfolders and the templates in alphabetical order, and
        the names of the notes in the order the folder happened to
        give them, which the note order file has yet to settle.

    Raises:
        NotesmgrError: The folder cannot be read.
    """
    entries = folder_entries(folder)
    names = [entry.name for entry in entries if entry.is_file()]
    return FolderContent(
        folders=[entry for entry in entries if is_shown_folder(entry)],
        templates=[folder / name for name in names if is_template(name)],
        notes=[name for name in names if is_plain_note(name)])


def folder_paths(folder: Folder) -> list[Path]:
    """Return a folder of a project and every folder below it.

    Args:
        folder: The folder to start from, which is the tree of the
            project when every folder of it is wanted.

    Returns:
        The folders, each one before the folders below it, which is
        the order that the explorer shows them in.
    """
    paths = [folder.path]
    for below in folder.folders:
        paths.extend(folder_paths(below))
    return paths
