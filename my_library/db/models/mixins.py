"""Mixins for inclusion in other classes."""

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime


class CreateUpdate(object):
    """Automatically track creation and updates."""

    created = Column(DateTime, default=datetime.utcnow)
    updated = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


class SoftDelete(object):
    """Provide a ``deleted`` boolean field."""

    deleted = Column(
        Boolean, default=False, nullable=False, server_default=False
    )
