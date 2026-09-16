# notesmgr implementation plan

This plan turns the feature sketch in `README_pypi.md` into an ordered
series of implementation steps.

Every step ends the same way:

1. all tools clean repo-wide:
   `./run_clean_build.py`, and for the last step of each feature area also
   `./run_clean_build.py python3.12` and `python3.13`.
2. Something that can be run to see the step in action, always the
   growing application itself.
3. The user reviews the changes and runs what can be run to see it in action.
4. The user does a git commit of the step.

Every step carries extensive tests written together with the code.

## Design summary

### The problem

`notesmgr` keeps small text notes (and AI prompts) in a folder tree with a
user-defined order, edits them in an external editor, creates them from a
per-folder template, and copies them to the clipboard as raw or as
formatted text. State lives entirely in ordinary files:

- `notesmgr.cfg` in the project root (project configuration, JSON)
- `template.<ext>` in each folder (initial content for new notes)
- `.notes_order.txt` in each folder (one note file name per line)
- note files with extension `.txt`, `.md` or `.md.txt`

Nothing is cached in a database, so anything a text editor or Finder does
to the tree behind the application's back has to be survivable.

### Inputs and edge cases that shape the design

- `.notes_order.txt` is user-editable and therefore arbitrary text:
  missing file, blank lines, CRLF, a BOM, duplicate names, names of files
  that no longer exist, files that exist but are unlisted, names with
  path separators, unreadable file. All of this is normalised by one
  repair function; nothing else in the code sees a broken order file.
- A folder can hold only a single template (`template.txt`, `template.md`,
  or `template.md.txt`) at any one time. Multiple templates in a folder
  is reported as an error to the user (with a dialog/pop-up) and the
  user has to choose which template to keep.
- `.md.txt` is a two-part extension, so extension classification must try
  the longest suffix first or every `.md.txt` note is seen as a `.txt`.
- Note content is user text: invalid UTF-8, an empty file, a very large
  file, markdown with embedded HTML.
- Note names come from dialogs: empty, only whitespace, path separators,
  a leading dot, a name that already exists, a name carrying a different
  extension than the configured one, names that differ only by case on a
  case-insensitive file system.
- The external editor is a configured command string: empty, quoted
  arguments, with or without the `{file}` placeholder, a program that is
  not installed, a program that returns immediately.
- The clipboard has no portable rich-text path in Tk, so each platform
  needs its own payload and its own way of putting it there.
- Platform differences run through the whole application: default editor,
  clipboard, trash, path case sensitivity, `shlex` rules.

### Shape of the solution

Two layers with a hard boundary:

- **Model layer, free of Tk.** Pure functions and small classes over
  `pathlib.Path`, `subprocess`, `shlex` and the `config_as_json`
  configuration object. This layer holds every rule and is where the
  extensive tests live; it runs headless and needs no display.
- **View layer, thin Tk.** Widgets that show what the model says and
  call model operations. Tested with a real but withdrawn `Tk` root. The
  few tests that need a genuinely focused window carry the
  `focus_sensitive` marker, are excluded from the normal build through
  `BuildSpec.excluded_test_markers`, and are run by
  `./run_focus_sensitive_tests.py`.

The rule for the boundary: **if a question has a right answer, it belongs
in the model.** Which note is at which index, whether a name is
acceptable, what the editor command line is, what bytes go on the
clipboard — all model. Only geometry, event binding and widget state are
view.

## Decisions taken before planning

