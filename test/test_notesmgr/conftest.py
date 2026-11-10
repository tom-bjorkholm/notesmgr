#! /usr/local/bin/python3
"""Shared pytest fixtures for the notesmgr tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
import tkinter
from contextlib import suppress
from pathlib import Path
from typing import Iterator
import pytest
from notesmgr import trash
from notesmgr.config_files import CONFIG_VARIABLE
from notesmgr.main_window import MainWindow


def tk_description() -> str:
    """Describe the Tk that the tests run on, or say there is no display.

    The exact Tk version and the windowing system are only known once
    Tk has opened a display, so without one only its major and minor
    version are told.
    """
    try:
        root = tkinter.Tk()
    except tkinter.TclError:
        return f'Tk {tkinter.TkVersion} (no display)'
    root.withdraw()
    patch_level = root.getvar('tk_patchLevel')
    system = root.call('tk', 'windowingsystem')
    root.destroy()
    return f'Tk {patch_level}, windowing system {system}'


def pytest_report_header() -> str:
    """Tell which Tcl/Tk the tests run on, to help explain Tk failures."""
    tcl_level = tkinter.Tcl().call('info', 'patchlevel')
    return f'tcl/tk: Tcl {tcl_level}, {tk_description()}'


@pytest.fixture(name='tk_root', scope='session')
def fixture_tk_root() -> Iterator[tkinter.Tk]:
    """Provide one hidden Tk root shared by the whole test session."""
    try:
        root = tkinter.Tk()
    except tkinter.TclError as error:
        pytest.skip(f'Tk has no usable display: {error}')
    root.withdraw()
    yield root
    with suppress(tkinter.TclError):
        root.destroy()


@pytest.fixture(name='top_window')
def fixture_top_window(tk_root: tkinter.Tk) -> Iterator[tkinter.Toplevel]:
    """Provide a hidden toplevel window that the test is free to destroy."""
    window = tkinter.Toplevel(tk_root)
    window.withdraw()
    yield window
    with suppress(tkinter.TclError):
        window.destroy()


@pytest.fixture(name='main_window')
def fixture_main_window(top_window: tkinter.Toplevel) -> MainWindow:
    """Provide a main window built in a hidden toplevel window."""
    return MainWindow(top_window)


@pytest.fixture(name='shown_window')
def fixture_shown_window(main_window: MainWindow) -> MainWindow:
    """Provide a main window that is really shown on the display.

    Only the focus-sensitive tests use this, so the normal test run
    never puts a window on the screen.
    """
    window = main_window.window
    window.deiconify()
    window.lift()
    window.focus_force()
    window.update()
    return main_window


@pytest.fixture(name='home', autouse=True)
def fixture_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Give every test a home folder of its own and no named file.

    No test can then read or write the configuration of whoever runs
    them, and a test that wants a user wide configuration writes one
    into the folder it is given here.
    """
    home = tmp_path / 'home'
    home.mkdir()
    monkeypatch.setattr(Path, 'home', lambda: home)
    monkeypatch.delenv(CONFIG_VARIABLE, raising=False)
    return home


@pytest.fixture(name='trashed')
def fixture_trashed(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Record what was trashed, and take it away without a real trash.

    The tests may not fill the trash of whoever runs them, so what
    notesmgr asks to have trashed is taken away here instead.
    """
    gone: list[Path] = []

    def record(path: Path) -> None:
        """Stand in for moving a file or a folder to the trash.

        What is not there is not taken away either, so the error
        that the real trash raises is raised here as well.
        """
        if path.is_dir():
            shutil.rmtree(path)
        else:
            path.unlink()
        gone.append(path)
    monkeypatch.setattr(trash, 'send2trash', record)
    return gone
