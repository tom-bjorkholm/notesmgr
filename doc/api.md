# Table of Contents

* [notesmgr.main\_window](#notesmgr.main_window)
  * [Shortcut](#notesmgr.main_window.Shortcut)
  * [tk\_window\_system](#notesmgr.main_window.tk_window_system)
  * [quit\_shortcut](#notesmgr.main_window.quit_shortcut)
  * [MainWindow](#notesmgr.main_window.MainWindow)
    * [\_\_init\_\_](#notesmgr.main_window.MainWindow.__init__)
    * [show\_project](#notesmgr.main_window.MainWindow.show_project)
    * [edit\_configuration](#notesmgr.main_window.MainWindow.edit_configuration)
    * [save\_user\_wide](#notesmgr.main_window.MainWindow.save_user_wide)
    * [show\_version](#notesmgr.main_window.MainWindow.show_version)
    * [quit](#notesmgr.main_window.MainWindow.quit)
* [notesmgr.version\_info](#notesmgr.version_info)
  * [MAIN\_PACKAGE](#notesmgr.version_info.MAIN_PACKAGE)
  * [REPORTED\_PACKAGES](#notesmgr.version_info.REPORTED_PACKAGES)
  * [RECOMMENDED\_PYTHON](#notesmgr.version_info.RECOMMENDED_PYTHON)
  * [SUPPORT\_EXPIRES](#notesmgr.version_info.SUPPORT_EXPIRES)
  * [NotesmgrVersions](#notesmgr.version_info.NotesmgrVersions)
    * [package\_names](#notesmgr.version_info.NotesmgrVersions.package_names)
    * [get\_app\_support\_expires](#notesmgr.version_info.NotesmgrVersions.get_app_support_expires)
    * [get\_main\_package\_name](#notesmgr.version_info.NotesmgrVersions.get_main_package_name)
    * [recommended\_python](#notesmgr.version_info.NotesmgrVersions.recommended_python)
  * [version\_report](#notesmgr.version_info.version_report)
* [notesmgr.menu\_bar](#notesmgr.menu_bar)
  * [MenuEntry](#notesmgr.menu_bar.MenuEntry)
  * [MenuSpec](#notesmgr.menu_bar.MenuSpec)
  * [MenuBar](#notesmgr.menu_bar.MenuBar)
  * [entry\_state](#notesmgr.menu_bar.entry_state)
  * [build\_menu](#notesmgr.menu_bar.build_menu)
  * [build\_menu\_bar](#notesmgr.menu_bar.build_menu_bar)
  * [set\_enabled](#notesmgr.menu_bar.set_enabled)
* [notesmgr.cmd\_line](#notesmgr.cmd_line)
  * [PROGRAM\_NAME](#notesmgr.cmd_line.PROGRAM_NAME)
  * [DESCRIPTION](#notesmgr.cmd_line.DESCRIPTION)
  * [FOLDER\_HELP](#notesmgr.cmd_line.FOLDER_HELP)
  * [VERSION\_HELP](#notesmgr.cmd_line.VERSION_HELP)
  * [CommandLine](#notesmgr.cmd_line.CommandLine)
  * [argument\_parser](#notesmgr.cmd_line.argument_parser)
  * [parse\_command\_line](#notesmgr.cmd_line.parse_command_line)
* [notesmgr.config](#notesmgr.config)
  * [EMPTY\_EDITOR](#notesmgr.config.EMPTY_EDITOR)
  * [NoteExtension](#notesmgr.config.NoteExtension)
  * [DEFAULT\_EXTENSION](#notesmgr.config.DEFAULT_EXTENSION)
  * [NotesmgrConfig](#notesmgr.config.NotesmgrConfig)
    * [\_\_init\_\_](#notesmgr.config.NotesmgrConfig.__init__)
    * [parse\_converters](#notesmgr.config.NotesmgrConfig.parse_converters)
    * [get\_validation\_plan](#notesmgr.config.NotesmgrConfig.get_validation_plan)
    * [stripped\_editor](#notesmgr.config.NotesmgrConfig.stripped_editor)
* [notesmgr.config\_files](#notesmgr.config_files)
  * [CONFIG\_VARIABLE](#notesmgr.config_files.CONFIG_VARIABLE)
  * [CONFIG\_NAME](#notesmgr.config_files.CONFIG_NAME)
  * [user\_config\_path](#notesmgr.config_files.user_config_path)
  * [user\_config\_source](#notesmgr.config_files.user_config_source)
  * [copy\_to\_user\_wide](#notesmgr.config_files.copy_to_user_wide)
* [notesmgr.config\_editor](#notesmgr.config_editor)
  * [open\_config\_editor](#notesmgr.config_editor.open_config_editor)
* [notesmgr.application](#notesmgr.application)
  * [main](#notesmgr.application.main)
* [notesmgr.config\_defaults](#notesmgr.config_defaults)
  * [VISUAL\_CODE](#notesmgr.config_defaults.VISUAL_CODE)
  * [EDITOR\_VARIABLE](#notesmgr.config_defaults.EDITOR_VARIABLE)
  * [PLATFORM\_EDITORS](#notesmgr.config_defaults.PLATFORM_EDITORS)
  * [OTHER\_EDITOR](#notesmgr.config_defaults.OTHER_EDITOR)
  * [default\_editor](#notesmgr.config_defaults.default_editor)
* [notesmgr.dialogs](#notesmgr.dialogs)
  * [MIN\_TEXT\_WIDTH](#notesmgr.dialogs.MIN_TEXT_WIDTH)
  * [MAX\_TEXT\_WIDTH](#notesmgr.dialogs.MAX_TEXT_WIDTH)
  * [MAX\_TEXT\_HEIGHT](#notesmgr.dialogs.MAX_TEXT_HEIGHT)
  * [CLOSE\_LABEL](#notesmgr.dialogs.CLOSE_LABEL)
  * [PADDING](#notesmgr.dialogs.PADDING)
  * [BUSY\_CURSOR](#notesmgr.dialogs.BUSY_CURSOR)
  * [text\_size](#notesmgr.dialogs.text_size)
  * [show\_text](#notesmgr.dialogs.show_text)
  * [show\_error](#notesmgr.dialogs.show_error)
  * [busy\_cursor](#notesmgr.dialogs.busy_cursor)
* [notesmgr.descriptions](#notesmgr.descriptions)
  * [DESCRIPTIONS](#notesmgr.descriptions.DESCRIPTIONS)

<a id="notesmgr.main_window"></a>

# notesmgr.main\_window

The main window of the notesmgr application.

<a id="notesmgr.main_window.Shortcut"></a>

## Shortcut Objects

```python
class Shortcut(NamedTuple)
```

A keyboard shortcut: its Tk event sequence and its menu label.

<a id="notesmgr.main_window.tk_window_system"></a>

#### tk\_window\_system

```python
def tk_window_system(window: tkinter.Misc) -> str
```

Return the windowing system Tk uses: aqua, win32 or x11.

<a id="notesmgr.main_window.quit_shortcut"></a>

#### quit\_shortcut

```python
def quit_shortcut(window_system: str) -> Shortcut
```

Return the keyboard shortcut that closes the main window.

macOS closes a window with Cmd+W, while Windows and the X11
desktops leave a program with Ctrl+Q.

<a id="notesmgr.main_window.MainWindow"></a>

## MainWindow Objects

```python
class MainWindow()
```

The notesmgr main window with its explorer and its note panel.

The window is given to the constructor instead of created by it, so
that the application can use the Tk root window while tests can use
a hidden toplevel window under one shared Tk root.

<a id="notesmgr.main_window.MainWindow.__init__"></a>

#### \_\_init\_\_

```python
def __init__(window: Union[tkinter.Tk, tkinter.Toplevel]) -> None
```

Fill the given toplevel window with the notesmgr main window.

<a id="notesmgr.main_window.MainWindow.show_project"></a>

#### show\_project

```python
def show_project(project_name: Optional[str]) -> None
```

Name the open project in the window title, None meaning none.

<a id="notesmgr.main_window.MainWindow.edit_configuration"></a>

#### edit\_configuration

```python
def edit_configuration() -> None
```

Open the editor of the user wide configuration.

One session at a time is enough, and the editor holds the
application while it is open, so a second one is not started.

<a id="notesmgr.main_window.MainWindow.save_user_wide"></a>

#### save\_user\_wide

```python
def save_user_wide() -> None
```

Copy the project's configuration to the user wide file.

<a id="notesmgr.main_window.MainWindow.show_version"></a>

#### show\_version

```python
def show_version() -> None
```

Show what notesmgr and the packages below it are.

Gathering the report asks PyPI whether there are newer
releases, which takes a moment, so the window says that it is
working while that is going on.

<a id="notesmgr.main_window.MainWindow.quit"></a>

#### quit

```python
def quit() -> None
```

Destroy the main window, which ends the application.

<a id="notesmgr.version_info"></a>

# notesmgr.version\_info

Version information about notesmgr and what it is built on.

<a id="notesmgr.version_info.MAIN_PACKAGE"></a>

#### MAIN\_PACKAGE

Package to install to get a newer notesmgr.

<a id="notesmgr.version_info.REPORTED_PACKAGES"></a>

#### REPORTED\_PACKAGES

Packages whose versions are worth reporting to a user.

<a id="notesmgr.version_info.RECOMMENDED_PYTHON"></a>

#### RECOMMENDED\_PYTHON

Python version that notesmgr is developed and recommended on.

<a id="notesmgr.version_info.SUPPORT_EXPIRES"></a>

#### SUPPORT\_EXPIRES

When notesmgr stops supporting a Python version.

A Python version is supported for about two and a half years after the
next Python version was released, and support always ends on the first
of March. Newer language features are then available sooner than
following the end of life of Python itself would allow.

<a id="notesmgr.version_info.NotesmgrVersions"></a>

## NotesmgrVersions Objects

```python
class NotesmgrVersions(VersionReporter)
```

Report what notesmgr and the packages below it are.

<a id="notesmgr.version_info.NotesmgrVersions.package_names"></a>

#### package\_names

```python
def package_names() -> list[str]
```

Return the packages whose versions are reported.

<a id="notesmgr.version_info.NotesmgrVersions.get_app_support_expires"></a>

#### get\_app\_support\_expires

```python
def get_app_support_expires() -> SupportExpires
```

Return when notesmgr stops supporting an older Python.

<a id="notesmgr.version_info.NotesmgrVersions.get_main_package_name"></a>

#### get\_main\_package\_name

```python
@classmethod
def get_main_package_name(cls) -> str
```

Return the package that an upgrade of notesmgr installs.

<a id="notesmgr.version_info.NotesmgrVersions.recommended_python"></a>

#### recommended\_python

```python
@classmethod
def recommended_python(cls) -> Version
```

Return the Python version that notesmgr recommends.

<a id="notesmgr.version_info.version_report"></a>

#### version\_report

```python
def version_report(out_file: TextIO) -> None
```

Write the version report of notesmgr to the given stream.

The command line gives it the standard output stream, and the
graphical user interface gives it a string that it then shows in a
window, so that both ways of asking report exactly the same thing.

**Arguments**:

- `out_file` - Stream that the report is written to.

<a id="notesmgr.menu_bar"></a>

# notesmgr.menu\_bar

The menu bar of a notesmgr window.

<a id="notesmgr.menu_bar.MenuEntry"></a>

## MenuEntry Objects

```python
class MenuEntry(NamedTuple)
```

One command of a menu, and whether it can be chosen.

<a id="notesmgr.menu_bar.MenuSpec"></a>

## MenuSpec Objects

```python
class MenuSpec(NamedTuple)
```

One menu of a menu bar and the commands it holds.

<a id="notesmgr.menu_bar.MenuBar"></a>

## MenuBar Objects

```python
class MenuBar(NamedTuple)
```

The menu bar widget of a window and its menus by title.

The menus are kept by title so that an entry which only makes
sense in some states can be greyed out and offered again later.

<a id="notesmgr.menu_bar.entry_state"></a>

#### entry\_state

```python
def entry_state(enabled: bool) -> Literal['normal', 'disabled']
```

Return the Tk state of an entry that can or cannot be chosen.

**Arguments**:

- `enabled` - Whether the entry can be chosen.
  

**Returns**:

  The state that Tk knows that by.

<a id="notesmgr.menu_bar.build_menu"></a>

#### build\_menu

```python
def build_menu(menu_bar: tkinter.Menu, spec: MenuSpec) -> tkinter.Menu
```

Create one described menu and add it to a menu bar.

**Arguments**:

- `menu_bar` - The menu bar that the menu is added to.
- `spec` - What the menu is called and what it holds.
  

**Returns**:

  The menu that was made.

<a id="notesmgr.menu_bar.build_menu_bar"></a>

#### build\_menu\_bar

```python
def build_menu_bar(window: Union[tkinter.Tk, tkinter.Toplevel],
                   menus: Sequence[MenuSpec]) -> MenuBar
```

Build the described menus and install them on a window.

An application says what its menus hold and gets them, instead of
calling Tk for every entry of every menu.

**Arguments**:

- `window` - The window that gets the menu bar.
- `menus` - The menus of the menu bar, in the order they are shown.
  

**Returns**:

  The menu bar that was made.

<a id="notesmgr.menu_bar.set_enabled"></a>

#### set\_enabled

```python
def set_enabled(menu: tkinter.Menu, label: str, enabled: bool) -> None
```

Let one entry of a menu be chosen, or grey it out.

**Arguments**:

- `menu` - The menu that the entry is in.
- `label` - Which entry of that menu it is.
- `enabled` - Whether the entry can now be chosen.

<a id="notesmgr.cmd_line"></a>

# notesmgr.cmd\_line

The command line of the notesmgr application.

<a id="notesmgr.cmd_line.PROGRAM_NAME"></a>

#### PROGRAM\_NAME

Name that the command line help calls this program.

<a id="notesmgr.cmd_line.DESCRIPTION"></a>

#### DESCRIPTION

What the command line help says this program is for.

<a id="notesmgr.cmd_line.FOLDER_HELP"></a>

#### FOLDER\_HELP

What the command line help says about the project folder.

<a id="notesmgr.cmd_line.VERSION_HELP"></a>

#### VERSION\_HELP

What the command line help says about the version flag.

<a id="notesmgr.cmd_line.CommandLine"></a>

## CommandLine Objects

```python
class CommandLine(NamedTuple)
```

What the command line asked notesmgr to do.

<a id="notesmgr.cmd_line.argument_parser"></a>

#### argument\_parser

```python
def argument_parser() -> argparse.ArgumentParser
```

Return the parser that reads the notesmgr command line.

<a id="notesmgr.cmd_line.parse_command_line"></a>

#### parse\_command\_line

```python
def parse_command_line(argv: Optional[list[str]] = None) -> CommandLine
```

Return what the given command line, or sys.argv, asked for.

Whether the named folder holds a project is not decided here. A
graphical application says that in a window of its own, and not on
an error stream that a program started from a desktop has not got.

**Arguments**:

- `argv` - Command line arguments, or None for the ones this
  program was started with.
  

**Returns**:

  What was asked for.

<a id="notesmgr.config"></a>

# notesmgr.config

The configuration of notesmgr and the values it accepts.

<a id="notesmgr.config.EMPTY_EDITOR"></a>

#### EMPTY\_EDITOR

What is said about an editor command that holds no command.

<a id="notesmgr.config.NoteExtension"></a>

## NoteExtension Objects

```python
class NoteExtension(StrEnum)
```

Note file extension: MD is .md, TXT is .txt, MD_TXT is .md.txt.

The configuration file holds the name of one of these members,
while the value of the member is the extension itself. MD_TXT is
the default, because many systems do not recognize .md as a safe
file type.

<a id="notesmgr.config.DEFAULT_EXTENSION"></a>

#### DEFAULT\_EXTENSION

Note file extension that a new configuration starts out with.

<a id="notesmgr.config.NotesmgrConfig"></a>

## NotesmgrConfig Objects

```python
class NotesmgrConfig(Config)
```

How notesmgr edits the notes of a project and what it names them.

The editor command is started whenever a note is edited, and the
extension is the one that new notes are given and that a file must
have to be a note at all.

<a id="notesmgr.config.NotesmgrConfig.__init__"></a>

#### \_\_init\_\_

```python
def __init__(from_json_data_text: Optional[str] = None,
             from_json_filename: Optional[PathOrStr] = None,
             stderr_file: TextIO = sys.stderr,
             member_name: Optional[str] = None) -> None
```

Construct the configuration with its default values.

**Arguments**:

- `from_json_data_text` - Optional JSON text to parse directly.
- `from_json_filename` - Optional path to a JSON file to read.
- `stderr_file` - Stream used for user-facing diagnostics.
- `member_name` - Path for reaching this object from the top
  level configuration, None for the top level itself.

<a id="notesmgr.config.NotesmgrConfig.parse_converters"></a>

#### parse\_converters

```python
def parse_converters() -> dict[str, ParseConverter]
```

Return how the name in the file becomes an extension again.

Declaring it is also what lets the configuration editor offer
the extensions to be chosen instead of to be spelled.

<a id="notesmgr.config.NotesmgrConfig.get_validation_plan"></a>

#### get\_validation\_plan

```python
def get_validation_plan(stderr_file: TextIO) -> ValidationPlan
```

Return the checks that every configuration has to pass.

<a id="notesmgr.config.NotesmgrConfig.stripped_editor"></a>

#### stripped\_editor

```python
def stripped_editor(value: object) -> str
```

Return the editor command without the blanks around it.

**Arguments**:

- `value` - The editor command as it was read or typed.
  

**Returns**:

  The same command with no leading or trailing blanks.
  

**Raises**:

- `InvalidConfiguration` - Nothing but blanks was given.

<a id="notesmgr.config_files"></a>

# notesmgr.config\_files

Where the user wide configuration of notesmgr is kept.

<a id="notesmgr.config_files.CONFIG_VARIABLE"></a>

#### CONFIG\_VARIABLE

Environment variable in which a user names the configuration file.

<a id="notesmgr.config_files.CONFIG_NAME"></a>

#### CONFIG\_NAME

Name the user wide configuration has in the home folder.

<a id="notesmgr.config_files.user_config_path"></a>

#### user\_config\_path

```python
def user_config_path() -> Path
```

Return the file the user wide configuration is written to.

The file the environment names is the one the user has asked for,
whether it is there yet or not, so that it is also where a first
configuration is written.

<a id="notesmgr.config_files.user_config_source"></a>

#### user\_config\_source

```python
def user_config_source() -> Optional[Path]
```

Return the user wide configuration file to read, None for none.

The file the environment names is read when it is there, and the
file in the home folder when it is not, so that a variable naming
a file that does not exist yet leaves the defaults to be used
rather than making the program refuse to start.

<a id="notesmgr.config_files.copy_to_user_wide"></a>

#### copy\_to\_user\_wide

```python
def copy_to_user_wide(source: Path) -> Path
```

Copy a project's configuration file to the user wide location.

**Arguments**:

- `source` - The project configuration file to copy.
  

**Returns**:

  The user wide configuration file that was written.
  

**Raises**:

- `OSError` - The file could not be read or could not be written.

<a id="notesmgr.config_editor"></a>

# notesmgr.config\_editor

Opening the editor of the notesmgr configuration.

<a id="notesmgr.config_editor.open_config_editor"></a>

#### open\_config\_editor

```python
def open_config_editor(parent: tkinter.Misc,
                       on_close: Callable[[], None]) -> TkEditorPanel
```

Open an editor of the user wide configuration over a window.

The application owns a Tk main loop already, and a second one
would be a second Tcl interpreter that no widget of the first can
reach, so the editor is a panel over the main window rather than
one of the entry points that own a main loop themselves. It
returns at once, and on_close says that the session has ended.

The editor reads the user wide configuration file when there is
one and starts from the built-in defaults when there is not, and
its own Save writes the file the user asked for either way.

**Arguments**:

- `parent` - The window that the editor is shown over.
- `on_close` - Told when the editing session has ended.
  

**Returns**:

  The panel of the session that was started.
  

**Raises**:

- `ConfigLoadError` - The configuration file cannot be edited.

<a id="notesmgr.application"></a>

# notesmgr.application

Start-up of the notesmgr application.

<a id="notesmgr.application.main"></a>

#### main

```python
def main(argv: Optional[list[str]] = None) -> None
```

Run the notesmgr graphical user interface until the user quits.

A command line asking for version information is answered on the
standard output stream, and no window is opened for it.

**Arguments**:

- `argv` - Command line arguments, or None for the ones this
  program was started with.

<a id="notesmgr.config_defaults"></a>

# notesmgr.config\_defaults

The values a notesmgr configuration starts out with.

<a id="notesmgr.config_defaults.VISUAL_CODE"></a>

#### VISUAL\_CODE

Command that starts Microsoft Visual Studio Code.

<a id="notesmgr.config_defaults.EDITOR_VARIABLE"></a>

#### EDITOR\_VARIABLE

Environment variable in which a user names a preferred editor.

<a id="notesmgr.config_defaults.PLATFORM_EDITORS"></a>

#### PLATFORM\_EDITORS

Editor command of the platforms that are known to have one.

<a id="notesmgr.config_defaults.OTHER_EDITOR"></a>

#### OTHER\_EDITOR

Editor command used on a platform that is not known here.

<a id="notesmgr.config_defaults.default_editor"></a>

#### default\_editor

```python
def default_editor() -> str
```

Return the editor command a new configuration starts out with.

Microsoft Visual Studio Code is taken when it is installed, then
the editor the user has named in the environment, and after that
whatever the running platform is known to have. A variable that
holds nothing but blanks names no editor and is passed over.

The command carries no arguments, because the name of the note
file is appended to a command that does not place it itself.

<a id="notesmgr.dialogs"></a>

# notesmgr.dialogs

Windows that notesmgr shows over a window of its own.

<a id="notesmgr.dialogs.MIN_TEXT_WIDTH"></a>

#### MIN\_TEXT\_WIDTH

Narrowest that a window showing a text is made, in characters.

<a id="notesmgr.dialogs.MAX_TEXT_WIDTH"></a>

#### MAX\_TEXT\_WIDTH

Widest that a window showing a text is made, in characters.

<a id="notesmgr.dialogs.MAX_TEXT_HEIGHT"></a>

#### MAX\_TEXT\_HEIGHT

Tallest that a window showing a text is made, in lines.

<a id="notesmgr.dialogs.CLOSE_LABEL"></a>

#### CLOSE\_LABEL

What the button that closes a shown text says.

<a id="notesmgr.dialogs.PADDING"></a>

#### PADDING

Space in pixels left around the button of a shown text.

<a id="notesmgr.dialogs.BUSY_CURSOR"></a>

#### BUSY\_CURSOR

Mouse cursor shown while an answer is being gathered.

<a id="notesmgr.dialogs.text_size"></a>

#### text\_size

```python
def text_size(text: str) -> tuple[int, int]
```

Return the width and height in characters that a text needs.

A window is never made narrower than a short line nor wider or
taller than a screen comfortably holds, so a very long line or a
very long text is scrolled to instead of being shown whole.

**Arguments**:

- `text` - The text that is going to be shown.
  

**Returns**:

  The width in characters and the height in lines.

<a id="notesmgr.dialogs.show_text"></a>

#### show\_text

```python
def show_text(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
              text: str) -> tkinter.Toplevel
```

Show a text that cannot be edited, over another window.

**Arguments**:

- `parent` - The window that the new window is shown over.
- `title` - What the new window is called.
- `text` - What the new window shows.
  

**Returns**:

  The window that was made, which its own button destroys.

<a id="notesmgr.dialogs.show_error"></a>

#### show\_error

```python
def show_error(parent: Union[tkinter.Tk, tkinter.Toplevel], title: str,
               message: str) -> None
```

Tell the user what went wrong, in a window of its own.

**Arguments**:

- `parent` - The window that the message is shown over.
- `title` - What the message window is called.
- `message` - What went wrong.

<a id="notesmgr.dialogs.busy_cursor"></a>

#### busy\_cursor

```python
@contextmanager
def busy_cursor(window: Union[tkinter.Tk, tkinter.Toplevel]) -> Iterator[None]
```

Show the waiting cursor while something slow is being done.

**Arguments**:

- `window` - The window that is going to be busy.
  

**Yields**:

  Nothing. The cursor is put back when the block has ended,
  whether it ended by finishing or by raising.

<a id="notesmgr.descriptions"></a>

# notesmgr.descriptions

What notesmgr says about the members of its configuration.

<a id="notesmgr.descriptions.DESCRIPTIONS"></a>

#### DESCRIPTIONS

What each member of the configuration is for.

Python keeps no docstring of an instance attribute at runtime, so what
a member is for is said here and read by the configuration editor.

The extensions themselves are deliberately not listed here: the editor
reads them from the type of the member and lists them below its row, so
naming them here as well would be writing them twice.

