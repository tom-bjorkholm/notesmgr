#! /usr/local/bin/python3
"""The user guide of notesmgr, as the Help menu shows it.

The user guide is the README that PyPI.org shows, which every
installed notesmgr carries as the long description of its package,
so the guide shown is always the one of the version that is run.
The guide is cut into sections by its headings, as markdown is.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from importlib.metadata import PackageNotFoundError, metadata
from typing import Mapping, Sequence
from notesmgr.errors import NotesmgrError
from notesmgr.note_blocks import HEADINGS, Block, BlockKind, \
    markdown_blocks
from notesmgr.version_info import MAIN_PACKAGE

LEVELS: Mapping[BlockKind, int] = {
    kind: level for level, kind in enumerate(HEADINGS.values(), start=1)}
"""The level of each kind of heading, 1 for the outermost."""

TEST_SUMMARY = 'Test summary'
"""Heading of the build report at the end of the README.

It tells how notesmgr was tested, which says nothing to a user.
"""

SHORTCUTS = 'Buttons and keyboard shortcuts'
"""Heading of the section of the guide that lists the shortcuts."""

NO_GUIDE = 'The user guide cannot be shown, as notesmgr is not ' \
    'installed\nas a package, which is where the guide is kept.'
"""What is said when the installed package carries no guide."""

NO_SECTION = 'The user guide has no section called "{title}".'
"""What is said when the guide has lost a section it is asked for."""


def readme_text() -> str:
    """Return the markdown of the README of the installed notesmgr.

    Raises:
        NotesmgrError: notesmgr is not installed, or its package
            carries no README.
    """
    try:
        text = metadata(MAIN_PACKAGE).json.get('description', '')
    except PackageNotFoundError as error:
        raise NotesmgrError(NO_GUIDE) from error
    if not isinstance(text, str) or not text.strip():
        raise NotesmgrError(NO_GUIDE)
    return text


def heading_level(block: Block) -> int:
    """Return the level of a heading, 0 for a piece that is none."""
    return LEVELS.get(block.kind, 0)


def block_text(block: Block) -> str:
    """Return the text that a piece of a note says, without styles."""
    return ''.join(span.text for span in block.spans)


def section_slice(blocks: Sequence[Block], title: str) -> slice:
    """Return where the section under a heading is among the pieces.

    A section starts with the first heading that says the title and
    ends before the next heading that is as high or higher, which
    leaves its subsections inside it.

    Args:
        blocks: The pieces of a markdown text, in order.
        title: What the heading of the section says.

    Returns:
        The slice of the pieces that the section is, heading
        included, and an empty slice when no heading says the title.
    """
    starts = [index for index, block in enumerate(blocks)
              if heading_level(block) and block_text(block) == title]
    if not starts:
        return slice(0, 0)
    start = starts[0]
    level = heading_level(blocks[start])
    ends = [index for index in range(start + 1, len(blocks))
            if 0 < heading_level(blocks[index]) <= level]
    return slice(start, ends[0] if ends else len(blocks))


def guide_blocks(text: str) -> tuple[Block, ...]:
    """Return the whole user guide, without the test summary.

    Args:
        text: The markdown of the README.

    Returns:
        The pieces that the guide is drawn in.
    """
    blocks = markdown_blocks(text)
    summary = section_slice(blocks, TEST_SUMMARY)
    return blocks[:summary.start] + blocks[summary.stop:]


def shortcut_blocks(text: str) -> tuple[Block, ...]:
    """Return the section of the user guide that lists the shortcuts.

    Args:
        text: The markdown of the README.

    Returns:
        The pieces that the section is drawn in, heading included.

    Raises:
        NotesmgrError: The README has no such section.
    """
    blocks = markdown_blocks(text)
    section = blocks[section_slice(blocks, SHORTCUTS)]
    if not section:
        raise NotesmgrError(NO_SECTION.format(title=SHORTCUTS))
    return section
