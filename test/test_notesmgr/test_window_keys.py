#! /usr/local/bin/python3
"""Tests for the keys the main window listens for and the size it draws."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
import pytest
from test_notesmgr.helpers import build_project
from notesmgr.actions import MOVE_DOWN, NEW_FOLDER
from notesmgr.main_window import FILE_MENU, FOLDER_MENU, NORMAL_SIZE_ENTRY, \
    NOTE_MENU, QUIT_ENTRY, VIEW_MENU, ZOOM_IN_ENTRY, ZOOM_OUT_ENTRY, \
    ZOOM_STEP, MainWindow, handled
from notesmgr.menu_bar import entry_labels
from notesmgr.order_file import read_order_text
from notesmgr.shortcuts import TREE_EDIT_KEYS, Shortcut, Shortcuts, \
    quit_shortcut, tk_window_system, window_shortcuts


@pytest.fixture(name='shortcut')
def fixture_shortcut(top_window: tkinter.Toplevel) -> Shortcut:
    """Provide the shortcut that quits on the windowing system in use."""
    return quit_shortcut(tk_window_system(top_window))


@pytest.fixture(name='keys')
def fixture_keys(top_window: tkinter.Toplevel) -> Shortcuts:
    """Provide every shortcut on the windowing system in use."""
    return window_shortcuts(tk_window_system(top_window))


@pytest.mark.parametrize('entry', [ZOOM_IN_ENTRY, ZOOM_OUT_ENTRY,
                                   NORMAL_SIZE_ENTRY])
def test_view_accelerators(main_window: MainWindow, keys: Shortcuts,
                           entry: str) -> None:
    """Every entry of the view menu shows the keys that stand for it."""
    menu = main_window.menu_bar.menus[VIEW_MENU]
    labels = {keys.larger.label, keys.smaller.label, keys.normal.label}
    assert str(menu.entrycget(entry, 'accelerator')) in labels


def test_view_entries_live(main_window: MainWindow) -> None:
    """How large a note is drawn can be said whatever is selected."""
    menu = main_window.menu_bar.menus[VIEW_MENU]
    for entry in (ZOOM_IN_ENTRY, ZOOM_OUT_ENTRY, NORMAL_SIZE_ENTRY):
        assert str(menu.entrycget(entry, 'state')) == 'normal'


def note_size_of(main_window: MainWindow) -> int:
    """Return the size that the note panel draws a note in."""
    return main_window.note_panel.view.tags.fonts.size


def tree_size_of(main_window: MainWindow) -> int:
    """Return the size that the explorer draws the names of items in."""
    return main_window.explorer.font.size


def test_zoom_menu_entries(main_window: MainWindow) -> None:
    """The entries of the view menu draw the note larger and smaller."""
    menu = main_window.menu_bar.menus[VIEW_MENU]
    started = note_size_of(main_window)
    menu.invoke(ZOOM_IN_ENTRY)
    assert note_size_of(main_window) == started + ZOOM_STEP
    menu.invoke(ZOOM_OUT_ENTRY)
    assert note_size_of(main_window) == started
    menu.invoke(ZOOM_IN_ENTRY)
    menu.invoke(NORMAL_SIZE_ENTRY)
    assert note_size_of(main_window) == started


def test_zoom_reaches_tree(main_window: MainWindow) -> None:
    """The explorer is drawn larger and smaller along with the note."""
    menu = main_window.menu_bar.menus[VIEW_MENU]
    started = tree_size_of(main_window)
    menu.invoke(ZOOM_IN_ENTRY)
    assert tree_size_of(main_window) == started + ZOOM_STEP
    menu.invoke(ZOOM_OUT_ENTRY)
    menu.invoke(ZOOM_OUT_ENTRY)
    assert tree_size_of(main_window) == started - ZOOM_STEP
    menu.invoke(NORMAL_SIZE_ENTRY)
    assert tree_size_of(main_window) == started


def test_one_size_for_both(main_window: MainWindow) -> None:
    """The note and the names beside it are drawn in one size."""
    assert tree_size_of(main_window) == note_size_of(main_window)
    main_window.zoom(2)
    assert tree_size_of(main_window) == note_size_of(main_window)


def test_zoom_keys_bound(main_window: MainWindow, keys: Shortcuts) \
        -> None:
    """The window listens for every key that asks for another size."""
    for shortcut in (keys.larger, keys.smaller, keys.normal):
        for sequence in shortcut.sequences:
            assert main_window.window.bind(sequence)


def test_quit_accelerator(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The Quit entry shows the shortcut that the window listens for."""
    menu = main_window.menu_bar.menus[FILE_MENU]
    assert menu.entrycget(QUIT_ENTRY, 'accelerator') == shortcut.label


