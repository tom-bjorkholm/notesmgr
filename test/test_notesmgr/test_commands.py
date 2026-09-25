#! /usr/local/bin/python3
"""Tests for what the buttons and the menu entries do."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Optional, Sequence
import pytest
from test_notesmgr.helpers import TEMPLATE_TEXT, build_project, \
    refuse_choice, write_notes
from notesmgr import commands as commands_module
from notesmgr.actions import DELETE, DELETE_FOLDER, DUPLICATE, EDIT, \
    MOVE_UP, NEW, NEW_FOLDER, RENAME_FOLDER
from notesmgr.commands import Commands, WindowHooks, folder_of, shown_folder
from notesmgr.dialogs import NameFolder
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.explorer_drop import Drop
from notesmgr.order_file import read_order_text
from notesmgr.project_ops import open_project
from notesmgr.session import Session

NOTES = ['first.md.txt', 'second.md.txt']
"""The notes that the project of these tests holds, in their order."""

TEMPLATE = 'template.md.txt'
"""What the template of every folder of these tests is called."""

EXTENSION = NoteExtension.MD_TXT
"""The extension that the notes of these tests carry."""


@pytest.fixture(name='root')
def fixture_root(tmp_path: Path) -> Path:
    """Provide a project folder holding two notes and a subfolder."""
    root = build_project(tmp_path / 'notes', NOTES)
    write_notes(root / 'sub', ['deep.md.txt'])
    return root


@pytest.fixture(name='session')
def fixture_session(root: Path) -> Session:
    """Provide a session with the project of these tests open."""
    session = Session(root)
    session.opened(open_project(root, refuse_choice).project)
    return session


@pytest.fixture(name='reopened')
def fixture_reopened() -> list[Optional[Path]]:
    """Provide the list that the commands ask to reopen into."""
    return []


@pytest.fixture(name='offers')
def fixture_offers() -> list[frozenset[str]]:
    """Provide the list that the commands offer their actions into."""
    return []


@pytest.fixture(name='errors', autouse=True)
def fixture_errors(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the commands reported to the user as an error."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for reporting an error to the user."""
        told.append(message)
    monkeypatch.setattr(commands_module, 'show_error', record)
    return told


@pytest.fixture(name='no_dialogs', autouse=True)
def fixture_no_dialogs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Let no test of this module put a real dialog on the screen."""
    answer_name(monkeypatch, None)
    answer_yes_no(monkeypatch, False)
    answer_copy(monkeypatch, None)


@pytest.fixture(name='launched', autouse=True)
def fixture_launched(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Record the notes that an editor was asked to open."""
    started: list[Path] = []

    def record(_command: str, path: Path) -> None:
        """Stand in for starting the editor of the project."""
        started.append(path)
    monkeypatch.setattr(commands_module, 'launch_editor', record)
    return started


@pytest.fixture(name='commands')
def fixture_commands(top_window: tkinter.Toplevel, session: Session,
                     reopened: list[Optional[Path]],
                     offers: list[frozenset[str]]) -> Commands:
    """Provide commands acting on the project of these tests."""
    hooks = WindowHooks(reopened.append, offers.append)
    return Commands(top_window, session, hooks)


def answer_name(monkeypatch: pytest.MonkeyPatch,
                answer: Optional[str]) -> list[str]:
    """Make the name question be answered in the given way.

    Returns:
        The names that the field held before anything was typed.
    """
    given: list[str] = []

    def asked(_parent: object, _title: str, _question: str,
              start: str = '') -> Optional[str]:
        """Stand in for asking the user for a name."""
        given.append(start)
        return answer
    monkeypatch.setattr(commands_module, 'ask_name', asked)
    return given


def answer_yes_no(monkeypatch: pytest.MonkeyPatch, answer: bool) -> None:
    """Make the yes or no question be answered in the given way."""
    def asked(_parent: object, _title: str, _question: str) -> bool:
        """Stand in for asking the user a question of yes or no."""
        return answer
    monkeypatch.setattr(commands_module, 'ask_yes_no', asked)


