from db import async_session
from . import BaseManager
from models import Post, Like
from typing import Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy import select


class PostManager(BaseManager):
    async def create(self,
                     post,
                     as_dict: Optional[bool] = False,
                     *args,
                     **kwargs):
        creator_id = kwargs.get('creator_id')
        post = post.dict()
        post.update(
            {
                'creator_id': creator_id,
                'published': datetime.now()
            }
        )
        new_post = await super().create(post)

        return new_post.as_dict_extra()

    async def update(self,
                     post,
                     id,
                     as_dict: Optional[bool] = False,
                     *args,
                     **kwargs):
        current_user = kwargs.get('current_user')
        post_for_update = await self.get_by_id(id)
        if current_user != post_for_update.creator_id:
            raise HTTPException(
                        status_code=403,
                        detail={"error": f'You can edit only your posts'})
        post = post.dict()

        if not post.get('title'):
            post['title'] = post_for_update.title
        if not post.get('text'):
            post['text'] = post_for_update.text
        updated_post = await super().update(post, id, as_dict=True)
        return updated_post

    async def delete(self, id, **kwargs):
        current_user = kwargs.get('current_user')
        post_for_delete = await self.get_by_id(id)
        if current_user != post_for_delete.creator_id:
            raise HTTPException(
                status_code=403,
                detail={"error": f'You can delete only your posts'})
        await super().delete(id)


post_manager = PostManager(Post)
