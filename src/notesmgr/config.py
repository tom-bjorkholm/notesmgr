#! /usr/local/bin/python3
"""The configuration of notesmgr and the values it accepts."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from enum import StrEnum
from typing import Optional, TextIO
from config_as_json import CallingMemberValidator, Config, ConfigPath, \
    IntFloatValidator, InvalidConfiguration, MemberValidationStep, \
    ParseConverter, PathOrStr, ReadOldConfiguration, ValidationPlan, \
    ValueTypeValidator
from notesmgr.config_defaults import default_editor

EMPTY_EDITOR = 'The editor command must name a program to start.'
"""What is said about an editor command that holds no command."""


class NoteExtension(StrEnum):
    """Note file extension: MD is .md, TXT is .txt, MD_TXT is .md.txt.

    The configuration file holds the name of one of these members,
    while the value of the member is the extension itself. MD_TXT is
    the default, because many systems do not recognize .md as a safe
    file type.
    """

    MD = '.md'
    TXT = '.txt'
    MD_TXT = '.md.txt'


DEFAULT_EXTENSION = NoteExtension.MD_TXT
"""Note file extension that a new configuration starts out with."""

DEFAULT_NOTE_SIZE = 25000
"""Characters of a note that are shown when nothing else is said."""

MIN_NOTE_SIZE = 2000
"""Fewest characters of a note that may be asked to be shown.

A note is meant to be read whole, so a limit small enough to cut a
short note in two is taken for a misunderstanding rather than a wish.
"""

MAX_NOTE_SIZE = 100000
"""Most characters of a note that may be asked to be shown.

Reading a note is meant to stay quick, and a window that has to draw
far more than this is no longer a notes manager to work in.
"""


class OldNotesmgrConfig(ReadOldConfiguration):
    """How a configuration file of an older notesmgr is read.

    Every member of the configuration has to be named in the file,
    so a file written before a member existed is read with the
    built-in default of that member rather than being refused.
    """

    def get_missing_path_values(self) -> dict[ConfigPath, object]:
        """Add configuration parameter for things missing in old files.

        This is only relevant for configuration parameters that
        have been added after the first **released** version of notesmgr.
        """
        return {}


class NotesmgrConfig(Config):
    """How notesmgr edits the notes of a project and what it names them.

    The editor command is started whenever a note is edited, the
    extension is the one that new notes are given and that a file must
    have to be a note at all, and the size is how much of a note is
    shown before the rest of it is left out.
    """

    def __init__(self, from_json_data_text: Optional[str] = None,
                 from_json_filename: Optional[PathOrStr] = None,
                 stderr_file: TextIO = sys.stderr,
                 member_name: Optional[str] = None) -> None:
        """Construct the configuration with its default values.

        Args:
            from_json_data_text: Optional JSON text to parse directly.
            from_json_filename: Optional path to a JSON file to read.
            stderr_file: Stream used for user-facing diagnostics.
            member_name: Path for reaching this object from the top
                level configuration, None for the top level itself.
        """
        self.editor: str = default_editor()
        self.file_extension: NoteExtension = DEFAULT_EXTENSION
        self.max_note_size: int = DEFAULT_NOTE_SIZE
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

    def _get_read_old_config(self) -> ReadOldConfiguration:
        """Return how a file of an older notesmgr is read."""
        return OldNotesmgrConfig()

    def parse_converters(self) -> dict[str, ParseConverter]:
        """Return how the name in the file becomes an extension again.

        Declaring it is also what lets the configuration editor offer
        the extensions to be chosen instead of to be spelled.
        """
        return {'file_extension': Config.get_converter_dict(NoteExtension)}

    def get_validation_plan(self, stderr_file: TextIO) -> ValidationPlan:
        """Return the checks that every configuration has to pass."""
        _ = stderr_file
        is_text = ValueTypeValidator(str)
        is_extension = ValueTypeValidator(NoteExtension)
        is_command = CallingMemberValidator(method_name='stripped_editor',
                                            arg_name_value='value',
                                            normalizing=True)
        is_whole = ValueTypeValidator(int, not_allowed_type=bool)
        in_range = IntFloatValidator(min_value=MIN_NOTE_SIZE,
                                     max_value=MAX_NOTE_SIZE,
                                     allowed_values=None)
        return [MemberValidationStep(member_names=['editor'],
                                     validator=is_text),
                MemberValidationStep(member_names=['editor'],
                                     validator=is_command),
                MemberValidationStep(member_names=['file_extension'],
                                     validator=is_extension),
                MemberValidationStep(member_names=['max_note_size'],
                                     validator=is_whole),
                MemberValidationStep(member_names=['max_note_size'],
                                     validator=in_range)]

    def stripped_editor(self, value: object) -> str:
        """Return the editor command without the blanks around it.

        Args:
            value: The editor command as it was read or typed.

        Returns:
            The same command with no leading or trailing blanks.

        Raises:
            InvalidConfiguration: Nothing but blanks was given.
        """
        assert isinstance(value, str)
        command = value.strip()
        if not command:
            raise InvalidConfiguration(EMPTY_EDITOR)
        return command
