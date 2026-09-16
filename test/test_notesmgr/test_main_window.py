#! /usr/local/bin/python3
"""Tests for the notesmgr main window."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Callable, NamedTuple, Optional, Sequence, TextIO
import pytest
from edit_cfg_json import ConfigLoadError
from test_notesmgr.helpers import write_config, write_notes, write_template
from notesmgr import commands as commands_module
from notesmgr import main_window as window_module
from notesmgr.actions import COPY_FORMATTED, COPY_RAW, DELETE, \
    DELETE_FOLDER, DUPLICATE, EDIT, MOVE_DOWN, MOVE_UP, NEW, NEW_FOLDER, \
    RENAME_FOLDER
from notesmgr.config import NoteExtension
from notesmgr.config_files import CONFIG_NAME
from notesmgr.errors import NotesmgrError
from notesmgr.main_window import APPLICATION_NAME, CONFIG_MENU, \
    EDIT_CONFIG_ENTRY, FILE_MENU, FOLDER_MENU, HELP_MENU, INITIAL_GEOMETRY, \
    MINIMUM_HEIGHT, MINIMUM_WIDTH, NEW_PROJECT_ENTRY, NOTE_MENU, \
    OPEN_PROJECT_ENTRY, QUIT_ENTRY, USER_WIDE_ENTRY, VERSION_ENTRY, \
    VERSION_TITLE, MainWindow, Shortcut, quit_shortcut, tk_window_system
from notesmgr.order_file import read_order_text
from notesmgr.project import config_path

REPORT = 'notesmgr 0.0.1\n'
"""What the version report says in these tests."""

NOTES = ['b.md.txt', 'a.md.txt']
"""Notes that the project of these tests holds."""


class ShownText(NamedTuple):
    """One text that the main window asked to have shown."""

    title: str
    text: str


class PanelCall(NamedTuple):
    """What the main window asked the configuration editor to edit."""

    on_close: Callable[[], None]
    config_file: Optional[Path]


@pytest.fixture(name='main_window')
def fixture_main_window(top_window: tkinter.Toplevel) -> MainWindow:
    """Provide a main window built in a hidden toplevel window."""
    return MainWindow(top_window)


@pytest.fixture(name='project')
def fixture_project(tmp_path: Path) -> Path:
    """Provide a project folder holding two notes and a subfolder."""
    root = tmp_path / 'notes'
    write_config(root, NoteExtension.MD_TXT)
    write_template(root, NoteExtension.MD_TXT)
    write_notes(root, NOTES)
    write_notes(root / 'sub', ['deep.md.txt'])
    write_template(root / 'sub', NoteExtension.MD_TXT)
    return root


@pytest.fixture(name='shortcut')
def fixture_shortcut(top_window: tkinter.Toplevel) -> Shortcut:
    """Provide the shortcut that quits on the windowing system in use."""
    return quit_shortcut(tk_window_system(top_window))


@pytest.fixture(name='shown_window')
def fixture_shown_window(main_window: MainWindow) -> MainWindow:
    """Provide a main window that is really shown on the display.

    Only the focus-sensitive tests use this, so the normal test run
    never puts a window on the screen.
    """
    window = main_window.window
    window.deiconify()
    window.lift()
    window.focus_force()
    window.update()
    return main_window


@pytest.fixture(name='panels')
def fixture_panels(monkeypatch: pytest.MonkeyPatch) -> list[PanelCall]:
    """Record the editor sessions that were asked for, opening none."""
    opened: list[PanelCall] = []

    def record(_parent: tkinter.Misc, on_close: Callable[[], None],
               config_file: Optional[Path]) -> object:
        """Stand in for opening the configuration editor panel."""
        opened.append(PanelCall(on_close, config_file))
        return object()
    monkeypatch.setattr(window_module, 'open_config_editor', record)
    return opened


@pytest.fixture(name='no_dialogs', autouse=True)
def fixture_no_dialogs(monkeypatch: pytest.MonkeyPatch) -> None:
    """Let no test of this module put a real dialog on the screen.

    A test that wants another answer than these says so itself, and
    every other test is then sure to open no window that waits for a
    user who is not there.
    """
    _ = answer_folder(monkeypatch, None)
    answer_yes_no(monkeypatch, False)
    answer_choice(monkeypatch, None)
    answer_copy(monkeypatch)


@pytest.fixture(name='refused', autouse=True)
def fixture_refused(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the window and its commands reported as an error."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for reporting an error to the user."""
        told.append(message)
    monkeypatch.setattr(window_module, 'show_error', record)
    monkeypatch.setattr(commands_module, 'show_error', record)
    return told


