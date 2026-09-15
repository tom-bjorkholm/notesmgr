#! /usr/local/bin/python3
"""Tests for the configuration of notesmgr."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import json
from pathlib import Path
from typing import Iterator
import pytest
from config_as_json import InvalidConfiguration, InvalidConfigurationType
from notesmgr import config as config_module
from notesmgr.config import DEFAULT_EXTENSION, NoteExtension, \
    NotesmgrConfig

TEST_EDITOR = 'test-editor'
"""Editor that the built-in default is replaced by in these tests."""


@pytest.fixture(name='known_default', autouse=True)
def fixture_known_default(monkeypatch: pytest.MonkeyPatch) -> Iterator[str]:
    """Let the default editor be the same on every machine."""
    monkeypatch.setattr(config_module, 'default_editor', lambda: TEST_EDITOR)
    yield TEST_EDITOR


def config_from(text: str) -> NotesmgrConfig:
    """Return the configuration that the given JSON text holds."""
    return NotesmgrConfig(from_json_data_text=text, stderr_file=io.StringIO())


def test_default_values() -> None:
    """A configuration that read nothing holds the built-in defaults."""
    config = NotesmgrConfig()
    assert config.editor == TEST_EDITOR
    assert config.file_extension is DEFAULT_EXTENSION


def test_default_is_md_txt() -> None:
    """New notes are named .md.txt, which every system accepts."""
    assert DEFAULT_EXTENSION.value == '.md.txt'


@pytest.mark.parametrize('member,extension', [
    (NoteExtension.MD, '.md'),
    (NoteExtension.TXT, '.txt'),
    (NoteExtension.MD_TXT, '.md.txt')])
def test_extension_values(member: NoteExtension, extension: str) -> None:
    """Each extension member holds the extension it stands for."""
    assert member.value == extension


def test_file_holds_the_name() -> None:
    """The configuration file holds the name of the extension member."""
    written = NotesmgrConfig().as_json_string(io.StringIO())
    assert json.loads(written)['file_extension'] == 'MD_TXT'


def test_json_round_trip() -> None:
    """A written configuration reads back as the same values."""
    config = NotesmgrConfig()
    config.editor = 'code -w'
    config.file_extension = NoteExtension.TXT
    read_back = config_from(config.as_json_string(io.StringIO()))
    assert read_back.editor == 'code -w'
    assert read_back.file_extension is NoteExtension.TXT


def test_file_round_trip(tmp_path: Path) -> None:
    """A configuration written to a file reads back as the same values."""
    written = tmp_path / 'notesmgr.cfg'
    config = NotesmgrConfig()
    config.file_extension = NoteExtension.MD
    config.write(written, io.StringIO())
    read_back = NotesmgrConfig(from_json_filename=written,
                               stderr_file=io.StringIO())
    assert read_back.file_extension is NoteExtension.MD


@pytest.mark.parametrize('written,expected', [
    ('MD', NoteExtension.MD),
    ('TXT', NoteExtension.TXT),
    ('MD_TXT', NoteExtension.MD_TXT),
    ('md_txt', NoteExtension.MD_TXT),
    ('Md_Txt', NoteExtension.MD_TXT),
    ('T', NoteExtension.TXT)])
def test_reads_extension(written: str, expected: NoteExtension) -> None:
    """An extension is read by name, in any case and by a clear start."""
    config = config_from(f'{{"editor": "vi", "file_extension": "{written}"}}')
    assert config.file_extension is expected


@pytest.mark.parametrize('written', ['', 'MD.TXT', '.md.txt', 'markdown',
                                     'M', '17'])
def test_refuses_extension(written: str) -> None:
    """A name that no extension member has is refused when it is read."""
    with pytest.raises(ValueError):
        config_from(f'{{"editor": "vi", "file_extension": "{written}"}}')


@pytest.mark.parametrize('written,expected', [
    ('vi', 'vi'),
    ('  vi  ', 'vi'),
    ('code -w {file}', 'code -w {file}'),
    ('\tnotepad\n', 'notepad')])
def test_editor_is_stripped(written: str, expected: str) -> None:
    """The editor command is kept without the blanks around it."""
    config = config_from(json.dumps({'editor': written,
                                     'file_extension': 'MD'}))
    assert config.editor == expected


@pytest.mark.parametrize('written', ['', ' ', '\t\n  '])
def test_refuses_empty_editor(written: str) -> None:
    """An editor command that names no program at all is refused."""
    with pytest.raises(InvalidConfiguration):
        config_from(json.dumps({'editor': written, 'file_extension': 'MD'}))


@pytest.mark.parametrize('written,refusal', [
    (17, InvalidConfigurationType),
    (3.5, InvalidConfigurationType),
    (True, InvalidConfigurationType),
    (None, InvalidConfigurationType),
    (['vi'], InvalidConfigurationType),
    ({'a': 'vi'}, KeyError)])
def test_refuses_other_type(written: object, refusal: type[Exception]) -> None:
    """An editor command that is not a text at all is refused.

    A JSON object where a value was expected is a shape that does not
    match, which config_as_json reports as a KeyError rather than as
    an invalid configuration type.
    """
    with pytest.raises(refusal):
        config_from(json.dumps({'editor': written, 'file_extension': 'MD'}))


def test_validate_accepts() -> None:
    """A configuration holding sensible values passes validation."""
    config = NotesmgrConfig()
    config.validate(io.StringIO())
    assert config.editor == TEST_EDITOR


def test_validate_refuses() -> None:
    """A configuration given an empty editor fails validation."""
    config = NotesmgrConfig()
    config.editor = '   '
    with pytest.raises(InvalidConfiguration):
        config.validate(io.StringIO())
