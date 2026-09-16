#! /usr/local/bin/python3
"""Tests for the keys the main window listens for and the size it draws."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from notesmgr.main_window import FILE_MENU, NORMAL_SIZE_ENTRY, QUIT_ENTRY, \
    VIEW_MENU, ZOOM_IN_ENTRY, ZOOM_OUT_ENTRY, ZOOM_STEP, MainWindow, \
    Shortcut, Shortcuts, held_shortcut, modifier, quit_shortcut, \
    tk_window_system, window_shortcuts


@pytest.fixture(name='shortcut')
def fixture_shortcut(top_window: tkinter.Toplevel) -> Shortcut:
    """Provide the shortcut that quits on the windowing system in use."""
    return quit_shortcut(tk_window_system(top_window))


@pytest.fixture(name='keys')
def fixture_keys(top_window: tkinter.Toplevel) -> Shortcuts:
    """Provide every shortcut on the windowing system in use."""
    return window_shortcuts(tk_window_system(top_window))


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut(('<Command-w>',), 'Cmd+W')),
    ('win32', Shortcut(('<Control-q>',), 'Ctrl+Q')),
    ('x11', Shortcut(('<Control-q>',), 'Ctrl+Q')),
    ('', Shortcut(('<Control-q>',), 'Ctrl+Q'))])
def test_quit_shortcut(window_system: str, expected: Shortcut) -> None:
    """The shortcut is Cmd+W on macOS and Ctrl+Q on other systems."""
    assert quit_shortcut(window_system) == expected


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', ('Command', 'Cmd')),
    ('win32', ('Control', 'Ctrl')),
    ('x11', ('Control', 'Ctrl')),
    ('', ('Control', 'Ctrl'))])
def test_modifier(window_system: str, expected: tuple[str, str]) \
        -> None:
    """The command key holds macOS, and the control key the rest."""
    assert modifier(window_system) == expected


def test_held_shortcut() -> None:
    """A shortcut binds every key that stands for it and shows one."""
    shortcut = held_shortcut('aqua', ('plus', 'KP_Add'), '+')
    assert shortcut == Shortcut(('<Command-plus>', '<Command-KP_Add>'),
                                'Cmd++')


@pytest.mark.parametrize('window_system', ['aqua', 'win32', 'x11'])
def test_zoom_shortcuts(window_system: str) -> None:
    """Every way of asking for another size has keys of its own."""
    keys = window_shortcuts(window_system)
    zooming = (keys.larger, keys.smaller, keys.normal)
    assert all(shortcut.sequences for shortcut in zooming)
    assert len({shortcut.label for shortcut in zooming}) == 3
    bound = [sequence for shortcut in zooming
             for sequence in shortcut.sequences]
    assert len(set(bound)) == len(bound)


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


def test_window_system_known(top_window: tkinter.Toplevel) -> None:
    """Tk reports one of the three windowing systems that it supports."""
    assert tk_window_system(top_window) in ('aqua', 'win32', 'x11')


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
