#! /usr/local/bin/python3
"""Opening the editor of the notesmgr configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import tkinter
from typing import Callable
from edit_cfg_json_tk import TkEditorPanel
from notesmgr.config import NotesmgrConfig
from notesmgr.config_files import user_config_path, user_config_source
from notesmgr.descriptions import DESCRIPTIONS


def open_config_editor(parent: tkinter.Misc,
                       on_close: Callable[[], None]) -> TkEditorPanel:
    """Open an editor of the user wide configuration over a window.

    The application owns a Tk main loop already, and a second one
    would be a second Tcl interpreter that no widget of the first can
    reach, so the editor is a panel over the main window rather than
    one of the entry points that own a main loop themselves. It
    returns at once, and on_close says that the session has ended.

    The editor reads the user wide configuration file when there is
    one and starts from the built-in defaults when there is not, and
    its own Save writes the file the user asked for either way.

    Args:
        parent: The window that the editor is shown over.
        on_close: Told when the editing session has ended.

    Returns:
        The panel of the session that was started.

    Raises:
        ConfigLoadError: The configuration file cannot be edited.
    """
    return TkEditorPanel(NotesmgrConfig(), parent=parent,
                         descriptions=DESCRIPTIONS,
                         in_file=user_config_source(),
                         out_file=user_config_path(), on_close=on_close)
