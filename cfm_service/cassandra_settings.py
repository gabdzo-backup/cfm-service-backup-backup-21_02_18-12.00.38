"""Docstring."""

from cfm_service.default_settings import Config


class CassandraConfig(Config):
    """Docstring."""

    DEBUG = True

    STORAGE = "cassandra"

    CASSANDRA = {
        "username": "<redacted>",
        "password": "<redacted>",
        "cloud": "secure-connect.cfm.zip",
        "log_level": "INFO",
    }
