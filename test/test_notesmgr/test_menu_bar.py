#! /usr/local/bin/python3
"""Tests for the menu bar of a notesmgr window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
import pytest
from notesmgr.menu_bar import MenuBar, MenuEntry, MenuSpec, build_menu_bar, \
    entry_labels, entry_state, set_enabled

EDIT_MENU = 'Edit'
"""Title of the second menu that these tests build."""

FILE_MENU = 'File'
"""Title of the first menu that these tests build."""


@pytest.fixture(name='chosen')
def fixture_chosen() -> list[str]:
    """Collect the labels of the entries that were chosen."""
    return []


@pytest.fixture(name='menu_bar')
def fixture_menu_bar(top_window: tkinter.Toplevel,
                     chosen: list[str]) -> MenuBar:
    """Provide a menu bar of two menus on a hidden window."""
    open_entry = MenuEntry('Open', lambda: chosen.append('Open'), 'Ctrl+O')
    quit_entry = MenuEntry('Quit', lambda: chosen.append('Quit'))
    copy_entry = MenuEntry('Copy', lambda: chosen.append('Copy'),
                           enabled=False)
    return build_menu_bar(top_window,
                          [MenuSpec(FILE_MENU, [open_entry, quit_entry]),
                           MenuSpec(EDIT_MENU, [copy_entry])])


@pytest.mark.parametrize('enabled,expected', [(True, 'normal'),
                                              (False, 'disabled')])
def test_entry_state(enabled: bool, expected: str) -> None:
    """An entry that can be chosen is normal and another is disabled."""
    assert entry_state(enabled) == expected


def test_menus_in_order(menu_bar: MenuBar) -> None:
    """The menus are shown in the order they were described in."""
    assert entry_labels(menu_bar.widget) == [FILE_MENU, EDIT_MENU]


def test_menus_by_title(menu_bar: MenuBar) -> None:
    """Every menu that was built is reachable by its own title."""
    assert set(menu_bar.menus) == {FILE_MENU, EDIT_MENU}


def test_entries_in_order(menu_bar: MenuBar) -> None:
    """The entries of a menu are in the order they were described in."""
    assert entry_labels(menu_bar.menus[FILE_MENU]) == ['Open', 'Quit']


def test_installed_on_window(menu_bar: MenuBar,
                             top_window: tkinter.Toplevel) -> None:
    """The window shows the menu bar that was built for it."""
    assert str(top_window.cget('menu')) == str(menu_bar.widget)


def test_accelerator_shown(menu_bar: MenuBar) -> None:
    """An entry that has a shortcut says so, and one without shows none."""
    menu = menu_bar.menus[FILE_MENU]
    assert menu.entrycget('Open', 'accelerator') == 'Ctrl+O'
    assert menu.entrycget('Quit', 'accelerator') == ''


def test_entry_disabled(menu_bar: MenuBar) -> None:
    """An entry described as not choosable is greyed out."""
    assert menu_bar.menus[EDIT_MENU].entrycget('Copy', 'state') == 'disabled'


def test_choosing_an_entry(menu_bar: MenuBar, chosen: list[str]) -> None:
    """Choosing an entry runs the command that was described for it."""
    menu_bar.menus[FILE_MENU].invoke('Open')
    assert chosen == ['Open']


def test_set_enabled(menu_bar: MenuBar, chosen: list[str]) -> None:
    """An entry that was greyed out can be offered again."""
    menu = menu_bar.menus[EDIT_MENU]
    set_enabled(menu, 'Copy', True)
    assert menu.entrycget('Copy', 'state') == 'normal'
    menu.invoke('Copy')
    assert chosen == ['Copy']


def test_set_disabled(menu_bar: MenuBar) -> None:
    """An entry that was offered can be greyed out."""
    menu = menu_bar.menus[FILE_MENU]
    set_enabled(menu, 'Open', False)
    assert menu.entrycget('Open', 'state') == 'disabled'


def test_no_tearoff(menu_bar: MenuBar) -> None:
    """A menu cannot be torn off, as no desktop does that any more."""
    assert not menu_bar.menus[FILE_MENU].cget('tearoff')


def test_labels_of_no_entries(top_window: tkinter.Toplevel) -> None:
    """A menu that holds no entries says nothing at all."""
    assert not entry_labels(tkinter.Menu(top_window, tearoff=False))
