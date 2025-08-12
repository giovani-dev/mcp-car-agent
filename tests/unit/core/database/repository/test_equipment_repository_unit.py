import pytest

from mcp_car_agent.core.database.models import EquipmentModel
from mcp_car_agent.core.database.repository.equipment_repository import (
    EquipmentRepository,
)
from mcp_car_agent.core.schemas.equipment_schema import Equipment


class TestEquipmentRepositoryUnit:
    """
    Testes unitários para a classe EquipmentRepository.
    """

    def test_quando_repositorio_e_iniciado_entao_model_e_schema_sao_corretos(
        self, mock_session
    ):
        """
        Verifica se EquipmentRepository é inicializado com o modelo e schema corretos.

        Cenário:
            Instanciação do repositório.

        Dado que:
            - Uma sessão de mock assíncrona é fornecida.
        Quando:
            - O repositório é instanciado.
        Então:
            - O atributo `model` de `EquipmentRepository` é `EquipmentModel`.
            - O atributo `schema` de `EquipmentRepository` é `Equipment`.
        """
        # Quando
        repository = EquipmentRepository(mock_session)

        # Então
        assert repository.model == EquipmentModel
        assert repository.schema == Equipment

    @pytest.mark.asyncio
    async def test_quando_metodo_input_e_chamado_entao_retorna_modelo_correto_do_banco(
        self, mock_session
    ):
        """
        Verifica se o método `input` do repositório de equipamento retorna o modelo do banco de dados correto.

        Cenário:
            Criação de um objeto de modelo de banco de dados a partir de um schema.

        Dado que:
            - Uma instância de `EquipmentRepository` é criada com uma sessão de mock.
            - Um objeto `Equipment` com dados válidos é fornecido.
        Quando:
            - O método `input` do repositório é chamado com o objeto de dados.
        Então:
            - Um objeto `EquipmentModel` é retornado.
            - Os atributos do objeto `EquipmentModel` correspondem aos do objeto `Equipment`.
        """
        # Dado que
        repository = EquipmentRepository(mock_session)
        equipment_data = Equipment(
            category="Seguranca",
            description="Airbag Duplo Frontal",
            is_standard=True,
            is_optional=False,
        )

        # Quando
        result = await repository.input(equipment_data)

        # Então
        assert isinstance(result, EquipmentModel)
        assert result.category == equipment_data.category
        assert result.description == equipment_data.description
        assert result.is_standard == equipment_data.is_standard
        assert result.is_optional == equipment_data.is_optional
