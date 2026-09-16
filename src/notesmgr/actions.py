#! /usr/local/bin/python3
"""What can be done with what is selected, and when it can be done."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import NamedTuple

COPY_RAW = 'Copy raw'
"""What the action that copies the note as it is written is called."""

COPY_FORMATTED = 'Copy formatted'
"""What the action that copies the note formatted is called."""

DUPLICATE = 'Duplicate'
"""What the action that copies the note into the project is called."""

EDIT = 'Edit'
"""What the action that opens the note in an editor is called."""

NEW = 'New'
"""What the action that makes another note is called."""

DELETE = 'Delete'
"""What the action that takes the note away is called."""

MOVE_UP = 'Up'
"""What the action that moves the note one place up is called."""

MOVE_DOWN = 'Down'
"""What the action that moves the note one place down is called."""

NEW_FOLDER = 'New folder…'
"""What the action that makes another folder is called."""

RENAME_FOLDER = 'Rename folder…'
"""What the action that gives a folder another name is called."""

DELETE_FOLDER = 'Delete folder'
"""What the action that takes an empty folder away is called."""

ON_NOTE = (COPY_RAW, COPY_FORMATTED, EDIT)
"""What can be done with any note that is shown, template or not."""

ON_PLAIN = (DUPLICATE, DELETE, MOVE_UP, MOVE_DOWN)
"""What can be done with a note that is no template of a folder."""

ON_PROJECT = (NEW, NEW_FOLDER)
"""What can be done as long as there is a project to do it in."""

ON_FOLDER = (RENAME_FOLDER, DELETE_FOLDER)
"""What can be done with a folder that is no root of a project."""


class Selected(NamedTuple):
    """What is selected, as far as it says what can be done with it.

    The panel knows whether there is a note to act on, because a note
    can be taken away by another program while it is shown, and the
    rest follows from the item that the explorer has selected.
    """

    note: bool = False
    plain: bool = False
    project: bool = False
    folder: bool = False


NOTHING = Selected()
"""What is selected while nothing at all is."""


def offered(selected: Selected) -> frozenset[str]:
    """Return what can be done with what is selected.

    Args:
        selected: What the explorer has selected now.

    Returns:
        The actions that the buttons and the menu entries offer,
        every other action of the application being greyed out.
    """
    groups = ((selected.note, ON_NOTE), (selected.plain, ON_PLAIN),
              (selected.project, ON_PROJECT), (selected.folder, ON_FOLDER))
    return frozenset(action for allowed, group in groups if allowed
                     for action in group)