| Topic | Decision |
| --- | --- |
| Formatted preview | `markdown` package for markdown → HTML, drawn into an ordinary `tkinter.Text` by a renderer notesmgr owns. The spike in step 6 ruled out both HTML widget dependencies |
| `Copy formatted` | Real rich text on the system pasteboard using tools the OS already ships, no new Python dependency (macOS `textutil`+`osascript`/`pbcopy`, Windows CF_HTML through `ctypes`, Linux `xclip`/`wl-copy`) |
| Configuration editor | `TkEditorPanel(config, parent=main_window, modal=True)`; the application already owns a `tkinter.Tk`, so `edit()`/`TkEditor` cannot be used |
| Configuration saving | The panel's own Save writes `<project>/notesmgr.cfg`; a separate menu item copies that file to the user-wide location |
| `.notes_order.txt` | Orders notes only; subfolders are shown above the notes of their folder, sorted alphabetically |
| Templates | Shown in the tree as a special first item per folder: selectable and editable, but not reorderable, duplicable or deletable |
| External editor | Launched detached; the preview follows the file through an mtime poll |
| `editor` value | One command string, split with `shlex`, `{file}` replaced by the note path and appended when the placeholder is absent |
| `Delete` | Moves the note to the OS trash (`send2trash`), after confirmation |
| Folder operations | New, rename, and delete only when the folder is empty |
| New project | Any folder; existing note files are adopted into `.notes_order.txt`; a folder that already has `notesmgr.cfg` is refused and offered to be opened |
| Start-up | No memory of the last project. `notesmgr [PROJECT_FOLDER]` and `notesmgr --version` |
| Testing | Model headless, view with a withdrawn Tk root, `focus_sensitive` suite outside the normal build |

## Module inventory

One flat package, small modules, model and view kept apart.
`test/test_notesmgr/` mirrors it one test module per source module.

### Model

| Module | Responsibility |
| --- | --- |
| `config.py` | `NotesmgrConfig(Config)`: `editor`, `file_extension`, `max_note_size`, validation plan |
| `config_defaults.py` | Built-in defaults, default editor discovery per platform |
| `config_files.py` | User-wide path lookup, load, save, copy to user-wide |
| `descriptions.py` | `Descriptions` mapping for the configuration editor |
| `note_file.py` | Extension classification, template names, name validation |
| `order_file.py` | `.notes_order.txt` read, repair, atomic write |
| `project.py` | `Project`: root, configuration, scanned folder/note tree |
| `project_ops.py` | New, duplicate, delete, move, reorder, folder operations |
| `editor_command.py` | Editor argv construction and detached launch |
| `file_watch.py` | Modification-time polling of the shown note |
| `note_text.py` | Reading a note: decoding, size limit, what cannot be shown |
| `markdown_render.py` | Markdown → HTML, and the stylesheet for the widget |
| `rich_clipboard.py` | Backend selection and payload construction |
| `clipboard_macos.py`, `clipboard_windows.py`, `clipboard_linux.py` | One platform each |
| `version_info.py` | `versionreporter` wiring |
| `cmd_line.py` | `argparse` + `argcomplete` |

### View

| Module | Responsibility |
| --- | --- |
| `application.py` | `main()`: command line, root window, mainloop |
| `main_window.py` | Window, panes, wiring of view to model |
| `menu_bar.py` | Menu definitions and their commands |
| `explorer_tree.py` | `ttk.Treeview` of the project |
| `explorer_drag.py` | Drag-and-drop behaviour of the tree (step 9) |
| `note_panel.py` | Right panel: button row and note area |
| `button_row.py` | The button row, laid out in as many rows as fit |
| `note_view.py` | Raw and formatted display of a note |
| `dialogs.py` | Name/folder dialogs, confirmations, error reporting |

## The steps

### Step 1 — Framework repair and a window that opens

Status: **Implemented and committed**

**Goal:** a repaired stub, a green build on 3.12/3.13/3.14, and an
application that starts.

Already done before this plan was written:

- `pyproject.toml`: `[project.gui-scripts]` said
  `backlogops-gui = "backlogops_gui.application:main"`; now
  `notesmgr = "notesmgr.application:main"`, matching `setup.py`.
  Empty string removed from `keywords`.
- `README.md`: "Notes managar" → "Notes manager".
- `README_pypi.md`: `fomatted`, `clipbaord`, `allthough`, `aphabetical`,
  `detemines a new aspects`, `main windows`, `always have`,
  `projects configuation file`, `dragged to into`, and a `Down` button
  described as moving the note up.
