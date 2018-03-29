"""Base classes for data representations."""

from __future__ import absolute_import, unicode_literals

from functools import partial
from logging import getLogger

from flask import (
    current_app as app,
    request,
    url_for as flask_url_for
)
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from my_library.spec.request import CollectionQueryArgs


log = getLogger(__name__)


class BaseResource(Resource):
    """A base resource class, providing convenience methods.

    Subclasses must define class attributes ``path`` and
    ``endpoint_name``.
    """

    path = None
    endpoint_name = None

    @classmethod
    def add_to_api(cls, api):
        """Add the resource to the provided flask-rest(ful/plus) API."""
        if isinstance(cls.path, str):
            adder = partial(api.add_resource, cls, cls.path)
        else:
            adder = partial(api.add_resource, cls, *cls.path)
        adder(endpoint=cls.endpoint_name)

    @classmethod
    def url_for(cls, **kwargs):
        """Return the URL for the specified resource.

        :param kwargs: keyword arguments to pass to flask's ``url_for``
            method, corresponding to variable portions of the URL,
            e.g. ``id=7`` for a URL with an ``<int:id>`` section.
        """
        return flask_url_for(
            '.{}'.format(cls.endpoint_name),
            **kwargs
        )


class ModelResource(BaseResource):
    """Parse or return JSON representations of a resource.

    :cvar model_name: the name of the ORM model associated with this
        resource
    :cvar default_limit: the default limit for collection results
    :cvar default_offset: the default offset for collection results

    :ivar model: the ORM model corresponding to the class attribute
        ``model_name``
    """

    model_name = None
    default_limit = 20
    default_offset = 0

    def __init__(self, *args, **kwargs):
        """Instantiate the model resource."""
        super(ModelResource, self).__init__(*args, **kwargs)
        self._collection_query_args = None
        self.model = getattr(app.db.models, self.model_name)

    @property
    def collection_query_args(self):
        """Common arguments for any collection endpoint."""
        if self._collection_query_args is None:
            args, errors = CollectionQueryArgs().load(request.args)
            if errors:
                raise BadRequest(errors)
            self._collection_query_args = args
        return self._collection_query_args

    @property
    def limit(self):
        """The limit for a collection query."""
        return self.collection_query_args.get('limit', self.default_limit)

    @property
    def offset(self):
        """The offset for a collection query."""
        return self.collection_query_args.get('offset', self.default_offset)

    @property
    def query(self):
        """A query instance for the instance's ``model``."""
        return app.db.session.query(self.model)

    @property
    def query_many(self):
        """A query instance with ``limit`` and ``offset`` applied."""
        return self.apply_limit_and_offset(self.query)

    def apply_limit_and_offset(self, query):
        """Apply the instance's ``limit`` and ``offset`` to the query."""
        return query.offset(self.offset).limit(self.limit)

    def collection_ctx(self, query):
        """Return the expected schema context for the Collection mixin."""
        return {
            'limit': self.limit,
            'offset': self.offset,
            'total': self.total(query),
        }

    def representation(self, item_or_query, many=False):
        """Convert an item or a query into a representation.

        :param item_or_query: an ORM object, an iterable of ORM objects,
            or a SQLAlchemy query (which is a particular iterable of
            ORM objects)
        :param many: explicitly state that a collection is being
            handled. ``many=True`` is implicit when a query is passed
            to this method.
        """
        if isinstance(item_or_query, self.query.__class__) or many:
            many = True
            context = self.collection_ctx(item_or_query)
        else:
            context = None

        schema = self.model.spec(context=context, many=many)
        dumped, errors = schema.dump(item_or_query)
        if errors:
            log.warning(
                '{}: errors dumping {}: {}'.format(
                    self.endpoint_name, item_or_query, errors
                )
            )
        return dumped

    def total(self, query):
        """Return the total number of results matching the query."""
        return query.limit(None).count()
