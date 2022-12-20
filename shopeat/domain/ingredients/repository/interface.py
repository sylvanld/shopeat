from abc import ABC, abstractmethod
from typing import Sequence

from shopeat.domain.ingredients.dtos import (
    IngredientCreateDTO,
    IngredientReadDTO,
    IngredientUpdateDTO,
    ShelveCreateDTO,
    ShelveReadDTO,
)


class ShelveRepository(ABC):
    @abstractmethod
    async def get_by_uid(self, shelve_uid: str) -> ShelveReadDTO:
        ...

    @abstractmethod
    async def get_all(self) -> Sequence[ShelveReadDTO]:
        ...

    @abstractmethod
    async def create(self, shelve_create_dto: ShelveCreateDTO) -> ShelveReadDTO:
        ...


class IngredientRepository(ABC):
    @abstractmethod
    async def search(self, query: str) -> Sequence[IngredientReadDTO]:
        ...

    @abstractmethod
    async def get_several_by_uids(
        self, ingredient_uids: Sequence[str]
    ) -> Sequence[IngredientReadDTO]:
        ...

    @abstractmethod
    async def create(
        self, ingredient_create_dto: IngredientCreateDTO
    ) -> IngredientReadDTO:
        ...

    @abstractmethod
    async def update(
        self, ingredient_uid: str, ingredient_update_dto: IngredientUpdateDTO
    ) -> IngredientReadDTO:
        ...
