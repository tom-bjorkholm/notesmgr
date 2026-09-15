#! /usr/local/bin/python3
"""The names that the files of a notesmgr project carry."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Iterable, Optional
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError

TEMPLATE_STEM = 'template'
"""Name, without any extension, of the template file of a folder."""

NOTE_EXTENSIONS = tuple(sorted(NoteExtension, key=len, reverse=True))
"""The extensions a note file can have, the longest one first.

Trying the longest one first is what makes a name ending in .md.txt a
markdown note rather than a text note whose name ends in .md.
"""

SEPARATORS = ('/', '\\')
"""What a name cannot hold, because it would then name a folder too.

Both are refused on every platform, so that a project written on one
platform holds no name that another platform reads as a path.
"""

NO_NAME = 'A note needs a name.'
"""What is said about a name that is empty or nothing but blanks."""

IN_FOLDER = 'The name {name} names a folder as well as a note.'
"""What is said about a name that holds a path separator."""

HIDDEN = 'The name {name} starts with a dot, which hides the note.'
"""What is said about a name that would make a hidden file."""

WRONG_EXTENSION = 'The notes of this project end with {wanted}, not {given}.'
"""What is said about a name carrying the extension of another project."""

RESERVED = 'The name {name} belongs to the template of the folder.'
"""What is said about a note that would be taken for a template."""


def note_extension(name: str) -> Optional[NoteExtension]:
    """Return the note extension a file name carries, None for none.

    A name starting with a dot is a hidden file and no note, and a
    name that is nothing but an extension holds no note name at all.
    The extension is recognized whatever its case, because the file
    systems of macOS and Windows keep no case apart either.

    Args:
        name: File name, without any folders before it.

    Returns:
        The extension the name ends with, None when it ends with none.
    """
    if name.startswith('.'):
        return None
    lowered = name.casefold()
    for extension in NOTE_EXTENSIONS:
        if lowered.endswith(extension) and len(name) > len(extension):
            return extension
    return None


def is_note(name: str) -> bool:
    """Return whether a file name is the name of a note."""
    return note_extension(name) is not None


def note_stem(name: str) -> str:
    """Return a note file name without the extension it ends with.

    Args:
        name: File name of a note.

    Returns:
        The name without its extension, and the name unchanged when
        it is no note name at all.
    """
    extension = note_extension(name)
    return name if extension is None else name[:-len(extension)]


def template_name(extension: NoteExtension) -> str:
    """Return what a template is called in a project of an extension."""
    return TEMPLATE_STEM + extension


def is_template(name: str) -> bool:
    """Return whether a file name is the name of a folder's template."""
    return is_note(name) and note_stem(name).casefold() == TEMPLATE_STEM


def is_plain_note(name: str) -> bool:
    """Return whether a file name is a note that is no template."""
    return is_note(name) and not is_template(name)


def name_key(name: str) -> tuple[str, str]:
    """Return the key that orders file names alphabetically.

    Case tells two names apart only when nothing else does, so that
    the order does not depend on where the names were read from.
    """
    return (name.casefold(), name)


def sorted_names(names: Iterable[str]) -> list[str]:
    """Return the given file names in alphabetical order."""
    return sorted(names, key=name_key)


def checked_extension(name: str, extension: NoteExtension) -> str:
    """Return a note name carrying the extension of the project.

    Args:
        name: Name of a note, with or without an extension.
        extension: The extension that the notes of the project have.

    Returns:
        The name as it stands when it carries that extension already,
        and the name with the extension added when it carries none.

    Raises:
        NotesmgrError: The name carries another note extension, or it
            is the name that the template of a folder has.
    """
    carried = note_extension(name)
    if carried is not None and carried is not extension:
        raise NotesmgrError(WRONG_EXTENSION.format(wanted=extension,
                                                   given=carried))
    full_name = name if carried is extension else name + extension
    if is_template(full_name):
        raise NotesmgrError(RESERVED.format(name=full_name))
    return full_name


def note_file_name(typed: str, extension: NoteExtension) -> str:
    """Return the file name that a name typed by a user asks for.

    Args:
        typed: What the user typed as the name of a note.
        extension: The extension that the notes of the project have.

    Returns:
        The name of the file, with the extension of the project on it.

    Raises:
        NotesmgrError: What was typed names no note file.
    """
    name = typed.strip()
    if not name:
        raise NotesmgrError(NO_NAME)
    if any(separator in name for separator in SEPARATORS):
        raise NotesmgrError(IN_FOLDER.format(name=name))
    if name.startswith('.'):
        raise NotesmgrError(HIDDEN.format(name=name))
    return checked_extension(name, extension)
