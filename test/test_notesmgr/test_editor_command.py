#! /usr/local/bin/python3
"""Tests for starting the editor that a project is configured with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import time
from pathlib import Path
import pytest
from notesmgr.editor_command import editor_argv, launch_editor, \
    split_command, start_detached
from notesmgr.errors import NotesmgrError

NOTE = Path('/notes/first.md.txt')
"""The note that these tests open in an editor."""

WAIT_STEP = 0.05
"""Seconds between two looks for what a started program wrote."""

WAITS = 100
"""How many times these tests look before giving a program up."""


@pytest.mark.parametrize('command,words', [
    ('code', ['code']),
    ('  code  ', ['code']),
    ('', []),
    ('code -w', ['code', '-w']),
    ('code "my editor" -w', ['code', 'my editor', '-w']),
    ("'/usr/local/my editor/ed'", ['/usr/local/my editor/ed']),
    ('ed {file}', ['ed', '{file}']),
    (r'ed \{file\}', ['ed', '{file}'])])
def test_posix_splitting(command: str, words: list[str]) -> None:
    """A command is split into words the way a POSIX shell splits it."""
    assert split_command(command, windows=False) == words


@pytest.mark.parametrize('command,words', [
    ('notepad', ['notepad']),
    (r'C:\Windows\notepad.exe', [r'C:\Windows\notepad.exe']),
    (r'"C:\Program Files\ed\ed.exe" {file}',
     [r'C:\Program Files\ed\ed.exe', '{file}']),
    (r'ed.exe -w C:\notes\a.md', ['ed.exe', '-w', r'C:\notes\a.md'])])
def test_windows_splitting(command: str, words: list[str]) -> None:
    """A Windows command keeps the backslashes of its paths whole."""
    assert split_command(command, windows=True) == words


def test_posix_eats_backslash() -> None:
    """The POSIX rules are the reason that Windows has its own.

    A backslash escapes the character after it in a POSIX shell, so a
    Windows path split by those rules loses its separators, which is
    what splitting by the rules of the platform avoids.
    """
    assert split_command(r'C:\bin\ed.exe', windows=False) == ['C:bined.exe']


@pytest.mark.parametrize('command,argv', [
    ('code', ['code', str(NOTE)]),
    ('code -w', ['code', '-w', str(NOTE)]),
    ('code {file}', ['code', str(NOTE)]),
    ('code -w {file}', ['code', '-w', str(NOTE)]),
    ('code {file} -w', ['code', str(NOTE), '-w']),
    ('diff {file} {file}', ['diff', str(NOTE), str(NOTE)]),
    ('ed --file={file}', ['ed', f'--file={NOTE}']),
    ('ed "{file}"', ['ed', str(NOTE)])])
def test_argv_built(command: str, argv: list[str]) -> None:
    """The note takes the place of every {file}, or is added at the end."""
    assert editor_argv(command, NOTE) == argv


@pytest.mark.parametrize('command', ['', '   ', '\t'])
def test_argv_needs_a_program(command: str) -> None:
    """A command naming no program at all is refused."""
    with pytest.raises(NotesmgrError):
        editor_argv(command, NOTE)


@pytest.mark.parametrize('command', ['code "unclosed', "ed 'unclosed"])
def test_argv_needs_quotes(command: str) -> None:
    """A command whose quotes do not match is refused with its reason."""
    with pytest.raises(NotesmgrError):
        editor_argv(command, NOTE)


def test_editor_is_started() -> None:
    """Starting the editor runs the command line that was built."""
    started: list[list[str]] = []
    launch_editor('code -w {file}', NOTE, started.append)
    assert started == [['code', '-w', str(NOTE)]]


def test_start_failure_told() -> None:
    """An editor that the system refuses to start is reported."""
    def refuse(_argv: list[str]) -> None:
        """Stand in for a program that the system does not start."""
        raise OSError('no such program')
    with pytest.raises(NotesmgrError, match='no such program'):
        launch_editor('code {file}', NOTE, refuse)


def test_missing_program_told() -> None:
    """An editor that is not installed is reported as an error.

    This is the one test that lets the real runner try to start a
    program, so that what a missing editor raises is what the code
    is written against and not what a test was told to raise.
    """
    with pytest.raises(NotesmgrError):
        launch_editor('notesmgr-no-such-editor {file}', NOTE)


def wait_for(path: Path) -> bool:
    """Return whether a file turns up within a few seconds."""
    for _ in range(WAITS):
        if path.is_file():
            return True
        time.sleep(WAIT_STEP)
    return False


def test_detached_start(tmp_path: Path) -> None:
    """A started program goes on running without being waited for."""
    written = tmp_path / 'written.txt'
    program = f'open({str(written)!r}, "w").write("done")'
    start_detached([sys.executable, '-c', program])
    assert wait_for(written)
