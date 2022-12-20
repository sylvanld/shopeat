from typing import Sequence

from fastapi import HTTPException

from shopeat.domain.ingredients.dtos import (
    IngredientCreateDTO,
    IngredientUpdateDTO,
    ShelveCreateDTO,
    ShelveReadDTO,
)
from shopeat.domain.ingredients.repository.interface import (
    IngredientRepository,
    ShelveRepository,
)


class IngredientService:
    def __init__(
        self,
        ingredient_repository: IngredientRepository,
        shelve_repository: ShelveRepository,
    ):
        self.ingredient_repository = ingredient_repository
        self.shelve_repository = shelve_repository

    async def shelve_exists(self, shelve_uid: str) -> bool:
        shelve = await self.shelve_repository.get_by_uid(shelve_uid)
        return shelve is not None

    async def create_ingredient_shelve(
        self, shelve_create_dto: ShelveCreateDTO
    ) -> ShelveReadDTO:
        return await self.shelve_repository.create(shelve_create_dto)

    async def list_ingredient_shelves(self):
        return await self.shelve_repository.get_all()

    async def search_ingredients(self, query: str):
        return await self.ingredient_repository.search(query)

    async def get_ingredients_by_uids(self, ingredient_uids: Sequence[str]):
        ingredients = await self.ingredient_repository.get_several_by_uids(
            ingredient_uids
        )
        if len(ingredients) < len(ingredient_uids):
            raise HTTPException(404, detail="Some ingredients where not found!")
        return ingredients

    async def create_ingredient(self, ingredient_create_dto: IngredientCreateDTO):
        # ensure shelve exists before attaching ingredient to this shelve
        if not await self.shelve_exists(ingredient_create_dto.shelve_uid):
            raise HTTPException(
                400,
                detail=f"Shelve with UID {ingredient_create_dto.shelve_uid} does not exists",
            )
        return await self.ingredient_repository.create(ingredient_create_dto)

    async def update_ingredient(
        self, ingredient_uid: str, ingredient_update_dto: IngredientUpdateDTO
    ):
        updated_ingredient_data = ingredient_update_dto.dict()
        # ensure shelve exists before attaching ingredient to this shelve
        if "shelve_uid" in updated_ingredient_data and not await self.shelve_exists(
            ingredient_update_dto.shelve_uid
        ):
            raise HTTPException(
                400,
                detail=f"Shelve with UID {ingredient_update_dto.shelve_uid} does not exists",
            )
        return await self.ingredient_repository.update(
            ingredient_uid, ingredient_update_dto
        )
