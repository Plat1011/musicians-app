from typing import Optional

from pydantic import BaseModel, Field


class InstrumentIn(BaseModel):
    name: str = Field(min_length=1, max_length=64)
    kind: Optional[str] = Field(default=None, max_length=32)
