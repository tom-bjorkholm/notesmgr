#! /usr/local/bin/python3
"""Repository-specific build specification for common_build_tools."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from pathlib import Path
from typing import Optional
from build_spec import BuildSpec

TEST_FOLDER = Path('test')
"""Folder that the test packages are found under.

It is on the path of mypy so that the test modules can share the
helpers that build the projects on disk that they are run against.
"""


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return BuildSpec(excluded_test_markers=['focus_sensitive'],
                     python_layout_max_name_length=25,
                     mypy_paths=[TEST_FOLDER])
