#! /usr/local/bin/python3
"""Tests for turning the markdown of a note into HTML."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import pytest
from notesmgr.markdown_render import EXTENSIONS, TAB_LENGTH, note_html

NESTED = '- outer\n  - inner\n'
"""A list nested with two spaces, as a linter asks it to be written."""


def test_extensions_asked_for() -> None:
    """The markdown beyond the plain kind is named in one place."""
    assert EXTENSIONS == ['fenced_code', 'tables', 'sane_lists']


@pytest.mark.parametrize('text,expected', [
    ('', ''),
    ('plain words', '<p>plain words</p>'),
    ('# A heading', '<h1>A heading</h1>'),
    ('###### Level six', '<h6>Level six</h6>'),
    ('A *word* in **bold**',
     '<p>A <em>word</em> in <strong>bold</strong></p>'),
    ('`code`', '<p><code>code</code></p>'),
    ('---', '<hr />'),
    ('[text](target)', '<p><a href="target">text</a></p>'),
    ('![alt](picture.png)',
     '<p><img alt="alt" src="picture.png" /></p>')])
def test_html_of_markdown(text: str, expected: str) -> None:
    """The markdown of a note becomes the HTML it is drawn from."""
    assert note_html(text) == expected


def test_fenced_code() -> None:
    """A fence becomes a code block, whatever it holds."""
    html = note_html('```python\n# not a heading\n```')
    assert '<pre><code class="language-python"># not a heading\n' in html


def test_table_becomes_table() -> None:
    """A markdown table becomes an HTML table with its alignment."""
    html = note_html('| a | b |\n| --- | ---: |\n| 1 | 2 |')
    assert '<table>' in html
    assert '<th>a</th>' in html
    assert 'text-align: right' in html


def test_two_space_nesting() -> None:
    """A list nested with two spaces is read as a nested list.

    Python-Markdown counts four spaces to a step unless it is told
    otherwise, which is what the tab length of two is for.
    """
    assert TAB_LENGTH == 2
    assert note_html(NESTED).count('<ul>') == 2


@pytest.mark.parametrize('text,expected', [
    ('<b>bold</b>', '<p>&lt;b&gt;bold&lt;/b&gt;</p>'),
    ("<script>alert('no')</script>",
     "<p>&lt;script&gt;alert('no')&lt;/script&gt;</p>"),
    ('<div>\n\nA block\n\n</div>',
     '<p>&lt;div&gt;</p>\n<p>A block</p>\n<p>&lt;/div&gt;</p>')])
def test_html_is_text(text: str, expected: str) -> None:
    """Markup that a note holds is drawn as the text that it is."""
    assert note_html(text) == expected


def test_entity_is_kept() -> None:
    """An entity written by hand in a note is left as the entity.

    The HTML carries it on to whatever reads the HTML, which is the
    note area, where it is read as the character that it names.
    """
    assert note_html('&amp; and &#8212;') == '<p>&amp; and &#8212;</p>'


@pytest.mark.parametrize('text,expected', [
    ('~~gone~~', '<p><del>gone</del></p>'),
    ('a ~~b~~ c', '<p>a <del>b</del> c</p>'),
    ('~~over\ntwo lines~~', '<p><del>over\ntwo lines</del></p>'),
    ('`~~kept~~`', '<p><code>~~kept~~</code></p>'),
    ('one ~ tilde', '<p>one ~ tilde</p>'),
    ('x~~y', '<p>x~~y</p>')])
def test_struck_through(text: str, expected: str) -> None:
    """Two tildes around text strike it through, and one does not."""
    assert note_html(text) == expected


def test_converter_is_fresh() -> None:
    """The same note gives the same HTML however often it is shown.

    A converter keeps what it read of a note, the targets of its
    reference links among it, so every conversion is given one of
    its own rather than the leavings of the note shown before.
    """
    first = note_html('[a][ref]\n\n[ref]: target\n')
    assert note_html('[a][ref]\n') == '<p>[a][ref]</p>'
    assert note_html('[a][ref]\n\n[ref]: target\n') == first
