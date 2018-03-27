"""Test mixins."""

from os import environ

import pytest

from .util import run


class SessionFreshDB(object):
    """Ensure a fresh database for each test session.

    Also exercises the full migration path (both up and down).
    """

    @pytest.fixture(scope='session', autouse=True)
    def run_migrations(self):
        """Run database migrations. On cleanup, downgrade to base."""
        environ['FLASK_APP'] = 'my_library.main'
        run('flask db upgrade')
        yield
        run('flask db downgrade base')
