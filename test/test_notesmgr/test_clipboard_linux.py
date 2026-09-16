#! /usr/local/bin/python3
"""Tests for the formatted copy that an X11 or Wayland desktop is given."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import shutil
from functools import partial
from typing import AbstractSet, NamedTuple, Optional, Sequence
import pytest
from notesmgr import clipboard_linux
from notesmgr.clipboard_linux import CHARSET, NO_TOOL, WL_COPY, XCLIP, \
    copy_to_clipboard, html_tool
from notesmgr.clipboard_tool import RichText
from notesmgr.errors import NotesmgrError

HTML = '<h1>Rubrik</h1><p>Text with åäö in it.</p>'
"""The HTML of the note that these tests copy."""

TEXT = '# Rubrik\n\nText with åäö in it.\n'
"""The note that these tests copy, as it is written."""

COPY = RichText(HTML, TEXT)
"""The copy that these tests hand to the clipboard."""

BOTH = {'xclip', 'wl-copy'}
"""A desktop that has both of the programs installed."""


class Run(NamedTuple):
    """One program that the backend asked to have run."""

    argv: tuple[str, ...]
    data: bytes
    capture: bool


def found(names: AbstractSet[str], name: str) -> Optional[str]:
    """Stand in for which(), finding only the programs that are named."""
    return f'/usr/bin/{name}' if name in names else None


@pytest.fixture(name='runs')
def fixture_runs(monkeypatch: pytest.MonkeyPatch) -> list[Run]:
    """Record the programs the backend runs, running none of them."""
    asked: list[Run] = []

    def record(argv: Sequence[str], data: bytes,
               capture: bool = True) -> bytes:
        """Stand in for running a program of the system."""
        asked.append(Run(tuple(argv), data, capture))
        return b''
    monkeypatch.setattr(clipboard_linux, 'run_tool', record)
    return asked


def install(monkeypatch: pytest.MonkeyPatch, names: AbstractSet[str]) -> None:
    """Let the desktop of a test have the named programs and no others."""
    monkeypatch.setattr(shutil, 'which', partial(found, names))


@pytest.mark.parametrize('names,expected', [
    ({'xclip'}, XCLIP),
    ({'wl-copy'}, WL_COPY),
    (BOTH, XCLIP),
    (set(), None),
    ({'pbcopy'}, None)])
def test_html_tool(monkeypatch: pytest.MonkeyPatch, names: AbstractSet[str],
                   expected: Optional[Sequence[str]]) -> None:
    """The program that takes a formatted copy is the one installed."""
    install(monkeypatch, names)
    assert html_tool() == expected


def test_html_is_given(monkeypatch: pytest.MonkeyPatch,
                       runs: list[Run]) -> None:
    """The HTML of the note is what the clipboard is given."""
    install(monkeypatch, {'xclip'})
    copy_to_clipboard(COPY)
    assert runs == [Run(XCLIP, (CHARSET + HTML).encode('utf-8'), False)]


def test_wayland_is_used(monkeypatch: pytest.MonkeyPatch,
                         runs: list[Run]) -> None:
    """A desktop with wl-copy alone has its copy taken by wl-copy."""
    install(monkeypatch, {'wl-copy'})
    copy_to_clipboard(COPY)
    assert runs[0].argv == WL_COPY


def test_owner_not_waited_for(monkeypatch: pytest.MonkeyPatch,
                              runs: list[Run]) -> None:
    """The program that goes on owning the clipboard is not waited for."""
    install(monkeypatch, BOTH)
    copy_to_clipboard(COPY)
    assert not runs[0].capture


def test_no_tool_told(monkeypatch: pytest.MonkeyPatch,
                      runs: list[Run]) -> None:
    """A desktop with neither program is told to be missing one."""
    install(monkeypatch, set())
    with pytest.raises(NotesmgrError) as raised:
        copy_to_clipboard(COPY)
    assert str(raised.value) == NO_TOOL
    assert runs == []
