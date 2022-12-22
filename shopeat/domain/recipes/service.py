from typing import Sequence

from fastapi import HTTPException

from shopeat.domain.recipes.dtos import RecipeDetailsDTO, RecipeReadDTO, RecipeWriteDTO
from shopeat.domain.recipes.repository.interface import RecipeRepository
from shopeat.domain.recipes.repository.sql import RecipeNotFoundError


class RecipeService:
    def __init__(self, recipe_repository: RecipeRepository):
        self.recipe_repository = recipe_repository

    async def search_recipes(self, query: str) -> Sequence[RecipeReadDTO]:
        return await self.recipe_repository.search(query)

    async def get_recipe_details(self, recipe_uid: str) -> RecipeDetailsDTO:
        try:
            return await self.recipe_repository.get_detail(recipe_uid)
        except RecipeNotFoundError:
            raise HTTPException(404, detail=f"No recipe with UID {recipe_uid}")

    async def create_recipe(self, recipe_create_dto: RecipeWriteDTO) -> RecipeReadDTO:
        return await self.recipe_repository.create(recipe_create_dto)

    async def update_recipe(
        self, recipe_uid: str, recipe_update_dto: RecipeWriteDTO
    ) -> RecipeReadDTO:
        try:
            return await self.recipe_repository.update(recipe_uid, recipe_update_dto)
        except RecipeNotFoundError:
            raise HTTPException(404, detail=f"No recipe with UID {recipe_uid}")

    async def delete_recipe(self, recipe_uid: str) -> RecipeReadDTO:
        try:
            return await self.recipe_repository.delete(recipe_uid)
        except RecipeNotFoundError:
            raise HTTPException(404, detail=f"No recipe with UID {recipe_uid}")
