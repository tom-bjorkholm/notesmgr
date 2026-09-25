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
from notesmgr import commands as commands_module
from notesmgr import note_panel as panel_module
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, DUPLICATE, \
    EDIT, MOVE_DOWN, MOVE_UP, NEW, NEW_FOLDER
from notesmgr.clipboard_tool import RichText
from notesmgr.commands import Commands, WindowHooks
from notesmgr.config import DEFAULT_NOTE_SIZE, MIN_NOTE_SIZE, NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_blocks import BlockKind
from notesmgr.note_file import template_name
from notesmgr.note_panel import PLAIN_INSTEAD, NotePanel
from notesmgr.note_text import NOT_UTF8
from notesmgr.project_ops import open_project
from notesmgr.session import Session
from notesmgr.shortcuts import ACTION_KEYS

NOTE_NAME = 'first.md.txt'
"""Name of the note that these tests show in the panel."""

NOTE_TEXT = f'This is {NOTE_NAME}.\n'
"""What the note of these tests holds, as write_notes writes it."""

TEMPLATE_TEXT = 'Template of the folder\n'
"""What the template of the project of these tests holds."""

ROW = [COPY_RAW, COPY_FORMATTED, DUPLICATE, EDIT, NEW, DELETE, MOVE_UP,
       MOVE_DOWN]
"""The buttons of the panel, in the order the README gives them."""

NO_NOTE = [label for label in ROW if label != NEW]
"""The buttons that are greyed out while no note is shown."""

LATER = 100.0
"""Seconds to put between two writes, so that the times differ."""

MARKER = 'what was on the clipboard before'
"""Text that a test puts on the clipboard to see it left alone."""

PICTURE = bytes.fromhex(
    '89504e470d0a1a0a0000000d494844520000000100000001080600000'
    '01f15c4890000000a49444154789c6300010000050001'
    '0d0a2db40000000049454e44ae426082')
"""A picture of one dot, as small a PNG file as there is."""


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


