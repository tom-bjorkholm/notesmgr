#! /usr/local/bin/python3
"""Opening the editor of the notesmgr configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from pathlib import Path
from typing import Callable, Optional
from edit_cfg_json_tk import TkEditorPanel
from notesmgr.config import NotesmgrConfig
from notesmgr.config_files import user_config_path, user_config_source
from notesmgr.descriptions import DESCRIPTIONS


def editor_files(config_file: Optional[Path]) -> tuple[Optional[Path], Path]:
    """Return the files that the configuration editor reads and writes.

    The configuration of a project is read and written in the one
    place it lives. The user wide configuration is read where there is
    one and started from the built-in defaults where there is not,
    while it is written to the file the user asked for either way.

    Args:
        config_file: The configuration file of the open project, None
            when no project is open.

    Returns:
        The file to read, None for the built-in defaults, and the file
        to write.
    """
    if config_file is None:
        return user_config_source(), user_config_path()
    return config_file, config_file


def open_config_editor(parent: tkinter.Misc, on_close: Callable[[], None],
                       config_file: Optional[Path] = None) -> TkEditorPanel:
    """Open an editor of the configuration in use, over a window.

    The application owns a Tk main loop already, and a second one
    would be a second Tcl interpreter that no widget of the first can
    reach, so the editor is a panel over the main window rather than
    one of the entry points that own a main loop themselves. It
    returns at once, and on_close says that the session has ended.

    Args:
        parent: The window that the editor is shown over.
        on_close: Told when the editing session has ended.
        config_file: The configuration file of the open project, None
            for editing the user wide configuration.

    Returns:
        The panel of the session that was started.

    Raises:
        ConfigLoadError: The configuration file cannot be edited.
    """
    in_file, out_file = editor_files(config_file)
    return TkEditorPanel(NotesmgrConfig(), parent=parent,
                         descriptions=DESCRIPTIONS, in_file=in_file,
                         out_file=out_file, on_close=on_close)
