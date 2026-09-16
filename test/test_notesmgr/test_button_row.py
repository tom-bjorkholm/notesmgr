#! /usr/local/bin/python3
"""Tests for the row of buttons above the note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from functools import partial
from typing import Callable
import pytest
from notesmgr.button_row import GAP, ButtonRow, ButtonSpec, fitting_columns, \
    grid_width

MEASURED = [98, 136, 98, 64, 67, 80, 58, 75]
"""How wide the eight buttons of the note panel are on macOS.

Measured in the aqua theme, which is the widest of the themes that
notesmgr is used with, and used here so that the widths these tests
reason about are widths that really occur.
"""

ONE_ROW = 708
"""Width that the eight measured buttons need side by side."""

LABELS = ['First', 'Second', 'Third', 'Fourth', 'Fifth']
"""What the buttons of the row of these tests say."""

WORKING = ['First', 'Fourth']
"""Which of those buttons have something to do when pressed."""


@pytest.fixture(name='pressed')
def fixture_pressed() -> list[str]:
    """Provide the list that the buttons report their presses into."""
    return []


def press(label: str, pressed: list[str]) -> Callable[[], None]:
    """Return what a button does, which is to report that it was pressed."""
    return partial(pressed.append, label)


@pytest.fixture(name='row')
def fixture_row(top_window: tkinter.Toplevel, pressed: list[str]) -> ButtonRow:
    """Provide a row of five buttons, two of which do something."""
    specs = [ButtonSpec(label, press(label, pressed))
             if label in WORKING else ButtonSpec(label)
             for label in LABELS]
    return ButtonRow(top_window, specs)


def labels_of(row: ButtonRow) -> list[str]:
    """Return what the buttons of a row say, in the order they are in."""
    return [str(button.cget('text')) for button in row.buttons]


def places_of(row: ButtonRow) -> list[tuple[int, int]]:
    """Return the grid row and column that each button is placed in."""
    return [(int(button.grid_info()['row']), int(button.grid_info()['column']))
            for button in row.buttons]


def states_of(row: ButtonRow) -> list[str]:
    """Return whether each button of a row can be pressed."""
    return [str(button.cget('state')) for button in row.buttons]


@pytest.mark.parametrize('widths,columns,gap,expected', [
    ([100, 50], 2, 0, 150),
    ([100, 50], 2, 4, 158),
    ([100, 50], 1, 0, 100),
    ([100, 50, 30], 2, 0, 150),
    ([100, 50, 30], 3, 0, 180),
    ([100, 50], 5, 0, 150),
    ([100], 1, 6, 106),
    ([], 3, 4, 0),
    ([100, 50], 0, 4, 0),
    ([100, 50], -1, 4, 0)])
def test_grid_width(widths: list[int], columns: int, gap: int,
                    expected: int) -> None:
    """A column is as wide as the widest button standing in it."""
    assert grid_width(widths, columns, gap) == expected


def test_one_row_width() -> None:
    """The measured buttons side by side need the width they are said to."""
    assert grid_width(MEASURED, len(MEASURED), GAP) == ONE_ROW


@pytest.mark.parametrize('available,expected', [
    (2000, 8),
    (ONE_ROW, 8),
    (ONE_ROW - 1, 4),
    (724, 8),
    (700, 4),
    (423, 4),
    (422, 3),
    (344, 3),
    (343, 2),
    (100, 1),
    (0, 1)])
def test_fitting_columns(available: int, expected: int) -> None:
    """The buttons are spread over the fewest rows that fit the width."""
    assert fitting_columns(MEASURED, available, GAP) == expected


def test_no_buttons_fit() -> None:
    """A row holding no buttons at all asks for one column."""
    assert fitting_columns([], 500, GAP) == 1


@pytest.mark.parametrize('available', [200, 400, 600, 800, 1000])
def test_layout_fits(available: int) -> None:
    """Whatever the width, what is laid out is no wider than it.

    The one exception is a width too small for the widest button
    alone, which is narrower than any window notesmgr can be given.
    """
    columns = fitting_columns(MEASURED, available, GAP)
    assert grid_width(MEASURED, columns, GAP) <= available


def test_wider_is_never_worse() -> None:
    """A wider row never puts fewer buttons side by side."""
    fitting = [fitting_columns(MEASURED, available, GAP)
               for available in range(100, 1000, 7)]
    assert fitting == sorted(fitting)


def test_buttons_are_built(row: ButtonRow) -> None:
    """The row holds the buttons it was described, in that order."""
    assert labels_of(row) == LABELS


def test_all_start_dead(row: ButtonRow) -> None:
    """Every button starts out greyed out, there being nothing to act on."""
    assert states_of(row) == ['disabled'] * len(LABELS)


def test_only_working_offered(row: ButtonRow) -> None:
    """A button with nothing to do is never offered to be pressed."""
    row.offer(set(LABELS))
    assert [label for label in LABELS
            if states_of(row)[LABELS.index(label)] == 'normal'] == WORKING


def test_offering_one(row: ButtonRow) -> None:
    """Only the buttons that are named are offered to be pressed."""
    row.offer({WORKING[1]})
    assert [label for label in LABELS
            if states_of(row)[LABELS.index(label)] == 'normal'] == \
        [WORKING[1]]


def test_offering_taken_back(row: ButtonRow) -> None:
    """The buttons are greyed out again when there is nothing to act on."""
    row.offer(set(LABELS))
    row.offer(set())
    assert states_of(row) == ['disabled'] * len(LABELS)


def test_pressing_a_button(row: ButtonRow, pressed: list[str]) -> None:
    """A button that is offered does what it was described to do."""
    row.offer(set(LABELS))
    row.working[WORKING[0]].invoke()
    assert pressed == [WORKING[0]]


def test_specs_are_kept(row: ButtonRow) -> None:
    """The row remembers what its buttons are and what they do."""
    assert [spec.label for spec in row.specs] == LABELS


def test_starts_as_one_row(row: ButtonRow) -> None:
    """Before any width is known the buttons stand side by side."""
    assert row.columns == len(LABELS)
    assert places_of(row) == [(0, place) for place in range(len(LABELS))]


def test_laid_out_in_rows(row: ButtonRow) -> None:
    """Fewer columns than buttons puts the rest on the rows below."""
    row.lay_out(2)
    assert places_of(row) == [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0)]


def test_narrow_row_wraps(row: ButtonRow) -> None:
    """A row too narrow for every button lays them out in several rows."""
    widest = max(row.widths())
    row.fit_into(widest + GAP)
    assert row.columns == 1
    assert places_of(row) == [(place, 0) for place in range(len(LABELS))]


def test_wide_row_is_one(row: ButtonRow) -> None:
    """A row wide enough for every button puts them side by side."""
    row.fit_into(2000)
    assert row.columns == len(LABELS)


def test_width_kept_as_it_was(row: ButtonRow) -> None:
    """A width that changes nothing leaves the buttons where they are."""
    row.fit_into(2000)
    places = places_of(row)
    row.fit_into(2000)
    assert places_of(row) == places
