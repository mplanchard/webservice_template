"""Books Resources."""

from logging import getLogger

from werkzeug.exceptions import NotFound

from .resource import ModelResource


log = getLogger(__name__)


class BookResource(ModelResource):

    path = '/books/<int:id>'
    endpoint_name = 'book'
    model_name = 'Book'

    def get(self, id):
        item = self.query.get(id)
        if item is None:
            raise NotFound('No such {}: {}'.format(self.model_name, id))
        dumped, errors = item.dump()
        if errors:
            log.warning('Errors dumping {}: {}'.format(item, errors))
        return dumped


class BooksResource(ModelResource):

    path = '/books'
    endpoint_name = 'books'
    model_name = 'Book'

    def get(self):
        items, errors = self.model.schema(
            context=self.collection_ctx(self.query_many)
        ).dump(self.query_many, many=True)
        if errors:
            log.warning(
                'Errors dumping {} {}: {}'.format(
                    len(items), self.endpoint_name, errors
                )
            )
        return items
