from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import EngineModel, EngineSpecModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.engine_schema import Engine, EngineSpec


class EngineRepository(BaseRepository[Engine, EngineModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=EngineModel, schema=Engine)

    async def input(self, data: Engine) -> EngineModel:
        return EngineModel(
            compression_rate=data.compression_rate,
            total_cc=data.total_cc,
            aspiration=data.aspiration,
        )


class EngineSpecRepository(BaseRepository[EngineSpec, EngineSpecModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, model=EngineSpecModel, schema=EngineSpec)

    async def input(self, data: EngineSpec) -> EngineSpecModel:
        return EngineSpecModel(
            gas_type=data.gas_type,
            max_hp=data.max_hp,
            max_hp_rpm=data.max_hp_rpm,
            max_torque=data.max_torque,
            max_torque_rpm=data.max_torque_rpm,
            torque_unit_measure=data.torque_unit_measure,
            engine_id=data.engine.id,
        )
