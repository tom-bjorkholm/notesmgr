#! /usr/local/bin/python3
"""Tests for opening the editor of the notesmgr configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Callable, NamedTuple, Optional
import pytest
from config_as_json import Config
from notesmgr import config_editor
from notesmgr.config import NotesmgrConfig
from notesmgr.config_files import CONFIG_NAME, CONFIG_VARIABLE
from notesmgr.config_editor import editor_files, open_config_editor
from notesmgr.descriptions import DESCRIPTIONS

CONFIG_TEXT = '{"editor": "vi", "file_extension": "MD"}'
"""Content of a user wide configuration file in these tests."""


class PanelCall(NamedTuple):
    """What the configuration editor panel was asked to open."""

    config: Config
    parent: object
    descriptions: object
    in_file: Optional[Path]
    out_file: Path
    on_close: Callable[[], None]


@pytest.fixture(name='opened')
def fixture_opened(monkeypatch: pytest.MonkeyPatch) -> list[PanelCall]:
    """Record what the editor panel was asked for, opening no window."""
    calls: list[PanelCall] = []

    def record(config: Config, **kwargs: object) -> PanelCall:
        """Stand in for the editor panel of edit-cfg-json-tk."""
        call = PanelCall(config=config, **kwargs)  # type: ignore[arg-type]
        calls.append(call)
        return call
    monkeypatch.setattr(config_editor, 'TkEditorPanel', record)
    return calls


def open_over(window: tkinter.Toplevel,
              config_file: Optional[Path] = None) -> Callable[[], None]:
    """Open the editor over a window and return what it tells at the end."""
    def closed() -> None:
        """Stand in for what the application does at the end."""
    open_config_editor(window, closed, config_file)
    return closed


def test_edits_own_config(opened: list[PanelCall],
                          top_window: tkinter.Toplevel) -> None:
    """The panel is given a notesmgr configuration to edit."""
    open_over(top_window)
    assert isinstance(opened[0].config, NotesmgrConfig)


def test_opened_over_window(opened: list[PanelCall],
                            top_window: tkinter.Toplevel) -> None:
    """The panel is opened over the window it was given."""
    open_over(top_window)
    assert opened[0].parent is top_window


def test_members_described(opened: list[PanelCall],
                           top_window: tkinter.Toplevel) -> None:
    """The panel is told what the members of the configuration are for."""
    open_over(top_window)
    assert opened[0].descriptions is DESCRIPTIONS


def test_closing_is_told(opened: list[PanelCall],
                         top_window: tkinter.Toplevel) -> None:
    """The panel is told whom to tell that the session has ended."""
    told = open_over(top_window)
    assert opened[0].on_close is told


def test_reads_existing_file(home: Path, opened: list[PanelCall],
                             top_window: tkinter.Toplevel) -> None:
    """A user wide configuration that is there already is edited."""
    written = home / CONFIG_NAME
    written.write_text(CONFIG_TEXT, encoding='utf-8')
    open_over(top_window)
    assert opened[0].in_file == written
    assert opened[0].out_file == written


def test_starts_from_defaults(home: Path, opened: list[PanelCall],
                              top_window: tkinter.Toplevel) -> None:
    """With no configuration file yet, the defaults are what is edited."""
    open_over(top_window)
    assert opened[0].in_file is None
    assert opened[0].out_file == home / CONFIG_NAME


def test_writes_named_file(opened: list[PanelCall], tmp_path: Path,
                           top_window: tkinter.Toplevel,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """The file the environment names is the one that is written."""
    named = tmp_path / 'named.cfg'
    monkeypatch.setenv(CONFIG_VARIABLE, str(named))
    open_over(top_window)
    assert opened[0].out_file == named


def test_project_file_edited(opened: list[PanelCall],
                             top_window: tkinter.Toplevel,
                             tmp_path: Path) -> None:
    """The configuration of a project is read and written where it lives."""
    project = tmp_path / 'notesmgr.cfg'
    project.write_text(CONFIG_TEXT, encoding='utf-8')
    open_over(top_window, project)
    assert opened[0].in_file == project
    assert opened[0].out_file == project


def test_files_of_project(tmp_path: Path) -> None:
    """A project configuration file is the file read and the file written."""
    project = tmp_path / 'notesmgr.cfg'
    assert editor_files(project) == (project, project)


def test_files_of_user_wide(home: Path) -> None:
    """With no project the user wide file is written, and read when there."""
    assert editor_files(None) == (None, home / CONFIG_NAME)
    (home / CONFIG_NAME).write_text(CONFIG_TEXT, encoding='utf-8')
    assert editor_files(None) == (home / CONFIG_NAME, home / CONFIG_NAME)
