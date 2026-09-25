#! /usr/local/bin/python3
"""What the user is told of a failure that notesmgr was not made for."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
import traceback
from types import TracebackType
from typing import Callable, Optional
from notesmgr.dialogs import show_text

FAILURE_TITLE = 'notesmgr ran into a problem'
"""What the window telling of an unexpected failure is called."""

FAILURE_TEXT = 'Something went wrong that notesmgr was not made for, so\n' \
    'what was asked for may have been done only in part, or not at all.\n' \
    'The details below say what happened, for a report to the maker\n' \
    'of notesmgr.\n\n{details}'
"""What the user is told of a failure that notesmgr was not made for."""


def failure_details(error_type: type[BaseException], error: BaseException,
                    trace: Optional[TracebackType]) -> str:
    """Return where a failure happened and what it said, as Python does."""
    return ''.join(traceback.format_exception(error_type, error, trace))


class FailureReport:
    """Tells the user of every failure that nothing else has handled.

    Tk writes such a failure of a callback to the standard error
    stream and carries on, and a program started from a desktop has
    no terminal where that stream is read. It is shown in a window
    instead, and is still written to the stream when there is one.

    A failure that recurs, such as one in a file watch that polls
    every second, would open a window every time it happens, so a
    window is opened only while none of them is open already.
    """

    def __init__(self, root: tkinter.Tk) -> None:
        """Get ready to tell of failures over the given root window."""
        self.root = root
        self.window: Optional[tkinter.Toplevel] = None

    def __call__(self, error_type: type[BaseException], error: BaseException,
                 trace: Optional[TracebackType]) -> None:
        """Tell of a failure, in the way that Tk reports one.

        Args:
            error_type: The class of what was raised.
            error: What was raised.
            trace: Where it was raised, None when that is not known.
        """
        details = failure_details(error_type, error, trace)
        if sys.stderr is not None:
            sys.stderr.write(details)
        if self.window is None or not self.window.winfo_exists():
            self.window = show_text(self.root, FAILURE_TITLE,
                                    FAILURE_TEXT.format(details=details))

    def run(self, action: Callable[[], None]) -> None:
        """Do what is done before the main loop, telling of its failure.

        Tk handles only the failures of what it calls itself, so what
        is done before the main loop has started is told of here, in
        the same way.

        Args:
            action: What is to be done.
        """
        try:
            action()
        except Exception as error:  # pylint: disable=broad-exception-caught
            self(type(error), error, error.__traceback__)


def report_failures(root: tkinter.Tk) -> FailureReport:
    """Have every unhandled failure under a root window told of.

    Args:
        root: The root window of the application.

    Returns:
        What tells of the failures, which also runs what is done
        before the main loop has started.
    """
    report = FailureReport(root)
    root.report_callback_exception = report
    return report
