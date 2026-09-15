#! /usr/local/bin/python3
"""Tests for opening a folder of notes as a notesmgr project."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import stat
from pathlib import Path
from typing import Sequence
import pytest
from test_notesmgr.helpers import first_choice, refuse_choice, write_config, \
    write_file, write_notes, write_order, write_template
from notesmgr import project_ops
from notesmgr.config import NoteExtension
from notesmgr.config_files import CONFIG_NAME
from notesmgr.errors import NotesmgrError
from notesmgr.order_file import ORDER_NAME, order_text, read_order_text
from notesmgr.project import Folder, config_path, read_config
from notesmgr.project_ops import CREATED_HEAD, RENAMED_HEAD, changed_message, \
    create_project, open_project

USER_CONFIG = '{"editor": "nano", "file_extension": "MD"}'
"""A user wide configuration that a new project is to start out as."""


@pytest.fixture(name='trashed')
def fixture_trashed(monkeypatch: pytest.MonkeyPatch) -> list[Path]:
    """Record what was trashed, and remove it without a real trash.

    The tests may not fill the trash of whoever runs them, so what
    notesmgr asks to have trashed is taken away here instead.
    """
    gone: list[Path] = []

    def record(path: Path) -> None:
        """Stand in for moving a file to the trash of the platform."""
        gone.append(path)
        path.unlink()
    monkeypatch.setattr(project_ops, 'send2trash', record)
    return gone


@pytest.fixture(name='root')
def fixture_root(tmp_path: Path) -> Path:
    """Provide a folder of notes that is not a project yet."""
    root = tmp_path / 'notes'
    write_notes(root, ['b.md.txt', 'a.md.txt'])
    write_notes(root / 'sub', ['c.md.txt'])
    return root


@pytest.fixture(name='project')
def fixture_project(root: Path) -> Path:
    """Provide a project whose notes carry the default extension."""
    write_config(root, NoteExtension.MD_TXT)
    return root


def names_of(folder: Folder) -> list[str]:
    """Return the names of the notes of a folder, in shown order."""
    return [path.name for path in folder.notes]


def test_create_writes_config(root: Path, home: Path) -> None:
    """A new project starts out as a copy of the user wide configuration."""
    (home / CONFIG_NAME).write_text(USER_CONFIG, encoding='utf-8')
    report = create_project(root, refuse_choice)
    assert config_path(root).is_file()
    assert report.project.config.editor == 'nano'
    assert read_config(root).file_extension is NoteExtension.MD


def test_create_uses_defaults(root: Path) -> None:
    """With no user wide configuration, the built-in defaults are used."""
    report = create_project(root, refuse_choice)
    assert report.project.config.file_extension is NoteExtension.MD_TXT


def test_create_adopts_notes(root: Path) -> None:
    """The notes a folder holds already become the notes of the project."""
    report = create_project(root, refuse_choice)
    assert names_of(report.project.tree) == ['a.md.txt', 'b.md.txt']
    assert read_order_text(root) == order_text(['a.md.txt', 'b.md.txt'])


def test_create_reaches_down(root: Path) -> None:
    """Every folder of a new project gets its own note order file."""
    report = create_project(root, refuse_choice)
    below = report.project.tree.folders
    assert [folder.path.name for folder in below] == ['sub']
    assert names_of(below[0]) == ['c.md.txt']
    assert read_order_text(root / 'sub') == order_text(['c.md.txt'])


def test_create_on_project(project: Path) -> None:
    """A folder that is a project already is not made into one twice."""
    with pytest.raises(NotesmgrError):
        create_project(project, refuse_choice)


def test_create_needs_folder(tmp_path: Path) -> None:
    """A folder that is not there cannot be made into a project."""
    with pytest.raises(NotesmgrError):
        create_project(tmp_path / 'no_such', refuse_choice)


def test_open_needs_project(root: Path) -> None:
    """A folder holding no configuration file cannot be opened."""
    with pytest.raises(NotesmgrError):
        open_project(root, refuse_choice)


def test_open_keeps_order(project: Path) -> None:
    """The order file of a project says in which order its notes come."""
    write_order(project, ['b.md.txt', 'a.md.txt'])
    report = open_project(project, refuse_choice)
    assert names_of(report.project.tree) == ['b.md.txt', 'a.md.txt']
    assert not report.problems


def test_open_repairs_order(project: Path) -> None:
    """A note that is gone is dropped and a new one is listed last."""
    write_order(project, ['gone.md.txt', 'b.md.txt'])
    report = open_project(project, refuse_choice)
    assert names_of(report.project.tree) == ['b.md.txt', 'a.md.txt']


def test_root_template_empty(project: Path) -> None:
    """The root folder of a project gets a template that is empty."""
    report = open_project(project, refuse_choice)
    template = report.project.tree.template
    assert template is not None
    assert template.name == 'template.md.txt'
    assert template.read_text(encoding='utf-8') == ''
    assert list(report.created) == [template,
                                    project / 'sub' / 'template.md.txt']


def test_subfolder_template(project: Path) -> None:
    """A folder below the root gets a copy of the template above it."""
    write_template(project, NoteExtension.MD_TXT, 'Written above.\n')
    report = open_project(project, refuse_choice)
    below = report.project.tree.folders[0].template
    assert below is not None
    assert below.read_text(encoding='utf-8') == 'Written above.\n'
    assert list(report.created) == [below]


def test_template_kept_as_is(project: Path) -> None:
    """A template that is already right is neither written nor renamed."""
    write_template(project, NoteExtension.MD_TXT, 'Mine.\n')
    write_template(project / 'sub', NoteExtension.MD_TXT, 'Also mine.\n')
    report = open_project(project, refuse_choice)
    assert not report.created
    assert not report.renamed
    assert report.project.tree.template == project / 'template.md.txt'


def test_template_renamed(project: Path) -> None:
    """A template carrying another extension is given the right one."""
    write_template(project, NoteExtension.TXT, 'Mine.\n')
    report = open_project(project, refuse_choice)
    wanted = project / 'template.md.txt'
    assert report.project.tree.template == wanted
    assert list(report.renamed) == [wanted]
    assert wanted.read_text(encoding='utf-8') == 'Mine.\n'
    assert not (project / 'template.txt').exists()


def test_renamed_is_no_note(project: Path) -> None:
    """A renamed template is a template, and no note of the folder."""
    write_template(project, NoteExtension.MD)
    report = open_project(project, refuse_choice)
    assert names_of(report.project.tree) == ['a.md.txt', 'b.md.txt']
    assert read_order_text(project) == order_text(['a.md.txt', 'b.md.txt'])


def test_chosen_template_kept(project: Path, trashed: list[Path]) -> None:
    """Of several templates the chosen one is kept, and named rightly."""
    write_template(project, NoteExtension.MD, 'Keep me.\n')
    write_template(project, NoteExtension.TXT, 'Drop me.\n')
    report = open_project(project, first_choice)
    wanted = project / 'template.md.txt'
    assert trashed == [project / 'template.txt']
    assert report.project.tree.template == wanted
    assert wanted.read_text(encoding='utf-8') == 'Keep me.\n'


def test_choice_is_asked(project: Path, trashed: list[Path]) -> None:
    """The chooser is asked about the folder that holds the templates."""
    asked: list[tuple[Path, list[str]]] = []

    def choose(folder: Path, templates: Sequence[Path]) -> Path:
        """Stand in for a user choosing which template to keep."""
        asked.append((folder, [path.name for path in templates]))
        return templates[-1]
    write_template(project / 'sub', NoteExtension.MD)
    write_template(project / 'sub', NoteExtension.TXT)
    open_project(project, choose)
    assert asked == [(project / 'sub', ['template.md', 'template.txt'])]
    assert trashed == [project / 'sub' / 'template.md']


def test_no_choice_refuses(project: Path, trashed: list[Path]) -> None:
    """Choosing no template at all leaves the project unopened."""
    write_template(project, NoteExtension.MD)
    write_template(project, NoteExtension.TXT)
    with pytest.raises(NotesmgrError):
        open_project(project, refuse_choice)
    assert not trashed
    assert (project / 'template.md').is_file()
    assert (project / 'template.txt').is_file()


def test_trash_refused(project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A template that cannot be trashed is reported, not raised."""
    def refuse(path: Path) -> None:
        """Stand in for a trash that will not take the file."""
        raise OSError(f'no trash for {path}')
    monkeypatch.setattr(project_ops, 'send2trash', refuse)
    write_template(project, NoteExtension.MD)
    write_template(project, NoteExtension.TXT)
    report = open_project(project, first_choice)
    assert len(report.problems) == 1
    assert 'template.txt' in report.problems[0]


