from fastapi import APIRouter, Depends, Query

from db import get_db_session
from helpers import AuthJWT, JWTBearer, get_dict_from_token
from managers import post_manager
from schema import NewPost, Post, PostUpdate, View

router = APIRouter()


@router.post("/", dependencies=[Depends(JWTBearer())])
def create_post(post: Post, Authorize: AuthJWT = Depends()):
    creator_id = get_dict_from_token(Authorize)
    with get_db_session() as session:
        new_post = post_manager.create(post, session, creator_id=creator_id)
        session.commit()
        return NewPost.from_orm(new_post)


@router.get("/", dependencies=[Depends(JWTBearer())])
def get_all_posts(
    page: int = Query(1, description="Page number", ge=1),
    page_size: int = Query(50, description="Items per page", ge=1),
):
    with get_db_session() as session:
        posts, meta = post_manager.get_all(session, page=page, page_size=page_size)
        print(posts)

    return View.from_list(NewPost, posts, meta)


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
def get_post(id: int):
    with get_db_session() as session:
        post = post_manager.get_by_id(id, session)
    return NewPost.from_orm(post)


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
