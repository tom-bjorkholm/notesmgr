#! /usr/local/bin/python3
"""Tests for the tree of a project at the left of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Optional
import pytest
from test_notesmgr.helpers import refuse_choice, write_config, write_notes, \
    write_order, write_template
from notesmgr.config import NoteExtension
from notesmgr.explorer_tree import EXPLORER_WIDTH, ExplorerTree
from notesmgr.project import Project
from notesmgr.project_ops import open_project


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Project:
    """Provide an open project holding folders, notes and templates."""
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD_TXT)
    write_template(root, NoteExtension.MD_TXT)
    write_notes(root, ['first.md.txt', 'second.md.txt'])
    write_order(root, ['second.md.txt', 'first.md.txt'])
    write_notes(root / 'zebra', ['z.md.txt'])
    write_notes(root / 'apple', ['a.md.txt'])
    return open_project(root, refuse_choice).project


@pytest.fixture(name='selected')
def fixture_selected() -> list[Optional[Path]]:
    """Provide the list that the tree reports its selection into."""
    return []


@pytest.fixture(name='explorer')
def fixture_explorer(top_window: tkinter.Toplevel,
                     selected: list[Optional[Path]]) -> ExplorerTree:
    """Provide an explorer tree in a hidden window, showing nothing yet."""
    return ExplorerTree(top_window, selected.append)


def items_under(explorer: ExplorerTree, item: str) -> list[str]:
    """Return the names the tree shows under one of its items."""
    return [str(explorer.tree.item(child, 'text'))
            for child in explorer.tree.get_children(item)]


def test_explorer_is_narrow(explorer: ExplorerTree) -> None:
    """The explorer asks for the width the explorer pane is meant to have."""
    assert explorer.frame.winfo_reqwidth() == EXPLORER_WIDTH


def test_empty_at_first(explorer: ExplorerTree) -> None:
    """With no project open the tree shows nothing at all."""
    assert not explorer.tree.get_children('')
    assert explorer.selected_path() is None


def test_root_is_the_top(explorer: ExplorerTree, project: Project) -> None:
    """The root folder of the project is the one item at the top."""
    explorer.show(project)
    assert items_under(explorer, '') == ['notes']


def test_order_of_children(explorer: ExplorerTree, project: Project) -> None:
    """Folders come first, then the template, then the notes in order."""
    explorer.show(project)
    assert items_under(explorer, str(project.root)) == [
        'apple', 'zebra', 'template.md.txt', 'second.md.txt', 'first.md.txt']


def test_folders_hold_notes(explorer: ExplorerTree, project: Project) -> None:
    """A folder of the project holds what that folder holds."""
    explorer.show(project)
    assert items_under(explorer, str(project.root / 'apple')) == [
        'template.md.txt', 'a.md.txt']


def test_items_are_paths(explorer: ExplorerTree, project: Project) -> None:
    """Every item of the tree is known by the path it stands for."""
    explorer.show(project)
    note = project.root / 'first.md.txt'
    assert explorer.tree.exists(str(note))


def test_showing_none(explorer: ExplorerTree, project: Project) -> None:
    """Showing no project empties a tree that showed one."""
    explorer.show(project)
    explorer.show(None)
    assert not explorer.tree.get_children('')


def test_showing_again(explorer: ExplorerTree, project: Project) -> None:
    """A project shown twice is shown once, and not twice over."""
    explorer.show(project)
    explorer.show(project)
    assert items_under(explorer, '') == ['notes']


def test_selection_told(explorer: ExplorerTree, project: Project,
                        selected: list[Optional[Path]]) -> None:
    """Selecting an item tells whoever is listening which path it is."""
    explorer.show(project)
    note = project.root / 'first.md.txt'
    explorer.tree.selection_set(str(note))
    explorer.tree.update()
    assert selected == [note]
    assert explorer.selected_path() == note


def test_one_at_a_time(explorer: ExplorerTree, project: Project) -> None:
    """The explorer lets one item at a time be selected."""
    explorer.show(project)
    assert str(explorer.tree.cget('selectmode')) == 'browse'
