from shopeat.core.dtos import BaseDTO


class AccountBaseDTO(BaseDTO):
    email: str
    username: str


class AccountCreateDTO(AccountBaseDTO):
    password: str


class AccountReadDTO(AccountBaseDTO):
    uid: str


class CredentialsDTO(BaseDTO):
    username: str
    password: str
