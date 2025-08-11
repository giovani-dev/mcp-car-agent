import pytest_asyncio
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from tests.mocks.models import MockModel
from tests.mocks.schemas import MockSchema

# =========================================================================
# Database Configuration for Integration Tests
# =========================================================================
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine = create_async_engine(TEST_DATABASE_URL, echo=True)
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


# =========================================================================
# Repository Fixture
# =========================================================================
@pytest_asyncio.fixture(name="repository")
async def repository_fixture(session: AsyncSession):
    """
    Provides an instance of BaseRepository configured with the test session and mock models.
    """
    return BaseRepository(session=session, model=MockModel, schema=MockSchema)
