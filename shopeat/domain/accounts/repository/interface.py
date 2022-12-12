from abc import ABC, abstractmethod

from shopeat.domain.accounts.dtos import (
    AccountCreateDTO,
    AccountReadDTO,
    CredentialsDTO,
)


class AccountRepository(ABC):
    @abstractmethod
    async def authenticate(self, credentials_dto: CredentialsDTO) -> AccountReadDTO:
        ...

    @abstractmethod
    async def get_by_uid(self, account_uid: str) -> AccountReadDTO:
        ...

    @abstractmethod
    async def create(self, account_dto: AccountCreateDTO) -> AccountReadDTO:
        ...
