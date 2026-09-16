#! /usr/local/bin/python3
"""The tree of a project, shown at the left of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Callable, Optional
from notesmgr.explorer_drag import ExplorerDrag
from notesmgr.explorer_drop import Drop, drop_target
from notesmgr.explorer_font import TreeFont
from notesmgr.project import Folder, Project

EXPLORER_WIDTH = 260
"""Width in pixels that the explorer asks the main window for."""

SELECT_EVENT = '<<TreeviewSelect>>'
"""Tk event saying that another item of the tree is selected now."""


class ExplorerTree:
    """Shows the folders, templates and notes of a project as a tree.

    Every item of the tree is known by the path of the file or folder
    it stands for, so that what the user selected is a path, and the
    view keeps nothing of its own beside the tree itself.
    """

    def __init__(self, parent: tkinter.Misc,
                 on_select: Callable[[Optional[Path]], None],
                 on_drop: Callable[[Path, Drop], None]) -> None:
        """Build the tree in a frame of its own inside a parent widget.

        Args:
            parent: The widget that the explorer is placed in.
            on_select: Told which item is selected, whenever that
                changes, and told None when nothing is selected.
            on_drop: Told what was dragged in the tree and where it
                was dropped, once the user has let go of it.
        """
        self.on_select = on_select
        self.project: Optional[Project] = None
        self.frame = ttk.Frame(parent, width=EXPLORER_WIDTH)
        self.frame.pack_propagate(False)
        self.font = TreeFont(self.frame)
        self.tree = ttk.Treeview(self.frame, show='tree', selectmode='browse',
                                 style=self.font.name)
        self.scroll = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL,
                                    command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.tree.bind(SELECT_EVENT, self.selection_changed)
        self.drag = ExplorerDrag(self.tree, self.drop_at, on_drop)

    def selection_changed(self, _event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Tell whoever is listening what is selected now."""
        self.on_select(self.selected_path())

    def selected_path(self) -> Optional[Path]:
        """Return what the user selected, None when nothing is."""
        selection = self.tree.selection()
        return Path(selection[0]) if selection else None

    def select(self, path: Optional[Path]) -> Optional[Path]:
        """Select one item of the tree, or nothing at all.

        Args:
            path: What is to be selected, None for nothing at all.
                A path that the tree does not show selects nothing
                either, which is what a note that was taken away or
                renamed by another program leaves behind.

        Returns:
            What is selected now, None when nothing is.
        """
        if path is None or not self.tree.exists(str(path)):
            self.tree.selection_set(())
            return None
        self.tree.selection_set(str(path))
        self.tree.see(str(path))
        return path

    def drop_at(self, dragged: Path, over: Optional[Path],
                lower: bool) -> Optional[Drop]:
        """Return where a dragged item would land, None for nowhere.

        Args:
            dragged: The item that is being dragged.
            over: The item of the tree that the pointer is over,
                None when it is over no item at all.
            lower: Whether the pointer is in the lower half of it.

        Returns:
            Where the item lands, None when it lands nowhere, which
            is what every drag does while no project is open.
        """
        if self.project is None:
            return None
        return drop_target(self.project, dragged, over, lower)

    def zoom(self, step: int) -> None:
        """Draw the tree so many steps larger, or smaller below zero."""
        self.font.zoom(step)

    def zoom_normal(self) -> None:
        """Draw the tree in the size that it started out in."""
        self.font.normal_size()

    def show(self, project: Optional[Project]) -> None:
        """Show a project, or nothing at all when there is none."""
        self.drag.cancel()
        self.project = project
        self.tree.delete(*self.tree.get_children())
        if project is not None:
            self.add_folder(project.tree, '')

    def add_folder(self, folder: Folder, parent: str) -> None:
        """Add one folder of the project and everything below it.

        The subfolders come first, then the template of the folder,
        and after them the notes in the order the note order file
        gives them.

        Args:
            folder: The folder of the project to add.
            parent: Item the folder is added under, empty for the top.
        """
        item = self.tree.insert(parent, tkinter.END, iid=str(folder.path),
                                text=folder.path.name or str(folder.path),
                                open=True)
        for below in folder.folders:
            self.add_folder(below, item)
        for path in self.shown_files(folder):
            self.tree.insert(item, tkinter.END, iid=str(path), text=path.name)

    @staticmethod
    def shown_files(folder: Folder) -> list[Path]:
        """Return the template and the notes of a folder, in that order."""
        template = [] if folder.template is None else [folder.template]
        return template + list(folder.notes)
