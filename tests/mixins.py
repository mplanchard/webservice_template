"""Test mixins."""

import pytest

from my_library.app import create_app


class AppTest(object):
    """Create an application object and push the app context.

    Allows use of ``flask.current_app`` to get the app instance.
    """

    @pytest.fixture(scope='class', autouse=True)
    def setup_app(self):
        """Set up the app and push its context."""
        app = create_app()
        with app.app_context():
            yield
