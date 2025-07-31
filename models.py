from sqlmodel import SQLModel, Field
from pydantic import EmailStr, validator
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    """Base user model with common fields"""
    email: EmailStr = Field(unique=True, index=True, description="User's email address")
    username: str = Field(
        min_length=3,
        max_length=50,
        unique=True,
        index=True,
        description="Unique username"
    )

    @validator('username')
    def validate_username(cls, v):
        """Validate username format"""
        if not v.replace('_', '').replace('-', '').isalnum():
            raise ValueError('Username can only contain letters, numbers, hyphens, and underscores')
        return v.lower()


class User(UserBase, table=True):
    """User table model"""
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True, description="User ID")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserResponse(UserBase):
    """Schema for user response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True