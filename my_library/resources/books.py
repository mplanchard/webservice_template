"""Books Resources."""

from __future__ import absolute_import, unicode_literals

from logging import getLogger

from werkzeug.exceptions import NotFound

from .resource import ModelResource


log = getLogger(__name__)


class BookResource(ModelResource):
    """A book in the library."""

    path = '/books/<int:id>'
    endpoint_name = 'book'
    model_name = 'Book'

    def get(self, id):
        """Retrieve a representation of the book with the given ID."""
        item = self.query.get(id)
        if item is None:
            raise NotFound('No such {}: {}'.format(self.model_name, id))
        return self.representation(item)


class BooksResource(ModelResource):
    """The books in the library."""

    path = '/books'
    endpoint_name = 'books'
    model_name = 'Book'

    def get(self):
        """Retrieve a representation of all books in the library."""
        return self.representation(self.query_many)
