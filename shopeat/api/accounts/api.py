from typing import Dict
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from shopeat.api.accounts.dtos import AccountCreateDTO, AccountReadDTO, CredentialsDTO
from shopeat.auth.fastapi import authenticate
from shopeat.auth.tokens import generate_token

router = APIRouter()
accounts: Dict[str, AccountReadDTO] = {}


@router.post("/auth/token")
async def get_token(credentials: CredentialsDTO):
    try:
        account = next(
            account
            for account in accounts.values()
            if account.username == credentials.username
        )
    except StopIteration:
        raise HTTPException(401, detail="Failed to authenticate from credentials")
    return {"access_token": generate_token(account.uid)}


@router.post("/accounts/create", response_model=AccountReadDTO)
async def create_account(account: AccountCreateDTO):
    account_data = account.dict()
    account_data["uid"] = uuid4().hex
    account = AccountReadDTO.parse_obj(account_data)
    accounts[account_data["uid"]] = account
    return account


@router.get("/accounts/whoami", response_model=AccountReadDTO)
async def get_account_from_token(account_uid: str = Depends(authenticate)):
    account = accounts.get(account_uid)
    if account is None:
        raise HTTPException(401, detail="Failed to authenticate from token")
    return account
