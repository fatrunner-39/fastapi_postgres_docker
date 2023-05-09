import math
from typing import List, TypeVar

from fastapi import HTTPException, Query
from sqlalchemy.orm.session import Session

from db import Base
from schema.base import Pagi

ModelType = TypeVar("ModelType", bound=Base)


class BaseManager:
    def __init__(self, model: ModelType):
        self.model = model

    def create(self, schema, session: Session, *args, **kwargs) -> ModelType:
        if type(schema) == dict:
            instance: ModelType = self.model(**schema)
        else:
            instance: ModelType = self.model(**schema.dict())
        session.add(instance)
        return instance

    def get_all(self, session: Session) -> List[ModelType]:
        instances: List[ModelType] = session.query(self.model).order_by(self.model.id)

        return instances

    def get_by_id(self, id, session: Session):
        instance: ModelType = session.query(self.model).filter_by(id=id).scalar()
        if not instance:
            raise HTTPException(
                status_code=404,
                detail={"error": f"Instance with id = {id} doesn't exist!"},
            )
        return instance

    def update(self, schema, id, session: Session, *args, **kwargs):
        self.get_by_id(id, session)
        if type(schema) == dict:
            session.query(self.model).filter_by(id=id).update(
                schema, synchronize_session=False
            )
        else:
            session.query(self.model).filter_by(id=id).update(
                schema.dict(), synchronize_session=False
            )
        instance = self.get_by_id(id, session)
        return instance

    def delete(self, id, session: Session) -> None:
        session.query(self.model).filter_by(id=id).delete(synchronize_session=False)

    def paginate(self, objects: Query, page: int = 1, page_size: int = 50):
        total_count = objects.count()
        total_pages = math.ceil(total_count / page_size)
        objects = objects.limit(page_size).offset((page - 1) * page_size)
        page = f"Page {page} from {total_pages}"
        return Pagi(objects.all(), page, total_count)
