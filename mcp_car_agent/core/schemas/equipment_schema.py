from typing import Optional

from pydantic import BaseModel, Field


class Equipment(BaseModel):
    id: Optional[int] = None
    category: str = Field(max_length=50, min_length=1)
    description: str = Field(max_length=150, min_length=1)
    is_standard: bool = Field(default=False)
    is_optional: bool = Field(default=False)
    car_id: Optional[int] = None
