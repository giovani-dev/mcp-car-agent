import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import (
    CarModel,
    CarSpecsModel,
    EngineModel,
    ManufacturerModel,
    TransmissionModel,
)
from mcp_car_agent.core.database.repository.car_repository import (
    CarRepository,
    CarSpecsRepository,
)
from mcp_car_agent.core.database.repository.engine_repository import (
    EngineRepository,
    EngineSpecRepository,
)
from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture(name="session")
async def session_fixture():
    """
    Provides a database session for each individual test.
    This ensures that each test runs in an isolated transaction.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    async with AsyncSessionLocal() as session:
        yield session
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest_asyncio.fixture
async def setup_dependencies(session: AsyncSession):
    """Cria e retorna dependências para os testes de CarRepository e EngineRepository."""
    engine_data = Engine(compression_rate="10:1", total_cc=2000, aspiration="Turbo")
    transmission_data = Transmission(gearbox_type="Manual")
    manufacturer_data = Manufacturer(name="Honda")

    engine_model = EngineModel.model_validate(engine_data.model_dump())
    transmission_model = TransmissionModel.model_validate(
        transmission_data.model_dump()
    )
    manufacturer_model = ManufacturerModel.model_validate(
        manufacturer_data.model_dump()
    )

    session.add(engine_model)
    session.add(transmission_model)
    session.add(manufacturer_model)
    await session.commit()
    await session.refresh(engine_model)
    await session.refresh(transmission_model)
    await session.refresh(manufacturer_model)

    return {
        "engine_id": engine_model.id,
        "transmission_id": transmission_model.id,
        "manufacturer_id": manufacturer_model.id,
    }


@pytest_asyncio.fixture
async def car_with_specs(session: AsyncSession, setup_dependencies):
    """Cria um carro com specs para os testes."""
    carro_com_specs = CarModel(
        name="Carro com Specs",
        engine_id=setup_dependencies["engine_id"],
        transmission_id=setup_dependencies["transmission_id"],
        manufacturer_id=setup_dependencies["manufacturer_id"],
    )
    session.add(carro_com_specs)
    await session.commit()
    await session.refresh(carro_com_specs)

    car_specs = CarSpecsModel(
        car_id=carro_com_specs.id, gas="Gasolina", doors=4, spaces=5
    )
    session.add(car_specs)
    await session.commit()
    await session.refresh(car_specs)

    return {"carro": carro_com_specs, "specs": car_specs}


@pytest.fixture
def car_repository(session: AsyncSession):
    """Fornece uma instância de CarRepository para os testes."""
    return CarRepository(session=session)


@pytest.fixture
def car_spec_repository(session: AsyncSession):
    """Fornece uma instância de CarSpecRepository para os testes."""
    return CarSpecsRepository(session)


@pytest.fixture
def engine_repository(session: AsyncSession):
    """Fornece uma instância de EngineRepository para os testes."""
    return EngineRepository(session=session)


@pytest.fixture
def engine_spec_repository(session: AsyncSession):
    """Fornece uma instância de EngineSpecRepository para os testes."""
    return EngineSpecRepository(session=session)
