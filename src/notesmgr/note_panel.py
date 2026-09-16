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
from notesmgr.errors import NotesmgrError
from notesmgr.file_watch import FileWatch
from notesmgr.note_file import is_markdown, is_note
from notesmgr.note_text import EMPTY_NOTE, NoteText, read_note_text
from notesmgr.note_view import NoteView
from notesmgr.rich_clipboard import copy_rich, note_rich_text
from notesmgr.session import Session

PADDING = 8
"""Space in pixels left around what the panel shows."""

PLAIN_INSTEAD = '{reason}\nThe note was copied as plain text instead.'
"""What is said when the formatting could not be carried along."""


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
                ButtonSpec(COPY_FORMATTED, self.copy_formatted),
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
        if note is None:
            self.view.show(EMPTY_NOTE)
        else:
            self.view.show(read_note_text(note, self.note_limit()),
                           is_markdown(note.name), note.parent)
        self.commands.note_shown(self.has_note())

    def zoom(self, step: int) -> None:
        """Draw the note so many steps larger, or smaller below zero."""
        self.view.zoom(step)

    def zoom_normal(self) -> None:
        """Draw the note in the size that it started out in."""
        self.view.zoom_normal()

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

    def copied_note(self) -> Optional[NoteText]:
        """Return the note that a copy is taken of, None for none.

        A note that could not be read at all holds no text to copy,
        so what is wrong with it is reported rather than the
        clipboard being emptied. A note that is shown only in part is
        copied as far as it is shown, which is what the warning above
        it says.
        """
        if self.watch.path is None:
            return None
        note = self.view.shown_note()
        if not note.text and note.warning:
            self.commands.report_error(note.warning)
            return None
        return note

    def put_on_clipboard(self, text: str) -> None:
        """Put a text on the clipboard, in place of what was on it."""
        self.frame.clipboard_clear()
        self.frame.clipboard_append(text)

    def copy_raw(self) -> None:
        """Put the text of the note that is shown on the clipboard."""
        note = self.copied_note()
        if note is not None:
            self.put_on_clipboard(note.text)

    def copy_formatted(self) -> None:
        """Put the note that is shown on the clipboard formatted.

        Each platform carries formatted text in a way of its own, and
        one that has not got what it needs for it can still carry the
        plain text. That is put on the clipboard instead, so that a
        copy is never lost, and the user is told why it is plain.
        """
        note = self.copied_note()
        path = self.watch.path
        if note is None or path is None:
            return
        payload = note_rich_text(note.text, is_markdown(path.name),
                                 path.parent)
        try:
            copy_rich(payload)
        except NotesmgrError as error:
            self.put_on_clipboard(payload.text)
            self.commands.report_notice(PLAIN_INSTEAD.format(reason=error))
