#!/usr/bin/env python
"""Freeze requirements."""

from __future__ import absolute_import

from pathlib import Path
from subprocess import Popen


def get_parent_directory():
    """Return the parent of this file's directory.

    :returns: a pathlib object for the parent directory
    :rtype: Path
    """
    return Path(__file__).parent.parent


def requirements_path():
    """Return a Path object for the requirements file.

    :returns: a pathlib object for the requirements file
    :rtype: Path
    """
    return get_parent_directory()/'requirements.txt'


def yield_freeze_command():
    """Yield the command to be run in main.

    :returns: an iterable over the command items
    :rtype: Iterable
    """
    for part in (
            'pip',
            'freeze',
            '|', 'sort',
            '>>', str(requirements_path()),):
        yield part


def yield_header():
    """Yield the header for the reqfile.

    :returns: iterable lines of the header
    :rtype: Iterable
    """
    to_yield = (
        '# This file is automatically generated. Other than for debugging',
        '# purposes, please update ``requirements_unfrozen.txt`` instead.',
        '# To automatically run tests with updated packages and update ',
        '# requirements if successful, run ``tox -e update_requirements``.',
    )
    for line in to_yield:
        yield line
        yield '\n'


def main():
    """Freeze the requirements."""
    with open(str(requirements_path()), 'w') as reqfile:
        reqfile.writelines(yield_header())
    Popen(' '.join(yield_freeze_command()), shell=True).communicate()


if __name__ == '__main__':
    main()
