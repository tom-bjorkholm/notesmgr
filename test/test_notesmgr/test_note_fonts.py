#! /usr/local/bin/python3
"""Tests for the fonts that a note is drawn with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import AbstractSet
import pytest
from notesmgr.note_blocks import BlockKind, SpanStyle
from notesmgr.note_fonts import BODY_KEY, HEADING_SCALES, MAX_SIZE, \
    MIN_SIZE, FontKey, NoteFonts, default_size, family_of, font_key, \
    font_tag, note_size

START_SIZE = 12
"""The size that the fonts of these tests start out at."""


@pytest.fixture(name='fonts')
def fixture_fonts(tk_root: tkinter.Tk) -> NoteFonts:
    """Provide fonts of a known size, so that a change is seen."""
    return NoteFonts(tk_root, START_SIZE)


@pytest.mark.parametrize('asked,expected', [
    (START_SIZE, START_SIZE),
    (MIN_SIZE, MIN_SIZE),
    (MAX_SIZE, MAX_SIZE),
    (MIN_SIZE - 1, MIN_SIZE),
    (MAX_SIZE + 1, MAX_SIZE),
    (0, MIN_SIZE),
    (-100, MIN_SIZE),
    (10000, MAX_SIZE)])
def test_note_size(asked: int, expected: int) -> None:
    """A size is kept within what a note can be read at."""
    assert note_size(asked) == expected


def test_default_size(tk_root: tkinter.Tk) -> None:
    """The size a note starts at is a size that Tk can be asked for."""
    assert MIN_SIZE <= default_size(tk_root) <= MAX_SIZE


def test_families_are_named(tk_root: tkinter.Tk) -> None:
    """The fonts of a note are the fonts that the system itself uses."""
    assert family_of('TkTextFont', tk_root)
    assert family_of('TkFixedFont', tk_root)


@pytest.mark.parametrize('kind,styles,expected', [
    (BlockKind.PARAGRAPH, set(), FontKey()),
    (BlockKind.PARAGRAPH, {SpanStyle.BOLD}, FontKey(bold=True)),
    (BlockKind.PARAGRAPH, {SpanStyle.ITALIC}, FontKey(italic=True)),
    (BlockKind.PARAGRAPH, {SpanStyle.BOLD, SpanStyle.ITALIC},
     FontKey(bold=True, italic=True)),
    (BlockKind.PARAGRAPH, {SpanStyle.CODE}, FontKey(fixed=True)),
    (BlockKind.PARAGRAPH, {SpanStyle.LINK}, FontKey()),
    (BlockKind.PARAGRAPH, {SpanStyle.STRIKE}, FontKey()),
    (BlockKind.CODE, set(), FontKey(fixed=True)),
    (BlockKind.TABLE, set(), FontKey(fixed=True)),
    (BlockKind.RULE, set(), FontKey(fixed=True)),
    (BlockKind.QUOTE, set(), FontKey(italic=True)),
    (BlockKind.QUOTE, {SpanStyle.BOLD}, FontKey(bold=True, italic=True)),
    (BlockKind.HEADING1, set(), FontKey(1.8, bold=True)),
    (BlockKind.HEADING6, set(), FontKey(1.0, bold=True)),
    (BlockKind.HEADING2, {SpanStyle.CODE},
     FontKey(1.5, fixed=True, bold=True))])
def test_font_key(kind: BlockKind, styles: AbstractSet[SpanStyle],
                  expected: FontKey) -> None:
    """A heading, a quote and code each bring their own font along."""
    assert font_key(kind, styles) == expected


def test_body_is_plain() -> None:
    """The ordinary text of a note is drawn with the plainest font."""
    assert font_key(BlockKind.PARAGRAPH) == BODY_KEY


def test_heading_sizes() -> None:
    """Every level of heading is drawn in a size of its own, and larger."""
    scales = list(HEADING_SCALES.values())
    assert scales == sorted(scales, reverse=True)
    assert min(scales) >= 1.0


def test_tags_are_apart() -> None:
    """Every font of a note has a tag of its own to be drawn with."""
    keys = [FontKey(), FontKey(fixed=True), FontKey(bold=True),
            FontKey(italic=True), FontKey(1.8, bold=True),
            FontKey(1.8, bold=True, italic=True)]
    assert len({font_tag(key) for key in keys}) == len(keys)


def test_font_is_made_once(fonts: NoteFonts) -> None:
    """A font that a note needs twice is made once and kept."""
    assert not fonts.fonts
    first = fonts.font(BODY_KEY)
    assert fonts.font(BODY_KEY) is first
    assert len(fonts.fonts) == 1


def test_font_of_a_key(fonts: NoteFonts) -> None:
    """A font is made as large, as heavy and as slanted as it is asked."""
    made = fonts.font(FontKey(2.0, fixed=True, bold=True, italic=True))
    assert int(made.actual('size')) == 2 * START_SIZE
    assert str(made.actual('weight')) == 'bold'
    assert str(made.actual('slant')) == 'italic'
    assert str(made.actual('family')) == fonts.fixed_family


def test_body_font_is_plain(fonts: NoteFonts) -> None:
    """The font of the ordinary text of a note is upright and light."""
    made = fonts.font(BODY_KEY)
    assert int(made.actual('size')) == START_SIZE
    assert str(made.actual('weight')) == 'normal'
    assert str(made.actual('slant')) == 'roman'
    assert str(made.actual('family')) == fonts.body_family


def test_resize_every_font(fonts: NoteFonts) -> None:
    """Changing the size changes every font that the note is drawn with."""
    body = fonts.font(BODY_KEY)
    heading = fonts.font(FontKey(2.0))
    assert fonts.resize(20) == 20
    assert int(body.actual('size')) == 20
    assert int(heading.actual('size')) == 40


def test_font_after_resize(fonts: NoteFonts) -> None:
    """A font that a note needs later is made in the size in use now."""
    fonts.resize(20)
    assert int(fonts.font(BODY_KEY).actual('size')) == 20


@pytest.mark.parametrize('steps,expected', [
    (1, START_SIZE + 1),
    (5, START_SIZE + 5),
    (-1, START_SIZE - 1),
    (-100, MIN_SIZE),
    (100, MAX_SIZE)])
def test_zoom(fonts: NoteFonts, steps: int, expected: int) -> None:
    """Zooming draws the note so many steps larger or smaller."""
    assert fonts.zoom(steps) == expected
    assert fonts.size == expected


def test_normal_size(fonts: NoteFonts) -> None:
    """Whatever the note was zoomed to, it goes back to where it began."""
    fonts.zoom(7)
    assert fonts.normal_size() == START_SIZE
    assert int(fonts.font(BODY_KEY).actual('size')) == START_SIZE


def test_normal_of_odd_start(tk_root: tkinter.Tk) -> None:
    """A note asked to start at no readable size starts at a readable one."""
    fonts = NoteFonts(tk_root, 0)
    assert fonts.size == MIN_SIZE
    assert fonts.normal_size() == MIN_SIZE


def test_scaled_is_never_gone(fonts: NoteFonts) -> None:
    """A font of a tiny part of the text is still a font to be seen."""
    fonts.resize(MIN_SIZE)
    assert fonts.scaled(FontKey(0.01)) == 1


def test_indent_step(fonts: NoteFonts) -> None:
    """One step of indentation is as wide as a few letters are."""
    step = fonts.indent_step()
    assert step > 0
    fonts.resize(MAX_SIZE)
    assert fonts.indent_step() > step
