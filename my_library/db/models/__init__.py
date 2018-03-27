"""Define the public model interface.

Also serves to ensure that inherited classes are registered with
the Base class, which happens on import.
"""

# flake8: noqa
from .author import Author
from .book import Book
