from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    text: str


class PostUpdate(BaseModel):
    title: Optional[str]
    text: Optional[str]
    