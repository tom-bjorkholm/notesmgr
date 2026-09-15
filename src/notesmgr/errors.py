#! /usr/local/bin/python3
"""What notesmgr raises when it cannot do what it was asked to do."""

# Copyright (c) 2026 Tom Björkholm
# MIT License


class NotesmgrError(Exception):
    """Something cannot be done, said in words meant for the user.

    The message is shown in a window as it stands, so it names the
    file or the folder it is about and says what is wrong with it,
    rather than saying what the code was doing at the time.
    """
