import time
from typing import Optional, TypeVar, Union, List

from fastapi import HTTPException
from sqlalchemy import delete, select, update

from db import Base, async_session, get_db_session

ModelType = TypeVar("ModelType", bound=Base)


class BaseManager:

    def __init__(self, model: ModelType):
        self.model = model

    def create(self, schema, session, *args, **kwargs) -> ModelType:
        if type(schema) == dict:
            instance: ModelType = self.model(**schema)
        else:
            instance = self.model(**schema.dict())
        session.add(instance)
        return instance

    def get_all(self, session) -> List[ModelType]:
        instances: List[ModelType] = session.query(self.model).all()
        return instances

    async def update(self, schema, id, as_dict: Optional[bool] = False, *args, **kwargs):
        await self.get_by_id(id)
        async with async_session() as session:
            async with session.begin():
                if type(schema) == dict:
                    await session.execute(update(self.model).where(self.model.id == id).values(**schema))
                else:
                    await session.execute(update(self.model).where(self.model.id == id).values(**schema.dict()))
                await session.commit()
                instance = await self.get_by_id(id)
                if not as_dict:
                    return instance
                else:
                    return instance.as_dict()

    async def get_by_id(self, id, as_dict: Optional[bool] = False,):
        async with async_session() as session:
            async with session.begin():
                instance = await session.execute(select(self.model).where(self.model.id == id))
                instance = instance.scalar()
                if not instance:
                    raise HTTPException(
                        status_code=404,
                        detail={"error": f"Instance with id = {id} doesn't exist!"})
                if as_dict:
                    return instance.as_dict()
                else:
                    return instance

    async def delete(self, id):
        async with async_session() as session:
            async with session.begin():
                await session.execute(delete(self.model).where(self.model.id == id))
                await session.commit()
