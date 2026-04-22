from typing import Optional

from pydantic import BaseModel, Field


class PerformanceIn(BaseModel):
    musician_id: int
    concert_id: int
    instrument_id: Optional[int] = None
    fee: Optional[float] = Field(default=None, ge=0)
