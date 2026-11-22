#! /usr/local/bin/python3
"""Tests of the user guide that the Help menu shows."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from importlib.metadata import PackageNotFoundError
from typing import NamedTuple, Union
import pytest
from notesmgr import user_guide as guide_module
from notesmgr.errors import NotesmgrError
from notesmgr.note_blocks import Block, BlockKind, Span, markdown_blocks
from notesmgr.user_guide import NO_GUIDE, SHORTCUTS, TEST_SUMMARY, \
    block_text, guide_blocks, heading_level, readme_text, section_slice, \
    shortcut_blocks

README = f"""# Title

Intro.

## First

Text of first.

### Sub of first

Text of sub.

## {SHORTCUTS}

| Button | mac | Windows and Linux |
| --- | --- | --- |
| `New` | `Cmd+N` | `Ctrl+N` |

### Sub of `shortcuts`

More keys.

## Last

Text of last.

## {TEST_SUMMARY}

- No flake8 warnings.
"""
"""A README of the shape that the guide is cut out of."""


class FakeMetadata(NamedTuple):
    """Stands in for the metadata of an installed package."""

    json: dict[str, Union[str, list[str]]]


def titles(blocks: tuple[Block, ...]) -> list[str]:
    """Return what the headings among the pieces say, in order."""
    return [block_text(block) for block in blocks if heading_level(block)]


def use_metadata(monkeypatch: pytest.MonkeyPatch,
                 description: Union[str, list[str]]) -> None:
    """Make the installed package carry the given long description."""
    def fake(_package: str) -> FakeMetadata:
        """Stand in for reading the metadata of the package."""
        return FakeMetadata({'description': description})
    monkeypatch.setattr(guide_module, 'metadata', fake)


@pytest.mark.parametrize('kind,expected', [
    (BlockKind.HEADING1, 1), (BlockKind.HEADING2, 2),
    (BlockKind.HEADING6, 6), (BlockKind.PARAGRAPH, 0),
    (BlockKind.TABLE, 0), (BlockKind.CODE, 0)])
def test_heading_level(kind: BlockKind, expected: int) -> None:
    """A heading has its level, and every other piece has none."""
    assert heading_level(Block(kind)) == expected


def test_block_text() -> None:
    """The text of a piece is its runs of text put together."""
    block = Block(BlockKind.HEADING2, (Span('How '), Span('Copy'),
                                       Span(' works')))
    assert block_text(block) == 'How Copy works'


@pytest.mark.parametrize('title,expected', [
    ('Title', ['Title', 'First', 'Sub of first', SHORTCUTS,
               'Sub of shortcuts', 'Last', TEST_SUMMARY]),
    ('First', ['First', 'Sub of first']),
    ('Sub of first', ['Sub of first']),
    (SHORTCUTS, [SHORTCUTS, 'Sub of shortcuts']),
    ('Sub of shortcuts', ['Sub of shortcuts']),
    (TEST_SUMMARY, [TEST_SUMMARY]),
    ('Text of first.', []),
    ('Missing', []),
    ('', [])])
def test_section_slice(title: str, expected: list[str]) -> None:
    """A section holds its subsections and ends at the next heading."""
    blocks = markdown_blocks(README)
    assert titles(blocks[section_slice(blocks, title)]) == expected


def test_section_to_the_end() -> None:
    """The last section reaches to the last piece of the text."""
    blocks = markdown_blocks(README)
    assert section_slice(blocks, TEST_SUMMARY).stop == len(blocks)


def test_first_of_same_title() -> None:
    """Of two headings saying the same, the first starts the section."""
    blocks = markdown_blocks('## A\n\none\n\n## A\n\ntwo\n')
    assert section_slice(blocks, 'A') == slice(0, 2)


def test_section_of_nothing() -> None:
    """No pieces hold no section."""
    assert section_slice((), 'A') == slice(0, 0)


def test_guide_no_summary() -> None:
    """The guide is the README without its test summary."""
    shown = guide_blocks(README)
    assert titles(shown) == ['Title', 'First', 'Sub of first', SHORTCUTS,
                             'Sub of shortcuts', 'Last']
    assert shown == markdown_blocks(README.partition(f'## {TEST_SUMMARY}')[0])


def test_guide_whole() -> None:
    """A README with no test summary is shown whole."""
    text = '# Title\n\nIntro.\n'
    assert guide_blocks(text) == markdown_blocks(text)


def test_shortcut_blocks() -> None:
    """The shortcuts are their section, with its table and subsections."""
    shown = shortcut_blocks(README)
    assert titles(shown) == [SHORTCUTS, 'Sub of shortcuts']
    assert BlockKind.TABLE in [block.kind for block in shown]


def test_shortcuts_missing() -> None:
    """A README that has lost the shortcuts says so."""
    with pytest.raises(NotesmgrError, match=SHORTCUTS):
        shortcut_blocks('# Title\n\nIntro.\n')


def test_installed_readme() -> None:
    """The installed notesmgr carries the guide with its shortcuts."""
    text = readme_text()
    assert titles(shortcut_blocks(text))[0] == SHORTCUTS
    assert TEST_SUMMARY not in titles(guide_blocks(text))


def test_readme_from_metadata(monkeypatch: pytest.MonkeyPatch) -> None:
    """The guide is the long description of the installed package."""
    use_metadata(monkeypatch, README)
    assert readme_text() == README


@pytest.mark.parametrize('description', ['', ' \n', ['a', 'b']])
def test_readme_empty(monkeypatch: pytest.MonkeyPatch,
                      description: Union[str, list[str]]) -> None:
    """A package that carries no README has no guide to show."""
    use_metadata(monkeypatch, description)
    with pytest.raises(NotesmgrError) as caught:
        readme_text()
    assert str(caught.value) == NO_GUIDE


def test_not_installed(monkeypatch: pytest.MonkeyPatch) -> None:
    """A notesmgr that is not installed has no guide to show."""
    def missing(package: str) -> FakeMetadata:
        """Stand in for a package that is not installed."""
        raise PackageNotFoundError(package)
    monkeypatch.setattr(guide_module, 'metadata', missing)
    with pytest.raises(NotesmgrError) as caught:
        readme_text()
    assert str(caught.value) == NO_GUIDE
