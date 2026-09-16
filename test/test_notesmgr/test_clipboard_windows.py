#! /usr/local/bin/python3
"""Tests for the formatted copy that the clipboard of Windows is given."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
import pytest
from notesmgr.clipboard_tool import RichText
from notesmgr.clipboard_windows import CLOSING, NOT_WINDOWS, OPENING, \
    byte_length, cf_html, copy_to_clipboard, html_bytes, text_bytes
from notesmgr.errors import NotesmgrError

FRAGMENTS = ['<p>plain ascii</p>',
             '<p>Text with åäö in it</p>',
             '<p>A note of one 🎉 emoji</p>',
             '<h1>Rubrik</h1>\r\n<ul><li>one</li><li>två</li></ul>',
             '<pre>{braces} and %s and {0}</pre>',
             '']
"""Notes whose HTML the payload is built from and measured on."""

ON_WINDOWS = sys.platform == 'win32'
"""Whether these tests are running on the platform they are about."""

HEADER_LINES = 5
"""How many lines of a payload say where its pieces are."""


def offsets(payload: str) -> dict[str, int]:
    """Return the offsets that the header of a payload names."""
    lines = payload.splitlines()[1:HEADER_LINES]
    return {name: int(value)
            for name, value in (line.split(':', 1) for line in lines)}


@pytest.mark.parametrize('text,expected', [
    ('', 0), ('abc', 3), ('åäö', 6), ('🎉', 4), ('a\r\nb', 4)])
def test_byte_length(text: str, expected: int) -> None:
    """A text is measured in the bytes that UTF-8 writes it as."""
    assert byte_length(text) == expected


@pytest.mark.parametrize('fragment', FRAGMENTS)
def test_document_is_found(fragment: str) -> None:
    """The header says where the document of the payload stands."""
    payload = cf_html(fragment)
    where = offsets(payload)
    raw = payload.encode('utf-8')
    assert raw[where['StartHTML']:where['EndHTML']] == \
        (OPENING + fragment + CLOSING).encode('utf-8')


@pytest.mark.parametrize('fragment', FRAGMENTS)
def test_fragment_is_found(fragment: str) -> None:
    """The header says where the piece that is pasted stands."""
    payload = cf_html(fragment)
    where = offsets(payload)
    raw = payload.encode('utf-8')
    assert raw[where['StartFragment']:where['EndFragment']] == \
        fragment.encode('utf-8')


@pytest.mark.parametrize('fragment', FRAGMENTS)
def test_document_ends_last(fragment: str) -> None:
    """The document reaches to the very end of the payload."""
    payload = cf_html(fragment)
    assert offsets(payload)['EndHTML'] == byte_length(payload)


def test_version_is_first() -> None:
    """The payload begins by saying which version it is written in."""
    assert cf_html(FRAGMENTS[0]).startswith('Version:0.9\r\n')


def test_offsets_stay_put() -> None:
    """The header is the same length whatever the numbers in it are."""
    lengths = {len(cf_html(fragment).splitlines()[1])
               for fragment in FRAGMENTS}
    assert len(lengths) == 1


def test_html_bytes_end() -> None:
    """The formatted shape is handed over as text that ends in a zero."""
    held = html_bytes(FRAGMENTS[1])
    assert held.endswith(b'\0')
    assert held[:-1].decode('utf-8') == cf_html(FRAGMENTS[1])


@pytest.mark.parametrize('text', ['', 'a note', 'åäö and 🎉'])
def test_text_bytes(text: str) -> None:
    """The plain shape is handed over as the wide text Windows takes."""
    assert text_bytes(text) == text.encode('utf-16-le') + b'\0\0'


@pytest.mark.skipif(ON_WINDOWS, reason='every other platform')
def test_only_on_windows() -> None:
    """The clipboard of Windows is not asked for anywhere else."""
    with pytest.raises(NotesmgrError) as raised:
        copy_to_clipboard(RichText('<p>a note</p>', 'a note'))
    assert str(raised.value) == NOT_WINDOWS
