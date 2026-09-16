#! /usr/local/bin/python3
"""Laying a table of a note out in columns of monospaced text."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from enum import StrEnum
from textwrap import wrap
from typing import Sequence

MAX_COLUMN = 24
"""Most characters that one column of a table is made wide.

A cell holding more than this is written over several lines instead
of making the table wider than the panel can show.
"""

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
    """Return how wide one column of a table is made.

    A column is as wide as its widest cell, up to the most a column
    may be, and one character wide when all of its cells are empty,
    so that the line under the headings is drawn for it as well.
    """
    return max(1, min(MAX_COLUMN, max(len(row[index]) for row in rows)))


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


def table_text(rows: Sequence[Sequence[str]], aligns: Sequence[Align],
               headings: int = 0) -> str:
    """Return a table written in columns of monospaced text.

    Args:
        rows: The cells of each row, where a row is allowed to hold
            fewer cells than the widest row of the table does.
        aligns: Which side of its column each column is written
            against, as far as the table said.
        headings: How many rows at the top of the table are heading
            rows, which is what the line across it is drawn under.

    Returns:
        The lines of the table, and nothing at all for a table that
        holds no cells to write.
    """
    columns = max((len(row) for row in rows), default=0)
    if not columns:
        return ''
    cells = squared(rows, columns)
    widths = [column_width(cells, index) for index in range(columns)]
    sides = every_align(aligns, columns)
    lines: list[str] = []
    for number, row in enumerate(cells):
        lines.extend(row_lines(row, widths, sides))
        if number + 1 == headings:
            lines.append(rule_line(widths))
    return '\n'.join(lines)
