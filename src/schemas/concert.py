from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class ConcertIn(BaseModel):
    title: str = Field(min_length=1, max_length=128)
    concert_date: date
    venue: Optional[str] = Field(default=None, max_length=128)
    city: Optional[str] = Field(default=None, max_length=64)
