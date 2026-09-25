#! /usr/local/bin/python3
"""Projects on disk that the notesmgr tests are run against."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import json
from pathlib import Path
from typing import Optional, Sequence
import pytest
from notesmgr.config import NoteExtension, DEFAULT_NOTE_SIZE
from notesmgr.note_file import template_name
from notesmgr.order_file import ORDER_NAME
from notesmgr.project import config_path

TEST_EDITOR = 'vi'
"""Editor that the projects of these tests are configured with."""

TEMPLATE_TEXT = 'Written from the template\n'
"""What the template of a project built here holds."""


def write_config(root: Path, extension: NoteExtension = NoteExtension.MD_TXT,
                 size: Optional[int] = None) -> Path:
    """Write the configuration file that makes a folder a project.

    Args:
        root: The folder to make into a project.
        extension: The extension that its notes are to carry.
        size: How much of a note it shows, None for the default that
            a configuration file naming no size is read with.

    Returns:
        The configuration file that was written.
    """
    root.mkdir(parents=True, exist_ok=True)
    held: dict[str, object] = {'editor': TEST_EDITOR,
                               'file_extension': extension.name,
                               'max_note_size': DEFAULT_NOTE_SIZE}
    if size is not None:
        held['max_note_size'] = size
    written = config_path(root)
    written.write_text(json.dumps(held, indent=4), encoding='utf-8')
    return written


def write_file(path: Path, text: str = '') -> Path:
    """Write a file with the given text, making the folders it needs."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return path


def write_notes(folder: Path, names: Sequence[str]) -> list[Path]:
    """Write a note holding its own name for each of the given names."""
    return [write_file(folder / name, f'This is {name}.\n')
            for name in names]


def write_order(folder: Path, names: Sequence[str]) -> Path:
    """Write the note order file of a folder, holding the given names."""
    return write_file(folder / ORDER_NAME,
                      ''.join(f'{name}\n' for name in names))


def write_template(folder: Path, extension: NoteExtension,
                   text: str = '') -> Path:
    """Write the template of a folder, carrying the given extension."""
    return write_file(folder / template_name(extension), text)


def fail_on(monkeypatch: pytest.MonkeyPatch, owner: object, name: str,
            refused: Path) -> None:
    """Make a function of the file system fail on one path alone.

    The function raises the OSError that a file system raises
    whenever it is handed the refused path, and does what it does
    for every other path, so that what notesmgr writes elsewhere,
    such as the note order files, is written as it always is.

    Args:
        monkeypatch: Where the function is stood in for.
        owner: The class or the module that holds the function.
        name: What the function is called there.
        refused: The path that the function fails on.
    """
    original = getattr(owner, name)

    def failing(*args: object, **kwargs: object) -> object:
        """Stand in for the function, failing on the refused path."""
        if refused in args:
            raise OSError(f'{name} refused for {refused}')
        return original(*args, **kwargs)
    monkeypatch.setattr(owner, name, failing)


def reports(told: str, message: str, path: Path) -> bool:
    """Return whether what was told is a message about a path.

    The reason at the end of the message is what the operating system
    said, which differs from one system to the next, so only what the
    message says before it is compared.

    Args:
        told: What the user was told.
        message: The message, with a path and a reason to fill in.
        path: The path that the message is to be about.
    """
    return told.startswith(message.format(path=path, reason=''))


def refuse_choice(_folder: Path, _templates: Sequence[Path]) -> Optional[Path]:
    """Stand in for a user who chooses no template at all."""
    return None


def first_choice(_folder: Path, templates: Sequence[Path]) -> Optional[Path]:
    """Stand in for a user who keeps the first template offered."""
    return templates[0]


def build_project(root: Path, names: Sequence[str],
                  extension: NoteExtension = NoteExtension.MD_TXT) -> Path:
    """Write a project holding the given notes in its root folder.

    Args:
        root: The folder to make into a project.
        names: The notes of the root folder, in the order they get.
        extension: The extension that its notes are to carry.

    Returns:
        The root folder of the project that was written.
    """
    write_config(root, extension)
    write_template(root, extension, TEMPLATE_TEXT)
    write_notes(root, names)
    write_order(root, names)
    return root


def build_folder_project(root: Path) -> Path:
    """Write a project of two notes and two folders holding one each.

    The folders hold no template of their own, so that opening the
    project writes one, which is what the explorer shows above the
    notes of a folder.

    Args:
        root: The folder to make into a project.

    Returns:
        The root folder of the project that was written.
    """
    build_project(root, ['second.md.txt', 'first.md.txt'])
    write_notes(root / 'apple', ['a.md.txt'])
    write_notes(root / 'zebra', ['z.md.txt'])
    return root
