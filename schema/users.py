from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "username": "user@example.com",
                "password": "password"
            }
        }
