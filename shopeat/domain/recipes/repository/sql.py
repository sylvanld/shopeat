from typing import Sequence

from shopeat.core.database import Database
from shopeat.domain.recipes.dtos import RecipeDetailsDTO, RecipeReadDTO, RecipeWriteDTO
from shopeat.domain.recipes.repository.interface import RecipeRepository


class SQLRecipeRepository(RecipeRepository):
    def __init__(self, database: Database):
        self.database = database

    async def search(self, query: str) -> Sequence[RecipeReadDTO]:
        return await super().search(query)

    async def get_detail(self, recipe_uid: str) -> RecipeDetailsDTO:
        return await super().get_detail(recipe_uid)

    async def create(self, recipe_create_dto: RecipeWriteDTO) -> RecipeReadDTO:
        return await super().create(recipe_create_dto)

    async def update(
        self, recipe_uid: str, recipe_update_dto: RecipeWriteDTO
    ) -> RecipeReadDTO:
        return await super().update(recipe_uid, recipe_update_dto)

    async def delete(self, recipe_uid: str) -> RecipeReadDTO:
        return await super().delete(recipe_uid)
