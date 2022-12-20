from typing import List

from fastapi import APIRouter, Depends

from shopeat.core.auth.fastapi import authenticate
from shopeat.core.database import DATABASE
from shopeat.domain.groups.dtos import (
    AddMemberDTO,
    GroupMemberDTO,
    GroupReadDTO,
    GroupWriteDTO,
    UpdateMemberDTO,
)
from shopeat.domain.groups.repository.sql import SQLGroupRepository
from shopeat.domain.groups.service import GroupService

router = APIRouter(tags=["Groups"])
group_service = GroupService(SQLGroupRepository(DATABASE))


@router.get("/groups", response_model=List[GroupReadDTO])
async def search_groups(token_account_uid: str = Depends(authenticate)):
    """Search in groups of which the current user is a member."""
    return await group_service.get_several_by_member(account_uid=token_account_uid)


@router.post("/groups", response_model=GroupReadDTO, status_code=201)
async def create_group(
    create_group_dto: GroupWriteDTO, token_account_uid: str = Depends(authenticate)
):
    """Create a group of users.

    Current user is automatically defined as group owner.
    """
    return await group_service.create_group(
        create_group_dto, group_owner=token_account_uid
    )


@router.post("/groups/{group_uid}/leave")
async def leave_group(group_uid: str, token_account_uid: str = Depends(authenticate)):
    """Make current user leave a group of which it is a member.

    If group contains others members and you are the only owner,
    you must delegate ownership of the group to another member before.
    """
    return await group_service.leave_group(group_uid, account_uid=token_account_uid)


@router.post("/groups/{group_uid}/admin/members", response_model=GroupMemberDTO)
async def add_group_member(
    group_uid: str,
    add_member_dto: AddMemberDTO,
    token_account_uid: str = Depends(authenticate),
):
    """Add user as a new member of the group."""
    return await group_service.add_group_member(group_uid, add_member_dto)


@router.put(
    "/groups/{group_uid}/admin/members/{account_uid}", response_model=GroupMemberDTO
)
async def update_role_of_a_group_member(
    group_uid: str,
    account_uid: str,
    update_member_dto: UpdateMemberDTO,
    token_account_uid: str = Depends(authenticate),
):
    """Update role of a user in the group."""
    return await group_service.update_role_of_a_group_member(
        group_uid, account_uid, update_member_dto
    )


@router.delete(
    "/groups/{group_uid}/admin/members/{account_uid}", response_model=GroupMemberDTO
)
async def remove_group_member(
    group_uid: str, token_account_uid: str = Depends(authenticate)
):
    """Remove user from group members."""
    return await group_service.remove_group_member(
        group_uid, account_uid=token_account_uid
    )
