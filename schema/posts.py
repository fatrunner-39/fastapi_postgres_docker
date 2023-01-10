from pydantic import BaseModel
from typing import Optional


class Post(BaseModel):
    title: str
    text: str

    class Config:
        schema_extra = {
            "example": {
                "title": "Example title",
                "text": "Example textt"
            }
        }


class PostUpdate(BaseModel):
    title: Optional[str]
    text: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "title": "Updated example",
                "text": "Updated text"
            }
        }
    