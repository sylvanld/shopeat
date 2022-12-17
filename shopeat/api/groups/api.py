from typing import List

from fastapi import APIRouter

from shopeat.domain.groups.dtos import (
    AddMemberDTO,
    GroupMemberDTO,
    GroupReadDTO,
    GroupWriteDTO,
    UpdateMemberDTO,
)

router = APIRouter(tags=["Groups"])


@router.get("/groups", response_model=List[GroupReadDTO])
async def search_groups():
    """Search in groups of which the current user is a member."""


@router.post("/groups", response_model=GroupReadDTO)
async def create_group(create_group_dto: GroupWriteDTO):
    """Create a group of users.

    Current user is automatically defined as group owner.
    """


@router.post("/groups/{group_uid}/leave")
async def leave_group():
    """Make current user leave a group of which it is a member.

    If group contains others members and you are the only owner,
    you must delegate ownership of the group to another member before.
    """


@router.post("/groups/{group_uid}/admin/members", response_model=GroupMemberDTO)
async def add_group_member(group_uid: str, add_member_dto: AddMemberDTO):
    """Add user as a new member of the group."""


@router.put(
    "/groups/{group_uid}/admin/members/{account_uid}", response_model=GroupMemberDTO
)
async def update_role_of_a_group_member(
    group_uid: str, update_member_dto: UpdateMemberDTO
):
    """Update role of a user in the group."""


@router.delete(
    "/groups/{group_uid}/admin/members/{account_uid}", response_model=GroupMemberDTO
)
async def remove_group_member(group_uid: str):
    """Remove user from group members."""
