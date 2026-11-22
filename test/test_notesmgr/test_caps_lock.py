#! /usr/local/bin/python3
"""Tests that the shortcuts of letters are typed with Caps Lock on."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from functools import partial
from tkinter import ttk
import pytest
from test_notesmgr.tk_windows import show_filled
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DUPLICATE, EDIT, \
    FOCUS_FOLDER, NEW, NEW_FOLDER, SHOW_ALL
from notesmgr.shortcuts import Shortcut, modifier, tk_window_system, \
    window_shortcuts

QUIT = 'quit'
REFRESH = 'refresh'
LETTER_SHORTCUTS = [QUIT, REFRESH, COPY_RAW, COPY_FORMATTED, DUPLICATE,
                    EDIT, NEW, NEW_FOLDER, FOCUS_FOLDER, SHOW_ALL]
"""The shortcuts that are typed with a letter held with Cmd or Ctrl."""


def named_shortcuts(window_system: str) -> dict[str, Shortcut]:
    """Return every shortcut of the main window by what it does."""
    keys = window_shortcuts(window_system)
    return {QUIT: keys.quit, REFRESH: keys.refresh, 'larger': keys.larger,
            'smaller': keys.smaller, 'normal': keys.normal, **keys.actions}


def record(pressed: list[str], name: str,
           _event: 'tkinter.Event[tkinter.Misc]') -> None:
    """Add the name of a shortcut that was run to those that were run."""
    pressed.append(name)


def record_presses(window: tkinter.Misc,
                   shortcuts: dict[str, Shortcut]) -> list[str]:
    """Bind every shortcut on a window to record what it stands for.

    Returns:
        The list that each shortcut adds its name to when it is run.
    """
    pressed: list[str] = []
    for name, shortcut in shortcuts.items():
        for sequence in shortcut.sequences:
            window.bind(sequence, partial(record, pressed, name))
    return pressed


def typed(window_system: str, shortcut: Shortcut, lock: str) -> str:
    """Return the key event of a person typing the letter of a shortcut.

    The letter is given small, as the key itself, and Tk works out what
    it is called with Shift and Caps Lock held, as for a real key.

    Args:
        window_system: The windowing system that Tk is using.
        shortcut: The shortcut, whose menu label ends with its letter.
        lock: Lock- for Caps Lock on, and nothing for Caps Lock off.
    """
    held = modifier(window_system)[0]
    shift = 'Shift-' if '+Shift+' in shortcut.label else ''
    return f'<{held}-{lock}{shift}Key-{shortcut.label[-1].lower()}>'


@pytest.mark.focus_sensitive
@pytest.mark.parametrize('lock', ['', 'Lock-'])
@pytest.mark.parametrize('name', LETTER_SHORTCUTS)
def test_letter_typed(top_window: tkinter.Toplevel, lock: str,
                      name: str) -> None:
    """A letter shortcut does what it stands for, Caps Lock on or not.

    Only that one shortcut is run, so neither Cmd+C is taken for
    Cmd+Shift+C nor Cmd+L for Cmd+Shift+L, whatever case Tk gives.
    """
    window_system = tk_window_system(top_window)
    shortcuts = named_shortcuts(window_system)
    pressed = record_presses(top_window, shortcuts)
    show_filled(ttk.Frame(top_window))
    top_window.focus_force()
    top_window.update()
    event = typed(window_system, shortcuts[name], lock)
    top_window.event_generate(event, when='now')
    assert pressed == [name]
