import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from mcp_car_agent.core.database.models import CarModel, CarSpecsModel
from mcp_car_agent.core.database.repository.base_repository import BaseRepository
from mcp_car_agent.core.schemas.car_schema import Car, CarSpecs
from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission


@pytest.mark.asyncio
class TestCarRepositoryIntegration:
    """
    Testes de integração para a classe CarRepository.
    """

    async def test_quando_dados_carro_validos_entao_registro_e_criado_e_encontrado_no_db(
        self, car_repository, session, setup_dependencies
    ):
        """
        Verifica a criação de um registro de carro no banco de dados.

        Cenário:
            Criação de um novo carro com dados válidos e dependências existentes.

        Dado que:
            - Dependências (engine, transmission, manufacturer) já existem no banco de dados.
            - Um objeto Car com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro de Carro é inserido no banco de dados e pode ser consultado.
        """
        # Dado que
        initial_count = len((await session.exec(select(CarModel))).all())
        assert initial_count == 0

        car_data = Car(
            name="Civic",
            version="Type R",
            year=None,
            engine=Engine(total_cc=2000),
            transmission=Transmission(gearbox_type="Manual"),
            manufacturer=Manufacturer(name="Honda"),
        )
        # Força o uso dos IDs das dependências criadas no setup
        car_data.engine.id = setup_dependencies["engine_id"]
        car_data.transmission.id = setup_dependencies["transmission_id"]
        car_data.manufacturer.id = setup_dependencies["manufacturer_id"]

        # Quando
        created_item = await car_repository.create(car_data)

        # Então
        db_item = await session.get(CarModel, created_item.id)
        assert created_item.name == "Civic"
        assert db_item is not None
        assert db_item.name == "Civic"

    async def test_quando_carro_existe_entao_registro_e_atualizado_e_verificado_no_db(
        self, car_repository, session, setup_dependencies
    ):
        """
        Verifica a atualização de um registro de carro existente.

        Cenário:
            Atualização de um registro de carro já presente no banco de dados.

        Dado que:
            - Um registro `carro_antigo` existe no banco de dados.
            - Um objeto `Car` com novos dados é fornecido.
        Quando:
            - O método `update` do repositório é chamado.
        Então:
            - O registro no banco de dados é alterado com os novos dados.
        """
        # Dado que
        carro_antigo = CarModel(
            name="Civic",
            version="VTI",
            year=None,
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        session.add(carro_antigo)
        await session.commit()
        await session.refresh(carro_antigo)

        update_data = Car(
            name="Civic",
            version="Type R",
        )

        # Quando
        updated_item = await car_repository.update(update_data, carro_antigo.id)

        # Então
        db_item = await session.get(CarModel, carro_antigo.id)
        assert updated_item.version == "Type R"
        assert db_item.version == "Type R"

    async def test_quando_id_carro_existe_entao_registro_e_deletado_e_nao_encontrado_no_db(
        self, car_repository, session, setup_dependencies
    ):
        """
        Verifica a exclusão de um registro de carro.

        Cenário:
            Exclusão de um registro de carro existente.

        Dado que:
            - Um registro `carro_para_deletar` existe no banco de dados.
        Quando:
            - O método `delete` do repositório é chamado.
        Então:
            - O registro não é mais encontrado no banco de dados.
            - O método retorna `True`.
        """
        # Dado que
        carro_para_deletar = CarModel(
            name="Civic",
            version="VTI",
            year=None,
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        session.add(carro_para_deletar)
        await session.commit()
        await session.refresh(carro_para_deletar)

        item_id = carro_para_deletar.id

        # Quando
        result = await car_repository.delete(item_id)

        # Então
        db_item = await session.get(CarModel, item_id)
        assert result is True
        assert db_item is None

    async def test_quando_filtros_validos_entao_registros_filtrados_sao_buscados_corretamente(
        self, car_repository, session, setup_dependencies
    ):
        """
        Verifica se a busca com filtros de carro retorna os resultados esperados.

        Cenário:
            Busca por registros de carros com um nome específico.

        Dado que:
            - Vários registros de carros com nomes diferentes existem no banco de dados.
        Quando:
            - O método `search` é chamado com o filtro `{"name": "Focus"}`.
        Então:
            - Apenas os registros com o nome "Focus" são retornados.
        """
        # Dado que
        carro_a = CarModel(
            name="Focus",
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        carro_b = CarModel(
            name="Ka",
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        carro_c = CarModel(
            name="Focus",
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        session.add(carro_a)
        session.add(carro_b)
        session.add(carro_c)
        await session.commit()

        # Quando
        results = await car_repository.search(filters={"name": "Focus"})

        # Então
        assert len(results) == 2
        for item in results:
            assert item.name == "Focus"

    async def test_quando_criterio_unico_e_valido_entao_registro_unico_e_retornado(
        self, car_repository, session, setup_dependencies
    ):
        """
        Verifica se a busca por um único registro de carro retorna o objeto correto.

        Cenário:
            Busca por um registro específico usando o método `get_one`.

        Dado que:
            - Um registro `carro_unico` existe no banco de dados.
        Quando:
            - O método `get_one` é chamado com o critério `{"name": "Carro Unico"}`.
        Então:
            - O objeto retornado é exatamente o registro do banco de dados.
        """
        # Dado que
        carro_unico = CarModel(
            name="Carro Unico",
            engine_id=setup_dependencies["engine_id"],
            transmission_id=setup_dependencies["transmission_id"],
            manufacturer_id=setup_dependencies["manufacturer_id"],
        )
        session.add(carro_unico)
        await session.commit()
        await session.refresh(carro_unico)

        # Quando
        result = await car_repository.get_one(by={"name": "Carro Unico"})

        # Então
        assert result.name == "Carro Unico"


@pytest.mark.asyncio
class TestCarSpecRepositoryIntegration:
    """
    Testes de integração para a classe CarSpecRepository.
    """

    async def test_quando_specs_validos_entao_registro_e_criado_e_encontrado(
        self, car_spec_repository, session, car_with_specs
    ):
        """
        Verifica a criação de um registro de especificação de carro.

        Cenário:
            Criação de uma nova especificação de carro.

        Dado que:
            - Um objeto CarSpecs com dados válidos é fornecido.
        Quando:
            - O método `create` do repositório é chamado.
        Então:
            - Um registro de CarSpecs é inserido no banco de dados e pode ser consultado.
        """
        # Dado que
        initial_count = len((await session.exec(select(CarSpecsModel))).all())
        assert initial_count == 1

        car_specs_data = CarSpecs(
            gas="Alcool",
            config="Config",
            doors=2,
            spaces=4,
            car=Car(id=car_with_specs["carro"].id),
        )

        # Quando
        created_item = await car_spec_repository.create(car_specs_data)

        # Então
        db_item = await session.get(CarSpecsModel, created_item.id)
        assert created_item.gas == "Alcool"
        assert db_item is not None
        assert db_item.gas == "Alcool"
        assert db_item.car_id == car_with_specs["carro"].id
