from pydantic import BaseModel, Field


class Manufacturer(BaseModel):
    name: str = Field(max_length=150, min_length=1)
