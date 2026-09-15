#! /usr/local/bin/python3
"""Tests for the area of the main window that a note is read in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from notesmgr.note_text import NoteText
from notesmgr.note_view import NoteView

WARNING = 'Something about this note is worth saying.'
"""A warning that these tests show above a note."""


@pytest.fixture(name='view')
def fixture_view(top_window: tkinter.Toplevel) -> NoteView:
    """Provide a note area in a hidden window, showing nothing yet."""
    return NoteView(top_window)


def test_empty_at_first(view: NoteView) -> None:
    """An area that was shown nothing shows nothing and warns of nothing."""
    assert view.area_text() == ''
    assert not view.warning_shown()


def test_cannot_be_typed_in(view: NoteView) -> None:
    """The note is shown to be read, and is edited in an editor."""
    assert str(view.area.cget('state')) == 'disabled'


@pytest.mark.parametrize('text', ['', 'One line\n', 'No end of line',
                                  'Two\nlines\n', 'Å i Ö and 😀\n'])
def test_text_is_shown(view: NoteView, text: str) -> None:
    """A note is shown as it was read, to the last line ending."""
    view.show(NoteText(text))
    assert view.area_text() == text


def test_no_warning_for_none(view: NoteView) -> None:
    """A note with nothing wrong with it is shown without a warning."""
    view.show(NoteText('the text\n'))
    assert not view.warning_shown()


def test_warning_is_shown(view: NoteView) -> None:
    """A note that has something to warn about says so above itself."""
    view.show(NoteText('the text\n', WARNING))
    assert view.warning_shown()
    assert str(view.warning.cget('text')) == WARNING


def test_warning_goes_away(view: NoteView) -> None:
    """A note without a warning after one leaves no warning behind."""
    view.show(NoteText('', WARNING))
    view.show(NoteText('another note\n'))
    assert not view.warning_shown()
    assert view.area_text() == 'another note\n'


def test_shown_note_is_kept(view: NoteView) -> None:
    """The area knows the note it was given, warning and all."""
    note = NoteText('the text\n', WARNING)
    view.show(note)
    assert view.shown_note() == note


def test_showing_again(view: NoteView) -> None:
    """A note shown after another replaces it rather than following it."""
    view.show(NoteText('first\n'))
    view.show(NoteText('second\n'))
    assert view.area_text() == 'second\n'
