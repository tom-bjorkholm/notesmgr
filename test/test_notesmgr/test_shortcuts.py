#! /usr/local/bin/python3
"""Tests for the keyboard shortcuts of the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from notesmgr.actions import COPY_RAW, FOCUS_FOLDER, NEW_FOLDER, ON_NOTE, \
    ON_PLAIN, ON_PROJECT, RENAME, SHOW_ALL
from notesmgr.shortcuts import Shortcut, action_shortcuts, held_shortcut, \
    modifier, quit_shortcut, tk_window_system, window_shortcuts

WINDOW_SYSTEMS = ['aqua', 'win32', 'x11']
"""The windowing systems that Tk runs on."""


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut(('<Command-w>',), 'Cmd+W')),
    ('win32', Shortcut(('<Control-q>',), 'Ctrl+Q')),
    ('x11', Shortcut(('<Control-q>',), 'Ctrl+Q')),
    ('', Shortcut(('<Control-q>',), 'Ctrl+Q'))])
def test_quit_shortcut(window_system: str, expected: Shortcut) -> None:
    """The shortcut is Cmd+W on macOS and Ctrl+Q on other systems."""
    assert quit_shortcut(window_system) == expected


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', ('Command', 'Cmd')),
    ('win32', ('Control', 'Ctrl')),
    ('x11', ('Control', 'Ctrl')),
    ('', ('Control', 'Ctrl'))])
def test_modifier(window_system: str, expected: tuple[str, str]) \
        -> None:
    """The command key holds macOS, and the control key the rest."""
    assert modifier(window_system) == expected


def test_held_shortcut() -> None:
    """A shortcut binds every key that stands for it and shows one."""
    shortcut = held_shortcut('aqua', ('plus', 'KP_Add'), '+')
    assert shortcut == Shortcut(('<Command-plus>', '<Command-KP_Add>'),
                                'Cmd++')


@pytest.mark.parametrize('window_system', ['aqua', 'win32', 'x11'])
def test_zoom_shortcuts(window_system: str) -> None:
    """Every way of asking for another size has keys of its own."""
    keys = window_shortcuts(window_system)
    zooming = (keys.larger, keys.smaller, keys.normal)
    assert all(shortcut.sequences for shortcut in zooming)
    assert len({shortcut.label for shortcut in zooming}) == 3
    bound = [sequence for shortcut in zooming
             for sequence in shortcut.sequences]
    assert len(set(bound)) == len(bound)


def test_window_system_known(top_window: tkinter.Toplevel) -> None:
    """Tk reports one of the three windowing systems that it supports."""
    assert tk_window_system(top_window) in ('aqua', 'win32', 'x11')


@pytest.mark.parametrize('window_system', WINDOW_SYSTEMS)
@pytest.mark.parametrize('action', [*ON_NOTE, *ON_PLAIN, *ON_PROJECT])
def test_actions_have_keys(window_system: str, action: str) -> None:
    """Every action of a note and of the project has a key of its own."""
    assert action in action_shortcuts(window_system)


@pytest.mark.parametrize('window_system', WINDOW_SYSTEMS)
def test_rename_key(window_system: str) -> None:
    """Renaming is F2 alone on every platform, as in file managers."""
    assert action_shortcuts(window_system)[RENAME] == \
        Shortcut(('<F2>',), 'F2')


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut(('<Command-c>',), 'Cmd+C')),
    ('win32', Shortcut(('<Control-c>',), 'Ctrl+C')),
    ('x11', Shortcut(('<Control-c>',), 'Ctrl+C'))])
def test_copy_raw_keys(window_system: str, expected: Shortcut) -> None:
    """Copy raw is the copy key that every platform knows."""
    assert action_shortcuts(window_system)[COPY_RAW] == expected


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut(('<Command-Shift-N>',), 'Cmd+Shift+N')),
    ('x11', Shortcut(('<Control-Shift-N>',), 'Ctrl+Shift+N'))])
def test_shifted_keys(window_system: str, expected: Shortcut) -> None:
    """A capital letter is bound and shown with the shift key held."""
    assert action_shortcuts(window_system)[NEW_FOLDER] == expected


@pytest.mark.parametrize('window_system,action,expected', [
    ('aqua', FOCUS_FOLDER, Shortcut(('<Command-l>',), 'Cmd+L')),
    ('aqua', SHOW_ALL, Shortcut(('<Command-Shift-L>',), 'Cmd+Shift+L')),
    ('win32', FOCUS_FOLDER, Shortcut(('<Control-l>',), 'Ctrl+L')),
    ('win32', SHOW_ALL, Shortcut(('<Control-Shift-L>',), 'Ctrl+Shift+L')),
    ('x11', FOCUS_FOLDER, Shortcut(('<Control-l>',), 'Ctrl+L')),
    ('x11', SHOW_ALL, Shortcut(('<Control-Shift-L>',), 'Ctrl+Shift+L'))])
def test_focus_keys(window_system: str, action: str,
                    expected: Shortcut) -> None:
    """L focuses on the local folder, and with Shift shows the large view."""
    assert action_shortcuts(window_system)[action] == expected


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut(('<Command-r>',), 'Cmd+R')),
    ('win32', Shortcut(('<Control-r>',), 'Ctrl+R')),
    ('x11', Shortcut(('<Control-r>',), 'Ctrl+R'))])
def test_refresh_keys(window_system: str, expected: Shortcut) -> None:
    """Refreshing the project is Cmd+R on macOS and Ctrl+R elsewhere."""
    assert window_shortcuts(window_system).refresh == expected


@pytest.mark.parametrize('window_system', WINDOW_SYSTEMS)
def test_no_key_twice(window_system: str) -> None:
    """No two shortcuts share a key sequence or what they are shown as."""
    keys = window_shortcuts(window_system)
    shortcuts = [keys.quit, keys.refresh, keys.larger, keys.smaller,
                 keys.normal, *keys.actions.values()]
    bound = [sequence for shortcut in shortcuts
             for sequence in shortcut.sequences]
    assert len(set(bound)) == len(bound)
    labels = [shortcut.label for shortcut in shortcuts]
    assert len(set(labels)) == len(labels)


def test_action_keys_valid(top_window: tkinter.Toplevel) -> None:
    """Tk takes every key sequence of an action as one it can bind.

    Tk refuses a sequence that it does not know the keys of, so every
    sequence of the windowing system in use is bound and taken away.
    """
    window_system = tk_window_system(top_window)
    for shortcut in action_shortcuts(window_system).values():
        for sequence in shortcut.sequences:
            top_window.bind(sequence, lambda _event: None)
            top_window.unbind(sequence)
