import pytest
from pydantic import ValidationError

from mcp_car_agent.core.schemas.engine_schema import Engine, EngineSpec


class TestEngineSchemas:
    """
    Testes unitários para os schemas de Motor.
    """

    def test_quando_dados_engine_spec_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto EngineSpec é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de EngineSpec com dados válidos para todos os campos.

        Dado que:
            - Dados válidos para EngineSpec, como 'gasolina', 150 hp, 4000 rpm, etc.
        Quando:
            - O objeto EngineSpec é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - Os atributos do objeto correspondem aos dados de entrada.
        """
        # Dado que
        data = {
            "gas_type": "gasolina",
            "max_hp": 150,
            "max_hp_rpm": 6000,
            "max_torque": 250,
            "max_torque_rpm": 4000,
            "torque_unit_measure": "kgfm",
        }

        # Quando
        engine_spec_instance = EngineSpec(**data)

        # Então
        assert isinstance(engine_spec_instance, EngineSpec)
        assert engine_spec_instance.gas_type == "gasolina"
        assert engine_spec_instance.max_hp == 150
        assert engine_spec_instance.torque_unit_measure == "kgfm"

    def test_quando_engine_spec_gas_type_invalido_entao_erro_de_validacao_e_levantado(
        self,
    ):
        """
        Verifica se a criação de EngineSpec falha com um tipo de combustível inválido.

        Cenário:
            Instanciação de EngineSpec com um valor para `gas_type` que não está na lista permitida.

        Dado que:
            - Um valor de `gas_type` que não é "gasolina", "alcool" ou "gasolina/alcool".
        Quando:
            - O objeto EngineSpec é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data = {"gas_type": "diesel"}

        # Quando e Então
        with pytest.raises(ValidationError):
            EngineSpec(**invalid_data)

    def test_quando_dados_engine_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto Engine é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de Engine com todos os campos, incluindo o sub-schema EngineSpec.

        Dado que:
            - Dados válidos para Engine e EngineSpec.
        Quando:
            - O objeto Engine é instanciado.
        Então:
            - A criação do objeto é bem-sucedida.
            - O objeto EngineSpec aninhado é corretamente validado.
        """
        # Dado que
        engine_spec_data = EngineSpec(gas_type="gasolina")
        data = {
            "compression_rate": "10:1",
            "total_cc": 2000,
            "aspiration": "Turbo",
            "engine_specs": engine_spec_data,
        }

        # Quando
        engine_instance = Engine(**data)

        # Então
        assert isinstance(engine_instance, Engine)
        assert engine_instance.compression_rate == "10:1"
        assert isinstance(engine_instance.engine_specs, EngineSpec)
        assert engine_instance.engine_specs.gas_type == "gasolina"
