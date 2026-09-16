#! /usr/local/bin/python3
"""Tests for the font that the explorer tree is drawn with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from tkinter import ttk
import pytest
from notesmgr.explorer_font import ROW_PADDING, STYLE_KIND, TreeFont
from notesmgr.note_fonts import MAX_SIZE, MIN_SIZE


@pytest.fixture(name='tree_font')
def fixture_tree_font(top_window: tkinter.Toplevel) -> TreeFont:
    """Provide the font and the style of one tree in a hidden window."""
    return TreeFont(top_window)


def looked_up(tree_font: TreeFont, option: str) -> str:
    """Return what the style of the tree says about one of its options."""
    return str(tree_font.style.lookup(tree_font.name, option))


def test_style_is_a_tree(tree_font: TreeFont) -> None:
    """The style is one that a tree can be drawn with, and no other."""
    assert tree_font.name.endswith(f'.{STYLE_KIND}')


def test_style_of_its_own(top_window: tkinter.Toplevel,
                          tree_font: TreeFont) -> None:
    """Every tree has a style of its own, to be sized on its own."""
    assert TreeFont(top_window).name != tree_font.name


def test_style_holds_font(tree_font: TreeFont) -> None:
    """The tree is drawn with the font that was made for it."""
    assert looked_up(tree_font, 'font') == str(tree_font.font)


def test_rows_follow_font(tree_font: TreeFont) -> None:
    """A row is as high as the font needs, and a little more."""
    metrics = int(tree_font.font.metrics('linespace'))
    assert looked_up(tree_font, 'rowheight') == str(metrics + ROW_PADDING)


def test_larger_rows(tree_font: TreeFont) -> None:
    """A tree drawn larger is given rows that its names fit into."""
    before = int(looked_up(tree_font, 'rowheight'))
    tree_font.zoom(8)
    assert int(looked_up(tree_font, 'rowheight')) > before


def test_zoom_and_back(tree_font: TreeFont) -> None:
    """A tree is drawn larger and smaller, and back as it started."""
    started = tree_font.size
    assert tree_font.zoom(2) == started + 2
    assert tree_font.zoom(-3) == started - 1
    assert tree_font.normal_size() == started


def test_font_is_resized(tree_font: TreeFont) -> None:
    """The font itself is resized, so the tree needs no new style."""
    tree_font.zoom(4)
    assert int(tree_font.font.cget('size')) == tree_font.size


@pytest.mark.parametrize('size,expected', [(0, MIN_SIZE), (400, MAX_SIZE)])
def test_size_kept_readable(tree_font: TreeFont, size: int,
                            expected: int) -> None:
    """However large or small a tree is asked for, it can be read."""
    assert tree_font.resize(size) == expected


def test_tree_takes_the_style(top_window: tkinter.Toplevel,
                              tree_font: TreeFont) -> None:
    """A tree that is given the style is drawn with the font of it."""
    tree = ttk.Treeview(top_window, style=tree_font.name)
    assert str(tree.cget('style')) == tree_font.name
