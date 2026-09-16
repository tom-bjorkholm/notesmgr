#! /usr/local/bin/python3
"""Tests for laying a table of a note out in columns of text."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Sequence
import pytest
from notesmgr.note_table import MAX_COLUMN, Align, cell_align, \
    column_width, every_align, padded_cell, row_lines, rule_line, \
    squared, table_text, wrapped_cell

HEAD = ['Construct', 'Yes', 'Note']
"""The heading row of the table that these tests lay out."""

BODY = ['Heading', 'yes', 'six levels']
"""A row of the table that these tests lay out."""


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
    (['a' * (MAX_COLUMN + 10)], MAX_COLUMN)])
def test_column_width(cells: Sequence[str], expected: int) -> None:
    """A column is as wide as its widest cell, up to the most allowed."""
    assert column_width([[cell] for cell in cells], 0) == expected


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
    assert table_text([], []) == ''
    assert table_text([[]], []) == ''


def test_table_of_headings() -> None:
    """The heading rows are told from the rest by the line under them."""
    text = table_text([HEAD, BODY], [Align.LEFT] * 3, headings=1)
    lines = text.split('\n')
    assert len(lines) == 3
    assert set(lines[1]) == {'─', '┼'}
    assert lines[0].startswith('Construct')
    assert lines[2].startswith('Heading')


def test_no_heading_row() -> None:
    """A table with no heading row gets no line drawn across it."""
    text = table_text([BODY, BODY], [Align.LEFT] * 3)
    assert '┼' not in text
    assert len(text.split('\n')) == 2


def test_columns_line_up() -> None:
    """Every line of the table has its separators in the same place."""
    long_cell = 'a cell with rather a lot of text in it to be wrapped'
    text = table_text([HEAD, BODY, ['Long', 'yes', long_cell]],
                      [Align.LEFT, Align.CENTER, Align.RIGHT], headings=1)
    places = {tuple(index for index, letter in enumerate(line)
                    if letter in '│┼') for line in text.split('\n')}
    assert len(places) == 1


def test_missing_cells() -> None:
    """A row that names fewer cells than the table has is filled out."""
    text = table_text([HEAD, ['Only one']], [Align.LEFT] * 3, headings=1)
    assert text.split('\n')[2] == 'Only one  │     │'


def test_long_cell_is_wrapped() -> None:
    """A cell too wide for its column is wrapped and nothing is lost."""
    words = ' '.join(f'word{number}' for number in range(20))
    text = table_text([['a', words]], [Align.LEFT, Align.LEFT])
    assert max(len(line) for line in text.split('\n')) <= MAX_COLUMN + 10
    assert all(word in text for word in words.split())
