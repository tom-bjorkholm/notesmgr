#! /usr/local/bin/python3
"""Tests for the panel at the right of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
import pytest
from notesmgr.note_panel import NotePanel


@pytest.fixture(name='panel')
def fixture_panel(top_window: tkinter.Toplevel) -> NotePanel:
    """Provide a note panel in a hidden window."""
    return NotePanel(top_window)


def test_empty_at_first(panel: NotePanel) -> None:
    """A panel that was told nothing shows nothing."""
    assert panel.shown_path() == ''


def test_shows_the_path(panel: NotePanel, tmp_path: Path) -> None:
    """The panel shows the path of what is selected."""
    note = tmp_path / 'notes' / 'first.md.txt'
    panel.show_path(note)
    assert panel.shown_path() == str(note)


def test_shows_nothing_again(panel: NotePanel, tmp_path: Path) -> None:
    """Selecting nothing leaves the panel showing nothing."""
    panel.show_path(tmp_path / 'first.md.txt')
    panel.show_path(None)
    assert panel.shown_path() == ''
