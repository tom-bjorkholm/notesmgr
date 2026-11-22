#! /usr/local/bin/python3
"""A project of nested folders, and which of them the explorer opens."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from test_notesmgr.helpers import build_project, write_notes, write_order, \
    write_template
from notesmgr.config import NoteExtension
from notesmgr.explorer_tree import ExplorerTree

ROOT_NOTE = 'first.md.txt'
"""The one note of the root folder of the nested project."""

SUBFOLDER_NOTES = {'apple': 'a.md.txt', 'apple/deep': 'd.md.txt',
                   'zebra': 'z.md.txt'}
"""The one note of each folder below the root, by folder."""

ALL_FOLDERS = {'.', *SUBFOLDER_NOTES}
"""Every folder of the nested project, the root folder being '.'.

That is what the root is called when a path is made relative to it.
"""


def build_nested(root: Path) -> Path:
    """Write a project whose folder apple holds a folder deep.

    Every folder has its template and its note order file, so that
    opening the project has nothing to add and nothing to tell.

    Args:
        root: The folder to make into a project.

    Returns:
        The root folder of the project that was written.
    """
    build_project(root, [ROOT_NOTE])
    for folder, note in SUBFOLDER_NOTES.items():
        write_notes(root / folder, [note])
        write_order(root / folder, [note])
        write_template(root / folder, NoteExtension.MD_TXT)
    return root


def open_folders(explorer: ExplorerTree, root: Path) -> set[str]:
    """Return the folders that the explorer shows open.

    Args:
        explorer: The explorer that shows the project.
        root: The root folder of the project.

    Returns:
        The open folders, relative to the root and written with
        slashes, the root folder itself being '.'.
    """
    tree = explorer.tree
    return {Path(item).relative_to(root).as_posix()
            for item in explorer.items()
            if Path(item).is_dir()
            and tree.tk.getboolean(tree.item(item, 'open'))}
