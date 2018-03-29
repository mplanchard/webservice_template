"""Provide automatic registration of schemas for SQLAlchemy models."""

# Note: we do not import unicode_literals here because we don't
# want to have to convert unicode back to bytestrings in Python2
# when constructing a type() object.
from __future__ import absolute_import

from marshmallow_sqlalchemy import ModelConverter, ModelSchema
from marshmallow_sqlalchemy.fields import Related

from .mixins import Collection, Resource


def property_stub_factory(key):
    """Make a property stub, with a key mapping to the attribute name."""
    return type('{}PropertyStub'.format(key), (object,), {u'key': key})


class CustomRelatedField(Related):
    """Retrieve both primary keys and "href" attrs for related objects."""

    @property
    def related_keys(self):
        """Retrieve keys to include from the related model.

        The overridden method here just returns primary keys. We
        return those, as well as property stubs (objects with a ``key``
        attribute corresponding to the attribute name on the model
        object) or actual properties for some other fields.

        Those fields include ``href``, which is the URL of the model's
        resource, and any names defined in the model's ``__nested__``
        class attribute, which can be names of columns or arbitrary
        class attributes or properties.

        :returns: a list of properties
        :rtype: list
        """
        keys = super(CustomRelatedField, self).related_keys
        if hasattr(self.related_model, u'href'):
            keys.append(property_stub_factory(u'href'))
        if hasattr(self.related_model, u'__nested__'):
            for attr in self.related_model.__nested__:
                if self.related_model.__mapper__.has_property(attr):
                    keys.append(
                        self.related_model.__mapper__.get_property(attr)
                    )
                else:
                    keys.append(property_stub_factory(attr))
        return keys


class CustomConverter(ModelConverter):
    """Ensure the "href" attribute is pulled for mtm relationships."""

    def _get_field_class_for_property(self, prop):
        """Ensure we use our custom Relation field for relationships."""
        if hasattr(prop, u'direction'):
            return CustomRelatedField
        else:
            return super(
                CustomConverter, self
            )._get_field_class_for_property(prop)


def dump(self, context=None, many=False, **schema_kwargs):
    """Convert the model instance to a serializable dict."""
    context = context or {}
    return self.spec(context=context, many=many, **schema_kwargs).dump(self)


def dumps(self, context=None, many=False, **schema_kwargs):
    """Serialize the model instance to JSON text."""
    context = context or {}
    return self.spec(context=context, many=many, **schema_kwargs).dumps(self)


def load(self, data, context=None, many=False, **schema_kwargs):
    """Load the model from a serializable dict."""
    context = context or {}
    return self.spec(context=context, many=many, **schema_kwargs).load(data)


def loads(self, data, context=None, many=False, **schema_kwargs):
    """Load the model from JSON text."""
    context = context or {}
    return self.spec(context=context, many=many, **schema_kwargs).loads(data)


def autospec_model(model, session, add_load_dump_methods=True,
                   **schema_overrides):
    """Automatically create a specification schema for an ORM model.

    :param sqlalchemy.ext.declarative.DeclarativeMeta model:
        a sqlalchemy ORM class
    :param sqlalchemy.orm.session.Session session: a sqlalchemy session
    :param bool add_load_dump_methods: whether to add ``load`` and
        ``dump`` (and ``loads`` and ``dumps``) methods to the ORM
        model utilizing the automatically generated schema.
    :param **schema_overrides: extra items to include in the generated
        schema's class dictionary
    """
    options_cls = type(
        'Meta',
        (object,),
        {
            u'model': model,
            u'session': session,
            u'model_converter': CustomConverter
        }
    )
    cls_dict = {u'Meta': options_cls}
    cls_dict.update(schema_overrides)

    setattr(
        model,
        u'spec',
        type(
            '{}Schema'.format(model.__name__),
            (ModelSchema, Collection, Resource),
            cls_dict,
        )
    )

    if add_load_dump_methods:
        setattr(model, u'dump', dump)
        setattr(model, u'dumps', dumps)
        setattr(model, u'load', load)
        setattr(model, u'loads', loads)
