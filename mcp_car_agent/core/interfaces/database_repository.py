"""
Módulo de interfaces para repositórios de banco de dados.

Este módulo define os contratos (interfaces) para a camada de persistência.
O objetivo é garantir que a lógica de negócios não dependa de uma
implementação de banco de dados específica, seguindo o padrão "Ports and Adapters".
"""

from abc import ABC, abstractmethod
from typing import AsyncGenerator, Generic, Optional, TypeVar

T = TypeVar("T")


class IConnectionRepository(ABC, Generic[T]):
    """
    Interface para repositórios de conexão de banco de dados.

    Define um contrato para classes que gerenciam a conexão com o banco de dados,
    fornecendo uma maneira de obter uma sessão de forma assíncrona.
    """

    @staticmethod
    @abstractmethod
    async def connect() -> AsyncGenerator[T, None]:
        """
        Método abstrato para estabelecer e gerenciar uma conexão com o banco de dados.

        A implementação deve retornar um gerador assíncrono para ser usado em um
        contexto de ciclo de vida da aplicação ou como uma dependência.

        Returns:
            AsyncGenerator[T, None]: Um gerador assíncrono que cede uma sessão de banco de dados.
        """
        pass


class IDefaultRepository(ABC, Generic[T]):
    """
    Interface para operações CRUD de repositórios.

    Define os métodos básicos para operações de criação, leitura, atualização e
    exclusão (CRUD), garantindo que qualquer repositório que implemente
    esta interface siga este padrão.
    """

    @abstractmethod
    async def create(self, data: T):
        """
        Cria um novo registro no repositório.

        Args:
            data (T): O objeto de dados a ser criado.
        """
        pass

    @abstractmethod
    async def update(self, data: T, _id: int):
        """
        Atualiza um registro existente com um ID específico.

        Args:
            data (T): O objeto de dados com as informações de atualização.
            _id (int): O identificador do registro a ser atualizado.
        """
        pass

    @abstractmethod
    async def delete(self, _id: int):
        """
        Exclui um registro com um ID específico.

        Args:
            _id (int): O identificador do registro a ser excluído.
        """
        pass

    @abstractmethod
    async def search(
        self,
        filters: Optional[dict] = None,
        order_by: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[T]:
        """
        Busca registros no repositório, com suporte a filtros e paginação.

        Args:
            filters (Optional[dict]): Dicionário de filtros para a consulta.
            order_by (Optional[str]): Coluna para ordenação dos resultados.
            offset (Optional[int]): O ponto de partida da paginação.
            limit (Optional[int]): O número máximo de resultados a serem retornados.

        Returns:
            list[T]: Uma lista de objetos que correspondem aos critérios de busca.
        """
        pass

    @abstractmethod
    async def get_one(self, by: dict) -> T:
        """
        Busca e retorna um único registro com base em um critério específico.

        Args:
            by (dict): Um dicionário de critérios para a busca, como {"id": 1}.

        Returns:
            T: O objeto que corresponde ao critério de busca.

        Raises:
            Exception: Se mais de um registro for encontrado ou nenhum.
        """
        pass
