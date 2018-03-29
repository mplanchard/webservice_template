"""Global test fixtures.

To maintain maximum compatibility with other test suites, items
here should be kept to a minimum.
"""

from os import environ, unlink, path

import pytest
from flask_migrate import downgrade, upgrade

from my_library.app import create_app
from .util import local_db


@pytest.fixture(scope='session', autouse=True)
def fresh_db_fixture():
    """Ensure a fresh DB with migrations for tests."""
    local_db()
    app = create_app()
    with app.app_context():
        upgrade()
    yield
    with app.app_context():
        downgrade(revision='base')
    if path.exists(environ['DB_HOST']):
        unlink(environ['DB_HOST'])
