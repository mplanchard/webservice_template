"""Register the API with the Flask App"""

from flask_restplus import Api

from .books import BookResource, BooksResource


RESOURCES = [
    BookResource,
    BooksResource,
]


def register(app):
    api = Api(app)
    for resource in RESOURCES:
        resource.add_to_api(api)

