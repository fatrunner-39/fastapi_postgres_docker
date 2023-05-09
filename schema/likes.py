from .base import BaseSchema


class Like(BaseSchema):
    user_id: int | None = None
    post_id: int
    is_like: bool | None = None


class NewLike(BaseSchema):
    id: int
    user_id: int
    post_id: int
    is_like: bool
