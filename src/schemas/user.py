from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    email: EmailStr
    age: Optional[int] = Field(default=None, ge=0, le=150)


class User(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
