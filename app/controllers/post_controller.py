from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.post_model import Post
from app.models.user_model import User
from app.schemas.post_schema import PostCreate


def create_post(db: Session, user: User, post_data: PostCreate):
    post = Post(content=post_data.content, user_id=user.id)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


def get_all_posts(db: Session):
    return db.query(Post).order_by(Post.created_at.desc()).all()


def get_post(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


def delete_post(db: Session, user: User, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    if post.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not allowed to delete this post")

    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}