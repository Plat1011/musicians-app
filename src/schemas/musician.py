from typing import Optional

from pydantic import BaseModel, Field


class MusicianIn(BaseModel):
    name: str = Field(min_length=1, max_length=128)
    country: Optional[str] = Field(default=None, max_length=64)
    birth_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    bio: Optional[str] = None
