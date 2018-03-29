"""Test utilities."""

from os import environ, path, mkdir
from shlex import split
from uuid import uuid4
from subprocess import Popen
from sys import exit


REPO_DIR = path.abspath(
    path.join(path.realpath(path.dirname(__file__)), '..')
)


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


def local_db():
    """Set environment variables to ensure a test-local DB."""
    DB_DIR = path.join(REPO_DIR, 'local')
    if not path.isdir(DB_DIR):
        mkdir(DB_DIR)
    DB_PATH = path.join(DB_DIR, 'test-{}.sqlite'.format(uuid4()))
    with open(DB_PATH, 'w'):
        pass
    environ['DB_HOST'] = DB_PATH
    environ['DB_ENGINE'] = 'sqlite'
