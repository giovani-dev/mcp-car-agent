from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission


class CarSpecs(BaseModel):
    gas: Optional[str] = Field(max_length=50)
    config: Optional[str] = Field(max_length=45)
    doors: Optional[int] = Field(default=None)
    spaces: Optional[int] = Field(default=None)


class Car(BaseModel):
    name: Optional[str] = Field(max_length=80)
    version: Optional[str] = Field(max_length=80)
    year: Optional[date] = Field(default=None)
    engine: Engine
    transmission: Transmission
    manufacturer: Manufacturer
    equipments: List
    car_specs: List[CarSpecs]
