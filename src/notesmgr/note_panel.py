#! /usr/local/bin/python3
"""The panel at the right of the main window, showing a note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import AbstractSet, Optional, Sequence
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, DUPLICATE, \
    EDIT, MOVE_DOWN, MOVE_UP, NEW
from notesmgr.button_row import ButtonRow, ButtonSpec
from notesmgr.commands import Commands
from notesmgr.config import DEFAULT_NOTE_SIZE
from notesmgr.file_watch import FileWatch
from notesmgr.note_file import is_note
from notesmgr.note_text import EMPTY_NOTE, read_note_text
from notesmgr.note_view import NoteView
from notesmgr.session import Session

PADDING = 8
"""Space in pixels left around what the panel shows."""


class NotePanel:
    """Shows the selected note and the buttons that act upon it.

    The note that the buttons act on is the file that the watch is
    following, so that one place says what the panel is showing. It
    is the selected file when that is a note or the template of a
    folder, and nothing when a folder or nothing at all is selected.
    """

    def __init__(self, parent: tkinter.Misc, session: Session,
                 commands: Commands) -> None:
        """Build the panel in a frame of its own inside a parent widget.

        Args:
            parent: The widget that the panel is placed in.
            session: What the run knows, which is the open project and
                therefore the editor and the size that are configured.
            commands: What the buttons of the panel do when pressed,
                which is also what is told what is selected now.
        """
        self.session = session
        self.commands = commands
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
        commands = self.commands
        return [ButtonSpec(COPY_RAW, self.copy_raw),
                ButtonSpec(COPY_FORMATTED),
                ButtonSpec(DUPLICATE, commands.duplicate_note),
                ButtonSpec(EDIT, self.edit_note),
                ButtonSpec(NEW, commands.new_note),
                ButtonSpec(DELETE, commands.delete_note),
                ButtonSpec(MOVE_UP, commands.move_up),
                ButtonSpec(MOVE_DOWN, commands.move_down)]

    def actions(self) -> Sequence[ButtonSpec]:
        """Return what the buttons of the panel are and what they do."""
        return self.row.specs

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
        self.commands.select(path)
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
        self.commands.note_shown(self.has_note())

    def offer(self, labels: AbstractSet[str]) -> None:
        """Let the buttons that can be used now be pressed.

        Args:
            labels: What the actions that can be done now are called.
        """
        self.row.offer(labels)

    def shown_path(self) -> str:
        """Return the path the panel is showing, empty for none."""
        return str(self.path_label.cget('text'))

    def edit_note(self) -> None:
        """Open the note that is shown in the editor of the project."""
        note = self.watch.path
        if note is not None:
            self.commands.edit(note)

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
            self.commands.report_error(note.warning)
            return
        self.frame.clipboard_clear()
        self.frame.clipboard_append(note.text)
