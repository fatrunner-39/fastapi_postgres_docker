from dataclasses import dataclass
from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


T = TypeVar("T")


@dataclass
class Pagi:
    items: list
    page: str
    total_count: int

    def from_paginate_func(self):
        return {"page": self.page, "total_count": self.total_count}


class View(GenericModel, Generic[T]):
    items: list[T]
    meta: dict

    @classmethod
    def from_list(cls, model: BaseSchema, objects: Pagi):
        return View(
            items=list(map(model.from_orm, objects.items)),
            meta=objects.from_paginate_func(),
        )
