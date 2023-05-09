from pydantic import EmailStr

from .base import BaseSchema


class User(BaseSchema):
    username: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {"username": "user@example.com", "password": "password"}
        }


class NewUser(BaseSchema):
    id: int
    username: str
