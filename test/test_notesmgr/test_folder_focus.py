#! /usr/local/bin/python3
"""Tests for focusing on the current folder and showing all folders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Optional
import pytest
from test_notesmgr.tree_folders import ALL_FOLDERS, ROOT_NOTE, build_nested, \
    open_folders
from notesmgr import main_window as window_module
from notesmgr.actions import DELETE_FOLDER, FOCUS_FOLDER, NEW_FOLDER, \
    RENAME_FOLDER, SHOW_ALL
from notesmgr.main_window import FOLDER_MENU, NOTE_MENU, MainWindow
from notesmgr.menu_bar import entry_labels
from notesmgr.shortcuts import Shortcuts, tk_window_system, window_shortcuts

FOLDER_VIEWS = [FOCUS_FOLDER, SHOW_ALL]
"""The actions that say which folders the explorer shows open."""

DEEP_NOTE = 'apple/deep/d.md.txt'
"""A note of the nested project, two folders below the root."""


def refuse_telling(_parent: object, _title: str, message: str) -> None:
    """Stand in for a message box, failing the test that shows one."""
    raise AssertionError(message)


@pytest.fixture(name='nothing_told', autouse=True)
def fixture_nothing_told(monkeypatch: pytest.MonkeyPatch) -> None:
    """Show no message box, as opening the project has nothing to tell."""
    for name in ('show_info', 'show_error'):
        monkeypatch.setattr(window_module, name, refuse_telling)


@pytest.fixture(name='root')
def fixture_root(tmp_path: Path) -> Path:
    """Provide the root of a project whose folder apple holds deep."""
    return build_nested(tmp_path / 'notes')


@pytest.fixture(name='keys')
def fixture_keys(top_window: tkinter.Toplevel) -> Shortcuts:
    """Provide every shortcut on the windowing system in use."""
    return window_shortcuts(tk_window_system(top_window))


def entry_state(main_window: MainWindow, label: str) -> str:
    """Return whether one entry of the folder menu can be chosen."""
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    return str(menu.entrycget(label, 'state'))


def test_folder_menu_order(main_window: MainWindow) -> None:
    """The folder views come last in the folder menu, below a line."""
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    assert entry_labels(menu) == [NEW_FOLDER, RENAME_FOLDER, DELETE_FOLDER,
                                  FOCUS_FOLDER, SHOW_ALL]
    above = menu.index(FOCUS_FOLDER)
    assert above is not None
    assert menu.type(above - 1) == 'separator'


@pytest.mark.parametrize('label', FOLDER_VIEWS)
def test_folder_popup_only(main_window: MainWindow, label: str) -> None:
    """A right-click on a folder offers the views, one on a note does not."""
    popups = main_window.menu_bar.popups
    assert label in entry_labels(popups[FOLDER_MENU])
    assert label not in entry_labels(popups[NOTE_MENU])


@pytest.mark.parametrize('label', FOLDER_VIEWS)
def test_dead_without_project(main_window: MainWindow, label: str) -> None:
    """With no project open there are no folders to open or close."""
    assert entry_state(main_window, label) == 'disabled'


@pytest.mark.parametrize('label', FOLDER_VIEWS)
@pytest.mark.parametrize('selected', [None, '', ROOT_NOTE, 'apple',
                                      DEEP_NOTE])
def test_live_with_project(main_window: MainWindow, root: Path, label: str,
                           selected: Optional[str]) -> None:
    """With a project open the views can be chosen whatever is selected."""
    assert main_window.load_project(
        root, None if selected is None else root / selected)
    assert entry_state(main_window, label) == 'normal'


@pytest.mark.parametrize('label', FOLDER_VIEWS)
def test_view_accelerator(main_window: MainWindow, keys: Shortcuts,
                          label: str) -> None:
    """Every folder view shows the keys that stand for it."""
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    assert str(menu.entrycget(label, 'accelerator')) == \
        keys.actions[label].label


def test_menu_focuses(main_window: MainWindow, root: Path) -> None:
    """The menu entries focus on the current folder and show all again."""
    assert main_window.load_project(root, root / DEEP_NOTE)
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    menu.invoke(FOCUS_FOLDER)
    explorer = main_window.explorer
    assert open_folders(explorer, root) == {'.', 'apple', 'apple/deep'}
    menu.invoke(SHOW_ALL)
    assert open_folders(explorer, root) == ALL_FOLDERS


def test_popup_focuses(main_window: MainWindow, root: Path) -> None:
    """The popup of a folder focuses on the folder that it was shown for.

    A right-click selects what was clicked before its popup is shown,
    and showing the popup is left out, as it waits for the user.
    """
    assert main_window.load_project(root)
    main_window.select(root / 'zebra')
    main_window.menu_bar.popups[FOLDER_MENU].invoke(FOCUS_FOLDER)
    assert open_folders(main_window.explorer, root) == {'.', 'zebra'}


def test_refresh_keeps_focus(main_window: MainWindow, root: Path) -> None:
    """Refreshing the project leaves closed the folders that were closed."""
    assert main_window.load_project(root, root / 'zebra')
    main_window.explorer.focus_selected()
    main_window.refresh()
    assert open_folders(main_window.explorer, root) == {'.', 'zebra'}
    assert main_window.explorer.selected_path() == root / 'zebra'


@pytest.mark.focus_sensitive
def test_keys_focus(shown_window: MainWindow, root: Path,
                    keys: Shortcuts) -> None:
    """The keys of the tree focus on the current folder and show all."""
    assert shown_window.load_project(root, root / DEEP_NOTE)
    tree = shown_window.explorer.tree
    tree.focus_set()
    shown_window.window.update()
    tree.event_generate(keys.actions[FOCUS_FOLDER].sequences[0], when='now')
    explorer = shown_window.explorer
    assert open_folders(explorer, root) == {'.', 'apple', 'apple/deep'}
    tree.event_generate(keys.actions[SHOW_ALL].sequences[0], when='now')
    assert open_folders(explorer, root) == ALL_FOLDERS
