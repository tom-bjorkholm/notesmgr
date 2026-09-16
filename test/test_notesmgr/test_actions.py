#! /usr/local/bin/python3
"""Tests for what can be done with what is selected."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, \
    DELETE_FOLDER, DUPLICATE, EDIT, MOVE_DOWN, MOVE_UP, NEW, NEW_FOLDER, \
    NOTHING, ON_FOLDER, ON_NOTE, ON_PLAIN, ON_PROJECT, RENAME_FOLDER, \
    Selected, offered

EVERY_ACTION = ON_NOTE + ON_PLAIN + ON_PROJECT + ON_FOLDER
"""Every action that the buttons and the menu entries offer."""


def test_nothing_selected() -> None:
    """With nothing selected there is nothing at all to be done."""
    assert offered(NOTHING) == frozenset()


def test_every_action_named() -> None:
    """Every action belongs to one group, and to one group only."""
    assert len(set(EVERY_ACTION)) == len(EVERY_ACTION)
    assert set(EVERY_ACTION) == {COPY_RAW, COPY_FORMATTED, DUPLICATE, EDIT,
                                 NEW, DELETE, MOVE_UP, MOVE_DOWN, NEW_FOLDER,
                                 RENAME_FOLDER, DELETE_FOLDER}


@pytest.mark.parametrize('selected,expected', [
    (Selected(note=True), set(ON_NOTE)),
    (Selected(note=True, plain=True), set(ON_NOTE) | set(ON_PLAIN)),
    (Selected(project=True), set(ON_PROJECT)),
    (Selected(folder=True), set(ON_FOLDER)),
    (Selected(project=True, folder=True), set(ON_PROJECT) | set(ON_FOLDER)),
    (Selected(note=True, plain=True, project=True), set(ON_NOTE) |
     set(ON_PLAIN) | set(ON_PROJECT))])
def test_offered(selected: Selected, expected: set[str]) -> None:
    """What is selected says which actions can be done with it."""
    assert offered(selected) == expected


def test_template_is_no_plain() -> None:
    """A template is read and copied, but not moved or taken away."""
    labels = offered(Selected(note=True, project=True))
    assert EDIT in labels
    assert DUPLICATE not in labels
    assert DELETE not in labels
    assert MOVE_UP not in labels


def test_everything_at_once() -> None:
    """A note in a folder of an open project allows every action."""
    everything = Selected(note=True, plain=True, project=True, folder=True)
    assert offered(everything) == set(EVERY_ACTION)


def test_new_needs_a_project() -> None:
    """Making a note or a folder asks for a project to make it in."""
    assert NEW not in offered(Selected(note=True, plain=True))
    assert NEW_FOLDER not in offered(Selected(folder=True))
