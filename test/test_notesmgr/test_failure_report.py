#! /usr/local/bin/python3
"""Tests for what the user is told of a failure nothing else handled."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import tkinter
from typing import NamedTuple
import pytest
from notesmgr import failure_report as report_module
from notesmgr.failure_report import FAILURE_TITLE, FailureReport, \
    failure_details, report_failures

MESSAGE = 'something is not as it should be'
"""What the failures of these tests say."""


class ShownText(NamedTuple):
    """One text that was asked to be shown in a window of its own."""

    title: str
    text: str


@pytest.fixture(name='shown')
def fixture_shown(top_window: tkinter.Toplevel,
                  monkeypatch: pytest.MonkeyPatch) -> list[ShownText]:
    """Record the texts that were shown, in hidden windows of their own.

    The report asks whether the window it opened is still open, so a
    window is really made for every text, and it is made hidden and
    inside the window of the test, which takes it away afterwards.
    """
    shown: list[ShownText] = []

    def record(_parent: object, title: str, text: str) -> tkinter.Toplevel:
        """Stand in for showing a text in a window of its own."""
        shown.append(ShownText(title, text))
        window = tkinter.Toplevel(top_window)
        window.withdraw()
        return window
    monkeypatch.setattr(report_module, 'show_text', record)
    return shown


@pytest.fixture(name='report')
def fixture_report(tk_root: tkinter.Tk) -> FailureReport:
    """Provide a report over the root window, installed nowhere."""
    return FailureReport(tk_root)


def fail() -> None:
    """Fail in the way that the failures of these tests fail."""
    raise ValueError(MESSAGE)


def raised() -> ValueError:
    """Return a failure that was really raised, and carries its trace."""
    try:
        fail()
    except ValueError as error:
        return error
    raise AssertionError('fail() did not fail')


def tell_of_failure(report: FailureReport) -> None:
    """Have a report tell of a failure that was really raised."""
    error = raised()
    report(type(error), error, error.__traceback__)


def test_details_of_failure() -> None:
    """The details say what was raised and where it was raised."""
    error = raised()
    details = failure_details(type(error), error, error.__traceback__)
    assert f'ValueError: {MESSAGE}' in details
    assert 'in fail' in details


def test_failure_shown(report: FailureReport, shown: list[ShownText]) \
        -> None:
    """A failure is shown in a window, with what it said."""
    tell_of_failure(report)
    assert len(shown) == 1
    assert shown[0].title == FAILURE_TITLE
    assert f'ValueError: {MESSAGE}' in shown[0].text


def test_failure_written(report: FailureReport, shown: list[ShownText],
                         capsys: pytest.CaptureFixture[str]) -> None:
    """A failure is also written to the error stream, where there is one."""
    tell_of_failure(report)
    assert f'ValueError: {MESSAGE}' in capsys.readouterr().err
    assert len(shown) == 1


def test_no_error_stream(report: FailureReport, shown: list[ShownText],
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """With no error stream at all the failure is still shown."""
    monkeypatch.setattr(sys, 'stderr', None)
    tell_of_failure(report)
    assert len(shown) == 1


def test_one_window_at_a_time(report: FailureReport,
                              shown: list[ShownText]) -> None:
    """A failure that recurs opens no second window beside the first."""
    tell_of_failure(report)
    tell_of_failure(report)
    assert len(shown) == 1


def test_again_once_closed(report: FailureReport,
                           shown: list[ShownText]) -> None:
    """A failure after the window was closed opens a window again."""
    tell_of_failure(report)
    assert report.window is not None
    report.window.destroy()
    tell_of_failure(report)
    assert len(shown) == 2


def test_run_tells_of_failure(report: FailureReport,
                              shown: list[ShownText]) -> None:
    """What fails before the main loop is told of, and does not raise."""
    report.run(fail)
    assert len(shown) == 1
    assert MESSAGE in shown[0].text


def test_run_does_it(report: FailureReport, shown: list[ShownText]) -> None:
    """What does not fail is done, and nothing is shown."""
    done: list[bool] = []
    report.run(lambda: done.append(True))
    assert done == [True]
    assert not shown


@pytest.fixture(name='installed')
def fixture_installed(tk_root: tkinter.Tk,
                      monkeypatch: pytest.MonkeyPatch) -> FailureReport:
    """Provide a report installed on the root window for one test only.

    The root window is shared by every test, so what reports its
    failures is put back once the test is over.
    """
    monkeypatch.setattr(tk_root, 'report_callback_exception',
                        tk_root.report_callback_exception)
    return report_failures(tk_root)


def test_report_installed(tk_root: tkinter.Tk,
                          installed: FailureReport) -> None:
    """The root window reports its failures through the report."""
    assert tk_root.report_callback_exception is installed


def test_callback_told_of(tk_root: tkinter.Tk, installed: FailureReport,
                          shown: list[ShownText]) -> None:
    """A command that Tk calls and that fails is told of in a window."""
    _ = installed
    command = tk_root.register(fail)
    try:
        tk_root.tk.call(command)
    finally:
        tk_root.deletecommand(command)
    assert len(shown) == 1
    assert MESSAGE in shown[0].text
