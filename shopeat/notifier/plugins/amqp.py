import aio_pika

from shopeat.core.config import Config
from shopeat.notifier.models import Notification
from shopeat.notifier.plugins.interface import NotificationsBroker
from shopeat.settings import SHOPEAT_AMQP_BROKER_URL


class AMQPNotificationsBroker(NotificationsBroker):
    def __init__(self, broker_url: str):
        self.broker_url = broker_url
        self.queue_name = "notifications"

    async def iterate(self):
        connection = await aio_pika.connect_robust(self.broker_url)
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue(self.queue_name, auto_delete=True)
            async with queue.iterator() as notifications:
                async for notification in notifications:
                    yield Notification.parse_raw(notification.body.decode("utf-8"))

    @classmethod
    def from_config(cls):
        return cls(broker_url=Config.get(SHOPEAT_AMQP_BROKER_URL))
