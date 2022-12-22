from abc import ABC, abstractmethod
from typing import Sequence

from shopeat.domain.recipes.dtos import RecipeDetailsDTO, RecipeReadDTO, RecipeWriteDTO


class RecipeRepository(ABC):
    @abstractmethod
    async def search(self, query: str) -> Sequence[RecipeReadDTO]:
        ...

    @abstractmethod
    async def get_detail(self, recipe_uid: str) -> RecipeDetailsDTO:
        ...

    @abstractmethod
    async def create(self, recipe_create_dto: RecipeWriteDTO) -> RecipeReadDTO:
        ...

    @abstractmethod
    async def update(
        self, recipe_uid: str, recipe_update_dto: RecipeWriteDTO
    ) -> RecipeReadDTO:
        ...

    @abstractmethod
    async def delete(self, recipe_uid: str) -> RecipeReadDTO:
        ...
