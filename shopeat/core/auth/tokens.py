from datetime import datetime, timedelta

import jwt

from shopeat.core.auth.exceptions import InvalidAccessToken
from shopeat.core.config import Config
from shopeat.settings import SHOPEAT_JWT_SECRET

JWT_SECRET = Config.get(SHOPEAT_JWT_SECRET)


def generate_token(account_uid: str) -> str:
    return jwt.encode(
        {"sub": account_uid, "exp": datetime.utcnow() + timedelta(days=1)},
        JWT_SECRET,
        algorithm="HS256",
    )


def account_uid_from_token(token: str) -> str:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    except jwt.exceptions.DecodeError:
        raise InvalidAccessToken
    return payload["sub"]
