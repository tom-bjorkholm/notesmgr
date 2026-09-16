#! /usr/local/bin/python3
"""What a formatted copy of a note is, and running what takes it.

The clipboard of Tk carries plain text and nothing else, so a copy
that keeps its formatting is handed to a program of the system
instead. Running such a program and saying what it could not do is
the same on every platform, and is therefore done here.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import subprocess
from typing import NamedTuple, Optional, Sequence
from notesmgr.errors import NotesmgrError

NOT_INSTALLED = 'The program {program} is not installed, and it is what ' \
    'puts a formatted copy on the clipboard here.'
"""What is said when the system has not got the program it needs."""

REFUSED = 'The program {program} did not take a formatted copy of the ' \
    'note.\n{reason}'
"""What is said when the program was there but did not do it."""


class RichText(NamedTuple):
    """A copy of a note in the shapes that a clipboard takes it in.

    The HTML is what goes inside the body of a document rather than
    a whole document, so that each platform can wrap it the way its
    own clipboard asks for. The text is the note as it is written,
    which is what a plain text field is pasted with.
    """

    html: str
    text: str


def said_by(output: Optional[bytes]) -> str:
    """Return what a program wrote about itself, as text.

    Args:
        output: What the program wrote on its error output, None
            when nothing was read from it.

    Returns:
        What it said, and nothing at all when it said nothing.
    """
    return '' if not output else output.decode('utf-8', 'replace').strip()


def run_tool(argv: Sequence[str], data: bytes, capture: bool = True) -> bytes:
    """Run a program of the system, and return what it wrote.

    Args:
        argv: The program to run and the arguments to give it.
        data: What is written to the program on its input.
        capture: Whether to read what the program writes. A program
            that goes on running to own the clipboard, as the ones
            of the X11 and the Wayland desktops do, never closes its
            output, and waiting for that output to end would be
            waiting for the program to end.

    Returns:
        What the program wrote, and nothing when it is not read.

    Raises:
        NotesmgrError: The program is not installed, could not be
            started, or refused to do it.
    """
    where = subprocess.PIPE if capture else subprocess.DEVNULL
    try:
        done = subprocess.run(argv, input=data, stdout=where, stderr=where,
                              check=True)
    except FileNotFoundError as error:
        raise NotesmgrError(NOT_INSTALLED.format(program=argv[0])) from error
    except subprocess.CalledProcessError as error:
        reason = said_by(error.stderr) or str(error)
        raise NotesmgrError(REFUSED.format(program=argv[0],
                                           reason=reason)) from error
    except OSError as error:
        raise NotesmgrError(REFUSED.format(program=argv[0],
                                           reason=error)) from error
    return done.stdout or b''
