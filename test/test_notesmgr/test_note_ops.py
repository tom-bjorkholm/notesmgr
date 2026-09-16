#! /usr/local/bin/python3
"""Tests for making, copying, moving and taking away notes."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from test_notesmgr.helpers import TEMPLATE_TEXT, build_project, \
    refuse_choice, write_config, write_file, write_notes, write_template
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_ops import delete_note, duplicate_note, free_path, \
    moved_order, moved_to, move_note, new_note, new_path, resync_order, \
    shift_note, template_text
from notesmgr.order_file import order_text, read_order_text
from notesmgr.project_ops import open_project

NOTES = ['first.md.txt', 'second.md.txt', 'third.md.txt']
"""The notes that the project of these tests holds, in their order."""

EXTENSION = NoteExtension.MD_TXT
"""The extension that the notes of these tests carry."""


@pytest.fixture(name='root')
def fixture_root(tmp_path: Path) -> Path:
    """Provide an opened project of three notes and a subfolder."""
    root = build_project(tmp_path / 'notes', NOTES)
    write_notes(root / 'sub', ['other.md.txt'])
    open_project(root, refuse_choice)
    return root


def order_of(folder: Path) -> list[str]:
    """Return the notes that the order file of a folder lists."""
    text = read_order_text(folder)
    return [] if text is None else text.splitlines()


def test_new_note_written(root: Path) -> None:
    """A new note holds what the template of its folder holds."""
    made = new_note(root, 'fourth', EXTENSION)
    assert made == root / 'fourth.md.txt'
    assert made.read_text(encoding='utf-8') == TEMPLATE_TEXT


def test_new_note_ordered(root: Path) -> None:
    """A new note is put last in the order of its folder."""
    new_note(root, 'fourth', EXTENSION)
    assert order_of(root) == NOTES + ['fourth.md.txt']


def test_new_note_below(root: Path) -> None:
    """A note is made in whichever folder of the project is asked for."""
    made = new_note(root / 'sub', 'another', EXTENSION)
    assert made.parent == root / 'sub'
    assert order_of(root / 'sub') == ['other.md.txt', 'another.md.txt']


def test_new_note_empty_tmpl(root: Path) -> None:
    """A folder whose template holds nothing makes an empty note."""
    write_template(root, EXTENSION, '')
    made = new_note(root, 'fourth', EXTENSION)
    assert made.read_text(encoding='utf-8') == ''


def test_new_note_no_template(tmp_path: Path) -> None:
    """A folder holding no template at all still makes the note."""
    folder = tmp_path / 'bare'
    folder.mkdir()
    assert new_note(folder, 'note', EXTENSION).is_file()


@pytest.mark.parametrize('typed', [
    'first', 'first.md.txt', 'FIRST', 'First.MD.TXT', 'template', '', '  ',
    '.hidden', 'sub/deep', 'note.md', 'template.md.txt'])
def test_new_note_refused(root: Path, typed: str) -> None:
    """A name that names no note that can be made here is refused."""
    with pytest.raises(NotesmgrError):
        new_note(root, typed, EXTENSION)


def test_refused_not_written(root: Path) -> None:
    """A name that is refused leaves the folder exactly as it was."""
    with pytest.raises(NotesmgrError):
        new_note(root, 'first', EXTENSION)
    assert order_of(root) == NOTES


def test_new_path_extension(root: Path) -> None:
    """A name is given the extension that the project is configured with."""
    assert new_path(root, 'fourth', NoteExtension.MD) == root / 'fourth.md'


def test_free_path_taken(root: Path) -> None:
    """A name that any file of the folder has, case and all, is taken."""
    with pytest.raises(NotesmgrError):
        free_path(root, 'notesmgr.cfg')
    with pytest.raises(NotesmgrError):
        free_path(root, '.NOTES_ORDER.TXT')


def test_template_text(root: Path) -> None:
    """The template of a folder is what a new note starts out as."""
    assert template_text(root, EXTENSION) == TEMPLATE_TEXT


def test_template_not_text(root: Path) -> None:
    """A template that is no text is read as nothing at all."""
    (root / 'template.md.txt').write_bytes(b'not \xff\xfe text\n')
    assert template_text(root, EXTENSION) == ''


def test_duplicate_copies(root: Path) -> None:
    """A copy of a note holds what the note holds, under its own name."""
    made = duplicate_note(root / NOTES[0], root, 'copied', EXTENSION)
    assert made == root / 'copied.md.txt'
    assert made.read_text(encoding='utf-8') == \
        (root / NOTES[0]).read_text(encoding='utf-8')
    assert order_of(root) == NOTES + ['copied.md.txt']


def test_duplicate_elsewhere(root: Path) -> None:
    """A note is copied into any folder of the project, not only its own."""
    made = duplicate_note(root / NOTES[0], root / 'sub', 'copied', EXTENSION)
    assert made == root / 'sub' / 'copied.md.txt'
    assert order_of(root) == NOTES
    assert order_of(root / 'sub') == ['other.md.txt', 'copied.md.txt']


def test_duplicate_refused(root: Path) -> None:
    """A copy under a name that is taken is refused, not written over."""
    with pytest.raises(NotesmgrError):
        duplicate_note(root / NOTES[0], root, 'second', EXTENSION)
    assert (root / NOTES[1]).read_text(encoding='utf-8') != \
        (root / NOTES[0]).read_text(encoding='utf-8')


def test_delete_trashes(root: Path, trashed: list[Path]) -> None:
    """A note that is taken away goes to the trash and out of the order."""
    delete_note(root / NOTES[1])
    assert trashed == [root / NOTES[1]]
    assert order_of(root) == [NOTES[0], NOTES[2]]


def test_delete_last_note(tmp_path: Path, trashed: list[Path]) -> None:
    """Taking away the only note of a folder leaves an empty order."""
    root = tmp_path / 'notes'
    write_config(root, EXTENSION)
    write_notes(root, ['only.md.txt'])
    open_project(root, refuse_choice)
    delete_note(root / 'only.md.txt')
    assert trashed == [root / 'only.md.txt']
    assert order_of(root) == []


def test_delete_what_is_gone(root: Path, trashed: list[Path]) -> None:
    """A note that another program took away cannot be trashed twice."""
    (root / NOTES[0]).unlink()
    with pytest.raises(NotesmgrError):
        delete_note(root / NOTES[0])
    assert trashed == []


@pytest.mark.parametrize('name,offset,expected', [
    ('b', -1, ['b', 'a', 'c']),
    ('b', 1, ['a', 'c', 'b']),
    ('a', -1, ['a', 'b', 'c']),
    ('c', 1, ['a', 'b', 'c']),
    ('a', 1, ['b', 'a', 'c']),
    ('c', -1, ['a', 'c', 'b']),
    ('gone', -1, ['a', 'b', 'c']),
    ('a', -5, ['a', 'b', 'c']),
    ('a', 5, ['b', 'c', 'a'])])
def test_moved_order(name: str, offset: int, expected: list[str]) -> None:
    """A note moves by so many places, and stops at the ends."""
    assert moved_order(['a', 'b', 'c'], name, offset) == expected


@pytest.mark.parametrize('names', [[], ['only']])
def test_moved_order_short(names: list[str]) -> None:
    """A folder of one note or none has nothing to move anywhere."""
    assert moved_order(names, 'only', -1) == names


def test_shift_note_up(root: Path) -> None:
    """A note moved up changes places with the note above it."""
    shift_note(root / NOTES[2], -1)
    assert order_of(root) == [NOTES[0], NOTES[2], NOTES[1]]


def test_shift_note_down(root: Path) -> None:
    """A note moved down changes places with the note below it."""
    shift_note(root / NOTES[0], 1)
    assert order_of(root) == [NOTES[1], NOTES[0], NOTES[2]]


def test_shift_at_the_end(root: Path) -> None:
    """A note at the end of its folder stays where it is."""
    shift_note(root / NOTES[0], -1)
    assert order_of(root) == NOTES


def test_shift_gives_the_note(root: Path) -> None:
    """Moving a note gives back the note, which is what stays selected."""
    assert shift_note(root / NOTES[0], 1) == root / NOTES[0]


def test_resync_adds_drops(root: Path) -> None:
    """The order takes up a note that is new and drops one that is gone."""
    write_file(root / 'added.md.txt', 'added by another program\n')
    (root / NOTES[0]).unlink()
    assert resync_order(root) == [NOTES[1], NOTES[2], 'added.md.txt']
    assert read_order_text(root) == \
        order_text([NOTES[1], NOTES[2], 'added.md.txt'])


@pytest.mark.parametrize('name,index,expected', [
    ('a', 0, ['a', 'b', 'c']), ('a', 1, ['a', 'b', 'c']),
    ('a', 2, ['b', 'a', 'c']), ('a', 3, ['b', 'c', 'a']),
    ('c', 0, ['c', 'a', 'b']), ('c', 1, ['a', 'c', 'b']),
    ('c', 2, ['a', 'b', 'c']), ('c', 3, ['a', 'b', 'c']),
    ('b', 0, ['b', 'a', 'c']), ('b', 3, ['a', 'c', 'b']),
    ('a', -2, ['a', 'b', 'c']), ('a', 9, ['b', 'c', 'a']),
    ('d', 0, ['a', 'b', 'c'])])
def test_moved_to(name: str, index: int, expected: list[str]) -> None:
    """A note lands at the place it is put, counted as the notes stand."""
    assert moved_to(['a', 'b', 'c'], name, index) == expected


@pytest.mark.parametrize('names', [[], ['only']])
def test_moved_to_short(names: list[str]) -> None:
    """A folder of one note or none has nothing to put anywhere else."""
    assert moved_to(names, 'only', 0) == names


@pytest.mark.parametrize('index,expected', [
    (0, [NOTES[2], NOTES[0], NOTES[1]]), (1, [NOTES[0], NOTES[2], NOTES[1]]),
    (3, NOTES)])
def test_move_in_folder(root: Path, index: int, expected: list[str]) \
        -> None:
    """A note put at a place in its own folder is shown there."""
    assert move_note(root / NOTES[2], root, index) == root / NOTES[2]
    assert order_of(root) == expected


def test_move_to_folder(root: Path) -> None:
    """A note moved to another folder is the file that is there now."""
    moved = move_note(root / NOTES[0], root / 'sub', 0)
    assert moved == root / 'sub' / NOTES[0]
    assert moved.is_file()
    assert not (root / NOTES[0]).exists()


def test_move_orders_both(root: Path) -> None:
    """A note moved away leaves one order and is put into the other."""
    move_note(root / NOTES[0], root / 'sub', 0)
    assert order_of(root) == [NOTES[1], NOTES[2]]
    assert order_of(root / 'sub') == [NOTES[0], 'other.md.txt']


def test_move_to_the_end(root: Path) -> None:
    """A note dropped below the last note of a folder comes last."""
    move_note(root / NOTES[0], root / 'sub', 1)
    assert order_of(root / 'sub') == ['other.md.txt', NOTES[0]]


def test_move_name_taken(root: Path) -> None:
    """A note is not moved into a folder that holds that name already."""
    write_notes(root / 'sub', [NOTES[0]])
    with pytest.raises(NotesmgrError):
        move_note(root / NOTES[0], root / 'sub', 0)
    assert (root / NOTES[0]).is_file()
    assert order_of(root) == NOTES


def test_move_keeps_content(root: Path) -> None:
    """A note moved to another folder holds what it held before."""
    held = (root / NOTES[0]).read_text(encoding='utf-8')
    moved = move_note(root / NOTES[0], root / 'sub', 0)
    assert moved.read_text(encoding='utf-8') == held
