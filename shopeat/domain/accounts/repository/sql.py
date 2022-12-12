from uuid import uuid4

from sqlalchemy import Integer, String, select
from sqlalchemy.orm import mapped_column

from shopeat.core.database import Database, DBModel
from shopeat.domain.accounts.dtos import (
    AccountCreateDTO,
    AccountReadDTO,
    CredentialsDTO,
)
from shopeat.domain.accounts.repository.interface import AccountRepository


class Account(DBModel):
    __tablename__ = "accounts"

    id = mapped_column(Integer, primary_key=True)
    uid = mapped_column(String(36), unique=True, nullable=False)
    email = mapped_column(String(50), unique=True, nullable=False)
    username = mapped_column(String(25), unique=True, nullable=False)
    password = mapped_column(String(36), nullable=False)


class SQLAccountRepository(AccountRepository):
    def __init__(self, database: Database):
        self.database = database

    async def authenticate(self, credentials_dto: CredentialsDTO) -> AccountReadDTO:
        async with self.database.session.begin() as session:
            account = (
                await session.execute(
                    select(Account).where(
                        Account.username == credentials_dto.username,
                        Account.password == credentials_dto.password,
                    )
                )
            ).scalar_one()
            return AccountReadDTO.from_orm(account)

    async def get_by_uid(self, account_uid: str) -> AccountReadDTO:
        async with self.database.session.begin() as session:
            account = (
                await session.execute(select(Account).where(Account.uid == account_uid))
            ).scalar_one()
            return AccountReadDTO.from_orm(account)

    async def create(self, account_dto: AccountCreateDTO) -> AccountReadDTO:
        async with self.database.session.begin() as session:
            account = Account(uid=uuid4().hex, **account_dto.dict())
            session.add(account)
            return AccountReadDTO.from_orm(account)
