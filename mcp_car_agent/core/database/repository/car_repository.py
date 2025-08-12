from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import CarModel, CarSpecsModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.car_schema import Car, CarSpecs


class CarRepository(BaseRepository[Car, CarModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=CarModel, schema=Car)

    async def input(self, data: Car) -> CarModel:
        return CarModel(
            name=data.name,
            version=data.version,
            year=data.year,
            engine_id=data.engine.id,
            transmission_id=data.transmission.id,
            manufacturer_id=data.manufacturer.id,
        )


class CarSpecsRepository(BaseRepository[CarSpecs, CarSpecsModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=CarSpecsModel, schema=CarSpecs)

    async def input(self, data: CarSpecs) -> CarSpecsModel:
        return CarSpecsModel(
            gas=data.gas,
            config=data.config,
            doors=data.doors,
            spaces=data.spaces,
            car_id=data.car.id,
        )
