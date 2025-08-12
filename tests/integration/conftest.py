import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import CarModel, CarSpecsModel
from mcp_car_agent.core.database.repository.car_repository import (
    CarRepository,
    CarSpecsRepository,
)

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
