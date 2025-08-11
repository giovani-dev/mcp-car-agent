from typing import Optional

from sqlmodel import Field, SQLModel


class MockModel(SQLModel, table=True):
    __tablename__ = "mock_table"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=50)
    is_active: bool = Field(default=False)
