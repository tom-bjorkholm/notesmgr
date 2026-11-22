#! /usr/local/bin/python3
"""The main window of the notesmgr application."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import tkinter
from functools import partial
from pathlib import Path
from tkinter import ttk
from typing import AbstractSet, Callable, Optional, Sequence, Union
from edit_cfg_json import ConfigLoadError
from edit_cfg_json_tk import TkEditorPanel
from notesmgr.actions import DELETE_FOLDER, FOCUS_FOLDER, NEW_FOLDER, \
    RENAME_FOLDER, SHOW_ALL
from notesmgr.commands import Commands, WindowHooks
from notesmgr.config_editor import open_config_editor
from notesmgr.config_files import copy_to_user_wide
from notesmgr.dialogs import ask_choice, ask_folder, ask_yes_no, \
    busy_cursor, show_error, show_info, show_text
from notesmgr.errors import NotesmgrError
from notesmgr.explorer_drop import Drop
from notesmgr.explorer_tree import ExplorerTree
from notesmgr.menu_bar import MenuEntry, MenuSpec, build_menu_bar, \
    entry_labels, set_enabled
from notesmgr.note_file import is_note_file
from notesmgr.note_panel import NotePanel
from notesmgr.project import is_project
from notesmgr.project_ops import OpenReport, changed_message, \
    create_project, open_project
from notesmgr.session import Session
from notesmgr.shortcuts import TREE_EDIT_KEYS, Shortcut, Shortcuts, \
    tk_window_system, window_shortcuts
from notesmgr.version_info import version_report

APPLICATION_NAME = 'notesmgr'
INITIAL_WIDTH = 1000
INITIAL_HEIGHT = 650
SCREEN_SHARE = 90
MINIMUM_WIDTH = 640
MINIMUM_HEIGHT = 400
FILE_MENU = 'File'
NOTE_MENU = 'Note'
FOLDER_MENU = 'Folder'
VIEW_MENU = 'View'
CONFIG_MENU = 'Configuration'
HELP_MENU = 'Help'
ACTION_MENUS = (NOTE_MENU, FOLDER_MENU)
"""The menus whose entries act on what is selected in the explorer.

