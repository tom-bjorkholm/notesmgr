#! /usr/local/bin/python3
"""The main window of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from tkinter import ttk
from typing import NamedTuple, Optional, Union

APPLICATION_NAME = 'notesmgr'
INITIAL_GEOMETRY = '1000x650'
MINIMUM_WIDTH = 640
MINIMUM_HEIGHT = 400
EXPLORER_WIDTH = 260


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
        self.quit_shortcut = quit_shortcut(tk_window_system(window))
        self.panes = ttk.PanedWindow(window, orient=tkinter.HORIZONTAL)
        self.explorer = ttk.Frame(self.panes, width=EXPLORER_WIDTH)
        self.note_panel = ttk.Frame(self.panes)
        self.menu_bar = tkinter.Menu(window)
        self.file_menu = self._add_file_menu()
        self._shape_window()
        self._bind_quit_shortcut()
        self.show_project(None)

    def _add_file_menu(self) -> tkinter.Menu:
        """Create the File menu, add it to the menu bar and return it."""
        file_menu = tkinter.Menu(self.menu_bar, tearoff=False)
        file_menu.add_command(label='Quit', command=self.quit,
                              accelerator=self.quit_shortcut.label)
        self.menu_bar.add_cascade(label='File', menu=file_menu)
        return file_menu

    def _bind_quit_shortcut(self) -> None:
        """Let the shortcut shown on the Quit entry close the window.

        Tk installs no binding for a menu accelerator, so the key
        sequence has to be bound as well. It is bound on this window
        only, so that it cannot close the main window from a dialog
        that happens to have the keyboard focus.
        """
        self.window.bind(self.quit_shortcut.sequence,
                         lambda _event: self.quit())

    def _shape_window(self) -> None:
        """Lay out the panes and give the window its size and menu bar."""
        self.panes.add(self.explorer, weight=0)
        self.panes.add(self.note_panel, weight=1)
        self.panes.pack(fill=tkinter.BOTH, expand=True)
        self.window.geometry(INITIAL_GEOMETRY)
        self.window.minsize(MINIMUM_WIDTH, MINIMUM_HEIGHT)
        self.window.configure(menu=self.menu_bar)

    def show_project(self, project_name: Optional[str]) -> None:
        """Name the open project in the window title, None meaning none."""
        if project_name is None:
            self.window.title(APPLICATION_NAME)
        else:
            self.window.title(f'{APPLICATION_NAME} — {project_name}')

    def quit(self) -> None:
        """Destroy the main window, which ends the application."""
        self.window.destroy()
