"""Author resources."""

from __future__ import absolute_import, unicode_literals

from .resource import ModelResource


class AuthorResource(ModelResource):
    """An author represented in the library's collection."""

    path = '/authors/<int:id>'
    endpoint_name = 'author'
    model_name = 'Author'


class AuthorsResource(ModelResource):
    """The authors represented in the library's collection."""