They are also the popup menus of a right-click in the explorer.
"""
NEW_PROJECT_ENTRY = 'New project…'
OPEN_PROJECT_ENTRY = 'Open project…'
REFRESH_ENTRY = 'Refresh project'
QUIT_ENTRY = 'Quit'
ZOOM_IN_ENTRY = 'Larger text'
ZOOM_OUT_ENTRY = 'Smaller text'
NORMAL_SIZE_ENTRY = 'Normal text size'
ZOOM_STEP = 1
EDIT_CONFIG_ENTRY = 'Edit configuration…'
USER_WIDE_ENTRY = 'Save configuration as user wide…'
USER_WIDE_SAVED = 'The configuration of the project is now the user wide\n' \
    'configuration, in the file {path}.'
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


def fitted(wanted: int, screen: int) -> int:
    """Return a length of the window that the screen has room for.

    A window larger than its screen has its edges and its title bar
    out of reach, so a small screen gives nine tenths of itself
    rather than the length that was wanted.

    Args:
        wanted: Pixels the window would like to have.
        screen: Pixels the screen has in the same direction.

    Returns:
        The pixels that the window is given.
    """
    return min(wanted, screen * SCREEN_SHARE // 100)


def accelerator(keys: Shortcuts, action: str) -> Optional[str]:
    """Return what a menu entry shows of its keys, None for no keys."""
    shortcut = keys.actions.get(action)
    return None if shortcut is None else shortcut.label


def popup_title(path: Path) -> Optional[str]:
    """Return which menu a right-click on an item of the explorer shows.

    What the item is on the disk decides it, not what it is named. A
    folder gets the folder menu even when it is named like a note, a
    note file and the template of a folder get the note menu, which
    is what the panel shows them as, and anything else, such as a
    note that another program has taken away, gets no menu at all.

    Args:
        path: The item of the explorer that was right-clicked.

    Returns:
        The title of the menu, None for no menu.
    """
    if path.is_dir():
        return FOLDER_MENU
    return NOTE_MENU if is_note_file(path) else None


def handled(command: Callable[[], None],
            _event: 'tkinter.Event[tkinter.Misc]') -> str:
    """Run the command of a key, and end the handling of that key."""
    command()
    return 'break'


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
        self.explorer = ExplorerTree(self.panes, self.show_selected,
                                     self.dropped, self.context_menu)
        hooks = WindowHooks(self.reopen, self.offer_actions)
        commands = Commands(window, self.session, hooks)
        self.note_panel = NotePanel(self.panes, self.session, commands)
        self.config_panel: Optional[TkEditorPanel] = None
        keys = window_shortcuts(tk_window_system(window))
        self.menu_bar = build_menu_bar(window, self._menu_specs(keys),
                                       ACTION_MENUS)
        self._shape_window()
        self._bind_shortcuts(keys)
        self.show_project(None)
        self.explorer.tree.focus_set()

    def _menu_specs(self, keys: Shortcuts) -> list[MenuSpec]:
        """Return the menus of the main window and what they hold.

        The entries that act on a note need a note to act on, the
        entries that act on a folder need a folder, and copying the
        configuration to the user wide location asks for a project
        configuration file to copy, so all of them are greyed out
        until what they need is selected. Refreshing reads the open
        project again, so it waits for a project to be opened.
        """
        new_entry = MenuEntry(NEW_PROJECT_ENTRY, self.new_project_dialog)
        open_entry = MenuEntry(OPEN_PROJECT_ENTRY, self.open_project_dialog)
        refresh = MenuEntry(REFRESH_ENTRY, self.refresh, keys.refresh.label,
                            enabled=False)
        quit_entry = MenuEntry(QUIT_ENTRY, self.quit, keys.quit.label)
        edit_entry = MenuEntry(EDIT_CONFIG_ENTRY, self.edit_configuration)
        user_wide = MenuEntry(USER_WIDE_ENTRY, self.save_user_wide,
                              enabled=False)
        versions = MenuEntry(VERSION_ENTRY, self.show_version)
        return [MenuSpec(FILE_MENU, [new_entry, open_entry, refresh,
                                     quit_entry]),
                MenuSpec(NOTE_MENU, self._note_entries(keys)),
                MenuSpec(FOLDER_MENU, self._folder_entries(keys)),
                MenuSpec(VIEW_MENU, self._view_entries(keys)),
                MenuSpec(CONFIG_MENU, [edit_entry, user_wide]),
                MenuSpec(HELP_MENU, [versions])]

    def _note_entries(self, keys: Shortcuts) -> list[MenuEntry]:
        """Return one entry of the note menu for every action on a note.

        The note menu and the button row do the same things, so they
        are described in one place, which is the panel that holds the
        buttons, though the row leaves a few of them to the menu. An
        action that was described with no command has nothing to do,
        and is left out of the menu until it has.
        """
        return [MenuEntry(spec.label, spec.command,
                          accelerator(keys, spec.label), enabled=False)
                for spec in self.note_panel.actions()
                if spec.command is not None]

    def _folder_entries(self, keys: Shortcuts) -> list[MenuEntry]:
        """Return the entries that act on a folder of the project.

        Below a line come the entries that say which folders the
        explorer shows open.
        """
        commands = self.note_panel.commands
        acting = [MenuEntry(NEW_FOLDER, commands.new_folder,
                            accelerator(keys, NEW_FOLDER), enabled=False),
                  MenuEntry(RENAME_FOLDER, commands.rename_folder,
                            enabled=False),
                  MenuEntry(DELETE_FOLDER, commands.delete_folder,
                            enabled=False)]
        showing = [MenuEntry(label, command, accelerator(keys, label),
                             enabled=False, separated=index == 0)
                   for index, (label, command)
                   in enumerate(self._tree_commands().items())]
        return acting + showing

    def _tree_commands(self) -> dict[str, Callable[[], None]]:
        """Return what each action on the folders the explorer opens runs."""
        return {FOCUS_FOLDER: self.explorer.focus_selected,
                SHOW_ALL: self.explorer.open_all}

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
        """Return what draws the window so many steps larger or smaller."""
        return partial(self.zoom, step)

    def _normal_command(self) -> Callable[[], None]:
        """Return what draws the window in the size it started out in."""
        return self.zoom_normal

    def zoom(self, step: int) -> None:
        """Draw the note and the tree so many steps larger or smaller.

        The note and the names of the notes are read on one screen
        and at one distance from it, so they are made larger and
        smaller together rather than each for itself.
        """
        self.note_panel.zoom(step)
        self.explorer.zoom(step)

    def zoom_normal(self) -> None:
        """Draw the note and the tree in the size they started out in."""
        self.note_panel.zoom_normal()
        self.explorer.zoom_normal()

    def _bind_shortcuts(self, keys: Shortcuts) -> None:
        """Let the shortcuts shown on the menu entries be typed.

        Tk installs no binding for a menu accelerator, so every key
        sequence has to be bound as well. They are bound on this
        window only, so that a dialog which happens to have the
        keyboard focus cannot reach the main window with them. The
        Return key of the tree edits the selected note, and still
        opens and closes a selected folder as the tree itself does.
        """
        self._bind(keys.quit, self.quit)
        self._bind(keys.refresh, self.refresh)
        self._bind(keys.larger, self._zoom_command(ZOOM_STEP))
        self._bind(keys.smaller, self._zoom_command(-ZOOM_STEP))
        self._bind(keys.normal, self._normal_command())
        commands = self.note_panel.key_commands() | self._tree_commands()
        for action, command in commands.items():
            self._bind(keys.actions[action], command)
        for sequence in TREE_EDIT_KEYS:
            self.explorer.tree.bind(sequence, self._edit_key)

    def _bind(self, shortcut: Shortcut, command: Callable[[], None]) \
            -> None:
        """Let every key sequence of one shortcut run a command.

        The tree moves its selection on an arrow key whatever key is
        held down with it, so the sequences are bound on the tree as
        well. A binding of the tree itself comes before what the tree
        does, and ends the handling of the key once it has run.
        """
        for widget in (self.window, self.explorer.tree):
            for sequence in shortcut.sequences:
                widget.bind(sequence, partial(handled, command))

    def _edit_key(self, _event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Open the note that is shown in the editor of the project."""
        self.note_panel.edit_note()

    def _shape_window(self) -> None:
        """Lay out the panes and give the window its size.

        The window starts out in its own size and is kept above its
        smallest size, except that neither is larger than the screen.
        """
        self.panes.add(self.explorer.frame, weight=0)
        self.panes.add(self.note_panel.frame, weight=1)
        self.panes.pack(fill=tkinter.BOTH, expand=True)
        width = self.window.winfo_screenwidth()
        height = self.window.winfo_screenheight()
        self.window.geometry(f'{fitted(INITIAL_WIDTH, width)}x'
                             f'{fitted(INITIAL_HEIGHT, height)}')
        self.window.minsize(fitted(MINIMUM_WIDTH, width),
                            fitted(MINIMUM_HEIGHT, height))

    def show_project(self, project_name: Optional[str]) -> None:
        """Name the open project in the window title, None meaning none."""
        if project_name is None:
            self.window.title(APPLICATION_NAME)
        else:
            self.window.title(f'{APPLICATION_NAME} — {project_name}')

    def show_selected(self, path: Optional[Path]) -> None:
        """Show what the explorer has selected in the note panel."""
        self.note_panel.show_path(path)

    def dropped(self, item: Path, drop: Drop) -> None:
        """Move what was dragged in the explorer to where it was dropped.

        Args:
            item: The note or the folder that was dragged.
            drop: Where it was dropped, as the tree worked it out.
        """
        self.note_panel.commands.drop(item, drop)

    def offer_actions(self, labels: AbstractSet[str]) -> None:
        """Offer what can be done now, and grey out what cannot.

        The buttons of the panel, the entries of the note and folder
        menus and the entries of the right-click menus do the same
        things, so they are offered and taken back together, whenever
        another item is selected and whenever the note that is shown
        is taken away.

        Args:
            labels: What the actions that can be done now are called.
        """
        self.note_panel.offer(labels)
        menu_bar = self.menu_bar
        menus = [menu_bar.menus[title] for title in ACTION_MENUS]
        for menu in menus + list(menu_bar.popups.values()):
            for label in entry_labels(menu):
                set_enabled(menu, label, label in labels)

    def context_menu(self, path: Path, x_root: int, y_root: int) -> None:
        """Select a right-clicked item, and show its menu where clicked.

        The item is selected first, so that the menu acts on it and
        offers what can be done with it. Which menu it gets is what
        popup_title says, and an item that gets none is selected all
        the same.

        Args:
            path: The item of the explorer that was right-clicked.
            x_root: Where on the screen it was clicked, from the left.
            y_root: Where on the screen it was clicked, from the top.
        """
        self.select(path)
        title = popup_title(path)
        if title is not None:
            self.menu_bar.popups[title].tk_popup(x_root, y_root)

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
                     selected: Optional[Path] = None) -> bool:
        """Open an existing project and show what it holds.

        Args:
            root: The root folder of the project to open.
            selected: What to select in it, None for nothing at all.

        Returns:
            Whether the project was opened, which it was not when the
            user has been told why it could not be.
        """
        return self._opened(partial(open_project, root,
                                    self.choose_template), selected)

    def make_project(self, root: Path) -> None:
        """Make a folder into a project, then open it and show it."""
        self._opened(partial(create_project, root, self.choose_template))

    def refresh(self) -> None:
        """Read the open project again, keeping what is selected.

        The folders that were closed stay closed, as they do whenever
        the project is shown again, and the entry that shows all
        folders is what opens them all.

        Another program, or notesmgr on another computer sharing the
        folder, can change the project while it is open, and notesmgr
        hears nothing of it, so the user asks for it to be read again.
        """
        self.reopen(self.explorer.selected_path())

    def reopen(self, selected: Optional[Path]) -> None:
        """Show the open project again, selecting one item of it.

        Every command changes the files of the project, so the whole
        project is read again rather than the tree being mended item
        by item. That way the tree says what the folders really hold,
        whatever another program did to them meanwhile. A project that
        can no longer be read is closed, once the user has been told
        why, so that no command acts on a tree that is not there.

        Args:
            selected: What to select once it is shown again, None to
                select nothing at all.
        """
        project = self.session.project
        if project is None:
            return
        if not self.load_project(project.root, selected):
            self._close_project()

    def _close_project(self) -> None:
        """Show no project at all, and offer nothing that needs one."""
        self.session.closed()
        self._offer_project(False)
        self.show_project(None)
        self.explorer.show(None)
        self.select(None)

    def _offer_project(self, is_open: bool) -> None:
        """Offer the entries that need an open project, or grey them out.

        Args:
            is_open: Whether there is a project open now.
        """
        set_enabled(self.menu_bar.menus[FILE_MENU], REFRESH_ENTRY, is_open)
        set_enabled(self.menu_bar.menus[CONFIG_MENU], USER_WIDE_ENTRY, is_open)

    def _opened(self, opening: Callable[[], OpenReport],
                selected: Optional[Path] = None) -> bool:
        """Show what an opening gave, or say why it gave nothing.

        Returns:
            Whether a project was shown, which it was not when the
            user has been told why the opening gave nothing.
        """
        try:
            report = opening()
        except NotesmgrError as error:
            show_error(self.window, PROJECT_TITLE, str(error))
            return False
        self._show_opened(report, selected)
        return True

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

    def _show_opened(self, report: OpenReport,
                     selected: Optional[Path]) -> None:
        """Show a project that was opened, and what opening it did.

        What was to be selected may have been taken away or renamed
        by another program, and the nearest folder above it that is
        still there is then selected instead.
        """
        self.session.opened(report.project)
        self._offer_project(True)
        self.show_project(report.project.root.name)
        self.explorer.show(report.project)
        self.select(self.explorer.nearest_shown(selected))
        self._tell_about_opening(report)

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

    def _tell_about_opening(self, report: OpenReport) -> None:
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
        """Copy the project's configuration to the user wide file.

        The user wide file is found in more than one way, so the user
        is told which file it was written to.
        """
        source = self.session.config_file()
        if source is None:
            return
        try:
            target = copy_to_user_wide(source)
        except OSError as error:
            show_error(self.window, CONFIG_TITLE, str(error))
            return
        show_info(self.window, CONFIG_TITLE, USER_WIDE_SAVED.format(
            path=target))

    def show_version(self) -> None:
        """Show what notesmgr and the packages below it are.

        Gathering the report asks PyPI whether there are newer
        releases, which takes a moment, so the window says that it is
        working while that is going on.
        """
        report = io.StringIO()
        try:
            with busy_cursor(self.window):
                version_report(report)
        except NotesmgrError as error:
            show_error(self.window, VERSION_TITLE, str(error))
            return
        show_text(self.window, VERSION_TITLE, report.getvalue())

    def quit(self) -> None:
        """Destroy the main window, which ends the application."""
        self.window.destroy()
