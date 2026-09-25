#! /usr/local/bin/python3
"""Tests for the tree of a project at the left of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Optional
import pytest
from test_notesmgr.helpers import build_folder_project, refuse_choice
from notesmgr.explorer_drop import Drop
from notesmgr.explorer_tree import EXPLORER_WIDTH, ExplorerTree
from notesmgr.project import Project
from notesmgr.project_ops import open_project


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Project:
    """Provide an open project holding folders, notes and templates."""
    root = build_folder_project(tmp_path / 'notes')
    return open_project(root, refuse_choice).project


@pytest.fixture(name='selected')
def fixture_selected() -> list[Optional[Path]]:
    """Provide the list that the tree reports its selection into."""
    return []


@pytest.fixture(name='dropped')
def fixture_dropped() -> list[tuple[Path, Drop]]:
    """Provide the list that the tree reports its drops into."""
    return []


@pytest.fixture(name='explorer')
def fixture_explorer(top_window: tkinter.Toplevel,
                     selected: list[Optional[Path]],
                     dropped: list[tuple[Path, Drop]]) -> ExplorerTree:
    """Provide an explorer tree in a hidden window, showing nothing yet."""
    def taken(item: Path, drop: Drop) -> None:
        """Stand in for the window that carries a drop out."""
        dropped.append((item, drop))
    return ExplorerTree(top_window, selected.append, taken)


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


def test_select_an_item(explorer: ExplorerTree, project: Project) -> None:
    """An item that the tree shows is selected when it is asked for."""
    explorer.show(project)
    note = project.root / 'first.md.txt'
    assert explorer.select(note) == note
    assert explorer.selected_path() == note


def test_select_moves_focus(explorer: ExplorerTree, project: Project) \
        -> None:
    """The arrow keys carry on from the item that was selected."""
    explorer.show(project)
    note = project.root / 'first.md.txt'
    explorer.select(note)
    assert explorer.tree.focus() == str(note)


def test_select_nothing(explorer: ExplorerTree, project: Project) -> None:
    """Selecting nothing at all leaves nothing selected."""
    explorer.show(project)
    explorer.select(project.root / 'first.md.txt')
    assert explorer.select(None) is None
    assert explorer.selected_path() is None


def test_select_what_is_gone(explorer: ExplorerTree, project: Project) \
        -> None:
    """A path the tree does not show selects nothing, and does not raise."""
    explorer.show(project)
    assert explorer.select(project.root / 'no_such.md.txt') is None
    assert explorer.selected_path() is None


def test_select_a_folder(explorer: ExplorerTree, project: Project) -> None:
    """A folder of the project is selected like any other item."""
    explorer.show(project)
    folder = project.root / 'apple'
    assert explorer.select(folder) == folder


def test_tree_takes_its_style(explorer: ExplorerTree) -> None:
    """The tree is drawn with the style that its own font is in."""
    assert str(explorer.tree.cget('style')) == explorer.font.name


def test_no_project_no_drop(explorer: ExplorerTree, project: Project) -> None:
    """While no project is shown nothing can be dropped anywhere."""
    note = project.root / 'first.md.txt'
    assert explorer.drop_at(note, project.root, False) is None


def test_drop_at_a_place(explorer: ExplorerTree, project: Project) -> None:
    """The tree answers where a dragged note would land in the project."""
    explorer.show(project)
    note = project.root / 'apple' / 'a.md.txt'
    assert explorer.drop_at(note, project.root / 'first.md.txt', True) == \
        Drop(project.root, 2)


def test_drop_at_nowhere(explorer: ExplorerTree, project: Project) -> None:
    """A drag over no item of the tree lands nowhere at all."""
    explorer.show(project)
    note = project.root / 'apple' / 'a.md.txt'
    assert explorer.drop_at(note, None, False) is None


def test_showing_forgets(explorer: ExplorerTree, project: Project) -> None:
    """Showing no project leaves nothing that can be dropped anywhere."""
    explorer.show(project)
    explorer.show(None)
    assert explorer.project is None
    assert explorer.drop_at(project.root / 'first.md.txt', project.root,
                            False) is None


def test_zoom_larger(explorer: ExplorerTree) -> None:
    """The tree is drawn larger, and back in the size it started in."""
    started = explorer.font.size
    explorer.zoom(3)
    assert explorer.font.size == started + 3
    explorer.zoom_normal()
    assert explorer.font.size == started


def test_zoom_smaller(explorer: ExplorerTree) -> None:
    """The tree is drawn smaller as well as larger."""
    started = explorer.font.size
    explorer.zoom(-2)
    assert explorer.font.size == started - 2
