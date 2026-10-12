from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.ai_controller import generate_post, summarize_comments
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user_model import User
from app.schemas.ai_schema import (
    GeneratePostRequest,
    GeneratePostResponse,
    CommentSummaryResponse,
)

router = APIRouter(tags=["AI"])


@router.post("/ai/generate-post", response_model=GeneratePostResponse)
def generate_post_route(
    data: GeneratePostRequest,
    current_user: User = Depends(get_current_user),
):
    return generate_post(data.idea)


@router.get("/posts/{post_id}/comments/summary", response_model=CommentSummaryResponse)
def comments_summary(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return summarize_comments(db, post_id)