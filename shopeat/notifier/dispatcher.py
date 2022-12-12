from typing import DefaultDict

from shopeat.notifier.models import Notification


class WSNotificationDispatcher:
    def __init__(self):
        self.clients = DefaultDict(list)

    async def register_client(self, websocket):
        self.clients[websocket.account_uid].append(websocket)

    async def dispatch(self, notification: Notification):
        # TODO: sync sending using asyncio.gather
        for _, clients in self.clients.items():
            for client in clients:
                await client.send(notification.json())
