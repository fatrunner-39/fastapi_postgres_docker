from typing import Optional

from pydantic import BaseModel


class Like(BaseModel):
    post_id: int
