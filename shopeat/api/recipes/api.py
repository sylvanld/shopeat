from typing import Sequence

from fastapi import APIRouter, Depends

from shopeat.core.auth.fastapi import authenticate
from shopeat.core.database import DATABASE
from shopeat.domain.recipes.dtos import RecipeDetailsDTO, RecipeReadDTO, RecipeWriteDTO
from shopeat.domain.recipes.repository.sql import SQLRecipeRepository
from shopeat.domain.recipes.service import RecipeService

router = APIRouter(tags=["Recipes"])
recipe_service = RecipeService(SQLRecipeRepository(DATABASE))


@router.get("/recipes/search", response_model=Sequence[RecipeReadDTO])
async def search_recipes(query: str, token_account_uid: str = Depends(authenticate)):
    return await recipe_service.search_recipes(query)


@router.post("/recipes", response_model=RecipeReadDTO, status_code=201)
async def create_recipe(
    recipe_create_dto: RecipeWriteDTO, token_account_uid: str = Depends(authenticate)
):
    return await recipe_service.create_recipe(recipe_create_dto)


@router.get("/recipes/{recipe_uid}", response_model=RecipeDetailsDTO)
async def get_recipe_details(
    recipe_uid: str, token_account_uid: str = Depends(authenticate)
):
    return await recipe_service.get_recipe_details(recipe_uid)


@router.put("/recipes/{recipe_uid}", response_model=RecipeReadDTO)
async def update_recipe(
    recipe_uid: str,
    recipe_update_dto: RecipeWriteDTO,
    token_account_uid: str = Depends(authenticate),
):
    return await recipe_service.update_recipe(recipe_uid, recipe_update_dto)


@router.delete("/recipes/{recipe_uid}", response_model=RecipeReadDTO)
async def delete_recipe(
    recipe_uid: str, token_account_uid: str = Depends(authenticate)
):
    return await recipe_service.delete_recipe(recipe_uid)
