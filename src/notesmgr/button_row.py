#! /usr/local/bin/python3
"""The row of buttons above the note, and how it is made to fit."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from tkinter import ttk
from typing import AbstractSet, Callable, NamedTuple, Optional, Sequence
from notesmgr.menu_bar import entry_state

GAP = 4
"""Pixels left between two buttons that stand side by side."""


class ButtonSpec(NamedTuple):
    """One button of the row, and what pressing it does.

    A button whose operation belongs to a later step of the plan has
    no command, and is greyed out whatever is selected, so that the
    row is the whole row from the start.
    """

    label: str
    command: Optional[Callable[[], None]] = None


def grid_width(widths: Sequence[int], columns: int, gap: int) -> int:
    """Return how wide a grid of buttons of these widths is.

    The buttons are placed row by row, so the buttons of one column
    are every columns-th of them, and a column is as wide as the
    widest button standing in it.

    Args:
        widths: How wide each button is, in the order they are shown.
        columns: How many buttons stand side by side.
        gap: Pixels left beside each button.

    Returns:
        The width the grid needs, and nothing for no buttons at all.
    """
    if columns < 1:
        return 0
    return sum(max(widths[column::columns]) + gap
               for column in range(min(columns, len(widths))))


def fitting_columns(widths: Sequence[int], available: int, gap: int) -> int:
    """Return how many buttons to put side by side in a given width.

    The buttons are spread over the fewest rows that fit, so that a
    wide panel shows one row and a narrow one shows several rows of
    about the same length rather than one long row and a short one.
    A width too small for even one button still gives one column,
    because a button cut off at the edge is better than none at all.

    Args:
        widths: How wide each button is, in the order they are shown.
        available: Pixels the row has to lay the buttons out in.
        gap: Pixels left beside each button.

    Returns:
        How many buttons stand side by side, at least one.
    """
    for rows in range(1, len(widths) + 1):
        columns = (len(widths) + rows - 1) // rows
        if grid_width(widths, columns, gap) <= available:
            return columns
    return 1


class ButtonRow:
    """The buttons above the note, in as few rows as the width allows.

    A button is as wide as its text and the theme of the platform
    make it, and the panel is as wide as the user makes the window,
    so the buttons are laid out again whenever the width changes.
    That way none of them is ever cut off at the edge of the panel,
    at any size the window can be given.
    """

    def __init__(self, parent: tkinter.Misc,
                 specs: Sequence[ButtonSpec]) -> None:
        """Build the described buttons in a frame of their own.

        Args:
            parent: The widget that the row is placed in.
            specs: The buttons, in the order they are shown.
        """
        self.frame = ttk.Frame(parent)
        self.specs = list(specs)
        self.buttons = [self._built(spec) for spec in specs]
        self.working = {spec.label: button
                        for spec, button in zip(specs, self.buttons)
                        if spec.command is not None}
        self.columns = 0
        self.lay_out(max(len(self.buttons), 1))
        self.frame.bind('<Configure>', self._width_changed)

    def _built(self, spec: ButtonSpec) -> ttk.Button:
        """Return one button of the row, greyed out to start with."""
        button = ttk.Button(self.frame, text=spec.label,
                            state=entry_state(False))
        if spec.command is not None:
            button.configure(command=spec.command)
        return button

    def _width_changed(self, event: 'tkinter.Event[ttk.Frame]') -> None:
        """Lay the buttons out again when the row has another width."""
        self.fit_into(event.width)

    def widths(self) -> list[int]:
        """Return how wide each button of the row asks to be."""
        return [button.winfo_reqwidth() for button in self.buttons]

    def fit_into(self, available: int) -> None:
        """Lay the buttons out for a row of the given width.

        Laying out a grid that is already laid out that way would
        make Tk report another width and ask again, so it is only
        done when another number of buttons fits now.

        Args:
            available: Pixels the row has to lay the buttons out in.
        """
        columns = fitting_columns(self.widths(), available, GAP)
        if columns != self.columns:
            self.lay_out(columns)

    def lay_out(self, columns: int) -> None:
        """Put the buttons into a grid so many buttons wide."""
        self.columns = columns
        for index, button in enumerate(self.buttons):
            button.grid(row=index // columns, column=index % columns,
                        padx=GAP // 2, pady=GAP // 2, sticky=tkinter.W)

    def offer(self, labels: AbstractSet[str]) -> None:
        """Let the buttons that can be used now be pressed.

        A button whose operation belongs to a later step of the plan
        has nothing to do when pressed, and stays greyed out however
        much the selection would allow it.

        Args:
            labels: What the buttons that can be used now say.
        """
        for label, button in self.working.items():
            button.configure(state=entry_state(label in labels))
