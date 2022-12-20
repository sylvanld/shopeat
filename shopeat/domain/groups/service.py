from fastapi import HTTPException
from shopeat.domain.groups.dtos import AddMemberDTO, GroupWriteDTO, UpdateMemberDTO
from shopeat.domain.groups.repository.exceptions import CantDeleteLastGroupMemberError
from shopeat.domain.groups.repository.interface import GroupRepository


class GroupService:
    def __init__(self, group_repository: GroupRepository):
        self.group_repository = group_repository

    async def get_several_by_member(self, account_uid: str):
        return await self.group_repository.get_several_by_member(account_uid)

    async def create_group(self, create_group_dto: GroupWriteDTO, group_owner: str):
        return await self.group_repository.create(create_group_dto, group_owner=group_owner)

    async def leave_group(self, group_uid: str, account_uid: str):
        # TODO: move controls in service instead of repository
        return await self.group_repository.remove_member(group_uid, account_uid)
    
    async def add_group_member(self, group_uid: str, add_member_dto: AddMemberDTO):
        return await self.group_repository.add_member(group_uid, add_member_dto)

    async def update_role_of_a_group_member(
        self, group_uid: str, account_uid: str, update_member_dto: UpdateMemberDTO
    ):
        return await self.group_repository.update_member_role(group_uid, account_uid, update_member_dto)

    async def remove_group_member(self, group_uid: str, account_uid: str):
        # TODO: check that user performing operation is owner to ensure he has the right to kick someone
        return await self.group_repository.remove_member(group_uid, account_uid)
