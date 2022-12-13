from fastapi import APIRouter, Depends

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

router = APIRouter()
account_service = AccountService(SQLAccountRepository(DATABASE))


@router.post("/auth/token")
async def get_token(credentials: CredentialsDTO):
    account = await account_service.authenticate(credentials)
    return {"access_token": generate_token(account.uid)}


@router.post("/accounts", response_model=AccountReadDTO)
async def create_account(account_dto: AccountCreateDTO):
    return await account_service.create_account(account_dto)


@router.get("/accounts/whoami", response_model=AccountReadDTO)
async def get_account_from_token(account_uid: str = Depends(authenticate)):
    return await account_service.get_account_by_uid(account_uid)
