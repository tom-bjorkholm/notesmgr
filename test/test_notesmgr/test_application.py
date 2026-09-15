#! /usr/local/bin/python3
"""Tests for the start-up of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
from typing import NamedTuple, TextIO
import pytest
from notesmgr import application as application_module
from notesmgr.application import main
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
