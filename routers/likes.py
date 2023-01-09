from fastapi import Request

from schema import Like
from fastapi import APIRouter, Depends

from managers import like_manager
from helpers import JWTBearer, get_dict_from_token, AuthJWT

router = APIRouter()


@router.put("/like/", dependencies=[Depends(JWTBearer())])
async def create_or_update_like(request: Request, like: Like, Authorize:AuthJWT = Depends()):
    current_user = get_dict_from_token(Authorize)
    object = await like_manager.update_or_create(request, like, as_dict=True, current_user=current_user)
    return object


@router.put("/dislike/", dependencies=[Depends(JWTBearer())])
async def create_or_update_like(request: Request, like: Like, Authorize:AuthJWT = Depends()):
    current_user = get_dict_from_token(Authorize)
    object = await like_manager.update_or_create(request, like, as_dict=True, current_user=current_user)
    return object

