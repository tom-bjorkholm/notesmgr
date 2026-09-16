#! /usr/local/bin/python3
"""Tests for the formatted copy that macOS is given."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import subprocess
import sys
from pathlib import Path
from typing import NamedTuple, Optional, Sequence
import pytest
from notesmgr import clipboard_macos
from notesmgr.clipboard_macos import OSASCRIPT, RTF_NAME, TEXTUTIL, \
    TEXT_NAME, copy_to_clipboard, written
from notesmgr.clipboard_tool import RichText

RTF = b'{\\rtf1 what textutil gave back}'
"""What the stand-in for textutil answers with."""

HTML = '<h1>Rubrik</h1><p>Text with åäö in it.</p>'
"""The HTML of the note that these tests copy."""

TEXT = '# Rubrik\n\nText with åäö in it.\n'
"""The note that these tests copy, as it is written."""

COPY = RichText(HTML, TEXT)
"""The copy that these tests hand to the pasteboard."""

ON_MACOS = sys.platform == 'darwin'
"""Whether these tests are running on the platform they are about."""


class Run(NamedTuple):
    """One program that the backend asked to have run.

    What the files named on the command line held is kept as well,
    because they are written into a folder that is taken away again
    as soon as the copy has been made.
    """

    argv: tuple[str, ...]
    data: bytes
    files: tuple[bytes, ...]


def read_file(word: str) -> Optional[bytes]:
    """Return what the file a word names holds, None for no file.

    A command line holds words that name no file at all, and a word
    too long to be a file name makes the file system complain rather
    than answer, so anything that cannot be read counts as no file.
    """
    try:
        return Path(word).read_bytes()
    except OSError:
        return None


def files_named(argv: Sequence[str]) -> tuple[bytes, ...]:
    """Return what the files named on a command line hold just now."""
    return tuple(held for held in map(read_file, argv) if held is not None)


@pytest.fixture(name='runs')
def fixture_runs(monkeypatch: pytest.MonkeyPatch) -> list[Run]:
    """Record the programs the backend runs, running none of them."""
    asked: list[Run] = []

    def record(argv: Sequence[str], data: bytes,
               capture: bool = True) -> bytes:
        """Stand in for running a program of the system."""
        assert capture
        asked.append(Run(tuple(argv), data, files_named(argv)))
        return RTF
    monkeypatch.setattr(clipboard_macos, 'run_tool', record)
    return asked


def test_written_names_file(tmp_path: Path) -> None:
    """One shape of a copy is written into a folder and named there."""
    named = written(tmp_path, RTF_NAME, RTF)
    assert Path(named) == tmp_path / RTF_NAME
    assert Path(named).read_bytes() == RTF


def test_two_programs_run(runs: list[Run]) -> None:
    """A copy is made by one program and given away by another."""
    copy_to_clipboard(COPY)
    assert [run.argv[0] for run in runs] == ['textutil', 'osascript']


def test_html_to_textutil(runs: list[Run]) -> None:
    """The HTML of the note is what the rich text is made from."""
    copy_to_clipboard(COPY)
    assert runs[0].argv == TEXTUTIL
    assert runs[0].data == HTML.encode('utf-8')


def test_script_is_run(runs: list[Run]) -> None:
    """The script that fills the pasteboard is run with two files."""
    copy_to_clipboard(COPY)
    assert runs[1].argv[:len(OSASCRIPT)] == OSASCRIPT
    assert len(runs[1].argv) == len(OSASCRIPT) + 2


def test_both_shapes_given(runs: list[Run]) -> None:
    """The script is given the rich text and the plain text alike."""
    copy_to_clipboard(COPY)
    assert runs[1].files == (RTF, TEXT.encode('utf-8'))


def test_files_are_named(runs: list[Run]) -> None:
    """The two files are told apart by the names they are given."""
    copy_to_clipboard(COPY)
    named = runs[1].argv[len(OSASCRIPT):]
    assert [Path(word).name for word in named] == [RTF_NAME, TEXT_NAME]


def test_files_taken_away(runs: list[Run]) -> None:
    """The files of a copy are gone once the copy has been made."""
    copy_to_clipboard(COPY)
    named = runs[1].argv[len(OSASCRIPT):]
    assert not [word for word in named if Path(word).exists()]


def test_empty_note_copied(runs: list[Run]) -> None:
    """A note holding nothing at all is copied as the nothing it is."""
    copy_to_clipboard(RichText('', ''))
    assert runs[0].data == b''
    assert runs[1].files == (RTF, b'')


def pasteboard_shapes() -> str:
    """Return what the pasteboard of this machine holds just now."""
    done = subprocess.run(['osascript', '-e', 'clipboard info'],
                          capture_output=True, check=True)
    return done.stdout.decode('utf-8')


def pasted_text() -> str:
    """Return the plain text that the pasteboard offers just now."""
    done = subprocess.run(['pbpaste'], capture_output=True, check=True)
    return done.stdout.decode('utf-8')


@pytest.mark.focus_sensitive
@pytest.mark.skipif(not ON_MACOS, reason='the pasteboard of macOS only')
def test_pasteboard_trip() -> None:
    """A copy really made offers both of its shapes to be pasted.

    This one fills the pasteboard of whoever runs it, which is why
    it is left out of the build and run by hand.
    """
    copy_to_clipboard(COPY)
    assert 'RTF' in pasteboard_shapes()
    assert pasted_text() == TEXT