def answer_copy(monkeypatch: pytest.MonkeyPatch,
                answer: Optional[NameFolder]) -> list[NameFolder]:
    """Make the name and folder question be answered in the given way.

    Returns:
        What the two fields held before anything was filled in.
    """
    given: list[NameFolder] = []

    def asked(_parent: object, _title: str, start: NameFolder,
              _folders: Sequence[str]) -> Optional[NameFolder]:
        """Stand in for asking the user for a name and a folder."""
        given.append(start)
        return answer
    monkeypatch.setattr(commands_module, 'ask_name_folder', asked)
    return given


def order_of(folder: Path) -> list[str]:
    """Return the notes that the order file of a folder lists."""
    text = read_order_text(folder)
    return [] if text is None else text.splitlines()


def test_shown_folder(root: Path) -> None:
    """A folder is named by the way from the project down to it."""
    assert shown_folder(root, root) == 'notes'
    assert shown_folder(root, root / 'sub') == str(Path('notes') / 'sub')


def test_folder_of(root: Path) -> None:
    """A folder that was named to the user is that folder again."""
    for folder in (root, root / 'sub'):
        assert folder_of(root, shown_folder(root, folder)) == folder


def test_nothing_selected(commands: Commands) -> None:
    """With nothing selected there is no note and no folder to act on."""
    assert commands.plain_note() is None
    assert commands.chosen_folder() is None


def test_selected_note(commands: Commands, root: Path) -> None:
    """A selected note is a note to act on, and no folder."""
    commands.select(root / NOTES[0])
    assert commands.plain_note() == root / NOTES[0]
    assert commands.chosen_folder() is None
    assert commands.selected(True).plain


def test_selected_template(commands: Commands, root: Path) -> None:
    """The template of a folder is shown, but is not one to move."""
    commands.select(root / TEMPLATE)
    assert commands.plain_note() is None
    assert commands.selected(True).note
    assert not commands.selected(True).plain


def test_selected_folder(commands: Commands, root: Path) -> None:
    """A selected folder is a folder to act on, and no note."""
    commands.select(root / 'sub')
    assert commands.chosen_folder() == root / 'sub'
    assert commands.plain_note() is None


def test_root_is_no_folder(commands: Commands, root: Path) -> None:
    """The root folder is the project, and is not renamed or removed."""
    commands.select(root)
    assert commands.chosen_folder() is None
    assert commands.selected(False).project


def test_note_folder(commands: Commands, root: Path) -> None:
    """A new note goes where what is selected is."""
    assert commands.note_folder() == root
    commands.select(root / 'sub' / 'deep.md.txt')
    assert commands.note_folder() == root / 'sub'
    commands.select(root / 'sub')
    assert commands.note_folder() == root / 'sub'


def test_offer_told(commands: Commands, root: Path,
                    offers: list[frozenset[str]]) -> None:
    """What can be done with what is selected is told to the window."""
    commands.select(root / NOTES[0])
    commands.note_shown(True)
    assert offers[-1] >= {EDIT, DUPLICATE, DELETE, MOVE_UP, NEW}


def test_offer_for_folder(commands: Commands, root: Path,
                          offers: list[frozenset[str]]) -> None:
    """A selected folder offers what is done to a folder, and no more."""
    commands.select(root / 'sub')
    commands.note_shown(False)
    assert offers[-1] == {NEW, NEW_FOLDER, RENAME_FOLDER, DELETE_FOLDER}


def test_new_note(commands: Commands, root: Path,
                  monkeypatch: pytest.MonkeyPatch,
                  reopened: list[Optional[Path]],
                  launched: list[Path]) -> None:
    """A new note is made, shown and opened in the editor."""
    answer_name(monkeypatch, 'third')
    commands.new_note()
    made = root / 'third.md.txt'
    assert made.read_text(encoding='utf-8') == TEMPLATE_TEXT
    assert reopened == [made]
    assert launched == [made]


