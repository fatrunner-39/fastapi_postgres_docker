from fastapi import HTTPException, Query
from sqlalchemy.orm.session import Session

from models import Post

from . import BaseManager


class PostManager(BaseManager):
    def create(self, post, session: Session, *args, **kwargs) -> Post:
        creator_id = kwargs.get("creator_id")
        post.creator_id = creator_id
        new_post: Post = super().create(post, session, *args, **kwargs)
        return new_post

    def update(self, post, id, session: Session, *args, **kwargs) -> Post:
        current_user = kwargs.get("current_user")
        post_for_update = self.get_by_id(id, session)
        if current_user != post_for_update.creator_id:
            raise HTTPException(
                status_code=403, detail={"error": f"You can edit only your posts"}
            )
        updated_post = super().update(post, id, session)
        return updated_post

    def delete(self, id, session: Session, **kwargs):
        current_user = kwargs.get("current_user")
        post_for_delete = self.get_by_id(id, session)
        if current_user != post_for_delete.creator_id:
            raise HTTPException(
                status_code=403, detail={"error": f"You can delete only your posts"}
            )
        super().delete(id, session)

    def filter_by_text(self, instances: Query, text: str):
        return instances.filter(Post.title.ilike(f"%{text}%"))


post_manager = PostManager(Post)
