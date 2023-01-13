import time

from db import async_session, Base, get_db_session
from typing import TypeVar, Optional, Union
from sqlalchemy import select, update, delete
from fastapi import HTTPException

ModelType = TypeVar("ModelType", bound=Base)


class BaseManager:

    def __init__(self, model: ModelType):
        self.model = model

    async def create(self, schema, as_dict: Optional[bool] = False, *args, **kwargs):
        async with async_session() as session:
            async with session.begin():
                if type(schema) == dict:
                    instance = self.model(**schema)
                else:
                    instance = self.model(**schema.dict())
                session.add(instance)
                await session.commit()
                if not as_dict:
                    return instance
                return instance.as_dict()

    async def get_all(self, as_dict: Optional[bool] = False):
        with get_db_session() as db:
            instances = db.query(self.model).all()
            time.sleep(15)
            if not as_dict:
                return instances
            else:
                return [instance.as_dict() for instance in instances]
        # async with async_session() as session:
        #     async with session.begin():
        #         instances = await session.execute(select(self.model))
        #         instances = instances.scalars().all()
        #         if not as_dict:
        #             return instances
        #         else:
        #             return [instance.as_dict() for instance in instances]

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
