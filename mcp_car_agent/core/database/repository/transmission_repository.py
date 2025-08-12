from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import TransmissionModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.transmission_schema import Transmission


class TransmissionRepository(BaseRepository[Transmission, TransmissionModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=TransmissionModel, schema=Transmission)
