#! /usr/local/bin/python3
"""Which file an image of a note names, and how large it is drawn."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

MAX_IMAGE_WIDTH = 900
"""Widest that an image of a note is drawn, in pixels.

An image wider than this is drawn smaller, so that a note holding a
screenshot of a whole screen can still be read in the panel.
"""


def is_remote(target: str) -> bool:
    """Return whether what an image of a note names is on the network.

    A scheme of a single letter is the drive of a path on Microsoft
    Windows rather than a scheme of a URL, which is the one case
    that tells a path from an address.

    Args:
        target: What the note names the image as.

    Returns:
        Whether that is an address rather than a file.
    """
    return len(urlparse(target).scheme) > 1


def image_path(folder: Optional[Path], target: str) -> Optional[Path]:
    """Return the file that an image of a note names, None for none.

    An image is looked for beside the note rather than in the folder
    that the program was started from, because that is where a note
    that names an image of its own keeps it. An image that is
    somewhere on the network is not fetched at all, so that reading
    a note never waits for anything.

    Args:
        folder: The folder that holds the note, None when the note
            is shown from nowhere in particular.
        target: What the note names the image as.

    Returns:
        The file to draw, None where the note names no file that can
        be drawn from where it stands.
    """
    if not target or is_remote(target):
        return None
    named = Path(target)
    if named.is_absolute():
        return named
    return None if folder is None else folder / named


def shrink_factor(width: int, limit: int = MAX_IMAGE_WIDTH) -> int:
    """Return by how much an image wider than the panel is drawn smaller.

    Args:
        width: How wide the image is, in pixels.
        limit: How wide it may be drawn, in pixels.

    Returns:
        The smallest whole factor that brings the image within the
        width, which is what Tk can shrink an image by, and one for
        an image that fits as it is.
    """
    if limit < 1 or width <= limit:
        return 1
    return -(-width // limit)
