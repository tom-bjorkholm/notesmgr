#! /usr/local/bin/python3
"""The menu bar of a notesmgr window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Callable, Container, Literal, Mapping, NamedTuple, \
    Optional, Sequence, Union

UNLABELED_TYPES = ('tearoff', 'separator')
"""Types of menu entries that have no label, as they say nothing."""


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
    """The menu bar widget of a window, its menus and popup menus.

    The menus are kept by title so that an entry which only makes
    sense in some states can be greyed out and offered again later.
    A popup menu holds what the menu of the same title holds, to be
    shown wherever the user right-clicks something it acts on.
    """

    widget: tkinter.Menu
    menus: Mapping[str, tkinter.Menu]
    popups: Mapping[str, tkinter.Menu]


def entry_state(enabled: bool) -> Literal['normal', 'disabled']:
    """Return the Tk state of an entry that can or cannot be chosen.

    Args:
        enabled: Whether the entry can be chosen.

    Returns:
        The state that Tk knows that by.
    """
    return 'normal' if enabled else 'disabled'


def entry_menu(parent: tkinter.Misc,
               entries: Sequence[MenuEntry]) -> tkinter.Menu:
    """Create a menu holding the described entries, and nothing else.

    The menu is in no menu bar, so it serves as a menu of the menu
    bar once it is added to one, and as a popup menu as it is.

    Args:
        parent: The widget that the menu belongs to.
        entries: The commands of the menu, in the order they are shown.

    Returns:
        The menu that was made.
    """
    menu = tkinter.Menu(parent, tearoff=False)
    for entry in entries:
        menu.add_command(label=entry.label, command=entry.command,
                         accelerator=entry.accelerator or '',
                         state=entry_state(entry.enabled))
    return menu


def build_menu(menu_bar: tkinter.Menu, spec: MenuSpec) -> tkinter.Menu:
    """Create one described menu and add it to a menu bar.

    Args:
        menu_bar: The menu bar that the menu is added to.
        spec: What the menu is called and what it holds.

    Returns:
        The menu that was made.
    """
    menu = entry_menu(menu_bar, spec.entries)
    menu_bar.add_cascade(label=spec.title, menu=menu)
    return menu


def build_menu_bar(window: Union[tkinter.Tk, tkinter.Toplevel],
                   menus: Sequence[MenuSpec],
                   popups: Container[str] = ()) -> MenuBar:
    """Build the described menus and install them on a window.

    An application says what its menus hold and gets them, instead of
    calling Tk for every entry of every menu.

    Args:
        window: The window that gets the menu bar.
        menus: The menus of the menu bar, in the order they are shown.
        popups: The titles of the menus that are also made as popup
            menus, none by default.

    Returns:
        The menu bar that was made.
    """
    widget = tkinter.Menu(window, tearoff=False)
    built = {spec.title: build_menu(widget, spec) for spec in menus}
    copies = {spec.title: entry_menu(window, spec.entries)
              for spec in menus if spec.title in popups}
    window.configure(menu=widget)
    return MenuBar(widget=widget, menus=built, popups=copies)


def set_enabled(menu: tkinter.Menu, label: str, enabled: bool) -> None:
    """Let one entry of a menu be chosen, or grey it out.

    Args:
        menu: The menu that the entry is in.
        label: Which entry of that menu it is.
        enabled: Whether the entry can now be chosen.
    """
    menu.entryconfigure(label, state=entry_state(enabled))


def entry_labels(menu: tkinter.Menu) -> list[str]:
    """Return what the entries of a menu say, in the order they are in.

    Tearoff entries and separators say nothing, so they are left out.

    Args:
        menu: The menu to look through.

    Returns:
        The labels of the entries that have a label, in menu order, or
        an empty list when no entry has one.
    """
    last = menu.index(tkinter.END)
    if last is None:
        return []
    return [str(menu.entrycget(index, 'label')) for index in range(last + 1)
            if menu.type(index) not in UNLABELED_TYPES]
