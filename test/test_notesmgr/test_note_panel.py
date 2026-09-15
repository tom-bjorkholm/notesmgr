#! /usr/local/bin/python3
"""Tests for the panel at the right of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import time
import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Optional
import pytest
from test_notesmgr.helpers import refuse_choice, write_config, write_file, \
    write_notes, write_template
from notesmgr import note_panel as panel_module
from notesmgr.config import DEFAULT_NOTE_SIZE, MIN_NOTE_SIZE, NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import template_name
from notesmgr.note_panel import COPY_FORMATTED, COPY_RAW, DELETE, DUPLICATE, \
    EDIT, MOVE_DOWN, MOVE_UP, NEW, NotePanel, PanelHooks
from notesmgr.note_text import NOT_UTF8
from notesmgr.project_ops import open_project
from notesmgr.session import Session

NOTE_NAME = 'first.md.txt'
"""Name of the note that these tests show in the panel."""

NOTE_TEXT = f'This is {NOTE_NAME}.\n'
"""What the note of these tests holds, as write_notes writes it."""

TEMPLATE_TEXT = 'Template of the folder\n'
"""What the template of the project of these tests holds."""

ROW = [COPY_RAW, COPY_FORMATTED, DUPLICATE, EDIT, NEW, DELETE, MOVE_UP,
       MOVE_DOWN]
"""The buttons of the panel, in the order the README gives them."""

LATER = 100.0
"""Seconds to put between two writes, so that the times differ."""

MARKER = 'what was on the clipboard before'
"""Text that a test puts on the clipboard to see it left alone."""


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide a project folder holding a note and a template."""
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD_TXT)
    write_template(root, NoteExtension.MD_TXT, TEMPLATE_TEXT)
    write_notes(root, [NOTE_NAME])
    return root


def show_little(project: Path, session: Session, size: int) -> None:
    """Configure the open project to show only so much of a note."""
    write_config(project, NoteExtension.MD_TXT, size=size)
    session.opened(open_project(project, refuse_choice).project)


@pytest.fixture(name='note')
def fixture_note(project: Path) -> Path:
    """Provide the note that the panel of these tests shows."""
    return project / NOTE_NAME


@pytest.fixture(name='session')
def fixture_session(project: Path) -> Session:
    """Provide a session with the project of these tests open."""
    session = Session(project)
    session.opened(open_project(project, refuse_choice).project)
    return session


@pytest.fixture(name='errors')
def fixture_errors() -> list[str]:
    """Provide the list that the panel reports its problems into."""
    return []


@pytest.fixture(name='told')
def fixture_told() -> list[bool]:
    """Provide the list that the panel tells about a note into."""
    return []


@pytest.fixture(name='panel')
def fixture_panel(top_window: tkinter.Toplevel, session: Session,
                  errors: list[str], told: list[bool]) -> NotePanel:
    """Provide a note panel in a hidden window, showing nothing yet."""
    return NotePanel(top_window, session, PanelHooks(errors.append,
                                                     told.append))


@pytest.fixture(name='launched')
def fixture_launched(
        monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, Path]]:
    """Record the editors that were asked for, starting none."""
    started: list[tuple[str, Path]] = []

    def record(command: str, path: Path) -> None:
        """Stand in for starting the editor of the project."""
        started.append((command, path))
    monkeypatch.setattr(panel_module, 'launch_editor', record)
    return started


def row_buttons(panel: NotePanel) -> list[ttk.Button]:
    """Return the buttons of the panel, in the order they are shown."""
    return list(panel.row.buttons)


def button_state(panel: NotePanel, label: str) -> str:
    """Return the Tk state of one button of the panel."""
    for button in row_buttons(panel):
        if str(button.cget('text')) == label:
            return str(button.cget('state'))
    raise AssertionError(f'There is no {label} button.')


def unusable(panel: NotePanel) -> list[str]:
    """Return the labels of the buttons that cannot be pressed."""
    return [str(button.cget('text')) for button in row_buttons(panel)
            if str(button.cget('state')) == 'disabled']


