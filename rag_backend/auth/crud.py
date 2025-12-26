from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from .models import User, AuthSession
from .schemas import UserCreate, UserUpdate
from .security import get_password_hash, verify_password
from typing import Optional
import uuid
from datetime import datetime, timedelta


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by their email address."""
    stmt = select(User).where(User.email == email)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def get_user_by_id(db: Session, user_id: uuid.UUID) -> Optional[User]:
    """Get a user by their ID."""
    stmt = select(User).where(User.id == user_id)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user in the database."""
    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create the user object
    db_user = User(
        email=user.email,
        password_hash=hashed_password,
        hardware_exp=user.hardware_exp,
        software_exp=user.software_exp,
        robotics_level=user.robotics_level,
        goals=user.goals
    )

    # Add to database
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        db.rollback()
        raise ValueError("Email already registered")


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def update_user_profile(db: Session, user_id: uuid.UUID, user_update: UserUpdate) -> Optional[User]:
    """Update a user's profile information."""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    # Update fields if provided
    if user_update.hardware_exp is not None:
        user.hardware_exp = user_update.hardware_exp
    if user_update.software_exp is not None:
        user.software_exp = user_update.software_exp
    if user_update.robotics_level is not None:
        user.robotics_level = user_update.robotics_level
    if user_update.goals is not None:
        user.goals = user_update.goals

    db.commit()
    db.refresh(user)
    return user


def create_auth_session(db: Session, user_id: uuid.UUID, token: str, expires_at: datetime) -> AuthSession:
    """Create a new authentication session."""
    db_session = AuthSession(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session


def get_session_by_token(db: Session, token: str) -> Optional[AuthSession]:
    """Get an authentication session by token."""
    stmt = select(AuthSession).where(AuthSession.token == token)
    result = db.execute(stmt)
    session = result.scalar_one_or_none()

    # Check if session is expired
    if session and session.expires_at < datetime.utcnow():
        # Delete expired session
        db.delete(session)
        db.commit()
        return None

    return session


def delete_session_by_token(db: Session, token: str) -> bool:
    """Delete an authentication session by token."""
    stmt = select(AuthSession).where(AuthSession.token == token)
    result = db.execute(stmt)
    session = result.scalar_one_or_none()

    if session:
        db.delete(session)
        db.commit()
        return True
    return False


def cleanup_expired_sessions(db: Session) -> int:
    """Remove all expired sessions from the database."""
    from sqlalchemy import and_

    current_time = datetime.utcnow()
    stmt = select(AuthSession).where(AuthSession.expires_at < current_time)
    result = db.execute(stmt)
    expired_sessions = result.scalars().all()

    count = 0
    for session in expired_sessions:
        db.delete(session)
        count += 1

    if count > 0:
        db.commit()

    return count