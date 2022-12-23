from typing import Sequence
from uuid import uuid4

from pydantic import parse_obj_as
from sqlalchemy import Column, Integer, String, select
from sqlalchemy.ext.asyncio import AsyncSession

from shopeat.core.database import Database, DBModel
from shopeat.domain.recipes.dtos import RecipeDetailsDTO, RecipeReadDTO, RecipeWriteDTO
from shopeat.domain.recipes.repository.interface import RecipeRepository


class Recipe(DBModel):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    thumbnail_url = Column(String)
    description = Column(String)

    ingredients = []
    steps = []


class RecipeNotFoundError(Exception):
    ...


async def get_recipe_by_uid(session: AsyncSession, recipe_uid: str):
    recipe = (
        await session.execute(select(Recipe).where(Recipe.uid == recipe_uid))
    ).scalar()
    if recipe is None:
        raise RecipeNotFoundError
    return recipe


class SQLRecipeRepository(RecipeRepository):
    def __init__(self, database: Database):
        self.database = database

    async def search(self, query: str) -> Sequence[RecipeReadDTO]:
        async with self.database.session.begin() as session:
            query_results = await session.execute(
                select(Recipe).where(Recipe.name.contains(query)).limit(50)
            )
            recipes = query_results.scalars().all()
            return parse_obj_as(Sequence[RecipeReadDTO], recipes)

    async def get_detail(self, recipe_uid: str) -> RecipeDetailsDTO:
        async with self.database.session.begin() as session:
            recipe = await get_recipe_by_uid(session, recipe_uid)
            session.add(recipe)
            return RecipeDetailsDTO.from_orm(recipe)

    async def create(self, recipe_create_dto: RecipeWriteDTO) -> RecipeReadDTO:
        async with self.database.session.begin() as session:
            recipe = Recipe(uid=uuid4().hex, **recipe_create_dto.dict())
            session.add(recipe)
            return RecipeReadDTO.from_orm(recipe)

    async def update(
        self, recipe_uid: str, recipe_update_dto: RecipeWriteDTO
    ) -> RecipeReadDTO:
        async with self.database.session.begin() as session:
            recipe = await get_recipe_by_uid(session, recipe_uid)
            for attr, value in recipe_update_dto.dict().items():
                setattr(recipe, attr, value)
            return RecipeReadDTO.from_orm(recipe)

    async def delete(self, recipe_uid: str) -> RecipeReadDTO:
        async with self.database.session.begin() as session:
            recipe = await get_recipe_by_uid(session, recipe_uid)
            await session.delete(recipe)
            return RecipeReadDTO.from_orm(recipe)
