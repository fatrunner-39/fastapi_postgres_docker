from pydantic import BaseModel
from typing import Optional


class Like(BaseModel):
    post_id: int
