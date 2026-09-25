#! /usr/local/bin/python3
"""Version information about notesmgr and what it is built on."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from datetime import date
from typing import TextIO
from packaging.version import Version
from versionreporter import SupportExpires, VersionReporter
from notesmgr.errors import NotesmgrError

MAIN_PACKAGE = 'notesmgr'
"""Package to install to get a newer notesmgr."""

REPORTED_PACKAGES = [MAIN_PACKAGE, 'edit-cfg-json-tk', 'edit-cfg-json',
                     'config-as-json', 'versionreporter', 'argcomplete',
                     'packaging', 'send2trash', 'markdown']
"""Packages whose versions are worth reporting to a user."""

RECOMMENDED_PYTHON = '3.14'
"""Python version that notesmgr is developed and recommended on."""

NO_REPORT = 'The version report cannot be made, as PyPI.org, which says\n' \
    'what newer releases there are, cannot be reached.\n{reason}'
"""What is said when the releases on PyPI.org cannot be asked about."""

SUPPORT_EXPIRES: SupportExpires = {date(2027, 3, 1): '3.12',
                                   date(2028, 3, 1): '3.13'}
"""When notesmgr stops supporting a Python version.

A Python version is supported for about two and a half years after the
next Python version was released, and support always ends on the first
of March. Newer language features are then available sooner than
following the end of life of Python itself would allow.
"""


class NotesmgrVersions(VersionReporter):
    """Report what notesmgr and the packages below it are."""

    def package_names(self) -> list[str]:
        """Return the packages whose versions are reported."""
        return list(REPORTED_PACKAGES)

    def get_app_support_expires(self) -> SupportExpires:
        """Return when notesmgr stops supporting an older Python."""
        return dict(SUPPORT_EXPIRES)

    @classmethod
    def get_main_package_name(cls) -> str:
        """Return the package that an upgrade of notesmgr installs."""
        return MAIN_PACKAGE

    @classmethod
    def recommended_python(cls) -> Version:
        """Return the Python version that notesmgr recommends."""
        return Version(RECOMMENDED_PYTHON)


def version_report(out_file: TextIO) -> None:
    """Write the version report of notesmgr to the given stream.

    The command line gives it the standard output stream, and the
    graphical user interface gives it a string that it then shows in a
    window, so that both ways of asking report exactly the same thing.

    Args:
        out_file: Stream that the report is written to.

    Raises:
        NotesmgrError: PyPI.org cannot be reached, which is what a
            computer with no network connection is told.
    """
    try:
        NotesmgrVersions().print(out_file=out_file)
    except OSError as error:
        raise NotesmgrError(NO_REPORT.format(reason=error)) from error
