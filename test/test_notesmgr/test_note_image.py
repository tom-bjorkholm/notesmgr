#! /usr/local/bin/python3
"""Tests for which file an image of a note names."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
import pytest
from notesmgr.note_image import MAX_IMAGE_WIDTH, image_path, is_remote, \
    shrink_factor

FOLDER = Path('/notes/project')
"""The folder that the note of these tests is taken to be in."""


@pytest.mark.parametrize('target,expected', [
    ('picture.png', False),
    ('deeper/picture.png', False),
    ('../beside/picture.png', False),
    ('/absolute/picture.png', False),
    ('C:/windows/picture.png', False),
    ('c:\\windows\\picture.png', False),
    ('', False),
    ('http://example.com/picture.png', True),
    ('https://example.com/picture.png', True),
    ('ftp://example.com/picture.png', True),
    ('data:image/png;base64,AAAA', True)])
def test_is_remote(target: str, expected: bool) -> None:
    """What names an address is told from what names a file.

    The drive of a path on Microsoft Windows looks like a scheme of
    a single letter, which is the one case that has to be told apart.
    """
    assert is_remote(target) == expected


@pytest.mark.parametrize('target,expected', [
    ('picture.png', FOLDER / 'picture.png'),
    ('deeper/picture.png', FOLDER / 'deeper/picture.png'),
    ('../picture.png', FOLDER / '../picture.png'),
    ('/elsewhere/picture.png', Path('/elsewhere/picture.png')),
    ('', None),
    ('https://example.com/picture.png', None)])
def test_image_beside_note(target: str, expected: Optional[Path]) -> None:
    """An image is looked for beside the note that shows it."""
    assert image_path(FOLDER, target) == expected


@pytest.mark.parametrize('target', ['picture.png', 'deeper/picture.png'])
def test_image_of_no_folder(target: str) -> None:
    """An image named beside a note that is nowhere names no file."""
    assert image_path(None, target) is None


def test_whole_path_alone() -> None:
    """An image named by its whole path needs no folder to be in."""
    assert image_path(None, '/elsewhere/picture.png') == \
        Path('/elsewhere/picture.png')


@pytest.mark.parametrize('width,limit,expected', [
    (10, 100, 1),
    (100, 100, 1),
    (101, 100, 2),
    (200, 100, 2),
    (201, 100, 3),
    (900, 100, 9),
    (100, 0, 1),
    (0, 100, 1)])
def test_shrink_factor(width: int, limit: int, expected: int) -> None:
    """An image too wide for the panel is shrunk by a whole factor."""
    assert shrink_factor(width, limit) == expected


def test_shrink_to_the_panel() -> None:
    """The width that an image is brought within is the panel's own."""
    assert shrink_factor(MAX_IMAGE_WIDTH) == 1
    assert shrink_factor(MAX_IMAGE_WIDTH + 1) == 2
