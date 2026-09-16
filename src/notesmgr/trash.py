#! /usr/local/bin/python3
"""Moving what notesmgr takes away to the trash of the system."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from send2trash import send2trash
from notesmgr.errors import NotesmgrError


def send_to_trash(path: Path, message: str) -> None:
    """Move a file or a folder to the trash of the operating system.

    Nothing that notesmgr takes away is deleted outright, so that
    anything taken away by mistake can be taken back out of the
    trash again.

    Args:
        path: The file or folder that is to be moved to the trash.
        message: What to tell the user when it cannot be, holding a
            {path} and a {reason} to be filled in.

    Raises:
        NotesmgrError: The trash did not take it.
    """
    try:
        send2trash(path)
    except OSError as error:
        told = message.format(path=path, reason=error)
        raise NotesmgrError(told) from error
