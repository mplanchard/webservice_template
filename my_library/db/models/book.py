"""Model(s) for books."""

from __future__ import absolute_import, unicode_literals

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from .association import books_authors
from .base import Base

from my_library.resources.books import BookResource


class Book(Base):
    """Book model."""

    __tablename__ = 'books'
    __resource__ = BookResource
    __nested__ = ('title',)

    title = Column(String(512), nullable=False)
    published = Column(Integer)
    authors = relationship(
        'Author',
        secondary=books_authors,
        back_populates='books'
    )
