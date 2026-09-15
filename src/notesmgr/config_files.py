#! /usr/local/bin/python3
"""Where the user wide configuration of notesmgr is kept."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import os
import shutil
from pathlib import Path
from typing import Optional

CONFIG_VARIABLE = 'NOTESMGR_CFG'
"""Environment variable in which a user names the configuration file."""

CONFIG_NAME = '.notesmgr.cfg'
"""Name the user wide configuration has in the home folder."""


def user_config_path() -> Path:
    """Return the file the user wide configuration is written to.

    The file the environment names is the one the user has asked for,
    whether it is there yet or not, so that it is also where a first
    configuration is written.
    """
    named = os.environ.get(CONFIG_VARIABLE, '').strip()
    return Path(named) if named else Path.home() / CONFIG_NAME


def user_config_source() -> Optional[Path]:
    """Return the user wide configuration file to read, None for none.

    The file the environment names is read when it is there, and the
    file in the home folder when it is not, so that a variable naming
    a file that does not exist yet leaves the defaults to be used
    rather than making the program refuse to start.
    """
    named = user_config_path()
    if named.is_file():
        return named
    in_home = Path.home() / CONFIG_NAME
    return in_home if in_home.is_file() else None


def copy_to_user_wide(source: Path) -> Path:
    """Copy a project's configuration file to the user wide location.

    Args:
        source: The project configuration file to copy.

    Returns:
        The user wide configuration file that was written.

    Raises:
        OSError: The file could not be read or could not be written.
    """
    target = user_config_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return target
