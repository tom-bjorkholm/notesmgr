#! /usr/local/bin/python3
"""The main window of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import tkinter
from functools import partial
from pathlib import Path
from tkinter import ttk
from typing import AbstractSet, Callable, NamedTuple, Optional, Sequence, \
    Union
from edit_cfg_json import ConfigLoadError
from edit_cfg_json_tk import TkEditorPanel
from notesmgr.actions import DELETE_FOLDER, NEW_FOLDER, RENAME_FOLDER
from notesmgr.commands import Commands, WindowHooks
from notesmgr.config_editor import open_config_editor
from notesmgr.config_files import copy_to_user_wide
from notesmgr.dialogs import ask_choice, ask_folder, ask_yes_no, \
    busy_cursor, show_error, show_info, show_text
from notesmgr.errors import NotesmgrError
from notesmgr.explorer_tree import ExplorerTree
from notesmgr.menu_bar import MenuEntry, MenuSpec, build_menu_bar, \
    entry_labels, set_enabled
from notesmgr.note_panel import NotePanel
from notesmgr.project import is_project
from notesmgr.project_ops import OpenReport, changed_message, \
    create_project, open_project
from notesmgr.session import Session
from notesmgr.version_info import version_report

APPLICATION_NAME = 'notesmgr'
INITIAL_GEOMETRY = '1000x650'
MINIMUM_WIDTH = 640
MINIMUM_HEIGHT = 400
FILE_MENU = 'File'
NOTE_MENU = 'Note'
FOLDER_MENU = 'Folder'
VIEW_MENU = 'View'
CONFIG_MENU = 'Configuration'
HELP_MENU = 'Help'
NEW_PROJECT_ENTRY = 'New project…'
OPEN_PROJECT_ENTRY = 'Open project…'
QUIT_ENTRY = 'Quit'
ZOOM_IN_ENTRY = 'Larger text'
ZOOM_OUT_ENTRY = 'Smaller text'
NORMAL_SIZE_ENTRY = 'Normal text size'
ZOOM_STEP = 1
ZOOM_IN_KEYS = ('plus', 'equal', 'KP_Add')
ZOOM_OUT_KEYS = ('minus', 'KP_Subtract')
NORMAL_SIZE_KEYS = ('Key-0', 'KP_0')
EDIT_CONFIG_ENTRY = 'Edit configuration…'
USER_WIDE_ENTRY = 'Save configuration as user wide…'
VERSION_ENTRY = 'Version information…'
VERSION_TITLE = 'notesmgr versions'
CONFIG_TITLE = 'Configuration'
PROJECT_TITLE = 'Project'
TEMPLATE_TITLE = 'Templates'
NEW_PROJECT_TITLE = 'Folder to make into a notesmgr project'
OPEN_PROJECT_TITLE = 'notesmgr project folder to open'
OFFER_OPEN = 'The folder {folder} is a notesmgr project already.\n' \
    'Open that project?'
TEMPLATE_QUESTION = 'The folder {folder} holds more than one template.\n' \
    'Which one is to be kept? The others are moved to the trash, and\n' \
    'the one that is kept is given the file extension of the project.'


class Shortcut(NamedTuple):
    """A keyboard shortcut: its Tk event sequences and its menu label.

    A shortcut has more than one sequence wherever more than one key
    stands for it, such as the plus of the keypad and the plus that
    is typed with the shift key held down.
    """

    sequences: tuple[str, ...]
    label: str


class Shortcuts(NamedTuple):
    """The keyboard shortcuts that the main window listens for."""

    quit: Shortcut
    larger: Shortcut
    smaller: Shortcut
    normal: Shortcut


def tk_window_system(window: tkinter.Misc) -> str:
    """Return the windowing system Tk uses: aqua, win32 or x11."""
    return str(window.tk.call('tk', 'windowingsystem'))


def quit_shortcut(window_system: str) -> Shortcut:
    """Return the keyboard shortcut that closes the main window.

    macOS closes a window with Cmd+W, while Windows and the X11
    desktops leave a program with Ctrl+Q.
    """
    if window_system == 'aqua':
        return Shortcut(('<Command-w>',), 'Cmd+W')
    return Shortcut(('<Control-q>',), 'Ctrl+Q')


def modifier(window_system: str) -> tuple[str, str]:
    """Return the key held down for a shortcut, and what it is called.

    macOS holds the command key down where Windows and the X11
    desktops hold the control key down.
    """
    if window_system == 'aqua':
        return ('Command', 'Cmd')
    return ('Control', 'Ctrl')


def held_shortcut(window_system: str, keysyms: Sequence[str],
                  shown: str) -> Shortcut:
    """Return a shortcut of the held key and the keys that stand for it.

    Args:
        window_system: The windowing system that Tk is using.
        keysyms: What Tk calls each of the keys that stand for it.
        shown: What the key is called on the menu entry.

    Returns:
        The shortcut to bind and to show.
    """
    held, name = modifier(window_system)
    sequences = tuple(f'<{held}-{keysym}>' for keysym in keysyms)
    return Shortcut(sequences, f'{name}+{shown}')


def window_shortcuts(window_system: str) -> Shortcuts:
    """Return the shortcuts of the main window on a windowing system.

    Making a note larger is asked for with a plus, which is typed
    with the shift key held down on most keyboards and is a key of
    its own on the keypad, so every key that stands for it is bound
    and the plainest of them is the one that is shown.
    """
    return Shortcuts(
        quit=quit_shortcut(window_system),
        larger=held_shortcut(window_system, ZOOM_IN_KEYS, '+'),
        smaller=held_shortcut(window_system, ZOOM_OUT_KEYS, '-'),
        normal=held_shortcut(window_system, NORMAL_SIZE_KEYS, '0'))


class MainWindow:
    """The notesmgr main window with its explorer and its note panel.

    The window is given to the constructor instead of created by it, so
    that the application can use the Tk root window while tests can use
    a hidden toplevel window under one shared Tk root.
    """

    def __init__(self, window: Union[tkinter.Tk, tkinter.Toplevel]) -> None:
        """Fill the given toplevel window with the notesmgr main window."""
        self.window = window
        self.session = Session()
        self.panes = ttk.PanedWindow(window, orient=tkinter.HORIZONTAL)
        self.explorer = ExplorerTree(self.panes, self.show_selected)
        hooks = WindowHooks(self.reopen, self.offer_actions)
        commands = Commands(window, self.session, hooks)
        self.note_panel = NotePanel(self.panes, self.session, commands)
        self.config_panel: Optional[TkEditorPanel] = None
        keys = window_shortcuts(tk_window_system(window))
        self.menu_bar = build_menu_bar(window, self._menu_specs(keys))
        self._shape_window()
        self._bind_shortcuts(keys)
        self.show_project(None)

    def _menu_specs(self, keys: Shortcuts) -> list[MenuSpec]:
        """Return the menus of the main window and what they hold.

        The entries that act on a note need a note to act on, the
        entries that act on a folder need a folder, and copying the
        configuration to the user wide location asks for a project
        configuration file to copy, so all of them are greyed out
        until what they need is selected.
        """
        new_entry = MenuEntry(NEW_PROJECT_ENTRY, self.new_project_dialog)
        open_entry = MenuEntry(OPEN_PROJECT_ENTRY, self.open_project_dialog)
        quit_entry = MenuEntry(QUIT_ENTRY, self.quit, keys.quit.label)
        edit_entry = MenuEntry(EDIT_CONFIG_ENTRY, self.edit_configuration)
        user_wide = MenuEntry(USER_WIDE_ENTRY, self.save_user_wide,
                              enabled=False)
        versions = MenuEntry(VERSION_ENTRY, self.show_version)
        return [MenuSpec(FILE_MENU, [new_entry, open_entry, quit_entry]),
                MenuSpec(NOTE_MENU, self._note_entries()),
                MenuSpec(FOLDER_MENU, self._folder_entries()),
                MenuSpec(VIEW_MENU, self._view_entries(keys)),
                MenuSpec(CONFIG_MENU, [edit_entry, user_wide]),
                MenuSpec(HELP_MENU, [versions])]

    def _note_entries(self) -> list[MenuEntry]:
        """Return one entry of the note menu for every working button.

        The note menu and the button row do the same things, so they
        are described in one place, which is the panel that holds the
        buttons. A button whose operation belongs to a later step of
        the plan has nothing to do yet, and is left out of the menu
        until it has.
        """
        return [MenuEntry(spec.label, spec.command, enabled=False)
                for spec in self.note_panel.actions()
                if spec.command is not None]

    def _folder_entries(self) -> list[MenuEntry]:
        """Return the entries that act on a folder of the project."""
        commands = self.note_panel.commands
        return [MenuEntry(NEW_FOLDER, commands.new_folder, enabled=False),
                MenuEntry(RENAME_FOLDER, commands.rename_folder,
                          enabled=False),
                MenuEntry(DELETE_FOLDER, commands.delete_folder,
                          enabled=False)]

    def _view_entries(self, keys: Shortcuts) -> list[MenuEntry]:
        """Return the entries that say how large a note is drawn.

        A note is read on whatever screen the user has, so how large
        it is drawn is theirs to say, and it can always be said
        however small or large the note itself is.
        """
        return [MenuEntry(ZOOM_IN_ENTRY, self._zoom_command(ZOOM_STEP),
                          keys.larger.label),
                MenuEntry(ZOOM_OUT_ENTRY, self._zoom_command(-ZOOM_STEP),
                          keys.smaller.label),
                MenuEntry(NORMAL_SIZE_ENTRY, self._normal_command(),
                          keys.normal.label)]

    def _zoom_command(self, step: int) -> Callable[[], None]:
        """Return what draws the note so many steps larger or smaller."""
        return partial(self.note_panel.zoom, step)

    def _normal_command(self) -> Callable[[], None]:
        """Return what draws the note in the size it started out in."""
        return self.note_panel.zoom_normal

    def _bind_shortcuts(self, keys: Shortcuts) -> None:
        """Let the shortcuts shown on the menu entries be typed.

        Tk installs no binding for a menu accelerator, so every key
        sequence has to be bound as well. They are bound on this
        window only, so that a dialog which happens to have the
        keyboard focus cannot reach the main window with them.
        """
        self._bind(keys.quit, self.quit)
        self._bind(keys.larger, self._zoom_command(ZOOM_STEP))
        self._bind(keys.smaller, self._zoom_command(-ZOOM_STEP))
        self._bind(keys.normal, self._normal_command())

    def _bind(self, shortcut: Shortcut, command: Callable[[], None]) \
            -> None:
        """Let every key sequence of one shortcut run a command."""
        for sequence in shortcut.sequences:
            self.window.bind(sequence, lambda _event: command())

    def _shape_window(self) -> None:
        """Lay out the panes and give the window its size."""
        self.panes.add(self.explorer.frame, weight=0)
        self.panes.add(self.note_panel.frame, weight=1)
        self.panes.pack(fill=tkinter.BOTH, expand=True)
        self.window.geometry(INITIAL_GEOMETRY)
        self.window.minsize(MINIMUM_WIDTH, MINIMUM_HEIGHT)

    def show_project(self, project_name: Optional[str]) -> None:
        """Name the open project in the window title, None meaning none."""
        if project_name is None:
            self.window.title(APPLICATION_NAME)
        else:
            self.window.title(f'{APPLICATION_NAME} — {project_name}')

    def show_selected(self, path: Optional[Path]) -> None:
        """Show what the explorer has selected in the note panel."""
        self.note_panel.show_path(path)

    def offer_actions(self, labels: AbstractSet[str]) -> None:
        """Offer what can be done now, and grey out what cannot.

        The buttons of the panel and the entries of the note and
        folder menus do the same things, so they are offered and
        taken back together, whenever another item is selected and
        whenever the note that is shown is taken away.

        Args:
            labels: What the actions that can be done now are called.
        """
        self.note_panel.offer(labels)
        for title in (NOTE_MENU, FOLDER_MENU):
            menu = self.menu_bar.menus[title]
            for label in entry_labels(menu):
                set_enabled(menu, label, label in labels)

    def new_project_dialog(self) -> None:
        """Ask for a folder and make a notesmgr project of it.

        A folder that is a project already is not made into one twice,
        and opening it is what the user is offered instead.
        """
        folder = ask_folder(self.window, NEW_PROJECT_TITLE,
                            self.session.chooser_folder())
        if folder is None:
            return
        if not is_project(folder):
            self.make_project(folder)
        elif ask_yes_no(self.window, PROJECT_TITLE,
                        OFFER_OPEN.format(folder=folder)):
            self.load_project(folder)

    def open_project_dialog(self) -> None:
        """Ask for a project folder and open the project in it."""
        folder = ask_folder(self.window, OPEN_PROJECT_TITLE,
                            self.session.chooser_folder())
        if folder is not None:
            self.load_project(folder)

    def load_project(self, root: Path,
                     selected: Optional[Path] = None) -> None:
        """Open an existing project and show what it holds.

        Args:
            root: The root folder of the project to open.
            selected: What to select in it, None for nothing at all.
        """
        self.opened(partial(open_project, root, self.choose_template),
                    selected)

    def make_project(self, root: Path) -> None:
        """Make a folder into a project, then open it and show it."""
        self.opened(partial(create_project, root, self.choose_template))

    def reopen(self, selected: Optional[Path]) -> None:
        """Show the open project again, selecting one item of it.

        Every command changes the files of the project, so the whole
        project is read again rather than the tree being mended item
        by item. That way the tree says what the folders really hold,
        whatever another program did to them meanwhile.

        Args:
            selected: What to select once it is shown again, None to
                select nothing at all.
        """
        project = self.session.project
        if project is not None:
            self.load_project(project.root, selected)

    def opened(self, opening: Callable[[], OpenReport],
               selected: Optional[Path] = None) -> None:
        """Show what an opening gave, or say why it gave nothing."""
        try:
            report = opening()
        except NotesmgrError as error:
            show_error(self.window, PROJECT_TITLE, str(error))
            return
        self.show_opened(report, selected)

    def choose_template(self, folder: Path,
                        templates: Sequence[Path]) -> Optional[Path]:
        """Ask which of the templates of a folder is the one to keep.

        Args:
            folder: The folder that holds more than one template.
            templates: The templates that it holds.

        Returns:
            The template to keep, None when the user chose none.
        """
        question = TEMPLATE_QUESTION.format(folder=folder)
        names = [path.name for path in templates]
        chosen = ask_choice(self.window, TEMPLATE_TITLE, question, names)
        return None if chosen is None else folder / chosen

    def show_opened(self, report: OpenReport,
                    selected: Optional[Path]) -> None:
        """Show a project that was opened, and what opening it did."""
        self.session.opened(report.project)
        set_enabled(self.menu_bar.menus[CONFIG_MENU], USER_WIDE_ENTRY, True)
        self.show_project(report.project.root.name)
        self.explorer.show(report.project)
        self.select(selected)
        self.tell_about_opening(report)

    def select(self, path: Optional[Path]) -> None:
        """Select one item of the tree, and show what is selected.

        Tk tells of a selection it was given only once it comes to
        handle its own events, which is too late for a command that
        wants to see the project as it now stands, so the panel is
        told here rather than waiting for the event.

        Args:
            path: What to select, None to select nothing at all.
        """
        self.show_selected(self.explorer.select(path))

    def tell_about_opening(self, report: OpenReport) -> None:
        """Tell what opening a project changed and what it could not do."""
        changed = changed_message(report)
        if changed:
            show_info(self.window, PROJECT_TITLE, changed)
        if report.problems:
            show_error(self.window, PROJECT_TITLE, '\n'.join(report.problems))

    def edit_configuration(self) -> None:
        """Open the editor of the configuration that is in use.

        That is the configuration of the open project, and the user
        wide configuration while no project is open. One session at a
        time is enough, and the editor holds the application while it
        is open, so a second one is not started.
        """
        if self.config_panel is not None:
            return
        try:
            self.config_panel = open_config_editor(self.window,
                                                   self._config_closed,
                                                   self.session.config_file())
        except ConfigLoadError as error:
            show_error(self.window, CONFIG_TITLE, str(error))

    def _config_closed(self) -> None:
        """Take up again what the configuration editor may have changed.

        The configuration says what the notes and the templates of a
        project are called, so an open project is opened once more
        when an editing session has ended.
        """
        self.config_panel = None
        if self.session.project is not None:
            self.load_project(self.session.project.root)

    def save_user_wide(self) -> None:
        """Copy the project's configuration to the user wide file."""
        source = self.session.config_file()
        if source is None:
            return
        try:
            copy_to_user_wide(source)
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
