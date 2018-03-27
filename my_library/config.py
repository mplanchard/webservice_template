"""Application configuration."""

from enum import Enum
from os import environ

from . import errors


class ConfState(Enum):
    notset = 1


class ConfVar(object):
    """A configuration variable."""

    TRUE_STRINGS = ('t', 'true', 'yes', 'on')
    FALSE_STRINGS = ('f', 'false', 'no', 'off')
    NONZERO_INTS_ARE_TRUE = True
    UNKNOWN_STRINGS_ARE_FALSE = False

    def __init__(self, name, default, type_=None):
        """Instantiate a ConfVar.

        :param str name: the name of the variable
        :param Any default: the default value
        :param type type_: the type of the variable. Not required
            unless the ``default`` is ``None``. Used when casting
            values from environment variables.
        """
        if default is not None:
            if type_ is not None and not isinstance(default, type_):
                raise errors.InvalidConfVarType(
                    '{} is not an instance of {}'.format(default, type_)
                )
        self.name = name
        self.default = default
        self.type_ = type_ or type(default)
        self._value = ConfState.notset

    @property
    def value(self):
        """Return the value of the variable.

        The value is the default if the variable has not been set.
        """
        if self._value is ConfState.notset:
            return self.default
        return self._value

    @value.setter
    def value(self, value):
        """Set the value of this ConfVar.

        :param Any value: the value to which to set the ConfVar.
        """
        if self.type_ is not None and not isinstance(value, self.type_):
            raise errors.InvalidConfVarType(
                '{} is not an instance of {}'.format(value, self.type_)
            )
        self._value = value

    def cast(self, value):
        """Cast the value to the ``ConfVar`` ``type_``.

        This isn't meant for complex casting. Some special casing is
        done for booleans when the value is a string, but otherwise,
        we just do a simple cast.

        :param Any value: the value to cast
        """
        if self.type_ is bool and isinstance(value, str):
            if self.NONZERO_INTS_ARE_TRUE:
                try:
                    val = int(value)
                except ValueError:
                    pass
                else:
                    return bool(val)
            val = value.lower()
            if val in self.TRUE_STRINGS:
                return True
            elif val in self.FALSE_STRINGS:
                return False
            else:
                if self.UNKNOWN_STRINGS_ARE_FALSE:
                    return False
                raise errors.InvalidConfVarValue(
                    '{} is not a valid boolean value.'.format(value)
                )
        return self.type_(value)

    def to_environment_variable(self, prefix=None):
        """Return the environment variable name of this ConfVar.

        The environment variable name is the capitalized variable name,
        optionally preceded by the ``prefix`` and an underscore.

        :param str prefix: the prefix to expect in front of the variable
            name
        """
        prefix_str = '{}_'.format(prefix) if prefix else ''
        return (prefix_str + self.name).upper()


class Config(object):
    """Pull config values from the environment, or resort to defaults."""

    def __init__(self, *conf_vars, **kwargs):
        """Instantiate a config.

        Due to Python 2.7 syntax compatibility, we can't include
        a named positional argument after the unpacked ``conf_vars``.
        However, ``prefix`` may be provided, in which case environment
        variables will be expected with the form
        ``{PREFIX}_{VAR_NAME}``.

        :param ConfVar conf_vars: config variables for this config
        :param str prefix: the environment variable prefix to use for
            this config (default ``None``)
        """
        self.prefix = kwargs.get('prefix')
        self._map = {cv.name: cv for cv in conf_vars}

    def __iter__(self):
        """Iterate through ConfVar name/value pairs.

        Allows conversion of ``Config`` to a dict with the standard
        ``dict()`` constructor.
        """
        for name, conf_var in self._map.items():
            yield name, conf_var.value

    def load(self):
        """Load config values from the environment, if present."""
        for conf_var in self._map.values():
            env_var = conf_var.to_environment_variable(self.prefix)
            if env_var in environ:
                conf_var.value = conf_var.cast(environ[env_var])

    def get(self, name):
        """Get a config variable."""
        try:
            return self._map[name].value
        except KeyError:
            raise errors.NoSuchConfVar(name)

    def set(self, name, value, type_=None):
        """Set a config variable.

        The config variable does *not* have to exist prior to being set.
        If it does not exist, a ``ConfVar`` is created with the
        specified ``value``. If the optional ``type_`` is provided,
        this is also used in the instantiation of the ``ConfVar``.

        :param str name: the variable name
        :param str value: the value to set for the variable
        :param type type_: the type of the variable. This is only
            useful if the variable is being set to ``None``.
        """
        if name in self._map:
            self._map[name].value = value
        else:
            self._map[name] = ConfVar(name, value, type_=type_)
            self._map[name].value = value
