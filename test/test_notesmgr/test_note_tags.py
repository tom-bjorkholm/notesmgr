#! /usr/local/bin/python3
"""Tests for the tags that the pieces of a note are drawn with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Optional, Sequence
import pytest
from notesmgr.note_blocks import Block, BlockKind, Span, SpanStyle
from notesmgr.note_fonts import BODY_KEY, FontKey, font_tag
from notesmgr.note_tags import CODE_SPAN_TAG, GAP_TAG, HEADING_GAPS, \
    IMAGE_TAG, LINK_TAG, MAX_INDENT, RAW_KEY, STRIKE_TAG, NoteTags, \
    gap_lines, indent_tag, span_styles

START_SIZE = 12
"""The size that the note of these tests is drawn in at first."""

PARAGRAPH = Block(BlockKind.PARAGRAPH, (Span('words'),))
"""An ordinary piece of a note, at the left and unmarked."""

ITEM = Block(BlockKind.PARAGRAPH, (Span('words'),), 1, '• ')
"""An item of a list, which carries a bullet."""

HEADING = Block(BlockKind.HEADING2, (Span('words'),))
"""A heading, which is set off from the part above it."""


@pytest.fixture(name='area')
def fixture_area(top_window: tkinter.Toplevel) -> tkinter.Text:
    """Provide a text area of a hidden window to define tags in."""
    return tkinter.Text(top_window)


@pytest.fixture(name='tags')
def fixture_tags(area: tkinter.Text) -> NoteTags:
    """Provide the tags of a note drawn in a known size."""
    return NoteTags(area, START_SIZE)


@pytest.mark.parametrize('block,previous,expected', [
    (PARAGRAPH, None, 0),
    (HEADING, None, 0),
    (PARAGRAPH, PARAGRAPH, 1),
    (HEADING, PARAGRAPH, HEADING_GAPS),
    (HEADING, ITEM, HEADING_GAPS),
    (ITEM, PARAGRAPH, 1),
    (PARAGRAPH, ITEM, 1),
    (ITEM, ITEM, 0)])
def test_gap_lines(block: Block, previous: Optional[Block],
                   expected: int) -> None:
    """A heading is set off, the items of a list follow one another."""
    assert gap_lines(block, previous) == expected


@pytest.mark.parametrize('indent,prefix,expected', [
    (0, '', 'indent0'),
    (2, '', 'indent2'),
    (0, '• ', 'item0'),
    (3, '1. ', 'item3'),
    (MAX_INDENT, '', f'indent{MAX_INDENT}'),
    (MAX_INDENT + 5, '', f'indent{MAX_INDENT}'),
    (MAX_INDENT + 5, '• ', f'item{MAX_INDENT}')])
def test_indent_tag(indent: int, prefix: str, expected: str) -> None:
    """A piece is written where it belongs, a list item hanging out."""
    block = Block(BlockKind.PARAGRAPH, (Span('words'),), indent, prefix)
    assert indent_tag(block) == expected


@pytest.mark.parametrize('styles,expected', [
    (set(), ()),
    ({SpanStyle.BOLD}, ()),
    ({SpanStyle.ITALIC}, ()),
    ({SpanStyle.LINK}, (LINK_TAG,)),
    ({SpanStyle.CODE}, (CODE_SPAN_TAG,)),
    ({SpanStyle.STRIKE}, (STRIKE_TAG,)),
    ({SpanStyle.IMAGE}, (IMAGE_TAG,))])
def test_span_styles(styles: set[SpanStyle],
                     expected: tuple[str, ...]) -> None:
    """What is drawn on top of the font of a run of text is its own tag."""
    assert span_styles(Span('words', frozenset(styles))) == expected


def test_two_styles_at_once() -> None:
    """A run of text that is two things at once is drawn as both."""
    styles = frozenset({SpanStyle.LINK, SpanStyle.CODE})
    assert set(span_styles(Span('words', styles))) == {LINK_TAG,
                                                       CODE_SPAN_TAG}


def test_colour_tags_defined(tags: NoteTags) -> None:
    """The tags that colour a note are there as soon as it is drawn."""
    defined = set(tags.area.tag_names())
    assert {str(BlockKind.CODE), str(BlockKind.QUOTE), str(BlockKind.RULE),
            str(BlockKind.TABLE), CODE_SPAN_TAG, STRIKE_TAG, LINK_TAG,
            GAP_TAG} <= defined


def test_rule_is_not_wrapped(tags: NoteTags) -> None:
    """A line across the note and a table are not broken into lines."""
    for kind in (BlockKind.RULE, BlockKind.TABLE):
        assert str(tags.area.tag_cget(kind, 'wrap')) == 'none'


def test_raw_note_font(tags: NoteTags) -> None:
    """A note shown as it is written is drawn in the font of the area."""
    assert str(tags.area.cget('font')) == str(tags.fonts.font(RAW_KEY).name)


def test_font_tag_is_defined(tags: NoteTags) -> None:
    """A tag carrying a font is defined the first time it is asked for."""
    name = tags.font_tag_of(BlockKind.HEADING1, Span('words'))
    assert name == font_tag(FontKey(1.8, bold=True))
    assert name in tags.area.tag_names()
    assert str(tags.area.tag_cget(name, 'font'))


def test_font_tag_is_kept(tags: NoteTags) -> None:
    """A font that the note needs again is not defined a second time."""
    first = tags.font_tag_of(BlockKind.PARAGRAPH, Span('a'))
    assert tags.font_tag_of(BlockKind.PARAGRAPH, Span('b')) == first
    assert len(tags.made) == 1


def test_span_tags(tags: NoteTags) -> None:
    """A run of text carries its piece, its place, its font and its style."""
    span = Span('words', frozenset({SpanStyle.LINK}))
    given = tags.span_tags(BlockKind.QUOTE, span, 'indent1')
    assert given == (str(BlockKind.QUOTE), 'indent1',
                     font_tag(FontKey(italic=True)), LINK_TAG)


def margins(tags: NoteTags, name: str) -> tuple[int, int]:
    """Return how far a tag writes the first line and the rest."""
    return (int(tags.area.tag_cget(name, 'lmargin1')),
            int(tags.area.tag_cget(name, 'lmargin2')))


@pytest.mark.parametrize('depth', [0, 1, MAX_INDENT])
def test_indent_margins(tags: NoteTags, depth: int) -> None:
    """A piece is written as many steps from the left as it is deep."""
    first, rest = margins(tags, f'indent{depth}')
    assert first == rest == depth * tags.fonts.indent_step()


@pytest.mark.parametrize('depth', [0, 1, MAX_INDENT])
def test_item_margins(tags: NoteTags, depth: int) -> None:
    """A list item leaves room for its bullet on the lines after the first."""
    first, rest = margins(tags, f'item{depth}')
    assert first == depth * tags.fonts.indent_step()
    assert rest > first


def test_margins_follow_size(tags: NoteTags) -> None:
    """Making a note larger moves the indentation of a list with it."""
    before = margins(tags, 'indent2')
    tags.resize(START_SIZE * 2)
    assert margins(tags, 'indent2')[0] > before[0]


def test_gap_follows_the_size(tags: NoteTags) -> None:
    """The room between two pieces of a note follows the size as well."""
    gap = tags.fonts.font(FontKey(scale=0.4))
    before = int(gap.actual('size'))
    tags.resize(START_SIZE * 2)
    assert int(gap.actual('size')) > before


def test_zoom_and_back(tags: NoteTags) -> None:
    """A note zoomed away from where it began goes back to it."""
    assert tags.zoom(3) == START_SIZE + 3
    assert tags.zoom(-1) == START_SIZE + 2
    assert tags.normal_size() == START_SIZE


def all_tags(tags: NoteTags) -> Sequence[str]:
    """Return the names of every tag that the area knows of."""
    return [str(name) for name in tags.area.tag_names()]


def test_every_indent_defined(tags: NoteTags) -> None:
    """Every depth that a piece can be written at has its tags."""
    defined = set(all_tags(tags))
    for depth in range(MAX_INDENT + 1):
        assert {f'indent{depth}', f'item{depth}'} <= defined


def test_body_font_size(tags: NoteTags) -> None:
    """The font of the ordinary text of a note is the size it is drawn in."""
    assert int(tags.fonts.font(BODY_KEY).actual('size')) == START_SIZE
