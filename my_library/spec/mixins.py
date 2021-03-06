"""Schema mixins for representation specification."""

from __future__ import absolute_import, unicode_literals

from marshmallow import fields, post_dump, pre_load


class Collection(object):
    """Implement automatic collection enveloping."""

    context = {}
    envelope_key = 'items'

    @post_dump(pass_many=True)
    def envelope_items(self, data, many):
        """Wrap the collection of items in an envelope.

        The schema context is used to pass data about the limit, offset,
        and total, if available, e.g.
        ``Schema(context={'limit': 5}, many=True).dump(data)`` or::

            sch = Schema(many=True)
            sch.context['limit'] = 5
            return sch.dump(data)

        """
        if many:
            data_len = len(data)
            return {
                'count': data_len,
                'total': self.context.get('total', data_len),
                'limit': self.context.get('limit', 0),
                'offset': self.context.get('offset', 0),
                self.envelope_key: data
            }

    @pre_load(pass_many=True)
    def unwrap_envelope(self, data, many):
        """Retrieve data from the envelope key."""
        if many:
            return data[self.envelope_key]


class Resource(object):
    """Automatically populate resource location on dump() if available."""

    href = fields.String()
