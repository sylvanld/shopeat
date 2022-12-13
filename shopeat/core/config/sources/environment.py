import os

from shopeat.core.config.sources.base import ConfigSource

UNDEFINED = ...


class EnvironmentConfig(ConfigSource):
    def get(self, key: str):
        variable_name = key.upper().replace(".", "_")
        return os.getenv(variable_name, UNDEFINED)

    def missing_key_exception(self, key: str):
        variable_name = key.upper().replace(".", "_")
        return ValueError("Missing environment variable: %s" % variable_name)
