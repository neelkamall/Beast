from fastapi import FastAPI

from app.core.database import Base, engine
from app.models.user_model import User  # noqa: F401
from app.models.post_model import Post  # noqa: F401
from app.models.comment_model import Comment  # noqa: F401
from app.models.likes_model import Like  # noqa: F401
from app.routers.user_router import router as user_router
from app.routers.post_router import router as post_router
from app.routers.comment_router import router as comment_router
from app.routers.likes_router import router as like_router
from app.routers.ai_router import router as ai_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Beast")

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(like_router)
app.include_router(ai_router)


@app.get("/")
def root():
    return {"message": "Beast is running"}