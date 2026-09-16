#! /usr/local/bin/python3
"""Windows that notesmgr shows over a window of its own."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from contextlib import contextmanager
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Iterator, NamedTuple, Optional, Sequence, Union

MIN_TEXT_WIDTH = 40
"""Narrowest that a window showing a text is made, in characters."""

MAX_TEXT_WIDTH = 100
"""Widest that a window showing a text is made, in characters."""

MAX_TEXT_HEIGHT = 30
"""Tallest that a window showing a text is made, in lines."""

CLOSE_LABEL = 'Close'
"""What the button that closes a shown text says."""

PADDING = 8
"""Space in pixels left around the button of a shown text."""

BUSY_CURSOR = 'watch'
"""Mouse cursor shown while an answer is being gathered."""

CHOOSE_LABEL = 'Keep'
"""What the button that takes the chosen option says."""

CANCEL_LABEL = 'Cancel'
"""What the button that answers nothing at all says."""

ACCEPT_LABEL = 'OK'
"""What the button that takes what was filled in says."""

NAME_LABEL = 'Name'
"""What the field holding a name is called."""

FOLDER_LABEL = 'Folder'
"""What the field holding a folder of the project is called."""

ENTRY_WIDTH = 40
"""Width in characters of the field that a name is typed into."""


def text_size(text: str) -> tuple[int, int]:
    """Return the width and height in characters that a text needs.

    A window is never made narrower than a short line nor wider or
    taller than a screen comfortably holds, so a very long line or a
    very long text is scrolled to instead of being shown whole.

    Args:
        text: The text that is going to be shown.

    Returns:
        The width in characters and the height in lines.
    """
    lines = text.splitlines() or ['']
    widest = max(len(line) for line in lines)
    width = min(max(widest, MIN_TEXT_WIDTH), MAX_TEXT_WIDTH)
    return width, min(len(lines), MAX_TEXT_HEIGHT)


def show_text(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              text: str) -> tkinter.Toplevel:
    """Show a text that cannot be edited, over another window.

    Args:
        parent: The window that the new window is shown over.
        title: What the new window is called.
        text: What the new window shows.

    Returns:
        The window that was made, which its own button destroys.
    """
    window = tkinter.Toplevel(parent)
    window.title(title)
    window.transient(parent)
    _fill_with_text(window, text)
    return window


def _fill_with_text(window: tkinter.Toplevel, text: str) -> None:
    """Fill a window with a text, a scroll bar and a close button."""
    width, height = text_size(text)
    area = tkinter.Text(window, width=width, height=height, wrap='none',
                        font='TkFixedFont')
    scroll = ttk.Scrollbar(window, orient=tkinter.VERTICAL, command=area.yview)
    area.configure(yscrollcommand=scroll.set)
    area.insert('1.0', text)
    area.configure(state=tkinter.DISABLED)
    button = ttk.Button(window, text=CLOSE_LABEL, command=window.destroy)
    button.pack(side=tkinter.BOTTOM, pady=PADDING)
    scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
    area.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)


def show_error(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               message: str) -> None:
    """Tell the user what went wrong, in a window of its own.

    Args:
        parent: The window that the message is shown over.
        title: What the message window is called.
        message: What went wrong.
    """
    messagebox.showerror(title=title, message=message, parent=parent)


@contextmanager
def busy_cursor(window: Union[tkinter.Tk, tkinter.Toplevel]) -> Iterator[None]:
    """Show the waiting cursor while something slow is being done.

    Args:
        window: The window that is going to be busy.

    Yields:
        Nothing. The cursor is put back when the block has ended,
        whether it ended by finishing or by raising.
    """
    window.configure(cursor=BUSY_CURSOR)
    window.update_idletasks()
    try:
        yield
    finally:
        window.configure(cursor='')


def ask_folder(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               folder: Path) -> Optional[Path]:
    """Ask the user for a folder that is there.

    Args:
        parent: The window that the question is asked over.
        title: What the window asking is called.
        folder: The folder that the chooser starts in.

    Returns:
        The folder that was chosen, None when none was.
    """
    chosen = filedialog.askdirectory(parent=parent, title=title,
                                     mustexist=True, initialdir=folder)
    return Path(chosen) if chosen else None


def ask_yes_no(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               question: str) -> bool:
    """Ask the user something that is answered with yes or no.

    Args:
        parent: The window that the question is asked over.
        title: What the window asking is called.
        question: What the user is asked.

    Returns:
        Whether the user answered yes.
    """
    return messagebox.askyesno(title=title, message=question, parent=parent)


def show_info(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              message: str) -> None:
    """Tell the user something that is no cause for worry.

    Args:
        parent: The window that the message is shown over.
        title: What the message window is called.
        message: What the user is told.
    """
    messagebox.showinfo(title=title, message=message, parent=parent)


class AskingWindow:
    """A window that asks the user something and waits for an answer.

    The window is built by the constructor, and the answer is waited
    for by answered(), so that a test can look at the window and
    answer it by pressing its buttons without a main loop of its own.
    """

    def __init__(self, parent: Union[tkinter.Tk, tkinter.Toplevel],
                 title: str) -> None:
        """Build the window, which is empty until it is filled in.

        Args:
            parent: The window that the question is asked over.
            title: What the window asking is called.
        """
        self.taken = False
        self.window = tkinter.Toplevel(parent)
        self.window.title(title)
        self.window.transient(parent)
        self.window.protocol('WM_DELETE_WINDOW', self.cancel)

    def ask(self, question: str) -> None:
        """Put what the user is asked at the top of the window."""
        asked = ttk.Label(self.window, text=question, justify=tkinter.LEFT)
        asked.pack(side=tkinter.TOP, anchor=tkinter.W, padx=PADDING,
                   pady=PADDING)

    def add_buttons(self, accept_label: str) -> None:
        """Put the button that answers and the one that does not.

        Args:
            accept_label: What the button taking the answer says.
        """
        cancel = ttk.Button(self.window, text=CANCEL_LABEL,
                            command=self.cancel)
        accept = ttk.Button(self.window, text=accept_label,
                            command=self.accept)
        cancel.pack(side=tkinter.RIGHT, padx=PADDING, pady=PADDING)
        accept.pack(side=tkinter.RIGHT, pady=PADDING)

    def accept(self) -> None:
        """Take what the user filled in as the answer."""
        self.taken = True
        self.window.destroy()

    def cancel(self) -> None:
        """Answer nothing at all."""
        self.taken = False
        self.window.destroy()

    def answered(self) -> bool:
        """Wait for the answer, holding the rest of the application.

        Returns:
            Whether the user answered rather than answering nothing.
        """
        self.window.grab_set()
        self.window.wait_window()
        return self.taken


class ChoiceDialog(AskingWindow):
    """Asks the user to choose one of several named things."""

    def __init__(self, parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
                 question: str, options: Sequence[str]) -> None:
        """Build the window that asks the question.

        Args:
            parent: The window that the question is asked over.
            title: What the window asking is called.
            question: What the user is asked.
            options: What the user chooses between.
        """
        super().__init__(parent, title)
        self.picked = tkinter.StringVar(self.window,
                                        value=options[0] if options else '')
        self.ask(question)
        for option in options:
            offered = ttk.Radiobutton(self.window, text=option, value=option,
                                      variable=self.picked)
            offered.pack(side=tkinter.TOP, anchor=tkinter.W, padx=PADDING)
        self.add_buttons(CHOOSE_LABEL)

    @property
    def chosen(self) -> Optional[str]:
        """Return what was chosen, None while nothing was."""
        return self.picked.get() if self.taken else None

    def choose(self) -> Optional[str]:
        """Wait for the answer, holding the rest of the application.

        Returns:
            What the user chose, None when the user chose nothing.
        """
        self.answered()
        return self.chosen


def ask_choice(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               question: str, options: Sequence[str]) -> Optional[str]:
    """Ask the user to choose one of several named things.

    Args:
        parent: The window that the question is asked over.
        title: What the window asking is called.
        question: What the user is asked.
        options: What the user chooses between.

    Returns:
        What the user chose, None when the user chose nothing.
    """
    return ChoiceDialog(parent, title, question, options).choose()


def ask_name(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
             question: str, given: str = '') -> Optional[str]:
    """Ask the user for the name of a note or a folder.

    What the name may be is the model's to say, so anything at all
    can be typed here and is refused, if it is to be refused, where
    the file is made.

    Args:
        parent: The window that the question is asked over.
        title: What the window asking is called.
        question: What the user is asked.
        given: What the field holds before anything is typed.

    Returns:
        What the user typed, None when the user typed nothing at all.
    """
    return simpledialog.askstring(title, question, parent=parent,
                                  initialvalue=given)


class NameFolder(NamedTuple):
    """A name, and the folder of the project that it is to be in."""

    name: str
    folder: str


class NameFolderDialog(AskingWindow):
    """Asks the user for a name and for a folder of the project.

    The folders are offered to be chosen rather than to be typed, so
    that what is asked for is always a folder of the project, and
    the file chooser of the platform is not let anywhere near it.
    """

    def __init__(self, parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
                 given: NameFolder, folders: Sequence[str]) -> None:
        """Build the window that asks for the name and the folder.

        Args:
            parent: The window that the question is asked over.
            title: What the window asking is called.
            given: What the two fields hold to begin with.
            folders: The folders of the project, as they are named.
        """
        super().__init__(parent, title)
        self.typed = tkinter.StringVar(self.window, value=given.name)
        self.picked = tkinter.StringVar(self.window, value=given.folder)
        self._fill_in(folders)
        self.add_buttons(ACCEPT_LABEL)

    def _fill_in(self, folders: Sequence[str]) -> None:
        """Put the field for the name above the one for the folder."""
        self.ask(NAME_LABEL)
        entry = ttk.Entry(self.window, textvariable=self.typed,
                          width=ENTRY_WIDTH)
        entry.pack(side=tkinter.TOP, fill=tkinter.X, padx=PADDING)
        self.ask(FOLDER_LABEL)
        chooser = ttk.Combobox(self.window, textvariable=self.picked,
                               values=list(folders), state='readonly')
        chooser.pack(side=tkinter.TOP, fill=tkinter.X, padx=PADDING)
        entry.focus_set()

    @property
    def given(self) -> Optional[NameFolder]:
        """Return what was filled in, None while nothing was taken."""
        if not self.taken:
            return None
        return NameFolder(name=self.typed.get(), folder=self.picked.get())

    def ask_for(self) -> Optional[NameFolder]:
        """Wait for the answer, holding the rest of the application.

        Returns:
            The name and the folder, None when the user gave none.
        """
        self.answered()
        return self.given


def ask_name_folder(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
                    given: NameFolder,
                    folders: Sequence[str]) -> Optional[NameFolder]:
    """Ask the user for a name and for a folder of the project.

    Args:
        parent: The window that the question is asked over.
        title: What the window asking is called.
        given: What the two fields hold to begin with.
        folders: The folders of the project, as they are named.

    Returns:
        The name and the folder, None when the user gave none.
    """
    return NameFolderDialog(parent, title, given, folders).ask_for()