@pytest.mark.skipif(os.name == 'nt', reason='file modes differ on Windows')
def test_order_problem_told(project: Path) -> None:
    """A folder whose order cannot be read is reported and still shown."""
    written = write_order(project, ['b.md.txt'])
    written.chmod(stat.S_IWUSR)
    try:
        report = open_project(project, refuse_choice)
    finally:
        written.chmod(stat.S_IRUSR | stat.S_IWUSR)
    assert len(report.problems) == 1
    assert names_of(report.project.tree) == ['a.md.txt', 'b.md.txt']


@pytest.mark.skipif(os.name == 'nt', reason='file modes differ on Windows')
def test_folder_problem_told(project: Path) -> None:
    """A folder that cannot be read is reported and shown as empty."""
    closed = project / 'sub'
    closed.chmod(stat.S_IWUSR)
    try:
        report = open_project(project, refuse_choice)
    finally:
        closed.chmod(stat.S_IRWXU)
    assert len(report.problems) == 1
    below = report.project.tree.folders[0]
    assert below.template is None
    assert not below.notes


def test_hidden_files_left(project: Path) -> None:
    """What notesmgr keeps for itself is no part of what it shows."""
    write_file(project / '.hidden.md.txt', 'not a note')
    report = open_project(project, refuse_choice)
    assert names_of(report.project.tree) == ['a.md.txt', 'b.md.txt']
    assert ORDER_NAME not in names_of(report.project.tree)


@pytest.mark.parametrize('renamed,created,holds', [
    ([], [], []),
    (['a'], [], [RENAMED_HEAD, 'a']),
    ([], ['b'], [CREATED_HEAD, 'b']),
    (['a'], ['b'], [RENAMED_HEAD, 'a', CREATED_HEAD, 'b'])])
def test_changed_message(project: Path, renamed: list[str], created: list[str],
                         holds: list[str]) -> None:
    """What opening a project changed is told, and nothing else is."""
    report = open_project(project, refuse_choice)._replace(
        renamed=[project / name for name in renamed],
        created=[project / name for name in created])
    message = changed_message(report)
    for part in holds:
        assert part in message
    assert bool(message) == bool(holds)
