#! /usr/local/bin/python3
"""Libraries of Windows made up for the tests, answering as told.

The clipboard of Windows is reached through ctypes, which is only
there on Windows. These stand in for the two libraries, so that what
notesmgr asks of them is tested on every platform. The memory they
hand out is real memory of this process, because notesmgr writes the
copy into it, and a made-up address would be written through.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import ctypes
from dataclasses import dataclass, field
from types import SimpleNamespace
from typing import Callable

HTML_ID = 49321
"""What the made-up clipboard numbers the shape named HTML Format."""


@dataclass
class Function:
    """One function of a library of Windows, as ctypes shows it.

    ctypes is told what a function takes and gives by setting its
    argtypes and restype, which is kept here to be looked at, and
    every call is recorded before it is answered.
    """

    does: Callable[..., int]
    restype: object = None
    argtypes: list[object] = field(default_factory=list)
    calls: list[tuple[object, ...]] = field(default_factory=list)

    def __call__(self, *args: object) -> int:
        """Record the call, and answer it."""
        self.calls.append(args)
        return self.does(*args)


def refuse(*_args: object) -> int:
    """Answer as a function of Windows answers when it failed."""
    return 0


def succeed(*_args: object) -> int:
    """Answer as a function of Windows answers when it did it."""
    return 1


class Memory:
    """The memory that the made-up kernel32 hands out, by its handle."""

    def __init__(self) -> None:
        """Hold no memory at all to begin with."""
        self.blocks: dict[int, ctypes.Array[ctypes.c_char]] = {}

    def alloc(self, _flags: int, size: int) -> int:
        """Hand out a block of real memory, as large as was asked."""
        handle = len(self.blocks) + 1
        self.blocks[handle] = ctypes.create_string_buffer(size)
        return handle

    def lock(self, handle: int) -> int:
        """Return where the block that a handle stands for is."""
        return ctypes.addressof(self.blocks[handle])

    def held(self, handle: int) -> bytes:
        """Return what the block that a handle stands for holds."""
        return self.blocks[handle].raw


def fake_kernel32(memory: Memory, allocates: bool = True,
                  locks: bool = True) -> SimpleNamespace:
    """Return a kernel32 that hands out memory, or refuses to.

    Args:
        memory: Where the memory that is handed out is kept.
        allocates: Whether memory is had at all.
        locks: Whether memory that was had can be written to.
    """
    return SimpleNamespace(
        GlobalAlloc=Function(memory.alloc if allocates else refuse),
        GlobalLock=Function(memory.lock if locks else refuse),
        GlobalUnlock=Function(succeed), GlobalFree=Function(refuse))


def given_back(_named: int, handle: int) -> int:
    """Answer as SetClipboardData does when it takes the memory."""
    return handle


def fake_user32(opens: bool = True, takes: bool = True) -> SimpleNamespace:
    """Return a user32 whose clipboard opens and takes, or refuses to.

    Args:
        opens: Whether the clipboard can be opened.
        takes: Whether the clipboard takes what it is given.
    """
    return SimpleNamespace(
        OpenClipboard=Function(succeed if opens else refuse),
        EmptyClipboard=Function(succeed), CloseClipboard=Function(succeed),
        SetClipboardData=Function(given_back if takes else refuse),
        RegisterClipboardFormatW=Function(lambda _name: HTML_ID))
