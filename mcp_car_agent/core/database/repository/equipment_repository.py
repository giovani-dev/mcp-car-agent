from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import EquipmentModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.equipment_schema import Equipment


class EquipmentRepository(BaseRepository[Equipment, EquipmentModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=EquipmentModel, schema=Equipment)

    async def input(self, data: Equipment) -> EquipmentModel:
        return EquipmentModel(
            category=data.category,
            description=data.description,
            is_standard=data.is_standard,
            is_optional=data.is_optional,
            car_id=data.car_id,
        )
