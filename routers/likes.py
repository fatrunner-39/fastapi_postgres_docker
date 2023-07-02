from fastapi import APIRouter, Depends, Request

from db import get_db_session
from helpers import AuthJWT, JWTBearer, get_dict_from_token
from helpers.base_schemas import BaseSchema
from managers import like_manager

router = APIRouter()


class Like(BaseSchema):
    user_id: int | None
    post_id: int
    is_like: bool | None = None

    class Config:
        schema_extra = {
            "example": {"post_id": 1, "is_like": True}
        }


class NewLike(BaseSchema):
    id: int
    user_id: int
    post_id: int
    is_like: bool


@router.put("/like/", dependencies=[Depends(JWTBearer())])
def create_or_update_like(request: Request, like: Like, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        object = like_manager.update_or_create(
            like, request, session, current_user=current_user
        )
        session.commit()
        return NewLike.from_orm(object)


@router.put("/dislike/", dependencies=[Depends(JWTBearer())])
def create_or_update_like(request: Request, like: Like, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        object = like_manager.update_or_create(
            like, request, session, current_user=current_user
        )
        session.commit()
        return NewLike.from_orm(object)
