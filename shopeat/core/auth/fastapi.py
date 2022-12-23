from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from shopeat.core.auth.exceptions import InvalidAccessToken
from shopeat.core.auth.tokens import account_uid_from_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_access_token():
    return oauth2_scheme


async def authenticate(token: str = Depends(get_access_token())):
    try:
        return account_uid_from_token(token)
    except InvalidAccessToken as error:
        raise HTTPException(401, "Invalid access token") from error
