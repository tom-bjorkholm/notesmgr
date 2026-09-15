#! /usr/local/bin/python3
"""Tests for the command line of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
from pathlib import Path
import pytest
import argcomplete
from notesmgr.cmd_line import PROGRAM_NAME, parse_command_line


def test_nothing_asked_for() -> None:
    """An empty command line opens no project and asks no question."""
    asked = parse_command_line([])
    assert asked.project is None
    assert not asked.show_version


@pytest.mark.parametrize('folder', ['notes', '/tmp/notes', '../notes',
                                    'notes with space', '.'])
def test_project_folder(folder: str) -> None:
    """The one positional argument is the project folder to open."""
    assert parse_command_line([folder]).project == Path(folder)


def test_version_asked_for() -> None:
    """The version flag asks for version information and no project."""
    asked = parse_command_line(['--version'])
    assert asked.show_version
    assert asked.project is None


def test_folder_and_version() -> None:
    """A folder and the version flag are both understood together."""
    asked = parse_command_line(['--version', 'notes'])
    assert asked.show_version
    assert asked.project == Path('notes')


def test_folder_not_checked(tmp_path: Path) -> None:
    """A folder that is no project is not refused on the command line.

    A graphical application says what is wrong with a folder in a
    window, so the command line only reads what was asked for.
    """
    missing = tmp_path / 'no_such_folder'
    assert parse_command_line([str(missing)]).project == missing


@pytest.mark.parametrize('argv,code', [
    (['--help'], 0),
    (['--no-such-option'], 2),
    (['one', 'two'], 2),
    (['--version=yes'], 2)])
def test_exit_codes(argv: list[str], code: int) -> None:
    """A command line that is answered or refused ends with its code."""
    with pytest.raises(SystemExit) as refusal:
        parse_command_line(argv)
    assert refusal.value.code == code


def test_program_named(capsys: pytest.CaptureFixture[str]) -> None:
    """The help text calls the program by the name it is started by."""
    with pytest.raises(SystemExit):
        parse_command_line(['--help'])
    assert PROGRAM_NAME in capsys.readouterr().out


def test_completion_offered(monkeypatch: pytest.MonkeyPatch) -> None:
    """The parser is offered to argcomplete so a shell can complete."""
    offered: list[argparse.ArgumentParser] = []
    monkeypatch.setattr(argcomplete, 'autocomplete', offered.append)
    parse_command_line([])
    assert len(offered) == 1
