from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.likes_model import Like
from app.models.post_model import Post
from app.models.user_model import User


def toggle_like(db: Session, user: User, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    existing = (
        db.query(Like)
        .filter(Like.user_id == user.id, Like.post_id == post_id)
        .first()
    )

    if existing:
        db.delete(existing)
        liked = False
    else:
        db.add(Like(user_id=user.id, post_id=post_id))
        liked = True

    db.commit()

    likes_count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"liked": liked, "likes_count": likes_count}


def get_likes_count(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    likes_count = db.query(Like).filter(Like.post_id == post_id).count()
    return {"likes_count": likes_count}