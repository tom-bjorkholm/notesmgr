#! /usr/local/bin/python3
"""Tests for the values a notesmgr configuration starts out with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
import sys
from typing import Callable, NamedTuple, Optional
import pytest
from notesmgr.config_defaults import EDITOR_VARIABLE, default_editor


class EditorCase(NamedTuple):
    """One machine, and the editor command that follows from it."""

    code: bool
    """Whether Microsoft Visual Studio Code is installed."""

    named: Optional[str]
    """What the environment names as the editor, None for nothing."""

    platform: str
    """What sys.platform says this machine is."""

    expected: str
    """The editor command that a new configuration gets here."""


def which_result(found: bool) -> Callable[[str], Optional[str]]:
    """Return a stand-in for shutil.which that finds a program or not."""
    return lambda name: f'/usr/bin/{name}' if found else None


@pytest.fixture(name='machine')
def fixture_machine(monkeypatch: pytest.MonkeyPatch
                    ) -> Callable[[EditorCase], None]:
    """Let a test describe the machine the default is chosen on."""
    def describe(case: EditorCase) -> None:
        """Make the environment answer as the described machine would."""
        monkeypatch.setattr(shutil, 'which', which_result(case.code))
        if case.named is None:
            monkeypatch.delenv(EDITOR_VARIABLE, raising=False)
        else:
            monkeypatch.setenv(EDITOR_VARIABLE, case.named)
        monkeypatch.setattr(sys, 'platform', case.platform)
    return describe


@pytest.mark.parametrize('case', [
    EditorCase(True, None, 'darwin', 'code -n'),
    EditorCase(True, 'vi', 'win32', 'code -n'),
    EditorCase(True, 'vi', 'linux', 'code -n'),
    EditorCase(False, 'vi', 'darwin', 'vi'),
    EditorCase(False, 'subl -w', 'win32', 'subl -w'),
    EditorCase(False, '  vi -n  ', 'linux', 'vi -n'),
    EditorCase(False, '', 'darwin', 'open'),
    EditorCase(False, '   ', 'darwin', 'open'),
    EditorCase(False, None, 'darwin', 'open'),
    EditorCase(False, None, 'win32', 'notepad'),
    EditorCase(False, None, 'linux', 'emacs'),
    EditorCase(False, None, 'freebsd14', 'emacs')])
def test_default_editor(machine: Callable[[EditorCase], None],
                        case: EditorCase) -> None:
    """The installed editor wins, then the named one, then the platform."""
    machine(case)
    assert default_editor() == case.expected


def test_editor_is_a_command(machine: Callable[[EditorCase], None]) -> None:
    """The default editor carries no file name and no placeholder."""
    machine(EditorCase(False, None, 'darwin', 'open'))
    assert '{file}' not in default_editor()
