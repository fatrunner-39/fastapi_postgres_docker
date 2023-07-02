from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query

from db import get_db_session
from helpers import AuthJWT, JWTBearer, get_dict_from_token
from helpers.base_schemas import BaseSchema, View
from managers import post_manager

router = APIRouter()


class Post(BaseSchema):
    title: str
    text: str
    creator_id: int | None = None

    class Config:
        schema_extra = {"example": {"title": "Example title", "text": "Example text"}}


class NewPost(BaseSchema):
    id: int
    title: Optional[str]
    text: Optional[str]
    creator_id: Optional[int]
    published: Optional[datetime]
    like: int
    dislike: int


@router.post("/", dependencies=[Depends(JWTBearer())])
def create_post(post: Post, Authorize: AuthJWT = Depends()):
    creator_id = get_dict_from_token(Authorize)
    with get_db_session() as session:
        new_post = post_manager.create(post, session, creator_id=creator_id)
        session.commit()
        return NewPost.from_orm(new_post)


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_posts(
    filter: str = None,
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(50, description="Items per page", ge=1),
):
    with get_db_session() as session:
        posts = post_manager.get_all(session)
        if filter:
            posts = post_manager.filter_by_text(posts, filter)

        posts = post_manager.paginate(posts, page, page_size)

    return View.from_list(NewPost, posts)


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
def get_post(id: int):
    with get_db_session() as session:
        post = post_manager.get_by_id(id, session)
    return NewPost.from_orm(post)


class PostUpdate(BaseSchema):
    title: Optional[str]
    text: Optional[str]

    class Config:
        schema_extra = {"example": {"title": "Updated example", "text": "Updated text"}}


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
def update_post(post: PostUpdate, id: int, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        updated_post = post_manager.update(
            post, id, current_user=current_user, session=session
        )
        session.commit()
        session.refresh(updated_post)

    return NewPost.from_orm(updated_post)


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
def delete_post(id: int, Authorize: AuthJWT = Depends()):
    with get_db_session() as session:
        current_user = get_dict_from_token(Authorize)
        post_manager.delete(id, current_user=current_user, session=session)
        session.commit()
    return {"success": f"post with id = {id} was deleted"}
