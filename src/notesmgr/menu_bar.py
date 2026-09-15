#! /usr/local/bin/python3
"""The menu bar of a notesmgr window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Callable, Literal, Mapping, NamedTuple, Optional, \
    Sequence, Union


class MenuEntry(NamedTuple):
    """One command of a menu, and whether it can be chosen."""

    label: str
    command: Callable[[], None]
    accelerator: Optional[str] = None
    enabled: bool = True


class MenuSpec(NamedTuple):
    """One menu of a menu bar and the commands it holds."""

    title: str
    entries: Sequence[MenuEntry]


class MenuBar(NamedTuple):
    """The menu bar widget of a window and its menus by title.

    The menus are kept by title so that an entry which only makes
    sense in some states can be greyed out and offered again later.
    """

    widget: tkinter.Menu
    menus: Mapping[str, tkinter.Menu]


def entry_state(enabled: bool) -> Literal['normal', 'disabled']:
    """Return the Tk state of an entry that can or cannot be chosen.

    Args:
        enabled: Whether the entry can be chosen.

    Returns:
        The state that Tk knows that by.
    """
    return 'normal' if enabled else 'disabled'


def build_menu(menu_bar: tkinter.Menu, spec: MenuSpec) -> tkinter.Menu:
    """Create one described menu and add it to a menu bar.

    Args:
        menu_bar: The menu bar that the menu is added to.
        spec: What the menu is called and what it holds.

    Returns:
        The menu that was made.
    """
    menu = tkinter.Menu(menu_bar, tearoff=False)
    for entry in spec.entries:
        menu.add_command(label=entry.label, command=entry.command,
                         accelerator=entry.accelerator or '',
                         state=entry_state(entry.enabled))
    menu_bar.add_cascade(label=spec.title, menu=menu)
    return menu


def build_menu_bar(window: Union[tkinter.Tk, tkinter.Toplevel],
                   menus: Sequence[MenuSpec]) -> MenuBar:
    """Build the described menus and install them on a window.

    An application says what its menus hold and gets them, instead of
    calling Tk for every entry of every menu.

    Args:
        window: The window that gets the menu bar.
        menus: The menus of the menu bar, in the order they are shown.

    Returns:
        The menu bar that was made.
    """
    widget = tkinter.Menu(window)
    built = {spec.title: build_menu(widget, spec) for spec in menus}
    window.configure(menu=widget)
    return MenuBar(widget=widget, menus=built)


def set_enabled(menu: tkinter.Menu, label: str, enabled: bool) -> None:
    """Let one entry of a menu be chosen, or grey it out.

    Args:
        menu: The menu that the entry is in.
        label: Which entry of that menu it is.
        enabled: Whether the entry can now be chosen.
    """
    menu.entryconfigure(label, state=entry_state(enabled))
