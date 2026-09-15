#! /usr/local/bin/python3
"""Tests for the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Callable, NamedTuple, Optional, TextIO
import pytest
from edit_cfg_json import ConfigLoadError
from notesmgr import main_window as window_module
from notesmgr.config_files import CONFIG_NAME
from notesmgr.main_window import APPLICATION_NAME, CONFIG_MENU, \
    EDIT_CONFIG_ENTRY, EXPLORER_WIDTH, FILE_MENU, HELP_MENU, \
    INITIAL_GEOMETRY, MINIMUM_HEIGHT, MINIMUM_WIDTH, QUIT_ENTRY, \
    USER_WIDE_ENTRY, VERSION_ENTRY, VERSION_TITLE, MainWindow, Shortcut, \
    quit_shortcut, tk_window_system

REPORT = 'notesmgr 0.0.1\n'
"""What the version report says in these tests."""

PROJECT_TEXT = '{"editor": "vi", "file_extension": "MD"}'
"""Content of the project configuration file in these tests."""


class ShownText(NamedTuple):
    """One text that the main window asked to have shown."""

    title: str
    text: str


@pytest.fixture(name='main_window')
def fixture_main_window(top_window: tkinter.Toplevel) -> MainWindow:
    """Provide a main window built in a hidden toplevel window."""
    return MainWindow(top_window)


@pytest.fixture(name='shortcut')
def fixture_shortcut(top_window: tkinter.Toplevel) -> Shortcut:
    """Provide the shortcut that quits on the windowing system in use."""
    return quit_shortcut(tk_window_system(top_window))


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


@pytest.fixture(name='panels')
def fixture_panels(monkeypatch: pytest.MonkeyPatch
                   ) -> list[Callable[[], None]]:
    """Record the editor sessions that were asked for, opening none."""
    opened: list[Callable[[], None]] = []

    def record(_parent: tkinter.Misc, on_close: Callable[[], None]) -> object:
        """Stand in for opening the configuration editor panel."""
        opened.append(on_close)
        return object()
    monkeypatch.setattr(window_module, 'open_config_editor', record)
    return opened


@pytest.fixture(name='refused')
def fixture_refused(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the main window reported to the user as an error."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for reporting an error to the user."""
        told.append(message)
    monkeypatch.setattr(window_module, 'show_error', record)
    return told


@pytest.fixture(name='shown_texts')
def fixture_shown_texts(monkeypatch: pytest.MonkeyPatch) -> list[ShownText]:
    """Record the texts the main window asked to have shown in a window."""
    shown: list[ShownText] = []

    def record(_parent: object, title: str, text: str) -> None:
        """Stand in for showing a text in a window of its own."""
        shown.append(ShownText(title, text))

    def report(out_file: TextIO) -> None:
        """Stand in for gathering the version report, which is slow."""
        out_file.write(REPORT)
    monkeypatch.setattr(window_module, 'show_text', record)
    monkeypatch.setattr(window_module, 'version_report', report)
    return shown


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
    """The window shows the menu bar that was built for it."""
    window_menu = str(main_window.window.cget('menu'))
    assert window_menu == str(main_window.menu_bar.widget)


def test_menus_of_the_bar(main_window: MainWindow) -> None:
    """The menu bar holds a File, a Configuration and a Help menu."""
    assert set(main_window.menu_bar.menus) == {FILE_MENU, CONFIG_MENU,
                                               HELP_MENU}


@pytest.mark.parametrize('menu,label', [
    (FILE_MENU, QUIT_ENTRY),
    (CONFIG_MENU, EDIT_CONFIG_ENTRY),
    (CONFIG_MENU, USER_WIDE_ENTRY),
    (HELP_MENU, VERSION_ENTRY)])
def test_menu_entries(main_window: MainWindow, menu: str, label: str) -> None:
    """Every menu holds the entries that this step has given it."""
    assert main_window.menu_bar.menus[menu].index(label) is not None


def test_user_wide_disabled(main_window: MainWindow) -> None:
    """Copying to the user wide file waits until a project is open."""
    menu = main_window.menu_bar.menus[CONFIG_MENU]
    assert menu.entrycget(USER_WIDE_ENTRY, 'state') == 'disabled'


