#! /usr/local/bin/python3
"""The main window of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import tkinter
from pathlib import Path
from tkinter import ttk
from typing import NamedTuple, Optional, Union
from edit_cfg_json import ConfigLoadError
from edit_cfg_json_tk import TkEditorPanel
from notesmgr.config_editor import open_config_editor
from notesmgr.config_files import copy_to_user_wide
from notesmgr.dialogs import busy_cursor, show_error, show_text
from notesmgr.menu_bar import MenuEntry, MenuSpec, build_menu_bar
from notesmgr.version_info import version_report

APPLICATION_NAME = 'notesmgr'
INITIAL_GEOMETRY = '1000x650'
MINIMUM_WIDTH = 640
MINIMUM_HEIGHT = 400
EXPLORER_WIDTH = 260
FILE_MENU = 'File'
CONFIG_MENU = 'Configuration'
HELP_MENU = 'Help'
QUIT_ENTRY = 'Quit'
EDIT_CONFIG_ENTRY = 'Edit configuration…'
USER_WIDE_ENTRY = 'Save configuration as user wide…'
VERSION_ENTRY = 'Version information…'
VERSION_TITLE = 'notesmgr versions'
CONFIG_TITLE = 'Configuration'


class Shortcut(NamedTuple):
    """A keyboard shortcut: its Tk event sequence and its menu label."""

    sequence: str
    label: str


def tk_window_system(window: tkinter.Misc) -> str:
    """Return the windowing system Tk uses: aqua, win32 or x11."""
    return str(window.tk.call('tk', 'windowingsystem'))


def quit_shortcut(window_system: str) -> Shortcut:
    """Return the keyboard shortcut that closes the main window.

    macOS closes a window with Cmd+W, while Windows and the X11
    desktops leave a program with Ctrl+Q.
    """
    if window_system == 'aqua':
        return Shortcut('<Command-w>', 'Cmd+W')
    return Shortcut('<Control-q>', 'Ctrl+Q')


class MainWindow:
    """The notesmgr main window with its explorer and its note panel.

    The window is given to the constructor instead of created by it, so
    that the application can use the Tk root window while tests can use
    a hidden toplevel window under one shared Tk root.
    """

    def __init__(self, window: Union[tkinter.Tk, tkinter.Toplevel]) -> None:
        """Fill the given toplevel window with the notesmgr main window."""
        self.window = window
        self.panes = ttk.PanedWindow(window, orient=tkinter.HORIZONTAL)
        self.explorer = ttk.Frame(self.panes, width=EXPLORER_WIDTH)
        self.note_panel = ttk.Frame(self.panes)
        self.project_config: Optional[Path] = None
        self.config_panel: Optional[TkEditorPanel] = None
        shortcut = quit_shortcut(tk_window_system(window))
        self.menu_bar = build_menu_bar(window, self._menu_specs(shortcut))
        self._shape_window()
        self._bind_quit_shortcut(shortcut)
        self.show_project(None)

    def _menu_specs(self, shortcut: Shortcut) -> list[MenuSpec]:
        """Return the menus of the main window and what they hold.

        Copying the configuration to the user wide location asks for a
        project configuration file to copy, so it is greyed out until
        a project is open.
        """
        quit_entry = MenuEntry(QUIT_ENTRY, self.quit, shortcut.label)
        edit_entry = MenuEntry(EDIT_CONFIG_ENTRY, self.edit_configuration)
        user_wide = MenuEntry(USER_WIDE_ENTRY, self.save_user_wide,
                              enabled=False)
        versions = MenuEntry(VERSION_ENTRY, self.show_version)
        return [MenuSpec(FILE_MENU, [quit_entry]),
                MenuSpec(CONFIG_MENU, [edit_entry, user_wide]),
                MenuSpec(HELP_MENU, [versions])]

    def _bind_quit_shortcut(self, shortcut: Shortcut) -> None:
        """Let the shortcut shown on the Quit entry close the window.

        Tk installs no binding for a menu accelerator, so the key
        sequence has to be bound as well. It is bound on this window
        only, so that it cannot close the main window from a dialog
        that happens to have the keyboard focus.
        """
        self.window.bind(shortcut.sequence, lambda _event: self.quit())

    def _shape_window(self) -> None:
        """Lay out the panes and give the window its size."""
        self.panes.add(self.explorer, weight=0)
        self.panes.add(self.note_panel, weight=1)
        self.panes.pack(fill=tkinter.BOTH, expand=True)
        self.window.geometry(INITIAL_GEOMETRY)
        self.window.minsize(MINIMUM_WIDTH, MINIMUM_HEIGHT)

    def show_project(self, project_name: Optional[str]) -> None:
        """Name the open project in the window title, None meaning none."""
        if project_name is None:
            self.window.title(APPLICATION_NAME)
        else:
            self.window.title(f'{APPLICATION_NAME} — {project_name}')

    def edit_configuration(self) -> None:
        """Open the editor of the user wide configuration.

        One session at a time is enough, and the editor holds the
        application while it is open, so a second one is not started.
        """
        if self.config_panel is not None:
            return
        try:
            self.config_panel = open_config_editor(self.window,
                                                   self._config_closed)
        except ConfigLoadError as error:
            show_error(self.window, CONFIG_TITLE, str(error))

    def _config_closed(self) -> None:
        """Forget the configuration editor once its session has ended."""
        self.config_panel = None

    def save_user_wide(self) -> None:
        """Copy the project's configuration to the user wide file."""
        if self.project_config is None:
            return
        try:
            copy_to_user_wide(self.project_config)
        except OSError as error:
            show_error(self.window, CONFIG_TITLE, str(error))

    def show_version(self) -> None:
        """Show what notesmgr and the packages below it are.

        Gathering the report asks PyPI whether there are newer
        releases, which takes a moment, so the window says that it is
        working while that is going on.
        """
        report = io.StringIO()
        with busy_cursor(self.window):
            version_report(report)
        show_text(self.window, VERSION_TITLE, report.getvalue())

    def quit(self) -> None:
        """Destroy the main window, which ends the application."""
        self.window.destroy()
