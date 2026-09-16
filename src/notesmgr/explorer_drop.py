#! /usr/local/bin/python3
"""Where a note or a folder lands when it is dropped in the tree."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import NamedTuple, Optional
from notesmgr.folder_ops import move_folder
from notesmgr.note_ops import move_note
from notesmgr.project import Folder, Project, folder_at


class Drop(NamedTuple):
    """Where a dragged item lands: a folder, and a place in it.

    A note lands at a place among the notes of the folder, counted
    as the notes stand before it is moved. A folder lands in the
    folder itself and at no place in it, because the folders of a
    folder are shown in alphabetical order rather than in an order
    of their own, which is what a place of None says.

    The place is called so rather than an index, because a tuple
    numbers what it holds through a method of that name already.
    """

    folder: Path
    place: Optional[int]


def folder_drop(project: Project, dragged: Path, over: Path) \
        -> Optional[Drop]:
    """Return where a dragged folder lands, None when it cannot land.

    A folder goes into a folder of the project and nowhere else. It
    goes neither into itself nor into a folder of its own, which
    would take it out of the project altogether, and the root folder
    of the project is the project itself and does not move.

    Args:
        project: The project as the tree is showing it.
        dragged: The folder that is being dragged.
        over: The item of the tree that the pointer is over.

    Returns:
        The folder it lands in, None when it lands nowhere.
    """
    target = folder_at(project.tree, over)
    if target is None or dragged == project.tree.path:
        return None
    if target.path == dragged or dragged in target.path.parents:
        return None
    if target.path == dragged.parent:
        return None
    return Drop(target.path, None)


def note_place(project: Project, over: Path,
               lower: bool) -> Optional[tuple[Folder, int]]:
    """Return the folder and the place in it that an item stands for.

    The upper half of a note is the place of that note and the lower
    half the place after it, a folder is the place after its last
    note, and the lower half of a template is the place of the first
    note of its folder. The upper half of a template is above every
    note of the folder, where no note can go.

    Args:
        project: The project as the tree is showing it.
        over: The item of the tree that the pointer is over.
        lower: Whether the pointer is in the lower half of that item.

    Returns:
        The folder the note lands in and the place it lands at, None
        when the item stands for no place at all.
    """
    target = folder_at(project.tree, over)
    if target is not None:
        return (target, len(target.notes))
    holder = folder_at(project.tree, over.parent)
    if holder is None:
        return None
    if over == holder.template:
        return (holder, 0) if lower else None
    if over in holder.notes:
        return (holder, holder.notes.index(over) + int(lower))
    return None


def stays_put(holder: Folder, dragged: Path, index: int) -> bool:
    """Return whether a place is where a note is standing already.

    A note dropped upon itself, and a note dropped where it would
    land between the notes it is already between, has not moved, so
    there is nothing to do and nothing to show either.

    Args:
        holder: The folder that the note would land in.
        dragged: The note that is being dragged.
        index: The place it would land at.

    Returns:
        Whether the note is at that place already.
    """
    if dragged not in holder.notes:
        return False
    was = holder.notes.index(dragged)
    return index in (was, was + 1)


def dragged_note(project: Project, dragged: Path) -> bool:
    """Return whether an item of the tree is a note that can be dragged.

    The tree is asked rather than the name, so that the template of a
    folder, which is no note of the order of that folder, and a row
    that another program has taken away under the tree, are both left
    where they are.

    Args:
        project: The project as the tree is showing it.
        dragged: The item that is being dragged.

    Returns:
        Whether the project holds it as a note of one of its folders.
    """
    holder = folder_at(project.tree, dragged.parent)
    return holder is not None and dragged in holder.notes


def note_drop(project: Project, dragged: Path, over: Path,
              lower: bool) -> Optional[Drop]:
    """Return where a dragged note lands, None when it cannot land.

    Args:
        project: The project as the tree is showing it.
        dragged: The note that is being dragged.
        over: The item of the tree that the pointer is over.
        lower: Whether the pointer is in the lower half of that item.

    Returns:
        The folder and the place it lands at, None for nowhere.
    """
    place = note_place(project, over, lower)
    if place is None:
        return None
    holder, index = place
    if stays_put(holder, dragged, index):
        return None
    return Drop(holder.path, index)


def drop_target(project: Project, dragged: Path, over: Optional[Path],
                lower: bool) -> Optional[Drop]:
    """Return where what is dragged lands, None when it cannot land.

    A note and a folder of the project are dragged, and everything
    else the tree shows stays where it is: every folder has one
    template, and it is no note of the order of that folder.

    Args:
        project: The project as the tree is showing it.
        dragged: The item that is being dragged.
        over: The item of the tree that the pointer is over, None
            when the pointer is over no item of it at all.
        lower: Whether the pointer is in the lower half of that item.

    Returns:
        Where it lands, None when it lands nowhere.
    """
    if over is None:
        return None
    if folder_at(project.tree, dragged) is not None:
        return folder_drop(project, dragged, over)
    if dragged_note(project, dragged):
        return note_drop(project, dragged, over, lower)
    return None


def drop_item(item: Path, drop: Drop) -> Path:
    """Move a note or a folder to where it was dropped.

    Args:
        item: The note or the folder that was dragged.
        drop: Where it was dropped, as the tree worked it out.

    Returns:
        The note or the folder where it now is.

    Raises:
        NotesmgrError: The move cannot be made, which the message of
            the error says why.
    """
    if drop.place is None:
        return move_folder(item, drop.folder)
    return move_note(item, drop.folder, drop.place)
