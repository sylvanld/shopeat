from typing import Sequence
from uuid import uuid4

from pydantic import parse_obj_as
from sqlalchemy import Column, ForeignKey, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from shopeat.core.database import Database, DBModel
from shopeat.domain.ingredients.dtos import (
    IngredientCreateDTO,
    IngredientReadDTO,
    IngredientUpdateDTO,
    ShelveCreateDTO,
    ShelveReadDTO,
)
from shopeat.domain.ingredients.repository.exceptions import ShelveDoesNotExists
from shopeat.domain.ingredients.repository.interface import (
    IngredientRepository,
    ShelveRepository,
)


class Shelve(DBModel):
    __tablename__ = "shelves"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Ingredient(DBModel):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True)
    shelve_uid = Column(ForeignKey("shelves.uid"))
    uid = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    shelve = relationship("Shelve")


async def get_shelve_by_uid(session: AsyncSession, shelve_uid: str):
    shelve = (
        await session.execute(select(Shelve).where(Shelve.uid == shelve_uid))
    ).scalar()
    if shelve is None:
        raise ShelveDoesNotExists
    return shelve


class SQLShelveRepository(ShelveRepository):
    def __init__(self, database: Database):
        self.database = database

    async def get_all(self) -> Sequence[ShelveReadDTO]:
        async with self.database.session.begin() as session:
            query = await session.execute(select(Shelve))
            shelves = query.scalars().all()
            return parse_obj_as(Sequence[ShelveReadDTO], shelves)

    async def get_by_uid(self, shelve_uid: str) -> ShelveReadDTO:
        """Get shelve by UID.

        Returns None if no shelve match this UID.
        """
        async with self.database.session.begin() as session:
            query = await session.execute(
                select(Shelve).where(Shelve.uid == shelve_uid)
            )
            shelve = query.scalar()
            if shelve is None:
                return
            return ShelveReadDTO.from_orm(shelve)

    async def create(self, shelve_create_dto: ShelveCreateDTO) -> ShelveReadDTO:
        shelve_data = shelve_create_dto.dict()
        shelve_data["uid"] = uuid4().hex[:6]

        async with self.database.session.begin() as session:
            created_shelve = Shelve(**shelve_data)
            session.add(created_shelve)
            return ShelveReadDTO.from_orm(created_shelve)


class SQLIngredientRepository(IngredientRepository):
    def __init__(self, database: Database):
        self.database = database

    async def search(self, query: str) -> Sequence[IngredientReadDTO]:
        async with self.database.session.begin() as session:
            ingredients = (
                (
                    await session.execute(
                        select(Ingredient)
                        .where(Ingredient.name.contains(query))
                        .limit(50)
                    )
                )
                .scalars()
                .all()
            )
            return parse_obj_as(Sequence[IngredientReadDTO], ingredients)

    async def get_several_by_uids(
        self, ingredient_uids: Sequence[str]
    ) -> Sequence[IngredientReadDTO]:
        async with self.database.session.begin() as session:
            query = await session.execute(
                select(Ingredient).where(Ingredient.uid.in_(ingredient_uids))
            )
            ingredients = query.scalars().all()
            return parse_obj_as(Sequence[IngredientReadDTO], ingredients)

    async def create(
        self, ingredient_create_dto: IngredientCreateDTO
    ) -> IngredientReadDTO:
        ingredient_data = ingredient_create_dto.dict()
        ingredient_data["uid"] = uuid4().hex

        async with self.database.session.begin() as session:
            ingredient = Ingredient(**ingredient_data)
            session.add(ingredient)
            return IngredientReadDTO.from_orm(ingredient)

    async def update(
        self, ingredient_uid: str, ingredient_update_dto: IngredientUpdateDTO
    ) -> IngredientReadDTO:
        ...
