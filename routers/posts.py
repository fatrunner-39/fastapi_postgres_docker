from schema import Post, PostUpdate
from fastapi import APIRouter, Depends

from helpers import JWTBearer, get_dict_from_token, AuthJWT
from managers import post_manager

router = APIRouter()


@router.post("/", dependencies=[Depends(JWTBearer())])
async def create_post(post: Post, Authorize:AuthJWT = Depends()):
    creator_id = get_dict_from_token(Authorize)
    new_post = await post_manager.create(post, as_dict_extra=True, creator_id=creator_id)
    return new_post


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_all_posts():
    posts = await post_manager.get_all(as_dict=True)
    return posts


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def get_post(id: int):
    post = await post_manager.get_by_id(id, as_dict=True)
    return post


@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def update_post(post: PostUpdate, id:int, Authorize:AuthJWT = Depends()):
    current_user = get_dict_from_token(Authorize)
    updated_post = await post_manager.update(post, id, current_user=current_user, as_dict=True)
    return updated_post


@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def delete_post(id: int, Authorize:AuthJWT = Depends()):
    current_user = get_dict_from_token(Authorize)
    await post_manager.delete(id, current_user=current_user)
    return {'success': f'post with id = {id} was deleted'}
