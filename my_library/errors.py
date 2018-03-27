"""Custom exceptions."""


class ConfigError(Exception):
    """An error occurred related to configuration."""


class InvalidConfVarType(ConfigError):
    """A ConfVar was supplied with an invalid type."""


class NoSuchConfVar(ConfigError):
    """No such ConfVar was present in this config."""


class InvalidConfVarValue(ConfigError):
    """The provided value was invalid."""