- `custom_build_tools/custom_spec.py`: blank line before the docstring.
- Copyright year 2024 → 2026 in the two `__init__.py` files.

Remaining in this step:

- `pyproject.toml`: add `[tool.pytest.ini_options]` registering the
  `focus_sensitive` marker (no ini file is passed to pytest, so pytest
  reads its settings from `pyproject.toml`).
- `custom_build_tools/custom_spec.py`: return a real `BuildSpec` with
  `excluded_test_markers=['focus_sensitive']` and
  `python_layout_max_name_length=25` to match the name-length rule in
  `CLAUDE.md`.
- `run_focus_sensitive_tests.py` in the repo root, running
  `pytest -m focus_sensitive` in the venv, printing the warning that the
  machine must be left alone while it runs.
- `src/notesmgr/application.py` with `main()`, `src/notesmgr/__main__.py`,
  and `src/notesmgr/main_window.py` with the window, the paned layout, an
  empty explorer on the left, an empty panel on the right, and a menu bar
  holding only `File > Quit`.
- `test/test_notesmgr/conftest.py` with a session-scoped withdrawn `Tk`
  root fixture that skips the test when no display is available, and a
  `helpers.py` that builds temporary projects on disk.

**Tests:** `main()` builds and destroys the window with the mainloop
stubbed; the window has the expected panes, title and minimum size; Quit
destroys it; one `focus_sensitive` smoke test that a real window can be
raised and focused, proving the excluded-marker wiring.

**Risk to watch:** `custom_build_tools/test/` and
`common_build_tools/test/` both have an `__init__.py` and no package
above them, so both import as a package named `test`. Harmless while the
custom one holds no test files; if pytest reports an import mismatch,
exclude it with `pytest_exclude_folders`.

**In action:** `./venv/bin/notesmgr` and
`./venv/bin/python3 -m notesmgr` open the empty main window.

### Step 2 — Configuration, its editor, and version reporting

Status: **Implemented, committed.**

Decisions taken while implementing it, which later steps build on:

- `config_as_json` writes an enum member as its **name**, and
  `edit-cfg-json` builds its pull-down from the enum member names, so
  `notesmgr.cfg` holds `"file_extension": "MD_TXT"` and not `".md.txt"`.
  `NoteExtension.value` is the extension text that the rest of the code
  uses. `README_pypi.md` documents this.
- `--version` prints to standard output only. The graphical way of asking
  is `Help > Version information…`, and both go through
  `version_info.version_report(out_file)`, which the menu entry gives a
  `StringIO` that it then shows in a window.
- notesmgr supports a Python version for about two and a half years after
  the next Python version was released, always ending on the first of
  March: 3.12 ends 2027-03-01 and 3.13 ends 2028-03-01.
- `Save configuration as user wide…` is greyed out until a project is
  open. `MainWindow.project_config` is the path it copies, and step 3
  sets it and calls `menu_bar.set_enabled` when a project opens.
- `config_files.py` holds only what step 2 uses: `user_config_path`,
  `user_config_source` and `copy_to_user_wide`. Loading the user wide
  configuration into a `NotesmgrConfig` lands in step 3, where creating a
  project needs it.
- One module beyond the inventory: `config_editor.py`, which decides
  which files the editor panel reads and writes. Step 3 gives it the
  project variant, and it is also the seam that keeps a real editor
  window out of the normal test run.
- `menu_bar.py` builds menus from `MenuSpec`/`MenuEntry` descriptions and
  offers `set_enabled` for an entry that only makes sense in some states.

**Goal:** the configuration exists, can be edited in the
`edit-cfg-json-tk` panel, and the application can report its versions.

- `config.py`: `NotesmgrConfig(Config)` with `editor: str` and
  `file_extension: NoteExtension`. `NoteExtension` is a `StrEnum`
  (`.md`, `.txt`, `.md.txt`) with a parse converter, so the editor offers
  it as a pull-down rather than a free-text field. Validation plan:
  extension among the allowed values, editor non-empty.
