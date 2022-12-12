from shopeat.core.auth.tokens import account_uid_from_token
from shopeat.domain.accounts.dtos import AccountCreateDTO, CredentialsDTO
from shopeat.domain.accounts.repository.interface import AccountRepository


class AccountService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    async def authenticate(self, credentials: CredentialsDTO):
        return await self.account_repository.authenticate(credentials)
        # TODO: raise HTTPException(401, detail="Failed to authenticate from credentials")

    async def authenticate_from_token(self, access_token: str):
        account_uid = account_uid_from_token(access_token)
        return await self.account_repository.get_by_uid(account_uid)

    async def create_account(self, account_dto: AccountCreateDTO):
        return await self.account_repository.create(account_dto)

    async def get_account_by_uid(self, account_uid: str):
        return await self.account_repository.get_by_uid(account_uid)
