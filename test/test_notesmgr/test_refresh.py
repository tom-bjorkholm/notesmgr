#! /usr/local/bin/python3
"""Tests for reading the open project again after others changed it."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
from functools import partial
from pathlib import Path
import pytest
from test_notesmgr.helpers import build_folder_project, write_config, \
    write_notes
from notesmgr import main_window as window_module
from notesmgr.config import NoteExtension
from notesmgr.main_window import APPLICATION_NAME, CONFIG_MENU, FILE_MENU, \
    REFRESH_ENTRY, USER_WIDE_ENTRY, MainWindow
from notesmgr.project import config_path


@pytest.fixture(name='told', autouse=True)
def fixture_told(monkeypatch: pytest.MonkeyPatch) -> dict[str, list[str]]:
    """Record what the window told the user, by the kind of telling.

    Opening the project of these tests writes the templates that its
    folders lack, which the window tells the user of, so no message
    box may be put on the screen.
    """
    told: dict[str, list[str]] = {'error': [], 'info': []}
    for kind, messages in told.items():
        monkeypatch.setattr(window_module, f'show_{kind}',
                            partial(record_message, messages))
    return told


def record_message(messages: list[str], _parent: object, _title: str,
                   message: str) -> None:
    """Stand in for a message box, keeping what it would have said."""
    messages.append(message)


@pytest.fixture(name='project')
def fixture_project(main_window: MainWindow, tmp_path: Path) -> Path:
    """Provide the root of a project of folders that the window shows."""
    root = build_folder_project(tmp_path / 'notes')
    assert main_window.load_project(root)
    return root


def entry_state(main_window: MainWindow, menu: str, label: str) -> str:
    """Return whether one entry of a menu can be chosen."""
    return str(main_window.menu_bar.menus[menu].entrycget(label, 'state'))


def shows(main_window: MainWindow, path: Path) -> bool:
    """Return whether the explorer shows an item of the path."""
    return bool(main_window.explorer.tree.exists(str(path)))


def remove_item(path: Path) -> None:
    """Take a file, or a folder and all it holds, away as others would."""
    if path.is_dir():
        shutil.rmtree(path)
    else:
        path.unlink()


def test_refresh_waits(main_window: MainWindow) -> None:
    """With no project open, there is nothing to refresh."""
    assert entry_state(main_window, FILE_MENU, REFRESH_ENTRY) == 'disabled'


def test_refresh_offered(main_window: MainWindow, project: Path) -> None:
    """Once a project is open, it can be refreshed."""
    assert shows(main_window, project)
    assert entry_state(main_window, FILE_MENU, REFRESH_ENTRY) == 'normal'


def test_refresh_no_project(main_window: MainWindow,
                            told: dict[str, list[str]]) -> None:
    """Refreshing with no project open does nothing and tells nothing."""
    main_window.refresh()
    assert main_window.session.project is None
    assert told == {'error': [], 'info': []}


def test_refresh_shows_added(main_window: MainWindow, project: Path) -> None:
    """A note and a folder written by another program are shown."""
    write_notes(project / 'apple', ['new.md.txt'])
    write_notes(project / 'pear', ['p.md.txt'])
    main_window.menu_bar.menus[FILE_MENU].invoke(REFRESH_ENTRY)
    assert shows(main_window, project / 'apple' / 'new.md.txt')
    assert shows(main_window, project / 'pear' / 'p.md.txt')


def test_refresh_drops_gone(main_window: MainWindow, project: Path) -> None:
    """A note and a folder taken away by another program are not shown."""
    remove_item(project / 'first.md.txt')
    remove_item(project / 'zebra')
    main_window.refresh()
    assert not shows(main_window, project / 'first.md.txt')
    assert not shows(main_window, project / 'zebra')
    assert shows(main_window, project / 'second.md.txt')


def test_refresh_keeps_select(main_window: MainWindow, project: Path) -> None:
    """What was selected stays selected and shown when it is still there."""
    note = project / 'apple' / 'a.md.txt'
    main_window.select(note)
    main_window.refresh()
    assert main_window.explorer.selected_path() == note
    assert main_window.note_panel.shown_path() == str(note)


@pytest.mark.parametrize('selected,removed,expected', [
    ('apple/a.md.txt', 'apple/a.md.txt', 'apple'),
    ('apple/a.md.txt', 'apple', ''),
    ('zebra', 'zebra', '')])
def test_refresh_nearest(main_window: MainWindow, project: Path, selected: str,
                         removed: str, expected: str) -> None:
    """What was taken away leaves the nearest folder that is left selected.

    An empty expected path stands for the root folder of the project.
    """
    main_window.select(project / selected)
    remove_item(project / removed)
    main_window.refresh()
    assert main_window.explorer.selected_path() == project / expected
    assert main_window.note_panel.shown_path() == str(project / expected)


def test_refresh_reads_config(main_window: MainWindow, project: Path) \
        -> None:
    """A configuration changed by another program is taken up."""
    write_config(project, NoteExtension.TXT)
    main_window.refresh()
    config = main_window.session.config()
    assert config is not None
    assert config.file_extension == NoteExtension.TXT


@pytest.mark.parametrize('removed', [Path(), config_path(Path())])
def test_refresh_closes(main_window: MainWindow, project: Path,
                        told: dict[str, list[str]], removed: Path) -> None:
    """A project that cannot be read any more is told of and closed.

    An empty path stands for the root folder of the project.
    """
    remove_item(project / removed)
    main_window.refresh()
    assert len(told['error']) == 1
    assert main_window.session.project is None
    assert main_window.window.title() == APPLICATION_NAME
    assert not main_window.explorer.tree.get_children()
    assert main_window.note_panel.shown_path() == ''
    assert entry_state(main_window, FILE_MENU, REFRESH_ENTRY) == 'disabled'
    assert entry_state(main_window, CONFIG_MENU, USER_WIDE_ENTRY) == \
        'disabled'


def test_chooser_after_close(main_window: MainWindow, project: Path) -> None:
    """After a project is closed, a folder chooser starts where it was."""
    remove_item(config_path(project))
    main_window.refresh()
    assert main_window.session.chooser_folder() == project


def test_reopen_after_close(main_window: MainWindow, project: Path) -> None:
    """A closed project can be opened again once it can be read again."""
    config = config_path(project)
    text = config.read_text(encoding='utf-8')
    remove_item(config)
    main_window.refresh()
    config.write_text(text, encoding='utf-8')
    assert main_window.load_project(project)
    assert entry_state(main_window, FILE_MENU, REFRESH_ENTRY) == 'normal'
    assert shows(main_window, project / 'first.md.txt')
