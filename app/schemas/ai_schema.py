from pydantic import BaseModel, Field


class GeneratePostRequest(BaseModel):
    idea: str = Field(min_length=3, max_length=300)


class GeneratePostResponse(BaseModel):
    content: str


class CommentSummaryResponse(BaseModel):
    post_id: int
    comments_count: int
    summary: str