@pytest.fixture(name='errors', autouse=True)
def fixture_errors(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the panel reported to the user as a problem."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for reporting an error to the user."""
        told.append(message)
    monkeypatch.setattr(commands_module, 'show_error', record)
    return told


@pytest.fixture(name='notices')
def fixture_notices(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the panel told the user that is no failure."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for telling the user of something that was done."""
        told.append(message)
    monkeypatch.setattr(commands_module, 'show_info', record)
    return told


@pytest.fixture(name='copies', autouse=True)
def fixture_copies(monkeypatch: pytest.MonkeyPatch) -> list[RichText]:
    """Record the formatted copies, filling no real clipboard.

    The clipboard of whoever runs the tests may not be filled with
    what a test copies, so what the panel hands to the system is
    taken here instead of being handed on.
    """
    taken: list[RichText] = []
    monkeypatch.setattr(panel_module, 'copy_rich', taken.append)
    return taken


@pytest.fixture(name='offers')
def fixture_offers() -> list[frozenset[str]]:
    """Provide the list that the panel offers its actions into."""
    return []


@pytest.fixture(name='panel')
def fixture_panel(top_window: tkinter.Toplevel, session: Session,
                  offers: list[frozenset[str]]) -> NotePanel:
    """Provide a note panel wired up as the main window wires it.

    What the commands offer reaches the buttons of the panel, which
    is what the main window does with it, so that the buttons of
    these tests are offered and greyed out as they really are.
    """
    made: list[NotePanel] = []

    def offer(labels: frozenset[str]) -> None:
        """Stand in for the main window offering what can be done."""
        offers.append(labels)
        made[0].offer(labels)

    def reopen(_selected: Optional[Path]) -> None:
        """Stand in for the main window showing the project again."""
    commands = Commands(top_window, session, WindowHooks(reopen, offer))
    made.append(NotePanel(top_window, session, commands))
    return made[0]


@pytest.fixture(name='launched')
def fixture_launched(
        monkeypatch: pytest.MonkeyPatch) -> list[tuple[str, Path]]:
    """Record the editors that were asked for, starting none."""
    started: list[tuple[str, Path]] = []

    def record(command: str, path: Path) -> None:
        """Stand in for starting the editor of the project."""
        started.append((command, path))
    monkeypatch.setattr(commands_module, 'launch_editor', record)
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


def test_actions_are_the_row(panel: NotePanel) -> None:
    """What the panel says its actions are is what its buttons are."""
    assert [spec.label for spec in panel.actions()] == ROW


def test_buttons_start_dead(panel: NotePanel) -> None:
    """Before anything is selected there is nothing for a button to do."""
    assert unusable(panel) == ROW


def test_note_is_shown(panel: NotePanel, note: Path,
                       offers: list[frozenset[str]]) -> None:
    """A selected note is named and its text is shown."""
    panel.show_path(note)
    assert panel.shown_path() == str(note)
    assert panel.view.area_text() == NOTE_TEXT
    assert panel.note_path() == note
    assert EDIT in offers[-1]


def test_template_is_shown(panel: NotePanel, project: Path) -> None:
    """The template of a folder is shown and acted on like a note."""
    template = project / template_name(NoteExtension.MD_TXT)
    panel.show_path(template)
    assert panel.view.area_text() == TEMPLATE_TEXT
    assert panel.has_note()


def test_template_not_moved(panel: NotePanel, project: Path) -> None:
    """The template of a folder is not duplicated, moved or deleted."""
    panel.show_path(project / template_name(NoteExtension.MD_TXT))
    assert button_state(panel, EDIT) == 'normal'
    assert unusable(panel) == [DUPLICATE, DELETE, MOVE_UP, MOVE_DOWN]


def test_note_buttons_live(panel: NotePanel, note: Path) -> None:
    """A note to act on is what every button of the row waits for."""
    panel.show_path(note)
    assert unusable(panel) == []


def test_folder_is_no_note(panel: NotePanel, project: Path,
                           offers: list[frozenset[str]]) -> None:
    """A selected folder is named, and holds no text to show."""
    panel.show_path(project)
    assert panel.shown_path() == str(project)
    assert panel.view.area_text() == ''
    assert panel.note_path() is None
    assert offers[-1] == {NEW, NEW_FOLDER}


def test_nothing_selected(panel: NotePanel, note: Path) -> None:
    """Selecting nothing leaves the panel showing nothing again."""
    panel.show_path(note)
    panel.show_path(None)
    assert panel.shown_path() == ''
    assert panel.view.area_text() == ''
    assert unusable(panel) == NO_NOTE


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
    """A note longer than the project shows is read up to there.

    What was read is what the panel knows of the note, and it is
    what the area shows, formatted for reading in the case of a
    note written in markdown.
    """
    show_little(project, session, MIN_NOTE_SIZE)
    long_note = write_file(project / 'long.md.txt', 'a' * (MIN_NOTE_SIZE + 1))
    panel.show_path(long_note)
    assert len(panel.view.shown_note().text) == MIN_NOTE_SIZE
    assert panel.view.warning_shown()


def test_markdown_formatted(panel: NotePanel, project: Path) -> None:
    """A note written in markdown is shown formatted for reading."""
    note = write_file(project / 'formatted.md.txt', '# A heading\n')
    panel.show_path(note)
    assert panel.view.area_text() == 'A heading\n'
    tags = panel.view.area.tag_names('1.0')
    assert str(BlockKind.HEADING1) in [str(tag) for tag in tags]


def test_text_note_is_raw(panel: NotePanel, project: Path) -> None:
    """A note that says it is plain text is shown as it is written."""
    note = write_file(project / 'plain.txt', '# not a heading\n')
    panel.show_path(note)
    assert panel.view.area_text() == '# not a heading\n'
    tags = [str(tag) for tag in panel.view.area.tag_names('1.0')]
    assert str(BlockKind.HEADING1) not in tags


def test_template_formatted(panel: NotePanel, project: Path) -> None:
    """The template of a folder is shown the way a note of it is."""
    write_template(project, NoteExtension.MD_TXT, '## Template\n')
    panel.show_path(project / template_name(NoteExtension.MD_TXT))
    assert panel.view.area_text() == 'Template\n'


def test_image_beside_note(panel: NotePanel, project: Path) -> None:
    """An image of a note is looked for beside the note itself."""
    (project / 'dot.png').write_bytes(PICTURE)
    note = write_file(project / 'shows.md.txt', '![A dot](dot.png)\n')
    panel.show_path(note)
    assert len(panel.view.pictures) == 1


def test_zoom_reaches_note(panel: NotePanel, note: Path) -> None:
    """Zooming the panel draws the note it shows larger and smaller."""
    panel.show_path(note)
    started = panel.view.tags.fonts.size
    panel.zoom(2)
    assert panel.view.tags.fonts.size == started + 2
    panel.zoom_normal()
    assert panel.view.tags.fonts.size == started


def test_limit_from_project(panel: NotePanel, project: Path,
                            session: Session) -> None:
    """How much of a note is shown is what the project configured."""
    show_little(project, session, MIN_NOTE_SIZE)
    assert panel.note_limit() == MIN_NOTE_SIZE


def test_limit_no_project(top_window: tkinter.Toplevel,
                          tmp_path: Path) -> None:
    """With no project open the built-in default stands in."""
    def offer(_labels: frozenset[str]) -> None:
        """Stand in for the main window offering what can be done."""

    def reopen(_selected: Optional[Path]) -> None:
        """Stand in for the main window showing the project again."""
    session = Session(tmp_path)
    commands = Commands(top_window, session, WindowHooks(reopen, offer))
    panel = NotePanel(top_window, session, commands)
    assert panel.note_limit() == DEFAULT_NOTE_SIZE


def test_copy_raw(panel: NotePanel, note: Path) -> None:
    """Copying the note puts its text on the clipboard as it is."""
    panel.show_path(note)
    panel.copy_raw()
    assert on_clipboard(panel) == NOTE_TEXT


def test_every_action_keyed(panel: NotePanel) -> None:
    """Every action that has keys is given a command to run."""
    assert set(panel.key_commands()) == set(ACTION_KEYS)


def test_copy_key_copies_part(panel: NotePanel) -> None:
    """The copy key copies what is selected, where Copy raw copies all."""
    assert panel.key_commands()[COPY_RAW] == panel.copy_selection


def test_copy_selection(panel: NotePanel, note: Path) -> None:
    """The copy key copies what is selected of the note, and no more."""
    panel.show_path(note)
    panel.view.area.tag_add(tkinter.SEL, '1.0', '1.4')
    panel.copy_selection()
    assert on_clipboard(panel) == panel.view.area_text()[:4]


def test_copy_all_unselected(panel: NotePanel, note: Path) -> None:
    """With nothing selected the copy key copies the note as written."""
    panel.show_path(note)
    panel.copy_selection()
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


def test_copy_formatted(panel: NotePanel, note: Path,
                        copies: list[RichText]) -> None:
    """A markdown note is copied as the markup that it means."""
    panel.show_path(note)
    panel.copy_formatted()
    assert copies == [RichText(f'<p>{NOTE_TEXT.strip()}</p>', NOTE_TEXT)]


def test_formatted_plain_note(panel: NotePanel, project: Path,
                              copies: list[RichText]) -> None:
    """A note that is no markdown is copied exactly as it is written."""
    plain = write_file(project / 'plain.txt', 'col\tcol\n')
    panel.show_path(plain)
    panel.copy_formatted()
    assert copies == [RichText('<pre>col\tcol\n</pre>', 'col\tcol\n')]


def test_formatted_no_note(panel: NotePanel, copies: list[RichText]) -> None:
    """With no note selected there is nothing to copy formatted."""
    panel.copy_formatted()
    assert copies == []


def test_formatted_unread(panel: NotePanel, project: Path,
                          copies: list[RichText], errors: list[str]) -> None:
    """A note that could not be read is reported instead of copied."""
    odd = write_file(project / 'odd.md.txt')
    odd.write_bytes(b'not \xff\xfe text\n')
    panel.show_path(odd)
    panel.copy_formatted()
    assert errors == [NOT_UTF8]
    assert copies == []


def test_formatted_as_shown(panel: NotePanel, project: Path, session: Session,
                            copies: list[RichText]) -> None:
    """A note shown in part is copied formatted as far as it is shown."""
    show_little(project, session, MIN_NOTE_SIZE)
    long_note = write_file(project / 'long.md.txt', 'a' * (MIN_NOTE_SIZE + 1))
    panel.show_path(long_note)
    panel.copy_formatted()
    assert copies[0].text == 'a' * MIN_NOTE_SIZE


def test_formatted_fallback(panel: NotePanel, note: Path, notices: list[str],
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """A system that cannot carry the formatting still carries the note."""
    def refuse(_payload: RichText) -> None:
        """Stand in for a system that takes no formatted copy."""
        raise NotesmgrError('no xclip here')
    monkeypatch.setattr(panel_module, 'copy_rich', refuse)
    panel.show_path(note)
    panel.copy_formatted()
    assert on_clipboard(panel) == NOTE_TEXT
    assert notices == [PLAIN_INSTEAD.format(reason='no xclip here')]


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
    monkeypatch.setattr(commands_module, 'launch_editor', refuse)
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
                        offers: list[frozenset[str]]) -> None:
    """A note taken away by another program leaves nothing to act on."""
    panel.show_path(note)
    note.unlink()
    panel.watch.poll()
    assert panel.view.warning_shown()
    assert not panel.has_note()
    assert offers[-1] == {NEW, NEW_FOLDER}
    assert unusable(panel) == NO_NOTE


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