def touch_later(path: Path) -> None:
    """Give a file a modification time well after the one it has."""
    os.utime(path, (time.time() + LATER, time.time() + LATER))


def on_clipboard(panel: NotePanel) -> Optional[str]:
    """Return what is on the clipboard, None when nothing is."""
    try:
        return str(panel.frame.clipboard_get())
    except tkinter.TclError:
        return None


def test_empty_at_first(panel: NotePanel) -> None:
    """A panel that was told nothing shows nothing at all."""
    assert panel.shown_path() == ''
    assert panel.view.area_text() == ''
    assert panel.note_path() is None
    assert not panel.has_note()


def test_the_whole_button_row(panel: NotePanel) -> None:
    """The panel holds every button of the finished application."""
    assert [str(button.cget('text')) for button in row_buttons(panel)] == ROW


def test_buttons_start_dead(panel: NotePanel) -> None:
    """With nothing selected there is nothing for a button to act on."""
    assert unusable(panel) == ROW


def test_note_is_shown(panel: NotePanel, note: Path, told: list[bool]) -> None:
    """A selected note is named and its text is shown."""
    panel.show_path(note)
    assert panel.shown_path() == str(note)
    assert panel.view.area_text() == NOTE_TEXT
    assert panel.note_path() == note
    assert told == [True]


def test_template_is_shown(panel: NotePanel, project: Path) -> None:
    """The template of a folder is shown and acted on like a note."""
    template = project / template_name(NoteExtension.MD_TXT)
    panel.show_path(template)
    assert panel.view.area_text() == TEMPLATE_TEXT
    assert panel.has_note()


def test_live_buttons_offered(panel: NotePanel, note: Path) -> None:
    """A note to act on is what the two working buttons need."""
    panel.show_path(note)
    assert button_state(panel, COPY_RAW) == 'normal'
    assert button_state(panel, EDIT) == 'normal'


def test_later_buttons_dead(panel: NotePanel, note: Path) -> None:
    """The buttons of the steps to come stay greyed out for now."""
    panel.show_path(note)
    assert unusable(panel) == [COPY_FORMATTED, DUPLICATE, NEW, DELETE,
                               MOVE_UP, MOVE_DOWN]


def test_folder_is_no_note(panel: NotePanel, project: Path,
                           told: list[bool]) -> None:
    """A selected folder is named, and holds no text to show."""
    panel.show_path(project)
    assert panel.shown_path() == str(project)
    assert panel.view.area_text() == ''
    assert panel.note_path() is None
    assert told == [False]


def test_nothing_selected(panel: NotePanel, note: Path) -> None:
    """Selecting nothing leaves the panel showing nothing again."""
    panel.show_path(note)
    panel.show_path(None)
    assert panel.shown_path() == ''
    assert panel.view.area_text() == ''
    assert unusable(panel) == ROW


def test_empty_note_is_shown(panel: NotePanel, project: Path) -> None:
    """A note holding nothing is shown as the empty note it is."""
    empty = write_file(project / 'empty.md.txt', '')
    panel.show_path(empty)
    assert panel.view.area_text() == ''
    assert not panel.view.warning_shown()
    assert panel.has_note()


def test_not_utf8_warned(panel: NotePanel, project: Path) -> None:
    """A note that is no text says so instead of showing anything."""
    odd = project / 'odd.md.txt'
    odd.write_bytes(b'not \xff\xfe text\n')
    panel.show_path(odd)
    assert panel.view.warning_shown()
    assert panel.view.area_text() == ''


def test_long_note_cut(panel: NotePanel, project: Path,
                       session: Session) -> None:
    """A note longer than the project shows is shown up to there."""
    show_little(project, session, MIN_NOTE_SIZE)
    long_note = write_file(project / 'long.md.txt', 'a' * (MIN_NOTE_SIZE + 1))
    panel.show_path(long_note)
    assert len(panel.view.area_text()) == MIN_NOTE_SIZE
    assert panel.view.warning_shown()


