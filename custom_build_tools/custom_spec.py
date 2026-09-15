#! /usr/local/bin/python3
"""Repository-specific build specification for common_build_tools."""

# Copyright (c) 2026 Tom Björkholm
# MIT License

from typing import Optional
from build_spec import BuildSpec


def custom_spec() -> Optional[BuildSpec]:
    """Return custom build spec for this repository."""
    return None
