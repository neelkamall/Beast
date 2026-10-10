from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    user_id: int
    post_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)