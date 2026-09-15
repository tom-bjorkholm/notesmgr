#! /usr/local/bin/python3
"""Tests for what notesmgr says about its configuration members."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from notesmgr.config import NotesmgrConfig
from notesmgr.descriptions import DESCRIPTIONS


def configuration_members() -> list[str]:
    """Return the names of the members that a configuration holds."""
    return [name for name in vars(NotesmgrConfig())
            if not name.startswith('_')]


def test_every_member_told() -> None:
    """Every member of the configuration is described to the user."""
    described = {path[0] for path in DESCRIPTIONS}
    assert described == set(configuration_members())


@pytest.mark.parametrize('path', list(DESCRIPTIONS))
def test_paths_name_members(path: tuple[str, ...]) -> None:
    """Each description names one member of the configuration itself."""
    assert len(path) == 1


@pytest.mark.parametrize('path', list(DESCRIPTIONS))
def test_description_is_text(path: tuple[str, ...]) -> None:
    """Each description is a sentence and not an empty text."""
    assert DESCRIPTIONS[path].strip()


def test_extensions_unlisted() -> None:
    """The extensions are left to the editor, which reads them itself."""
    assert '.md.txt' not in DESCRIPTIONS[('file_extension',)]
