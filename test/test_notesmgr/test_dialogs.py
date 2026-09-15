#! /usr/local/bin/python3
"""Tests for the windows that notesmgr shows over its own."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import suppress
from tkinter import messagebox, ttk
from typing import Iterator
import pytest
from notesmgr.dialogs import BUSY_CURSOR, MAX_TEXT_HEIGHT, MAX_TEXT_WIDTH, \
    MIN_TEXT_WIDTH, busy_cursor, show_error, show_text, text_size

REPORT = 'notesmgr 0.0.1\npackaging 25.0\n'
"""A text of the kind that these windows are made to show."""


@pytest.fixture(name='shown')
def fixture_shown(top_window: tkinter.Toplevel) -> Iterator[tkinter.Toplevel]:
    """Provide a window showing a text, destroyed after the test."""
    window = show_text(top_window, 'Versions', REPORT)
    window.withdraw()
    yield window
    with suppress(tkinter.TclError):
        window.destroy()


def text_area(window: tkinter.Toplevel) -> tkinter.Text:
    """Return the text widget that a shown text window holds."""
    areas = [child for child in window.winfo_children()
             if isinstance(child, tkinter.Text)]
    assert len(areas) == 1
    return areas[0]


@pytest.mark.parametrize('text,expected', [
    ('', (MIN_TEXT_WIDTH, 1)),
    ('short', (MIN_TEXT_WIDTH, 1)),
    ('one\ntwo\nthree', (MIN_TEXT_WIDTH, 3)),
    ('x' * 60, (60, 1)),
    ('x' * 500, (MAX_TEXT_WIDTH, 1)),
    ('line\n' * 100, (MIN_TEXT_WIDTH, MAX_TEXT_HEIGHT)),
    ('\n\n\n', (MIN_TEXT_WIDTH, 3))])
def test_text_size(text: str, expected: tuple[int, int]) -> None:
    """A window is big enough for its text and no bigger than a screen."""
    assert text_size(text) == expected


def test_window_titled(shown: tkinter.Toplevel) -> None:
    """The window is called what the caller asked it to be called."""
    assert shown.title() == 'Versions'


def test_text_is_shown(shown: tkinter.Toplevel) -> None:
    """The window holds exactly the text that was given to it."""
    assert text_area(shown).get('1.0', 'end-1c') == REPORT


def test_text_read_only(shown: tkinter.Toplevel) -> None:
    """The text cannot be typed into, as it is a report and not a note."""
    assert str(text_area(shown).cget('state')) == 'disabled'


def test_close_button(shown: tkinter.Toplevel) -> None:
    """The window holds a button, and pressing it destroys the window."""
    buttons = [child for child in shown.winfo_children()
               if isinstance(child, ttk.Button)]
    assert len(buttons) == 1
    buttons[0].invoke()
    assert not shown.winfo_exists()


def test_show_error(top_window: tkinter.Toplevel,
                    monkeypatch: pytest.MonkeyPatch) -> None:
    """What went wrong is reported over the window it happened in."""
    told: list[dict[str, object]] = []
    monkeypatch.setattr(messagebox, 'showerror',
                        lambda **kwargs: told.append(kwargs))
    show_error(top_window, 'Configuration', 'No such file')
    assert told == [{'title': 'Configuration', 'message': 'No such file',
                     'parent': top_window}]


def test_busy_cursor(top_window: tkinter.Toplevel) -> None:
    """The waiting cursor is shown while the block runs, and then not."""
    with busy_cursor(top_window):
        assert str(top_window.cget('cursor')) == BUSY_CURSOR
    assert str(top_window.cget('cursor')) == ''


def test_cursor_put_back(top_window: tkinter.Toplevel) -> None:
    """The waiting cursor goes away even when the block raises."""
    with pytest.raises(ValueError):
        with busy_cursor(top_window):
            raise ValueError('something went wrong')
    assert str(top_window.cget('cursor')) == ''
