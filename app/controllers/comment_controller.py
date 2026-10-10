from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.comment_model import Comment
from app.models.post_model import Post
from app.models.user_model import User
from app.schemas.comment_schema import CommentCreate


def create_comment(db: Session, user: User, post_id: int, comment_data: CommentCreate):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    comment = Comment(text=comment_data.text, user_id=user.id, post_id=post_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def get_comments(db: Session, post_id: int):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return (
        db.query(Comment)
        .filter(Comment.post_id == post_id)
        .order_by(Comment.created_at.desc())
        .all()
    )


def delete_comment(db: Session, user: User, comment_id: int):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    if comment.user_id != user.id:
        raise HTTPException(
            status_code=403, detail="Not allowed to delete this comment"
        )

    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted"}