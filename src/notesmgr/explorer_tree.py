#! /usr/local/bin/python3
"""The tree of a project, shown at the left of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Callable, Optional
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
                 on_select: Callable[[Optional[Path]], None]) -> None:
        """Build the tree in a frame of its own inside a parent widget.

        Args:
            parent: The widget that the explorer is placed in.
            on_select: Told which item is selected, whenever that
                changes, and told None when nothing is selected.
        """
        self.on_select = on_select
        self.frame = ttk.Frame(parent, width=EXPLORER_WIDTH)
        self.frame.pack_propagate(False)
        self.tree = ttk.Treeview(self.frame, show='tree', selectmode='browse')
        self.scroll = ttk.Scrollbar(self.frame, orient=tkinter.VERTICAL,
                                    command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.tree.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)
        self.tree.bind(SELECT_EVENT, self.selection_changed)

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

    def show(self, project: Optional[Project]) -> None:
        """Show a project, or nothing at all when there is none."""
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
