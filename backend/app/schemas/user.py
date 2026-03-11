# backend/app/schemas/user.py
"""
Pydantic schemas for User API endpoints.
- UserCreate: What the client sends to register
- UserLogin: What the client sends to login
- UserResponse: What the API returns (no password!)
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: str
    full_name: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Allows converting SQLAlchemy model to Pydantic


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse