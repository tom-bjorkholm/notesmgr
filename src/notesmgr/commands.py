#! /usr/local/bin/python3
"""What the buttons and the menu entries do to the open project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from functools import partial
from pathlib import Path
from typing import Callable, NamedTuple, Optional, Sequence, Union
from notesmgr import folder_ops, note_ops
from notesmgr.actions import Selected, offered
from notesmgr.config import NoteExtension
from notesmgr.dialogs import NameFolder, ask_name, ask_name_folder, \
    ask_yes_no, show_error
from notesmgr.editor_command import launch_editor
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import is_plain_note, note_stem
from notesmgr.project import Project, folder_paths, is_project
from notesmgr.session import Session

NOTE_TITLE = 'Note'
"""What a window asking about or reporting about a note is called."""

FOLDER_TITLE = 'Folder'
"""What a window asking about a folder of the project is called."""

DUPLICATE_TITLE = 'Duplicate note'
"""What the window asking where to copy a note is called."""

ASK_NEW_NOTE = 'What is the new note to be called?'
"""What the user is asked when making a note."""

ASK_DELETE_NOTE = 'Move the note {name} to the trash?'
"""What the user is asked before a note is taken away."""

ASK_NEW_FOLDER = 'What is the new folder to be called?'
"""What the user is asked when making a folder."""

ASK_RENAME_FOLDER = 'What is the folder {name} to be called?'
"""What the user is asked when renaming a folder."""

ASK_DELETE_FOLDER = 'Move the folder {name} to the trash?'
"""What the user is asked before a folder is taken away."""

COPY_SUFFIX = ' copy'
"""What is put after the name of a note to name a copy of it."""


def shown_folder(root: Path, folder: Path) -> str:
    """Return how a folder of a project is named to the user.

    The root folder is named by itself and every folder below it by
    the way down to it, so that two folders of the same name in
    different places are told apart.

    Args:
        root: The root folder of the project.
        folder: The folder of the project to name.

    Returns:
        The name to show, which names the folder again through
        folder_of() when the user has chosen it.
    """
    return str(folder.relative_to(root.parent))


def folder_of(root: Path, shown: str) -> Path:
    """Return the folder that a name shown to the user stands for."""
    return root.parent / shown


class WindowHooks(NamedTuple):
    """What the commands ask the window that holds them to do.

    The window owns the tree and the menus, so it is what shows the
    project again once a command has changed it, and what offers the
    actions that can be used on what is selected now.
    """

    reopen: Callable[[Optional[Path]], None]
    offer: Callable[[frozenset[str]], None]


class Commands:
    """What the buttons and the menu entries do to the open project.

    Each command asks the user what it needs, has the model do it,
    and has the window show the project as it now stands with what
    was made or moved selected in it. What could not be done is put
    to the user in the words the model said it in, and the project
    is left exactly as it was.
    """

    def __init__(self, window: Union[tkinter.Tk, tkinter.Toplevel],
                 session: Session, hooks: WindowHooks) -> None:
        """Get ready to act upon a project, with nothing selected yet.

        Args:
            window: The window that the questions are asked over.
            session: What the run knows, which is the open project.
            hooks: What the commands ask the window to do.
        """
        self.window = window
        self.session = session
        self.hooks = hooks
        self.selection: Optional[Path] = None

    def select(self, path: Optional[Path]) -> None:
        """Take what the explorer has selected as what to act upon."""
        self.selection = path

    def note_shown(self, shown: bool) -> None:
        """Offer afresh what can be done with what is selected.

        Args:
            shown: Whether the panel has a note to act on, which a
                program other than notesmgr can take away at any time.
        """
        self.hooks.offer(offered(self.selected(shown)))

    def selected(self, shown: bool) -> Selected:
        """Return what is selected, as far as it says what can be done."""
        path = self.selection
        plain = shown and path is not None and is_plain_note(path.name)
        return Selected(note=shown, plain=plain,
                        project=self.session.project is not None,
                        folder=self.chosen_folder() is not None)

    def report_error(self, message: str) -> None:
        """Tell the user what could not be done, and why it could not."""
        show_error(self.window, NOTE_TITLE, message)

    def chosen_folder(self) -> Optional[Path]:
        """Return the folder that is selected, None when none is.

        The root folder of a project is the project itself rather
        than a folder in it to be renamed or taken away, so it
        counts as no folder here.
        """
        path = self.selection
        if path is None or not path.is_dir() or is_project(path):
            return None
        return path

    def note_folder(self) -> Optional[Path]:
        """Return the folder that a new note or folder goes into.

        That is the selected folder, the folder of the selected note,
        and the root folder of the project while nothing is selected.
        """
        project = self.session.project
        if project is None:
            return None
        path = self.selection
        if path is None:
            return project.root
        return path if path.is_dir() else path.parent

    def plain_note(self) -> Optional[Path]:
        """Return the selected note that is no template, None for none."""
        path = self.selection
        if path is None or not is_plain_note(path.name) or not path.is_file():
            return None
        return path

    def _extension(self) -> Optional[NoteExtension]:
        """Return the extension the notes of the open project carry."""
        config = self.session.config()
        return None if config is None else config.file_extension

    def done(self, doing: Callable[[], Optional[Path]]) -> Optional[Path]:
        """Do what changes the project, and show it as it now stands.

        Args:
            doing: What is to be done, giving what is to be selected
                afterwards and None when it leaves nothing to select.

        Returns:
            What was made or moved, None when the operation could not
            be done at all or left nothing to select.
        """
        try:
            given = doing()
        except NotesmgrError as error:
            self.report_error(str(error))
            return None
        self.hooks.reopen(given)
        return given

    def edit(self, note: Path) -> None:
        """Open a note in the editor that the project is configured with."""
        config = self.session.config()
        if config is None:
            return
        try:
            launch_editor(config.editor, note)
        except NotesmgrError as error:
            self.report_error(str(error))

    def new_note(self) -> None:
        """Make a note from the template and open it in the editor."""
        folder = self.note_folder()
        extension = self._extension()
        if folder is None or extension is None:
            return
        typed = ask_name(self.window, NOTE_TITLE, ASK_NEW_NOTE)
        if typed is None:
            return
        made = self.done(partial(note_ops.new_note, folder, typed, extension))
        if made is not None:
            self.edit(made)

    def duplicate_note(self) -> None:
        """Copy the selected note into a folder of the project."""
        note = self.plain_note()
        project = self.session.project
        extension = self._extension()
        if note is None or project is None or extension is None:
            return
        given = self._ask_copy(note, project)
        if given is not None:
            folder = folder_of(project.root, given.folder)
            self.done(partial(note_ops.duplicate_note, note, folder,
                              given.name, extension))

    def _ask_copy(self, note: Path, project: Project) \
            -> Optional[NameFolder]:
        """Ask what a copy of a note is called and where it is put."""
        root = project.root
        given = NameFolder(name=note_stem(note.name) + COPY_SUFFIX,
                           folder=shown_folder(root, note.parent))
        return ask_name_folder(self.window, DUPLICATE_TITLE, given,
                               self._folder_names(project))

    @staticmethod
    def _folder_names(project: Project) -> Sequence[str]:
        """Return the folders of a project as they are named to the user."""
        return [shown_folder(project.root, path)
                for path in folder_paths(project.tree)]

    def delete_note(self) -> None:
        """Move the selected note to the trash, once the user is sure."""
        note = self.plain_note()
        if note is None:
            return
        if ask_yes_no(self.window, NOTE_TITLE,
                      ASK_DELETE_NOTE.format(name=note.name)):
            self.done(partial(note_ops.delete_note, note))

    def move_up(self) -> None:
        """Move the selected note one place up in its folder."""
        self.move(-1)

    def move_down(self) -> None:
        """Move the selected note one place down in its folder."""
        self.move(1)

    def move(self, offset: int) -> None:
        """Move the selected note so many places in its folder."""
        note = self.plain_note()
        if note is not None:
            self.done(partial(note_ops.move_note, note, offset))

    def new_folder(self) -> None:
        """Make a folder in the folder that is selected."""
        parent = self.note_folder()
        extension = self._extension()
        if parent is None or extension is None:
            return
        typed = ask_name(self.window, FOLDER_TITLE, ASK_NEW_FOLDER)
        if typed is None:
            return
        self.done(partial(folder_ops.new_folder, parent, typed, extension))

    def rename_folder(self) -> None:
        """Give the selected folder another name."""
        folder = self.chosen_folder()
        if folder is None:
            return
        asked = ASK_RENAME_FOLDER.format(name=folder.name)
        typed = ask_name(self.window, FOLDER_TITLE, asked, folder.name)
        if typed is not None:
            self.done(partial(folder_ops.rename_folder, folder, typed))

    def delete_folder(self) -> None:
        """Move the selected folder to the trash, once the user is sure."""
        folder = self.chosen_folder()
        if folder is None:
            return
        if ask_yes_no(self.window, FOLDER_TITLE,
                      ASK_DELETE_FOLDER.format(name=folder.name)):
            self.done(partial(folder_ops.delete_folder, folder))
