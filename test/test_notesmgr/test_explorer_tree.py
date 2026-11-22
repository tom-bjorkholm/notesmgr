#! /usr/local/bin/python3
"""Tests for the tree of a project at the left of the main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Optional
import pytest
from test_notesmgr.helpers import build_folder_project, refuse_choice
from test_notesmgr.tk_windows import event_at, show_filled
from notesmgr import explorer_tree as tree_module
from notesmgr.explorer_drop import Drop
from notesmgr.explorer_tree import AQUA_RIGHT_CLICKS, EXPLORER_WIDTH, \
    RIGHT_CLICKS, SELECT_EVENT, ExplorerTree, context_clicks
from notesmgr.project import Project
from notesmgr.project_ops import open_project
from notesmgr.shortcuts import tk_window_system


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


@pytest.fixture(name='clicked')
def fixture_clicked() -> list[tuple[Path, int, int]]:
    """Provide the list that the tree reports its right-clicks into."""
    return []


@pytest.fixture(name='explorer')
def fixture_explorer(top_window: tkinter.Toplevel,
                     selected: list[Optional[Path]],
                     dropped: list[tuple[Path, Drop]],
                     clicked: list[tuple[Path, int, int]]) -> ExplorerTree:
    """Provide an explorer tree in a hidden window, showing nothing yet."""
    def taken(item: Path, drop: Drop) -> None:
        """Stand in for the window that carries a drop out."""
        dropped.append((item, drop))

    def context(item: Path, x_root: int, y_root: int) -> None:
        """Stand in for the window that shows the menu of an item."""
        clicked.append((item, x_root, y_root))
    return ExplorerTree(top_window, selected.append, taken, context)


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
    """Selecting an item tells whoever is listening which path it is.

    Tk only tells a widget of a window that is shown of a selection,
    so the handler that the tree binds is called here. That Tk calls
    it is tested in a window that is really shown, by
    test_tk_tells_selection.
    """
    explorer.show(project)
    note = project.root / 'first.md.txt'
    explorer.tree.selection_set(str(note))
    explorer.selection_changed(tkinter.Event())
    assert selected == [note]
    assert explorer.selected_path() == note


def test_selection_watched(explorer: ExplorerTree) -> None:
    """The tree listens for Tk telling it of a new selection."""
    assert SELECT_EVENT in explorer.tree.bind()


@pytest.mark.focus_sensitive
def test_tk_tells_selection(explorer: ExplorerTree, project: Project,
                            selected: list[Optional[Path]]) -> None:
    """Tk itself tells of a selection made in a window that is shown."""
    explorer.show(project)
    show_filled(explorer.frame)
    note = project.root / 'first.md.txt'
    explorer.tree.selection_set(str(note))
    explorer.tree.update()
    assert selected == [note]


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


@pytest.mark.parametrize('asked,expected', [
    ('first.md.txt', 'first.md.txt'),
    ('apple', 'apple'),
    ('apple/gone.md.txt', 'apple'),
    ('apple/gone/deeper.md.txt', 'apple'),
    ('gone/z.md.txt', '')])
def test_nearest_shown(explorer: ExplorerTree, project: Project, asked: str,
                       expected: str) -> None:
    """A path is itself when shown, or else the nearest folder above it.

    An empty expected path stands for the root folder of the project.
    """
    explorer.show(project)
    assert explorer.nearest_shown(project.root / asked) == \
        project.root / expected


@pytest.mark.parametrize('outside', [True, False])
def test_nearest_none(explorer: ExplorerTree, project: Project,
                      outside: bool) -> None:
    """No path, and a path outside the project, have nothing near."""
    explorer.show(project)
    asked = project.root.parent / 'elsewhere.md.txt' if outside else None
    assert explorer.nearest_shown(asked) is None


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


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', AQUA_RIGHT_CLICKS), ('win32', RIGHT_CLICKS),
    ('x11', RIGHT_CLICKS)])
def test_context_clicks(window_system: str, expected: tuple[str, ...]) \
        -> None:
    """Each windowing system has its own events of a right-click."""
    assert context_clicks(window_system) == expected


def test_right_click_bound(explorer: ExplorerTree) -> None:
    """The tree listens for every right-click of its windowing system."""
    bound = explorer.tree.bind()
    for sequence in context_clicks(tk_window_system(explorer.tree)):
        assert sequence in bound


@pytest.mark.parametrize('hit', [True, False])
def test_right_click(explorer: ExplorerTree, project: Project,
                     clicked: list[tuple[Path, int, int]],
                     monkeypatch: pytest.MonkeyPatch, hit: bool) -> None:
    """A right-click on an item asks for its menu, elsewhere for none.

    A window that is not on a screen has no rows to click, so which
    row is at the height clicked is answered here. That Tk calls the
    handler is tested in a window that is really shown, by
    test_tk_right_click.
    """
    explorer.show(project)
    note = project.root / 'first.md.txt'
    monkeypatch.setattr(tree_module, 'row_at', lambda _tree, _height:
                        note if hit else None)
    assert explorer.context_click(event_at(5, 10, 20)) == 'break'
    assert clicked == ([(note, 10, 20)] if hit else [])


@pytest.mark.focus_sensitive
@pytest.mark.parametrize('sequence', sorted(set(AQUA_RIGHT_CLICKS)
                                            | set(RIGHT_CLICKS)))
def test_tk_right_click(explorer: ExplorerTree, project: Project,
                        clicked: list[tuple[Path, int, int]],
                        sequence: str) -> None:
    """Tk itself tells of a right-click in a window that is shown.

    A click with the control key held down is a right-click on macOS,
    so it neither begins a drag nor selects what was clicked, which a
    click of the tree itself would do.
    """
    if sequence not in context_clicks(tk_window_system(explorer.tree)):
        pytest.skip(f'{sequence} is no right-click on this system')
    explorer.show(project)
    show_filled(explorer.frame)
    note = project.root / 'first.md.txt'
    box = explorer.tree.bbox(str(note))
    assert box
    explorer.tree.event_generate(sequence, x=box[0] + 5, y=box[1] + 2,
                                 when='now')
    assert [item for item, _x, _y in clicked] == [note]
    assert explorer.drag.state.item is None
    assert explorer.selected_path() is None
