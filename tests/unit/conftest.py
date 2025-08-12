from unittest.mock import AsyncMock

import pytest

from mcp_car_agent.core.database.repository.car_repository import (
    CarRepository,
    CarSpecsRepository,
)
from mcp_car_agent.core.database.repository.engine_repository import (
    EngineRepository,
    EngineSpecRepository,
)


@pytest.fixture(name="mock_session")
def setup_mock_session():
    """Cria uma sessão de mock assíncrona."""
    return AsyncMock()


@pytest.fixture
def car_repository(mock_session):
    """Cria uma instância de CarRepository com mocks."""
    return CarRepository(session=mock_session)


@pytest.fixture
def car_spec_repository(mock_session):
    """Cria uma instância de CarSpecsRepository com mocks."""
    return CarSpecsRepository(session=mock_session)


@pytest.fixture
def engine_repository(mock_session):
    """Cria uma instância de EngineRepository com mocks."""
    return EngineRepository(session=mock_session)


@pytest.fixture
def engine_spec_repository(mock_session):
    """Cria uma instância de EngineSpecRepository com mocks."""
    return EngineSpecRepository(session=mock_session)


@pytest.fixture
def mock_config(monkeypatch):
    """Mocks as variáveis de ambiente de configuração."""
    monkeypatch.setattr("mcp_car_agent.core.config.DB_USER", "user")
    monkeypatch.setattr("mcp_car_agent.core.config.DB_PWD", "pwd")
    monkeypatch.setattr("mcp_car_agent.core.config.DB_HOST", "host")
    monkeypatch.setattr("mcp_car_agent.core.config.DB_PORT", "port")
    monkeypatch.setattr("mcp_car_agent.core.config.DB_NAME", "db")
