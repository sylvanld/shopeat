from typing import Optional
from shopeat.core.dtos import BaseDTO


class GroupWriteDTO(BaseDTO):
    name: str
    thumbnail_url: str = None


class GroupReadDTO(BaseDTO):
    uid: str
    name: str
    thumbnail_url: Optional[str]


class AddMemberDTO(BaseDTO):
    account_uid: str
    nickname: str
    role: str


class UpdateMemberDTO(BaseDTO):
    nickname: str
    role: str


class GroupMemberDTO(BaseDTO):
    account_uid: str
    nickname: str
    role: str
