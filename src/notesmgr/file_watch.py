#! /usr/local/bin/python3
"""Following the note that is shown while it is edited elsewhere."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Callable, NamedTuple, Optional

POLL_INTERVAL = 1000
"""Milliseconds between two looks at the note that is shown."""


class FileState(NamedTuple):
    """What a file looked like when it was last looked at.

    A file is taken to have changed when any of this is no longer
    what it was, so that saving a note in an editor, deleting it and
    writing it again are all seen.
    """

    exists: bool
    mtime_ns: int
    size: int


MISSING = FileState(exists=False, mtime_ns=0, size=0)
"""What a file that is not there looks like, and no file at all."""


def file_state(path: Optional[Path]) -> FileState:
    """Return what a file looks like now.

    A file that cannot be asked about cannot be shown either, so it
    is taken to be missing rather than raising here.

    Args:
        path: The file to look at, None for no file at all.

    Returns:
        What it looks like now.
    """
    if path is None:
        return MISSING
    try:
        status = path.stat()
    except OSError:
        return MISSING
    return FileState(exists=True, mtime_ns=status.st_mtime_ns,
                     size=status.st_size)


class FileWatch:
    """Tells whoever listens that the file being watched has changed.

    The file system is asked about the file now and then, because a
    note is edited by another program that notesmgr hears nothing
    from. The asking is done by the Tk event loop, so the polling
    holds nothing up and needs no thread of its own.
    """

    def __init__(self, widget: tkinter.Misc, on_change: Callable[[], None],
                 interval: int = POLL_INTERVAL) -> None:
        """Get ready to watch, watching nothing yet.

        Args:
            widget: The widget whose event loop does the polling, and
                whose end is the end of the watching.
            on_change: Told whenever the watched file has changed.
            interval: Milliseconds between two looks at the file.
        """
        self.widget = widget
        self.on_change = on_change
        self.interval = interval
        self.path: Optional[Path] = None
        self.state = MISSING
        self.job: Optional[str] = None

    def watch(self, path: Optional[Path]) -> None:
        """Watch another file from now on, or no file at all.

        The file as it is now is what the watching starts from, so
        that taking up a file is no change of it.

        Args:
            path: The file to watch, None for no file at all.
        """
        self.path = path
        self.state = file_state(path)
        self.schedule()

    def poll(self) -> None:
        """Tell that the watched file has changed, when it has."""
        state = file_state(self.path)
        if state != self.state:
            self.state = state
            self.on_change()

    def tick(self) -> None:
        """Look at the file again, and go on while there is a window."""
        if self.widget.winfo_exists():
            self.poll()
            self.schedule()

    def schedule(self) -> None:
        """Ask for the next look, in place of one already asked for."""
        self.cancel()
        self.job = self.widget.after(self.interval, self.tick)

    def cancel(self) -> None:
        """Take back the look that was asked for, if there is one."""
        if self.job is not None:
            self.widget.after_cancel(self.job)
            self.job = None
