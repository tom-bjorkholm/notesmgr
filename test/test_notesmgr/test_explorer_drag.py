#! /usr/local/bin/python3
"""Tests for moving what the explorer shows by dragging it."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Union
import pytest
from test_notesmgr.helpers import build_folder_project, refuse_choice
from notesmgr.explorer_drag import DRAG_START, MARK_TAG
from notesmgr.explorer_drop import Drop
from notesmgr.explorer_tree import ExplorerTree
from notesmgr.project import Project
from notesmgr.project_ops import open_project

SHOWN_GEOMETRY = '300x400'
"""How large the window of the drag that is really shown is made."""

ROW = 20
"""How high a row of the tree is in the layout of these tests."""

WIDTH = 200
"""How wide a row of the tree is in the layout of these tests."""

ROOT_ROW = 0
"""The row of the tree that the root folder of the project is at."""

APPLE_ROW = 1
"""The row that the first folder of the project is at."""

A_NOTE_ROW = 3
"""The row that the one note of the first folder is at."""

ZEBRA_ROW = 4
"""The row that the second folder of the project is at."""

TEMPLATE_ROW = 7
"""The row that the template of the root folder is at."""

SECOND_ROW = 8
"""The row that the first note of the root folder is at."""

FIRST_ROW = 9
"""The row that the last note of the root folder is at."""


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Project:
    """Provide an open project holding folders, notes and templates."""
    root = build_folder_project(tmp_path / 'notes')
    return open_project(root, refuse_choice).project


@pytest.fixture(name='dropped')
def fixture_dropped() -> list[tuple[Path, Drop]]:
    """Provide the list that the drags of these tests are reported into."""
    return []


@pytest.fixture(name='explorer')
def fixture_explorer(top_window: tkinter.Toplevel, project: Project,
                     dropped: list[tuple[Path, Drop]]) -> ExplorerTree:
    """Provide an explorer showing the project of these tests."""
    def taken(item: Path, drop: Drop) -> None:
        """Stand in for the window that carries a drop out."""
        dropped.append((item, drop))
    explorer = ExplorerTree(top_window, lambda _path: None, taken)
    explorer.show(project)
    return explorer


@pytest.fixture(name='rows', autouse=True)
def fixture_rows(explorer: ExplorerTree,
                 monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Lay the rows of the tree out, as a window on a screen would.

    A window that is not on a screen has no rows to point at, so what
    Tk answers about the place of a row is answered here instead, one
    row of the same height per item that the tree shows.
    """
    shown = shown_rows(explorer.tree)

    def identify(height: int) -> str:
        """Stand in for Tk saying which row is at a height."""
        index = height // ROW
        return shown[index] if 0 <= index < len(shown) else ''

    def bbox(item: object, _column: object = None) \
            -> Union[tuple[int, int, int, int], str]:
        """Stand in for Tk saying where the row of an item is."""
        if str(item) not in shown:
            return ''
        return (0, shown.index(str(item)) * ROW, WIDTH, ROW)
    monkeypatch.setattr(explorer.tree, 'identify_row', identify)
    monkeypatch.setattr(explorer.tree, 'bbox', bbox)
    return shown


def shown_rows(tree: ttk.Treeview, item: str = '') -> list[str]:
    """Return every item of a tree, in the order it is shown in."""
    rows: list[str] = []
    for child in tree.get_children(item):
        rows.append(str(child))
        rows.extend(shown_rows(tree, str(child)))
    return rows


def event_at(height: int) -> 'tkinter.Event[ttk.Treeview]':
    """Return a Tk event of the pointer at a height in the tree."""
    event: 'tkinter.Event[ttk.Treeview]' = tkinter.Event()
    event.y = height
    return event


def upper(row: int) -> int:
    """Return a height in the upper half of a row of the tree."""
    return row * ROW + 1


def lower(row: int) -> int:
    """Return a height in the lower half of a row of the tree."""
    return row * ROW + ROW - 1


