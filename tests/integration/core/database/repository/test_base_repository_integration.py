import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from tests.mocks.models import MockModel
from tests.mocks.schemas import MockSchema


# =========================================================================
# Testes de Integração
# =========================================================================
@pytest.mark.asyncio
class TestBaseRepositoryIntegration:
    """
    Testes de integração para a classe BaseRepository, interagindo com um banco de dados real (em memória).
    """

    async def test_quando_dados_validos_entao_registro_e_criado_e_encontrado_no_db(
        self, repository: BaseRepository, session: AsyncSession
    ):
        """
        Verifica se a criação de um registro persiste os dados no banco de dados.

        Cenário:
            Criação de um novo registro e verificação de sua existência no banco de dados.

        Dado que:
            - A tabela `mock_table` está vazia.
            - Um objeto MockSchema com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro é inserido no banco de dados e pode ser consultado com os dados corretos.
        """
        # Dado que
        initial_count = len((await session.exec(select(MockModel))).all())
        assert initial_count == 0

        mock_data = MockSchema(name="Carro Teste", is_active=True)

        # Quando
        created_item = await repository.create(mock_data)

        # Então
        # Busca o item diretamente no banco de dados para validação
        db_item = await session.get(MockModel, created_item.id)

        assert created_item.name == "Carro Teste"
        assert db_item is not None
        assert db_item.name == "Carro Teste"
        assert db_item.is_active is True

    async def test_quando_id_existe_entao_registro_e_atualizado_e_verificado_no_db(
        self, repository: BaseRepository, session: AsyncSession
    ):
        """
        Verifica se a atualização de um registro persiste as alterações no banco de dados.

        Cenário:
            Atualização de um registro existente e verificação das mudanças.

        Dado que:
            - Um registro `mock_item` existe no banco de dados.
            - Um objeto MockSchema com novos dados é fornecido.
        Quando:
            - O método `update` do repositório é chamado.
        Então:
            - O registro no banco de dados é alterado com os novos dados.
        """
        # Dado que
        mock_item = MockModel(name="Item Antigo", is_active=False)
        session.add(mock_item)
        await session.commit()
        await session.refresh(mock_item)

        update_data = MockSchema(name="Item Novo", is_active=True)

        # Quando
        updated_item = await repository.update(update_data, mock_item.id)

        # Então
        # Busca o item atualizado para validação
        db_item = await session.get(MockModel, mock_item.id)
        assert updated_item.name == "Item Novo"
        assert db_item.name == "Item Novo"
        assert db_item.is_active is True

    async def test_quando_id_existe_entao_registro_e_deletado_e_nao_encontrado_no_db(
        self, repository: BaseRepository, session: AsyncSession
    ):
        """
        Verifica se a exclusão de um registro o remove permanentemente do banco de dados.

        Cenário:
            Exclusão de um registro existente.

        Dado que:
            - Um registro `mock_item` existe no banco de dados.
        Quando:
            - O método `delete` do repositório é chamado.
        Então:
            - O registro não é mais encontrado no banco de dados.
            - O método retorna `True`.
        """
        # Dado que
        mock_item = MockModel(name="Item para Deletar", is_active=False)
        session.add(mock_item)
        await session.commit()
        await session.refresh(mock_item)

        item_id = mock_item.id

        # Quando
        result = await repository.delete(item_id)

        # Então
        db_item = await session.get(MockModel, item_id)
        assert result is True
        assert db_item is None

    async def test_quando_filtros_sao_validos_entao_registros_filtrados_sao_buscados_corretamente(
        self, repository: BaseRepository, session: AsyncSession
    ):
        """
        Verifica se a busca com filtros retorna os resultados esperados do banco de dados.

        Cenário:
            Busca por registros ativos e inativos com filtros.

        Dado que:
            - Múltiplos registros, com status `is_active` True e False, existem no banco de dados.
        Quando:
            - O método `search` é chamado com o filtro `{"is_active": True}`.
        Então:
            - Apenas os registros com `is_active` igual a True são retornados.
        """
        # Dado que
        session.add(MockModel(name="Carro 1", is_active=True))
        session.add(MockModel(name="Carro 2", is_active=False))
        session.add(MockModel(name="Carro 3", is_active=True))
        await session.commit()

        # Quando
        results = await repository.search(filters={"is_active": True})

        # Então
        assert len(results) == 2
        for item in results:
            assert item.is_active is True

    async def test_quando_criterio_valido_e_unico_entao_registro_unico_e_retornado_corretamente(
        self, repository: BaseRepository, session: AsyncSession
    ):
        """
        Verifica se a busca por um único registro retorna o objeto correto.

        Cenário:
            Busca por um registro específico usando o método `get_one`.

        Dado que:
            - Um registro `mock_item` existe no banco de dados com um nome único.
        Quando:
            - O método `get_one` é chamado com o critério `{"name": "Item único"}`.
        Então:
            - O objeto retornado é exatamente o registro do banco de dados.
        """
        # Dado que
        mock_item = MockModel(name="Item único", is_active=True)
        session.add(mock_item)
        await session.commit()
        await session.refresh(mock_item)

        # Quando
        result = await repository.get_one(by={"name": "Item único"})

        # Então
        assert result.name == "Item único"
        assert result.is_active is True
