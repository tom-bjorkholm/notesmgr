#! /usr/local/bin/python3
"""Tests for the version information that notesmgr reports."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

import io
from datetime import date
from typing import Optional, TextIO
import pytest
from packaging.version import Version
from versionreporter import VersionInfo, VersionReporter
from notesmgr.errors import NotesmgrError
from notesmgr.version_info import MAIN_PACKAGE, RECOMMENDED_PYTHON, \
    NotesmgrVersions, version_report


@pytest.fixture(name='written')
def fixture_written(monkeypatch: pytest.MonkeyPatch) -> list[Optional[TextIO]]:
    """Record what stream a report was asked to be written to.

    The real report asks PyPI about newer releases, which a test may
    neither wait for nor depend on.
    """
    asked: list[Optional[TextIO]] = []

    def record(_self: VersionReporter, versions: Optional[VersionInfo] = None,
               out_file: Optional[TextIO] = None) -> None:
        """Stand in for VersionReporter.print."""
        assert versions is None
        asked.append(out_file)
    monkeypatch.setattr(VersionReporter, 'print', record)
    return asked


def test_main_package_first() -> None:
    """The application itself is the first package that is reported."""
    assert NotesmgrVersions().package_names()[0] == MAIN_PACKAGE


def test_upgrade_installs() -> None:
    """Upgrading the program means installing notesmgr."""
    assert NotesmgrVersions.get_main_package_name() == MAIN_PACKAGE


@pytest.mark.parametrize('package', ['notesmgr', 'edit-cfg-json-tk',
                                     'edit-cfg-json', 'config-as-json',
                                     'versionreporter', 'argcomplete',
                                     'packaging', 'send2trash', 'markdown'])
def test_package_reported(package: str) -> None:
    """Every package that notesmgr is built on is reported."""
    assert package in NotesmgrVersions().package_names()


def test_package_names_copied() -> None:
    """Changing the reported list does not change the next report."""
    reporter = NotesmgrVersions()
    reporter.package_names().append('unwanted')
    assert 'unwanted' not in reporter.package_names()


@pytest.mark.parametrize('ends,version', [(date(2027, 3, 1), '3.12'),
                                          (date(2028, 3, 1), '3.13')])
def test_support_expires(ends: date, version: str) -> None:
    """Support for a Python version ends on the first of March."""
    assert NotesmgrVersions().get_app_support_expires()[ends] == version


def test_expiry_is_copied() -> None:
    """Changing the returned dates does not change the next report."""
    reporter = NotesmgrVersions()
    reporter.get_app_support_expires()[date(2030, 1, 1)] = '3.14'
    assert date(2030, 1, 1) not in reporter.get_app_support_expires()


def test_recommended_python() -> None:
    """The recommended Python version is the one notesmgr is built on."""
    assert NotesmgrVersions.recommended_python() == Version(RECOMMENDED_PYTHON)


def test_report_to_stream(written: list[Optional[TextIO]]) -> None:
    """The report is written to the stream that was asked for."""
    stream = io.StringIO()
    version_report(stream)
    assert written == [stream]


def test_unreachable_told(monkeypatch: pytest.MonkeyPatch) -> None:
    """With PyPI.org out of reach the user is told so, in words."""
    def unreachable(_self: VersionReporter,
                    versions: Optional[VersionInfo] = None,
                    out_file: Optional[TextIO] = None) -> None:
        """Stand in for a report on a computer with no network."""
        _ = versions, out_file
        raise ConnectionError('no network')
    monkeypatch.setattr(VersionReporter, 'print', unreachable)
    with pytest.raises(NotesmgrError, match='PyPI.org') as raised:
        version_report(io.StringIO())
    assert 'no network' in str(raised.value)
