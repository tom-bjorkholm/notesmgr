#! /usr/local/bin/python3
"""The configuration of notesmgr and the values it accepts."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import sys
from enum import StrEnum
from typing import Optional, TextIO
from config_as_json import CallingMemberValidator, Config, \
    InvalidConfiguration, MemberValidationStep, ParseConverter, PathOrStr, \
    ValidationPlan, ValueTypeValidator
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


class NotesmgrConfig(Config):
    """How notesmgr edits the notes of a project and what it names them.

    The editor command is started whenever a note is edited, and the
    extension is the one that new notes are given and that a file must
    have to be a note at all.
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
        super().__init__(from_json_data_text=from_json_data_text,
                         from_json_filename=from_json_filename,
                         stderr_file=stderr_file, member_name=member_name)

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
        return [MemberValidationStep(member_names=['editor'],
                                     validator=is_text),
                MemberValidationStep(member_names=['editor'],
                                     validator=is_command),
                MemberValidationStep(member_names=['file_extension'],
                                     validator=is_extension)]

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
