from fastapi import APIRouter, Depends, Query
from pydantic import EmailStr

from db import get_db_session
from helpers import JWTBearer
from helpers.base_schemas import BaseSchema, View
from managers import user_manager

router = APIRouter()


class User(BaseSchema):
    username: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"username": "user@example.com", "password": "password"}
        }


class NewUser(BaseSchema):
    id: int
    username: str


@router.post("/sign_up")
def create_account(user: User):
    with get_db_session() as session:
        new_user = user_manager.create(user, session)
        session.commit()
        return NewUser.from_orm(new_user)


@router.post("/login/")
def login(user: User):
    with get_db_session() as session:
        result = user_manager.check_user(user, session)
    return result


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_users(
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(50, description="Items per page", ge=1),
):
    with get_db_session() as session:
        users = user_manager.get_all(session)
        users = user_manager.paginate(users, page, page_size)

    return View.from_list(NewUser, users)
