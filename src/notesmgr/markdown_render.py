#! /usr/local/bin/python3
"""Turning the markdown of a note into the HTML it is drawn from."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import markdown
from markdown.inlinepatterns import SimpleTagInlineProcessor

EXTENSIONS = ['fenced_code', 'tables', 'sane_lists']
"""The markdown that a note may be written in, beyond the plain kind.

Fenced code is how a note holds a program or a command line, tables
are what a note of comparisons is written as, and sane lists keeps a
list from beginning in the middle of a paragraph.
"""

STRIKE_PATTERN = r'(~{2})(.+?)~{2}'
"""What a note marks text that is struck through with.

Two tildes around the text is how it is written everywhere it is
written, and Python-Markdown knows nothing of it, so notesmgr says
what it means rather than taking a dependency for one pattern.
"""

STRIKE_TAG = 'del'
"""The HTML that text struck through in a note is turned into."""

STRIKE_NAME = 'strike'
"""What the pattern of text struck through is registered as."""

STRIKE_PRIORITY = 65
"""Where the pattern belongs among the patterns of Python-Markdown.

Just above the emphasis patterns, which is where the marking of a
run of text belongs, and well below the ones for code and links,
so that two tildes inside them are left as the text they are.
"""

TAB_LENGTH = 2
"""How many spaces one step of indentation is taken to be.

Python-Markdown counts four, which leaves a list nested with two
spaces, as most editors and markdown linters write one, read as a
list of its own rather than as a nested one. Notes are written by
hand, so the smaller step is the one that draws what was meant.
"""


def markdown_converter() -> markdown.Markdown:
    """Return the converter that the HTML of a note is made with.

    Python-Markdown passes markup that a note holds straight through
    into its output, and a note is read rather than obeyed, so the
    two processors that let it through are taken out and the markup
    is drawn as the text that it is. Text struck through is added,
    which Python-Markdown knows nothing of on its own.
    """
    converter = markdown.Markdown(extensions=EXTENSIONS, tab_length=TAB_LENGTH)
    converter.preprocessors.deregister('html_block')
    converter.inlinePatterns.deregister('html')
    strike = SimpleTagInlineProcessor(STRIKE_PATTERN, STRIKE_TAG)
    patterns = converter.inlinePatterns
    patterns.register(strike, STRIKE_NAME, STRIKE_PRIORITY)
    return converter


def note_html(text: str) -> str:
    """Return the HTML of a note that is written in markdown.

    Args:
        text: The markdown of the note, as much of it as is shown.

    Returns:
        The HTML that the note is drawn from, and that a formatted
        copy of the note is taken from.
    """
    return markdown_converter().convert(text)
