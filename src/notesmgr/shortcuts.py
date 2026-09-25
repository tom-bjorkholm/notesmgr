#! /usr/local/bin/python3
"""The keyboard shortcuts of the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Mapping, NamedTuple, Sequence
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, DUPLICATE, \
    EDIT, MOVE_DOWN, MOVE_UP, NEW, NEW_FOLDER

ZOOM_IN_KEYS = ('plus', 'equal', 'KP_Add')
"""What Tk calls the keys that ask for a larger note."""

ZOOM_OUT_KEYS = ('minus', 'KP_Subtract')
"""What Tk calls the keys that ask for a smaller note."""

NORMAL_SIZE_KEYS = ('Key-0', 'KP_0')
"""What Tk calls the keys that ask for the note in its first size."""

TREE_EDIT_KEYS = ('<Return>', '<KP_Enter>')
"""What Tk calls the keys of the tree that edit the selected note."""

ACTION_KEYS: Mapping[str, tuple[str, str]] = {
    COPY_RAW: ('c', 'C'),
    COPY_FORMATTED: ('Shift-C', 'Shift+C'),
    DUPLICATE: ('d', 'D'),
    EDIT: ('e', 'E'),
    NEW: ('n', 'N'),
    DELETE: ('BackSpace', 'Backspace'),
    MOVE_UP: ('Up', 'Up'),
    MOVE_DOWN: ('Down', 'Down'),
    NEW_FOLDER: ('Shift-N', 'Shift+N')}
"""The key of each action held with Cmd or Ctrl, and what it is called.

A capital letter is what Tk calls a letter typed with the shift key
held down, so the shift key is named along with it.
"""


class Shortcut(NamedTuple):
    """A keyboard shortcut: its Tk event sequences and its menu label.

    A shortcut has more than one sequence wherever more than one key
    stands for it, such as the plus of the keypad and the plus that
    is typed with the shift key held down.
    """

    sequences: tuple[str, ...]
    label: str


class Shortcuts(NamedTuple):
    """The keyboard shortcuts that the main window listens for.

    The actions are known by what their buttons and menu entries are
    called, so that a button, its menu entry and its keys are one
    action wherever it is asked for.
    """

    quit: Shortcut
    larger: Shortcut
    smaller: Shortcut
    normal: Shortcut
    actions: Mapping[str, Shortcut]


def tk_window_system(window: tkinter.Misc) -> str:
    """Return the windowing system Tk uses: aqua, win32 or x11."""
    return str(window.tk.call('tk', 'windowingsystem'))


def quit_shortcut(window_system: str) -> Shortcut:
    """Return the keyboard shortcut that closes the main window.

    macOS closes a window with Cmd+W, while Windows and the X11
    desktops leave a program with Ctrl+Q.
    """
    if window_system == 'aqua':
        return Shortcut(('<Command-w>',), 'Cmd+W')
    return Shortcut(('<Control-q>',), 'Ctrl+Q')


def modifier(window_system: str) -> tuple[str, str]:
    """Return the key held down for a shortcut, and what it is called.

    macOS holds the command key down where Windows and the X11
    desktops hold the control key down.
    """
    if window_system == 'aqua':
        return ('Command', 'Cmd')
    return ('Control', 'Ctrl')


def held_shortcut(window_system: str, keysyms: Sequence[str],
                  shown: str) -> Shortcut:
    """Return a shortcut of the held key and the keys that stand for it.

    Args:
        window_system: The windowing system that Tk is using.
        keysyms: What Tk calls each of the keys that stand for it.
        shown: What the key is called on the menu entry.

    Returns:
        The shortcut to bind and to show.
    """
    held, name = modifier(window_system)
    sequences = tuple(f'<{held}-{keysym}>' for keysym in keysyms)
    return Shortcut(sequences, f'{name}+{shown}')


def action_shortcuts(window_system: str) -> dict[str, Shortcut]:
    """Return the shortcut of every action that has one, by action."""
    return {action: held_shortcut(window_system, (keysym,), shown)
            for action, (keysym, shown) in ACTION_KEYS.items()}


def window_shortcuts(window_system: str) -> Shortcuts:
    """Return the shortcuts of the main window on a windowing system.

    Making a note larger is asked for with a plus, which is typed
    with the shift key held down on most keyboards and is a key of
    its own on the keypad, so every key that stands for it is bound
    and the plainest of them is the one that is shown.
    """
    return Shortcuts(
        quit=quit_shortcut(window_system),
        larger=held_shortcut(window_system, ZOOM_IN_KEYS, '+'),
        smaller=held_shortcut(window_system, ZOOM_OUT_KEYS, '-'),
        normal=held_shortcut(window_system, NORMAL_SIZE_KEYS, '0'),
        actions=action_shortcuts(window_system))
