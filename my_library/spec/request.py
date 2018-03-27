"""Generic schemas for parsing request parameters and data."""

from marshmallow import Schema, fields


class CollectionQueryArgs(Schema):
    """Arguments common to collection queries."""

    limit = fields.Integer()
    offset = fields.Integer()
