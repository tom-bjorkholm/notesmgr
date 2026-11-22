#! /usr/local/bin/python3
"""Tests for the menus that a right-click in the explorer shows."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Iterator, NamedTuple
import pytest
from test_notesmgr.helpers import build_project, write_notes, write_order, \
    write_template
from notesmgr import commands as commands_module
from notesmgr import main_window as window_module
from notesmgr.actions import COPY_RAW, MOVE_DOWN, RENAME
from notesmgr.config import NoteExtension
from notesmgr.main_window import ACTION_MENUS, FOLDER_MENU, NOTE_MENU, \
    MainWindow
from notesmgr.menu_bar import entry_labels
from notesmgr.order_file import read_order_text

NOTES = ['b.md.txt', 'a.md.txt']
"""Notes of the root folder of the project of these tests, in order."""

TEMPLATE = 'template.md.txt'
"""The template of a folder of the project of these tests."""

ITEMS = [NOTES[0], TEMPLATE, 'sub', '']
"""Items of the project that are right-clicked, relative to its root."""


class Popped(NamedTuple):
    """One popup menu that the main window showed, and where."""

    title: str
    x_root: int
    y_root: int


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide a project of two notes and a subfolder holding one."""
    root = build_project(tmp_path / 'notes', NOTES)
    write_notes(root / 'sub', ['deep.md.txt'])
    write_order(root / 'sub', ['deep.md.txt'])
    write_template(root / 'sub', NoteExtension.MD_TXT)
    return root


@pytest.fixture(name='nothing_told', autouse=True)
def fixture_nothing_told(monkeypatch: pytest.MonkeyPatch) -> Iterator[None]:
    """Show no dialog, and fail a test that would have shown one.

    Nothing that these tests do has anything to tell the user, so a
    message for the user is an error or a change that was not meant.
    """
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for telling the user something in a dialog."""
        told.append(message)
    for module in (window_module, commands_module):
        monkeypatch.setattr(module, 'show_error', record)
        monkeypatch.setattr(module, 'show_info', record)
    yield
    assert not told


@pytest.fixture(name='popped')
def fixture_popped(main_window: MainWindow,
                   monkeypatch: pytest.MonkeyPatch) -> list[Popped]:
    """Record the popup menus that were shown, showing none.

    A popup menu on macOS waits for the user to choose from it before
    tk_popup returns, so no test may really show one.
    """
    shown: list[Popped] = []
    for title, popup in main_window.menu_bar.popups.items():
        def record(x_root: int, y_root: int, _entry: object = '',
                   title: str = title) -> None:
            """Stand in for showing a popup menu on the screen."""
            shown.append(Popped(title, x_root, y_root))
        monkeypatch.setattr(popup, 'tk_popup', record)
    return shown


def test_popups_of_actions(main_window: MainWindow) -> None:
    """The menus that act on what is selected are the popup menus."""
    assert set(main_window.menu_bar.popups) == set(ACTION_MENUS)


@pytest.mark.parametrize('title', ACTION_MENUS)
def test_popup_like_menu(main_window: MainWindow, title: str) -> None:
    """A popup menu holds what the menu of the menu bar holds."""
    popup = main_window.menu_bar.popups[title]
    menu = main_window.menu_bar.menus[title]
    labels = entry_labels(menu)
    assert entry_labels(popup) == labels
    for label in labels:
        assert popup.entrycget(label, 'accelerator') == \
            menu.entrycget(label, 'accelerator')


def test_tree_asks_window(main_window: MainWindow) -> None:
    """A right-click in the explorer asks the window for the menu."""
    assert main_window.explorer.on_context == main_window.context_menu


@pytest.mark.parametrize('item,title', [
    (NOTES[0], NOTE_MENU), (TEMPLATE, NOTE_MENU), ('sub', FOLDER_MENU),
    ('', FOLDER_MENU)])
def test_context_menu(main_window: MainWindow, project: Path,
                      popped: list[Popped], item: str, title: str) -> None:
    """A right-clicked item is selected and its menu is shown there.

    A note and the template of a folder get the note menu, and a
    folder, the root folder of the project as well, the folder menu.
    """
    main_window.load_project(project)
    path = project / item
    main_window.context_menu(path, 10, 20)
    assert popped == [Popped(title, 10, 20)]
    assert main_window.explorer.selected_path() == path
    assert main_window.note_panel.shown_path() == str(path)


@pytest.mark.parametrize('item', ITEMS)
def test_popup_offers(main_window: MainWindow, project: Path,
                      popped: list[Popped], item: str) -> None:
    """A popup menu offers what its menu offers for the item clicked."""
    main_window.load_project(project, project / NOTES[1])
    main_window.context_menu(project / item, 10, 20)
    assert popped
    for title in ACTION_MENUS:
        popup = main_window.menu_bar.popups[title]
        menu = main_window.menu_bar.menus[title]
        for label in entry_labels(menu):
            assert popup.entrycget(label, 'state') == \
                menu.entrycget(label, 'state')


def test_template_popup(main_window: MainWindow, project: Path,
                        popped: list[Popped]) -> None:
    """The template of a folder is a note that is not renamed or moved."""
    main_window.load_project(project, project / NOTES[0])
    main_window.context_menu(project / TEMPLATE, 10, 20)
    assert popped
    popup = main_window.menu_bar.popups[NOTE_MENU]
    assert popup.entrycget(COPY_RAW, 'state') == 'normal'
    assert popup.entrycget(RENAME, 'state') == 'disabled'


def test_popup_acts(main_window: MainWindow, project: Path,
                    popped: list[Popped]) -> None:
    """Choosing from a popup menu acts on the item right-clicked."""
    main_window.load_project(project, project / NOTES[1])
    main_window.context_menu(project / NOTES[0], 10, 20)
    assert popped
    main_window.menu_bar.popups[NOTE_MENU].invoke(MOVE_DOWN)
    assert read_order_text(project) == '\n'.join(NOTES[::-1]) + '\n'
    assert main_window.explorer.selected_path() == project / NOTES[0]
