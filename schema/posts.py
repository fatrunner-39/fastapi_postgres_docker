from datetime import datetime
from typing import Optional

from .base import BaseSchema


class Post(BaseSchema):
    title: str
    text: str
    creator_id: int | None = None

    class Config:
        schema_extra = {"example": {"title": "Example title", "text": "Example textt"}}


class PostUpdate(BaseSchema):
    title: Optional[str]
    text: Optional[str]

    class Config:
        schema_extra = {"example": {"title": "Updated example", "text": "Updated text"}}


class NewPost(BaseSchema):
    id: int
    title: Optional[str]
    text: Optional[str]
    creator_id: Optional[int]
    published: Optional[datetime]
    like: int
    dislike: int
