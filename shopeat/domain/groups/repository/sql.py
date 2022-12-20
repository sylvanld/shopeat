from abc import abstractmethod
from typing import List
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

from shopeat.core.database import Database, DBModel
from shopeat.domain.groups.dtos import (
    AddMemberDTO,
    GroupMemberDTO,
    GroupReadDTO,
    GroupWriteDTO,
    UpdateMemberDTO,
)
from shopeat.domain.groups.repository.exceptions import CantDeleteLastGroupMemberError
from shopeat.domain.groups.repository.interface import GroupRepository


class Group(DBModel):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True)
    name = Column(String)
    thumbnail_url = Column(String)
    members = relationship("GroupMember")


class GroupMember(DBModel):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True)
    account_uid = Column(String, ForeignKey("accounts.uid"))
    group_id = Column(Integer, ForeignKey("groups.id"))
    role = Column(String)
    nickname = Column(String, nullable=True)


import sqlalchemy.exc


async def get_group_by_uid(session: AsyncSession, group_uid: str):
    print("getting group by uid", group_uid)
    query_result = await session.execute(
        select(Group).where(Group.uid == group_uid).options(selectinload(Group.members))
    )
    try:
        return query_result.scalar_one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(404, detail=f"Group with UID {group_uid} does not exists.")


async def get_group_member(session: AsyncSession, group: Group, account_uid: str):
    group = await get_group_by_uid(session, group.uid)
    query_result = await session.execute(
        select(GroupMember).where(
            GroupMember.group_id == group.id, GroupMember.account_uid == account_uid
        )
    )
    try:
        return query_result.scalar_one()
    except sqlalchemy.exc.NoResultFound:
        raise HTTPException(
            404, detail=f"Account {account_uid} is not member of group {group.uid}."
        )


class SQLGroupRepository(GroupRepository):
    def __init__(self, database: Database):
        self.database = database

    async def get_several_by_member(self, account_uid: str) -> List[GroupReadDTO]:
        print(f"Searching groups {account_uid} is a member")
        async with self.database.session.begin() as session:
            query = await session.execute(
                select(Group)
                .join(GroupMember)
                .where(GroupMember.account_uid == account_uid)
            )
            groups = query.scalars().all()
            return [GroupReadDTO.from_orm(group) for group in groups]

    async def create(
        self, create_group_dto: GroupWriteDTO, group_owner: str
    ) -> GroupReadDTO:
        async with self.database.session.begin() as session:
            group_data = create_group_dto.dict()
            group_data.update(uid=uuid4().hex)
            group = Group(**group_data)
            group.members.append(
                GroupMember(account_uid=group_owner, group_id=group.id, role="owner")
            )
            session.add(group)
            data = GroupReadDTO.from_orm(group)
            await session.commit()
            return data

    async def add_member(
        self, group_uid: str, add_member_dto: AddMemberDTO
    ) -> GroupMemberDTO:
        async with self.database.session.begin() as session:
            group = await get_group_by_uid(session, group_uid)
            group_member = GroupMember(group_id=group.id, **add_member_dto.dict())
            session.add(group_member)
            await session.commit()
            return GroupMemberDTO.from_orm(group_member)

    async def update_member_role(
        self, group_uid: str, account_uid: str, update_member_dto: UpdateMemberDTO
    ) -> GroupMemberDTO:
        async with self.database.session.begin() as session:
            group = await get_group_by_uid(session, group_uid)
            group_member = await get_group_member(session, group, account_uid)

            for attr, value in update_member_dto.dict().items():
                setattr(group_member, attr, value)

            updated_member = GroupMemberDTO.from_orm(group_member)
            await session.commit()
        return updated_member

    async def remove_member(self, group_uid: str, account_uid: str) -> GroupMemberDTO:
        async with self.database.session.begin() as session:
            group = await get_group_by_uid(session, group_uid=group_uid)

            if len(group.members) == 1:
                raise HTTPException(
                    403,
                    detail="You can't leave group as you are the latest member of the group. Please delete the group instead.",
                )

            number_of_owners = sum(
                1 for member in group.members if member.role == "owner"
            )
            if number_of_owners == 1:
                raise HTTPException(
                    403,
                    detail="You need to define at least one new owner before leaving this group.",
                )

            group_member = await get_group_member(
                session, group=group, account_uid=account_uid
            )
            await session.delete(group_member)
            await session.commit()
