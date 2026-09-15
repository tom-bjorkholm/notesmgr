#! /usr/local/bin/python3
"""The panel at the right of the main window, showing a note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Callable, NamedTuple, Optional
from notesmgr.button_row import ButtonRow, ButtonSpec
from notesmgr.config import DEFAULT_NOTE_SIZE
from notesmgr.editor_command import launch_editor
from notesmgr.errors import NotesmgrError
from notesmgr.file_watch import FileWatch
from notesmgr.note_file import is_note
from notesmgr.note_text import EMPTY_NOTE, read_note_text
from notesmgr.note_view import NoteView
from notesmgr.session import Session

PADDING = 8
"""Space in pixels left around what the panel shows."""

COPY_RAW = 'Copy raw'
"""What the button that copies the note as it is written says."""

COPY_FORMATTED = 'Copy formatted'
"""What the button that copies the note formatted says."""

DUPLICATE = 'Duplicate'
"""What the button that copies the note into the project says."""

EDIT = 'Edit'
"""What the button that opens the note in an editor says."""

NEW = 'New'
"""What the button that makes another note says."""

DELETE = 'Delete'
"""What the button that takes the note away says."""

MOVE_UP = 'Up'
"""What the button that moves the note one place up says."""

MOVE_DOWN = 'Down'
"""What the button that moves the note one place down says."""


class PanelHooks(NamedTuple):
    """What the panel tells the window that holds it.

    The window owns the menu entries that do what the buttons do, and
    it owns the way that a problem is put to the user, so the panel
    is given both rather than reaching back into the window.
    """

    report_error: Callable[[str], None]
    note_shown: Callable[[bool], None]


class NotePanel:
    """Shows the selected note and the buttons that act upon it.

    The note that the buttons act on is the file that the watch is
    following, so that one place says what the panel is showing. It
    is the selected file when that is a note or the template of a
    folder, and nothing when a folder or nothing at all is selected.
    """

    def __init__(self, parent: tkinter.Misc, session: Session,
                 hooks: PanelHooks) -> None:
        """Build the panel in a frame of its own inside a parent widget.

        Args:
            parent: The widget that the panel is placed in.
            session: What the run knows, which is the open project and
                therefore the editor and the size that are configured.
            hooks: What the panel tells the window that holds it.
        """
        self.session = session
        self.hooks = hooks
        self.frame = ttk.Frame(parent)
        self.row = ButtonRow(self.frame, self._button_specs())
        self.row.frame.pack(side=tkinter.TOP, fill=tkinter.X, padx=PADDING,
                            pady=PADDING)
        self.path_label = ttk.Label(self.frame, anchor=tkinter.W)
        self.path_label.pack(side=tkinter.TOP, fill=tkinter.X, padx=PADDING)
        self.view = NoteView(self.frame)
        self.view.frame.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True,
                             padx=PADDING, pady=PADDING)
        self.watch = FileWatch(self.frame, self.reload)

    def _button_specs(self) -> list[ButtonSpec]:
        """Return the buttons of the row in the order they are shown."""
        return [ButtonSpec(COPY_RAW, self.copy_raw),
                ButtonSpec(COPY_FORMATTED), ButtonSpec(DUPLICATE),
                ButtonSpec(EDIT, self.edit_note), ButtonSpec(NEW),
                ButtonSpec(DELETE), ButtonSpec(MOVE_UP),
                ButtonSpec(MOVE_DOWN)]

    def note_limit(self) -> int:
        """Return how much of a note the open project shows.

        With no project open there is no note to show either, so the
        built-in default stands in for a configuration that is not
        there rather than making the panel a special case.
        """
        config = self.session.config()
        return DEFAULT_NOTE_SIZE if config is None else config.max_note_size

    def note_path(self) -> Optional[Path]:
        """Return the note the panel is showing, None when it shows none."""
        return self.watch.path

    def has_note(self) -> bool:
        """Return whether there is a note for the buttons to act on."""
        return self.watch.path is not None and self.watch.state.exists

    def show_path(self, path: Optional[Path]) -> None:
        """Show what the explorer has selected.

        Args:
            path: What is selected in the explorer, None for nothing.
                A folder is shown by its path alone, and a note and
                the template of a folder are also read and shown.
        """
        self.path_label.configure(text='' if path is None else str(path))
        shown = path if path is not None and is_note(path.name) else None
        self.watch.watch(shown)
        self.reload()

    def reload(self) -> None:
        """Show what the note that is being watched holds now.

        This is what the watch calls when the note has been edited,
        written or taken away by another program, so a note that is
        gone leaves the panel saying so and the buttons greyed out.
        """
        note = self.watch.path
        self.view.show(EMPTY_NOTE if note is None
                       else read_note_text(note, self.note_limit()))
        self.offer_actions(self.has_note())

    def offer_actions(self, enabled: bool) -> None:
        """Offer what acts on a note, or grey it out.

        The buttons of the panel and the entries of the note menu are
        offered together, because they do the same things, so the
        window that holds the menu is told as well.

        Args:
            enabled: Whether there is a note to act on.
        """
        self.row.offer(enabled)
        self.hooks.note_shown(enabled)

    def shown_path(self) -> str:
        """Return the path the panel is showing, empty for none."""
        return str(self.path_label.cget('text'))

    def edit_note(self) -> None:
        """Open the note that is shown in the editor of the project."""
        note = self.watch.path
        config = self.session.config()
        if note is None or config is None:
            return
        try:
            launch_editor(config.editor, note)
        except NotesmgrError as error:
            self.hooks.report_error(str(error))

    def copy_raw(self) -> None:
        """Put the text of the note that is shown on the clipboard.

        A note that could not be read at all holds no text to copy,
        so what is wrong with it is reported rather than the
        clipboard being emptied. A note that is shown only in part is
        copied as far as it is shown, which is what the warning above
        it says.
        """
        if self.watch.path is None:
            return
        note = self.view.shown_note()
        if not note.text and note.warning:
            self.hooks.report_error(note.warning)
            return
        self.frame.clipboard_clear()
        self.frame.clipboard_append(note.text)