- `config_defaults.py`: default editor by the README's rules — `code` if
  on `PATH`, else `$EDITOR`, else `open` on macOS, else `notepad` on
  Windows, else `emacs`. Default extension `.md.txt`.
- `config_files.py`: user-wide path from `$NOTESMGR_CFG`, else
  `~/.notesmgr.cfg`, else built-in defaults; load, save, and copy the
  project file to the user-wide location.
- `descriptions.py`: what each member is for, shown by the editor.
- `version_info.py` and `cmd_line.py`: `notesmgr [PROJECT_FOLDER]`,
  `notesmgr --version` through `versionreporter`, `argcomplete` wired.
- Menu bar grows a `Configuration` menu (`Edit configuration…`,
  `Save configuration as user wide…`) and `Help > Version information…`.
  With no project open the editor edits the user-wide configuration file,
  which is a real use of its own; step 3 points it at the project file
  when a project is open.

**Tests:** default editor for each platform and environment combination
(`shutil.which`, `$EDITOR`, `sys.platform` monkeypatched); validation
accepts and refuses; JSON round trip; user-wide path precedence including
a `$NOTESMGR_CFG` naming a missing file; command line parsing and exit
codes; the menu commands with an injected panel factory so no real editor
window opens in the normal suite.

**In action:** `./venv/bin/notesmgr --version`; then start the
application, `Configuration > Edit configuration…`, change the editor,
save, and see `~/.notesmgr.cfg` written.

### Step 3 — Project model and the explorer tree

Status: **Implemented, committed.**

Decisions taken while implementing it, which later steps build on:

- A note is any file ending in `.txt`, `.md` or `.md.txt`, whatever the
  project is configured with. `file_extension` says what a *new* note
  and the template of a folder are called, not what counts as a note.
- Every folder holds exactly one template, and opening a project makes
  that true: a folder without one gets an empty template in the root
  and a copy of the template above it anywhere else; a template
  carrying another extension is renamed and the user is told which
  ones were renamed; a folder holding several templates is the one
  question the model cannot answer, so the user is asked which to keep,
  the others go to the trash, and answering nothing refuses to open the
  project at all.
- `send2trash` therefore lands in step 3 rather than step 5.
- The order file is written only when the repair changed something, so
  opening a project leaves the folders that were in order untouched.
  A folder whose order file cannot be read or written, and a folder
  that cannot be listed, is reported as a problem and shown in
  alphabetical order; the rest of the project still opens.
- Inside a folder the tree shows the subfolders first in alphabetical
  order, then the template, then the notes in order-file order.
- `errors.py` beyond the inventory: one `NotesmgrError` that every
  model module raises and the view turns into a message box.
- `note_panel.py` arrives in step 3 rather than step 4, holding only
  the path of what is selected. It keeps `MainWindow` down to the
  seven attributes pylint allows and gives step 4 its place to grow.
- `MainWindow.project_config` is a method and no longer an attribute,
  for the same reason: the open project is what knows the path.
- `Edit configuration…` edits the project's own `notesmgr.cfg` while a
  project is open, and the project is opened again when the editing
  session ends, so that a changed `file_extension` takes effect at
  once. `config_editor.editor_files()` is where that choice lives.
- The Tk file chooser, the yes-or-no question, the message and the
  window that asks which template to keep are all in `dialogs.py`, so
  that a test can answer them without a window reaching the screen.
- `mypy_paths=[Path('test')]` in the build spec, so that the test
  modules can share `test/test_notesmgr/helpers.py`.
- `session.py` beyond the inventory: `Session` holds what one run of
  the application knows, which is the open project and the folder a
  folder chooser starts in. That is the project opened last in this
  run, and the folder the application was started from until one has
  been opened; nothing is remembered from one run to the next. It
  also keeps `MainWindow` at the seven attributes pylint allows, by
  taking the place of the `project` attribute rather than adding to
  it, and `MainWindow.project_config()` moved into it as
  `Session.config_file()`.

