from datetime import date

import pytest
from pydantic import ValidationError

from mcp_car_agent.core.schemas.car_schema import Car, CarSpecs
from mcp_car_agent.core.schemas.engine_schema import Engine
from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer
from mcp_car_agent.core.schemas.transmission_schema import Transmission


class TestCarSchemas:
    """
    Testes unitários para os schemas de Carro.
    """

    def test_quando_dados_car_specs_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto CarSpecs é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de CarSpecs com todos os campos opcionais.

        Dado que:
            - Dados válidos para CarSpecs, incluindo gas, config, doors e spaces.
        Quando:
            - O objeto CarSpecs é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - Os atributos do objeto correspondem aos dados de entrada.
        """
        # Dado que
        data = {
            "gas": "Gasolina",
            "config": "Configuração",
            "doors": 4,
            "spaces": 5,
        }

        # Quando
        car_specs_instance = CarSpecs(**data)

        # Então
        assert isinstance(car_specs_instance, CarSpecs)
        assert car_specs_instance.gas == "Gasolina"
        assert car_specs_instance.config == "Configuração"
        assert car_specs_instance.doors == 4
        assert car_specs_instance.spaces == 5

    def test_quando_car_specs_dados_invalidos_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto CarSpecs falha com dados inválidos.

        Cenário:
            Instanciação de CarSpecs com dados que excedem o tamanho máximo.

        Dado que:
            - Dados de `gas` e `config` com mais de 50 e 45 caracteres, respectivamente.
        Quando:
            - O objeto CarSpecs é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data = {
            "gas": "a" * 51,
            "config": "b" * 46,
        }

        # Quando e Então
        with pytest.raises(ValidationError):
            CarSpecs(**invalid_data)

    def test_quando_dados_car_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto Car é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de Car com todos os campos obrigatórios e opcionais.

        Dado que:
            - Dados válidos para Car, incluindo sub-schemas Engine, Transmission, Manufacturer e listas.
        Quando:
            - O objeto Car é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - Os atributos do objeto correspondem aos dados de entrada.
        """
        # Dado que
        engine_data = Engine(compression_rate="10:1", total_cc=2000, aspiration="Turbo")
        transmission_data = Transmission(
            gearbox_type="Manual", gears_qtde=6, traction="FWD"
        )
        manufacturer_data = Manufacturer(name="Honda")
        car_specs_data = [CarSpecs(doors=4, spaces=5, gas="gasolina", config="sedan")]

        data = {
            "name": "Civic",
            "version": "Type R",
            "year": date(2025, 1, 1),
            "engine": engine_data,
            "transmission": transmission_data,
            "manufacturer": manufacturer_data,
            "equipments": ["Ar-condicionado"],
            "car_specs": car_specs_data,
        }

        # Quando
        car_instance = Car(**data)

        # Então
        assert isinstance(car_instance, Car)
        assert car_instance.name == "Civic"
        assert car_instance.engine.aspiration == "Turbo"
        assert len(car_instance.car_specs) == 1

    def test_quando_car_dados_invalidos_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto Car falha com dados inválidos.

        Cenário:
            Instanciação de Car com dados de sub-schemas inválidos ou campos obrigatórios faltando.

        Dado que:
            - Dados de `name` e `version` que excedem o tamanho máximo.
            - O campo obrigatório `engine` está ausente.
        Quando:
            - O objeto Car é instanciado com dados inválidos.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        transmission_data = Transmission(gearbox_type="Manual")
        manufacturer_data = Manufacturer(name="Toyota")
        invalid_data = {
            "name": "a" * 81,
            "version": "b" * 81,
            "transmission": transmission_data,
            "manufacturer": manufacturer_data,
            "equipments": [],
            "car_specs": [],
        }

        # Quando e Então
        with pytest.raises(ValidationError):
            Car(**invalid_data)
