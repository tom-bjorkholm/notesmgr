#! /usr/local/bin/python3
"""Tests for what a formatted copy of a note is made of."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path
from typing import Optional
import pytest
from notesmgr import clipboard_linux, clipboard_macos, clipboard_windows
from notesmgr import rich_clipboard
from notesmgr.clipboard_tool import RichText
from notesmgr.rich_clipboard import backend, copy_rich, local_images, \
    note_fragment, note_rich_text

MARKDOWN = '# Rubrik\n\nText **bold** and ~~struck~~.\n'
"""A note written in markdown, as these tests copy it."""

IMAGE = 'pic.png'
"""What a note of these tests names an image of its own."""


@pytest.mark.parametrize('text,expected', [
    ('# Rubrik\n', '<h1>Rubrik</h1>'),
    ('Text **bold**\n', '<p>Text <strong>bold</strong></p>'),
    ('Text ~~struck~~\n', '<p>Text <del>struck</del></p>'),
    ('', '')])
def test_markdown_fragment(text: str, expected: str) -> None:
    """A note written in markdown is copied as the markup it means."""
    assert note_fragment(text, True) == expected


@pytest.mark.parametrize('text,expected', [
    ('a note\n', '<pre>a note\n</pre>'),
    ('a & b\n', '<pre>a &amp; b\n</pre>'),
    ('<not markup>', '<pre>&lt;not markup&gt;</pre>'),
    ('col\tcol\n', '<pre>col\tcol\n</pre>'),
    ('', '<pre></pre>')])
def test_plain_fragment(text: str, expected: str) -> None:
    """A note that is no markdown is copied exactly as it is written."""
    assert note_fragment(text, False) == expected


def test_markup_is_text() -> None:
    """Markup that a note holds is copied as the text that it is."""
    assert note_fragment('A <b>tag</b> here\n', True) == \
        '<p>A &lt;b&gt;tag&lt;/b&gt; here</p>'


def test_copy_holds_both(tmp_path: Path) -> None:
    """A copy holds the note formatted and as it is written alike."""
    copy = note_rich_text(MARKDOWN, True, tmp_path)
    assert copy.text == MARKDOWN
    assert '<h1>Rubrik</h1>' in copy.html


def test_image_named_whole(tmp_path: Path) -> None:
    """An image beside the note is named by the file that it is."""
    html = f'<p><img alt="dot" src="{IMAGE}" /></p>'
    assert local_images(html, tmp_path) == \
        f'<p><img alt="dot" src="{(tmp_path / IMAGE).as_uri()}" /></p>'


def test_image_first_named() -> None:
    """An image is found however its description is written."""
    html = f'<img src="{IMAGE}">'
    named = local_images(html, Path('/notes'))
    assert named == f'<img src="{Path("/notes/pic.png").as_uri()}">'


@pytest.mark.parametrize('target', [
    'https://example.org/pic.png',
    'http://example.org/pic.png',
    ''])
def test_image_left_alone(target: str, tmp_path: Path) -> None:
    """An image that names no file of the machine is left as written."""
    html = f'<p><img alt="a" src="{target}" /></p>'
    assert local_images(html, tmp_path) == html


def test_image_without_folder() -> None:
    """An image beside a note of nowhere cannot be named any better."""
    html = f'<img alt="a" src="{IMAGE}" />'
    assert local_images(html, None) == html


def test_image_named_already(tmp_path: Path) -> None:
    """An image that names its whole file is named as a file is named."""
    named = tmp_path / IMAGE
    html = f'<img alt="a" src="{named}" />'
    assert local_images(html, None) == \
        f'<img alt="a" src="{named.as_uri()}" />'


def test_image_name_blank(tmp_path: Path) -> None:
    """A file whose name holds a blank is named so that it can be read."""
    html = '<img alt="a" src="my pic.png" />'
    named = local_images(html, tmp_path)
    assert (tmp_path / 'my pic.png').as_uri() in named
    assert ' pic.png"' not in named


def test_note_images_named(tmp_path: Path) -> None:
    """A markdown note has the images it shows named in the copy."""
    copy = note_rich_text(f'![dot]({IMAGE})\n', True, tmp_path)
    assert (tmp_path / IMAGE).as_uri() in copy.html


@pytest.mark.parametrize('platform,expected', [
    ('darwin', clipboard_macos.copy_to_clipboard),
    ('win32', clipboard_windows.copy_to_clipboard),
    ('linux', clipboard_linux.copy_to_clipboard),
    ('freebsd14', clipboard_linux.copy_to_clipboard)])
def test_backend_of_platform(monkeypatch: pytest.MonkeyPatch, platform: str,
                             expected: object) -> None:
    """Each platform has the way of copying that belongs to it."""
    monkeypatch.setattr(sys, 'platform', platform)
    assert backend() is expected


def test_copy_reaches_backend(monkeypatch: pytest.MonkeyPatch) -> None:
    """A copy is handed to whatever this platform takes a copy with."""
    taken: list[RichText] = []
    monkeypatch.setattr(sys, 'platform', 'linux')
    monkeypatch.setattr(clipboard_linux, 'copy_to_clipboard', taken.append)
    copy = note_rich_text(MARKDOWN, True)
    copy_rich(copy)
    assert taken == [copy]


def test_fragment_no_folder() -> None:
    """A note copied from nowhere in particular is copied all the same."""
    assert rich_clipboard.note_fragment(MARKDOWN, True, None) != ''


@pytest.mark.parametrize('folder', [None, Path('relative/folder')])
def test_relative_folder(folder: Optional[Path]) -> None:
    """A note of a folder that is no whole path names no image whole."""
    html = f'<img alt="a" src="{IMAGE}" />'
    assert local_images(html, folder) == html
