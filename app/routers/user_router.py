from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.controllers.user_controller import (
    register_user,
    login_user,
    logout_user,
    refresh_access_token,
    change_password,
)
from app.core.database import get_db
from app.middleware.auth import get_current_user
from app.models.user_model import User
from app.schemas.user_schema import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
    AccessTokenResponse,
    RefreshRequest,
    ChangePassword,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    return register_user(db, user_data)


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    return login_user(db, user_data.email, user_data.password)


@router.post("/logout")
def logout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return logout_user(db, current_user)


@router.post("/refresh", response_model=AccessTokenResponse)
def refresh(data: RefreshRequest, db: Session = Depends(get_db)):
    return refresh_access_token(db, data.refresh_token)


@router.post("/change-password")
def change_user_password(
    data: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return change_password(db, current_user, data.old_password, data.new_password)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user