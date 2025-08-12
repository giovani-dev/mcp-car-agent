import pytest
from sqlmodel import select

from mcp_car_agent.core.database.models import EngineModel, EngineSpecModel
from mcp_car_agent.core.schemas.engine_schema import Engine, EngineSpec


@pytest.mark.asyncio
class TestEngineRepositoryIntegration:
    """
    Testes de integração para as classes EngineRepository e EngineSpecRepository.
    """

    async def test_quando_dados_motor_validos_entao_registro_e_criado_e_encontrado_no_db(
        self, engine_repository, session
    ):
        """
        Verifica a criação de um registro de motor no banco de dados.

        Cenário:
            Criação de um novo motor com dados válidos.

        Dado que:
            - A tabela `engine` está vazia.
            - Um objeto `Engine` com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro de Motor é inserido no banco de dados e pode ser consultado.
        """
        # Dado que
        initial_count = len((await session.exec(select(EngineModel))).all())
        assert initial_count == 0

        engine_data = Engine(compression_rate="10:1", total_cc=2000, aspiration="Turbo")

        # Quando
        created_item = await engine_repository.create(engine_data)

        # Então
        db_item = await session.get(EngineModel, created_item.id)
        assert created_item.compression_rate == "10:1"
        assert db_item is not None
        assert db_item.total_cc == 2000

    async def test_quando_dados_especificacao_motor_validos_entao_registro_e_criado(
        self, engine_spec_repository, session, setup_dependencies
    ):
        """
        Verifica a criação de um registro de especificação de motor no banco de dados.

        Cenário:
            Criação de uma nova especificação de motor com dados válidos.

        Dado que:
            - A tabela `engine_specs` está vazia.
            - Um objeto `EngineSpec` com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro de EngineSpec é inserido no banco de dados e pode ser consultado.
        """
        # Dado que
        initial_count = len((await session.exec(select(EngineSpecModel))).all())
        assert initial_count == 0

        engine_spec_data = EngineSpec(
            gas_type="gasolina",
            max_hp=150,
            engine=Engine(id=setup_dependencies["engine_id"]),
        )

        # Quando
        created_item = await engine_spec_repository.create(engine_spec_data)

        # Então
        db_item = await session.get(EngineSpecModel, created_item.id)
        assert created_item.gas_type == "gasolina"
        assert db_item is not None
        assert db_item.max_hp == 150
        assert db_item.engine_id == setup_dependencies["engine_id"]