**Goal:** open and create projects, and see them in the tree.

- `note_file.py`: extension classification with the longest suffix first,
  template detection, name validation for new notes.
- `order_file.py`: tolerant read, repair against the real directory
  listing (drop what is gone, append what is new in alphabetical order),
  atomic write through a temporary file and `Path.replace`.
- `project.py`: `Project` holding root, configuration and a scanned tree;
  folders above notes, alphabetical; `notesmgr.cfg`, `.notes_order.txt`
  and other dot files never shown; the folder's template as its special
  first item.
- `project_ops.py` gains `create_project()` (adopt existing note files,
  refuse a folder that already has `notesmgr.cfg` and offer to open it)
  and `open_project()` (refuse a folder without `notesmgr.cfg`).
- `explorer_tree.py` and `File > New project…` / `Open project…` with
  `filedialog.askdirectory`. The right panel shows the selected item's
  path for now.

**Tests:** the order-file edge-case list from the design summary, one
case each; scan of a nested tree; several templates in one folder;
adoption on creation; both refusals; the repair actually written to disk;
the tree contents for a temporary project.

**In action:** `New project…` on a folder of existing `.md` files, watch
the tree appear and `.notes_order.txt` be written; restart with
`notesmgr <that folder>`.

### Step 4 — Note preview, external editor, `Copy raw`

Status: **Implemented and committed.**

Decisions taken while implementing it, which later steps build on:

- `max_note_size` joins the configuration: how many characters of a note
  the panel shows, 25000 by default and refused outside 2000 to 100000,
  so that a file that is no note at all cannot fill the window. A note
  longer than that is shown as far as the limit, and `Copy raw` then
  copies what is shown, which is what the warning above it says.
- A note that is not valid UTF-8 is not shown at all, warning only, so
  that nothing misleading is ever shown or copied. A note that cannot be
  read, and one that has been taken away, say so the same way.
- `config_as_json` wants every member named in the file, so adding a
  member would refuse every configuration file written before it.
  `OldNotesmgrConfig(ReadOldConfiguration)` fills in the default for a
  file that names no `max_note_size`, which is the library's own way of
  reading a file of an older version. Before first release (as we are
  now) there is no need to be compatible with old configuration files.
- The menu bar grows a `Note` menu holding `Edit` and `Copy raw`, greyed
  out until there is a note. Step 5 adds its entries to a menu that is
  there already.
- The template of a folder is a note to the panel: it is shown, edited
  and copied like any other. Only a folder and nothing at all leave the
  buttons greyed out.
- The poll follows the note that is shown and nothing else. A note that
  is gone leaves the panel saying so and every button greyed out, while
  the tree is left as it is until the project is opened again.
- `note_text.py` beyond the inventory holds the whole decision about
  decoding, warnings and limits, and `note_view.py` arrives here rather
  than in step 7, which grows the formatted display into it.
- `NotePanel` is given the `Session` and a `PanelHooks` pair of
  callbacks, which keeps both it and `MainWindow` inside the seven
  attributes that pylint allows. The hooks are how a note that
  disappears greys out the menu entries as well as the buttons.
- `subprocess.Popen(argv, start_new_session=True)` is the whole of
  launching detached: Windows ignores the argument, and a program
  started there is independent already.
- The eight buttons do not fit side by side in every window that
  notesmgr can be given: they need 708 pixels in the aqua theme, and
  the panel has 724 at the initial size and 364 at the smallest window
  size. `button_row.py` therefore lays them out in the fewest rows
  that fit and does it again whenever the width changes, which is one
  row at the initial size and three at the smallest. The decision is
  two pure functions over the button widths, so it is tested without a
  window, and macOS is the size that matters: the aqua theme ignores
  ttk padding, so the width of a button there cannot be reduced.

**Goal:** see a note, edit it outside, watch it update, copy it.

