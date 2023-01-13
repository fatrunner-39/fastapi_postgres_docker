from datetime import datetime

import schema
from fastapi import APIRouter, Depends

from helpers import JWTBearer, get_dict_from_token, AuthJWT
from managers import user_manager

router = APIRouter()


@router.post("/sign_up")
async def create_account(user: schema.User):
    new_user = await user_manager.create(user, as_dict=True)
    return new_user


@router.post("/login/")
async def login(user: schema.User):
    return await user_manager.check_user(user)


@router.get("/", dependencies=[Depends(JWTBearer())])
async def get_all_users(Authorize:AuthJWT = Depends()):
    start = datetime.now()
    get_dict_from_token(Authorize)
    users = await user_manager.get_all(as_dict=True)
    print('#########', datetime.now())
    print('#########', datetime.now() - start)
    return users
