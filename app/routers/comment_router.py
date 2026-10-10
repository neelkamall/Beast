from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.comment_controller import (
    create_comment,
    get_comments,
    delete_comment,
)
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user_model import User
from app.schemas.comment_schema import CommentCreate, CommentResponse

router = APIRouter(tags=["Comments"])


@router.post(
    "/posts/{post_id}/comments", response_model=CommentResponse, status_code=201
)
def add_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_comment(db, current_user, post_id, comment_data)


@router.get("/posts/{post_id}/comments", response_model=List[CommentResponse])
def list_comments(post_id: int, db: Session = Depends(get_db)):
    return get_comments(db, post_id)


@router.delete("/comments/{comment_id}")
def remove_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_comment(db, current_user, comment_id)