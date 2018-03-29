"""Application setup and definition.

To run Flask directly, ``export FLASK_APP=my_library.main:app``
"""

from __future__ import absolute_import, unicode_literals

from inspect import isclass

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config, ConfVar
from .db import models
from .db.models.base import Base
from .resources import api
from .spec.auto import autospec_model


class FlaskDBWrapper(object):
    """Expose only portions of Flask-SQLAlchemy to encourage portability."""

    def __init__(self, db, models):
        self.engine = db.engine
        self.metadata = db.metadata
        self.session = db.session
        self.models = models
        self.flask_sqla = db


def get_db_conf(load=True):
    """Return a DB configuration instance.

    :param bool load: if True, load the config before returning
    :returns: an optionally loaded config with DB values.
    :rtype: .config.Config
    """
    conf = Config(
        ConfVar('user', None, type_=str),
        ConfVar('password', None, type_=str),
        ConfVar('name', None, type_=str),
        ConfVar('host', 'local/local.sqlite', type_=str),
        ConfVar('port', None, type_=str),
        ConfVar('engine', 'sqlite'),
        prefix='DB'
    )
    if load:
        conf.load()
    return conf


def get_flask_conf(load=True):
    """Return a Flask configuration instance.

    :param bool load: if True, load the config before returning
    :returns: an optionally loaded config with flask app values.
    :rtype: .config.Config
    """
    conf = Config(
        ConfVar('DEBUG', False),
        ConfVar('TESTING', False),
        prefix='FLASK'
    )
    if load:
        conf.load()
    return conf


def get_logging_conf(load=True):
    """Return a logging configuration instance.

    :param bool load: if True, load the config before returning
    :returns: an optionally loaded config with logging values
    :rtype: .config.Config
    """
    conf = Config(
        ConfVar('LEVEL', 'INFO'),
        prefix='LOG'
    )
    if load:
        conf.load()
    return conf


def setup_database(app, db_conf):
    """Create the DB engine and scoped session, autospec models."""
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri(db_conf)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app, metadata=Base.metadata)

    for name, model in vars(models).items():
        if name.startswith('_'):
            continue
        if isclass(model) and issubclass(model, Base):
            autospec_model(model, db.session)

    Migrate(app=app, db=db)

    return FlaskDBWrapper(db, models)


def create_app():
    """Return the hydrated application instance."""
    app = Flask(__name__)

    db_conf = get_db_conf()
    flask_conf = get_flask_conf()
    logging_conf = get_logging_conf()

    for key, value in flask_conf:
        app.config[key] = value

    app.config['db'] = db_conf
    app.config['logging'] = logging_conf

    app.db = setup_database(app, db_conf)

    api.register(app)

    return app


def db_uri(db_conf):
    """Return the database URI, given the database config."""
    if db_conf.get('engine') == 'memory':
        return 'sqlite:///:memory:'
    elif db_conf.get('engine') == 'sqlite':
        return '{engine}:///{host}'.format(**dict(db_conf))
    return '{engine}://{user}:{password}@{host}:{port}/{name}'.format(
        **dict(db_conf)
    )
