from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import ManufacturerModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer


class ManufacturerRepository(BaseRepository[Manufacturer, ManufacturerModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=ManufacturerModel, schema=Manufacturer)
