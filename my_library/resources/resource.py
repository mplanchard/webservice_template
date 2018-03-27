"""Base classes for data representations."""

from functools import partial

from flask import (
    current_app as app,
    request,
    url_for as flask_url_for
)
from flask_restplus import Resource
from werkzeug.exceptions import BadRequest

from my_library.spec.request import CollectionQueryArgs


class BaseResource(Resource):

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
        return flask_url_for(
            '.{}'.format(cls.endpoint_name),
            **kwargs
        )


class ModelResource(BaseResource):
    """Parse or return JSON representations of a resource."""

    model_name = None
    default_limit = 20
    default_offset = 0

    def __init__(self, **kwargs):
        self._parsed_collection_query_args = None
        self.model = getattr(app.db.models, self.model_name)

    @property
    def collection_query_args(self):
        if self._parsed_collection_query_args is None:
            args, errors = CollectionQueryArgs().load(request.args)
            if errors:
                raise BadRequest(errors)
            self._parsed_collection_query_args = args
        return self._parsed_collection_query_args

    @property
    def limit(self):
        return self.collection_query_args.get('limit', self.default_limit)

    @property
    def offset(self):
        return self.collection_query_args.get('offset', self.default_offset)

    @property
    def query(self):
        return app.db.session.query(self.model)

    @property
    def query_many(self):
        return self.apply_limit_and_offset(self.query)

    def apply_limit_and_offset(self, query):
        return query.offset(self.offset).limit(self.limit)

    def collection_ctx(self, query):
        return {
            'limit': self.limit,
            'offset': self.offset,
            'total': self.total(query),
        }

    def total(self, query):
        return query.limit(None).count()
