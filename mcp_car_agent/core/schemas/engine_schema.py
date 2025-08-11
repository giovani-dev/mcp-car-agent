from typing import Literal, Optional

from pydantic import BaseModel, Field

# TODO: Trabalhar com validações


class EngineSpec(BaseModel):
    gas_type: Optional[Literal["gasolina", "alcool", "gasolina/alcool"]] = Field(
        max_length=45, min_length=1
    )
    max_hp: Optional[int] = Field(gt=0, default=None)
    max_hp_rpm: Optional[int] = Field(gt=0, default=None)
    max_torque: Optional[int] = Field(gt=0, default=None)
    max_torque_rpm: Optional[int] = Field(gt=0, default=None)
    torque_unit_measure: Optional[Literal["kgfm"]] = Field(
        max_length=10, default="kgfm"
    )


class Engine(BaseModel):
    compression_rate: Optional[str] = Field(max_length=10, default=None)
    total_cc: Optional[int] = Field(default=None)
    aspiration: Optional[str] = Field(max_length=45, default=None)
    engine_specs: Optional[EngineSpec] = Field(default=None)
