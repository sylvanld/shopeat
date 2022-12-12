from fastapi import APIRouter

from shopeat.notifier.client import Notification, NotificationClientFactory

router = APIRouter()
notifier = NotificationClientFactory.get_instance()


@router.post("/notify")
async def notify_endpoint(notification: Notification):
    await notifier.publish(notification)