def test_new_note_cancelled(commands: Commands, root: Path,
                            reopened: list[Optional[Path]]) -> None:
    """A name that is not given makes no note and changes nothing."""
    commands.new_note()
    assert order_of(root) == NOTES
    assert reopened == []


def test_new_note_refused(commands: Commands, monkeypatch: pytest.MonkeyPatch,
                          errors: list[str],
                          reopened: list[Optional[Path]]) -> None:
    """A name that cannot be used is reported and nothing is made."""
    answer_name(monkeypatch, NOTES[0])
    commands.new_note()
    assert len(errors) == 1
    assert reopened == []


def test_new_note_in_folder(commands: Commands, root: Path,
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """A new note is made in the folder that is selected."""
    answer_name(monkeypatch, 'third')
    commands.select(root / 'sub')
    commands.new_note()
    assert (root / 'sub' / 'third.md.txt').is_file()


def test_duplicate(commands: Commands, root: Path,
                   monkeypatch: pytest.MonkeyPatch,
                   reopened: list[Optional[Path]]) -> None:
    """A note is copied under the name and into the folder that was given."""
    answer_copy(monkeypatch, NameFolder('copied',
                                        shown_folder(root, root / 'sub')))
    commands.select(root / NOTES[0])
    commands.duplicate_note()
    made = root / 'sub' / 'copied.md.txt'
    assert made.is_file()
    assert reopened == [made]


def test_duplicate_offers(commands: Commands, root: Path,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """The copy is offered the note's own name and its own folder."""
    given = answer_copy(monkeypatch, None)
    commands.select(root / NOTES[0])
    commands.duplicate_note()
    assert given == [NameFolder('first copy', shown_folder(root, root))]


def test_duplicate_no_note(commands: Commands, root: Path,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """The template of a folder is not one to copy into the project."""
    given = answer_copy(monkeypatch, None)
    commands.select(root / TEMPLATE)
    commands.duplicate_note()
    assert not given


def test_delete_note(commands: Commands, root: Path,
                     monkeypatch: pytest.MonkeyPatch, trashed: list[Path],
                     reopened: list[Optional[Path]]) -> None:
    """A note is taken away once the user has said so, and nothing is shown."""
    answer_yes_no(monkeypatch, True)
    commands.select(root / NOTES[0])
    commands.delete_note()
    assert trashed == [root / NOTES[0]]
    assert reopened == [None]


def test_delete_answered_no(commands: Commands, root: Path,
                            trashed: list[Path]) -> None:
    """A note is left alone when the user does not say to take it away."""
    commands.select(root / NOTES[0])
    commands.delete_note()
    assert trashed == []
    assert (root / NOTES[0]).is_file()


def test_move_up(commands: Commands, root: Path,
                 reopened: list[Optional[Path]]) -> None:
    """A note moved up changes places with the note above it."""
    commands.select(root / NOTES[1])
    commands.move_up()
    assert order_of(root) == [NOTES[1], NOTES[0]]
    assert reopened == [root / NOTES[1]]


def test_move_down(commands: Commands, root: Path) -> None:
    """A note moved down changes places with the note below it."""
    commands.select(root / NOTES[0])
    commands.move_down()
    assert order_of(root) == [NOTES[1], NOTES[0]]


def test_move_no_note(commands: Commands, root: Path,
                      reopened: list[Optional[Path]]) -> None:
    """With a folder selected there is no note to move anywhere."""
    commands.select(root / 'sub')
    commands.move_up()
    assert reopened == []


def test_drop_in_folder(commands: Commands, root: Path,
                        reopened: list[Optional[Path]]) -> None:
    """A note dropped in another folder is moved there and selected."""
    commands.drop(root / NOTES[0], Drop(root / 'sub', 0))
    assert (root / 'sub' / NOTES[0]).is_file()
    assert order_of(root / 'sub') == [NOTES[0], 'deep.md.txt']
    assert reopened == [root / 'sub' / NOTES[0]]


def test_drop_reorders(commands: Commands, root: Path,
                       reopened: list[Optional[Path]]) -> None:
    """A note dropped in its own folder is put at the place it fell."""
    commands.drop(root / NOTES[1], Drop(root, 0))
    assert order_of(root) == [NOTES[1], NOTES[0]]
    assert reopened == [root / NOTES[1]]


def test_drop_a_folder(commands: Commands, root: Path,
                       reopened: list[Optional[Path]]) -> None:
    """A folder dropped in another folder is moved into it."""
    write_notes(root / 'other', ['far.md.txt'])
    commands.drop(root / 'sub', Drop(root / 'other', None))
    assert (root / 'other' / 'sub' / 'deep.md.txt').is_file()
    assert reopened == [root / 'other' / 'sub']


def test_drop_refused(commands: Commands, root: Path, errors: list[str],
                      reopened: list[Optional[Path]]) -> None:
    """A drop that cannot be made is reported and changes nothing."""
    write_notes(root / 'sub', [NOTES[0]])
    commands.drop(root / NOTES[0], Drop(root / 'sub', 0))
    assert len(errors) == 1
    assert (root / NOTES[0]).is_file()
    assert reopened == []


def test_new_folder(commands: Commands, root: Path,
                    monkeypatch: pytest.MonkeyPatch,
                    reopened: list[Optional[Path]]) -> None:
    """A folder is made where what is selected is."""
    answer_name(monkeypatch, 'ideas')
    commands.new_folder()
    assert (root / 'ideas' / TEMPLATE).is_file()
    assert reopened == [root / 'ideas']


def test_new_folder_refused(commands: Commands,
                            monkeypatch: pytest.MonkeyPatch,
                            errors: list[str]) -> None:
    """A folder name that is taken already is reported to the user."""
    answer_name(monkeypatch, 'sub')
    commands.new_folder()
    assert len(errors) == 1


def test_rename_folder(commands: Commands, root: Path,
                       monkeypatch: pytest.MonkeyPatch,
                       reopened: list[Optional[Path]]) -> None:
    """A folder is renamed, and the folder it became is shown."""
    given = answer_name(monkeypatch, 'renamed')
    commands.select(root / 'sub')
    commands.rename_folder()
    assert given == ['sub']
    assert reopened == [root / 'renamed']


def test_rename_no_folder(commands: Commands, root: Path,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """With no folder selected there is no folder to rename."""
    given = answer_name(monkeypatch, 'renamed')
    commands.select(root / NOTES[0])
    commands.rename_folder()
    assert not given


def test_delete_folder(commands: Commands, root: Path,
                       monkeypatch: pytest.MonkeyPatch,
                       trashed: list[Path]) -> None:
    """An empty folder is taken away once the user has said so."""
    answer_name(monkeypatch, 'ideas')
    commands.new_folder()
    answer_yes_no(monkeypatch, True)
    commands.select(root / 'ideas')
    commands.delete_folder()
    assert trashed == [root / 'ideas']


def test_delete_folder_full(commands: Commands, root: Path, errors: list[str],
                            monkeypatch: pytest.MonkeyPatch,
                            trashed: list[Path]) -> None:
    """A folder holding notes is reported rather than taken away."""
    answer_yes_no(monkeypatch, True)
    commands.select(root / 'sub')
    commands.delete_folder()
    assert trashed == []
    assert len(errors) == 1


def test_edit_starts_editor(commands: Commands, root: Path,
                            launched: list[Path]) -> None:
    """Editing a note starts the editor the project is configured with."""
    commands.edit(root / NOTES[0])
    assert launched == [root / NOTES[0]]


def test_edit_failure_told(commands: Commands, root: Path, errors: list[str],
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """An editor that cannot be started is reported to the user."""
    def refuse(_command: str, _path: Path) -> None:
        """Stand in for an editor that the system does not start."""
        raise NotesmgrError('no editor here')
    monkeypatch.setattr(commands_module, 'launch_editor', refuse)
    commands.edit(root / NOTES[0])
    assert errors == ['no editor here']


def test_no_project_no_note(top_window: tkinter.Toplevel, tmp_path: Path,
                            reopened: list[Optional[Path]],
                            offers: list[frozenset[str]]) -> None:
    """With no project open there is nowhere to make a note."""
    hooks = WindowHooks(reopened.append, offers.append)
    commands = Commands(top_window, Session(tmp_path), hooks)
    commands.new_note()
    commands.new_folder()
    assert commands.note_folder() is None
    assert reopened == []


def test_edit_no_project(top_window: tkinter.Toplevel, tmp_path: Path,
                         launched: list[Path], reopened: list[Optional[Path]],
                         offers: list[frozenset[str]]) -> None:
    """With no project open there is no editor to open a note in."""
    hooks = WindowHooks(reopened.append, offers.append)
    commands = Commands(top_window, Session(tmp_path), hooks)
    commands.edit(tmp_path / NOTES[0])
    assert launched == []


def test_delete_nothing(commands: Commands, root: Path,
                        monkeypatch: pytest.MonkeyPatch,
                        trashed: list[Path]) -> None:
    """With no note selected nothing is asked and nothing taken away."""
    asked: list[str] = []

    def record(_parent: object, _title: str, question: str) -> bool:
        """Stand in for a user who would say yes to anything."""
        asked.append(question)
        return True
    monkeypatch.setattr(commands_module, 'ask_yes_no', record)
    for selected in (None, root / TEMPLATE, root / 'sub'):
        commands.select(selected)
        commands.delete_note()
    assert not asked
    assert trashed == []


def test_new_folder_cancelled(commands: Commands, root: Path,
                              reopened: list[Optional[Path]]) -> None:
    """A folder name that is not given makes no folder at all."""
    before = sorted(root.iterdir())
    commands.new_folder()
    assert sorted(root.iterdir()) == before
    assert reopened == []


def test_rename_cancelled(commands: Commands, root: Path,
                          reopened: list[Optional[Path]]) -> None:
    """A new name that is not given leaves the folder as it was."""
    commands.select(root / 'sub')
    commands.rename_folder()
    assert (root / 'sub').is_dir()
    assert reopened == []


def test_rename_refused(commands: Commands, root: Path, errors: list[str],
                        monkeypatch: pytest.MonkeyPatch,
                        reopened: list[Optional[Path]]) -> None:
    """A new name that cannot be used is reported, and nothing renamed."""
    answer_name(monkeypatch, NOTES[0])
    commands.select(root / 'sub')
    commands.rename_folder()
    assert len(errors) == 1
    assert (root / 'sub').is_dir()
    assert reopened == []


@pytest.mark.parametrize('selected', [None, NOTES[0], ''])
def test_delete_folder_none(commands: Commands, root: Path,
                            monkeypatch: pytest.MonkeyPatch,
                            trashed: list[Path],
                            selected: Optional[str]) -> None:
    """With no folder selected, the root folder included, none is taken."""
    answer_yes_no(monkeypatch, True)
    commands.select(None if selected is None else root / selected)
    commands.delete_folder()
    assert trashed == []
    assert root.is_dir()


def test_folder_answered_no(commands: Commands, root: Path,
                            monkeypatch: pytest.MonkeyPatch,
                            trashed: list[Path],
                            reopened: list[Optional[Path]]) -> None:
    """A folder is left alone when the user does not say to take it."""
    answer_name(monkeypatch, 'ideas')
    commands.new_folder()
    commands.select(root / 'ideas')
    commands.delete_folder()
    assert trashed == []
    assert (root / 'ideas').is_dir()
    assert reopened == [root / 'ideas']


def test_duplicate_refused(commands: Commands, root: Path, errors: list[str],
                           monkeypatch: pytest.MonkeyPatch,
                           reopened: list[Optional[Path]]) -> None:
    """A copy whose name is taken already is reported, and not made."""
    answer_copy(monkeypatch, NameFolder(NOTES[1].removesuffix('.md.txt'),
                                        shown_folder(root, root)))
    commands.select(root / NOTES[0])
    commands.duplicate_note()
    assert len(errors) == 1
    assert order_of(root) == NOTES
    assert reopened == []
