#! /usr/local/bin/python3
"""Tests for what a notesmgr project is and what its folders hold."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import stat
from pathlib import Path
import pytest
from test_notesmgr.helpers import refuse_choice, write_config, write_file, \
    write_notes, write_template
from notesmgr.config import NoteExtension
from notesmgr.errors import NotesmgrError
from notesmgr.project import PROJECT_CONFIG, config_path, folder_content, \
    folder_entries, folder_paths, is_project, is_shown_folder, read_config
from notesmgr.project_ops import open_project


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide the root folder of a project holding a little of all."""
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD)
    write_notes(root, ['b.md', 'a.md', 'read me.txt'])
    write_template(root, NoteExtension.MD)
    write_file(root / '.hidden.md', 'not shown')
    write_file(root / 'notes.cfg', 'no note')
    write_file(root / 'sub' / 'c.md')
    write_file(root / '.git' / 'config')
    return root


def test_config_path(tmp_path: Path) -> None:
    """The configuration of a project is a file in its root folder."""
    assert config_path(tmp_path) == tmp_path / PROJECT_CONFIG


def test_is_project(project: Path, tmp_path: Path) -> None:
    """A folder is a project when it holds a configuration file."""
    assert is_project(project)
    assert not is_project(tmp_path)
    assert not is_project(project / 'sub')


def test_read_config(project: Path) -> None:
    """The configuration of a project is the one in its root folder."""
    config = read_config(project)
    assert config.file_extension is NoteExtension.MD
    assert config.editor == 'vi'


def test_read_no_project(tmp_path: Path) -> None:
    """A folder that holds no configuration file is no project."""
    with pytest.raises(NotesmgrError):
        read_config(tmp_path)


def test_read_broken_config(tmp_path: Path) -> None:
    """A configuration file that is no JSON is reported, not raised."""
    write_file(config_path(tmp_path), 'this is not JSON at all')
    with pytest.raises(NotesmgrError):
        read_config(tmp_path)


def test_read_wrong_value(tmp_path: Path) -> None:
    """A configuration naming no known extension is reported."""
    write_file(config_path(tmp_path),
               '{"editor": "vi", "file_extension": "RTF"}')
    with pytest.raises(NotesmgrError):
        read_config(tmp_path)


def test_folders_shown(project: Path) -> None:
    """The folders of a project are shown, but the hidden ones are not."""
    content = folder_content(project)
    assert [path.name for path in content.folders] == ['sub']


def test_notes_are_found(project: Path) -> None:
    """Every note is found, whatever of the three extensions it has."""
    content = folder_content(project)
    assert sorted(content.notes) == ['a.md', 'b.md', 'read me.txt']


def test_template_is_apart(project: Path) -> None:
    """The template of a folder is no note of the folder."""
    content = folder_content(project)
    assert [path.name for path in content.templates] == ['template.md']
    assert 'template.md' not in content.notes


def test_several_templates(project: Path) -> None:
    """A folder holding several templates says so, and settles nothing."""
    write_template(project, NoteExtension.TXT)
    content = folder_content(project)
    assert [path.name for path in content.templates] == ['template.md',
                                                         'template.txt']


def test_order_file_hidden(project: Path) -> None:
    """The files that notesmgr keeps for itself are no notes."""
    write_file(project / '.notes_order.txt', 'a.md\n')
    content = folder_content(project)
    assert 'notesmgr.cfg' not in content.notes
    assert '.notes_order.txt' not in content.notes
    assert '.hidden.md' not in content.notes


def test_content_sorted(project: Path) -> None:
    """What a folder holds comes back in alphabetical order."""
    write_notes(project, ['Zebra.md', 'apple.md'])
    content = folder_content(project)
    assert content.notes[:2] == ['a.md', 'apple.md']
    assert content.notes[-1] == 'Zebra.md'


def test_unreadable_folder(tmp_path: Path) -> None:
    """A folder that is not there at all is reported, not raised."""
    with pytest.raises(NotesmgrError):
        folder_content(tmp_path / 'no_such')


@pytest.mark.skipif(os.name == 'nt', reason='file modes differ on Windows')
def test_folder_not_listable(tmp_path: Path) -> None:
    """A folder that may not be listed is reported, not guessed at."""
    closed = tmp_path / 'closed'
    closed.mkdir()
    closed.chmod(stat.S_IWUSR)
    try:
        with pytest.raises(NotesmgrError):
            folder_content(closed)
    finally:
        closed.chmod(stat.S_IRWXU)


@pytest.mark.skipif(os.name == 'nt', reason='links need rights on Windows')
def test_linked_folder_left(project: Path) -> None:
    """A folder reached through a link is left out, so no link loops."""
    (project / 'loop').symlink_to(project, target_is_directory=True)
    assert not is_shown_folder(project / 'loop')
    assert [path.name for path in folder_content(project).folders] == ['sub']


def test_folder_entries(project: Path) -> None:
    """Everything a folder holds is there, hidden files and all."""
    names = [path.name for path in folder_entries(project)]
    assert '.hidden.md' in names
    assert 'notes.cfg' in names
    assert names == sorted(names, key=str.casefold)


def test_folder_paths(project: Path) -> None:
    """A project names its root folder and every folder below it."""
    tree = open_project(project, refuse_choice).project.tree
    assert folder_paths(tree) == [project, project / 'sub']