@pytest.fixture(name='typed', autouse=True)
def fixture_typed(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Let no test of this module ask a real name of a real user.

    Returns:
        The names that a test may put there to be typed next, which
        are taken one by one as the commands ask for them.
    """
    answers: list[str] = []

    def asked(_parent: object, _title: str, _question: str,
              _given: str = '') -> Optional[str]:
        """Stand in for asking the user for a name."""
        return answers.pop(0) if answers else None
    monkeypatch.setattr(commands_module, 'ask_name', asked)
    return answers


@pytest.fixture(name='informed', autouse=True)
def fixture_informed(monkeypatch: pytest.MonkeyPatch) -> list[str]:
    """Record what the main window told the user was worth knowing."""
    told: list[str] = []

    def record(_parent: object, _title: str, message: str) -> None:
        """Stand in for telling the user something."""
        told.append(message)
    monkeypatch.setattr(window_module, 'show_info', record)
    return told


@pytest.fixture(name='shown_texts')
def fixture_shown_texts(monkeypatch: pytest.MonkeyPatch) -> list[ShownText]:
    """Record the texts the main window asked to have shown in a window."""
    shown: list[ShownText] = []

    def record(_parent: object, title: str, text: str) -> None:
        """Stand in for showing a text in a window of its own."""
        shown.append(ShownText(title, text))

    def report(out_file: TextIO) -> None:
        """Stand in for gathering the version report, which is slow."""
        out_file.write(REPORT)
    monkeypatch.setattr(window_module, 'show_text', record)
    monkeypatch.setattr(window_module, 'version_report', report)
    return shown


def answer_folder(monkeypatch: pytest.MonkeyPatch,
                  folder: Optional[Path]) -> list[Path]:
    """Make the folder chooser answer with the given folder.

    Returns:
        The folders that the chooser was asked to start in, which is
        added to every time the chooser is asked.
    """
    started: list[Path] = []

    def chosen(_parent: object, _title: str, start: Path) -> Optional[Path]:
        """Stand in for asking the user for a folder."""
        started.append(start)
        return folder
    monkeypatch.setattr(window_module, 'ask_folder', chosen)
    return started


def answer_yes_no(monkeypatch: pytest.MonkeyPatch, answer: bool) -> None:
    """Make the yes or no question be answered in the given way.

    The window asks it of its own, and so do the commands that its
    buttons and menu entries run, so both are answered here.
    """
    def answered(_parent: object, _title: str, _question: str) -> bool:
        """Stand in for asking the user a question of yes or no."""
        return answer
    monkeypatch.setattr(window_module, 'ask_yes_no', answered)
    monkeypatch.setattr(commands_module, 'ask_yes_no', answered)


def answer_copy(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make the question of where to copy a note be answered with none."""
    def asked(_parent: object, _title: str, _given: object,
              _folders: Sequence[str]) -> None:
        """Stand in for asking the user for a name and a folder."""
        return None
    monkeypatch.setattr(commands_module, 'ask_name_folder', asked)


def answer_choice(monkeypatch: pytest.MonkeyPatch,
                  answer: Optional[str]) -> None:
    """Make the choosing question be answered in the given way."""
    def chosen(_parent: object, _title: str, _question: str,
               _options: Sequence[str]) -> Optional[str]:
        """Stand in for asking the user to choose one of several."""
        return answer
    monkeypatch.setattr(window_module, 'ask_choice', chosen)


def tree_names(main_window: MainWindow) -> list[str]:
    """Return what the explorer shows under the root of the project."""
    tree = main_window.explorer.tree
    root = tree.get_children('')[0]
    return [str(tree.item(child, 'text'))
            for child in tree.get_children(root)]


def test_title_no_project(main_window: MainWindow) -> None:
    """A main window with no open project is titled by the program name."""
    assert main_window.window.title() == APPLICATION_NAME


@pytest.mark.parametrize('project_name,expected', [
    (None, 'notesmgr'),
    ('notes', 'notesmgr — notes'),
    ('My Notes', 'notesmgr — My Notes'),
    ('', 'notesmgr — ')])
def test_title_shows_project(main_window: MainWindow,
                             project_name: Optional[str],
                             expected: str) -> None:
    """The window title names the open project when there is one."""
    main_window.show_project(project_name)
    assert main_window.window.title() == expected


def test_minimum_size(main_window: MainWindow) -> None:
    """The main window may not be made smaller than its minimum size."""
    assert main_window.window.minsize() == (MINIMUM_WIDTH, MINIMUM_HEIGHT)


def test_panes_layout(main_window: MainWindow) -> None:
    """The explorer and the note panel are the panes, in that order."""
    shown = [str(pane) for pane in main_window.panes.winfo_children()]
    assert shown == [str(main_window.explorer.frame),
                     str(main_window.note_panel.frame)]


def test_panes_side_by_side(main_window: MainWindow) -> None:
    """The explorer is placed beside the note panel, not above it."""
    assert str(main_window.panes.cget('orient')) == 'horizontal'


def test_menu_bar_installed(main_window: MainWindow) -> None:
    """The window shows the menu bar that was built for it."""
    window_menu = str(main_window.window.cget('menu'))
    assert window_menu == str(main_window.menu_bar.widget)


def test_menus_of_the_bar(main_window: MainWindow) -> None:
    """The menu bar holds one menu for each kind of thing it does."""
    assert set(main_window.menu_bar.menus) == {FILE_MENU, NOTE_MENU,
                                               FOLDER_MENU, CONFIG_MENU,
                                               HELP_MENU}


@pytest.mark.parametrize('menu,label', [
    (FILE_MENU, NEW_PROJECT_ENTRY),
    (FILE_MENU, OPEN_PROJECT_ENTRY),
    (FILE_MENU, QUIT_ENTRY),
    (NOTE_MENU, EDIT),
    (NOTE_MENU, COPY_RAW),
    (NOTE_MENU, DUPLICATE),
    (NOTE_MENU, NEW),
    (NOTE_MENU, DELETE),
    (NOTE_MENU, MOVE_UP),
    (NOTE_MENU, MOVE_DOWN),
    (FOLDER_MENU, NEW_FOLDER),
    (FOLDER_MENU, RENAME_FOLDER),
    (FOLDER_MENU, DELETE_FOLDER),
    (CONFIG_MENU, EDIT_CONFIG_ENTRY),
    (CONFIG_MENU, USER_WIDE_ENTRY),
    (HELP_MENU, VERSION_ENTRY)])
def test_menu_entries(main_window: MainWindow, menu: str, label: str) -> None:
    """Every menu holds the entries that this step has given it."""
    assert main_window.menu_bar.menus[menu].index(label) is not None


def test_copy_formatted_later(main_window: MainWindow) -> None:
    """What cannot be done yet is no entry of the note menu yet."""
    with pytest.raises(tkinter.TclError):
        main_window.menu_bar.menus[NOTE_MENU].index(COPY_FORMATTED)


def test_user_wide_disabled(main_window: MainWindow) -> None:
    """Copying to the user wide file waits until a project is open."""
    menu = main_window.menu_bar.menus[CONFIG_MENU]
    assert menu.entrycget(USER_WIDE_ENTRY, 'state') == 'disabled'


def note_entry_state(main_window: MainWindow, label: str) -> str:
    """Return whether one entry of the note menu can be chosen."""
    menu = main_window.menu_bar.menus[NOTE_MENU]
    return str(menu.entrycget(label, 'state'))


def folder_entry_state(main_window: MainWindow, label: str) -> str:
    """Return whether one entry of the folder menu can be chosen."""
    menu = main_window.menu_bar.menus[FOLDER_MENU]
    return str(menu.entrycget(label, 'state'))


def order_of(folder: Path) -> list[str]:
    """Return the notes that the order file of a folder lists."""
    text = read_order_text(folder)
    return [] if text is None else text.splitlines()


@pytest.mark.parametrize('label', [EDIT, COPY_RAW])
def test_note_entries_dead(main_window: MainWindow, label: str) -> None:
    """With nothing selected there is no note for an entry to act on."""
    assert note_entry_state(main_window, label) == 'disabled'


@pytest.mark.parametrize('label', [EDIT, COPY_RAW])
def test_note_entries_offered(main_window: MainWindow, project: Path,
                              label: str) -> None:
    """Selecting a note offers the entries that act on one."""
    main_window.load_project(project)
    main_window.show_selected(project / NOTES[0])
    assert note_entry_state(main_window, label) == 'normal'


def test_note_entries_off(main_window: MainWindow, project: Path) -> None:
    """Selecting a folder after a note leaves nothing to act on."""
    main_window.load_project(project)
    main_window.show_selected(project / NOTES[0])
    main_window.show_selected(project)
    assert note_entry_state(main_window, EDIT) == 'disabled'


def test_opening_selects_none(main_window: MainWindow, project: Path) -> None:
    """A project that has just been opened has nothing selected in it."""
    main_window.load_project(project)
    assert main_window.note_panel.shown_path() == ''
    assert note_entry_state(main_window, COPY_RAW) == 'disabled'


def test_folder_entries_dead(main_window: MainWindow) -> None:
    """With no project open there is no folder for an entry to act on."""
    for label in (NEW_FOLDER, RENAME_FOLDER, DELETE_FOLDER):
        assert folder_entry_state(main_window, label) == 'disabled'


def test_new_folder_offered(main_window: MainWindow, project: Path) -> None:
    """A project that is open is a project to make a folder in."""
    main_window.load_project(project)
    assert folder_entry_state(main_window, NEW_FOLDER) == 'normal'
    assert folder_entry_state(main_window, RENAME_FOLDER) == 'disabled'


def test_folder_entries_on(main_window: MainWindow, project: Path) -> None:
    """Selecting a folder of the project offers what acts on one."""
    main_window.load_project(project)
    main_window.show_selected(project / 'sub')
    assert folder_entry_state(main_window, RENAME_FOLDER) == 'normal'
    assert folder_entry_state(main_window, DELETE_FOLDER) == 'normal'


def test_root_is_no_folder(main_window: MainWindow, project: Path) -> None:
    """The root folder is the project, and is not renamed or removed."""
    main_window.load_project(project)
    main_window.show_selected(project)
    assert folder_entry_state(main_window, RENAME_FOLDER) == 'disabled'


def test_panel_errors_told(main_window: MainWindow, project: Path,
                           refused: list[str],
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """What a command could not do is put to the user."""
    monkeypatch.setattr(commands_module, 'launch_editor', no_editor)
    main_window.load_project(project)
    main_window.show_selected(project / NOTES[0])
    main_window.menu_bar.menus[NOTE_MENU].invoke(EDIT)
    assert refused == ['no editor here']


def no_editor(_command: str, _path: Path) -> None:
    """Stand in for an editor that the system does not start."""
    raise NotesmgrError('no editor here')


def test_new_note_from_menu(main_window: MainWindow, project: Path,
                            typed: list[str],
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing Note > New makes a note and selects it in the tree."""
    started: list[Path] = []

    def record(_command: str, path: Path) -> None:
        """Stand in for starting the editor of the project."""
        started.append(path)
    monkeypatch.setattr(commands_module, 'launch_editor', record)
    main_window.load_project(project)
    typed.append('third')
    main_window.menu_bar.menus[NOTE_MENU].invoke(NEW)
    made = project / 'third.md.txt'
    assert made.is_file()
    assert started == [made]
    assert main_window.explorer.selected_path() == made
    assert main_window.note_panel.note_path() == made


def test_delete_from_menu(main_window: MainWindow, project: Path,
                          trashed: list[Path],
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing Note > Delete takes the note away and shows the rest."""
    answer_yes_no(monkeypatch, True)
    main_window.load_project(project)
    main_window.show_selected(project / NOTES[0])
    main_window.menu_bar.menus[NOTE_MENU].invoke(DELETE)
    assert trashed == [project / NOTES[0]]
    assert tree_names(main_window) == ['sub', 'template.md.txt', NOTES[1]]
    assert main_window.note_panel.shown_path() == ''


def test_move_from_menu(main_window: MainWindow, project: Path) -> None:
    """Choosing Note > Up moves the note and leaves it selected."""
    main_window.load_project(project)
    main_window.show_selected(project / NOTES[1])
    main_window.menu_bar.menus[NOTE_MENU].invoke(MOVE_UP)
    assert order_of(project) == [NOTES[1], NOTES[0]]
    assert main_window.explorer.selected_path() == project / NOTES[1]


def test_new_folder_from_menu(main_window: MainWindow, project: Path,
                              typed: list[str]) -> None:
    """Choosing Folder > New folder makes a folder and shows it."""
    main_window.load_project(project)
    typed.append('ideas')
    main_window.menu_bar.menus[FOLDER_MENU].invoke(NEW_FOLDER)
    assert (project / 'ideas' / 'template.md.txt').is_file()
    assert main_window.explorer.selected_path() == project / 'ideas'


def test_reopen_no_project(main_window: MainWindow) -> None:
    """With no project open there is nothing to show again."""
    main_window.reopen(None)
    assert main_window.session.project is None


def test_select_what_is_gone(main_window: MainWindow, project: Path) -> None:
    """Selecting what the tree does not show selects nothing at all."""
    main_window.load_project(project)
    main_window.select(project / 'no_such.md.txt')
    assert main_window.explorer.selected_path() is None
    assert main_window.note_panel.shown_path() == ''


def test_copy_raw_from_menu(main_window: MainWindow, project: Path) -> None:
    """Choosing Note > Copy raw copies the note that is selected."""
    note = project / NOTES[0]
    main_window.load_project(project)
    main_window.show_selected(note)
    main_window.menu_bar.menus[NOTE_MENU].invoke(COPY_RAW)
    assert main_window.window.clipboard_get() == \
        note.read_text(encoding='utf-8')


def test_edit_from_menu(main_window: MainWindow, project: Path,
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing Note > Edit starts the editor on the note selected."""
    started: list[Path] = []

    def record(_command: str, path: Path) -> None:
        """Stand in for starting the editor of the project."""
        started.append(path)
    monkeypatch.setattr(commands_module, 'launch_editor', record)
    note = project / NOTES[0]
    main_window.load_project(project)
    main_window.show_selected(note)
    main_window.menu_bar.menus[NOTE_MENU].invoke(EDIT)
    assert started == [note]


def test_edit_config_offered(main_window: MainWindow) -> None:
    """Editing the configuration can be chosen with no project open."""
    menu = main_window.menu_bar.menus[CONFIG_MENU]
    assert menu.entrycget(EDIT_CONFIG_ENTRY, 'state') == 'normal'


@pytest.mark.parametrize('window_system,expected', [
    ('aqua', Shortcut('<Command-w>', 'Cmd+W')),
    ('win32', Shortcut('<Control-q>', 'Ctrl+Q')),
    ('x11', Shortcut('<Control-q>', 'Ctrl+Q')),
    ('', Shortcut('<Control-q>', 'Ctrl+Q'))])
def test_quit_shortcut(window_system: str, expected: Shortcut) -> None:
    """The shortcut is Cmd+W on macOS and Ctrl+Q on other systems."""
    assert quit_shortcut(window_system) == expected


def test_window_system_known(top_window: tkinter.Toplevel) -> None:
    """Tk reports one of the three windowing systems that it supports."""
    assert tk_window_system(top_window) in ('aqua', 'win32', 'x11')


def test_quit_accelerator(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The Quit entry shows the shortcut that the window listens for."""
    menu = main_window.menu_bar.menus[FILE_MENU]
    assert menu.entrycget(QUIT_ENTRY, 'accelerator') == shortcut.label


def test_quit_key_bound(main_window: MainWindow, shortcut: Shortcut) -> None:
    """The window itself listens for the shortcut, as Tk binds none."""
    assert main_window.window.bind(shortcut.sequence)


def test_quit_destroys(main_window: MainWindow) -> None:
    """Quitting destroys the window."""
    main_window.quit()
    assert not main_window.window.winfo_exists()


def test_quit_from_menu(main_window: MainWindow) -> None:
    """Choosing File > Quit destroys the window."""
    window = main_window.window
    main_window.menu_bar.menus[FILE_MENU].invoke(QUIT_ENTRY)
    assert not window.winfo_exists()


def test_nothing_open_first(main_window: MainWindow) -> None:
    """A main window starts with no project and an empty explorer."""
    assert main_window.session.project is None
    assert main_window.session.config_file() is None
    assert not main_window.explorer.tree.get_children('')


def test_project_is_shown(main_window: MainWindow, project: Path,
                          informed: list[str]) -> None:
    """An opened project is named in the title and shown in the tree."""
    main_window.load_project(project)
    assert main_window.window.title() == f'{APPLICATION_NAME} — notes'
    assert tree_names(main_window) == ['sub', 'template.md.txt', 'a.md.txt',
                                       'b.md.txt']
    assert not informed


def test_project_config_known(main_window: MainWindow, project: Path) -> None:
    """The configuration file of the open project is the one in use."""
    main_window.load_project(project)
    assert main_window.session.config_file() == config_path(project)


def test_user_wide_offered(main_window: MainWindow, project: Path) -> None:
    """Copying to the user wide file can be chosen once a project is open."""
    main_window.load_project(project)
    menu = main_window.menu_bar.menus[CONFIG_MENU]
    assert menu.entrycget(USER_WIDE_ENTRY, 'state') == 'normal'


def test_opening_is_refused(main_window: MainWindow, tmp_path: Path,
                            refused: list[str]) -> None:
    """A folder that is no project is reported, and nothing is opened."""
    main_window.load_project(tmp_path)
    assert len(refused) == 1
    assert main_window.session.project is None


def test_changes_are_told(main_window: MainWindow, project: Path,
                          informed: list[str]) -> None:
    """A template that opening the project wrote is told about."""
    (project / 'template.md.txt').unlink()
    main_window.load_project(project)
    assert len(informed) == 1
    assert 'template.md.txt' in informed[0]


def test_open_from_dialog(main_window: MainWindow, project: Path,
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing File > Open project opens the folder that was chosen."""
    answer_folder(monkeypatch, project)
    main_window.menu_bar.menus[FILE_MENU].invoke(OPEN_PROJECT_ENTRY)
    assert main_window.session.project is not None
    assert main_window.session.project.root == project


def test_open_none_chosen(main_window: MainWindow, refused: list[str],
                          monkeypatch: pytest.MonkeyPatch) -> None:
    """Choosing no folder at all opens nothing and reports nothing."""
    answer_folder(monkeypatch, None)
    main_window.open_project_dialog()
    assert main_window.session.project is None
    assert not refused


def test_new_from_dialog(main_window: MainWindow, tmp_path: Path,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """A folder of notes that is no project yet is made into one."""
    root = tmp_path / 'fresh'
    write_notes(root, NOTES)
    answer_folder(monkeypatch, root)
    main_window.menu_bar.menus[FILE_MENU].invoke(NEW_PROJECT_ENTRY)
    assert main_window.session.project is not None
    assert config_path(root).is_file()
    assert tree_names(main_window) == ['template.md.txt', 'a.md.txt',
                                       'b.md.txt']


def test_new_on_project(main_window: MainWindow, project: Path,
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """A folder that is a project already is offered to be opened."""
    answer_folder(monkeypatch, project)
    answer_yes_no(monkeypatch, True)
    main_window.new_project_dialog()
    assert main_window.session.project is not None
    assert main_window.session.project.root == project


def test_new_on_project_no(main_window: MainWindow, project: Path,
                           monkeypatch: pytest.MonkeyPatch) -> None:
    """Saying no to opening it instead leaves the project unopened."""
    answer_folder(monkeypatch, project)
    answer_yes_no(monkeypatch, False)
    main_window.new_project_dialog()
    assert main_window.session.project is None


def test_chooser_at_cwd(main_window: MainWindow,
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """With no project opened yet, a chooser starts where the run began."""
    started = answer_folder(monkeypatch, None)
    main_window.open_project_dialog()
    main_window.new_project_dialog()
    assert started == [Path.cwd(), Path.cwd()]


def test_chooser_after_open(main_window: MainWindow, project: Path,
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """Once a project has been opened, a chooser starts in that project."""
    main_window.load_project(project)
    started = answer_folder(monkeypatch, None)
    main_window.open_project_dialog()
    main_window.new_project_dialog()
    assert started == [project, project]


def test_chooser_if_refused(main_window: MainWindow, tmp_path: Path,
                            monkeypatch: pytest.MonkeyPatch) -> None:
    """A folder that was no project is no place to start looking again."""
    main_window.load_project(tmp_path)
    started = answer_folder(monkeypatch, None)
    main_window.open_project_dialog()
    assert started == [Path.cwd()]


def test_template_chosen(main_window: MainWindow, project: Path,
                         monkeypatch: pytest.MonkeyPatch) -> None:
    """The template to keep is asked for with the names of the templates."""
    asked: list[Sequence[str]] = []

    def choose(_parent: object, _title: str, _question: str,
               options: Sequence[str]) -> str:
        """Stand in for a user choosing which template to keep."""
        asked.append(options)
        return options[0]
    monkeypatch.setattr(window_module, 'ask_choice', choose)
    write_template(project, NoteExtension.TXT)
    chosen = main_window.choose_template(project,
                                         [project / 'template.md.txt',
                                          project / 'template.txt'])
    assert asked == [['template.md.txt', 'template.txt']]
    assert chosen == project / 'template.md.txt'


def test_template_not_chosen(main_window: MainWindow, project: Path) -> None:
    """Choosing no template at all is passed on as choosing none.

    The dialogs of this module answer nothing at all unless a test
    says otherwise, so this is what a cancelled question gives.
    """
    assert main_window.choose_template(project, []) is None


def test_editor_opened(main_window: MainWindow,
                       panels: list[PanelCall]) -> None:
    """Choosing to edit the configuration opens one editor session."""
    main_window.menu_bar.menus[CONFIG_MENU].invoke(EDIT_CONFIG_ENTRY)
    assert len(panels) == 1
    assert main_window.config_panel is not None


def test_editor_of_user_wide(main_window: MainWindow,
                             panels: list[PanelCall]) -> None:
    """With no project open the user wide configuration is edited."""
    main_window.edit_configuration()
    assert panels[0].config_file is None


def test_editor_of_project(main_window: MainWindow, project: Path,
                           panels: list[PanelCall]) -> None:
    """With a project open its own configuration file is edited."""
    main_window.load_project(project)
    main_window.edit_configuration()
    assert panels[0].config_file == config_path(project)


def test_one_editor_at_a_time(main_window: MainWindow,
                              panels: list[PanelCall]) -> None:
    """A second editor is not opened while the first one is still open."""
    main_window.edit_configuration()
    main_window.edit_configuration()
    assert len(panels) == 1


def test_editor_reopened(main_window: MainWindow,
                         panels: list[PanelCall]) -> None:
    """Once a session has ended, the editor can be opened again."""
    main_window.edit_configuration()
    panels[0].on_close()
    assert main_window.config_panel is None
    main_window.edit_configuration()
    assert len(panels) == 2


def test_project_read_again(main_window: MainWindow, project: Path,
                            panels: list[PanelCall]) -> None:
    """An edited configuration is taken up by the open project.

    The extension of the notes is what the configuration says, so the
    template is renamed once the configuration names another one.
    """
    main_window.load_project(project)
    main_window.edit_configuration()
    write_config(project, NoteExtension.MD)
    panels[0].on_close()
    assert tree_names(main_window) == ['sub', 'template.md', 'a.md.txt',
                                       'b.md.txt']


def test_editor_refused(main_window: MainWindow, refused: list[str],
                        monkeypatch: pytest.MonkeyPatch) -> None:
    """A configuration file that cannot be edited is reported, not raised."""
    def refuse(_parent: tkinter.Misc, _on_close: Callable[[], None],
               _config_file: Optional[Path]) -> object:
        """Stand in for an editor that refuses the configuration file."""
        raise ConfigLoadError('the file holds no configuration')
    monkeypatch.setattr(window_module, 'open_config_editor', refuse)
    main_window.edit_configuration()
    assert refused == ['the file holds no configuration']
    assert main_window.config_panel is None


def test_user_wide_without(main_window: MainWindow, home: Path) -> None:
    """With no project open there is no configuration file to copy."""
    main_window.save_user_wide()
    assert not (home / CONFIG_NAME).exists()


def test_user_wide_copied(main_window: MainWindow, home: Path,
                          project: Path) -> None:
    """The project's configuration file becomes the user wide one."""
    main_window.load_project(project)
    main_window.save_user_wide()
    written = (home / CONFIG_NAME).read_text(encoding='utf-8')
    assert written == config_path(project).read_text(encoding='utf-8')


def test_user_wide_refused(main_window: MainWindow, project: Path,
                           refused: list[str]) -> None:
    """A copy that cannot be made is reported, and does not raise."""
    main_window.load_project(project)
    config_path(project).unlink()
    main_window.save_user_wide()
    assert len(refused) == 1


def test_version_shown(main_window: MainWindow,
                       shown_texts: list[ShownText]) -> None:
    """Choosing version information shows the report in a window."""
    main_window.menu_bar.menus[HELP_MENU].invoke(VERSION_ENTRY)
    assert shown_texts == [ShownText(VERSION_TITLE, REPORT)]


def test_cursor_after_version(main_window: MainWindow,
                              shown_texts: list[ShownText]) -> None:
    """The waiting cursor is gone once the report has been gathered."""
    main_window.show_version()
    assert len(shown_texts) == 1
    assert str(main_window.window.cget('cursor')) == ''


@pytest.mark.focus_sensitive
def test_shown_window_size(shown_window: MainWindow) -> None:
    """A shown main window gets the size it asked for."""
    assert shown_window.window.geometry().startswith(INITIAL_GEOMETRY)


@pytest.mark.focus_sensitive
def test_buttons_all_shown(shown_window: MainWindow) -> None:
    """Every button of the panel is shown whole at the initial size.

    The buttons are as wide as the theme of the platform makes them,
    and the row lays them out in as many rows as it needs, so none of
    them is cut off at the edge of the panel.
    """
    row = shown_window.note_panel.row
    shown_window.window.update()
    width = row.frame.winfo_width()
    over = [button for button in row.buttons
            if button.winfo_x() + button.winfo_width() > width]
    assert not over


@pytest.mark.focus_sensitive
def test_narrow_window_wraps(shown_window: MainWindow) -> None:
    """A window made small lays the buttons out in several rows."""
    window = shown_window.window
    window.geometry(f'{MINIMUM_WIDTH}x{MINIMUM_HEIGHT}')
    window.update()
    row = shown_window.note_panel.row
    assert row.columns < len(row.buttons)
    assert max(button.winfo_x() + button.winfo_width()
               for button in row.buttons) <= row.frame.winfo_width()


@pytest.mark.focus_sensitive
def test_shown_window_panes(shown_window: MainWindow) -> None:
    """The explorer is shown narrow and to the left of the note panel."""
    explorer = shown_window.explorer.frame
    note_panel = shown_window.note_panel.frame
    assert explorer.winfo_x() < note_panel.winfo_x()
    assert explorer.winfo_width() < note_panel.winfo_width()


@pytest.mark.focus_sensitive
def test_window_gets_focus(shown_window: MainWindow) -> None:
    """A shown main window can take the keyboard focus."""
    window = shown_window.window
    focused = window.focus_get()
    assert focused is not None
    assert str(focused).startswith(str(window))


@pytest.mark.focus_sensitive
def test_shortcut_quits(shown_window: MainWindow, shortcut: Shortcut) -> None:
    """Pressing the shortcut closes a main window that has the focus."""
    window = shown_window.window
    window.event_generate(shortcut.sequence, when='now')
    assert not window.winfo_exists()
