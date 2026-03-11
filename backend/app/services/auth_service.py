# backend/app/services/auth_service.py
"""
Authentication business logic.
"""

from datetime import datetime, timedelta
from typing import Optional
from passlib.context import CryptContext
import jwt
import hashlib
from sqlalchemy.orm import Session
from app.config import settings
from app.models.user import User

# Bcrypt context for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prepare_password(password: str) -> str:
    """
    Prepare password for bcrypt.
    Bcrypt has a 72-byte limit, so we pre-hash long passwords with SHA-256.
    This is a common and secure pattern used by many applications.
    """
    if len(password.encode('utf-8')) > 72:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    return password


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt."""
    prepared = _prepare_password(password)
    return pwd_context.hash(prepared)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a plain password matches the hashed version."""
    prepared = _prepare_password(plain_password)
    return pwd_context.verify(prepared, hashed_password)


def create_access_token(user_id: int, email: str) -> str:
    """Create a JWT token."""
    expire = datetime.utcnow() + timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
    payload = {
        "sub": str(user_id),
        "email": email,
        "exp": expire
    }
    token = jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT token."""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Find a user by their email address."""
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Find a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, email: str, full_name: str, password: str) -> User:
    """Create a new user account."""
    hashed = hash_password(password)
    user = User(
        email=email,
        full_name=full_name,
        hashed_password=hashed
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user