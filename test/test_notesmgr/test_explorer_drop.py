#! /usr/local/bin/python3
"""Tests for where a dragged item lands when it is dropped."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from test_notesmgr.helpers import build_project, refuse_choice, write_notes
from notesmgr.errors import NotesmgrError
from notesmgr.explorer_drop import Drop, drop_item, drop_target
from notesmgr.order_file import read_order_text
from notesmgr.project import Project
from notesmgr.project_ops import open_project

NOTES = ['first.md.txt', 'second.md.txt', 'third.md.txt']
"""The notes of the root folder of these tests, in their order."""

DEEP = 'deep.md.txt'
"""The one note that the subfolder of these tests holds."""

TEMPLATE = 'template.md.txt'
"""What the template of every folder of these tests is called."""


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Project:
    """Provide a project of three notes, a subfolder and a folder in it."""
    root = build_project(tmp_path / 'notes', NOTES)
    write_notes(root / 'sub', [DEEP])
    write_notes(root / 'sub' / 'below', ['low.md.txt'])
    return open_project(root, refuse_choice).project


def order_of(folder: Path) -> list[str]:
    """Return the notes that the order file of a folder lists."""
    text = read_order_text(folder)
    return [] if text is None else text.splitlines()


@pytest.mark.parametrize('over,lower,expected', [
    (NOTES[0], False, 0), (NOTES[0], True, 1), (NOTES[1], False, 1),
    (NOTES[2], True, 3), (TEMPLATE, True, 0)])
def test_note_lands_at(project: Project, over: str, lower: bool,
                       expected: int) -> None:
    """A note lands above or below the row the pointer is over."""
    root = project.root
    dropped = drop_target(project, root / 'sub' / DEEP, root / over, lower)
    assert dropped == Drop(root, expected)


def test_note_over_template(project: Project) -> None:
    """Above the template of a folder there is no place for a note."""
    root = project.root
    assert drop_target(project, root / 'sub' / DEEP, root / TEMPLATE,
                       False) is None


def test_note_on_a_folder(project: Project) -> None:
    """A note dropped on a folder lands after the notes of that folder."""
    root = project.root
    dropped = drop_target(project, root / 'sub' / DEEP, root, True)
    assert dropped == Drop(root, len(NOTES))


@pytest.mark.parametrize('over,lower', [
    (NOTES[1], False), (NOTES[1], True), (NOTES[0], True),
    (NOTES[2], False)])
def test_note_stays_put(project: Project, over: str, lower: bool) -> None:
    """A note dropped where it is already has nowhere to land."""
    root = project.root
    assert drop_target(project, root / NOTES[1], root / over, lower) is None


def test_note_over_nothing(project: Project) -> None:
    """A note dropped on no item of the tree lands nowhere at all."""
    assert drop_target(project, project.root / NOTES[0], None, False) is None


def test_template_not_dragged(project: Project) -> None:
    """The template of a folder is no note and is not dragged anywhere."""
    root = project.root
    assert drop_target(project, root / TEMPLATE, root / 'sub', False) \
        is None


def test_folder_into_folder(project: Project) -> None:
    """A folder dropped on another folder lands in it, at no place."""
    root = project.root
    dropped = drop_target(project, root / 'sub' / 'below', root, False)
    assert dropped == Drop(root, None)


@pytest.mark.parametrize('over', [NOTES[0], TEMPLATE])
def test_folder_onto_a_note(project: Project, over: str) -> None:
    """A folder is dropped on a folder and on nothing else."""
    root = project.root
    assert drop_target(project, root / 'sub', root / over, False) is None


@pytest.mark.parametrize('over', ['sub', 'sub/below'])
def test_folder_into_its_own(project: Project, over: str) -> None:
    """A folder goes neither into itself nor into a folder of its own."""
    root = project.root
    assert drop_target(project, root / 'sub', root / over, False) is None


def test_folder_where_it_is(project: Project) -> None:
    """A folder dropped in the folder it is in already does not move."""
    root = project.root
    assert drop_target(project, root / 'sub', root, False) is None


def test_root_not_dragged(project: Project) -> None:
    """The root folder is the project itself and is dragged nowhere."""
    root = project.root
    assert drop_target(project, root, root / 'sub', False) is None


@pytest.mark.parametrize('dragged', ['gone.md.txt', 'sub/gone.md.txt',
                                     'nowhere/deep.md.txt'])
def test_unknown_not_dragged(project: Project, dragged: str) -> None:
    """What the tree does not show is dragged nowhere either."""
    root = project.root
    assert drop_target(project, root / dragged, root, False) is None


def test_drop_item_note(project: Project) -> None:
    """Dropping a note moves it to the place that the drop names."""
    root = project.root
    moved = drop_item(root / NOTES[2], Drop(root / 'sub', 0))
    assert moved == root / 'sub' / NOTES[2]
    assert order_of(root / 'sub') == [NOTES[2], DEEP]
    assert order_of(root) == [NOTES[0], NOTES[1]]


def test_drop_item_folder(project: Project) -> None:
    """Dropping a folder moves it into the folder that the drop names."""
    root = project.root
    moved = drop_item(root / 'sub' / 'below', Drop(root, None))
    assert moved == root / 'below'
    assert (moved / 'low.md.txt').is_file()


def test_drop_item_refused(project: Project) -> None:
    """A drop that the file system will not take is reported as an error."""
    root = project.root
    write_notes(root / 'sub', [NOTES[0]])
    with pytest.raises(NotesmgrError):
        drop_item(root / NOTES[0], Drop(root / 'sub', 0))


def test_drag_and_drop(project: Project) -> None:
    """A note dragged to another folder is in that folder afterwards."""
    root = project.root
    note = root / 'sub' / DEEP
    dropped = drop_target(project, note, root / NOTES[0], False)
    assert dropped is not None
    assert drop_item(note, dropped) == root / DEEP
    assert order_of(root) == [DEEP] + NOTES
    assert order_of(root / 'sub') == []


def test_drag_drop_folder(project: Project) -> None:
    """A folder dragged onto a folder is in that folder afterwards."""
    root = project.root
    folder = root / 'sub' / 'below'
    dropped = drop_target(project, folder, root, False)
    assert dropped is not None
    assert drop_item(folder, dropped) == root / 'below'
    assert (root / 'below' / 'low.md.txt').is_file()