def drag(explorer: ExplorerTree, taken: int, over: int,
         release: bool = True) -> None:
    """Drag the item at one height in the tree to another height."""
    explorer.drag.press(event_at(taken))
    explorer.drag.motion(event_at(over))
    if release:
        explorer.drag.release(event_at(over))


def marked_items(explorer: ExplorerTree) -> list[str]:
    """Return the items of the tree that are marked as a drop target."""
    return [item for item in shown_rows(explorer.tree)
            if MARK_TAG in explorer.tree.item(item, 'tags')]


def line_shown(explorer: ExplorerTree) -> bool:
    """Return whether the line that says where a note lands is drawn."""
    return explorer.drag.mark.line.winfo_manager() == 'place'


def test_drag_a_note_up(explorer: ExplorerTree, project: Project,
                        dropped: list[tuple[Path, Drop]]) -> None:
    """A note dragged above another note lands at that note's place."""
    drag(explorer, upper(FIRST_ROW), upper(SECOND_ROW))
    assert dropped == [(project.root / 'first.md.txt', Drop(project.root, 0))]


def test_drag_below_a_note(explorer: ExplorerTree, project: Project,
                           dropped: list[tuple[Path, Drop]]) -> None:
    """A note dragged below another note lands after that note."""
    drag(explorer, upper(A_NOTE_ROW), lower(SECOND_ROW))
    assert dropped == [(project.root / 'apple' / 'a.md.txt',
                        Drop(project.root, 1))]


def test_drag_onto_a_folder(explorer: ExplorerTree, project: Project,
                            dropped: list[tuple[Path, Drop]]) -> None:
    """A note dragged onto a folder lands after the notes of it."""
    drag(explorer, upper(FIRST_ROW), upper(ZEBRA_ROW))
    assert dropped == [(project.root / 'first.md.txt',
                        Drop(project.root / 'zebra', 1))]


def test_drag_a_folder(explorer: ExplorerTree, project: Project,
                       dropped: list[tuple[Path, Drop]]) -> None:
    """A folder dragged onto another folder lands in it, at no place."""
    drag(explorer, upper(APPLE_ROW), lower(ZEBRA_ROW))
    assert dropped == [(project.root / 'apple',
                        Drop(project.root / 'zebra', None))]


def test_drag_a_template(explorer: ExplorerTree,
                         dropped: list[tuple[Path, Drop]]) -> None:
    """The template of a folder is dragged nowhere at all."""
    drag(explorer, upper(TEMPLATE_ROW), upper(SECOND_ROW))
    assert dropped == []


def test_drag_over_nothing(explorer: ExplorerTree,
                           dropped: list[tuple[Path, Drop]]) -> None:
    """A note dropped below every row of the tree lands nowhere."""
    drag(explorer, upper(FIRST_ROW), upper(FIRST_ROW + 5))
    assert dropped == []
    assert not marked_items(explorer)
    assert not line_shown(explorer)


def test_a_press_is_no_drag(explorer: ExplorerTree,
                            dropped: list[tuple[Path, Drop]]) -> None:
    """Pressing an item without moving is choosing it, and no drag."""
    height = upper(FIRST_ROW)
    drag(explorer, height, height + DRAG_START - 1)
    assert dropped == []
    assert not line_shown(explorer)


def test_a_far_press_drags(explorer: ExplorerTree,
                           dropped: list[tuple[Path, Drop]]) -> None:
    """Moving far enough from where the press was is a drag."""
    drag(explorer, lower(A_NOTE_ROW), lower(A_NOTE_ROW) + DRAG_START)
    assert len(dropped) == 1


def test_escape_gives_up(explorer: ExplorerTree,
                         dropped: list[tuple[Path, Drop]]) -> None:
    """Escape while dragging leaves the project exactly as it was."""
    drag(explorer, upper(FIRST_ROW), upper(SECOND_ROW), release=False)
    explorer.drag.cancelled(event_at(upper(SECOND_ROW)))
    explorer.drag.release(event_at(upper(SECOND_ROW)))
    assert dropped == []
    assert not marked_items(explorer)
    assert not line_shown(explorer)