- `editor_command.py`: `shlex.split` with the platform's rules, `{file}`
  substituted or appended, detached `subprocess.Popen`, and a clear error
  when the program is missing.
- `file_watch.py`: a `tkinter.after` poll (about once a second) of the
  shown note's modification time and size, pure decision function
  separated from the scheduling.
- `note_panel.py`: the full button row with the not-yet-implemented
  buttons disabled, and the note shown as raw text. Text is read as UTF-8
  with a visible warning line when the file is not valid UTF-8.
- `Copy raw` through the ordinary Tk clipboard.

**Tests:** editor command construction, parametrized over quoting,
placeholder present/absent/repeated, empty value, Windows and POSIX
rules; launch with an injected runner; the poll decision function;
panel content for UTF-8, non-UTF-8, empty and large files;
`focus_sensitive` clipboard round trip.

**In action:** select a note, press `Edit`, change it in VS Code, save,
and watch the panel follow; press `Copy raw` and paste.

### Step 5 — Note and folder operations

Status: **Implemented, committed.**

Decisions taken while implementing it, which later steps build on:

- Every note operation ends by bringing the note order file of the
  folder back in line with what the folder now holds, which is the
  repair that opening a project already does. One `resync_order()`
  therefore covers making, copying and taking away a note, and only
  `move_note()` writes an order of its own.
- After an operation the whole project is read again and the tree
  built afresh, with what was made or moved selected in it. That is
  `MainWindow.reopen()`, and it also takes up whatever another
  program did to the folders meanwhile. Tk reports a selection it was
  given only when it comes to handle its own events, which is too
  late for the command that asked for it, so the panel is told at
  once rather than through the event.
- Which actions can be used now is a question with a right answer, so
  it is a model one: `actions.py` names the actions and says which of
  them a selection allows, and both the button row and the menus are
  set from that one answer. `ButtonRow.offer()` therefore takes the
  names of the actions that can be used rather than one flag.
- Three modules beyond the inventory: `note_ops.py` and
  `folder_ops.py`, because `project_ops.py` is about opening a
  project and was long enough already, and `trash.py`, which is the
  one place that asks `send2trash` to take something away.
- `commands.py` beyond the inventory holds what the buttons and the
  menu entries do: ask the user, have the model do it, report what
  could not be done, and have the window show the project again. It
  is what keeps `MainWindow` and `NotePanel` inside the seven
  attributes and twenty public methods that pylint allows, and it
  took over `PanelHooks`, which is gone.
- The note menu holds the same actions as the button row, under the
  same names, and is built from the same description, so that the two
  cannot drift apart. `Copy formatted` has nothing to do until step
  8, so it is a button of the row but no entry of the menu yet.
- A folder is renamed whatever it holds, because nothing outside a
  folder names it, and is taken away only when it holds no notes and
  no folders of its own. Its template and its note order file are
  notesmgr's own doing and do not count as holding anything. The root
  folder is the project itself, and is renamed and taken away from
  outside notesmgr.
- A new folder is given a copy of the template above it and a note
  order file at once, so that opening the project again reports
  nothing.
- A name is taken when the folder holds any name equal to it but for
  its case, whatever this file system makes of it, so that a project
  written on Linux holds no two names that macOS or Windows would
  read as one file.
- `Up` and `Down` at the first and the last place do nothing and stay
  offered, rather than being greyed out at the ends.
- `dialogs.py` grew an `AskingWindow` that `ChoiceDialog` and the new
  `NameFolderDialog` are both built on, a name question that is
  `tkinter.simpledialog.askstring`, and the name and folder question
  that `Duplicate` asks. The folders of the project are offered in a
  pull-down, named by the way down to them, so that what is asked for
  is always a folder of the project.
- `note_file.checked_name()` holds what a name may be, and
  `note_file_name()` is that with the extension of the project put
  on, so that a note and a folder are named by the same rules.
- `README_pypi.md` change 6 is applied: the menu list, the trash, and
  the folder operations.

