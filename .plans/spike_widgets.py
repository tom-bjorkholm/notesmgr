#! /usr/local/bin/python3
"""Spike comparing tkinterweb and tkhtmlview as the note preview widget.

Run with no argument to see both widgets side by side on the same
note, and with `--check` to print the same facts without opening a
window, which is what is run on each Python version.

This is the throwaway of step 6 of `.plans/initials_steps.md`. It is
no part of notesmgr and the build discovers nothing in this folder.
It needs `markdown`, and it reports rather than requires each of the
two candidates, so that a missing one does not hide the other.
"""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import argparse
import os
import sys
import time
import tkinter
from pathlib import Path
from tkinter import ttk
from typing import Callable, NamedTuple, Optional, Sequence
import markdown

HERE = Path(__file__).resolve().parent
"""Folder holding the sample note and the image that the note shows."""

NOTE = HERE / 'spike_note.md'
"""The sample note that both candidates are given."""

EXTENSIONS = ['fenced_code', 'tables', 'sane_lists']
"""The markdown extensions that step 7 plans to use."""

RELOADS = 10
"""How many loads the timing of a reload is averaged over."""

PADDING = 8
"""Space in pixels left around what a column shows."""

WRAP_WIDTH = 500
"""Pixels after which the reason for a missing candidate is broken."""

PHRASES = ('struck through', 'Deeply nested and ordered',
           'An unchecked task', 'Hello, {name} <&>', '# Not a heading',
           'indented code, four spaces', 'Missing cell',
           'A quote inside the quote', 'reference link',
           'this must not turn bold', "alert('no')", 'Level six')
"""Pieces of the note that the rendered text is looked for.

What a widget does not show at all is what it silently drops, which
is the part of rendering that can be judged without looking.
"""


class Pane(NamedTuple):
    """One candidate widget, its version, and how it is worked.

    The widget is kept apart from the two calls because the two
    libraries name them differently, and everything else here is
    then written once rather than once per candidate.
    """

    widget: tkinter.Widget
    version: str
    load: Callable[[str], None]
    text: Callable[[], str]


def build_tkinterweb(parent: tkinter.Misc) -> Pane:
    """Build the tkinterweb pane, a real HTML engine in a Tk widget.

    Scripts and forms are turned off because a note is a document
    and not a web page, and the folder of the note is given as the
    base url so that an image beside the note is found.
    """
    # pylint: disable=import-outside-toplevel
    import tkinterweb  # type: ignore[import-untyped]
    frame = tkinterweb.HtmlFrame(parent, messages_enabled=False,
                                 javascript_enabled=False, forms_enabled=False)

    def load(html: str) -> None:
        """Put HTML into the widget, with the note's folder as base."""
        frame.load_html(html, base_url=HERE.as_uri() + '/')
    return Pane(frame, tkinterweb.__version__, load, frame.get_page_text)


def build_tkhtmlview(parent: tkinter.Misc) -> Pane:
    """Build the tkhtmlview pane, which draws HTML with Text tags.

    It is a `tkinter.Text` underneath, so the text it shows is read
    the way any text area is read.
    """
    # pylint: disable=import-outside-toplevel
    import tkhtmlview  # type: ignore[import-untyped]
    widget = tkhtmlview.HTMLScrolledText(parent, wrap=tkinter.WORD)

    def text() -> str:
        """Return the text that the widget shows."""
        return str(widget.get('1.0', 'end-1c'))
    return Pane(widget, tkhtmlview.VERSION, widget.set_html, text)


BUILDERS: dict[str, Callable[[tkinter.Misc], Pane]] = {
    'tkinterweb': build_tkinterweb, 'tkhtmlview': build_tkhtmlview}
"""The candidates, in the order they are shown and reported."""


def make_note_folder_current() -> None:
    """Make the folder of the note current, for tkhtmlview's sake.

    Its parser looks for the file of an image relative to the folder
    that is current rather than to the note, so an image beside the
    note is found only while that folder is the current one.
    tkinterweb is given the folder as a base url and needs none of
    this, so making it current is what lets both be judged on the
    same note.
    """
    os.chdir(HERE)


def note_html() -> str:
    """Return the sample note converted to HTML as step 7 will do it.

    Python-Markdown lets raw HTML in the note through into the
    output, and a note is a document that is read rather than a page
    that is obeyed, so the two processors that pass it through are
    taken out and the markup becomes text instead.
    """
    converter = markdown.Markdown(extensions=EXTENSIONS)
    converter.preprocessors.deregister('html_block')
    converter.inlinePatterns.deregister('html')
    return converter.convert(NOTE.read_text(encoding='utf-8'))


