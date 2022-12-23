from typing import List

from shopeat.core.dtos import BaseDTO


class StepWriteDTO(BaseDTO):
    description: str
    duration_seconds: int = 0


class StepReadDTO(StepWriteDTO):
    uid: str


class IngredientQuantityWriteDTO(BaseDTO):
    quantity: float = None
    unit: str = None


class IngredientQuantityReadDTO(IngredientQuantityWriteDTO):
    uid: str


class RecipeWriteDTO(BaseDTO):
    name: str
    thumbnail_url: str = None
    description: str = None


class RecipeReadDTO(RecipeWriteDTO):
    uid: str


class RecipeDetailsDTO(RecipeReadDTO):
    steps: List[StepReadDTO]
    ingredients: List[IngredientQuantityReadDTO]
