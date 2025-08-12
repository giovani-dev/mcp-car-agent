from datetime import date
from typing import List, Optional

from pydantic import BaseModel, Field

from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.equipment_schema import Equipment
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission


class CarSpecs(BaseModel):
    id: Optional[int] = None
    gas: Optional[str] = Field(max_length=50)
    config: Optional[str] = Field(max_length=45)
    doors: Optional[int] = None
    spaces: Optional[int] = None
    car: Optional["Car"] = None


class Car(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = Field(default=None, max_length=80)
    version: Optional[str] = Field(default=None, max_length=80)
    year: Optional[date] = Field(default=None)
    engine: Optional[Engine] = None
    transmission: Optional[Transmission] = None
    manufacturer: Optional[Manufacturer] = None
    equipments: Optional[List[Equipment]] = None
    car_specs: Optional[List[CarSpecs]] = None
