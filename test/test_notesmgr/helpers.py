#! /usr/local/bin/python3
"""Projects on disk that the notesmgr tests are run against."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional, Sequence
from notesmgr.config import NoteExtension
from notesmgr.note_file import template_name
from notesmgr.order_file import ORDER_NAME
from notesmgr.project import config_path

CONFIG_TEXT = '{{\n    "editor": "vi",\n    "file_extension": "{name}"\n}}\n'
"""What a configuration file of a project looks like in these tests."""


def write_config(root: Path,
                 extension: NoteExtension = NoteExtension.MD_TXT) -> Path:
    """Write the configuration file that makes a folder a project.

    Args:
        root: The folder to make into a project.
        extension: The extension that its notes are to carry.

    Returns:
        The configuration file that was written.
    """
    root.mkdir(parents=True, exist_ok=True)
    written = config_path(root)
    written.write_text(CONFIG_TEXT.format(name=extension.name),
                       encoding='utf-8')
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


def refuse_choice(_folder: Path, _templates: Sequence[Path]) -> Optional[Path]:
    """Stand in for a user who chooses no template at all."""
    return None


def first_choice(_folder: Path, templates: Sequence[Path]) -> Optional[Path]:
    """Stand in for a user who keeps the first template offered."""
    return templates[0]
