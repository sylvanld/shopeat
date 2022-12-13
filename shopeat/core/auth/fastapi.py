from fastapi import Depends, Header, HTTPException

from shopeat.core.auth.tokens import account_uid_from_token


async def token_from_header(x_api_key: str = Header(None)):
    if x_api_key is None:
        raise HTTPException(401, detail="X-Api-Key header is missing!")
    return x_api_key


async def authenticate(token: str = Depends(token_from_header)):
    return account_uid_from_token(token)
