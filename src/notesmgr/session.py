#! /usr/local/bin/python3
"""What one run of the notesmgr application knows."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
from notesmgr.project import Project, config_path


def start_folder() -> Path:
    """Return the folder the application was started from.

    A folder that has been taken away while the program was starting
    is no place to look for notes in, so the home folder stands in
    for it rather than letting the program fail to start.
    """
    try:
        return Path.cwd()
    except OSError:
        return Path.home()


class Session:
    """The open project of one run, and where to look for the next one.

    notesmgr remembers no project from one run to the next, but within
    one run it remembers where the user was last looking: a folder
    chooser starts in the project that was opened last, and in the
    folder the application was started from until one has been.
    """

    def __init__(self, folder: Optional[Path] = None) -> None:
        """Begin a session in which no project has been opened yet.

        Args:
            folder: Where a folder chooser starts until a project has
                been opened, None for the folder the application was
                started from.
        """
        self.project: Optional[Project] = None
        self.folder = start_folder() if folder is None else folder

    def opened(self, project: Project) -> None:
        """Take a project as the one that is open from now on."""
        self.project = project

    def chooser_folder(self) -> Path:
        """Return the folder that a folder chooser is to start in."""
        if self.project is None:
            return self.folder
        return self.project.root

    def config_file(self) -> Optional[Path]:
        """Return the configuration file of the open project, if any."""
        if self.project is None:
            return None
        return config_path(self.project.root)
