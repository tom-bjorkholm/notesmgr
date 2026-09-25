#! /usr/local/bin/python3
"""Tests for the formatted copy that the clipboard of Windows is given."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import ctypes
import sys
from types import SimpleNamespace
from typing import cast
import pytest
from test_notesmgr.fake_windows import HTML_ID, Memory, fake_kernel32, \
    fake_user32
from notesmgr.clipboard_tool import RichText
from notesmgr.clipboard_windows import CLOSING, HTML_FORMAT, NO_MEMORY, \
    NOT_OPENED, NOT_TAKEN, NOT_WINDOWS, OPENING, UNICODE_TEXT, byte_length, \
    cf_html, copy_to_clipboard, html_bytes, moveable_memory, text_bytes, \
    write_clipboard
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

SHAPES = ((HTML_ID, b'<p>formatted</p>\0'), (UNICODE_TEXT, b'p\0\0\0'))
"""The two shapes of a copy that the made-up clipboard is given."""


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


def as_library(fake: SimpleNamespace) -> ctypes.CDLL:
    """Return a made-up library as the library that it stands in for."""
    return cast(ctypes.CDLL, fake)


def test_memory_holds_data() -> None:
    """The memory handed to the clipboard holds exactly what was given."""
    memory = Memory()
    kernel32 = fake_kernel32(memory)
    handle = moveable_memory(as_library(kernel32), b'held\0')
    assert memory.held(handle) == b'held\0'
    assert kernel32.GlobalUnlock.calls == [(handle,)]
    assert not kernel32.GlobalFree.calls


def test_memory_declared() -> None:
    """The memory functions are declared to take and give pointers."""
    kernel32 = fake_kernel32(Memory())
    moveable_memory(as_library(kernel32), b'\0')
    assert kernel32.GlobalAlloc.restype is ctypes.c_void_p
    assert kernel32.GlobalLock.restype is ctypes.c_void_p
    for name in ('GlobalLock', 'GlobalUnlock', 'GlobalFree'):
        assert getattr(kernel32, name).argtypes == [ctypes.c_void_p]


def test_no_memory() -> None:
    """Memory that is not had is reported, and nothing is written."""
    kernel32 = fake_kernel32(Memory(), allocates=False)
    with pytest.raises(NotesmgrError) as raised:
        moveable_memory(as_library(kernel32), b'lost\0')
    assert str(raised.value) == NO_MEMORY
    assert not kernel32.GlobalLock.calls


def test_lock_refused() -> None:
    """Memory that cannot be written to is freed again, and reported."""
    kernel32 = fake_kernel32(Memory(), locks=False)
    with pytest.raises(NotesmgrError) as raised:
        moveable_memory(as_library(kernel32), b'lost\0')
    assert str(raised.value) == NO_MEMORY
    assert kernel32.GlobalFree.calls == [(1,)]
    assert not kernel32.GlobalUnlock.calls


def test_every_shape_given() -> None:
    """Every shape is given in one session, holding what it is to hold."""
    memory = Memory()
    user32 = fake_user32()
    write_clipboard(as_library(user32), as_library(fake_kernel32(memory)),
                    SHAPES)
    given = user32.SetClipboardData.calls
    assert [named for named, _handle in given] == [HTML_ID, UNICODE_TEXT]
    assert [memory.held(handle) for _named, handle in given] == \
        [data for _named, data in SHAPES]
    for name in ('OpenClipboard', 'EmptyClipboard', 'CloseClipboard'):
        assert len(getattr(user32, name).calls) == 1


def test_clipboard_declared() -> None:
    """The clipboard is declared to take a handle of memory."""
    user32 = fake_user32()
    write_clipboard(as_library(user32), as_library(fake_kernel32(Memory())),
                    SHAPES)
    assert user32.SetClipboardData.restype is ctypes.c_void_p
    assert user32.SetClipboardData.argtypes == [ctypes.c_uint,
                                                ctypes.c_void_p]


def test_not_opened() -> None:
    """A clipboard held elsewhere is reported, and left untouched.

    It is neither emptied nor closed, because it was never opened.
    """
    user32 = fake_user32(opens=False)
    with pytest.raises(NotesmgrError) as raised:
        write_clipboard(as_library(user32),
                        as_library(fake_kernel32(Memory())), SHAPES)
    assert str(raised.value) == NOT_OPENED
    assert not user32.EmptyClipboard.calls
    assert not user32.CloseClipboard.calls


def test_shape_not_taken() -> None:
    """A shape the clipboard refuses is freed, reported and the last."""
    user32 = fake_user32(takes=False)
    kernel32 = fake_kernel32(Memory())
    with pytest.raises(NotesmgrError) as raised:
        write_clipboard(as_library(user32), as_library(kernel32), SHAPES)
    assert str(raised.value) == NOT_TAKEN
    assert kernel32.GlobalFree.calls == [(1,)]
    assert len(user32.SetClipboardData.calls) == 1
    assert len(user32.CloseClipboard.calls) == 1


def test_no_memory_closes() -> None:
    """The clipboard is closed again when a shape gets no memory."""
    user32 = fake_user32()
    kernel32 = fake_kernel32(Memory(), allocates=False)
    with pytest.raises(NotesmgrError) as raised:
        write_clipboard(as_library(user32), as_library(kernel32), SHAPES)
    assert str(raised.value) == NO_MEMORY
    assert not user32.SetClipboardData.calls
    assert len(user32.CloseClipboard.calls) == 1


def test_copied_on_windows(monkeypatch: pytest.MonkeyPatch) -> None:
    """On Windows the copy is given as HTML Format and as wide text."""
    memory = Memory()
    user32 = fake_user32()
    windll = SimpleNamespace(user32=user32, kernel32=fake_kernel32(memory))
    monkeypatch.setattr(sys, 'platform', 'win32')
    monkeypatch.setattr(ctypes, 'windll', windll, raising=False)
    copy_to_clipboard(RichText('<p>a note</p>', 'a note'))
    assert user32.RegisterClipboardFormatW.calls == [(HTML_FORMAT,)]
    given = user32.SetClipboardData.calls
    assert [named for named, _handle in given] == [HTML_ID, UNICODE_TEXT]
    assert [memory.held(handle) for _named, handle in given] == \
        [html_bytes('<p>a note</p>'), text_bytes('a note')]
