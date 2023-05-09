from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True


T = TypeVar("T")


class View(GenericModel, Generic[T]):
    items: list[T]
    meta: dict

    @classmethod
    def from_list(cls, model: BaseSchema, objects: list, meta: dict):
        return View(items=list(map(model.from_orm, objects)), meta=meta)
