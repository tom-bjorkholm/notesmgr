#! /usr/local/bin/python3
"""Tests for the file that keeps the notes of a folder in order."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import stat
from pathlib import Path
import pytest
from test_notesmgr.helpers import write_notes, write_order as put_order
from notesmgr.errors import NotesmgrError
from notesmgr.order_file import ORDER_NAME, order_path, order_text, \
    parse_order, read_order_text, repair_order, repair_order_file, \
    write_order

NOTES = ['one.md.txt', 'two.md.txt', 'three.md.txt']
"""Notes that the folder of these tests holds."""


@pytest.fixture(name='folder')
def fixture_folder(tmp_path: Path) -> Path:
    """Provide a folder holding three notes and no order file."""
    write_notes(tmp_path, NOTES)
    return tmp_path


def test_order_path(tmp_path: Path) -> None:
    """The note order of a folder is kept in a hidden file in it."""
    assert order_path(tmp_path) == tmp_path / ORDER_NAME


@pytest.mark.parametrize('text,expected', [
    ('', []),
    ('a.md\n', ['a.md']),
    ('a.md\nb.md\n', ['a.md', 'b.md']),
    ('a.md\r\nb.md\r\n', ['a.md', 'b.md']),
    ('a.md\rb.md\r', ['a.md', 'b.md']),
    ('a.md', ['a.md']),
    ('\n\na.md\n\n\nb.md\n', ['a.md', 'b.md']),
    ('  a.md  \n\tb.md\t\n', ['a.md', 'b.md']),
    ('a.md\na.md\nb.md\n', ['a.md', 'b.md']),
    ('sub/a.md\na.md\n', ['a.md']),
    ('sub\\a.md\na.md\n', ['a.md']),
    ('.\n..\na.md\n', ['a.md'])])
def test_parse_order(text: str, expected: list[str]) -> None:
    """Anything a hand-written order file holds is taken for what it meant."""
    assert parse_order(text) == expected


def test_byte_order_mark(folder: Path) -> None:
    """A byte order mark left by an editor is no part of the first name."""
    (folder / ORDER_NAME).write_text('one.md.txt\n', encoding='utf-8-sig')
    assert parse_order(read_order_text(folder) or '') == ['one.md.txt']


@pytest.mark.parametrize('listed,existing,expected', [
    ([], [], []),
    ([], ['b.md', 'a.md'], ['a.md', 'b.md']),
    (['b.md', 'a.md'], ['a.md', 'b.md'], ['b.md', 'a.md']),
    (['gone.md', 'a.md'], ['a.md'], ['a.md']),
    (['b.md'], ['b.md', 'c.md', 'a.md'], ['b.md', 'a.md', 'c.md']),
    (['a.md'], [], []),
    (['b.md', 'a.md'], ['a.md'], ['a.md'])])
def test_repair_order(listed: list[str], existing: list[str],
                      expected: list[str]) -> None:
    """The order keeps what is there and adds what it did not mention."""
    assert repair_order(listed, existing) == expected


@pytest.mark.parametrize('names,expected', [
    ([], ''),
    (['a.md'], 'a.md\n'),
    (['a.md', 'b.md'], 'a.md\nb.md\n')])
def test_order_text(names: list[str], expected: str) -> None:
    """An order file holds one name per line and ends with a line end."""
    assert order_text(names) == expected


def test_no_order_file(folder: Path) -> None:
    """A folder that has no order file yet is read as an empty order."""
    assert read_order_text(folder) is None


def test_order_file_read(folder: Path) -> None:
    """An order file that is there is read as it stands."""
    put_order(folder, NOTES)
    assert read_order_text(folder) == 'one.md.txt\ntwo.md.txt\nthree.md.txt\n'


def test_folder_in_its_place(tmp_path: Path) -> None:
    """A folder where the order file should be is reported, not used.

    There is nothing to read in a folder, so the repair goes on to
    write the order, and the folder in the way is met there.
    """
    (tmp_path / ORDER_NAME).mkdir()
    assert read_order_text(tmp_path) is None
    with pytest.raises(NotesmgrError):
        repair_order_file(tmp_path, [])


@pytest.mark.skipif(os.name == 'nt', reason='file modes differ on Windows')
def test_unreadable_order(folder: Path) -> None:
    """An order file that may not be read is reported, not guessed at."""
    written = put_order(folder, NOTES)
    written.chmod(stat.S_IWUSR)
    try:
        with pytest.raises(NotesmgrError):
            read_order_text(folder)
    finally:
        written.chmod(stat.S_IRUSR | stat.S_IWUSR)


def test_write_is_atomic(folder: Path) -> None:
    """Writing an order leaves the order file and no file beside it."""
    write_order(folder, order_text(NOTES))
    assert read_order_text(folder) == order_text(NOTES)
    left = [path.name for path in folder.iterdir()
            if path.name.startswith(ORDER_NAME) and path.name != ORDER_NAME]
    assert not left


def test_write_refused(tmp_path: Path) -> None:
    """Writing into a folder that is not there is reported, not raised."""
    with pytest.raises(NotesmgrError):
        write_order(tmp_path / 'no_such', 'a.md\n')


def test_repair_writes_new(folder: Path) -> None:
    """A folder with no order file gets one, in alphabetical order."""
    assert repair_order_file(folder, NOTES) == ['one.md.txt', 'three.md.txt',
                                                'two.md.txt']
    assert read_order_text(folder) == order_text(['one.md.txt',
                                                  'three.md.txt',
                                                  'two.md.txt'])


def test_repair_keeps_order(folder: Path) -> None:
    """An order file that is already right is written again by nobody."""
    written = put_order(folder, NOTES)
    before = written.stat().st_mtime_ns
    assert repair_order_file(folder, NOTES) == NOTES
    assert written.stat().st_mtime_ns == before


def test_repair_tidies(folder: Path) -> None:
    """An order file that needed tidying is written back tidied."""
    written = folder / ORDER_NAME
    written.write_text('\none.md.txt\n\ntwo.md.txt\nthree.md.txt\n',
                       encoding='utf-8')
    assert repair_order_file(folder, NOTES) == NOTES
    assert written.read_text(encoding='utf-8') == order_text(NOTES)


def test_repair_drops_adds(folder: Path) -> None:
    """A note that is gone goes, and one nobody listed is listed last."""
    put_order(folder, ['gone.md.txt', 'two.md.txt'])
    order = repair_order_file(folder, NOTES)
    assert order == ['two.md.txt', 'one.md.txt', 'three.md.txt']
    assert read_order_text(folder) == order_text(order)


def test_repair_empty_folder(tmp_path: Path) -> None:
    """A folder holding no notes still gets an order file of its own."""
    assert repair_order_file(tmp_path, []) == []
    assert read_order_text(tmp_path) == ''
