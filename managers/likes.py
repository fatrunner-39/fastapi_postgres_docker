from typing import Optional
from fastapi import HTTPException

from db import async_session
from . import BaseManager
from models import Like
from sqlalchemy import select, and_
from . import post_manager


class LikeManager(BaseManager):
    async def get_like_exist(self, user_id, post_id):
        async with async_session() as session:
            async with session.begin():
                instance = await session.execute(select(self.model).where(and_(self.model.user_id == user_id,
                                                                               self.model.post_id == post_id)))
                return instance.scalar()

    def get_choice(self, request):
        choice = str(request.url)
        choice = choice.split('/')
        if choice[-2] == 'like':
            return True
        else:
            return False

    async def update_or_create(self, request, like, as_dict: Optional[bool] = False, **kwargs):
        current_user = kwargs.get('current_user')
        like_exist = await self.get_like_exist(current_user, like.post_id)

        choice = self.get_choice(request)

        if not like_exist:
            data = {
                'user_id': current_user,
                'post_id': like.post_id,
                'is_like': choice
            }
            return await super().create(data, as_dict=True)
        else:

            post = await post_manager.get_by_id(like_exist.post_id)

            # prevent to like self posts
            if current_user == post.creator_id:
                raise HTTPException(
                    status_code=403,
                    detail={"failed": 'Forbidden'})

            if like_exist.is_like == choice:
                await super().delete(like_exist.id)
            else:
                return await super().update({'is_like': choice}, like_exist.id, as_dict)


like_manager = LikeManager(Like)
