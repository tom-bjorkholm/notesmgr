#! /usr/local/bin/python3
"""Tests for the pieces that a formatted note is drawn in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional, Sequence
import pytest
from notesmgr.note_blocks import Block, BlockKind, Span, SpanStyle, \
    html_blocks, item_prefix, markdown_blocks, squeezed, trimmed
from notesmgr.note_blocks import Container

HEADING_LEVELS = [(f'{"#" * level} Words', f'heading{level}')
                  for level in range(1, 7)]
"""Every level of heading, and the kind of piece it is drawn as."""


def text_of(block: Block) -> str:
    """Return the whole text of one piece of a note."""
    return ''.join(span.text for span in block.spans)


def texts(blocks: Sequence[Block]) -> list[str]:
    """Return the text of every piece of a note."""
    return [text_of(block) for block in blocks]


def kinds(blocks: Sequence[Block]) -> list[BlockKind]:
    """Return what every piece of a note is."""
    return [block.kind for block in blocks]


def styled(block: Block, style: SpanStyle) -> list[str]:
    """Return the text of every run of a piece that has a style."""
    return [span.text for span in block.spans if style in span.styles]


def only(blocks: Sequence[Block]) -> Block:
    """Return the one piece that a note of one piece is drawn in."""
    assert len(blocks) == 1
    return blocks[0]


@pytest.mark.parametrize('text', ['', '\n', '   \n\n  \n'])
def test_nothing_to_draw(text: str) -> None:
    """A note holding nothing at all is drawn in no pieces."""
    assert not markdown_blocks(text)


def test_a_paragraph() -> None:
    """A paragraph of a note is one piece, at the left and unmarked."""
    block = only(markdown_blocks('Just words.\n'))
    assert block == Block(BlockKind.PARAGRAPH, (Span('Just words.'),))


def test_breaks_are_blanks() -> None:
    """The line breaks a note was written with are blanks between words."""
    block = only(markdown_blocks('One line\nand another\nand a third\n'))
    assert text_of(block) == 'One line and another and a third'


def test_paragraphs_are_apart() -> None:
    """Two paragraphs of a note are two pieces of it."""
    blocks = markdown_blocks('First one.\n\nSecond one.\n')
    assert texts(blocks) == ['First one.', 'Second one.']
    assert kinds(blocks) == [BlockKind.PARAGRAPH] * 2


@pytest.mark.parametrize('text,kind', HEADING_LEVELS)
def test_heading_levels(text: str, kind: str) -> None:
    """A heading is drawn as the piece of its own level."""
    block = only(markdown_blocks(text))
    assert block.kind == kind
    assert text_of(block) == 'Words'


def test_hard_line_break() -> None:
    """A line break that the note asks for is drawn as a break."""
    block = only(markdown_blocks('Before  \nafter\n'))
    assert text_of(block) == 'Before\nafter'


@pytest.mark.parametrize('text,style,marked', [
    ('a **bold** word', SpanStyle.BOLD, ['bold']),
    ('a *slanted* word', SpanStyle.ITALIC, ['slanted']),
    ('a `code` word', SpanStyle.CODE, ['code']),
    ('a ~~gone~~ word', SpanStyle.STRIKE, ['gone']),
    ('a [linked](target) word', SpanStyle.LINK, ['linked']),
    ('***both***', SpanStyle.BOLD, ['both']),
    ('***both***', SpanStyle.ITALIC, ['both'])])
def test_inline_styles(text: str, style: SpanStyle, marked: list[str]) \
        -> None:
    """What a note says about a run of text is said of that run alone."""
    assert styled(only(markdown_blocks(text)), style) == marked


def test_link_target_is_kept() -> None:
    """Where a link leads is kept, which is what a copy of it needs."""
    block = only(markdown_blocks('[text](https://example.com/)'))
    links = [span for span in block.spans if SpanStyle.LINK in span.styles]
    assert [span.target for span in links] == ['https://example.com/']


def test_link_without_target() -> None:
    """A link that leads nowhere is still drawn as the text it is."""
    block = only(markdown_blocks('a [nowhere]() link'))
    assert styled(block, SpanStyle.LINK) == ['nowhere']
    assert text_of(block) == 'a nowhere link'


def test_html_is_text() -> None:
    """Markup that a note holds is drawn as the text that it is."""
    block = only(markdown_blocks('<b>not bold</b>'))
    assert text_of(block) == '<b>not bold</b>'
    assert block.spans[0].styles == frozenset()


def test_entity_is_the_letter() -> None:
    """An entity that a note holds is drawn as the letter it names."""
    block = only(markdown_blocks('&amp; and &#8212;'))
    assert text_of(block) == '& and —'


@pytest.mark.parametrize('text,prefixes', [
    ('- one\n- two\n', ['• ', '• ']),
    ('1. one\n2. two\n', ['1. ', '2. ']),
    ('3. one\n4. two\n', ['1. ', '2. '])])
def test_list_prefixes(text: str, prefixes: list[str]) -> None:
    """An item of a list carries the bullet or the number it is given."""
    assert [block.prefix for block in markdown_blocks(text)] == prefixes


def test_nested_list_depth() -> None:
    """A list nested in a list is drawn one step further from the left."""
    blocks = markdown_blocks('- one\n  - two\n    - three\n')
    assert [block.indent for block in blocks] == [1, 2, 3]
    assert [block.prefix for block in blocks] == ['• ', '◦ ', '▪ ']


def test_nested_numbering() -> None:
    """A list nested in a list is numbered on its own."""
    blocks = markdown_blocks('1. one\n  1. inner\n  2. inner\n2. two\n')
    assert [block.prefix for block in blocks] == ['1. ', '1. ', '2. ',
                                                  '2. ']


def test_item_of_no_list() -> None:
    """An item that is in no list at all carries no bullet."""
    assert item_prefix([]) == ''


def test_item_of_a_quote() -> None:
    """An item held by a quote rather than a list is given a bullet."""
    assert item_prefix([Container('blockquote')]) == '• '


def test_quoted_paragraph() -> None:
    """A quoted paragraph is drawn as a quote, one step from the left."""
    block = only(markdown_blocks('> quoted\n'))
    assert block.kind is BlockKind.QUOTE
    assert block.indent == 1


def test_quote_in_a_quote() -> None:
    """A quote inside a quote is drawn one step further from the left."""
    blocks = markdown_blocks('> outer\n>\n> > inner\n')
    assert kinds(blocks) == [BlockKind.QUOTE] * 2
    assert [block.indent for block in blocks] == [1, 2]


def test_list_in_a_quote() -> None:
    """A list inside a quote is quoted as well as being a list."""
    block = only(markdown_blocks('> - item\n'))
    assert block.kind is BlockKind.QUOTE
    assert block.prefix == '• '
    assert block.indent == 2


def test_code_is_kept_as_is() -> None:
    """A code block is drawn exactly as the note wrote it."""
    block = only(markdown_blocks('```\nif x:\n    y = 1\n```\n'))
    assert block == Block(BlockKind.CODE, (Span('if x:\n    y = 1'),))


def test_markdown_in_code() -> None:
    """A fence holding markdown is drawn as the code that it is."""
    block = only(markdown_blocks('```\n# Not a heading\n- Nor a list\n```\n'))
    assert block.kind is BlockKind.CODE
    assert text_of(block) == '# Not a heading\n- Nor a list'


def test_code_is_not_styled() -> None:
    """Nothing inside a code block is read as a style of the text."""
    block = only(markdown_blocks('```\nsee <b>this</b>\n```\n'))
    assert text_of(block) == 'see <b>this</b>'
    assert block.spans[0].styles == frozenset()


def test_indented_code() -> None:
    """A block indented by hand is drawn as code without the indent."""
    block = only(markdown_blocks('    four spaces in\n'))
    assert block.kind is BlockKind.CODE
    assert text_of(block) == 'four spaces in'


def test_empty_code_block() -> None:
    """A fence that holds nothing at all is drawn in no piece."""
    assert not markdown_blocks('```\n```\n')


def test_a_rule() -> None:
    """A line across the note is a piece of its own holding no text."""
    assert markdown_blocks('---\n') == (Block(BlockKind.RULE),)


def test_a_table() -> None:
    """A table is one piece, laid out in columns of text."""
    block = only(markdown_blocks('| a | b |\n| --- | --- |\n| 1 | 2 |\n'))
    assert block.kind is BlockKind.TABLE
    lines = text_of(block).split('\n')
    assert lines[0] == 'a │ b'
    assert lines[2] == '1 │ 2'


def test_table_missing_cell() -> None:
    """A row of a table that names too few cells is filled out."""
    block = only(markdown_blocks('| a | b |\n| --- | --- |\n| 1 |\n'))
    assert text_of(block).split('\n')[2] == '1 │'


def test_table_cell_of_words() -> None:
    """The line breaks inside a cell are blanks, as everywhere else."""
    block = only(markdown_blocks('| a |\n| --- |\n| one  two |\n'))
    assert text_of(block).split('\n')[2] == 'one two'


def test_image_is_named() -> None:
    """An image of a note is a run of text of its own, with its file."""
    block = only(markdown_blocks('![Some picture](file.png)'))
    span = block.spans[0]
    assert span == Span('Some picture', frozenset({SpanStyle.IMAGE}),
                        'file.png')


def test_image_without_words() -> None:
    """An image that the note says nothing about is still a run of text."""
    block = only(markdown_blocks('![](file.png)'))
    expected = Span('', frozenset({SpanStyle.IMAGE}), 'file.png')
    assert block.spans[0] == expected


def test_image_in_a_paragraph() -> None:
    """An image written in a line of prose stays where it is written."""
    block = only(markdown_blocks('before ![alt](file.png) after'))
    assert texts([block]) == ['before alt after']
    assert styled(block, SpanStyle.IMAGE) == ['alt']


@pytest.mark.parametrize('text,expected', [
    ('one two', 'one two'),
    ('one  two', 'one two'),
    ('one\ntwo', 'one two'),
    (' both ', ' both '),
    ('\n', ' ')])
def test_squeezed_blanks(text: str, expected: str) -> None:
    """Every stretch of blanks in a note is drawn as a single blank."""
    assert squeezed(text) == expected


@pytest.mark.parametrize('spans,expected', [
    ([], ()),
    ([Span(' ')], ()),
    ([Span(' a ')], (Span('a'),)),
    ([Span(' a '), Span(' b ')], (Span('a '), Span(' b'))),
    ([Span(''), Span('', frozenset(), 'file.png')],
     (Span('', frozenset(), 'file.png'),))])
def test_trimmed_spans(spans: list[Span], expected: tuple[Span, ...]) \
        -> None:
    """A piece of a note begins and ends with a word, not with a blank."""
    assert trimmed(spans) == expected


@pytest.mark.parametrize('html', [
    '', '<p>', '</p>', 'bare words', '<p>text',
    '<ul><li>item', '</ul></li>', '<table><tr><td>cell',
    '<blockquote>', '<pre><code>code'])
def test_odd_html(html: str) -> None:
    """HTML that ends in the middle is read as far as it goes."""
    assert isinstance(html_blocks(html), tuple)


def test_text_outside_a_piece() -> None:
    """Text that belongs to no piece of the note is drawn nowhere."""
    assert html_blocks('\n<ul>\n<li>item</li>\n</ul>\n') == (
        Block(BlockKind.PARAGRAPH, (Span('item'),), 1, '• '),)


def test_unclosed_paragraph() -> None:
    """A piece that the HTML never ends is drawn all the same."""
    assert html_blocks('<p>text') == (
        Block(BlockKind.PARAGRAPH, (Span('text'),)),)


@pytest.mark.parametrize('tag,style', [
    ('b', SpanStyle.BOLD), ('strong', SpanStyle.BOLD),
    ('i', SpanStyle.ITALIC), ('em', SpanStyle.ITALIC),
    ('s', SpanStyle.STRIKE), ('del', SpanStyle.STRIKE)])
def test_both_style_tags(tag: str, style: SpanStyle) -> None:
    """Either tag that HTML marks a run of text with is understood."""
    blocks = html_blocks(f'<p><{tag}>word</{tag}></p>')
    assert styled(only(blocks), style) == ['word']


def test_stray_end_tag() -> None:
    """An end of a style that began nowhere leaves the text as it is."""
    block = only(html_blocks('<p>a</em>b</p>'))
    assert text_of(block) == 'ab'


@pytest.mark.parametrize('deep,expected', [(3, 3), (12, 12)])
def test_deeply_nested(deep: int, expected: Optional[int]) -> None:
    """However deeply a list is nested, the depth is what it is.

    How far from the left that is drawn is the business of the area
    that draws it, which is where the depth is capped.
    """
    text = ''.join(f'{"  " * level}- item\n' for level in range(deep))
    assert markdown_blocks(text)[-1].indent == expected


@pytest.mark.parametrize('html', [
    '<br>', '<img src="file.png" alt="a picture">', '<td>cell</td>',
    '<tr>', '</td>', '</table>'])
def test_tag_outside_a_piece(html: str) -> None:
    """A tag that belongs inside a piece draws nothing outside of one."""
    assert not html_blocks(html)


def test_item_outside_a_list() -> None:
    """An item that no list holds is drawn as a paragraph, unmarked."""
    assert html_blocks('<li>stray</li>') == (
        Block(BlockKind.PARAGRAPH, (Span('stray'),)),)


@pytest.mark.parametrize('html', [
    '<table></table>', '<table><tr></tr></table>',
    '<table><tr><td></td></tr></table>'])
def test_empty_table(html: str) -> None:
    """A table holding no text at all is drawn in no piece."""
    assert not html_blocks(html)


def test_cell_outside_a_row() -> None:
    """A cell that no row of its table holds is drawn nowhere."""
    html = '<table><td>lost</td><tr><td>kept</td></tr></table>'
    assert texts(html_blocks(html)) == ['kept']


def test_table_in_a_quote() -> None:
    """A quoted table is drawn one step from the left, as a table."""
    block = only(markdown_blocks('> | a |\n> | --- |\n> | 1 |\n'))
    assert block.kind is BlockKind.TABLE
    assert block.indent == 1


def test_rule_in_a_quote() -> None:
    """A quoted line across the note is drawn one step from the left."""
    assert markdown_blocks('> ---\n') == (Block(BlockKind.RULE, indent=1),)


def test_text_after_a_table() -> None:
    """The piece after a table is read as it would be anywhere else."""
    blocks = markdown_blocks('| a |\n| --- |\n| 1 |\n\nAfter.\n')
    assert kinds(blocks) == [BlockKind.TABLE, BlockKind.PARAGRAPH]
    assert texts(blocks)[1] == 'After.'
