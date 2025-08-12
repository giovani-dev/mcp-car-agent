from typing import Optional
from pydantic import BaseModel, Field


class Manufacturer(BaseModel):
    id: Optional[int] = None
    name: str = Field(max_length=150, min_length=1)
