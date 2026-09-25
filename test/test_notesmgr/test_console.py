#! /usr/local/bin/python3
"""Tests for where notesmgr says what its command line asks it to say."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from tkinter import messagebox
from typing import Callable, NamedTuple, Optional, Union
import pytest
from notesmgr import console as console_module
from notesmgr.console import CONSOLE_TITLE, console_or_window, show_said


class Said(NamedTuple):
    """What was asked to be shown in a window, and whether it failed."""

    text: str
    failed: bool


@pytest.fixture(name='said')
def fixture_said(monkeypatch: pytest.MonkeyPatch) -> list[Said]:
    """Record what was asked to be shown in a window, showing nothing."""
    asked: list[Said] = []

    def record(text: str, failed: bool) -> None:
        """Stand in for showing in a window what was said."""
        asked.append(Said(text, failed))
    monkeypatch.setattr(console_module, 'show_said', record)
    return asked


def test_console_written(said: list[Said],
                         capsys: pytest.CaptureFixture[str]) -> None:
    """Where there is a console it is written to, and nothing is shown."""
    with console_or_window():
        print('on the console')
    assert capsys.readouterr().out == 'on the console\n'
    assert said == [Said('', False)]


def test_no_output_stream(said: list[Said],
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """With no output stream what is said is shown in a window instead."""
    monkeypatch.setattr(sys, 'stdout', None)
    with console_or_window():
        print('in a window')
    assert said == [Said('in a window\n', False)]
    assert sys.stdout is None


@pytest.mark.parametrize('code,failed', [(2, True), ('refused', True),
                                         (0, False), (None, False)])
def test_no_error_stream(said: list[Said], monkeypatch: pytest.MonkeyPatch,
                         code: Optional[Union[int, str]],
                         failed: bool) -> None:
    """A command line that leaves is shown as failed only when it failed.

    The help leaves with nothing to say about failing, and an error
    leaves with a code saying that it did, which is how argparse and
    sys.exit() tell the two apart.
    """
    monkeypatch.setattr(sys, 'stderr', None)
    with pytest.raises(SystemExit):
        with console_or_window():
            print('leaving', file=sys.stderr)
            sys.exit(code)
    assert said == [Said('leaving\n', failed)]


class Box(NamedTuple):
    """One message box that was asked to be shown."""

    kind: str
    title: Optional[str]
    message: Optional[str]


@pytest.fixture(name='boxes')
def fixture_boxes(monkeypatch: pytest.MonkeyPatch) -> list[Box]:
    """Record the message boxes that were asked for, showing none."""
    asked: list[Box] = []

    def recorder(kind: str) -> Callable[..., str]:
        """Return a stand in for one kind of message box."""
        def record(title: Optional[str] = None, message: Optional[str] = None,
                   **_options: object) -> str:
            """Stand in for a message box, which the user says OK to."""
            asked.append(Box(kind, title, message))
            return 'ok'
        return record
    monkeypatch.setattr(messagebox, 'showinfo', recorder('info'))
    monkeypatch.setattr(messagebox, 'showerror', recorder('error'))
    return asked


def test_nothing_said(boxes: list[Box]) -> None:
    """Nothing said opens no window at all."""
    show_said('', True)
    assert not boxes


@pytest.mark.parametrize('failed,kind', [(True, 'error'), (False, 'info')])
def test_said_in_box(boxes: list[Box], failed: bool, kind: str) -> None:
    """What was said is shown as an error only when it tells of one."""
    show_said('usage: notesmgr', failed)
    assert boxes == [Box(kind, CONSOLE_TITLE, 'usage: notesmgr')]
