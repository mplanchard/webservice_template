"""Entrypoint to get the Flask app.

To run Flask directly, ``export FLASK_APP=my_library.main:app``
"""

from __future__ import absolute_import

from .app import create_app


app = create_app()
