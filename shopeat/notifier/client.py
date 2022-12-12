from abc import ABC, abstractmethod

import aio_pika

from shopeat.settings import Config, SHOPEAT_AMQP_BROKER_URL
from shopeat.notifier.models import Notification


class NotificationClient(ABC):
    @abstractmethod
    async def publish(self, notification: Notification):
        ...


class AMQPNotificationClient(NotificationClient):
    __connection: aio_pika.RobustConnection = None
    __channel: aio_pika.RobustChannel = None
    __queue: aio_pika.RobustQueue = None

    def __init__(self, amqp_broker_url: str):
        self.amqp_broker_url = amqp_broker_url
        self.queue_name = "notifications"

    async def get_connection(self):
        if self.__connection is None:
            self.__connection = await aio_pika.connect_robust(self.amqp_broker_url)
        return self.__connection

    async def get_channel(self):
        if self.__channel is None:
            connection = await self.get_connection()
            self.__channel = await connection.channel()
            await self.get_queue()
        return self.__channel

    async def get_queue(self):
        if self.__queue is None:
            channel = await self.get_channel()
            self.__queue = await channel.declare_queue(
                self.queue_name, auto_delete=True
            )
        return self.__queue

    async def publish(self, notification: Notification):
        channel = await self.get_channel()
        await channel.default_exchange.publish(
            aio_pika.Message(body=notification.json().encode("utf-8")),
            routing_key=self.queue_name,
        )

    @classmethod
    def from_config(cls):
        return cls(amqp_broker_url=Config.get(SHOPEAT_AMQP_BROKER_URL))


class NotificationClientFactory:
    __instance: NotificationClient = None

    @classmethod
    def get_instance(cls) -> NotificationClient:
        if cls.__instance is None:

            cls.__instance = AMQPNotificationClient.from_config()
        return cls.__instance
