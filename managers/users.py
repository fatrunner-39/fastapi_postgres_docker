from . import BaseManager
from models import User
from db import async_session
from sqlalchemy import select
from helpers import get_password_hash, verify_password
from fastapi import HTTPException
from typing import Optional
from helpers import signJWT


class UserManager(BaseManager):
    async def get_user_by_username(self, user):
        async with async_session() as session:
            async with session.begin():
                user = await session.execute(select(User).where(User.username == user.username))
                return user.scalar()

    async def create(self, user, as_dict: Optional = False):
        async with async_session() as session:
            async with session.begin():
                exist_user = await self.get_user_by_username(user)
                if exist_user:
                    raise HTTPException(
                        status_code=400,
                        detail={"error": f'User with username = {user.username} already exists!'})
                # hash password
                user.password = get_password_hash(user.password)
                new_user = await super().create(user, as_dict)

                return new_user

    async def check_user(self, user):
        async with async_session() as session:
            async with session.begin():
                current_user = await self.get_user_by_username(user)
                if hasattr(current_user, "password"):
                    current_password = verify_password(getattr(user, "password"), current_user.password)
                else:
                    current_password = False

                if not (current_user and current_password):
                    raise HTTPException(
                        status_code=403,
                        detail={"error": f'Invalid user credentials'})
                else:
                    return signJWT(current_user.id)


user_manager = UserManager(User)
