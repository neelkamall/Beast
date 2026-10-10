from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.post_controller import (
    create_post,
    get_all_posts,
    get_post,
    delete_post,
)
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user_model import User
from app.schemas.post_schema import PostCreate, PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=PostResponse, status_code=201)
def create(
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_post(db, current_user, post_data)


@router.get("", response_model=List[PostResponse])
def list_posts(db: Session = Depends(get_db)):
    return get_all_posts(db)


@router.get("/{post_id}", response_model=PostResponse)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return get_post(db, post_id)


@router.delete("/{post_id}")
def remove_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return delete_post(db, current_user, post_id)