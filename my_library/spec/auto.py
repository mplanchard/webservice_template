"""Provide automatic registration of schemas for SQLAlchemy models."""

from marshmallow_sqlalchemy import ModelSchema

from .mixins import Collection


def load(self, data, context=None, **schema_kwargs):
    context = context or {}
    return self.schema(context=context, **schema_kwargs).load(data)


def dump(self, context=None, **schema_kwargs):
    context = context or {}
    return self.schema(context=context, **schema_kwargs).dump(self)


def dumps(self, context=None, **schema_kwargs):
    context = context or {}
    return self.schema(context=context, **schema_kwargs).dumps(self)


def loads(self, data, context=None, **schema_kwargs):
    context = context or {}
    return self.schema(context=context, **schema_kwargs).loads(data)


def autospec_model(model, session, add_load_dump_methods=True,
                   **schema_overrides):
    """Automatically create a specification schema for an ORM model."""

    options_cls = type(
        'Meta',
        (object,),
        {'model': model, 'session': session}
    )
    cls_dict = {'Meta': options_cls}
    cls_dict.update(schema_overrides)

    setattr(
        model,
        'spec',
        type(
            '{}Schema'.format(model.__name__),
            (ModelSchema, Collection),
            cls_dict,
        )
    )

    if add_load_dump_methods:
        setattr(model, 'dump', dump)
        setattr(model, 'dumps', dumps)
        setattr(model, 'load', load)
        setattr(model, 'loads', loads)