def test_folder_is_marked(explorer: ExplorerTree, project: Project) -> None:
    """The folder that a drop would land in is marked while dragging."""
    drag(explorer, upper(FIRST_ROW), upper(ZEBRA_ROW), release=False)
    assert marked_items(explorer) == [str(project.root / 'zebra')]
    assert not line_shown(explorer)


def test_line_says_the_place(explorer: ExplorerTree) -> None:
    """A note that lands among notes is shown the line it lands at."""
    drag(explorer, upper(FIRST_ROW), upper(SECOND_ROW), release=False)
    assert line_shown(explorer)
    assert not marked_items(explorer)


@pytest.mark.parametrize('over,drawn', [
    (upper(SECOND_ROW), SECOND_ROW * ROW),
    (lower(SECOND_ROW), (SECOND_ROW + 1) * ROW)])
def test_line_at_the_edge(explorer: ExplorerTree, over: int,
                          drawn: int) -> None:
    """The line is drawn at the edge of the row that is pointed at."""
    drag(explorer, upper(A_NOTE_ROW), over, release=False)
    assert abs(int(explorer.drag.mark.line.place_info()['y']) - drawn) <= 1


def test_marks_are_taken_away(explorer: ExplorerTree) -> None:
    """The marks are gone once the item has been let go of."""
    drag(explorer, upper(FIRST_ROW), upper(ZEBRA_ROW))
    assert not marked_items(explorer)
    assert not line_shown(explorer)


def test_no_project_no_drop(explorer: ExplorerTree,
                            dropped: list[tuple[Path, Drop]]) -> None:
    """With no project shown a drag lands nothing anywhere."""
    explorer.show(None)
    drag(explorer, upper(FIRST_ROW), upper(SECOND_ROW))
    assert dropped == []


def test_drag_where_it_is(explorer: ExplorerTree,
                          dropped: list[tuple[Path, Drop]]) -> None:
    """A note dropped where it stands already is not moved at all."""
    drag(explorer, upper(FIRST_ROW), lower(FIRST_ROW))
    assert dropped == []


def test_drag_from_nowhere(explorer: ExplorerTree,
                           dropped: list[tuple[Path, Drop]]) -> None:
    """A press below every row of the tree takes hold of nothing."""
    drag(explorer, upper(FIRST_ROW + 5), upper(SECOND_ROW))
    assert dropped == []


def test_events_are_bound(explorer: ExplorerTree) -> None:
    """The tree listens for the events that a drag is made of."""
    bound = explorer.tree.bind()
    assert {'<Button-1>', '<B1-Motion>', '<ButtonRelease-1>',
            '<Key-Escape>'} <= set(bound)


@pytest.mark.focus_sensitive
def test_real_drag(explorer: ExplorerTree, project: Project,
                   dropped: list[tuple[Path, Drop]],
                   monkeypatch: pytest.MonkeyPatch) -> None:
    """A drag of the real pointer over a real tree drops the note.

    The rows of a window that is really shown are where Tk says they
    are, so nothing is laid out here, and the drag is driven by the
    events that a mouse would send.
    """
    monkeypatch.undo()
    window = explorer.frame.winfo_toplevel()
    explorer.frame.pack(fill=tkinter.BOTH, expand=True)
    window.geometry(SHOWN_GEOMETRY)
    window.deiconify()
    window.lift()
    window.update()
    tree = explorer.tree
    note = str(project.root / 'first.md.txt')
    box = tree.bbox(note)
    assert box != ''
    over = tree.bbox(str(project.root / 'second.md.txt'))
    assert over != ''
    tree.event_generate('<ButtonPress-1>', x=5, y=box[1] + 2, when='now')
    tree.event_generate('<B1-Motion>', x=5, y=over[1] + 1, when='now')
    tree.event_generate('<ButtonRelease-1>', x=5, y=over[1] + 1, when='now')
    assert dropped == [(project.root / 'first.md.txt', Drop(project.root, 0))]
