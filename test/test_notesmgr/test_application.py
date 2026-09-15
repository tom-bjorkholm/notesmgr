#! /usr/local/bin/python3
"""Tests for the start-up of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
from pathlib import Path
from typing import NamedTuple, TextIO
import pytest
from test_notesmgr.helpers import write_config, write_notes, write_template
from notesmgr import application as application_module
from notesmgr import main_window as window_module
from notesmgr.application import main
from notesmgr.config import NoteExtension
from notesmgr.main_window import APPLICATION_NAME

REPORT = 'notesmgr 0.0.1\n'
"""What the version report says in these tests."""


class WindowState(NamedTuple):
    """What one window looked like when the main loop was entered.

    The application destroys its root window as soon as the main loop
    returns, so the state has to be taken while the window still exists.
    """

    root: tkinter.Tk
    title: str
    widget_classes: list[str]


@pytest.fixture(name='shown')
def fixture_shown(tk_root: tkinter.Tk,
                  monkeypatch: pytest.MonkeyPatch) -> list[WindowState]:
    """Record the windows given to the Tk main loop instead of showing."""
    _ = tk_root    # depended on only to skip these tests without a display
    shown: list[WindowState] = []

    def record(root: tkinter.Misc, _unused: int = 0) -> None:
        """Stand in for tkinter.Misc.mainloop."""
        assert isinstance(root, tkinter.Tk)
        classes = [child.winfo_class() for child in root.winfo_children()]
        shown.append(WindowState(root, root.title(), classes))
    monkeypatch.setattr(tkinter.Tk, 'mainloop', record)
    return shown


@pytest.fixture(name='reported')
def fixture_reported(monkeypatch: pytest.MonkeyPatch) -> list[TextIO]:
    """Record where a version report was written, gathering none."""
    streams: list[TextIO] = []

    def report(out_file: TextIO) -> None:
        """Stand in for gathering the version report, which is slow."""
        streams.append(out_file)
        out_file.write(REPORT)
    monkeypatch.setattr(application_module, 'version_report', report)
    return streams


def test_main_runs_mainloop(shown: list[WindowState]) -> None:
    """main() gives the root window to the Tk main loop exactly once."""
    main([])
    assert len(shown) == 1


def test_main_builds_window(shown: list[WindowState]) -> None:
    """main() fills the root window before the main loop is entered."""
    main([])
    assert shown[0].title == APPLICATION_NAME
    assert 'TPanedwindow' in shown[0].widget_classes
    assert 'Menu' in shown[0].widget_classes


def test_main_destroys_root(shown: list[WindowState]) -> None:
    """main() destroys the root window once the main loop has returned."""
    main([])
    with pytest.raises(tkinter.TclError):
        shown[0].root.winfo_exists()


def test_version_to_stdout(shown: list[WindowState],
                           reported: list[TextIO]) -> None:
    """A command line asking for versions reports them and opens nothing."""
    main(['--version'])
    assert reported == [sys.stdout]
    assert not shown


def test_version_is_printed(shown: list[WindowState], reported: list[TextIO],
                            capsys: pytest.CaptureFixture[str]) -> None:
    """The report really reaches the stream that a shell reads.

    The report itself is stood in for, because gathering the real one
    asks PyPI about newer releases over the network.
    """
    main(['--version'])
    assert capsys.readouterr().out == REPORT
    assert len(reported) == 1
    assert not shown


@pytest.fixture(name='no_dialogs', autouse=True)
def fixture_no_dialogs(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Let no test of this module put a real dialog on the screen."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for telling the user something in a window."""
        told.append(message)
    monkeypatch.setattr(window_module, 'show_info', record)
    monkeypatch.setattr(window_module, 'show_error', record)
    return told


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide a project folder that a command line can name.

    It holds its template already, so that opening it changes nothing
    and has nothing to tell the user about.
    """
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD_TXT)
    write_template(root, NoteExtension.MD_TXT)
    write_notes(root, ['a.md.txt'])
    return root


def test_named_project_opened(shown: list[WindowState], project: Path,
                              no_dialogs: list[str]) -> None:
    """A project folder on the command line is the project that opens."""
    main([str(project)])
    assert shown[0].title == f'{APPLICATION_NAME} — notes'
    assert not no_dialogs


def test_no_project_named(shown: list[WindowState]) -> None:
    """With no folder on the command line no project is opened."""
    main([])
    assert shown[0].title == APPLICATION_NAME


def test_named_no_project(shown: list[WindowState], tmp_path: Path,
                          no_dialogs: list[str]) -> None:
    """A folder that is no project is reported, and the window still opens."""
    main([str(tmp_path)])
    assert len(no_dialogs) == 1
    assert shown[0].title == APPLICATION_NAME
