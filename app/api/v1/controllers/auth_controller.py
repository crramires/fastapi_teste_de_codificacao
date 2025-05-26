from core.security import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    get_current_user,
    get_password_hash,
)
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.models.user_model import User
from app.schemas.auth_schema import TokenResponse, UserRegisterRequest

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegisterRequest, db: Session = Depends(get_db)):
    user_exists = (
        db.query(User)
        .filter(
            (User.username == user_data.username)
            | (User.email == user_data.email)
        )
        .first()
    )

    if user_exists:
        raise HTTPException(
            status_code=400, detail="Username or email already registered"
        )

    hashed_password = get_password_hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials",
        )

    access_token = create_access_token(data={"sub": user.username})
    refresh_token = create_refresh_token(data={"sub": user.username})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token
    )


@router.post("/refresh-token", response_model=TokenResponse)
def refresh_token(
    current_user: User = Depends(get_current_user),
):
    access_token = create_access_token(data={"sub": current_user.username})
    refresh_token = create_refresh_token(data={"sub": current_user.username})

    return TokenResponse(
        access_token=access_token, refresh_token=refresh_token
    )
