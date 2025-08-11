from unittest.mock import AsyncMock

import pytest

from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from tests.mocks.models import MockModel
from tests.mocks.schemas import MockSchema


@pytest.fixture
def mock_session():
    """Cria uma sessão de mock assíncrona."""
    return AsyncMock()


@pytest.fixture
def repository(mock_session):
    """Cria uma instância do BaseRepository com mocks."""
    return BaseRepository(mock_session, model=MockModel, schema=MockSchema)
