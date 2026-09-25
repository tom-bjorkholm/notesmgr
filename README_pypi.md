# notesmgr - Managing small notes and AI prompts

## What it does

`notesmgr` is a small desktop application that keeps small notes and AI
prompts in order. It is made for the texts you keep coming back to: the
prompts you paste into an AI assistant, snippets, checklists, and short
notes.

- Notes are ordinary text files in ordinary folders, so they can be kept
  in git, synced, backed up and edited with any editor.
- The notes of a folder are kept in an order of your choosing, and are
  reordered with a button, a key or by dragging.
- A note is edited in the editor you already use, such as Visual Studio
  Code, and the note shown in `notesmgr` follows as you save.
- Every folder has a template that each new note of the folder starts
  from.
- A note is copied to the clipboard with one key, either as it is
  written or formatted, so that pasting it into Mail, Word or Slack keeps
  headings, lists and bold text.
- Notes written in markdown are shown formatted for reading.

It runs on macOS, Microsoft Windows and Linux.

## Installing

`notesmgr` needs Python 3.12 or newer, with Tk (tkinter). Install it
from [PyPI](https://pypi.org/project/notesmgr):

On macOS and Linux:

````sh
pip3 install --upgrade notesmgr
````

On Microsoft Windows:

````sh
pip install --upgrade notesmgr
````

The Python from python.org has Tk built in on macOS and on Windows.
On Linux Tk is often a package of its own, such as `python3-tk` on
Debian and Ubuntu. Copying a note formatted needs `xclip` (X11) or
`wl-copy` (Wayland) on Linux; without them the note is copied as
plain text.

## Getting started

1. Start `notesmgr`.
2. Choose `File` → `New project…` and pick a folder. It can be an empty
   folder or one that already holds notes, which are then taken in.
3. Press `New` (`Cmd+N` on mac, `Ctrl+N` elsewhere), give the note a
   name, and write it in the editor that opens.
4. Select the note in the tree to the left to read it, and press
   `Copy raw` (`Cmd+C` / `Ctrl+C`) to put it on the clipboard.

Next time, open the project with `File` → `Open project…`, or name it
on the command line: `notesmgr ~/notes`.

## Using notesmgr

### The main window

To the left is the tree of the project: its folders, and in each
folder the template of the folder followed by its notes in their order.
Subfolders come first, in alphabetical order.

To the right is the selected note with a row of buttons above it. A
note whose name ends with `.md` or `.md.txt` is shown formatted, and a
note ending with `.txt` is shown exactly as it is written. When a note
is changed by your editor or by any other program, the note shown
follows about a second later.

A new note or folder is made in the selected folder, in the folder of
the selected note, or in the root folder of the project when nothing is
selected.

### Buttons and keyboard shortcuts

Every button is also in the `Note` menu. On mac the shortcuts use `Cmd`,
and on Windows and Linux they use `Ctrl`.

| Button | Shortcut | What it does |
| --- | --- | --- |
| `Copy raw` | `Cmd+C` | Copies the note as it is written. When part of the note is selected, the key copies just that part. |
| `Copy formatted` | `Cmd+Shift+C` | Copies the note formatted, for pasting into Mail, Word, Slack and the like. |
| `Duplicate` | `Cmd+D` | Copies the note, under a name and into a folder you choose. |
| `Edit` | `Cmd+E` | Opens the note in your editor. `Return` in the tree does the same. |
| `New` | `Cmd+N` | Makes a note from the template of the folder and opens it in your editor. |
| `Delete` | `Cmd+Backspace` | Moves the note to the trash, after asking. |
| `Up` | `Cmd+Up` | Moves the note one place up. |
| `Down` | `Cmd+Down` | Moves the note one place down. |

The other shortcuts are:

| Shortcut | What it does |
| --- | --- |
| `Cmd+Shift+N` | Makes a folder (`Folder` → `New folder…`). |
| `Cmd++`, `Cmd+-`, `Cmd+0` | Draws the note and the tree larger, smaller, and in the normal size again (`View` menu). |
| `Cmd+W` on mac, `Ctrl+Q` elsewhere | Quits. |
| `Tab` | Goes from the tree to the buttons and on to the note. |

The template of a folder is shown, edited and copied like any note,
but it cannot be duplicated, deleted or moved: every folder has exactly
one template.

### Dragging

Notes and folders can be dragged in the tree. A note dropped above or
below another note is moved to that place, and a note dropped on a
folder is moved to the end of that folder. A folder dropped on another
folder is moved into it with everything it holds. While you drag, a
line shows where a note would land and the folder that would take it is
marked. `Escape` gives up the drag. A name that the other folder holds
already is refused rather than moved.

### Folders

The `Folder` menu makes, renames and deletes folders of the project. A
new folder starts with a copy of the template of the folder above it. A
folder can be renamed at any time, and is deleted, to the trash, only
when it holds no notes and no folders. The root folder of the project
is renamed and deleted outside `notesmgr`.

### Configuration

`Configuration` → `Edit configuration…` edits the configuration of the
open project, which is stored in `notesmgr.cfg` in the root folder of the
project. It holds:

- `editor`: the command that opens a note. `{file}` stands for the note,
  and the note is put last when the command has no `{file}`, so `code`
  and `code {file}` mean the same thing. For a new configuration it is
  Visual Studio Code (`code`) when that is installed, otherwise the
  editor that `$EDITOR` names, otherwise `open` on mac, Notepad on
  Windows and `emacs` elsewhere.
- `file_extension`: what new notes are called, one of `.md.txt` (the
  default), `.md` and `.txt`. `.md.txt` is the default because many
  systems do not see `.md` as a safe kind of file.
- `max_note_size`: how many characters of a note are shown, from 2000 to
  100000 and 25000 unless you say otherwise. A longer note is shown up to
  there, with a warning above it.

A configuration file looks like this:

````json
{
    "editor": "code -n {file}",
    "file_extension": "MD_TXT",
    "max_note_size": 25000
}
````

`Configuration` → `Save configuration as user wide…` makes the
configuration of the project the one that every new project starts
with. With no project open, `Edit configuration…` edits that user wide
configuration.

### Command line

````sh
notesmgr [PROJECT_FOLDER]
notesmgr --version
````

Started with a folder, `notesmgr` opens the project in it. `--version`
reports the versions of `notesmgr` and of the packages it uses, and
which newer releases there are, just as `Help` → `Version information…`
does.

## Details

This section says what `notesmgr` does in the cases where you might
wonder.

### The files of a project

- `notesmgr.cfg` in the root folder holds the configuration of the
  project.
- Every folder holds one template, `template.md.txt`, `template.md` or
  `template.txt` after the `file_extension` of the project.
- Every folder holds a hidden `.notes_order.txt` that lists the notes of
  the folder, one name per line, in the order they are shown. Folders
  are not listed in it.
- Every other file ending with `.txt`, `.md` or `.md.txt` is a note.

All of these can be edited with any text editor while `notesmgr` is not
looking. Deleting a note, a folder or a template always moves it to the
trash of the operating system, so it can be taken back.

### What opening a project puts in order

- `.notes_order.txt` is repaired: names of notes that are gone are
  removed, and notes it does not name are added at the end in
  alphabetical order. A folder whose `.notes_order.txt` cannot be read or
  written is reported, and its notes are shown in alphabetical order.
- A folder without a template gets one: an empty one in the root
  folder, and a copy of the template of the folder above it elsewhere.
- A template whose extension is not the `file_extension` of the project
  is renamed, and you are told so. Changing `file_extension` therefore
  renames the templates the next time the project is opened.
- A folder holding more than one template is the one thing `notesmgr`
  cannot decide for you. You are asked which one to keep, and the others
  go to the trash. Answering nothing leaves every file as it is, and the
  project is not opened.

### What a formatted note shows

Headings, paragraphs, bold, italic, `~~struck through~~` text, code in a
line and code blocks, lists nested as deeply as you like, tables, block
quotes, horizontal lines, and the text of links. PNG and GIF images next
to the note are drawn where the note shows them, and other images are
named by their description. HTML in a note is shown as the text it is.
A note that is not valid UTF-8 is not shown, and says why.

### How `Copy formatted` works

The note goes on the clipboard as rich text and as plain text, so that
an application that takes formatting gets it, and a plain text field
gets the note as it is written. A note that is not markdown is copied
as preformatted text, so that a table lined up by hand stays lined up.
It uses what the operating system already has: `textutil` and
`osascript` on mac, the Windows clipboard itself, and `xclip` or
`wl-copy` on Linux. When the tool it needs is missing, the note is
copied as plain text and you are told why.

### Where the user wide configuration is

It is read from the file that `$NOTESMGR_CFG` names, when that file
exists, otherwise from `~/.notesmgr.cfg`, and otherwise the built-in
defaults are used. It is written to the file that `$NOTESMGR_CFG`
names, whether that file exists yet or not, and to `~/.notesmgr.cfg`
when the variable is not set.

### What is remembered

Nothing is remembered from one run to the next: not the last project,
not the size of the window, and not the size of the text. Within one
run, the folder chooser starts in the project opened last.

## What notesmgr is built on

`notesmgr` uses `config-as-json` and `edit-cfg-json-tk` for its
configuration, `markdown` for reading notes written in markdown,
`versionreporter` for the version report, `argcomplete` for the command
line, and `Send2Trash` for moving files to the trash.

## Source code

Source code and tests are available at
[https://github.com/tom-bjorkholm/notesmgr](https://github.com/tom-bjorkholm/notesmgr).

## Test summary

- Test result: 1489 passed, 13 deselected in 8s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.1.0
- Build and test using Python 3.14.7
