import pytest
from sqlmodel import select

from mcp_car_agent.core.database.models import EquipmentModel
from mcp_car_agent.core.schemas.car_schema import Car
from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.equipment_schema import Equipment
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission


@pytest.mark.asyncio
class TestEquipmentRepositoryIntegration:
    """
    Testes de integração para a classe EquipmentRepository.
    """

    async def test_quando_dados_equipamento_validos_entao_registro_e_criado_e_encontrado_no_db(
        self, car_repository, equipment_repository, session, setup_dependencies
    ):
        """
        Verifica a criação de um registro de equipamento no banco de dados.

        Cenário:
            Criação de um novo equipamento com dados válidos e um carro existente.

        Dado que:
            - Um registro de carro com ID válido já existe no banco de dados.
            - Um objeto `Equipment` com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro de Equipment é inserido no banco de dados e pode ser consultado.
        """
        # Dado que
        car_data = Car(
            name="Carro com Equipamento",
            version="Versão Teste",
            year=None,
            engine=Engine(id=setup_dependencies["engine_id"]),
            transmission=Transmission(
                id=setup_dependencies["transmission_id"], gearbox_type="11"
            ),
            manufacturer=Manufacturer(
                id=setup_dependencies["manufacturer_id"], name="11"
            ),
        )
        carro = await car_repository.create(car_data)

        initial_count = len((await session.exec(select(EquipmentModel))).all())
        assert initial_count == 0

        equipment_data = Equipment(
            category="Seguranca",
            description="Airbag Duplo",
            is_standard=True,
            is_optional=False,
            car_id=carro.id,
        )

        # Quando
        created_item = await equipment_repository.create(equipment_data)

        # Então
        db_item = await session.get(EquipmentModel, created_item.id)
        assert created_item.category == "Seguranca"
        assert db_item is not None
        assert db_item.description == "Airbag Duplo"
        assert db_item.car_id == carro.id