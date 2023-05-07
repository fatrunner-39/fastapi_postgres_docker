from fastapi import APIRouter, Depends

from schema import User, NewUser
from helpers import AuthJWT, JWTBearer, get_dict_from_token
from managers import user_manager
from db import get_db_session

router = APIRouter()


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
def get_all_users(Authorize:AuthJWT = Depends()):
    print(get_dict_from_token(Authorize))
    with get_db_session() as session:
        users = user_manager.get_all(session)
        # TODO: сделать уничерсальный метод для отображения get_all
        users = list(map(NewUser.from_orm, users))
        return users
