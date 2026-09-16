#! /usr/local/bin/python3
"""Moving the notes and the folders of the tree by dragging them."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Callable, NamedTuple, Optional
from notesmgr.explorer_drop import Drop

PRESS_EVENT = '<ButtonPress-1>'
"""Tk event of the mouse button going down, which may begin a drag."""

MOTION_EVENT = '<B1-Motion>'
"""Tk event of the pointer moving with the mouse button held down."""

RELEASE_EVENT = '<ButtonRelease-1>'
"""Tk event of the mouse button going up, dropping what is dragged."""

CANCEL_EVENT = '<Escape>'
"""Tk event of the key that gives up a drag that is going on."""

DRAG_START = 5
"""Pixels the pointer moves before a press is taken for a drag.

A press that moves no further than this is the user choosing an item
of the tree rather than taking hold of it, so nothing is marked and
nothing is moved when the button goes up again.
"""

MARK_TAG = 'drop_mark'
"""Name of the tag that marks the folder a drop would land in."""

MARK_COLOUR = '#3a7bd5'
"""Colour of the marks that say where a drop lands, a strong blue."""

MARK_TEXT_COLOUR = '#ffffff'
"""Colour of the name of a marked folder, which the mark is behind."""

LINE_HEIGHT = 2
"""How thick the line that says where a note lands is, in pixels."""


class Dragging(NamedTuple):
    """What is being dragged now, and where it would land.

    Nothing is being dragged while the item is None, which is how a
    drag that was given up and a drag that has not begun are told
    from one that is going on.
    """

    item: Optional[Path] = None
    drop: Optional[Drop] = None
    origin: int = 0
    started: bool = False


def row_at(tree: ttk.Treeview, height: int) -> Optional[Path]:
    """Return the item of a tree at a height, None for no item there."""
    item = tree.identify_row(height)
    return Path(item) if item else None


def row_box(tree: ttk.Treeview,
            item: Path) -> Optional[tuple[int, int, int, int]]:
    """Return where the row of an item is, None when it is nowhere.

    A row that is scrolled out of sight has no place in the tree, and
    neither has any row of a window that is not on the screen, which
    is what the None is for.
    """
    box = tree.bbox(str(item))
    return None if not box else box


def lower_half(tree: ttk.Treeview, over: Optional[Path], height: int) \
        -> bool:
    """Return whether a height is in the lower half of an item's row."""
    box = None if over is None else row_box(tree, over)
    return box is not None and height >= box[1] + box[3] / 2


class DropMark:
    """What the tree shows of where a drop would land.

    A drop into a folder is shown by marking that folder, and a drop
    among the notes of a folder by a line at the edge of a row, which
    is where the note would go.
    """

    def __init__(self, tree: ttk.Treeview) -> None:
        """Get ready to mark a tree, marking nothing yet."""
        self.tree = tree
        self.marked: Optional[str] = None
        self.line = tkinter.Frame(tree, height=LINE_HEIGHT,
                                  background=MARK_COLOUR)
        tree.tag_configure(MARK_TAG, background=MARK_COLOUR,
                           foreground=MARK_TEXT_COLOUR)

    def at_folder(self, folder: Path) -> None:
        """Mark the folder that what is dragged would be put into."""
        self.clear()
        self.marked = str(folder)
        self.tree.item(self.marked, tags=(MARK_TAG,))

    def at_edge(self, over: Path, lower: bool) -> None:
        """Draw the line at an edge of a row, which a note lands at."""
        self.clear()
        box = row_box(self.tree, over)
        if box is None:
            return
        edge = box[1] + box[3] if lower else box[1]
        self.line.place(x=0, y=edge - LINE_HEIGHT // 2, relwidth=1)

    def clear(self) -> None:
        """Take away the marks that said where a drop would land."""
        if self.marked is not None and self.tree.exists(self.marked):
            self.tree.item(self.marked, tags=())
        self.marked = None
        self.line.place_forget()


class ExplorerDrag:
    """Lets what the tree shows be moved by dragging it.

    The view supplies nothing but coordinates: which item the pointer
    is over, and whether it is in the lower half of that item. Where
    that lands the dragged item is answered elsewhere, and this shows
    the answer and asks for it to be carried out when the button
    goes up.

    A drop that lands nowhere is no drop at all, so a release over an
    item that nothing can be dropped on, and Escape while dragging,
    leave the project exactly as it was.
    """

    def __init__(self, tree: ttk.Treeview,
                 target: Callable[[Path, Optional[Path], bool],
                                  Optional[Drop]],
                 dropped: Callable[[Path, Drop], None]) -> None:
        """Let the items of a tree be dragged from now on.

        Args:
            tree: The tree whose items are dragged.
            target: Asked where a dragged item would land, given the
                item, what the pointer is over, and whether it is in
                the lower half of that item.
            dropped: Told what was dragged and where it was dropped.
        """
        self.tree = tree
        self.target = target
        self.dropped = dropped
        self.mark = DropMark(tree)
        self.state = Dragging()
        tree.bind(PRESS_EVENT, self.press)
        tree.bind(MOTION_EVENT, self.motion)
        tree.bind(RELEASE_EVENT, self.release)
        tree.bind(CANCEL_EVENT, self.cancelled)

    def press(self, event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Take hold of the item that the mouse button went down on."""
        self.cancel()
        self.state = Dragging(item=row_at(self.tree, event.y), origin=event.y)

    def motion(self, event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Show where what is being dragged would land now."""
        item = self.state.item
        if item is None or not self.dragging(event.y):
            return
        over = row_at(self.tree, event.y)
        lower = lower_half(self.tree, over, event.y)
        self.state = self.state._replace(drop=self.target(item, over, lower))
        self.show(over, lower)

    def release(self, _event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Move what was dragged to where it was dropped."""
        item, drop = self.state.item, self.state.drop
        self.cancel()
        if item is not None and drop is not None:
            self.dropped(item, drop)

    def cancelled(self, _event: 'tkinter.Event[ttk.Treeview]') -> None:
        """Give up the drag, leaving the project exactly as it was."""
        self.cancel()

    def cancel(self) -> None:
        """Forget what was dragged, and unmark where it would land."""
        self.mark.clear()
        self.state = Dragging()

    def dragging(self, height: int) -> bool:
        """Return whether the press has become a drag by now.

        Args:
            height: Where the pointer is in the tree.

        Returns:
            Whether the pointer has moved far enough from where the
            button went down, which it goes on having done for the
            rest of the drag.
        """
        if not self.state.started and \
                abs(height - self.state.origin) >= DRAG_START:
            self.state = self.state._replace(started=True)
        return self.state.started

    def show(self, over: Optional[Path], lower: bool) -> None:
        """Mark where what is dragged would land, or mark nothing.

        Args:
            over: The item of the tree that the pointer is over.
            lower: Whether the pointer is in the lower half of it.
        """
        drop = self.state.drop
        if drop is None or over is None:
            self.mark.clear()
        elif drop.folder == over:
            self.mark.at_folder(over)
        else:
            self.mark.at_edge(over, lower)
