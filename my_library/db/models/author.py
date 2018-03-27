"""Author models."""

from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from .association import books_authors
from .base import Base


class Author(Base):
    """Author model."""

    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    birth = Column(Date, nullable=False)
    death = Column(Date)
    name = Column(String(128), nullable=False)

    books = relationship(
        'Book',
        secondary=books_authors,
        back_populates='authors',
    )
