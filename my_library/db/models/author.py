"""Author models."""

from __future__ import absolute_import, unicode_literals

from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship

from my_library.resources.authors import AuthorResource
from .association import books_authors
from .base import Base


class Author(Base):
    """Author model."""

    __tablename__ = 'authors'
    __resource__ = AuthorResource
    __nested__ = ('name',)

    birth = Column(Date, nullable=False)
    death = Column(Date)
    name = Column(String(128), nullable=False)

    books = relationship(
        'Book',
        secondary=books_authors,
        back_populates='authors',
    )
