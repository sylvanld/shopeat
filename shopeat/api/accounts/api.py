import json
from typing import Optional
from urllib.parse import parse_qsl

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from shopeat.core.auth.fastapi import authenticate
from shopeat.core.auth.tokens import generate_token
from shopeat.core.database import DATABASE
from shopeat.domain.accounts.dtos import (
    AccountCreateDTO,
    AccountReadDTO,
    CredentialsDTO,
)
from shopeat.domain.accounts.repository.sql import SQLAccountRepository
from shopeat.domain.accounts.service import AccountService

router = APIRouter(tags=["Accounts"])
account_service = AccountService(SQLAccountRepository(DATABASE))


async def auth_credentials(request: Request):
    """Dependency used to accept credentials either from form data or json payload!"""

    content_type = request.headers.get("Content-Type", "application/json")

    if content_type == "application/x-www-form-urlencoded":
        raw_body = (await request.body()).decode("utf-8")
        request_data = dict(parse_qsl(raw_body))
    elif content_type == "application/json":
        request_data = await request.json()
    else:
        raise HTTPException(400, detail="Unsupported content type!")

    if request_data.get("username") is None or request_data.get("password") is None:
        raise HTTPException(
            400,
            "You must provide both username and password as form data, or json payload!",
            headers={"X-Received-Data": json.dumps(request_data)},
        )

    return CredentialsDTO.parse_obj(request_data)


@router.post("/auth/token")
async def get_token(credentials: CredentialsDTO = Depends(auth_credentials)):
    account = await account_service.authenticate(credentials)
    return {"access_token": generate_token(account.uid)}


@router.post("/accounts", response_model=AccountReadDTO, status_code=201)
async def create_account(account_dto: AccountCreateDTO):
    return await account_service.create_account(account_dto)


@router.get("/accounts/whoami", response_model=AccountReadDTO)
async def get_account_from_token(account_uid: str = Depends(authenticate)):
    return await account_service.get_account_by_uid(account_uid)
