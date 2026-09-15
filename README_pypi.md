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

#### Projects

A project in `notesmgr` is a folder tree with a few files with special meaning.

- in the root folder of the project there is a file called `notesmgr.cfg` that
  holds the configuration of the project. When creating a project it is
  automatically created from the user wide configuration

- in each folder (including the root folder of the project) there is a file
  called `template.txt` (or `template.md`, or `template.md.txt`). This file
  will be the initial content of every note created in the folder. It can be
  edited any time just like the notes files.

- notes files are files in the folders with an extension of either `.txt`,
  `.md` or `.md.txt`

- in each folder there is a hidden file with the name of `.notes_order.txt`.
  It lists the names (without paths) of the notes file in the folder one per
  line, and it determines the order in which the notes are shown in the
  "explorer" part of the notesmgr Graphical User Interface.

All files in the project are normal files that can be edited using a normal
text editor like Microsoft Visual Code, TextEdit on mac, or Notepad on Windows,
although using the `notesmgr` Graphical User Interface is recommended.

The `.notes_order.txt` is repaired whenever `notesmgr` is started.
Non-existing files are removed from the `.notes_order.txt` and existing
files not mentioned in `.notes_order.txt` are added to the end of it in
alphabetical order.

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
- Saving the configuration for the project
- Saving the configuration as the user wide configuration
- Reporting version information and information of available updates

#### Main window

To the left of the main window there is a tall and narrow "explorer" similar to
the explorer of Microsoft Visual Code and other IDEs. Here all items (notes and
folders) are listed in tree structure. Notes can be selected in the "explorer"
and notes can be dragged in the "explorer" to reorder the notes within a
folder. A note can also be dragged into or out of a folder.

To the right of the main window there is a wide panel with a row of buttons at
the top and an area showing the selected note. If the selected note is written
in markdown this area shows the note formatted for human reading.

The buttons at the top of the right side of the main window are:

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

- `editor` is the command used to edit a note. When creating configuration
  the default is:
  - If Microsoft Visual Code is in path, it is the default editor.
  - Otherwise the default editor is taken from environment variable `$EDITOR`
    if it exists
  - Otherwise on mac the default editor is `open {notes file name}`
  - Otherwise on Microsoft Windows the default editor is Notepad
  - Otherwise the default editor is `emacs`
- `file_extension` is the file extension of notes. It can be one of
  `.md`, `.txt` and `.md.txt`. When creating configuration
  the default is `.md.txt` as many systems do not recognize `.md` as
  a safe file type.

A project always has a configuration file `notesmgr.cfg` in the root
folder of the project. That configuration is used for the project.

When creating a new project the user wide configuration provides the
default values for the project's configuration file. The user wide
configuration is read from:

- The file named by the environment variable `$NOTESMGR_CFG` if
  it exists.
- Otherwise the file `$HOME/.notesmgr.cfg` if it exists
- Otherwise the programs built in defaults.

## Source code

Source code and tests are available at [https://github.com/tom-bjorkholm/notesmgr](https://github.com/tom-bjorkholm/notesmgr).

## Test summary

- Test result: 178 passed, 4 deselected in 3s
- No flake8 warnings.
- No mypy errors found.
- No pylint warnings.
- No python layout warnings.
- Built version(s): 0.0.1
- Build and test using Python 3.14.7