def test_limit_from_project(panel: NotePanel, project: Path,
                            session: Session) -> None:
    """How much of a note is shown is what the project configured."""
    show_little(project, session, MIN_NOTE_SIZE)
    assert panel.note_limit() == MIN_NOTE_SIZE


def test_limit_no_project(top_window: tkinter.Toplevel,
                          tmp_path: Path) -> None:
    """With no project open the built-in default stands in."""
    hooks = PanelHooks(lambda _message: None, lambda _shown: None)
    panel = NotePanel(top_window, Session(tmp_path), hooks)
    assert panel.note_limit() == DEFAULT_NOTE_SIZE


def test_copy_raw(panel: NotePanel, note: Path) -> None:
    """Copying the note puts its text on the clipboard as it is."""
    panel.show_path(note)
    panel.copy_raw()
    assert on_clipboard(panel) == NOTE_TEXT


def test_copy_without_note(panel: NotePanel) -> None:
    """With no note selected the clipboard is left as it was."""
    panel.frame.clipboard_clear()
    panel.frame.clipboard_append(MARKER)
    panel.copy_raw()
    assert on_clipboard(panel) == MARKER


def test_copy_what_is_unread(panel: NotePanel, project: Path,
                             errors: list[str]) -> None:
    """A note that could not be read is reported instead of copied."""
    odd = project / 'odd.md.txt'
    odd.write_bytes(b'not \xff\xfe text\n')
    panel.frame.clipboard_clear()
    panel.frame.clipboard_append(MARKER)
    panel.show_path(odd)
    panel.copy_raw()
    assert errors == [NOT_UTF8]
    assert on_clipboard(panel) == MARKER


def test_copy_what_is_shown(panel: NotePanel, project: Path,
                            session: Session) -> None:
    """A note shown in part is copied as far as it is shown."""
    show_little(project, session, MIN_NOTE_SIZE)
    long_note = write_file(project / 'long.md.txt', 'a' * (MIN_NOTE_SIZE + 1))
    panel.show_path(long_note)
    panel.copy_raw()
    assert on_clipboard(panel) == 'a' * MIN_NOTE_SIZE


def test_edit_starts_editor(panel: NotePanel, note: Path,
                            launched: list[tuple[str, Path]]) -> None:
    """Editing a note starts the editor the project is configured with."""
    panel.show_path(note)
    panel.edit_note()
    assert launched == [('vi', note)]


def test_edit_without_note(panel: NotePanel,
                           launched: list[tuple[str, Path]]) -> None:
    """With no note selected there is no editor to start."""
    panel.edit_note()
    assert launched == []


def test_edit_failure_told(panel: NotePanel, note: Path, errors: list[str],
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """An editor that cannot be started is reported to the user."""
    def refuse(_command: str, _path: Path) -> None:
        """Stand in for an editor that the system does not start."""
        raise NotesmgrError('no editor here')
    monkeypatch.setattr(panel_module, 'launch_editor', refuse)
    panel.show_path(note)
    panel.edit_note()
    assert errors == ['no editor here']


def test_edited_note_followed(panel: NotePanel, note: Path) -> None:
    """A note written by the editor is shown as it now stands."""
    panel.show_path(note)
    note.write_text('edited elsewhere\n', encoding='utf-8')
    touch_later(note)
    panel.watch.poll()
    assert panel.view.area_text() == 'edited elsewhere\n'


def test_gone_note_told(panel: NotePanel, note: Path,
                        told: list[bool]) -> None:
    """A note taken away by another program leaves nothing to act on."""
    panel.show_path(note)
    note.unlink()
    panel.watch.poll()
    assert panel.view.warning_shown()
    assert not panel.has_note()
    assert told == [True, False]
    assert unusable(panel) == ROW


@pytest.mark.focus_sensitive
def test_clipboard_round_trip(panel: NotePanel, note: Path,
                              top_window: tkinter.Toplevel) -> None:
    """A note copied from a window on the screen can be pasted back."""
    top_window.deiconify()
    top_window.lift()
    top_window.focus_force()
    top_window.update()
    panel.show_path(note)
    panel.copy_raw()
    assert on_clipboard(panel) == NOTE_TEXT
