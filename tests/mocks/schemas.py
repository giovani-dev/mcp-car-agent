from typing import Optional

from pydantic import BaseModel


class MockSchema(BaseModel):
    id: Optional[int] = None
    name: str
    is_active: bool = False
