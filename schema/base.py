from typing import Generic, TypeVar
from dataclasses import dataclass

from pydantic import BaseModel
from pydantic.generics import GenericModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


T = TypeVar("T")


class Pagi:
    page: str
    total_count: int

    def __init__(self, items, page, total_count):
        self.items = items
        self.page = page
        self.total_count = total_count

    def from_paginate_func(self):
        return {
            "page": self.page,
            "total_count": self.total_count
        }


class View(GenericModel, Generic[T]):
    items: list[T]
    meta: dict

    @classmethod
    def from_list(cls, model: BaseSchema, objects: Pagi):
        return View(items=list(map(model.from_orm, objects.items)), meta=objects.from_paginate_func())

