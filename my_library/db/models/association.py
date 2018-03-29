"""Association tables."""

from __future__ import absolute_import, unicode_literals

from sqlalchemy import Column, Integer, ForeignKey, Table

from .base import Base


books_authors = Table(
    'books_authors',
    Base.metadata,
    Column('author_id', Integer, ForeignKey('authors.id')),
    Column('book_id', Integer, ForeignKey('books.id')),
)
