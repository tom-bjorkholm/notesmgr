#! /usr/local/bin/python3
"""The keyboard shortcuts of the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Mapping, NamedTuple, Sequence
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, DUPLICATE, \
    EDIT, FOCUS_FOLDER, MOVE_DOWN, MOVE_UP, NEW, NEW_FOLDER, RENAME, SHOW_ALL

ZOOM_IN_KEYS = ('plus', 'equal', 'KP_Add')
"""What Tk calls the keys that ask for a larger note."""

ZOOM_OUT_KEYS = ('minus', 'KP_Subtract')
"""What Tk calls the keys that ask for a smaller note."""

NORMAL_SIZE_KEYS = ('Key-0', 'KP_0')
"""What Tk calls the keys that ask for the note in its first size."""

REFRESH_KEYS = ('r',)
"""What Tk calls the key that asks for the open project to be read again."""

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
    NEW_FOLDER: ('Shift-N', 'Shift+N'),
    FOCUS_FOLDER: ('l', 'L'),
    SHOW_ALL: ('Shift-L', 'Shift+L')}
"""The key of each action held with Cmd or Ctrl, and what it is called.

A capital letter is what Tk calls a letter typed with the shift key
held down, so the shift key is named along with it. L is for local,
the folder in focus, and with Shift for the large view of them all.
"""

UNHELD_KEYS: Mapping[str, str] = {RENAME: 'F2'}
"""The key of each action typed with nothing held, by what Tk calls it.

F2 renames what is selected in the file managers of Windows and Linux,
and a function key types nothing, so it needs no Cmd or Ctrl held.
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
    refresh: Shortcut
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
        return held_shortcut(window_system, ('w',), 'W')
    return held_shortcut(window_system, ('q',), 'Q')


def modifier(window_system: str) -> tuple[str, str]:
    """Return the key held down for a shortcut, and what it is called.

    macOS holds the command key down where Windows and the X11
    desktops hold the control key down.
    """
    if window_system == 'aqua':
        return ('Command', 'Cmd')
    return ('Control', 'Ctrl')


def caps_lock_variants(keysym: str) -> tuple[str, ...]:
    """Return a key and what it is called when Caps Lock is on.

    Caps Lock adds Lock to the keys held down and changes nothing but
    the case of a letter. Tk calls a letter typed with Caps Lock on a
    capital letter, but where Shift is held as well, Windows and most
    Linux desktops call it a small letter, so both are returned. Held
    with Lock, they are more specific than the keys of the shortcuts
    without it, so Cmd+C is never taken for Cmd+Shift+C. A key that is
    not a letter is not changed by Caps Lock and is returned alone.

    Args:
        keysym: What Tk calls the key, with Shift- in front of a
            capital letter typed with the shift key held down.

    Returns:
        The key, followed by its two variants if it is a letter.
    """
    *held, letter = keysym.split('-')
    if len(letter) != 1 or not letter.isalpha():
        return (keysym,)
    prefix = '-'.join(['Lock', *held, ''])
    return (keysym, prefix + letter.upper(), prefix + letter.lower())


def held_shortcut(window_system: str, keysyms: Sequence[str],
                  shown: str) -> Shortcut:
    """Return a shortcut of the held key and the keys that stand for it.

    A letter is bound with Caps Lock on as well, so that the shortcut
    works whether Caps Lock is on or not.

    Args:
        window_system: The windowing system that Tk is using.
        keysyms: What Tk calls each of the keys that stand for it.
        shown: What the key is called on the menu entry.

    Returns:
        The shortcut to bind and to show.
    """
    held, name = modifier(window_system)
    sequences = tuple(f'<{held}-{variant}>' for keysym in keysyms
                      for variant in caps_lock_variants(keysym))
    return Shortcut(sequences, f'{name}+{shown}')


def action_shortcuts(window_system: str) -> dict[str, Shortcut]:
    """Return the shortcut of every action that has one, by action."""
    held = {action: held_shortcut(window_system, (keysym,), shown)
            for action, (keysym, shown) in ACTION_KEYS.items()}
    unheld = {action: Shortcut((f'<{keysym}>',), keysym)
              for action, keysym in UNHELD_KEYS.items()}
    return held | unheld


def window_shortcuts(window_system: str) -> Shortcuts:
    """Return the shortcuts of the main window on a windowing system.

    Making a note larger is asked for with a plus, which is typed
    with the shift key held down on most keyboards and is a key of
    its own on the keypad, so every key that stands for it is bound
    and the plainest of them is the one that is shown.
    """
    return Shortcuts(
        quit=quit_shortcut(window_system),
        refresh=held_shortcut(window_system, REFRESH_KEYS, 'R'),
        larger=held_shortcut(window_system, ZOOM_IN_KEYS, '+'),
        smaller=held_shortcut(window_system, ZOOM_OUT_KEYS, '-'),
        normal=held_shortcut(window_system, NORMAL_SIZE_KEYS, '0'),
        actions=action_shortcuts(window_system))
