from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from db.connection import get_db
from .schemas import UserCreate, UserUpdate, LoginRequest, TokenResponse, UserResponse
from .crud import (
    create_user, authenticate_user, get_user_by_id,
    update_user_profile, create_auth_session
)
from .security import create_access_token, verify_password
from .middleware import JWTBearer
import uuid

router = APIRouter(tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    try:
        # Create the user
        db_user = create_user(db, user)

        # Create access token
        access_token_expires = timedelta(minutes=1440)  # 24 hours
        token_data = {
            "user_id": str(db_user.id),
            "email": db_user.email
        }
        token = create_access_token(data=token_data, expires_delta=access_token_expires)

        # Create auth session
        expires_at = db_user.created_at + timedelta(minutes=1440)  # 24 hours
        create_auth_session(db, db_user.id, token, expires_at)

        return TokenResponse(
            user_id=db_user.id,
            email=db_user.email,
            token=token
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login", response_model=TokenResponse)
async def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return an access token."""
    user = authenticate_user(db, login_request.email, login_request.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=1440)  # 24 hours
    token_data = {
        "user_id": str(user.id),
        "email": user.email
    }
    token = create_access_token(data=token_data, expires_delta=access_token_expires)

    # Create auth session
    from datetime import datetime
    expires_at = datetime.utcnow() + timedelta(minutes=1440)  # 24 hours
    create_auth_session(db, user.id, token, expires_at)

    return TokenResponse(
        user_id=user.id,
        email=user.email,
        token=token
    )


@router.get("/profile", response_model=UserResponse)
async def get_profile(token: str = Depends(JWTBearer()), db: Session = Depends(get_db)):
    """Get the current user's profile."""
    from rag_backend.auth.security import verify_token

    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = uuid.UUID(token_data.user_id)
    user = get_user_by_id(db, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user


@router.put("/profile", response_model=UserResponse)
async def update_profile(
    user_update: UserUpdate,
    token: str = Depends(JWTBearer()),
    db: Session = Depends(get_db)
):
    """Update the current user's profile."""
    from rag_backend.auth.security import verify_token
    from rag_backend.auth.crud import update_user_profile

    token_data = verify_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = uuid.UUID(token_data.user_id)
    updated_user = update_user_profile(db, user_id, user_update)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return updated_user