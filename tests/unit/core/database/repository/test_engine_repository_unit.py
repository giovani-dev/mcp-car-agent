from unittest.mock import AsyncMock

import pytest

from mcp_car_agent.core.database.models import EngineModel, EngineSpecModel
from mcp_car_agent.core.database.repository.engine_repository import (
    EngineRepository,
    EngineSpecRepository,
)
from mcp_car_agent.core.schemas.engine_schema import Engine, EngineSpec


class TestEngineRepositories:
    """
    Testes unitários para as classes EngineRepository e EngineSpecRepository.
    """

    def test_quando_repositorios_sao_iniciados_entao_model_e_schema_sao_corretos(
        self, mock_session
    ):
        """
        Verifica se EngineRepository e EngineSpecRepository são inicializados com o modelo e schema corretos.

        Cenário:
            Instanciação de ambos os repositórios.

        Dado que:
            - Uma sessão de mock assíncrona é fornecida.
        Quando:
            - Os repositórios são instanciados.
        Então:
            - O atributo `model` de `EngineRepository` é `EngineModel`.
            - O atributo `schema` de `EngineRepository` é `Engine`.
            - O atributo `model` de `EngineSpecRepository` é `EngineSpecModel`.
            - O atributo `schema` de `EngineSpecRepository` é `EngineSpec`.
        """
        engine_repo = EngineRepository(mock_session)
        assert engine_repo.model == EngineModel
        assert engine_repo.schema == Engine

        enginespec_repo = EngineSpecRepository(mock_session)
        assert enginespec_repo.model == EngineSpecModel
        assert enginespec_repo.schema == EngineSpec

    @pytest.mark.asyncio
    async def test_quando_metodo_create_e_chamado_entao_chama_create_da_base_com_corretos_argumentos(
        self, engine_repository
    ):
        """
        Verifica se o método `create` do repositório de motor chama o método
        correto da classe base com os argumentos apropriados.

        Cenário:
            Criação de um novo registro de motor.

        Dado que:
            - Um repositório de motor e uma sessão de mock estão disponíveis.
            - Um objeto de dados de motor válido é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - O método `create` da classe base é invocado uma vez.
        """
        # Dado que
        mock_data = Engine(compression_rate="10:1", total_cc=2000, aspiration="Turbo")

        engine_repository.create = AsyncMock(return_value=mock_data)

        # Quando
        result = await engine_repository.create(mock_data)

        # Então
        engine_repository.create.assert_called_once_with(mock_data)
        assert isinstance(result, Engine)
