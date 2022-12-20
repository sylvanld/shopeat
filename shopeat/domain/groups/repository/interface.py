from abc import ABC, abstractmethod
from typing import List

from shopeat.domain.groups.dtos import (
    AddMemberDTO,
    GroupMemberDTO,
    GroupReadDTO,
    GroupWriteDTO,
    UpdateMemberDTO,
)


class GroupRepository(ABC):
    @abstractmethod
    async def get_several_by_member(self, account_uid: str) -> List[GroupReadDTO]:
        ...

    @abstractmethod
    async def create(self, create_group_dto: GroupWriteDTO) -> GroupReadDTO:
        ...

    @abstractmethod
    async def add_member(
        self, group_uid: str, add_member_dto: AddMemberDTO
    ) -> GroupMemberDTO:
        ...

    @abstractmethod
    async def update_member_role(
        self, group_uid: str, account_uid: str, update_member_dto: UpdateMemberDTO
    ) -> GroupMemberDTO:
        ...

    @abstractmethod
    async def remove_member(self, group_uid: str, account_uid: str) -> GroupMemberDTO:
        ...
