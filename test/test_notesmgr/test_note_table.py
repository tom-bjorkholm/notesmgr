#! /usr/local/bin/python3
"""Tests for laying a table of a note out in columns of text."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence
import pytest
from notesmgr.note_table import CELL_GAP, RULE_GAP, Align, Table, \
    capped, cell_align, column_width, column_widths, every_align, \
    longest_word, padded_cell, row_lines, rule_line, squared, table_text, \
    wrapped_cell

HEAD = ('Construct', 'Yes', 'Note')
"""The heading row of the table that these tests lay out."""

BODY = ('Heading', 'yes', 'six levels')
"""A row of the table that these tests lay out."""

WIDE = 200
"""A width that every table of these tests fits in unwrapped."""

KEYS = Table((('Button', 'mac', 'What it does'),
              ('Copy raw', 'Cmd+C', 'Copies the note as it is written. '
               'When part of the note is selected, the key copies just '
               'that part.')), (), 1)
"""A table of short columns and one long one, as the guide has."""


def widths_of(text: str) -> list[int]:
    """Return how wide each column is, by the line under the headings."""
    rule = next(line for line in text.split('\n') if RULE_GAP in line)
    return [len(part) for part in rule.split(RULE_GAP)]


@pytest.mark.parametrize('style,expected', [
    ('', Align.LEFT),
    ('text-align: center;', Align.CENTER),
    ('text-align: right;', Align.RIGHT),
    ('text-align: left;', Align.LEFT),
    ('text-align:center;', Align.LEFT),
    ('color: red;', Align.LEFT)])
def test_cell_align(style: str, expected: Align) -> None:
    """A cell lines up the way its own style says, and left by default."""
    assert cell_align(style) == expected


def test_rows_are_squared() -> None:
    """Every row is given a cell for every column of the table."""
    assert squared([['a', 'b'], ['c']], 2) == [['a', 'b'], ['c', '']]


def test_squared_full_rows() -> None:
    """A row that holds every column already is left as it is."""
    assert squared([['a', 'b']], 2) == [['a', 'b']]


def test_align_of_columns() -> None:
    """A column that the table said nothing about lines up to the left."""
    assert every_align([Align.RIGHT], 3) == [Align.RIGHT, Align.LEFT,
                                             Align.LEFT]


def test_extra_aligns() -> None:
    """Alignments past the last column are dropped."""
    assert every_align([Align.RIGHT, Align.CENTER], 1) == [Align.RIGHT]


@pytest.mark.parametrize('cells,expected', [
    (['ab', 'abcd'], 4),
    (['', ''], 1),
    (['a' * 100], 100)])
def test_column_width(cells: Sequence[str], expected: int) -> None:
    """A column is as wide as its widest cell, however wide that is."""
    assert column_width([[cell] for cell in cells], 0) == expected


@pytest.mark.parametrize('cells,expected', [
    (['one three', 'four'], 5),
    (['', ''], 1),
    (['  '], 1),
    (['a' * 30], 30)])
def test_longest_word(cells: Sequence[str], expected: int) -> None:
    """A column needs room for its longest word, and at least 1."""
    assert longest_word([[cell] for cell in cells], 0) == expected


@pytest.mark.parametrize('tops,floors,room,expected', [
    ([2, 4], [1, 1], 6, [2, 4]),
    ([2, 4], [1, 1], 20, [2, 4]),
    ([5, 23], [2, 5], 15, [5, 10]),
    ([7, 9], [4, 6], 12, [6, 6]),
    ([10, 10], [1, 9], 12, [3, 9]),
    ([4, 8], [4, 8], 6, None),
    ([3], [1], 0, None)])
def test_capped(tops: list[int], floors: list[int], room: int,
                expected: Optional[list[int]]) -> None:
    """The widest columns are cut down to fit, none below its floor."""
    assert capped(tops, floors, room) == expected


@pytest.mark.parametrize('rows,room,expected', [
    ([['ab', 'abcd']], 10, [2, 4]),
    ([['ab', 'abcd']], 6, [2, 4]),
    ([['a', 'one two three four']], 12, [1, 11]),
    ([['ab cd', 'one two three four five']], 15, [5, 10]),
    ([['aaaa bb', 'cc dddddd']], 12, [6, 6]),
    ([['aaaa', 'bbbbbbbb']], 6, [3, 3]),
    ([['aaaa', 'bbbb']], 1, [1, 1])])
def test_column_widths(rows: list[list[str]], room: int,
                       expected: list[int]) -> None:
    """Columns fit the room, keeping words whole while they fit."""
    assert column_widths(rows, len(rows[0]), room) == expected


@pytest.mark.parametrize('text,width,expected', [
    ('', 5, ['']),
    ('short', 8, ['short']),
    ('two words here', 8, ['two', 'words', 'here']),
    ('unbreakable', 5, ['unbre', 'akabl', 'e'])])
def test_wrapped_cell(text: str, width: int, expected: list[str]) \
        -> None:
    """A cell is written over as many lines as its column needs."""
    assert wrapped_cell(text, width) == expected


@pytest.mark.parametrize('align,expected', [
    (Align.LEFT, 'ab   '),
    (Align.CENTER, '  ab '),
    (Align.RIGHT, '   ab')])
def test_padded_cell(align: Align, expected: str) -> None:
    """A cell is written against the side of its column."""
    assert padded_cell('ab', 5, align) == expected


def test_row_of_one_line() -> None:
    """A row whose cells all fit is written as a single line."""
    lines = row_lines(['a', 'bb'], [2, 2], [Align.LEFT, Align.RIGHT])
    assert lines == ['a  │ bb']


def test_row_of_several_lines() -> None:
    """A row is as tall as the cell of it that takes the most lines."""
    sides = [Align.LEFT, Align.LEFT]
    lines = row_lines(['one', 'two words'], [3, 5], sides)
    assert lines == ['one │ two', '    │ words']


def test_rule_line() -> None:
    """The line under the headings is as wide as the table is."""
    assert rule_line([2, 3]) == '───┼────'
    assert rule_line([1]) == '─'


def test_empty_table() -> None:
    """A table that holds no cells at all is written as nothing."""
    assert table_text(Table(()), WIDE) == ''
    assert table_text(Table(((),)), WIDE) == ''


@pytest.mark.parametrize('rows,expected', [
    ((), False), (((),), False), ((('', ''),), False),
    ((('', 'a'),), True)])
def test_holds_text(rows: tuple[tuple[str, ...], ...], expected: bool) \
        -> None:
    """A table holds text when any one of its cells does."""
    assert Table(rows).holds_text() is expected


def test_table_of_headings() -> None:
    """The heading rows are told from the rest by the line under them."""
    text = table_text(Table((HEAD, BODY), (), 1), WIDE)
    lines = text.split('\n')
    assert len(lines) == 3
    assert set(lines[1]) == {'─', '┼'}
    assert lines[0].startswith('Construct')
    assert lines[2].startswith('Heading')


def test_no_heading_row() -> None:
    """A table with no heading row gets no line drawn across it."""
    text = table_text(Table((BODY, BODY)), WIDE)
    assert '┼' not in text
    assert len(text.split('\n')) == 2


def test_columns_line_up() -> None:
    """Every line of the table has its separators in the same place."""
    long_cell = 'a cell with rather a lot of text in it to be wrapped'
    table = Table((HEAD, BODY, ('Long', 'yes', long_cell)),
                  (Align.LEFT, Align.CENTER, Align.RIGHT), 1)
    text = table_text(table, 30)
    places = {tuple(index for index, letter in enumerate(line)
                    if letter in '│┼') for line in text.split('\n')}
    assert len(places) == 1


def test_missing_cells() -> None:
    """A row that names fewer cells than the table has is filled out."""
    text = table_text(Table((HEAD, ('Only one',)), (), 1), WIDE)
    assert text.split('\n')[2] == 'Only one  │     │'


def test_long_cell_is_wrapped() -> None:
    """A cell too wide for its column is wrapped and nothing is lost."""
    words = ' '.join(f'word{number}' for number in range(20))
    text = table_text(Table((('a', words),)), 40)
    assert max(len(line) for line in text.split('\n')) <= 40
    assert all(word in text for word in words.split())


def test_natural_width() -> None:
    """A table that fits is as wide as its cells, however wide it may be."""
    text = table_text(KEYS, WIDE)
    assert len(text.split('\n')) == 3
    assert widths_of(text) == [8, 5, len(KEYS.rows[1][2])]


@pytest.mark.parametrize('width', [40, 60, 80, 100])
def test_fits_the_width(width: int) -> None:
    """A table too wide is wrapped to the width, no line wider."""
    text = table_text(KEYS, width)
    assert max(len(line) for line in text.split('\n')) <= width
    assert widths_of(text)[:2] == [8, 5]


def test_long_column_widest() -> None:
    """The column that would like most room gets the most of it."""
    widths = widths_of(table_text(KEYS, 60))
    assert widths == [8, 5, 60 - 8 - 5 - 2 * len(CELL_GAP)]


def test_too_narrow() -> None:
    """A table narrower than its words breaks them to fit."""
    text = table_text(KEYS, 12)
    assert max(len(line) for line in text.split('\n')) <= 12
    assert widths_of(text) == [2, 2, 2]
