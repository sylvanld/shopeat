from abc import ABC, abstractmethod
from typing import Any, Tuple

UNDEFINED = ...


class ConfigSource(ABC):
    @abstractmethod
    def get(self, key: str):
        ...

    @abstractmethod
    def missing_key_exception(self, key: str):
        ...
