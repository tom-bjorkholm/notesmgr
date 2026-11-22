#! /usr/local/bin/python3
"""Laying a table of a note out in columns of monospaced text."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import StrEnum
from textwrap import wrap
from typing import NamedTuple, Optional, Sequence

CELL_GAP = ' │ '
"""What is written between two cells of the same row."""

RULE_GAP = '─┼─'
"""What is written between two cells of the line under the headings."""

RULE_CHAR = '─'
"""What the line under the headings of a table is drawn with."""


class Align(StrEnum):
    """Which side of its column the text of a cell is written against."""

    LEFT = 'left'
    CENTER = 'center'
    RIGHT = 'right'


class Table(NamedTuple):
    """The cells of a table of a note, and how its columns line up.

    The table is kept as cells rather than as text, because how wide
    its columns are made depends on how wide the area that it is
    drawn in is. A row is allowed to hold fewer cells than the widest
    row of the table does, and the headings are the first rows.
    """

    rows: tuple[tuple[str, ...], ...]
    aligns: tuple[Align, ...] = ()
    headings: int = 0

    def holds_text(self) -> bool:
        """Return whether any cell of the table holds any text."""
        return any(any(row) for row in self.rows)


def cell_align(style: str) -> Align:
    """Return the alignment that the style of a cell asks for.

    Args:
        style: The style attribute of a cell of the HTML of a note,
            empty for a cell that carries none.

    Returns:
        What the text-align of the style says, and LEFT when it says
        nothing, which is what a markdown table without colons means.
    """
    for align in (Align.CENTER, Align.RIGHT):
        if f'text-align: {align}' in style:
            return align
    return Align.LEFT


def squared(rows: Sequence[Sequence[str]], columns: int) -> list[list[str]]:
    """Return the rows with every one of them holding every column.

    A markdown table is allowed to leave the cells at the end of a
    row out, and every row holding every column is what lets the
    rest of the laying out be written without asking each time.
    """
    return [list(row) + [''] * (columns - len(row)) for row in rows]


def every_align(aligns: Sequence[Align], columns: int) -> list[Align]:
    """Return an alignment for every column, LEFT for the unsaid ones."""
    kept = list(aligns[:columns])
    return kept + [Align.LEFT] * (columns - len(kept))


def column_width(rows: Sequence[Sequence[str]], index: int) -> int:
    """Return how wide one column of a table is when nothing is wrapped.

    A column is as wide as its widest cell, and one character wide
    when all of its cells are empty, so that the line under the
    headings is drawn for it as well.
    """
    return max(1, max(len(row[index]) for row in rows))


def longest_word(rows: Sequence[Sequence[str]], index: int) -> int:
    """Return how wide one column must be to break no word, at least 1."""
    return max([1, *(len(word) for row in rows
                     for word in row[index].split())])


def capped(tops: Sequence[int], floors: Sequence[int],
           room: int) -> Optional[list[int]]:
    """Return the widest widths that fit the room under one cap.

    Every column is made as wide as it would like up to a cap that is
    the same for all of them, but never narrower than its floor, and
    the cap is as high as lets the columns fit. The narrow columns
    are then left whole, and the room that is short is taken from the
    widest ones.

    Args:
        tops: How wide each column would like to be, at least 1.
        floors: How narrow each column may be made, at most its top.
        room: How wide all the columns may be together.

    Returns:
        The width of each column, or None when not even the floors
        fit the room.
    """
    for cap in range(max(tops), 0, -1):
        widths = [min(top, max(cap, floor))
                  for top, floor in zip(tops, floors)]
        if sum(widths) <= room:
            return widths
    return None


def column_widths(rows: Sequence[Sequence[str]], columns: int,
                  room: int) -> list[int]:
    """Return how wide each column is made to fit the room it has.

    When every column fits as wide as its widest cell, that is how
    wide it is made. Otherwise the widest columns are cut down, but
    no column narrower than its longest word, so that the narrow
    columns are written whole and the long texts are wrapped. When
    not even the longest words fit, the longest words are cut down
    the same way, and those words are broken.

    Args:
        rows: The cells of each row, every row holding every column.
        columns: How many columns the table has, at least 1.
        room: How many characters wide all the columns may be
            together, the gaps between them not counted.

    Returns:
        The width of each column, at least 1, all of them 1 when not
        even that fits the room.
    """
    wanted = [column_width(rows, index) for index in range(columns)]
    words = [longest_word(rows, index) for index in range(columns)]
    return capped(wanted, words, room) or \
        capped(words, [1] * columns, room) or [1] * columns


def wrapped_cell(text: str, width: int) -> list[str]:
    """Return the lines that a cell takes up in a column of a width."""
    return wrap(text, width) or ['']


def line_at(lines: Sequence[str], number: int) -> str:
    """Return one line of a wrapped cell, empty past its last line."""
    return lines[number] if number < len(lines) else ''


def padded_cell(text: str, width: int, align: Align) -> str:
    """Return the text of a cell written against its side of a column."""
    if align is Align.CENTER:
        return text.center(width)
    if align is Align.RIGHT:
        return text.rjust(width)
    return text.ljust(width)


def row_lines(row: Sequence[str], widths: Sequence[int],
              aligns: Sequence[Align]) -> list[str]:
    """Return the lines that one row of a table takes up.

    A row is as tall as the cell of it that takes the most lines,
    and the cells that take fewer are left blank underneath.
    """
    cells = [wrapped_cell(text, width) for text, width in zip(row, widths)]
    height = max(len(lines) for lines in cells)
    return [CELL_GAP.join(
        padded_cell(line_at(lines, number), width, align)
        for lines, width, align in zip(cells, widths, aligns)).rstrip()
        for number in range(height)]


def rule_line(widths: Sequence[int]) -> str:
    """Return the line that is drawn under the headings of a table."""
    return RULE_GAP.join(RULE_CHAR * width for width in widths)


def table_text(table: Table, width: int) -> str:
    """Return a table written in columns of monospaced text.

    Args:
        table: The cells of the table and how its columns line up.
        width: How many characters wide the table may be, which it
            is made wider than only when even one character for
            each column does not fit.

    Returns:
        The lines of the table, and nothing at all for a table that
        holds no cells to write.
    """
    columns = max((len(row) for row in table.rows), default=0)
    if not columns:
        return ''
    cells = squared(table.rows, columns)
    room = width - len(CELL_GAP) * (columns - 1)
    widths = column_widths(cells, columns, room)
    sides = every_align(table.aligns, columns)
    lines: list[str] = []
    for number, row in enumerate(cells):
        lines.extend(row_lines(row, widths, sides))
        if number + 1 == table.headings:
            lines.append(rule_line(widths))
    return '\n'.join(lines)
