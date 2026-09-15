#! /usr/local/bin/python3
"""The values a notesmgr configuration starts out with."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import shutil
import sys

VISUAL_CODE = 'code'
"""Command that starts Microsoft Visual Studio Code."""

VISUAL_CODE_FLAG = ' -n'
"""Flag to open a new window in Microsoft Visual Studio Code."""

EDITOR_VARIABLE = 'EDITOR'
"""Environment variable in which a user names a preferred editor."""

PLATFORM_EDITORS = {'darwin': 'open', 'win32': 'notepad'}
"""Editor command of the platforms that are known to have one."""

OTHER_EDITOR = 'emacs'
"""Editor command used on a platform that is not known here."""


def default_editor() -> str:
    """Return the editor command a new configuration starts out with.

    Microsoft Visual Studio Code is taken when it is installed, then
    the editor the user has named in the environment, and after that
    whatever the running platform is known to have. A variable that
    holds nothing but blanks names no editor and is passed over.

    The command carries no arguments, because the name of the note
    file is appended to a command that does not place it itself.
    """
    if shutil.which(VISUAL_CODE) is not None:
        return VISUAL_CODE + VISUAL_CODE_FLAG
    named = os.environ.get(EDITOR_VARIABLE, '').strip()
    return named or PLATFORM_EDITORS.get(sys.platform, OTHER_EDITOR)