def test_edit_config_offered(main_window: MainWindow) -> None:
    """Editing the configuration can be chosen with no project open."""
    menu = main_window.menu_bar.menus[CONFIG_MENU]
    assert menu.entrycget(EDIT_CONFIG_ENTRY, 'state') == 'normal'


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


def test_quit_accelerator(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The Quit entry shows the shortcut that the window listens for."""
    menu = main_window.menu_bar.menus[FILE_MENU]
    assert menu.entrycget(QUIT_ENTRY, 'accelerator') == shortcut.label


def test_quit_key_bound(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The window itself listens for the shortcut, as Tk binds none."""
    assert main_window.window.bind(shortcut.sequence)


def test_quit_destroys(main_window: MainWindow) -> None:
    """Quitting destroys the window."""
    main_window.quit()
    assert not main_window.window.winfo_exists()


def test_quit_from_menu(main_window: MainWindow) -> None:
    """Choosing File > Quit destroys the window."""
    window = main_window.window
    main_window.menu_bar.menus[FILE_MENU].invoke(QUIT_ENTRY)
    assert not window.winfo_exists()


def test_editor_opened(main_window: MainWindow,
                       panels: list[Callable[[], None]]) -> None:
    """Choosing to edit the configuration opens one editor session."""
    main_window.menu_bar.menus[CONFIG_MENU].invoke(EDIT_CONFIG_ENTRY)
    assert len(panels) == 1
    assert main_window.config_panel is not None


def test_one_editor_at_a_time(main_window: MainWindow,
                              panels: list[Callable[[], None]]) -> None:
    """A second editor is not opened while the first one is still open."""
    main_window.edit_configuration()
    main_window.edit_configuration()
    assert len(panels) == 1


def test_editor_reopened(main_window: MainWindow,
                         panels: list[Callable[[], None]]) -> None:
    """Once a session has ended, the editor can be opened again."""
    main_window.edit_configuration()
    panels[0]()
    assert main_window.config_panel is None
    main_window.edit_configuration()
    assert len(panels) == 2


def test_editor_refused(main_window: MainWindow, refused: list[str],
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """A configuration file that cannot be edited is reported, not raised."""
    def refuse(_parent: tkinter.Misc, _on_close: Callable[[], None]) -> object:
        """Stand in for an editor that refuses the configuration file."""
        raise ConfigLoadError('the file holds no configuration')
    monkeypatch.setattr(window_module, 'open_config_editor', refuse)
    main_window.edit_configuration()
    assert refused == ['the file holds no configuration']
    assert main_window.config_panel is None


def test_user_wide_without(main_window: MainWindow, home: Path) -> None:
    """With no project open there is no configuration file to copy."""
    main_window.save_user_wide()
    assert not (home / CONFIG_NAME).exists()


def test_user_wide_copied(main_window: MainWindow, home: Path,
                          tmp_path: Path) -> None:
    """The project's configuration file becomes the user wide one."""
    project = tmp_path / 'notesmgr.cfg'
    project.write_text(PROJECT_TEXT, encoding='utf-8')
    main_window.project_config = project
    main_window.save_user_wide()
    assert (home / CONFIG_NAME).read_text(encoding='utf-8') == PROJECT_TEXT


def test_user_wide_refused(main_window: MainWindow, refused: list[str],
                           tmp_path: Path) -> None:
    """A copy that cannot be made is reported, and does not raise."""
    main_window.project_config = tmp_path / 'no_such.cfg'
    main_window.save_user_wide()
    assert len(refused) == 1


def test_version_shown(main_window: MainWindow,
                       shown_texts: list[ShownText]) -> None:
    """Choosing version information shows the report in a window."""
    main_window.menu_bar.menus[HELP_MENU].invoke(VERSION_ENTRY)
    assert shown_texts == [ShownText(VERSION_TITLE, REPORT)]


def test_cursor_after_version(main_window: MainWindow,
                              shown_texts: list[ShownText]) -> None:
    """The waiting cursor is gone once the report has been gathered."""
    main_window.show_version()
    assert len(shown_texts) == 1
    assert str(main_window.window.cget('cursor')) == ''


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
def test_shortcut_quits(shown_window: MainWindow, shortcut: Shortcut) -> None:
    """Pressing the shortcut closes a main window that has the focus."""
    window = shown_window.window
    window.event_generate(shortcut.sequence, when='now')
    assert not window.winfo_exists()
