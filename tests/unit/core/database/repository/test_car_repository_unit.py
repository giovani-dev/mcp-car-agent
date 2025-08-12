from unittest.mock import AsyncMock, MagicMock

import pytest

from mcp_car_agent.core.database.models import CarModel, CarSpecsModel
from mcp_car_agent.core.database.repository.car_repository import (
    CarRepository,
    CarSpecsRepository,
)
from mcp_car_agent.core.schemas.car_schema import Car, CarSpecs


@pytest.mark.asyncio
class TestCarRepositories:
    """
    Testes unitários para as classes CarRepository e CarSpecsRepository.
    """

    def test_quando_repositorios_sao_iniciados_entao_model_e_schema_sao_corretos(
        self, mock_session
    ):
        """
        Verifica se CarRepository e CarSpecsRepository são inicializados com o modelo e schema corretos.

        Cenário:
            Instanciação de ambos os repositórios.

        Dado que:
            - Uma sessão de mock assíncrona é fornecida.
        Quando:
            - Os repositórios são instanciados.
        Então:
            - O atributo `model` de `CarRepository` é `CarModel`.
            - O atributo `schema` de `CarRepository` é `Car`.
            - O atributo `model` de `CarSpecsRepository` é `CarSpecsModel`.
            - O atributo `schema` de `CarSpecsRepository` é `CarSpecs`.
        """
        car_repo = CarRepository(mock_session)
        assert car_repo.model == CarModel
        assert car_repo.schema == Car

        carspec_repo = CarSpecsRepository(mock_session)
        assert carspec_repo.model == CarSpecsModel
        assert carspec_repo.schema == CarSpecs

    async def test_quando_metodo_create_e_chamado_entao_chama_create_da_base_com_corretos_argumentos(
        self, car_repository
    ):
        """
        Verifica se o método `create` do repositório de carro chama o método
        correto da classe base com os argumentos apropriados.

        Cenário:
            Criação de um novo registro de carro.

        Dado que:
            - Um repositório de carro e uma sessão de mock estão disponíveis.
            - Um objeto de dados de carro válido é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - O método `create` da classe base é invocado uma vez.
        """
        # Dado que
        mock_data = Car(name="Civic")

        car_repository.create = AsyncMock(return_value=mock_data)

        # Quando
        result = await car_repository.create(mock_data)

        # Então
        car_repository.create.assert_called_once_with(mock_data)
        assert isinstance(result, Car)
