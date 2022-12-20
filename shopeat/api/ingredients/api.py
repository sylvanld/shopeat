from typing import Sequence

from fastapi import APIRouter, Depends, Query

from shopeat.core.auth.fastapi import authenticate
from shopeat.core.database import DATABASE
from shopeat.domain.ingredients.dtos import (
    IngredientCreateDTO,
    IngredientReadDTO,
    ShelveCreateDTO,
    ShelveReadDTO,
)
from shopeat.domain.ingredients.repository.sql import (
    SQLIngredientRepository,
    SQLShelveRepository,
)
from shopeat.domain.ingredients.service import IngredientService

router = APIRouter(tags=["Ingredients"])
ingredient_service = IngredientService(
    ingredient_repository=SQLIngredientRepository(DATABASE),
    shelve_repository=SQLShelveRepository(DATABASE),
)


@router.get("/shelves", response_model=Sequence[ShelveReadDTO])
async def list_ingredient_shelves(token_account_uid: str = Depends(authenticate)):
    return await ingredient_service.list_ingredient_shelves()


@router.post("/shelves", response_model=ShelveReadDTO)
async def add_ingredient_shelve(
    shelve_create_dto: ShelveCreateDTO, token_account_uid: str = Depends(authenticate)
):
    return await ingredient_service.create_ingredient_shelve(shelve_create_dto)


@router.get("/ingredients/search", response_model=Sequence[IngredientReadDTO])
async def search_ingredients(
    query: str, token_account_uid: str = Depends(authenticate)
):
    return await ingredient_service.search_ingredients(query)


@router.get("/ingredients", response_model=Sequence[IngredientReadDTO])
async def get_several_ingredients_by_uids(
    uids: str = Query(description="Coma separated List of ingredients UIDs"),
    token_account_uid: str = Depends(authenticate),
):
    ingredient_uids = uids.split(",")
    return await ingredient_service.get_ingredients_by_uids(ingredient_uids)


@router.post("/ingredients", response_model=IngredientReadDTO)
async def add_ingredient(
    ingredient_create_dto: IngredientCreateDTO,
    token_account_uid: str = Depends(authenticate),
):
    return await ingredient_service.create_ingredient(ingredient_create_dto)
