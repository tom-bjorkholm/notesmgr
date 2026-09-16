#! /usr/local/bin/python3
"""Tests for the names that the files of a project carry."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
import pytest
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.note_file import NOTE_EXTENSIONS, checked_extension, \
    checked_name, is_markdown, is_note, is_plain_note, is_template, \
    note_extension, note_file_name, note_stem, sorted_names, template_name


def test_longest_first() -> None:
    """The extensions are tried longest first, so .md.txt wins over .txt."""
    assert NOTE_EXTENSIONS[0] == NoteExtension.MD_TXT
    assert set(NOTE_EXTENSIONS) == set(NoteExtension)


@pytest.mark.parametrize('name,expected', [
    ('note.md.txt', NoteExtension.MD_TXT),
    ('note.md', NoteExtension.MD),
    ('note.txt', NoteExtension.TXT),
    ('note.MD.TXT', NoteExtension.MD_TXT),
    ('NOTE.Md', NoteExtension.MD),
    ('a.b.md.txt', NoteExtension.MD_TXT),
    ('note.markdown', None),
    ('note', None),
    ('notesmgr.cfg', None),
    ('.notes_order.txt', None),
    ('.md.txt', None),
    ('.txt', None),
    ('.md', None),
    ('', None),
    ('.notes_order.txt.new', None)])
def test_note_extension(name: str, expected: Optional[NoteExtension]) -> None:
    """A file name carries the longest note extension it ends with."""
    assert note_extension(name) == expected
    assert is_note(name) == (expected is not None)


@pytest.mark.parametrize('name,expected', [
    ('note.md.txt', True),
    ('note.md', True),
    ('note.MD', True),
    ('note.Md.Txt', True),
    ('template.md.txt', True),
    ('note.txt', False),
    ('note.TXT', False),
    ('note.markdown', False),
    ('note', False),
    ('notesmgr.cfg', False),
    ('.notes_order.txt', False),
    ('', False)])
def test_is_markdown(name: str, expected: bool) -> None:
    """A note is written in markdown when its own name says so."""
    assert is_markdown(name) == expected


@pytest.mark.parametrize('name,expected', [
    ('note.md.txt', 'note'),
    ('note.md', 'note'),
    ('a.b.md.txt', 'a.b'),
    ('note.markdown', 'note.markdown'),
    ('notesmgr.cfg', 'notesmgr.cfg')])
def test_note_stem(name: str, expected: str) -> None:
    """The stem of a name is what is left when its extension is gone."""
    assert note_stem(name) == expected


@pytest.mark.parametrize('extension,expected', [
    (NoteExtension.MD, 'template.md'),
    (NoteExtension.TXT, 'template.txt'),
    (NoteExtension.MD_TXT, 'template.md.txt')])
def test_template_name(extension: NoteExtension, expected: str) -> None:
    """A template is called template with the extension of the project."""
    assert template_name(extension) == expected


@pytest.mark.parametrize('name,expected', [
    ('template.md.txt', True),
    ('template.md', True),
    ('template.txt', True),
    ('Template.MD', True),
    ('template', False),
    ('template.markdown', False),
    ('templates.md', False),
    ('my template.md', False),
    ('.template.md', False)])
def test_is_template(name: str, expected: bool) -> None:
    """A template is a note whose name, but for its extension, says so."""
    assert is_template(name) == expected
    assert is_plain_note(name) == (is_note(name) and not expected)


@pytest.mark.parametrize('names,expected', [
    ([], []),
    (['b.md', 'a.md'], ['a.md', 'b.md']),
    (['Zebra.md', 'apple.md'], ['apple.md', 'Zebra.md']),
    (['a.md', 'A.md'], ['A.md', 'a.md']),
    (['10.md', '2.md'], ['10.md', '2.md'])])
def test_sorted_names(names: list[str], expected: list[str]) -> None:
    """Names are ordered alphabetically, and by case only after that."""
    assert sorted_names(names) == expected


@pytest.mark.parametrize('typed,expected', [
    ('note', 'note.md.txt'),
    ('  note  ', 'note.md.txt'),
    ('note.md.txt', 'note.md.txt'),
    ('note.MD.TXT', 'note.MD.TXT'),
    ('my note', 'my note.md.txt'),
    ('a.b', 'a.b.md.txt'),
    ('note.markdown', 'note.markdown.md.txt')])
def test_note_file_name(typed: str, expected: str) -> None:
    """A typed name becomes a file name with the project's extension."""
    assert note_file_name(typed, NoteExtension.MD_TXT) == expected


@pytest.mark.parametrize('typed', [
    '', '   ', '\t\n', 'a/b', 'a\\b', '/', '.', '..', '.hidden',
    '.hidden.md.txt', 'note.md', 'note.txt', 'template.md.txt',
    'Template.MD.TXT', 'template'])
def test_refused_names(typed: str) -> None:
    """A name that names no note of this project is refused, not fixed."""
    with pytest.raises(NotesmgrError):
        note_file_name(typed, NoteExtension.MD_TXT)


@pytest.mark.parametrize('extension,typed,expected', [
    (NoteExtension.MD, 'note', 'note.md'),
    (NoteExtension.MD, 'note.md', 'note.md'),
    (NoteExtension.TXT, 'note', 'note.txt'),
    (NoteExtension.TXT, 'note.md.txt', None),
    (NoteExtension.MD, 'note.md.txt', None),
    (NoteExtension.MD_TXT, 'note.md', None)])
def test_checked_extension(extension: NoteExtension, typed: str,
                           expected: Optional[str]) -> None:
    """A name carrying another project's extension is refused."""
    if expected is None:
        with pytest.raises(NotesmgrError):
            checked_extension(typed, extension)
    else:
        assert checked_extension(typed, extension) == expected


@pytest.mark.parametrize('typed,expected', [
    ('ideas', 'ideas'),
    ('  ideas  ', 'ideas'),
    ('my ideas', 'my ideas'),
    ('notes.md', 'notes.md')])
def test_checked_name(typed: str, expected: str) -> None:
    """A name is what was typed, with the blanks around it taken off."""
    assert checked_name(typed) == expected


@pytest.mark.parametrize('typed', [
    '', '   ', '\t\n', 'a/b', 'a\\b', '/', '.', '..', '.hidden'])
def test_refused_plain_names(typed: str) -> None:
    """A name that names nothing that can be made in a folder is refused."""
    with pytest.raises(NotesmgrError):
        checked_name(typed)
