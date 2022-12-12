from datetime import datetime, timedelta

import jwt

from shopeat.config import SHOPEAT_JWT_SECRET_KEY, Config


def generate_token(account_uid: str) -> str:
    return jwt.encode(
        {"sub": account_uid, "exp": datetime.utcnow() + timedelta(days=1)},
        Config.get(SHOPEAT_JWT_SECRET_KEY),
        algorithm="HS256",
    )


def account_uid_from_token(token: str) -> str:
    payload = jwt.decode(
        token, Config.get(SHOPEAT_JWT_SECRET_KEY), algorithms=["HS256"]
    )
    return payload["sub"]
