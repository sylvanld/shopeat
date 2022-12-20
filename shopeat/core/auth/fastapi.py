from fastapi import Depends, Header, HTTPException
from fastapi.security import OAuth2PasswordBearer

from shopeat.core.auth.tokens import account_uid_from_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_access_token():
    return oauth2_scheme

async def authenticate(token: str = Depends(get_access_token())):
    return account_uid_from_token(token)
