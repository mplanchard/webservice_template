# -*- coding: utf-8 -*-
"""Define the base class for models."""

from __future__ import absolute_import, unicode_literals


from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


_Base = declarative_base()


class Base(_Base):
    """Base class for models.

    Includes an "id" integer primary key.

    All models imported into ``db.models.__init__`` will have
    Marshmallow schema automatically generated and attached to the
    model class on the ``spec`` attribute.

    Child classes of this base class may implement the following special
    class or instance properties:

    * __nested__: field names that should be included in nested
      representations of this model
    * __resource__: used to determine the URL of the model during
      serialization
    * href: this property is used to populate the "href" attribute
      of the serialized form of the model to send to the client.
      While a naïve implementation is provided here, subclasses
      will often have to implement the property more intelligently.
    """
    __abstract__ = True
    __nested__ = ()
    __resource__ = None

    id = Column(Integer, primary_key=True)

    @property
    def href(self):
        """Attempt, naïvely, to determine the model's URL.

        Should absolutely be overridden in child classes if a smarter
        implementation is required.
        """
        if self.__resource__ is not None:
            return self.__resource__.url_for(id=self.id)
