from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    id: int
    content: str
    user_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)