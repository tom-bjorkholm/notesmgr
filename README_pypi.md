# notesmgr - Managing small notes and AI prompts

## What it does

Notes manager is a very small application to keep small notes
and AI prompts files ordered. The main intended functionality includes:

- Keeping a project with folders of notes (that is small text files)
- Keeping the notes in a defined order, and allowing them to be
  reordered.
- Opening an external editor to create and edit notes.
- Keeping a template in each folder that will be prefilled into
  each new notes file.
- Allow copying of notes to the clipboard (used for instance if
  the note is an AI prompt)

## Using it

If you want to use it, install it using pip from

[https://pypi.org/project/notesmgr](https://pypi.org/project/notesmgr).

There is no need to download anything from GitHub to use the application
or to base your code on the library.

**Note: notesmgr is not yet ready, and is not yet uploaded to PyPI.org**

### Installing on macOS and Linux

````sh
pip3 install --upgrade notesmgr
````

### Installing on Microsoft Windows

````sh
pip install --upgrade notesmgr
````

### Usage overview

This is a simple Tk (Tkinter) based application. It has a menubar and a
main window.

#### Command line

````sh
notesmgr [PROJECT_FOLDER]
notesmgr --version
````

Started with no arguments, `notesmgr` opens with no project and a project
is opened from the menu. Started with a folder, it opens that project.
`notesmgr --version` reports the versions of `notesmgr` and of the packages
it is built on, together with the newer releases that are available, and
opens no window. The same report is in the menu as `Version information…`.

#### Projects

A project in `notesmgr` is a folder tree with a few files with special meaning.

- in the root folder of the project there is a file called `notesmgr.cfg` that
  holds the configuration of the project. When creating a project it is
  automatically created from the user wide configuration

- in each folder (including the root folder of the project) there is a file
  called `template.md.txt` (or `template.md`, or `template.txt`, whichever
  the `file_extension` of the project says). This file will be the initial
  content of every note created in the folder. It can be edited any time
  just like the notes files.

- notes files are files in the folders with an extension of either `.txt`,
  `.md` or `.md.txt`

- in each folder there is a hidden file with the name of `.notes_order.txt`.
  It lists the names (without paths) of the notes file in the folder one per
  line, and it determines the order in which the notes are shown in the
  "explorer" part of the notesmgr Graphical User Interface.

All files in the project are normal files that can be edited using a normal
text editor like Microsoft Visual Code, TextEdit on mac, or Notepad on Windows,
although using the `notesmgr` Graphical User Interface is recommended.

The `.notes_order.txt` is repaired whenever a project is opened.
Non-existing files are removed from the `.notes_order.txt` and existing
files not mentioned in `.notes_order.txt` are added to the end of it in
alphabetical order. A file that was already right is left untouched, and a
folder whose `.notes_order.txt` cannot be read or written is reported and
then shown in alphabetical order.

The templates are put in order at the same time:

- A folder that holds no template gets one. In the root folder of the
  project it is empty, and in any other folder it is a copy of the template
  of the folder above it.
- A template whose extension is not the `file_extension` of the project is
  renamed to carry it, and you are told which templates were renamed. So
  changing `file_extension` renames the templates of the project the next
  time it is opened.
- A folder that holds more than one template is the one case that `notesmgr`
  cannot settle on its own. You are asked which of them to keep; the others
  are moved to the trash of the operating system and the one you keep is
  renamed to carry the `file_extension` of the project. Answering nothing
  leaves every file as it is, and the project is not opened.

#### Menu bar

The menu bar has menus with actions for:

- Creating a new project
- Opening a project
- Creating a note (file) in a folder in the project
- Editing the selected notes file
- Copying the raw text of a selected notes file to clipboard
- Copying the formatted text of a selected note to clipboard
- Deleting the selected note
- Creating a new folder in the project
- Editing the configuration
- Saving the configuration as the user wide configuration
- Reporting version information and information of available updates

The configuration editor writes the configuration itself when you save in
it, so there is no separate menu item for saving the configuration of the
project.

Creating a project and opening a project both ask for a folder. The folder
chooser starts in the project that was opened last in this run of
`notesmgr`, and in the folder that `notesmgr` was started from while no
project has been opened yet. Nothing is remembered from one run to the next.

#### Main window

To the left of the main window there is a tall and narrow "explorer" similar to
the explorer of Microsoft Visual Code and other IDEs. Here all items (notes and
folders) are listed in tree structure. Inside a folder the subfolders come
first in alphabetical order, then the template of the folder, and after them
the notes in the order that `.notes_order.txt` gives. Notes can be selected in
the "explorer" and notes can be dragged in the "explorer" to reorder the notes
within a folder. A note can also be dragged into or out of a folder.

To the right of the main window there is a wide panel with a row of buttons at
the top and an area showing the selected note. If the selected note is written
in markdown this area shows the note formatted for human reading.

The area shows the selected note, and the template of a folder is shown and
edited just like a note. A note that is not valid UTF-8 text is not shown at
all, and a note longer than `max_note_size` is shown as far as that, each of
them with a warning above the note saying why. While a note is shown,
`notesmgr` follows the file, so a note saved in the external editor, or
changed or removed by any other program, is shown as it now stands about a
second later.

The buttons are laid out in as many rows as the width of the window needs,
so that none of them is cut off however small the window is made. They are:

- `Copy raw` take a raw copy of the note file content and store to clipboard
- `Copy formatted` take a copy of the note content formatted for human reading
  and store to clipboard
- `Duplicate` make a copy of the note in the project. The user is asked for
  file name and folder.
- `Edit` start an editor to edit the notes file.
- `New` create a new note. The user is asked for note file name,
  and it is opened in editor with the content of the template file.
- `Delete` the note will be deleted (after confirmation)
- `Up` the note is moved one position up in the list in the explorer
- `Down` the note is moved one position down in the list in the explorer

#### Configuration

The configuration determines a few aspects of how `notesmgr` behaves.

- `editor` is the command used to edit a note. The name of the note file
  replaces `{file}` in the command, and is added at the end of a command
  that holds no `{file}`, so `code` and `code {file}` mean the same thing.
  When creating configuration the default is:
  - If Microsoft Visual Code is in path, it is the default editor.
  - Otherwise the default editor is taken from environment variable `$EDITOR`
    if it exists
  - Otherwise on mac the default editor is `open`
  - Otherwise on Microsoft Windows the default editor is Notepad
  - Otherwise the default editor is `emacs`
- `file_extension` is the file extension of notes. It can be one of
  `.md`, `.txt` and `.md.txt`. The configuration file holds the name
  `MD`, `TXT` or `MD_TXT` rather than the extension itself, which is what
  lets the configuration editor offer the three to be chosen from.
  When creating configuration the default is `.md.txt` (written as
  `MD_TXT`) as many systems do not recognize `.md` as a safe file type.
- `max_note_size` is how many characters of a note the main window shows.
  A longer note is shown up to there, with a warning saying so above it,
  which keeps a file that is no note at all from filling the window. The
  default is 25000, and a value below 2000 or above 100000 is refused as a
  misunderstanding.

A configuration file therefore looks like this:

````json
{
    "editor": "code -n {file}",
    "file_extension": "MD_TXT",
    "max_note_size": 25000
}
````

A project always has a configuration file `notesmgr.cfg` in the root
folder of the project. That configuration is used for the project.

When creating a new project the user wide configuration provides the
default values for the project's configuration file. The user wide
configuration is read from:

- The file named by the environment variable `$NOTESMGR_CFG` if
  that file exists.
- Otherwise the file `$HOME/.notesmgr.cfg` if it exists
- Otherwise the programs built in defaults.

The user wide configuration is *written* to the file that
`$NOTESMGR_CFG` names, whether that file exists yet or not, and to
`$HOME/.notesmgr.cfg` when the variable names nothing. So a variable
naming a file that has not been written yet is a place to write rather
than a reason to refuse to start.

## What notesmgr is built on

`notesmgr` uses `config-as-json` and `edit-cfg-json-tk` for its
configuration, `versionreporter` for the version report, `argcomplete` for
the command line, and `Send2Trash` for everything it removes, so that a file
`notesmgr` takes away can be taken back out of the trash of the operating
system.

## Source code

Source code and tests are available at [https://github.com/tom-bjorkholm/notesmgr](https://github.com/tom-bjorkholm/notesmgr).

## Test summary

- Test result: 698 passed, 7 deselected in 5s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.7
