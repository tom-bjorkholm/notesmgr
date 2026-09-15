#! /usr/local/bin/python3
"""Tests for reading the text of a note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from test_notesmgr.helpers import write_file
from notesmgr.note_text import NOT_READ, NOT_UTF8, TOO_LONG, read_note_text

LIMIT = 100
"""How much of a note these tests let it show."""


def note_of(path: Path, text: str) -> Path:
    """Write a note holding the given text and return it."""
    return write_file(path, text)


@pytest.mark.parametrize('text', ['', 'One line\n', 'No newline at the end',
                                  'Two\nlines\n', 'Å i Ö, þ and 😀\n'])
def test_text_is_given_back(tmp_path: Path, text: str) -> None:
    """A note that can be read is given back as it was written."""
    note = read_note_text(note_of(tmp_path / 'a.md.txt', text), LIMIT)
    assert note == (text, '')


def test_line_endings_evened(tmp_path: Path) -> None:
    """Lines written by another system end the way this one ends them."""
    path = tmp_path / 'a.md.txt'
    path.write_bytes(b'first\r\nsecond\r\n')
    assert read_note_text(path, LIMIT).text == 'first\nsecond\n'


def test_not_utf8_not_shown(tmp_path: Path) -> None:
    """A note that is no UTF-8 text is not shown, and says why."""
    path = tmp_path / 'a.md.txt'
    path.write_bytes(b'text and then \xff\xfe bytes\n')
    assert read_note_text(path, LIMIT) == ('', NOT_UTF8)


def test_missing_note_told(tmp_path: Path) -> None:
    """A note that is not there is reported and shows nothing."""
    note = read_note_text(tmp_path / 'gone.md.txt', LIMIT)
    assert note.text == ''
    assert note.warning.startswith(NOT_READ.split('\n', maxsplit=1)[0])


def test_folder_is_no_note(tmp_path: Path) -> None:
    """A folder holds no text to show, which is reported as well."""
    assert read_note_text(tmp_path, LIMIT).text == ''
    assert read_note_text(tmp_path, LIMIT).warning


def test_whole_note_fits(tmp_path: Path) -> None:
    """A note exactly as long as may be shown is shown whole."""
    text = 'a' * LIMIT
    assert read_note_text(note_of(tmp_path / 'a.md.txt', text), LIMIT) == \
        (text, '')


def test_long_note_is_cut(tmp_path: Path) -> None:
    """A note longer than may be shown is shown up to the limit."""
    path = note_of(tmp_path / 'a.md.txt', 'b' * (LIMIT + 1))
    assert read_note_text(path, LIMIT) == ('b' * LIMIT,
                                           TOO_LONG.format(limit=LIMIT))


def test_cut_counts_chars(tmp_path: Path) -> None:
    """The limit counts characters, so no character is cut in two."""
    path = note_of(tmp_path / 'a.md.txt', 'å' * (LIMIT * 2))
    assert read_note_text(path, LIMIT).text == 'å' * LIMIT


def test_large_note_is_cut(tmp_path: Path) -> None:
    """A note far larger than the limit is still only read that far."""
    path = note_of(tmp_path / 'a.md.txt', 'c' * 500000)
    note = read_note_text(path, LIMIT)
    assert len(note.text) == LIMIT
    assert note.warning
