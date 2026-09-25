#! /usr/local/bin/python3
"""The pieces that a formatted note is drawn in, read from its HTML.

Everything about a note that has a right answer is settled here: how
deeply a piece of it is nested, what bullet or number a list item
carries, which runs of text are bold or code or a link, and how the
cells of a table line up. Drawing the note is then a matter of
writing text with tags and nothing else, and all of this is tested
without a window.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import re
from dataclasses import dataclass, field
from enum import StrEnum
from html.parser import HTMLParser
from textwrap import dedent
from typing import Mapping, NamedTuple, Optional, Sequence
from notesmgr.markdown_render import note_html
from notesmgr.note_table import Align, cell_align, table_text


class SpanStyle(StrEnum):
    """What is said about one run of text inside a piece of a note."""

    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    STRIKE = 'strike'
    LINK = 'link'
    IMAGE = 'image'


class BlockKind(StrEnum):
    """What one piece of a note is, which is how it is drawn."""

    PARAGRAPH = 'paragraph'
    HEADING1 = 'heading1'
    HEADING2 = 'heading2'
    HEADING3 = 'heading3'
    HEADING4 = 'heading4'
    HEADING5 = 'heading5'
    HEADING6 = 'heading6'
    CODE = 'code'
    QUOTE = 'quote'
    RULE = 'rule'
    TABLE = 'table'


class Span(NamedTuple):
    """One run of text of a piece of a note, and what is said about it.

    The target is where a link leads and which file an image is in,
    and is empty for a run of text that is neither of those.
    """

    text: str
    styles: frozenset[SpanStyle] = frozenset()
    target: str = ''


class Block(NamedTuple):
    """One piece of a note: a paragraph, a heading, a list item.

    The indent is how many steps from the left the piece is written,
    which is how deeply it is nested in lists and block quotes. The
    prefix is the bullet or the number of a list item, and is empty
    for every other kind of piece. A line across the note is a piece
    holding no text at all.
    """

    kind: BlockKind
    spans: tuple[Span, ...] = ()
    indent: int = 0
    prefix: str = ''


HEADINGS: Mapping[str, BlockKind] = {
    'h1': BlockKind.HEADING1, 'h2': BlockKind.HEADING2,
    'h3': BlockKind.HEADING3, 'h4': BlockKind.HEADING4,
    'h5': BlockKind.HEADING5, 'h6': BlockKind.HEADING6}
"""The heading of each level, as the HTML of a note names them."""

STYLES: Mapping[str, SpanStyle] = {
    'strong': SpanStyle.BOLD, 'b': SpanStyle.BOLD,
    'em': SpanStyle.ITALIC, 'i': SpanStyle.ITALIC,
    'code': SpanStyle.CODE, 'del': SpanStyle.STRIKE,
    's': SpanStyle.STRIKE}
"""What each tag of the HTML says about the text inside it."""

CONTAINERS = ('ul', 'ol', 'blockquote')
"""The tags that hold pieces of a note inside themselves."""

TEXT_TAGS = ('p', 'li')
"""The tags that hold the text of one piece of a note."""

TABLE_TAGS = ('table', 'tr', 'th', 'td')
"""The tags of a table that say something about its cells."""

CELL_TAGS = ('th', 'td')
"""The tags that hold one cell of a table."""

BULLETS = ('•', '◦', '▪')
"""What the items of a list are marked with, by depth of nesting."""

BLANKS = re.compile(r'\s+')
"""What is written as one blank, the line breaks of a note included."""


def squeezed(text: str) -> str:
    """Return a run of text with every stretch of blanks made one.

    The HTML of a note holds the line breaks that the note was
    written with. They are blanks between words rather than breaks
    to be drawn, because the panel breaks the lines where the window
    is wide enough for them to be broken.
    """
    return BLANKS.sub(' ', text)


def kept(spans: Sequence[Span]) -> list[Span]:
    """Return the runs of text that there is anything to draw for."""
    return [span for span in spans if span.text or span.target]


def trimmed(spans: Sequence[Span]) -> tuple[Span, ...]:
    """Return the runs of text without the blanks at either end.

    A piece of a note begins and ends with a word rather than with
    the line break that the note was written with.
    """
    inside = kept(spans)
    if not inside:
        return ()
    first = inside[0]
    inside[0] = Span(first.text.lstrip(), first.styles, first.target)
    last = inside[-1]
    inside[-1] = Span(last.text.rstrip(), last.styles, last.target)
    return tuple(kept(inside))


@dataclass
class Container:
    """One list or block quote that is open, and how far it has come."""

    tag: str
    items: int = 0


@dataclass
class OpenBlock:
    """The piece of a note that is being read, as far as it is read."""

    kind: BlockKind = BlockKind.PARAGRAPH
    spans: list[Span] = field(default_factory=list)
    indent: int = 0
    prefix: str = ''
    writing: bool = False


@dataclass
class OpenStyles:
    """What is said about the run of text that is being read."""

    styles: list[SpanStyle] = field(default_factory=list)
    target: str = ''


@dataclass
class TableReader:
    """The cells of a table of a note, as far as they are read.

    The headings are counted rather than kept apart, because they
    are the first rows of the table and the only thing that being a
    heading changes is the line that is drawn under them.
    """

    rows: list[list[str]] = field(default_factory=list)
    aligns: list[Align] = field(default_factory=list)
    headings: int = 0
    cell: Optional[list[str]] = None

    def start_row(self) -> None:
        """Begin another row of the table."""
        self.rows.append([])

    def start_cell(self, style: str, heading: bool) -> None:
        """Begin another cell of the row that is being read.

        Args:
            style: The style attribute of the cell, which is where
                the markdown table said how the column lines up.
            heading: Whether the cell is a heading of its column.
        """
        self.cell = []
        if len(self.rows) == 1:
            self.aligns.append(cell_align(style))
        if heading:
            self.headings = len(self.rows)

    def add_text(self, text: str) -> None:
        """Take a run of text that belongs to the cell being read."""
        if self.cell is not None:
            self.cell.append(text)

    def end_cell(self) -> None:
        """Put the cell that was read at the end of its row."""
        if self.cell is not None and self.rows:
            self.rows[-1].append(squeezed(''.join(self.cell)).strip())
        self.cell = None

    def text(self) -> str:
        """Return the table written in columns of monospaced text."""
        return table_text(self.rows, self.aligns, self.headings)


def item_prefix(containers: Sequence[Container]) -> str:
    """Return the bullet or the number that a list item carries.

    An ordered list numbers its items as it goes, and an unordered
    one marks them with a bullet that says how deeply the list is
    nested, so that a nested list is told from the one holding it
    even where the indentation is easy to miss.
    """
    if not containers:
        return ''
    holder = containers[-1]
    if holder.tag == 'ol':
        return f'{holder.items}. '
    depth = sum(1 for item in containers if item.tag == 'ul')
    return f'{BULLETS[(max(depth, 1) - 1) % len(BULLETS)]} '


class NoteParser(HTMLParser):
    """Reads the HTML of a note into the pieces that it is drawn in."""

    def __init__(self) -> None:
        """Get ready to read HTML, no piece of it having been read."""
        super().__init__(convert_charrefs=True)
        self.blocks: list[Block] = []
        self.containers: list[Container] = []
        self.block = OpenBlock()
        self.inline = OpenStyles()
        self.table: Optional[TableReader] = None
        self.in_code = False

    def note_blocks(self) -> tuple[Block, ...]:
        """Return the pieces of the note, all of it having been read."""
        self._flush()
        return tuple(self.blocks)

    def handle_starttag(self, tag: str,
                        attrs: list[tuple[str, Optional[str]]]) -> None:
        """Begin what a tag begins, ignoring one that begins nothing."""
        if tag in HEADINGS:
            self._open_block(HEADINGS[tag])
        elif tag in STYLES:
            self._open_style(STYLES[tag])
        elif tag in CONTAINERS:
            self._open_container(tag)
        elif tag in TABLE_TAGS:
            self._open_table_tag(tag, dict(attrs))
        else:
            self._open_other(tag, dict(attrs))

    def handle_endtag(self, tag: str) -> None:
        """End what a tag ends, ignoring one that ends nothing."""
        if tag in HEADINGS or tag in TEXT_TAGS:
            self._flush()
        elif tag in STYLES:
            self._close_style(STYLES[tag])
        elif tag in CONTAINERS:
            self._close_container()
        elif tag in TABLE_TAGS:
            self._close_table_tag(tag)
        elif tag == 'pre':
            self._close_code()
        elif tag == 'a':
            self._close_link()

    def handle_data(self, data: str) -> None:
        """Take a run of text of whatever is being read."""
        if self.table is not None:
            self.table.add_text(data)
        else:
            self._add_text(data)

    def _open_other(self, tag: str,
                    attrs: Mapping[str, Optional[str]]) -> None:
        """Begin one of the tags that stands on its own."""
        if tag == 'p':
            self._open_block(self._text_kind())
        elif tag == 'li':
            self._open_item()
        elif tag == 'pre':
            self._open_code()
        elif tag == 'hr':
            self._add_rule()
        elif tag == 'br':
            self._add_break()
        elif tag == 'a':
            self._open_link(attrs.get('href') or '')
        elif tag == 'img':
            self._add_image(attrs)

    def _depth(self) -> int:
        """Return how many lists and quotes what is read is inside."""
        return len(self.containers)

    def _text_kind(self) -> BlockKind:
        """Return whether text now read is quoted or an ordinary piece."""
        if any(item.tag == 'blockquote' for item in self.containers):
            return BlockKind.QUOTE
        return BlockKind.PARAGRAPH

    def _open_block(self, kind: BlockKind) -> None:
        """Begin another piece of the note, at the depth it is read at."""
        self._flush()
        self.block.kind = kind
        self.block.indent = self._depth()
        self.block.writing = True

    def _block_spans(self) -> tuple[Span, ...]:
        """Return the runs of text of the piece that was read.

        The text of a code block is kept exactly as it is written,
        while a paragraph loses the blanks at either end of it.
        """
        if self.block.kind is BlockKind.CODE:
            return tuple(kept(self.block.spans))
        return trimmed(self.block.spans)

    def _flush(self) -> None:
        """Put the piece that was read among the pieces of the note."""
        spans = self._block_spans()
        if spans:
            piece = self.block
            self.blocks.append(Block(piece.kind, spans, piece.indent,
                                     piece.prefix))
            self.block.prefix = ''
        self.block.spans = []
        self.block.writing = False

    def _open_container(self, tag: str) -> None:
        """Begin a list or a block quote, which holds pieces of its own."""
        self._flush()
        self.containers.append(Container(tag))

    def _close_container(self) -> None:
        """End a list or a block quote, ignoring an end of neither."""
        self._flush()
        if self.containers:
            self.containers.pop()

    def _open_item(self) -> None:
        """Begin a list item, with the bullet or the number it carries."""
        if self.containers:
            self.containers[-1].items += 1
        self._open_block(self._text_kind())
        self.block.prefix = item_prefix(self.containers)

    def _open_code(self) -> None:
        """Begin a code block, whose text is taken as it is written."""
        self._open_block(BlockKind.CODE)
        self.in_code = True

    def _close_code(self) -> None:
        """Put a code block among the pieces, without its indentation.

        A code block that is nested is written indented in the note,
        and that indentation is taken off so that the code stands
        where the piece holding it stands.
        """
        text = ''.join(span.text for span in self.block.spans)
        self.block.spans = [Span(dedent(text).strip('\n'))]
        self.in_code = False
        self._flush()

    def _open_style(self, style: SpanStyle) -> None:
        """Begin what is said about the run of text that follows.

        Inside a code block nothing is said about the text, because
        the tags of the HTML are the text of the note there.
        """
        if not self.in_code:
            self.inline.styles.append(style)

    def _close_style(self, style: SpanStyle) -> None:
        """End what was said, ignoring an end of what was not said."""
        if style in self.inline.styles:
            self.inline.styles.remove(style)

    def _open_link(self, target: str) -> None:
        """Begin a link, whose text is drawn as leading somewhere."""
        self._open_style(SpanStyle.LINK)
        self.inline.target = target

    def _close_link(self) -> None:
        """End a link, so that what follows is ordinary text again."""
        self._close_style(SpanStyle.LINK)
        self.inline.target = ''

    def _add_text(self, text: str) -> None:
        """Take a run of text of the piece being read, if one is open."""
        if not self.block.writing:
            return
        self.block.spans.append(self._span(self._read(text)))

    def _read(self, text: str) -> str:
        """Return a run of text as it belongs in the piece being read.

        Inside a code block the text is what the note holds, and
        everywhere else every stretch of blanks is one blank. The
        blanks after a line break that the note asked for are
        dropped, because the next line begins with its first word.
        """
        if self.in_code:
            return text
        blanked = squeezed(text)
        return blanked.lstrip() if self._after_break() else blanked

    def _after_break(self) -> bool:
        """Return whether a line break was the last thing read."""
        return bool(self.block.spans) \
            and self.block.spans[-1].text.endswith('\n')

    def _span(self, text: str, target: str = '') -> Span:
        """Return a run of text with what is said about it now."""
        return Span(text, frozenset(self.inline.styles),
                    target or self.inline.target)

    def _add_break(self) -> None:
        """Take a line break that the note asks to have drawn."""
        if self.block.writing:
            self.block.spans.append(self._span('\n'))

    def _add_image(self, attrs: Mapping[str, Optional[str]]) -> None:
        """Take an image of the note as a run of text of its own."""
        if not self.block.writing:
            return
        span = self._span(attrs.get('alt') or '', attrs.get('src') or '')
        styles = frozenset(span.styles | {SpanStyle.IMAGE})
        self.block.spans.append(Span(span.text, styles, span.target))

    def _add_rule(self) -> None:
        """Put a line across the note among the pieces of it."""
        self._flush()
        self.blocks.append(Block(BlockKind.RULE, indent=self._depth()))

    def _open_table_tag(self, tag: str,
                        attrs: Mapping[str, Optional[str]]) -> None:
        """Begin a table, a row of it, or a cell of a row of it."""
        if tag == 'table':
            self._open_table()
        elif self.table is None:
            return
        elif tag == 'tr':
            self.table.start_row()
        else:
            self.table.start_cell(attrs.get('style') or '', tag == 'th')

    def _close_table_tag(self, tag: str) -> None:
        """End a table or a cell of it, a row needing no ending."""
        if self.table is None:
            return
        if tag == 'table':
            self._close_table(self.table)
        elif tag in CELL_TAGS:
            self.table.end_cell()

    def _open_table(self) -> None:
        """Begin a table, which is read on its own and drawn as text."""
        self._flush()
        self.table = TableReader()

    def _close_table(self, table: TableReader) -> None:
        """Put the table that was read among the pieces of the note."""
        text = table.text()
        self.table = None
        if text:
            self.blocks.append(Block(BlockKind.TABLE, (Span(text),),
                                     self._depth()))


def html_blocks(html: str) -> tuple[Block, ...]:
    """Return the pieces that the HTML of a note is drawn in.

    Args:
        html: The HTML of the note, as the markdown of it gave.

    Returns:
        Every piece of the note, in the order it is drawn in.
    """
    parser = NoteParser()
    parser.feed(html)
    parser.close()
    return parser.note_blocks()


def markdown_blocks(text: str) -> tuple[Block, ...]:
    """Return the pieces that a note written in markdown is drawn in.

    Args:
        text: The markdown of the note, as much of it as is shown.

    Returns:
        Every piece of the note, in the order it is drawn in.
    """
    return html_blocks(note_html(text))
