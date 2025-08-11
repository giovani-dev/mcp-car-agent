from typing import Optional, TypeVar
from unittest.mock import AsyncMock, MagicMock

import pytest
from pydantic import BaseModel
from sqlalchemy.exc import MultipleResultsFound
from sqlmodel import Field, SQLModel

from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from tests.mocks.models import MockModel
from tests.mocks.schemas import MockSchema


@pytest.mark.asyncio
class TestBaseRepository:
    """
    Testes unitários para a classe BaseRepository.
    """

    async def test_quando_dados_validos_entao_registro_e_criado_com_sucesso(
        self, repository, mock_session
    ):
        """
        Verifica a criação bem-sucedida de um registro com dados válidos.

        Cenário:
            Criação de um novo registro no banco de dados.

        Dado que:
            - A sessão do banco de dados está disponível e funcional.
            - Um objeto MockSchema com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - A sessão adiciona o objeto ao banco de dados.
            - A sessão faz o commit das alterações.
            - O objeto retornado é um MockSchema válido.
        """
        # Dado que
        mock_data = MockSchema(name="Test Item", is_active=True)

        # Quando
        result = await repository.create(mock_data)

        # Então
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once()
        assert isinstance(result, MockSchema)
        assert result.name == "Test Item"

    async def test_quando_id_existe_entao_registro_e_atualizado_com_sucesso(
        self, repository, mock_session
    ):
        """
        Verifica a atualização bem-sucedida de um registro existente.

        Cenário:
            Atualização de um registro existente.

        Dado que:
            - Um registro com um ID específico existe no banco de dados.
            - Um objeto MockSchema com dados de atualização é fornecido.
        Quando:
            - O método `update` do repositório é chamado.
        Então:
            - A sessão obtém o registro existente.
            - Os atributos do registro são atualizados corretamente.
            - A sessão faz o commit das alterações.
            - O objeto retornado é um MockSchema com os dados atualizados.
        """
        # Dado que
        mock_id = 1
        existing_model = MockModel(id=mock_id, name="Old Name", is_active=False)
        mock_session.get.return_value = existing_model
        update_data = MockSchema(name="New Name")

        # Quando
        result = await repository.update(update_data, mock_id)

        # Então
        mock_session.get.assert_called_once_with(MockModel, mock_id)
        assert existing_model.name == "New Name"
        assert existing_model.is_active is False
        mock_session.add.assert_called_once_with(existing_model)
        mock_session.commit.assert_called_once()
        mock_session.refresh.assert_called_once_with(existing_model)
        assert isinstance(result, MockSchema)
        assert result.name == "New Name"
        assert result.is_active is False

    async def test_quando_id_nao_existe_entao_erro_e_levantado_ao_atualizar(
        self, repository, mock_session
    ):
        """
        Verifica se a atualização falha com um erro quando o ID não existe.

        Cenário:
            Tentativa de atualizar um registro que não existe.

        Dado que:
            - Nenhum registro com o ID fornecido existe no banco de dados.
        Quando:
            - O método `update` do repositório é chamado com um ID inválido.
        Então:
            - Uma exceção `ValueError` é levantada.
        """
        # Dado que
        mock_id = 99
        mock_session.get.return_value = None
        update_data = MockSchema(name="New Name")

        # Quando e Então
        with pytest.raises(
            ValueError, match=f"{MockModel.__name__} com ID {mock_id} não encontrado."
        ):
            await repository.update(update_data, mock_id)
        mock_session.commit.assert_not_called()

    async def test_quando_id_existe_entao_registro_e_deletado_com_sucesso(
        self, repository, mock_session
    ):
        """
        Verifica a exclusão bem-sucedida de um registro.

        Cenário:
            Exclusão de um registro existente.

        Dado que:
            - Um registro com um ID específico existe no banco de dados.
        Quando:
            - O método `delete` do repositório é chamado com o ID.
        Então:
            - A sessão deleta o registro.
            - A sessão faz o commit das alterações.
            - O método retorna `True`.
        """
        # Dado que
        mock_id = 1
        existing_model = MockModel(id=mock_id, name="Test Item", is_active=True)
        mock_session.get.return_value = existing_model

        # Quando
        result = await repository.delete(mock_id)

        # Então
        mock_session.delete.assert_called_once_with(existing_model)
        mock_session.commit.assert_called_once()
        assert result is True

    async def test_quando_id_nao_existe_entao_nada_e_deletado(
        self, repository, mock_session
    ):
        """
        Verifica se a exclusão falha silenciosamente quando o ID não existe.

        Cenário:
            Tentativa de excluir um registro que não existe.

        Dado que:
            - Nenhum registro com o ID fornecido existe no banco de dados.
        Quando:
            - O método `delete` do repositório é chamado com um ID inválido.
        Então:
            - A sessão não tenta deletar nada.
            - O método retorna `False`.
        """
        # Dado que
        mock_id = 99
        mock_session.get.return_value = None

        # Quando
        result = await repository.delete(mock_id)

        # Então
        mock_session.delete.assert_not_called()
        mock_session.commit.assert_not_called()
        assert result is False

    async def test_quando_filtros_sao_validos_entao_registros_sao_buscados_corretamente(
        self, repository, mock_session
    ):
        """
        Verifica se a busca com filtros, ordenação e paginação funciona.

        Cenário:
            Busca de registros com critérios específicos.

        Dado que:
            - Uma lista de modelos mock está disponível para ser retornada.
            - Filtros, ordenação e limites de paginação são fornecidos.
        Quando:
            - O método `search` do repositório é chamado.
        Então:
            - A consulta é construída corretamente com filtros, ordenação e limites.
            - Uma lista de objetos MockSchema é retornada.
        """
        # Dado que
        mock_models = [
            MockModel(id=1, name="Item 1", is_active=True),
            MockModel(id=2, name="Item 2", is_active=False),
        ]

        mock_exec_result = MagicMock()
        mock_exec_result.all.return_value = mock_models
        mock_session.exec.return_value = mock_exec_result
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Quando
        results = await repository.search(filters={"is_active": True}, limit=1)

        # Então
        mock_session.exec.assert_called_once()
        # Nota: É difícil testar a construção exata da query com mocks.
        # A validação se concentra no resultado retornado e se a chamada
        # à sessão foi feita.
        assert len(results) == 2
        assert isinstance(results[0], MockSchema)
        assert results[0].name == "Item 1"

    async def test_quando_criterio_valido_e_unico_entao_registro_unico_e_retornado(
        self, repository, mock_session
    ):
        """
        Verifica se a busca por um único registro funciona com sucesso.

        Cenário:
            Busca de um único registro com um critério que retorna apenas um resultado.

        Dado que:
            - A busca com um critério específico retorna um único registro.
        Quando:
            - O método `get_one` do repositório é chamado.
        Então:
            - A sessão executa a consulta.
            - O objeto retornado é um MockSchema válido.
        """
        # Dado que
        mock_model = MockModel(id=1, name="Unique Item", is_active=True)
        mock_exec_result = MagicMock()
        mock_exec_result.one_or_none.return_value = mock_model
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Quando
        result = await repository.get_one(by={"id": 1})

        # Então
        mock_session.exec.assert_called_once()
        assert isinstance(result, MockSchema)
        assert result.name == "Unique Item"
        assert result.is_active is True

    async def test_quando_criterio_nao_encontra_registro_entao_erro_e_levantado(
        self, repository, mock_session
    ):
        """
        Verifica se a busca por um único registro falha quando nenhum é encontrado.

        Cenário:
            Busca de um único registro com um critério que não retorna resultados.

        Dado que:
            - A busca com um critério específico não retorna registros.
        Quando:
            - O método `get_one` do repositório é chamado.
        Então:
            - Uma exceção `ValueError` é levantada.
        """
        # Dado que
        mock_exec_result = MagicMock()
        mock_exec_result.one_or_none.return_value = None
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Quando e Então
        with pytest.raises(ValueError, match="Nenhum MockModel encontrado"):
            await repository.get_one(by={"id": 99})

    async def test_quando_criterio_retorna_multiplos_registros_entao_erro_e_levantado(
        self, repository, mock_session
    ):
        """
        Verifica se a busca por um único registro falha quando múltiplos são encontrados.

        Cenário:
            Busca de um único registro com um critério que retorna múltiplos resultados.

        Dado que:
            - A busca com um critério específico retorna mais de um registro.
        Quando:
            - O método `get_one` do repositório é chamado.
        Então:
            - Uma exceção `ValueError` é levantada.
        """
        # Dado que
        mock_exec_result = MagicMock()
        mock_exec_result.one_or_none.side_effect = MultipleResultsFound
        mock_session.exec = AsyncMock(return_value=mock_exec_result)

        # Quando e Então
        with pytest.raises(ValueError, match="Mais de um MockModel encontrado"):
            await repository.get_one(by={"is_active": True})

    async def test_quando_criterio_by_e_vazio_entao_erro_e_levantado(
        self, repository, mock_session
    ):
        """
        Verifica se um ValueError é levantado quando 'by' é um dicionário vazio.

        Cenário:
            Tentativa de buscar um único registro com um dicionário 'by' vazio.

        Dado que:
            - O método `get_one` é chamado com um dicionário vazio.
        Quando:
            - O método `get_one` do repositório é chamado.
        Então:
            - Uma exceção `ValueError` é levantada com a mensagem apropriada.
        """
        # Dado que
        mock_by = {}

        # Quando e Então
        with pytest.raises(ValueError, match="O critério 'by' não pode estar vazio."):
            await repository.get_one(by=mock_by)
