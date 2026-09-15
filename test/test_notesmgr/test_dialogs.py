#! /usr/local/bin/python3
"""Tests for the windows that notesmgr shows over its own."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import suppress
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Iterator, Optional
import pytest
from notesmgr.dialogs import BUSY_CURSOR, CANCEL_LABEL, CHOOSE_LABEL, \
    MAX_TEXT_HEIGHT, MAX_TEXT_WIDTH, MIN_TEXT_WIDTH, ChoiceDialog, \
    ask_folder, ask_yes_no, busy_cursor, show_error, show_info, show_text, \
    text_size

TEMPLATES = ['template.md', 'template.txt']
"""Options of the kind that the choosing window is made to offer."""

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


@pytest.fixture(name='choice')
def fixture_choice(top_window: tkinter.Toplevel) -> Iterator[ChoiceDialog]:
    """Provide a window asking which template to keep, answered by hand.

    The window is built but not waited for, so that the test answers
    it by pressing its buttons and needs no main loop of its own.
    """
    dialog = ChoiceDialog(top_window, 'Templates', 'Which one?', TEMPLATES)
    dialog.window.withdraw()
    yield dialog
    with suppress(tkinter.TclError):
        dialog.window.destroy()


def buttons_of(window: tkinter.Toplevel) -> dict[str, ttk.Button]:
    """Return the buttons of a window, by what they say."""
    return {str(child.cget('text')): child
            for child in window.winfo_children()
            if isinstance(child, ttk.Button)}


@pytest.mark.parametrize('answered,expected', [
    ('/tmp/notes', Path('/tmp/notes')),
    ('', None)])
def test_ask_folder(top_window: tkinter.Toplevel, answered: str,
                    expected: Optional[Path], tmp_path: Path,
                    monkeypatch: pytest.MonkeyPatch) -> None:
    """A folder that was chosen is a path, and choosing none is None."""
    monkeypatch.setattr(filedialog, 'askdirectory', lambda **kwargs: answered)
    assert ask_folder(top_window, 'Open', tmp_path) == expected


def test_ask_folder_asks(top_window: tkinter.Toplevel, tmp_path: Path,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """It is asked over the window it came from, starting where told."""
    asked: list[dict[str, object]] = []

    def record(**kwargs: object) -> str:
        """Stand in for the folder chooser of Tk."""
        asked.append(kwargs)
        return ''
    monkeypatch.setattr(filedialog, 'askdirectory', record)
    ask_folder(top_window, 'Open', tmp_path)
    assert asked == [{'parent': top_window, 'title': 'Open',
                      'mustexist': True, 'initialdir': tmp_path}]


@pytest.mark.parametrize('answered', [True, False])
def test_ask_yes_no(top_window: tkinter.Toplevel, answered: bool,
                    monkeypatch: pytest.MonkeyPatch) -> None:
    """A question answered with yes or no is answered with yes or no."""
    monkeypatch.setattr(messagebox, 'askyesno', lambda **kwargs: answered)
    assert ask_yes_no(top_window, 'Project', 'Open it?') is answered


def test_show_info(top_window: tkinter.Toplevel,
                   monkeypatch: pytest.MonkeyPatch) -> None:
    """What is worth knowing is told over the window it happened in."""
    told: list[dict[str, object]] = []
    monkeypatch.setattr(messagebox, 'showinfo',
                        lambda **kwargs: told.append(kwargs))
    show_info(top_window, 'Project', 'A template was written.')
    assert told == [{'title': 'Project', 'message': 'A template was written.',
                     'parent': top_window}]


def test_choice_offers_all(choice: ChoiceDialog) -> None:
    """Every option is offered, and the first one is marked to begin with."""
    offered = [str(child.cget('text'))
               for child in choice.window.winfo_children()
               if isinstance(child, ttk.Radiobutton)]
    assert offered == TEMPLATES
    assert choice.picked.get() == TEMPLATES[0]


def test_choice_taken(choice: ChoiceDialog) -> None:
    """The option that is marked is the answer when it is taken."""
    choice.picked.set(TEMPLATES[1])
    buttons_of(choice.window)[CHOOSE_LABEL].invoke()
    assert choice.chosen == TEMPLATES[1]
    assert not choice.window.winfo_exists()


def test_choice_cancelled(choice: ChoiceDialog) -> None:
    """Cancelling answers nothing at all, whatever was marked."""
    choice.picked.set(TEMPLATES[1])
    buttons_of(choice.window)[CANCEL_LABEL].invoke()
    assert choice.chosen is None
    assert not choice.window.winfo_exists()


def test_choice_closed(choice: ChoiceDialog) -> None:
    """Closing the window answers nothing at all."""
    choice.cancel()
    assert choice.chosen is None


def test_choice_of_none(top_window: tkinter.Toplevel) -> None:
    """A question offering nothing at all is still a window that closes."""
    dialog = ChoiceDialog(top_window, 'Templates', 'Which one?', [])
    dialog.window.withdraw()
    dialog.cancel()
    assert dialog.chosen is None
