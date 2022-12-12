import json
from typing import Any, Callable, Dict, Type

from shopeat.core.config.sources.base import ConfigSource

UNDEFINED = ...


def load_boolean(v: str):
    try:
        return bool(json.loads(v))
    except Exception:
        raise ValueError


class Config:
    __instance: ConfigSource = None
    __cache: Dict[str, str] = {}
    __loader: Dict[Type[Any], Callable[[str], Any]] = {bool: load_boolean}

    @classmethod
    def __get_instance(cls):
        if cls.__instance is None:
            from shopeat.core.config.sources.environment import EnvironmentConfig

            cls.__instance = EnvironmentConfig()
        return cls.__instance

    @classmethod
    def get(cls, key: str, *, type=UNDEFINED, default=UNDEFINED):
        value = cls.__cache.get(key, UNDEFINED)

        if value is UNDEFINED:  # if value is not in cache
            value = cls.__get_instance().get(key)

        if value is UNDEFINED:  # if value is not defined
            if default is UNDEFINED:
                raise cls.__get_instance().missing_key_exception(key)
            value = default
        else:  # if value is defined
            cls.__cache[key] = value

        if type is not UNDEFINED:
            loader = cls.__loader.get(type)
            if loader is None:
                loader = type
            return loader(value)

        return value
