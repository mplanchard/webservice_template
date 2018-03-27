"""Test utilities."""

from os import environ
from shlex import split
from subprocess import Popen
from sys import exit


def run(cmd, **kwargs):
    """Run a command, with the given kwargs passed to Popen."""
    if isinstance(cmd, str):
        cmd = split(cmd)
    proc = Popen(cmd, env=environ, **kwargs)
    try:
        proc.communicate()
    except KeyboardInterrupt:
        print('Aborted!')
        exit(1)
    if proc.returncode:
        print('Exiting due to called process error')
        exit(1)
