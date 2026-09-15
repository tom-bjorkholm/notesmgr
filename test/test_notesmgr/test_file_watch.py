#! /usr/local/bin/python3
"""Tests for following a note while it is edited elsewhere."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import time
import tkinter
from pathlib import Path
import pytest
from test_notesmgr.helpers import write_file
from notesmgr.file_watch import MISSING, FileWatch, file_state

LATER = 100.0
"""Seconds to put between two writes, so that the times differ."""

SHORT = 5
"""Milliseconds between two looks, for a test that waits for one."""

WAITED = 0.2
"""Seconds that a test waits for a look that was asked for."""


@pytest.fixture(name='note')
def fixture_note(tmp_path: Path) -> Path:
    """Provide a note on disk that a watch can be set on."""
    return write_file(tmp_path / 'first.md.txt', 'first text\n')


@pytest.fixture(name='changes')
def fixture_changes() -> list[int]:
    """Provide the list that a watch reports its changes into."""
    return []


@pytest.fixture(name='watch')
def fixture_watch(top_window: tkinter.Toplevel,
                  changes: list[int]) -> FileWatch:
    """Provide a watch in a hidden window, watching nothing yet."""
    return FileWatch(top_window, lambda: changes.append(1))


def touch_later(path: Path) -> None:
    """Give a file a modification time well after the one it has."""
    os.utime(path, (time.time() + LATER, time.time() + LATER))


def test_no_file_is_missing() -> None:
    """No file at all looks the same as a file that is not there."""
    assert file_state(None) == MISSING


def test_gone_file_is_missing(tmp_path: Path) -> None:
    """A file that is not there is missing rather than an error."""
    assert file_state(tmp_path / 'gone.md.txt') == MISSING


def test_state_of_a_file(note: Path) -> None:
    """A file that is there is described by its time and its size."""
    state = file_state(note)
    assert state.exists
    assert state.size == note.stat().st_size
    assert state.mtime_ns == note.stat().st_mtime_ns


def test_watching_no_change(watch: FileWatch, note: Path,
                            changes: list[int]) -> None:
    """Taking up a file to watch is no change of that file."""
    watch.watch(note)
    watch.poll()
    assert changes == []


def test_unchanged_file_quiet(watch: FileWatch, note: Path,
                              changes: list[int]) -> None:
    """A file that is left alone is polled without anything being told."""
    watch.watch(note)
    for _ in range(3):
        watch.poll()
    assert changes == []


def test_written_file_told(watch: FileWatch, note: Path,
                           changes: list[int]) -> None:
    """A note written by another program is reported once."""
    watch.watch(note)
    note.write_text('another text\n', encoding='utf-8')
    touch_later(note)
    watch.poll()
    watch.poll()
    assert changes == [1]


def test_same_size_told(watch: FileWatch, note: Path,
                        changes: list[int]) -> None:
    """A note whose text was replaced by as much text is reported."""
    watch.watch(note)
    note.write_text('other text\n', encoding='utf-8')
    touch_later(note)
    watch.poll()
    assert changes == [1]


def test_deleted_file_told(watch: FileWatch, note: Path,
                           changes: list[int]) -> None:
    """A note that is taken away is reported, and is then missing."""
    watch.watch(note)
    note.unlink()
    watch.poll()
    assert changes == [1]
    assert watch.state == MISSING


def test_watching_nothing(watch: FileWatch, note: Path,
                          changes: list[int]) -> None:
    """A watch told to watch nothing reports nothing about the old file."""
    watch.watch(note)
    watch.watch(None)
    note.unlink()
    watch.poll()
    assert changes == []


def test_another_file_watched(watch: FileWatch, note: Path, tmp_path: Path,
                              changes: list[int]) -> None:
    """A watch moved to another file follows that one from then on."""
    other = write_file(tmp_path / 'second.md.txt', 'second\n')
    watch.watch(note)
    watch.watch(other)
    other.write_text('second and more\n', encoding='utf-8')
    touch_later(other)
    watch.poll()
    assert changes == [1]


def test_polling_is_asked_for(watch: FileWatch, note: Path) -> None:
    """Watching a file asks the event loop for the next look."""
    assert watch.job is None
    watch.watch(note)
    assert watch.job is not None


def test_one_poll_at_a_time(watch: FileWatch, note: Path) -> None:
    """Asking again takes back the look that was asked for before."""
    watch.watch(note)
    first = watch.job
    watch.schedule()
    assert watch.job != first


def test_cancelling_the_poll(watch: FileWatch, note: Path) -> None:
    """A watch that is taken back asks for no further look."""
    watch.watch(note)
    watch.cancel()
    assert watch.job is None


def test_tick_goes_on(watch: FileWatch, note: Path) -> None:
    """Every look asks for the next one, so the watching goes on."""
    watch.watch(note)
    watch.cancel()
    watch.tick()
    assert watch.job is not None


def test_closed_window_stops(watch: FileWatch, note: Path,
                             top_window: tkinter.Toplevel,
                             changes: list[int]) -> None:
    """The watching ends with the window that was doing it."""
    watch.watch(note)
    watch.cancel()
    top_window.destroy()
    note.unlink()
    watch.tick()
    assert changes == []
    assert watch.job is None


def test_event_loop_polls(top_window: tkinter.Toplevel, note: Path,
                          changes: list[int]) -> None:
    """A change is noticed without anyone asking the watch to look.

    This is the one test that lets the Tk event loop do the polling,
    which is what the application relies on while the user is editing
    the note in another program.
    """
    watch = FileWatch(top_window, lambda: changes.append(1), interval=SHORT)
    watch.watch(note)
    note.write_text('edited elsewhere\n', encoding='utf-8')
    touch_later(note)
    time.sleep(WAITED)
    top_window.update()
    watch.cancel()
    assert changes == [1]