def test_quit_key_bound(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The window itself listens for the shortcut, as Tk binds none."""
    assert all(main_window.window.bind(sequence)
               for sequence in shortcut.sequences)


def test_quit_destroys(main_window: MainWindow) -> None:
    """Quitting destroys the window."""
    main_window.quit()
    assert not main_window.window.winfo_exists()


def test_quit_from_menu(main_window: MainWindow) -> None:
    """Choosing File > Quit destroys the window."""
    window = main_window.window
    main_window.menu_bar.menus[FILE_MENU].invoke(QUIT_ENTRY)
    assert not window.winfo_exists()


@pytest.mark.focus_sensitive
def test_shortcut_quits(shown_window: MainWindow, shortcut: Shortcut) -> None:
    """Pressing the shortcut closes a main window that has the focus."""
    window = shown_window.window
    window.event_generate(shortcut.sequences[0], when='now')
    assert not window.winfo_exists()


def test_note_accelerators(main_window: MainWindow, keys: Shortcuts) \
        -> None:
    """Every entry of the note menu shows the keys that stand for it."""
    menu = main_window.menu_bar.menus[NOTE_MENU]
    for label in entry_labels(menu):
        shown = str(menu.entrycget(label, 'accelerator'))
        assert shown == keys.actions[label].label


def test_folder_accelerator(main_window: MainWindow, keys: Shortcuts) \
        -> None:
    """The entry that makes a folder shows the keys that make one."""
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    shown = str(menu.entrycget(NEW_FOLDER, 'accelerator'))
    assert shown == keys.actions[NEW_FOLDER].label


def test_action_keys_bound(main_window: MainWindow, keys: Shortcuts) \
        -> None:
    """Both the window and the tree listen for the keys of an action.

    The tree moves its selection on an arrow key whatever is held
    with it, so it has to be told of the keys itself to leave that be.
    """
    tree = main_window.explorer.tree
    for shortcut in keys.actions.values():
        for sequence in shortcut.sequences:
            assert main_window.window.bind(sequence)
            assert tree.bind(sequence)


def test_tree_edit_keys(main_window: MainWindow) -> None:
    """The tree listens for Return, which edits the selected note."""
    tree = main_window.explorer.tree
    assert all(tree.bind(sequence) for sequence in TREE_EDIT_KEYS)


def test_handled_ends_the_key() -> None:
    """A key that ran its command is handled no further by Tk."""
    ran: list[bool] = []
    assert handled(lambda: ran.append(True), tkinter.Event()) == 'break'
    assert ran == [True]


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide a project holding the notes b and a, in that order."""
    return build_project(tmp_path / 'notes', ['b.md.txt', 'a.md.txt'])


@pytest.mark.focus_sensitive
def test_focus_starts_in_tree(main_window: MainWindow) -> None:
    """The keyboard works the explorer as soon as the window is shown.

    Tk gives a window that is not on the screen no focus, and keeps it
    for when the window is shown, so the window is shown here without
    forcing the focus on it the way the shown window of a test is.
    """
    window = main_window.window
    window.deiconify()
    window.update()
    assert window.focus_lastfor() == main_window.explorer.tree


@pytest.mark.focus_sensitive
def test_tab_order(shown_window: MainWindow, project: Path) -> None:
    """Tab goes from the explorer to the buttons and then to the note."""
    shown_window.load_project(project, project / 'b.md.txt')
    shown_window.window.update()
    tree = shown_window.explorer.tree
    visited: list[str] = []
    widget = tree.tk_focusNext()
    while widget is not None and widget != tree:
        visited.append(widget.winfo_class())
        widget = widget.tk_focusNext()
    assert widget == tree
    assert visited[0] == 'TButton'
    assert visited[-1] == 'Text'
    assert set(visited) == {'TButton', 'Text'}


@pytest.mark.focus_sensitive
def test_key_moves_note(shown_window: MainWindow, project: Path,
                        keys: Shortcuts) -> None:
    """The key of Down moves the note, and not the selection of the tree."""
    note = project / 'b.md.txt'
    shown_window.load_project(project, note)
    tree = shown_window.explorer.tree
    tree.focus_set()
    shown_window.window.update()
    tree.event_generate(keys.actions[MOVE_DOWN].sequences[0], when='now')
    shown_window.window.update()
    assert read_order_text(project) == 'a.md.txt\nb.md.txt\n'
    assert shown_window.explorer.selected_path() == note
