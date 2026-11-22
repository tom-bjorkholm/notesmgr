#! /usr/local/bin/python3
"""Tests of the Help menu entries that show the user guide."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import NamedTuple, Sequence, Union
import pytest
from notesmgr import main_window as window_module
from notesmgr.errors import NotesmgrError
from notesmgr.main_window import GUIDE_ENTRY, GUIDE_TITLE, HELP_MENU, \
    SHORTCUTS_ENTRY, SHORTCUTS_TITLE, VERSION_ENTRY, MainWindow
from notesmgr.menu_bar import entry_labels
from notesmgr.note_blocks import Block
from notesmgr.user_guide import NO_GUIDE, guide_blocks, readme_text, \
    shortcut_blocks


class Shown(NamedTuple):
    """What the main window asked to have shown formatted, or said."""

    title: str
    content: Union[tuple[Block, ...], str]


@pytest.fixture(name='shown')
def fixture_shown(monkeypatch: pytest.MonkeyPatch) -> list[Shown]:
    """Record the formatted texts and the errors the window showed."""
    shown: list[Shown] = []

    def formatted(_parent: object, title: str,
                  blocks: Sequence[Block]) -> None:
        """Stand in for showing a formatted text in a window."""
        shown.append(Shown(title, tuple(blocks)))

    def error(_parent: object, title: str, message: str) -> None:
        """Stand in for reporting an error to the user."""
        shown.append(Shown(title, message))
    monkeypatch.setattr(window_module, 'show_formatted', formatted)
    monkeypatch.setattr(window_module, 'show_error', error)
    return shown


def test_help_entries(main_window: MainWindow) -> None:
    """The guide comes first in the Help menu, and versions last."""
    labels = entry_labels(main_window.menu_bar.menus[HELP_MENU])
    assert labels == [GUIDE_ENTRY, SHORTCUTS_ENTRY, VERSION_ENTRY]


def test_guide_shown(main_window: MainWindow, shown: list[Shown]) -> None:
    """Choosing the user guide shows the whole guide formatted."""
    main_window.menu_bar.menus[HELP_MENU].invoke(GUIDE_ENTRY)
    assert shown == [Shown(GUIDE_TITLE, guide_blocks(readme_text()))]


def test_shortcuts_shown(main_window: MainWindow, shown: list[Shown]) \
        -> None:
    """Choosing the keyboard shortcuts shows only that section."""
    main_window.menu_bar.menus[HELP_MENU].invoke(SHORTCUTS_ENTRY)
    assert shown == [Shown(SHORTCUTS_TITLE, shortcut_blocks(readme_text()))]


@pytest.mark.parametrize('label,title', [(GUIDE_ENTRY, GUIDE_TITLE),
                                         (SHORTCUTS_ENTRY, SHORTCUTS_TITLE)])
def test_guide_missing(main_window: MainWindow, shown: list[Shown],
                       monkeypatch: pytest.MonkeyPatch, label: str,
                       title: str) -> None:
    """A guide that cannot be found is said, and nothing is shown."""
    def missing() -> str:
        """Stand in for a notesmgr that is not installed."""
        raise NotesmgrError(NO_GUIDE)
    monkeypatch.setattr(window_module, 'readme_text', missing)
    main_window.menu_bar.menus[HELP_MENU].invoke(label)
    assert shown == [Shown(title, NO_GUIDE)]


@pytest.mark.focus_sensitive
def test_guide_main_size(shown_window: MainWindow) -> None:
    """The user guide opens as large as the main window it is shown over."""
    window = shown_window.window
    window.update()
    shown_window.menu_bar.menus[HELP_MENU].invoke(GUIDE_ENTRY)
    guides = [child for child in window.winfo_children()
              if isinstance(child, tkinter.Toplevel)]
    assert len(guides) == 1
    guides[0].update()
    assert (guides[0].winfo_width(), guides[0].winfo_height()) == \
        (window.winfo_width(), window.winfo_height())
    guides[0].destroy()


@pytest.mark.focus_sensitive
def test_table_uses_width(shown_window: MainWindow) -> None:
    """The shortcuts are laid out to the width of the shown window.

    Before it is on the screen the window lays its tables out to the
    80 letters that its area asks for, so a table wider than that
    shows that it was laid out again once the window was shown.
    """
    window = shown_window.window
    window.update()
    shown_window.menu_bar.menus[HELP_MENU].invoke(SHORTCUTS_ENTRY)
    shortcuts = [child for child in window.winfo_children()
                 if isinstance(child, tkinter.Toplevel)][0]
    shortcuts.update()
    areas = [grandchild for child in shortcuts.winfo_children()
             for grandchild in child.winfo_children()
             if isinstance(grandchild, tkinter.Text)]
    rules = [line for line in str(areas[0].get('1.0', 'end')).split('\n')
             if '┼' in line]
    assert len(rules[0]) > 80
    shortcuts.destroy()
