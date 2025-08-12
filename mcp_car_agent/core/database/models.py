from datetime import date
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


class EngineModel(SQLModel, table=True):
    """
    Representa a tabela `engine` no banco de dados.
    """

    __tablename__ = "engine"

    id: Optional[int] = Field(primary_key=True)
    compression_rate: Optional[str] = Field(max_length=10, default=None)
    total_cc: Optional[int] = Field(default=None)
    aspiration: Optional[str] = Field(max_length=45, default=None)

    engine_specs: List["EngineSpecModel"] = Relationship(back_populates="engine")
    cars: List["CarModel"] = Relationship(back_populates="engine")


class TransmissionModel(SQLModel, table=True):
    """
    Representa a tabela `transmission` no banco de dados.
    """

    __tablename__ = "transmission"

    id: Optional[int] = Field(default=None, primary_key=True)
    gearbox_type: str = Field(max_length=20, min_length=1)
    gears_qtde: Optional[int] = Field(default=None)
    traction: Optional[str] = Field(max_length=45, default=None)
    cars: List["CarModel"] = Relationship(back_populates="transmission")


class ManufacturerModel(SQLModel, table=True):
    """
    Representa a tabela `manufacturer` no banco de dados.
    """

    __tablename__ = "manufacturer"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=150, min_length=1)

    cars: List["CarModel"] = Relationship(back_populates="manufacturer")


class CarModel(SQLModel, table=True):
    """
    Representa a tabela `car` no banco de dados.
    """

    __tablename__ = "car"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(max_length=80)
    version: Optional[str] = Field(max_length=80)
    year: Optional[date] = Field(default=None)
    engine_id: int = Field(foreign_key="engine.id")
    transmission_id: int = Field(foreign_key="transmission.id")
    manufacturer_id: int = Field(foreign_key="manufacturer.id")

    engine: EngineModel = Relationship(back_populates="cars")
    transmission: TransmissionModel = Relationship(back_populates="cars")
    manufacturer: ManufacturerModel = Relationship(back_populates="cars")

    equipments: List["EquipmentModel"] = Relationship(back_populates="car")
    car_specs: List["CarSpecsModel"] = Relationship(back_populates="car")


class EquipmentModel(SQLModel, table=True):
    """
    Representa a tabela `equipment` no banco de dados.
    """

    __tablename__ = "equipment"

    id: Optional[int] = Field(default=None, primary_key=True)
    category: str = Field(max_length=50, min_length=1)
    description: str = Field(max_length=150, min_length=1)
    is_standard: bool = Field(default=False)
    is_optional: bool = Field(default=False)
    car_id: int = Field(foreign_key="car.id")

    car: CarModel = Relationship(back_populates="equipments")


class CarSpecsModel(SQLModel, table=True):
    """
    Representa a tabela `car_specs` no banco de dados.
    """

    __tablename__ = "car_specs"

    id: int = Field(default=None, primary_key=True)
    gas: Optional[str] = Field(max_length=50)
    config: Optional[str] = Field(max_length=45)
    doors: Optional[int] = Field(default=None)
    spaces: Optional[int] = Field(default=None)
    car_id: int = Field(foreign_key="car.id")

    car: CarModel = Relationship(back_populates="car_specs")


class EngineSpecModel(SQLModel, table=True):
    """
    Representa a tabela `engine_specs` no banco de dados.
    """

    __tablename__ = "engine_specs"

    id: Optional[int] = Field(primary_key=True)

    gas_type: Optional[str] = Field(max_length=45, min_length=1)
    max_hp: Optional[int] = Field(gt=0, default=None)
    max_hp_rpm: Optional[int] = Field(gt=0, default=None)
    max_torque: Optional[int] = Field(gt=0, default=None)
    max_torque_rpm: Optional[int] = Field(gt=0, default=None)
    torque_unit_measure: Optional[str] = Field(max_length=10, default="kgfm")
    engine_id: int = Field(foreign_key="engine.id")

    engine: EngineModel = Relationship(back_populates="engine_specs")
