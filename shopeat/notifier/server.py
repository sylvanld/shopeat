import logging

import jwt.exceptions
import websockets

from shopeat.core.auth.tokens import account_uid_from_token
from shopeat.core.config import Config
from shopeat.notifier.dispatcher import WSNotificationDispatcher
from shopeat.notifier.plugins.amqp import AMQPNotificationsBroker
from shopeat.notifier.plugins.interface import NotificationsBroker
from shopeat.settings import SHOPEAT_NOTIFIER_HOST, SHOPEAT_NOTIFIER_PORT

LOGGER = logging.getLogger(__name__)


class WSAuthenticationProtocol(websockets.BasicAuthWebSocketServerProtocol):
    async def check_credentials(self, username, access_token):
        if username != "token":
            LOGGER.warning(
                "Websocket authentication failed, user must be 'token'. Received: %s",
                username,
            )
            return False

        try:
            self.account_uid = account_uid_from_token(access_token)
        except jwt.exceptions.InvalidTokenError:
            LOGGER.warning("Invalid access token received!")
            return False

        LOGGER.debug("Account authenticated from token: %s", self.account_uid)
        return True


class WSNotificationServer:
    def __init__(self, notifications_broker: NotificationsBroker):
        self.dispatcher = WSNotificationDispatcher()
        self.notifications_broker = notifications_broker

    async def handle_connection(self, websocket):
        """
        Handle trafic incoming from a given connection and dispatch it to appropriate handlers.
        """
        remote_address = "%s:%s" % websocket.remote_address[0:2]
        LOGGER.info(
            "Connection received from %s. User: %s",
            remote_address,
            websocket.account_uid,
        )
        await self.dispatcher.register_client(websocket)

        async for message in websocket:
            LOGGER.info(
                "Received message from %s. Message: %s", remote_address, message
            )
            await websocket.send("Received 5/5: %s" % message)

    async def run(self):
        """
        Wait for websocket connections.
        Then delegate handling of incoming connections to handle_connection method.
        """
        host = Config.get(SHOPEAT_NOTIFIER_HOST, default="127.0.0.1")
        port = Config.get(SHOPEAT_NOTIFIER_PORT, default=7000)

        LOGGER.info(
            "Notification server waiting for websockets connections on %s:%s",
            host,
            port,
        )
        async with websockets.serve(
            self.handle_connection,
            host,
            int(port),
            create_protocol=WSAuthenticationProtocol,
        ):
            async for notification in self.notifications_broker.iterate():
                await self.dispatcher.dispatch(notification)

    @classmethod
    def from_config(cls):
        return cls(notifications_broker=AMQPNotificationsBroker.from_config())
