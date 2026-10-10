from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.likes_controller import toggle_like, get_likes_count
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user_model import User
from app.schemas.likes_schema import LikeResponse, LikeCountResponse

router = APIRouter(tags=["Likes"])


@router.post("/posts/{post_id}/like", response_model=LikeResponse)
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return toggle_like(db, current_user, post_id)


@router.get("/posts/{post_id}/likes", response_model=LikeCountResponse)
def likes_count(post_id: int, db: Session = Depends(get_db)):
    return get_likes_count(db, post_id)