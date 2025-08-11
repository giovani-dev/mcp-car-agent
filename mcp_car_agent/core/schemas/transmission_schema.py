from typing import Optional

from pydantic import BaseModel, Field


class Transmission(BaseModel):
    gearbox_type: str = Field(max_length=20, min_length=1)
    gears_qtde: Optional[int] = Field(default=None)
    traction: Optional[str] = Field(max_length=45, default=None)
