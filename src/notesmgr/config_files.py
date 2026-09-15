#! /usr/local/bin/python3
"""Where the user wide configuration of notesmgr is kept."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
import os
import shutil
from pathlib import Path
from typing import Optional
from notesmgr.config import NotesmgrConfig
from notesmgr.errors import NotesmgrError

CONFIG_VARIABLE = 'NOTESMGR_CFG'
"""Environment variable in which a user names the configuration file."""

CONFIG_NAME = '.notesmgr.cfg'
"""Name the user wide configuration has in the home folder."""

MISSING = 'There is no configuration file {path}.'
"""What is said about a configuration file that is not there."""

NOT_READ = 'The configuration file {path} cannot be used.\n{reason}'
"""What is said about a configuration file that cannot be read."""

NOT_WRITTEN = 'The configuration file {path} cannot be written.\n{reason}'
"""What is said about a configuration file that cannot be written."""


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


def config_error(template: str, path: Path, said: str,
                 error: Exception) -> NotesmgrError:
    """Return what to raise when a configuration file cannot be used.

    What the configuration library said while it was failing tells the
    user far more than the exception does, so it is what is shown when
    there is any, and the exception is what is shown when there is not.

    Args:
        template: What is said about the file, holding path and reason.
        path: The configuration file that could not be used.
        said: What the configuration library reported while failing.
        error: What the configuration library raised.

    Returns:
        The error to raise, said in words meant for the user.
    """
    reason = said or str(error)
    return NotesmgrError(template.format(path=path, reason=reason))


def read_config_file(path: Path) -> NotesmgrConfig:
    """Return the configuration that a file holds.

    Args:
        path: The configuration file to read.

    Returns:
        The configuration it holds.

    Raises:
        NotesmgrError: There is no such file, or it holds no
            configuration that notesmgr can use.
    """
    if not path.is_file():
        raise NotesmgrError(MISSING.format(path=path))
    said = io.StringIO()
    try:
        return NotesmgrConfig(from_json_filename=path, stderr_file=said)
    except (ValueError, KeyError, OSError) as error:
        raise config_error(NOT_READ, path, said.getvalue(), error) from error


def write_config_file(config: NotesmgrConfig, path: Path) -> None:
    """Write a configuration to a file, replacing what was there.

    Args:
        config: The configuration to write.
        path: The configuration file to write it to.

    Raises:
        NotesmgrError: The file cannot be written.
    """
    said = io.StringIO()
    try:
        config.write(path, stderr_file=said)
    except (ValueError, KeyError, OSError) as error:
        raise config_error(NOT_WRITTEN, path, said.getvalue(),
                           error) from error


def user_wide_config() -> NotesmgrConfig:
    """Return the user wide configuration, or the built-in defaults.

    Returns:
        What a new project starts its own configuration out as.

    Raises:
        NotesmgrError: There is a user wide configuration file and it
            holds no configuration that notesmgr can use.
    """
    source = user_config_source()
    return NotesmgrConfig() if source is None else read_config_file(source)
