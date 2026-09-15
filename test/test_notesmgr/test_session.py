#! /usr/local/bin/python3
"""Tests for what one run of the notesmgr application knows."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
from pathlib import Path
import pytest
from test_notesmgr.helpers import refuse_choice, write_config, write_notes
from notesmgr.config import NoteExtension
from notesmgr.project import Project, config_path
from notesmgr.project_ops import open_project
from notesmgr.session import Session, start_folder


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Project:
    """Provide an opened project that a session can be told about."""
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD_TXT)
    write_notes(root, ['a.md.txt'])
    return open_project(root, refuse_choice).project


def test_start_folder_is_cwd(tmp_path: Path,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """The application starts out looking where it was started from."""
    monkeypatch.chdir(tmp_path)
    assert start_folder() == Path.cwd()


def test_start_folder_gone(home: Path,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """A folder that is gone is no place to look, so the home folder is."""
    def refuse() -> Path:
        """Stand in for a working folder that has been taken away."""
        raise OSError('no such folder')
    monkeypatch.setattr(os, 'getcwd', refuse)
    assert start_folder() == home


def test_nothing_open_first(tmp_path: Path) -> None:
    """A session that has opened nothing yet has no project."""
    session = Session(tmp_path)
    assert session.project is None
    assert session.config_file() is None


def test_chooser_starts_there(tmp_path: Path) -> None:
    """Until a project is opened, a chooser starts where the run began."""
    assert Session(tmp_path).chooser_folder() == tmp_path


def test_chooser_from_cwd(tmp_path: Path,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Told no folder, a session looks where the application was started."""
    monkeypatch.chdir(tmp_path)
    assert Session().chooser_folder() == Path.cwd()


def test_chooser_after_open(tmp_path: Path, project: Project) -> None:
    """Once a project is open, a chooser starts in that project."""
    session = Session(tmp_path)
    session.opened(project)
    assert session.chooser_folder() == project.root


def test_config_after_open(tmp_path: Path, project: Project) -> None:
    """The configuration file of the session is the project's own."""
    session = Session(tmp_path)
    session.opened(project)
    assert session.project is project
    assert session.config_file() == config_path(project.root)