def platform_line(root: tkinter.Misc) -> str:
    """Return the Python, the Tcl/Tk and the platform this runs on."""
    version = '.'.join(str(part) for part in sys.version_info[:3])
    return (f'Python {version}, Tcl/Tk {root.tk.call("info", "patchlevel")}'
            f', {sys.platform}')


def load_seconds(pane: Pane, html: str, times: int) -> float:
    """Return the average seconds that loading the note takes.

    The widget is brought up to date inside the timing, because a
    library that only queues the work would otherwise look free.
    """
    start = time.monotonic()
    for _ in range(times):
        pane.load(html)
        pane.widget.update()
    return (time.monotonic() - start) / times


def report_text(pane: Pane) -> None:
    """Print how much of the note the widget shows, and what is lost."""
    shown = pane.text()
    missing = [phrase for phrase in PHRASES if phrase not in shown]
    print(f'  shows        {len(shown)} characters')
    print(f'  drops        {missing if missing else "nothing"}')


def report_candidate(root: tkinter.Misc, name: str, html: str) -> None:
    """Print one block of facts about one candidate."""
    try:
        pane = BUILDERS[name](root)
    except (ImportError, OSError, tkinter.TclError) as error:
        print(f'{name}: UNUSABLE HERE')
        print(f'  {type(error).__name__}: {error}')
        return
    print(f'{name} {pane.version}: usable')
    print(f'  first load   {load_seconds(pane, html, 1):.3f} s')
    print(f'  reload       {load_seconds(pane, html, RELOADS):.3f} s')
    report_text(pane)


def report_check(html: str) -> None:
    """Print what can be learnt of every candidate without a window."""
    root = tkinter.Tk()
    root.withdraw()
    print(platform_line(root))
    print(f'markdown {markdown.__version__}, {NOTE.name} gives '
          f'{len(html)} characters of HTML')
    for name in BUILDERS:
        print()
        report_candidate(root, name, html)
    root.destroy()


def add_column(root: tkinter.Misc, column: int, name: str,
               html: str) -> Optional[Pane]:
    """Put one candidate in a column of its own, or say why it is not.

    Returns:
        The pane that was built, and None when the candidate cannot
        be used on this machine.
    """
    frame = ttk.Frame(root, padding=PADDING)
    frame.grid(row=1, column=column, sticky=tkinter.NSEW)
    root.columnconfigure(column, weight=1, uniform='candidates')
    frame.rowconfigure(1, weight=1)
    frame.columnconfigure(0, weight=1)
    try:
        pane = BUILDERS[name](frame)
    except (ImportError, OSError, tkinter.TclError) as error:
        ttk.Label(frame, text=f'{name} cannot be used here:\n\n{error}',
                  wraplength=WRAP_WIDTH, justify=tkinter.LEFT).grid(row=0,
                                                                    column=0)
        return None
    ttk.Label(frame, text=f'{name} {pane.version}').grid(row=0, column=0)
    pane.widget.grid(row=1, column=0, sticky=tkinter.NSEW)
    pane.load(html)
    return pane


def reload_all(panes: Sequence[Optional[Pane]], html: str) -> None:
    """Load the note again, which is what the file watch will do."""
    for name, pane in zip(BUILDERS, panes):
        if pane is not None:
            print(f'{name} reload {load_seconds(pane, html, 1):.3f} s')


def show_window(html: str) -> None:
    """Open one window holding every candidate side by side."""
    root = tkinter.Tk()
    root.title(f'notesmgr step 6 spike: {platform_line(root)}')
    root.geometry('1500x950')
    root.rowconfigure(1, weight=1)
    panes = [add_column(root, column, name, html)
             for column, name in enumerate(BUILDERS)]
    ttk.Button(root, text='Reload both', padding=PADDING,
               command=lambda: reload_all(panes, html)).grid(
                   row=0, column=0, columnspan=len(BUILDERS), pady=PADDING)
    root.mainloop()


def main() -> None:
    """Show the window, or print the facts when --check is given."""
    parser = argparse.ArgumentParser(description='Compare the two '
                                     'candidate HTML widgets.')
    parser.add_argument('--check', action='store_true',
                        help='print the facts and open no window')
    checking = parser.parse_args().check
    make_note_folder_current()
    html = note_html()
    if checking:
        report_check(html)
    else:
        show_window(html)


if __name__ == '__main__':
    main()
