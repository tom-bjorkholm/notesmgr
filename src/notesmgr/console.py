#! /usr/local/bin/python3
"""Where notesmgr says what its command line asks it to say."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import sys
import tkinter
from contextlib import ExitStack, contextmanager, redirect_stderr, \
    redirect_stdout
from tkinter import messagebox
from typing import Iterator

CONSOLE_TITLE = 'notesmgr'
"""What the window showing what the command line said is called."""


def show_said(text: str, failed: bool) -> None:
    """Show in a window of its own what the command line said.

    Nothing has been shown yet when the command line is read, so the
    window is shown over a root window of its own that is never seen.

    Args:
        text: What was said, nothing at all meaning no window.
        failed: Whether it says that the command line was refused.
    """
    if not text:
        return
    root = tkinter.Tk()
    root.withdraw()
    show = messagebox.showerror if failed else messagebox.showinfo
    show(title=CONSOLE_TITLE, message=text, parent=root)
    root.destroy()


@contextmanager
def console_or_window() -> Iterator[None]:
    """Show in a window what is said while there is no console.

    Windows starts a program that is installed as a graphical one
    with no standard output and no standard error stream, so what the
    command line asks to have said, the help and the errors among it,
    would be lost. It is gathered instead and shown in a window once
    all of it is said, while a stream that is there is written to as
    usual.
    """
    gathered = io.StringIO()
    failed = False
    with ExitStack() as stack:
        if sys.stdout is None:
            stack.enter_context(redirect_stdout(gathered))
        if sys.stderr is None:
            stack.enter_context(redirect_stderr(gathered))
        try:
            yield
        except SystemExit as leaving:
            failed = leaving.code not in (None, 0)
            raise
        finally:
            show_said(gathered.getvalue(), failed)
