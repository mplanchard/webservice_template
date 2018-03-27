"""Model(s) for books."""

from sqlalchemy import Column, Date, Integer, String, Table
from sqlalchemy.orm import relationship

from .association import books_authors
from .base import Base


class Book(Base):
    """Book model."""

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    publication_date = Column(Date)
    authors = relationship(
        'Author',
        secondary=books_authors,
        back_populates='books'
    )
