from typing import Optional

from shopeat.core.dtos import BaseDTO


class IngredientReadDTO(BaseDTO):
    uid: str
    name: str
    shelve_uid: str


class IngredientCreateDTO(BaseDTO):
    name: str
    shelve_uid: str


class IngredientUpdateDTO(BaseDTO):
    name: Optional[str]
    shelve_uid: Optional[str]


class ShelveReadDTO(BaseDTO):
    uid: str
    name: str


class ShelveCreateDTO(BaseDTO):
    name: str
