#! /usr/local/bin/python3
"""Tests for the area of the main window that a note is read in."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
import pytest
from notesmgr.note_blocks import Block, BlockKind, Span
from notesmgr.note_tags import GAP_TAG, LINK_TAG, STRIKE_TAG
from notesmgr.note_text import NoteText
from notesmgr.note_view import MISSING_ALT, NoteView

WARNING = 'Something about this note is worth saying.'
"""A warning that these tests show above a note."""

PICTURE = bytes.fromhex(
    '89504e470d0a1a0a0000000d494844520000000100000001080600000'
    '01f15c4890000000a49444154789c6300010000050001'
    '0d0a2db40000000049454e44ae426082')
"""A picture of one dot, as small a PNG file as there is."""


@pytest.fixture(name='view')
def fixture_view(top_window: tkinter.Toplevel) -> NoteView:
    """Provide a note area in a hidden window, showing nothing yet."""
    return NoteView(top_window)


@pytest.fixture(name='picture')
def fixture_picture(tmp_path: Path) -> Path:
    """Provide a picture beside a note, of a kind that Tk can draw."""
    path = tmp_path / 'dot.png'
    path.write_bytes(PICTURE)
    return path


def test_empty_at_first(view: NoteView) -> None:
    """An area that was shown nothing shows nothing and warns of nothing."""
    assert view.area_text() == ''
    assert not view.warning_shown()


def test_cannot_be_typed_in(view: NoteView) -> None:
    """The note is shown to be read, and is edited in an editor."""
    assert str(view.area.cget('state')) == 'disabled'


@pytest.mark.parametrize('text', ['', 'One line\n', 'No end of line',
                                  'Two\nlines\n', 'Å i Ö and 😀\n'])
def test_text_is_shown(view: NoteView, text: str) -> None:
    """A note is shown as it was read, to the last line ending."""
    view.show(NoteText(text))
    assert view.area_text() == text


def test_no_warning_for_none(view: NoteView) -> None:
    """A note with nothing wrong with it is shown without a warning."""
    view.show(NoteText('the text\n'))
    assert not view.warning_shown()


def test_warning_is_shown(view: NoteView) -> None:
    """A note that has something to warn about says so above itself."""
    view.show(NoteText('the text\n', WARNING))
    assert view.warning_shown()
    assert str(view.warning.cget('text')) == WARNING


def test_warning_goes_away(view: NoteView) -> None:
    """A note without a warning after one leaves no warning behind."""
    view.show(NoteText('', WARNING))
    view.show(NoteText('another note\n'))
    assert not view.warning_shown()
    assert view.area_text() == 'another note\n'


def test_shown_note_is_kept(view: NoteView) -> None:
    """The area knows the note it was given, warning and all."""
    note = NoteText('the text\n', WARNING)
    view.show(note)
    assert view.shown_note() == note


def test_showing_again(view: NoteView) -> None:
    """A note shown after another replaces it rather than following it."""
    view.show(NoteText('first\n'))
    view.show(NoteText('second\n'))
    assert view.area_text() == 'second\n'


def tags_at(view: NoteView, place: str) -> set[str]:
    """Return the tags that the area draws one place with."""
    return {str(name) for name in view.area.tag_names(place)}


def line_of(view: NoteView, number: int) -> str:
    """Return one line of what the area shows, without its ending."""
    return str(view.area.get(f'{number}.0', f'{number}.end'))


@pytest.mark.parametrize('text', ['plain words\n', '# not a heading\n',
                                  '- not a list\n', '', 'a\n\nb\n'])
def test_raw_is_untouched(view: NoteView, text: str) -> None:
    """A note that is no markdown is shown exactly as it is written."""
    view.show(NoteText(text))
    assert view.area_text() == text


def test_formatted_paragraph(view: NoteView) -> None:
    """A paragraph of a markdown note is shown as the paragraph it is."""
    view.show(NoteText('Just words.\n'), formatted=True)
    assert view.area_text() == 'Just words.\n'
    assert str(BlockKind.PARAGRAPH) in tags_at(view, '1.0')


def test_heading_is_marked(view: NoteView) -> None:
    """A heading is shown with the tags of a heading of its level."""
    view.show(NoteText('## A heading\n'), formatted=True)
    assert view.area_text() == 'A heading\n'
    assert str(BlockKind.HEADING2) in tags_at(view, '1.0')


def test_list_is_bulleted(view: NoteView) -> None:
    """The items of a list are shown with their bullets and indented."""
    view.show(NoteText('- one\n- two\n'), formatted=True)
    assert view.area_text() == '• one\n• two\n'
    assert 'item1' in tags_at(view, '1.0')


def test_code_is_marked(view: NoteView) -> None:
    """A code block is shown as written, with the tags of code."""
    view.show(NoteText('```\nif x:\n    y = 1\n```\n'), formatted=True)
    assert view.area_text() == 'if x:\n    y = 1\n'
    assert str(BlockKind.CODE) in tags_at(view, '1.0')


def test_table_is_lined_up(view: NoteView) -> None:
    """A table is shown laid out in columns, and is not wrapped."""
    view.show(NoteText('| a | b |\n| --- | --- |\n| 1 | 2 |\n'),
              formatted=True)
    assert line_of(view, 1) == 'a │ b'
    assert str(BlockKind.TABLE) in tags_at(view, '1.0')


def test_quote_is_marked(view: NoteView) -> None:
    """A quoted paragraph is shown as a quote, indented one step."""
    view.show(NoteText('> quoted\n'), formatted=True)
    assert view.area_text() == 'quoted\n'
    assert {str(BlockKind.QUOTE), 'indent1'} <= tags_at(view, '1.0')


def test_rule_is_drawn(view: NoteView) -> None:
    """A line across the note is drawn as a line, not as three dashes."""
    view.show(NoteText('---\n'), formatted=True)
    assert set(line_of(view, 1)) == {'─'}
    assert str(BlockKind.RULE) in tags_at(view, '1.0')


def test_link_is_marked(view: NoteView) -> None:
    """The text of a link is shown as leading somewhere."""
    view.show(NoteText('a [link](target) here\n'), formatted=True)
    assert view.area_text() == 'a link here\n'
    assert LINK_TAG in tags_at(view, '1.2')


def test_struck_is_marked(view: NoteView) -> None:
    """Text struck through in a note has a line drawn over it."""
    view.show(NoteText('a ~~gone~~ word\n'), formatted=True)
    assert view.area_text() == 'a gone word\n'
    assert STRIKE_TAG in tags_at(view, '1.2')


def test_gap_between_pieces(view: NoteView) -> None:
    """Two paragraphs are shown with room left between them."""
    view.show(NoteText('First.\n\nSecond.\n'), formatted=True)
    assert view.area_text() == 'First.\n\nSecond.\n'
    assert GAP_TAG in tags_at(view, '2.0')


def test_gap_above_heading(view: NoteView) -> None:
    """A heading is set off from the part of the note above it."""
    view.show(NoteText('Words.\n\n## Heading\n'), formatted=True)
    assert view.area_text() == 'Words.\n\n\nHeading\n'


def test_raw_after_formatted(view: NoteView) -> None:
    """A note shown as written after a formatted one replaces it."""
    view.show(NoteText('# Heading\n'), formatted=True)
    view.show(NoteText('# Heading\n'))
    assert view.area_text() == '# Heading\n'
    assert str(BlockKind.HEADING1) not in tags_at(view, '1.0')


def test_blocks_can_be_shown(view: NoteView) -> None:
    """The area shows the pieces it is given, whoever read them."""
    view.show_blocks([Block(BlockKind.HEADING1, (Span('Given'),))])
    assert view.area_text() == 'Given\n'


def test_image_is_drawn(view: NoteView, picture: Path) -> None:
    """An image of a note is drawn where the note shows it."""
    view.show(NoteText(f'![A picture]({picture.name})\n'), True,
              picture.parent)
    assert len(view.pictures) == 1
    assert view.area.image_names()
    assert 'A picture' not in view.area_text()


def test_missing_image(view: NoteView, picture: Path) -> None:
    """An image whose file is not there is named by its description."""
    view.show(NoteText('![A picture](no_such_file.png)\n'), True,
              picture.parent)
    assert not view.pictures
    assert view.area_text() == '[A picture]\n'


def test_image_of_no_words(view: NoteView) -> None:
    """An image that the note says nothing about is named all the same."""
    view.show(NoteText('![](no_such_file.png)\n'), True, Path('/nowhere'))
    assert view.area_text() == f'[{MISSING_ALT}]\n'


def test_remote_image(view: NoteView, picture: Path) -> None:
    """An image somewhere on the network is named and never fetched."""
    view.show(NoteText('![Far away](https://example.com/a.png)\n'), True,
              picture.parent)
    assert not view.pictures
    assert view.area_text() == '[Far away]\n'


def test_image_of_wrong_kind(view: NoteView, tmp_path: Path) -> None:
    """A file that Tk cannot read is named rather than drawn."""
    odd = tmp_path / 'odd.png'
    odd.write_bytes(b'this is no picture')
    view.show(NoteText(f'![Odd]({odd.name})\n'), True, tmp_path)
    assert not view.pictures
    assert view.area_text() == '[Odd]\n'


def test_pictures_are_let_go(view: NoteView, picture: Path) -> None:
    """The pictures of a note are let go when another note is shown."""
    view.show(NoteText(f'![A picture]({picture.name})\n'), True,
              picture.parent)
    view.show(NoteText('Nothing to draw.\n'), formatted=True)
    assert not view.pictures


def test_image_without_folder(view: NoteView) -> None:
    """An image beside a note that is nowhere is named, not drawn."""
    view.show(NoteText('![A picture](beside.png)\n'), formatted=True)
    assert not view.pictures
    assert view.area_text() == '[A picture]\n'


def test_zoom_changes_size(view: NoteView) -> None:
    """Zooming draws the note that is shown larger and smaller."""
    started = view.tags.fonts.size
    view.zoom(2)
    assert view.tags.fonts.size == started + 2
    view.zoom(-3)
    assert view.tags.fonts.size == started - 1
    view.zoom_normal()
    assert view.tags.fonts.size == started


def test_zoom_holds_the_note(view: NoteView) -> None:
    """Zooming leaves the note that is shown exactly as it is."""
    view.show(NoteText('# Heading\n\nWords.\n'), formatted=True)
    shown = view.area_text()
    view.zoom(4)
    assert view.area_text() == shown
    assert str(BlockKind.HEADING1) in tags_at(view, '1.0')


def test_nothing_selected(view: NoteView) -> None:
    """A note that nothing is selected of gives no selected text."""
    view.show(NoteText('Some text of a note.\n', ''))
    assert view.selected_text() == ''


def test_part_selected(view: NoteView) -> None:
    """What is selected of a note is what is given, and no more."""
    view.show(NoteText('Some text of a note.\n', ''))
    view.area.tag_add(tkinter.SEL, '1.5', '1.9')
    assert view.selected_text() == 'text'


def test_tab_reaches_note(view: NoteView) -> None:
    """Tab reaches the note, which cannot be written in, all the same."""
    assert view.area.cget('takefocus')