**Goal:** every button and menu item that changes the tree.

- `project_ops.py`: `new_note` (template content, appended to the order
  file, opened in the editor), `duplicate_note` (name and folder asked),
  `delete_note` (confirmation, `send2trash`, removed from the order
  file), `move_up`/`move_down`, `new_folder`, `rename_folder`,
  `delete_folder` (empty folders only).
- `dialogs.py`: the name-and-folder dialog, confirmations, and one place
  where model errors become message boxes.
- `send2trash` added to `install_requires` and to both READMEs.

**Tests:** every operation on a temporary project, with the edge cases
named in the design summary — existing name, invalid name, wrong
extension, case-only difference, move at the first and last position,
deleting the only note, renaming onto an existing folder, deleting a
non-empty folder — and the order file checked after each one.

**In action:** create, duplicate, reorder and delete notes and folders in
the window, then look at `.notes_order.txt` and the trash.

### Step 6 — Markdown rendering spike and decision

Status: **Implemented, decision taken, committed.**

The comparison is in `.plans/spike_report.md`, and the spike itself is
`.plans/spike_widgets.py` over `.plans/spike_note.md`.

**The decision: neither HTML widget.** `markdown` and `types-Markdown`
are in `install_requires`, and step 7 draws the note into an ordinary
`tkinter.Text` with tags that notesmgr owns. If that turns out to be
harder than the spike suggests, `tkhtmlview` is the fallback to
reconsider, and the report says what it would cost.

What the spike found, in short:

- `tkinterweb` cannot be used. It needs a compiled Tkhtml3 binary, and
  no release of `tkinterweb-tkhtml` carries one for Tcl/Tk 9, which is
  what Python 3.14 brings and therefore what this repository builds on.
- `tkhtmlview` works on all three versions but is a 750-line tag-based
  parser rather than an engine: block quotes come out flat, horizontal
  rules vanish, tables become tab characters, a remote image freezes the
  window, and a local image is looked for in the current folder.
- The recommendation is therefore neither of the two, but a `tkinter.Text`
  renderer that notesmgr owns, fed from the same HTML, which adds no
  runtime dependency beyond `markdown` and cannot break on a Tk upgrade.
  That would make step 7 somewhat larger than planned.

**Goal:** settle the HTML widget dependency on evidence.

- Install `tkinterweb` and `tkhtmlview` into the venv and render the same
  sample note (headings, nested lists, fenced code, a table, a block
  quote, links, an inline image) in each, side by side, from a throwaway
  script in `.plans/`, which is outside every folder the build discovers.
- Check installation and rendering on 3.12, 3.13 and 3.14.
- Record the comparison and the decision in `.plans/`, and add the winner
  to `install_requires` together with `markdown`.

**In action:** the spike script shows both widgets on the same note, and
you choose.

### Step 7 — Formatted note preview

Status: **Not implemented yet.**

**Goal:** markdown notes shown formatted for reading.

- `markdown_render.py`: `markdown` with a documented extension set
  (fenced code, tables, sane lists). Embedded HTML in a note is rendered
  as text, not as markup, which step 6 established needs the `html_block`
  preprocessor and the `html` inline pattern deregistered. The HTML is
  also what step 8 puts on the clipboard.
- A pure function from that HTML to the segments and tags that a
  `tkinter.Text` is filled with, over `html.parser` from the standard
  library. This is where every question with a right answer lives, and
  it is tested headless over the markdown fixture corpus.
- `note_view.py`: applies the segments and owns the tag definitions
  (headings, code, block quote indent, list indent, link). Formatted for
  `.md` and `.md.txt`, raw for `.txt`, with the switch owned by the model.

Implement in 2 sub-steps: first the rendering of a markdown note
with basic tests, then a mid-review by a human looking at how
a note with content from `.plans/spike_note.md` is rendered, and
finally the implementation of the rest of the functionality and
the extensive tests. The reason is that we want to find out as
early as possible of the decision from the spike in step 6 is
correct.

