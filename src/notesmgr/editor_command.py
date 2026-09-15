#! /usr/local/bin/python3
"""Starting the editor that a project is configured with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import shlex
import subprocess
from pathlib import Path
from typing import Callable
from notesmgr.errors import NotesmgrError

PLACEHOLDER = '{file}'
"""What the name of the note replaces in the editor command."""

ON_WINDOWS = os.name == 'nt'
"""Whether a command line is to be read the way Windows reads one."""

QUOTES = ('"', "'")
"""What a Windows command line may have around one of its words."""

UNREADABLE = 'The editor command cannot be read.\n{command}\n{reason}'
"""What is said about a command whose quotes do not match."""

NO_PROGRAM = 'The editor command {command} names no program to start.'
"""What is said about a command that holds no word at all."""

NOT_STARTED = 'The editor cannot be started.\n{command}\n{reason}'
"""What is said about an editor that the system did not start."""


def unquoted(word: str) -> str:
    """Return one word of a command line without the quotes around it.

    Args:
        word: A word as a Windows command line holds it.

    Returns:
        The word itself, which is what is to be passed on.
    """
    for quote in QUOTES:
        if len(word) > 1 and word.startswith(quote) and word.endswith(quote):
            return word[1:-1]
    return word


def split_command(command: str, windows: bool = ON_WINDOWS) -> list[str]:
    """Return the words that an editor command is made of.

    A backslash is an escape character to a POSIX shell and a path
    separator on Windows, so a Windows command line is split by the
    rules that keep its paths whole, and the quotes that splitting
    leaves behind are then taken off.

    Args:
        command: The editor command as the configuration holds it.
        windows: Whether to split it the way Windows does.

    Returns:
        The words of the command, quotes taken off.

    Raises:
        ValueError: The quotes of the command do not match.
    """
    if windows:
        return [unquoted(word) for word in shlex.split(command, posix=False)]
    return shlex.split(command)


def editor_argv(command: str, path: Path) -> list[str]:
    """Return the command line that opens one note in the editor.

    The name of the note takes the place of every {file} in the
    command, and is added at the end of a command that holds none,
    so that 'code' and 'code {file}' mean the same thing.

    Args:
        command: The editor command as the configuration holds it.
        path: The note to open.

    Returns:
        The program to start and the arguments to give it.

    Raises:
        NotesmgrError: The command cannot be read, or names nothing
            to start.
    """
    try:
        words = split_command(command)
    except ValueError as error:
        raise NotesmgrError(UNREADABLE.format(command=command,
                                              reason=error)) from error
    if not words:
        raise NotesmgrError(NO_PROGRAM.format(command=command))
    name = str(path)
    if not any(PLACEHOLDER in word for word in words):
        return words + [name]
    return [word.replace(PLACEHOLDER, name) for word in words]


def start_detached(argv: list[str]) -> None:
    """Start a program and leave it running on its own.

    The editor outlives the command that started it and is not to be
    stopped by what stops notesmgr, so it is put in a session of its
    own. Windows knows no sessions and ignores that, which is right
    there, where a started program is independent already.

    Args:
        argv: The program to start and the arguments to give it.

    Raises:
        OSError: The program cannot be started.
    """
    # pylint: disable=consider-using-with
    subprocess.Popen(argv, start_new_session=True)


def launch_editor(command: str, path: Path,
                  run: Callable[[list[str]], None] = start_detached) -> None:
    """Open one note in the editor that the project is configured with.

    Args:
        command: The editor command as the configuration holds it.
        path: The note to open.
        run: What starts the editor, for a test to stand in for.

    Raises:
        NotesmgrError: The command cannot be read, names nothing to
            start, or names a program that the system did not start.
    """
    argv = editor_argv(command, path)
    try:
        run(argv)
    except OSError as error:
        raise NotesmgrError(NOT_STARTED.format(command=' '.join(argv),
                                               reason=error)) from error
