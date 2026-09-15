#! /usr/local/bin/python3
"""Tests for where the user wide configuration of notesmgr is kept."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
import pytest
from notesmgr.config import NoteExtension
from notesmgr.config_files import CONFIG_NAME, CONFIG_VARIABLE, \
    copy_to_user_wide, read_config_file, user_config_path, \
    user_config_source, user_wide_config, write_config_file
from notesmgr.errors import NotesmgrError

PROJECT_TEXT = '{"editor": "vi", "file_extension": "MD"}'
"""Content of the project configuration file that is copied."""

BROKEN_TEXT = 'this file holds no JSON at all'
"""Content of a file that is no configuration file."""


@pytest.fixture(name='project_config')
def fixture_project_config(tmp_path: Path) -> Path:
    """Provide a project configuration file that can be copied."""
    written = tmp_path / 'project' / 'notesmgr.cfg'
    written.parent.mkdir()
    written.write_text(PROJECT_TEXT, encoding='utf-8')
    return written


def test_path_in_home(home: Path) -> None:
    """With nothing named, the file in the home folder is the one."""
    assert user_config_path() == home / CONFIG_NAME


def test_path_from_variable(tmp_path: Path,
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """The file the environment names is the one that is written."""
    named = tmp_path / 'named.cfg'
    monkeypatch.setenv(CONFIG_VARIABLE, str(named))
    assert user_config_path() == named


@pytest.mark.parametrize('named', ['', '   ', '\t'])
def test_path_blank_variable(home: Path, named: str,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """A variable holding nothing but blanks names no file at all."""
    monkeypatch.setenv(CONFIG_VARIABLE, named)
    assert user_config_path() == home / CONFIG_NAME


def test_source_is_none() -> None:
    """With no configuration file anywhere, there is nothing to read."""
    assert user_config_source() is None


def test_source_in_home(home: Path) -> None:
    """The file in the home folder is read when it is there."""
    in_home = home / CONFIG_NAME
    in_home.write_text(PROJECT_TEXT, encoding='utf-8')
    assert user_config_source() == in_home


def test_source_from_variable(home: Path, tmp_path: Path,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """The file the environment names is read before the home one."""
    (home / CONFIG_NAME).write_text(PROJECT_TEXT, encoding='utf-8')
    named = tmp_path / 'named.cfg'
    named.write_text(PROJECT_TEXT, encoding='utf-8')
    monkeypatch.setenv(CONFIG_VARIABLE, str(named))
    assert user_config_source() == named


def test_source_named_missing(home: Path, tmp_path: Path,
                              monkeypatch: pytest.MonkeyPatch) -> None:
    """A named file that is not there yet leaves the home one to be read."""
    in_home = home / CONFIG_NAME
    in_home.write_text(PROJECT_TEXT, encoding='utf-8')
    monkeypatch.setenv(CONFIG_VARIABLE, str(tmp_path / 'not_written_yet.cfg'))
    assert user_config_source() == in_home


def test_source_named_folder(tmp_path: Path,
                             monkeypatch: pytest.MonkeyPatch) -> None:
    """A name that is a folder and not a file is nothing to read."""
    monkeypatch.setenv(CONFIG_VARIABLE, str(tmp_path))
    assert user_config_source() is None


def test_copy_to_user_wide(home: Path, project_config: Path) -> None:
    """The project's configuration becomes the user wide one."""
    written = copy_to_user_wide(project_config)
    assert written == home / CONFIG_NAME
    assert written.read_text(encoding='utf-8') == PROJECT_TEXT


def test_copy_makes_folder(project_config: Path, tmp_path: Path,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """A named file in a folder that is not there gets that folder."""
    named = tmp_path / 'settings' / 'notesmgr.cfg'
    monkeypatch.setenv(CONFIG_VARIABLE, str(named))
    assert copy_to_user_wide(project_config) == named
    assert named.read_text(encoding='utf-8') == PROJECT_TEXT


def test_copy_overwrites(home: Path, project_config: Path) -> None:
    """A user wide configuration that is there already is replaced."""
    (home / CONFIG_NAME).write_text('older content', encoding='utf-8')
    assert copy_to_user_wide(project_config).read_text(
        encoding='utf-8') == PROJECT_TEXT


def test_copy_missing_source(home: Path, tmp_path: Path) -> None:
    """Copying a project configuration that is not there is refused."""
    with pytest.raises(OSError):
        copy_to_user_wide(tmp_path / 'no_such.cfg')
    assert not (home / CONFIG_NAME).exists()


def test_read_config_file(project_config: Path) -> None:
    """A configuration file is read as the configuration it holds."""
    config = read_config_file(project_config)
    assert config.editor == 'vi'
    assert config.file_extension is NoteExtension.MD


def test_read_missing_file(tmp_path: Path) -> None:
    """A configuration file that is not there is reported, not exited."""
    with pytest.raises(NotesmgrError):
        read_config_file(tmp_path / 'no_such.cfg')


@pytest.mark.parametrize('text', [
    BROKEN_TEXT,
    '',
    '[1, 2, 3]',
    '{"editor": "vi", "file_extension": "RTF"}',
    '{"editor": "", "file_extension": "MD"}',
    '{"editor": "vi", "file_extension": "MD", "extra": 1}'])
def test_read_broken_file(tmp_path: Path, text: str) -> None:
    """A file holding no usable configuration is reported, not raised."""
    written = tmp_path / 'broken.cfg'
    written.write_text(text, encoding='utf-8')
    with pytest.raises(NotesmgrError):
        read_config_file(written)


def test_write_config_file(tmp_path: Path, project_config: Path) -> None:
    """A configuration that is written is read back as it was."""
    written = tmp_path / 'written.cfg'
    write_config_file(read_config_file(project_config), written)
    read_back = read_config_file(written)
    assert read_back.editor == 'vi'
    assert read_back.file_extension is NoteExtension.MD


def test_write_refused(tmp_path: Path, project_config: Path) -> None:
    """A configuration that cannot be written is reported, not raised."""
    config = read_config_file(project_config)
    with pytest.raises(NotesmgrError):
        write_config_file(config, tmp_path / 'no_such' / 'written.cfg')


def test_user_wide_defaults() -> None:
    """With no user wide configuration file, the defaults are what there is."""
    assert user_wide_config().file_extension is NoteExtension.MD_TXT


def test_user_wide_read(home: Path) -> None:
    """A user wide configuration file is what a new project starts from."""
    (home / CONFIG_NAME).write_text(PROJECT_TEXT, encoding='utf-8')
    assert user_wide_config().editor == 'vi'


def test_user_wide_broken(home: Path) -> None:
    """A user wide configuration file that is broken is reported."""
    (home / CONFIG_NAME).write_text(BROKEN_TEXT, encoding='utf-8')
    with pytest.raises(NotesmgrError):
        user_wide_config()
