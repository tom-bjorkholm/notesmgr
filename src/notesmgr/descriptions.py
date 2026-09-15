#! /usr/local/bin/python3
"""What notesmgr says about the members of its configuration."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from edit_cfg_json import Descriptions

DESCRIPTIONS: Descriptions = {
    ('editor',): ('Command that opens a note for editing. The name of the '
                  'note file replaces {file} in the command, and is added '
                  'at the end of a command that holds no {file}.'),
    ('file_extension',): ('Extension of the note files of a project. The '
                          'configuration file holds the name below, and '
                          'not the extension it stands for.'),
    ('max_note_size',): ('Characters of a note that are shown. A longer '
                         'note is shown only up to here, with a warning '
                         'saying so. Between 2000 and 100000.')}
"""What each member of the configuration is for.

Python keeps no docstring of an instance attribute at runtime, so what
a member is for is said here and read by the configuration editor.

The extensions themselves are deliberately not listed here: the editor
reads them from the type of the member and lists them below its row, so
naming them here as well would be writing them twice.
"""
