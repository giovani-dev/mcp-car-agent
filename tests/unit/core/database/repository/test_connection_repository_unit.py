from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_car_agent.core.database.repository.connection_repository import (
    ConnectionRepository,
)


class TestConnectionRepositoryUnit:
    """
    Testes unitários para a classe ConnectionRepository.
    """

    @pytest.mark.asyncio
    async def test_quando_connect_e_chamado_entao_configuracoes_corretas_sao_usadas(
        self, monkeypatch, mock_config
    ):
        """
        Verifica se o método `connect` usa as configurações de banco de dados
        corretamente para criar o engine e a sessão.

        Cenário:
            Criação de uma conexão assíncrona com o banco de dados.

        Dado que:
            - As variáveis de ambiente de configuração estão mockadas.
        Quando:
            - O método `connect` do repositório é chamado.
        Então:
            - `create_async_engine` é chamado com a string de conexão correta.
            - `SQLModel.metadata.create_all` é chamado.
            - Uma sessão é cedida (yielded) pelo gerador assíncrono.
        """
        # Dado que
        mock_conn = AsyncMock()

        mock_conn.run_sync = AsyncMock()

        mock_begin = AsyncMock()
        mock_begin.__aenter__ = AsyncMock(return_value=mock_conn)
        mock_begin.__aexit__ = AsyncMock(return_value=None)

        mock_engine = MagicMock()
        mock_engine.begin.return_value = mock_begin

        mock_create_async_engine = MagicMock(return_value=mock_engine)

        mock_session = AsyncMock()
        mock_session.__aenter__ = AsyncMock(return_value=mock_session)
        mock_session.__aexit__ = AsyncMock(return_value=None)
        mock_async_session = MagicMock(return_value=mock_session)

        mock_async_sessionmaker = MagicMock(return_value=mock_async_session)

        mock_sqlmodel = MagicMock()

        monkeypatch.setattr(
            "mcp_car_agent.core.database.repository.connection_repository.create_async_engine",
            mock_create_async_engine,
        )
        monkeypatch.setattr(
            "mcp_car_agent.core.database.repository.connection_repository.async_sessionmaker",
            mock_async_sessionmaker,
        )
        monkeypatch.setattr(
            "mcp_car_agent.core.database.repository.connection_repository.SQLModel.metadata.create_all",
            mock_sqlmodel,
        )
        monkeypatch.setattr("urllib.parse.quote", lambda s: s)

        # Quando
        async_gen = ConnectionRepository.connect()
        session = await async_gen.__anext__()

        # Então
        mock_create_async_engine.assert_called_once_with(
            "postgresql+asyncpg://user:pwd@host:port/db", echo=True
        )
        mock_conn.assert_not_called()
        mock_conn.run_sync.assert_called_once()
        mock_engine.assert_not_called()
        mock_engine.begin.assert_called_once()
        mock_begin.assert_not_called()
        mock_begin.__aenter__.assert_called_once()
        mock_begin.__aexit__.assert_called_once()
        mock_sqlmodel.metadata.create_all.assert_not_called()
        assert session is not None
        assert session == mock_session
