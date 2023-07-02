from typing import Union

from fastapi import HTTPException, Request
from sqlalchemy import and_
from sqlalchemy.orm.session import Session

from models import Like

from . import BaseManager
from .posts import post_manager


class LikeManager(BaseManager):
    def get_like_exist(
        self, user_id: int, post_id: int, session: Session
    ) -> Union[Like, None]:
        instance: Like | None = (
            session.query(self.model)
            .where(and_(self.model.user_id == user_id, self.model.post_id == post_id))
            .scalar()
        )
        return instance

    def get_choice(self, request):
        choice = str(request.url)
        choice = choice.split("/")
        if choice[-2] != "like":
            return False
        return True

    def update_or_create(
        self, like, request: Request, session: Session, **kwargs
    ) -> Like:
        current_user = kwargs.get("current_user")
        like_exist = self.get_like_exist(current_user, like.post_id, session)

        choice = self.get_choice(request)

        post = post_manager.get_by_id(like.post_id, session)

        # prevent to like self posts
        if current_user == post.creator_id:
            raise HTTPException(status_code=403, detail={"failed": "Forbidden"})

        if not like_exist:
            like.user_id = current_user
            like.is_like = choice

            return super().create(like, session)
        else:
            if like_exist.is_like == choice:
                super().delete(like_exist.id, session)
            else:
                return super().update({"is_like": choice}, like_exist.id, session)


like_manager = LikeManager(Like)
