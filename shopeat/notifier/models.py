from datetime import datetime

from pydantic import BaseModel, Field


class Notification(BaseModel):
    kind: str
    created: datetime = Field(default_factory=datetime.utcnow)
    data: dict
