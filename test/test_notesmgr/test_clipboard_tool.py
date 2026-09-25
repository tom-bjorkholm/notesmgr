#! /usr/local/bin/python3
"""Tests for running what takes a formatted copy of a note."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from pathlib import Path
from typing import Optional
import pytest
from notesmgr.clipboard_tool import NOT_INSTALLED, REFUSED, RichText, \
    run_tool, said_by
from notesmgr.errors import NotesmgrError

ECHO = 'import sys; sys.stdout.buffer.write(sys.stdin.buffer.read())'
"""A program that writes back whatever is written to it."""

COMPLAIN = 'import sys; sys.stderr.write("no good"); sys.exit(2)'
"""A program that refuses and says why it refuses."""

SILENT = 'import sys; sys.exit(3)'
"""A program that refuses without saying anything at all."""

MISSING = 'notesmgr-no-such-program'
"""The name of a program that no system has."""

SENT = 'a note with åäö in it\n'
"""What these tests write to the program they run."""


def program(source: str) -> tuple[str, ...]:
    """Return the command line that runs a program written here."""
    return (sys.executable, '-c', source)


def test_output_is_returned() -> None:
    """What the program writes is what running it gives back."""
    assert run_tool(program(ECHO), SENT.encode('utf-8')) == \
        SENT.encode('utf-8')


def test_nothing_read() -> None:
    """A program whose output is not read gives nothing back."""
    assert run_tool(program(ECHO), b'ignored', capture=False) == b''


def test_program_missing() -> None:
    """A program that is not installed is reported as missing."""
    with pytest.raises(NotesmgrError) as raised:
        run_tool((MISSING,), b'')
    assert str(raised.value) == NOT_INSTALLED.format(program=MISSING)


def test_not_a_program(tmp_path: Path) -> None:
    """A file that is there but cannot be run is reported as refusing."""
    text = tmp_path / 'not-a-program.txt'
    text.write_text('Just words.\n', encoding='utf-8')
    with pytest.raises(NotesmgrError) as raised:
        run_tool((str(text),), b'')
    told = str(raised.value)
    assert told.startswith(REFUSED.format(program=text, reason=''))


def test_refusal_explained() -> None:
    """What a program said about refusing is what the user is told."""
    with pytest.raises(NotesmgrError) as raised:
        run_tool(program(COMPLAIN), b'')
    assert str(raised.value) == REFUSED.format(program=sys.executable,
                                               reason='no good')


def test_silent_refusal() -> None:
    """A program that refuses without a word is still reported."""
    with pytest.raises(NotesmgrError) as raised:
        run_tool(program(SILENT), b'')
    told = str(raised.value)
    assert told.startswith(REFUSED.format(program=sys.executable, reason=''))
    assert 'exit status 3' in told


def test_silence_unread() -> None:
    """A refusal is reported even when the output was not read."""
    with pytest.raises(NotesmgrError) as raised:
        run_tool(program(COMPLAIN), b'', capture=False)
    assert 'exit status 2' in str(raised.value)


@pytest.mark.parametrize('output,expected', [
    (None, ''),
    (b'', ''),
    (b'  said it  \n', 'said it'),
    (b'first\nsecond', 'first\nsecond'),
    ('åäö\n'.encode('utf-8'), 'åäö'),
    (b'\xff\xfe not text', '�� not text')])
def test_said_by(output: Optional[bytes], expected: str) -> None:
    """What a program wrote about itself is read as the text it is."""
    assert said_by(output) == expected


def test_rich_text_shapes() -> None:
    """A copy holds the note as HTML and as the text it is written as."""
    copy = RichText('<p>a note</p>', 'a note\n')
    assert copy.html == '<p>a note</p>'
    assert copy.text == 'a note\n'
