from abc import ABC, abstractclassmethod, abstractmethod
from typing import Generator

from shopeat.notifier.models import Notification


class NotificationsBroker(ABC):
    @abstractmethod
    async def iterate(self) -> Generator[Notification, None, None]:
        ...

    @abstractclassmethod
    def from_config(cls) -> "NotificationsBroker":
        ...
