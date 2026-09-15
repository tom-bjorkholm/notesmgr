#! /usr/local/bin/python3
"""Shared pytest fixtures for the notesmgr tests."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import suppress
from typing import Iterator
import pytest


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
