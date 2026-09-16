#! /usr/local/bin/python3
"""Tests for making, renaming and taking away folders."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from test_notesmgr.helpers import TEMPLATE_TEXT, build_project, \
    refuse_choice, write_file, write_notes
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.folder_ops import delete_folder, is_empty, move_folder, \
    new_folder, rename_folder
from notesmgr.order_file import ORDER_NAME, read_order_text
from notesmgr.project_ops import open_project

EXTENSION = NoteExtension.MD_TXT
"""The extension that the notes of these tests carry."""


@pytest.fixture(name='root')
def fixture_root(tmp_path: Path) -> Path:
    """Provide an opened project holding one note and one subfolder."""
    root = build_project(tmp_path / 'notes', ['first.md.txt'])
    write_notes(root / 'full', ['deep.md.txt'])
    open_project(root, refuse_choice)
    return root


@pytest.fixture(name='empty')
def fixture_empty(root: Path) -> Path:
    """Provide a folder holding nothing but notesmgr's own files."""
    return new_folder(root, 'empty', EXTENSION)


def test_new_folder_made(root: Path) -> None:
    """A folder is made where it was asked for, under the name given."""
    made = new_folder(root, 'ideas', EXTENSION)
    assert made == root / 'ideas'
    assert made.is_dir()


def test_new_folder_template(root: Path) -> None:
    """A new folder starts out with the template of the folder above."""
    made = new_folder(root, 'ideas', EXTENSION)
    template = made / 'template.md.txt'
    assert template.read_text(encoding='utf-8') == TEMPLATE_TEXT


def test_new_folder_order(root: Path) -> None:
    """A new folder holds a note order file of its own, holding nothing."""
    made = new_folder(root, 'ideas', EXTENSION)
    assert read_order_text(made) == ''


def test_new_folder_is_clean(root: Path) -> None:
    """A new folder leaves nothing for the next opening to repair."""
    new_folder(root, 'ideas', EXTENSION)
    report = open_project(root, refuse_choice)
    assert not report.created
    assert not report.renamed
    assert not report.problems


@pytest.mark.parametrize('typed', [
    'full', 'FULL', '', '   ', '.hidden', 'a/b', 'first.md.txt',
    'notesmgr.cfg'])
def test_new_folder_refused(root: Path, typed: str) -> None:
    """A name that names no folder that can be made here is refused."""
    with pytest.raises(NotesmgrError):
        new_folder(root, typed, EXTENSION)


def test_rename_folder(root: Path) -> None:
    """A folder that is renamed keeps everything that it holds."""
    renamed = rename_folder(root / 'full', 'renamed')
    assert renamed == root / 'renamed'
    assert (renamed / 'deep.md.txt').is_file()
    assert not (root / 'full').exists()


def test_rename_to_same_name(root: Path) -> None:
    """Renaming a folder to the name it has leaves it as it is."""
    assert rename_folder(root / 'full', 'full') == root / 'full'
    assert (root / 'full' / 'deep.md.txt').is_file()


def test_rename_root_refused(root: Path) -> None:
    """The root folder is the project itself and is not renamed here."""
    with pytest.raises(NotesmgrError):
        rename_folder(root, 'elsewhere')


@pytest.mark.parametrize('typed', ['first.md.txt', '', '.hidden', 'a/b'])
def test_rename_refused(root: Path, typed: str) -> None:
    """A name that is taken or names no folder is refused."""
    with pytest.raises(NotesmgrError):
        rename_folder(root / 'full', typed)


def test_empty_is_empty(empty: Path) -> None:
    """A folder holding only its template and its order file is empty."""
    assert is_empty(empty)


def test_folder_with_note(root: Path) -> None:
    """A folder holding a note is not empty."""
    assert not is_empty(root / 'full')


def test_folder_with_folder(empty: Path) -> None:
    """A folder holding a folder is not empty, however empty that is."""
    (empty / 'below').mkdir()
    assert not is_empty(empty)


def test_folder_with_other(empty: Path) -> None:
    """A folder holding a file that is no note of ours is not empty."""
    write_file(empty / 'picture.png', 'not a note at all')
    assert not is_empty(empty)


def test_delete_folder(empty: Path, trashed: list[Path]) -> None:
    """An empty folder is moved to the trash with what notesmgr put in it."""
    delete_folder(empty)
    assert trashed == [empty]
    assert not empty.exists()


def test_delete_not_empty(root: Path, trashed: list[Path]) -> None:
    """A folder holding notes is not taken away with them."""
    with pytest.raises(NotesmgrError):
        delete_folder(root / 'full')
    assert trashed == []
    assert (root / 'full' / 'deep.md.txt').is_file()


def test_delete_root_refused(root: Path, trashed: list[Path]) -> None:
    """The root folder is the project itself and is not taken away here."""
    with pytest.raises(NotesmgrError):
        delete_folder(root)
    assert trashed == []


def test_order_name_ignored(empty: Path) -> None:
    """The note order file is notesmgr's own and does not fill a folder."""
    assert (empty / ORDER_NAME).is_file()
    assert is_empty(empty)


def test_move_folder(root: Path, empty: Path) -> None:
    """A folder moved into another one keeps everything that it holds."""
    moved = move_folder(root / 'full', empty)
    assert moved == empty / 'full'
    assert (moved / 'deep.md.txt').is_file()
    assert not (root / 'full').exists()


def test_move_folder_is_clean(root: Path, empty: Path) -> None:
    """A folder that was moved leaves nothing for an opening to repair."""
    move_folder(root / 'full', empty)
    report = open_project(root, refuse_choice)
    assert not report.created
    assert not report.renamed
    assert not report.problems


def test_move_folder_stays(root: Path) -> None:
    """A folder moved into the folder it is in already stays as it is."""
    assert move_folder(root / 'full', root) == root / 'full'
    assert (root / 'full' / 'deep.md.txt').is_file()


def test_move_into_itself(root: Path) -> None:
    """A folder is not moved into itself, which would lose it."""
    with pytest.raises(NotesmgrError):
        move_folder(root / 'full', root / 'full')
    assert (root / 'full').is_dir()


def test_move_into_its_own(root: Path) -> None:
    """A folder is not moved into a folder of its own either."""
    below = new_folder(root / 'full', 'below', EXTENSION)
    with pytest.raises(NotesmgrError):
        move_folder(root / 'full', below)
    assert below.is_dir()


def test_move_root_refused(root: Path, empty: Path) -> None:
    """The root folder is the project itself and is not moved here."""
    with pytest.raises(NotesmgrError):
        move_folder(root, empty)
    assert root.is_dir()


def test_move_folder_taken(root: Path, empty: Path) -> None:
    """A folder is not moved where its name is another file's already."""
    write_file(empty / 'full', 'a file that is no folder')
    with pytest.raises(NotesmgrError):
        move_folder(root / 'full', empty)
    assert (root / 'full' / 'deep.md.txt').is_file()
