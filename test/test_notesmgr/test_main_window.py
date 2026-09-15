#! /usr/local/bin/python3
"""Tests for the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Optional
import pytest
from notesmgr.main_window import (APPLICATION_NAME, EXPLORER_WIDTH,
                                  INITIAL_GEOMETRY, MINIMUM_HEIGHT,
                                  MINIMUM_WIDTH, MainWindow, Shortcut,
                                  quit_shortcut, tk_window_system)


@pytest.fixture(name='main_window')
def fixture_main_window(top_window: tkinter.Toplevel) -> MainWindow:
    """Provide a main window built in a hidden toplevel window."""
    return MainWindow(top_window)


@pytest.fixture(name='shown_window')
def fixture_shown_window(main_window: MainWindow) -> MainWindow:
    """Provide a main window that is really shown on the display.

    Only the focus-sensitive tests use this, so the normal test run
    never puts a window on the screen.
    """
    window = main_window.window
    window.deiconify()
    window.lift()
    window.focus_force()
    window.update()
    return main_window


def test_title_no_project(main_window: MainWindow) -> None:
    """A main window with no open project is titled by the program name."""
    assert main_window.window.title() == APPLICATION_NAME


@pytest.mark.parametrize('project_name,expected', [
    (None, 'notesmgr'),
    ('notes', 'notesmgr — notes'),
    ('My Notes', 'notesmgr — My Notes'),
    ('', 'notesmgr — ')])
def test_title_shows_project(main_window: MainWindow,
                             project_name: Optional[str],
                             expected: str) -> None:
    """The window title names the open project when there is one."""
    main_window.show_project(project_name)
    assert main_window.window.title() == expected


def test_minimum_size(main_window: MainWindow) -> None:
    """The main window may not be made smaller than its minimum size."""
    assert main_window.window.minsize() == (MINIMUM_WIDTH, MINIMUM_HEIGHT)


def test_panes_layout(main_window: MainWindow) -> None:
    """The explorer and the note panel are the panes, in that order."""
    shown = [str(pane) for pane in main_window.panes.winfo_children()]
    assert shown == [str(main_window.explorer), str(main_window.note_panel)]


def test_panes_side_by_side(main_window: MainWindow) -> None:
    """The explorer is placed beside the note panel, not above it."""
    assert str(main_window.panes.cget('orient')) == 'horizontal'


def test_explorer_is_narrow(main_window: MainWindow) -> None:
    """The explorer asks for the width the explorer pane is meant to have."""
    assert main_window.explorer.winfo_reqwidth() == EXPLORER_WIDTH


def test_menu_bar_installed(main_window: MainWindow) -> None:
    """The window shows a menu bar whose only menu is File."""
    window_menu = str(main_window.window.cget('menu'))
    assert window_menu == str(main_window.menu_bar)
    assert main_window.menu_bar.index('end') == 0
    assert main_window.menu_bar.entrycget(0, 'label') == 'File'


def test_file_menu_is_quit(main_window: MainWindow) -> None:
    """Quit is the only entry of the File menu."""
    assert main_window.file_menu.index('end') == 0
    assert main_window.file_menu.entrycget(0, 'label') == 'Quit'


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut('<Command-w>', 'Cmd+W')),
    ('win32', Shortcut('<Control-q>', 'Ctrl+Q')),
    ('x11', Shortcut('<Control-q>', 'Ctrl+Q')),
    ('', Shortcut('<Control-q>', 'Ctrl+Q'))])
def test_quit_shortcut(window_system: str, expected: Shortcut) -> None:
    """The shortcut is Cmd+W on macOS and Ctrl+Q on other systems."""
    assert quit_shortcut(window_system) == expected


def test_window_system_known(top_window: tkinter.Toplevel) -> None:
    """Tk reports one of the three windowing systems that it supports."""
    assert tk_window_system(top_window) in ('aqua', 'win32', 'x11')


def test_quit_accelerator(main_window: MainWindow) -> None:
    """The Quit entry shows the shortcut that the window listens for."""
    shown = main_window.file_menu.entrycget(0, 'accelerator')
    assert shown == main_window.quit_shortcut.label


def test_quit_key_bound(main_window: MainWindow) -> None:
    """The window itself listens for the shortcut, as Tk binds none."""
    assert main_window.window.bind(main_window.quit_shortcut.sequence)


def test_quit_destroys(main_window: MainWindow) -> None:
    """Quitting destroys the window."""
    main_window.quit()
    assert not main_window.window.winfo_exists()


def test_quit_from_menu(main_window: MainWindow) -> None:
    """Choosing File > Quit destroys the window."""
    window = main_window.window
    main_window.file_menu.invoke(0)
    assert not window.winfo_exists()


@pytest.mark.focus_sensitive
def test_shown_window_size(shown_window: MainWindow) -> None:
    """A shown main window gets the size it asked for."""
    assert shown_window.window.geometry().startswith(INITIAL_GEOMETRY)


@pytest.mark.focus_sensitive
def test_shown_window_panes(shown_window: MainWindow) -> None:
    """The explorer is shown narrow and to the left of the note panel."""
    explorer = shown_window.explorer
    note_panel = shown_window.note_panel
    assert explorer.winfo_x() < note_panel.winfo_x()
    assert explorer.winfo_width() < note_panel.winfo_width()


@pytest.mark.focus_sensitive
def test_window_gets_focus(shown_window: MainWindow) -> None:
    """A shown main window can take the keyboard focus."""
    window = shown_window.window
    focused = window.focus_get()
    assert focused is not None
    assert str(focused).startswith(str(window))


@pytest.mark.focus_sensitive
def test_shortcut_quits(shown_window: MainWindow) -> None:
    """Pressing the shortcut closes a main window that has the focus."""
    window = shown_window.window
    window.event_generate(shown_window.quit_shortcut.sequence, when='now')
    assert not window.winfo_exists()
