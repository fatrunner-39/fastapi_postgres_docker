from fastapi import APIRouter, Depends, Request

from db import get_db_session
from helpers import AuthJWT, JWTBearer, get_dict_from_token
from managers import like_manager
from schema import Like, NewLike

router = APIRouter()


@router.put("/like/", dependencies=[Depends(JWTBearer())])
def create_or_update_like(request: Request, like: Like, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        object = like_manager.update_or_create(
            request, like, session, current_user=current_user
        )
        session.commit()
        return NewLike.from_orm(object)


@router.put("/dislike/", dependencies=[Depends(JWTBearer())])
def create_or_update_like(request: Request, like: Like, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        object = like_manager.update_or_create(
            request, like, session, current_user=current_user
        )
        session.commit()
        return NewLike.from_orm(object)