**Tests:** the HTML for a corpus of markdown fixtures, including the
awkward ones (nested lists, a code fence holding markdown, a table with
missing cells, a link with no target, embedded HTML, an image whose file
is missing); widget population smoke tests with the Tk root fixture.

**In action:** select a markdown note and read it formatted; select a
`.txt` note and see raw text.

### Step 8 — `Copy formatted`

Status: **Not implemented yet.**

**Goal:** paste into Word, Mail or Slack and get formatted text.

- `rich_clipboard.py` picks a backend and builds the payload; each
  platform module owns its own mechanism:
  - **macOS:** `textutil -stdin -format html -convert rtf -stdout`, then
    the pasteboard set with both the RTF and a plain-text flavour in one
    write (a second write would replace the first).
  - **Windows:** one clipboard session through `ctypes` writing the
    registered `HTML Format` (with its byte-offset header, computed and
    tested) and `CF_UNICODETEXT`.
  - **Linux:** `xclip -selection clipboard -t text/html` or
    `wl-copy -t text/html`, with a plain-text fallback and a status
    message when neither is installed.

**Tests:** payload construction, especially the CF_HTML header offsets,
and the command lines, against injected runners; backend selection per
platform; the plain-text fallback path; `focus_sensitive` tests doing a
real round trip on the development machine.

**In action:** `Copy formatted` on a markdown note, then paste into Mail
and into TextEdit.

### Step 9 — Drag and drop in the explorer

Status: **Not implemented yet.**

**Goal:** reorder notes and move them between folders by dragging.

- `explorer_drag.py`: press, motion with a drop indicator, release;
  `Escape` cancels. The whole decision — given the dragged item and the
  pointer position, which folder and which index is the drop — is a pure
  function in the model, and the view only supplies coordinates.
- `project_ops.move_note(note, folder, index)` covers both reordering
  within a folder and moving between folders, including a name collision
  in the target folder.
- Refused drops: onto itself, onto a template, into a note, out of the
  project.

**Tests:** the drop-target function over a table of positions and trees;
the move operation and both order files after a cross-folder move;
`focus_sensitive` tests driving real drags with `event_generate`.

**In action:** drag notes within and between folders, then check the
order files.

### Step 10 — Polish, documentation and release readiness

Status: **Not implemented yet.**

**Goal:** a finished application.

- Every failure path reaches the user as a message box or a status line,
  never as a traceback in a terminal that a GUI launch does not have.
- Keyboard shortcuts for the button row, window geometry and minimum
  size, sensible focus order.
- `README_pypi.md` brought in line with what was built (the list of
  changes below), `README.md` development notes, generated `doc/api.md`
  reviewed.
- Clean builds on 3.12, 3.13 and 3.14, the focus-sensitive suite run by
  hand, and `./run_pypi_build.py` exercised.

**In action:** the finished application on a real notes project.

## Changes to the specification in `README_pypi.md`

These follow from the decisions above and are applied in the step where
the behaviour lands, not all at the end:

1. `Saving the configuration for the project` leaves the menu list: the
   configuration editor's own Save writes `notesmgr.cfg`, and
   `Save configuration as user wide` copies that file (step 2).
2. The `editor` value is documented with the `{file}` placeholder, which
   is the README's `{notes file name}` written in the form the code uses
   (step 2).
3. Subfolders are listed above the notes of their folder in alphabetical
   order and are not part of `.notes_order.txt` (step 3).
4. The template is shown in the tree as a special first item per folder
   (step 3).
5. The command line `notesmgr [PROJECT_FOLDER]` and `notesmgr --version`
   is documented (step 2).
6. `Delete` moves the note to the OS trash rather than deleting it
   permanently, and folders can be renamed and deleted when empty
   (step 5).
7. The new runtime dependencies (`markdown`, the HTML widget,
   `send2trash`) are listed (steps 5 to 7).
8. The configuration holds `max_note_size`, and what the note area shows
   of an awkward note is documented (step 4).
