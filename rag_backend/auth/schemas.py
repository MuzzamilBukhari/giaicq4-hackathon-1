from pydantic import BaseModel, EmailStr, validator
from typing import Optional
from datetime import datetime
import uuid


class UserBase(BaseModel):
    email: EmailStr
    hardware_exp: Optional[str] = None
    software_exp: Optional[str] = None
    robotics_level: str  # Must be one of: beginner, intermediate, advanced
    goals: Optional[str] = None

    @validator('robotics_level')
    def validate_robotics_level(cls, v):
        if v not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('robotics_level must be one of: beginner, intermediate, advanced')
        return v


class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserUpdate(BaseModel):
    hardware_exp: Optional[str] = None
    software_exp: Optional[str] = None
    robotics_level: Optional[str] = None
    goals: Optional[str] = None

    @validator('robotics_level', pre=True)
    def validate_robotics_level(cls, v):
        if v and v not in ['beginner', 'intermediate', 'advanced']:
            raise ValueError('robotics_level must be one of: beginner, intermediate, advanced')
        return v


class UserResponse(BaseModel):
    id: uuid.UUID
    email: EmailStr
    hardware_exp: Optional[str] = None
    software_exp: Optional[str] = None
    robotics_level: str
    goals: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    token: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user_id: uuid.UUID
    email: EmailStr
    token: str


class SessionResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    token: str
    expires_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True