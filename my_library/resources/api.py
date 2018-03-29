"""Register the API with the Flask App"""

from __future__ import absolute_import, unicode_literals

from flask_restplus import Api

from .authors import AuthorResource
from .books import BookResource, BooksResource


RESOURCES = [
    AuthorResource,
    BookResource,
    BooksResource,
]


def register(app):
    """Register the application API with the provided Flask app."""
    api = Api(app)
    for resource in RESOURCES:
        resource.add_to_api(api)
