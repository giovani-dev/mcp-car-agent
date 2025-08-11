import pytest
from pydantic import ValidationError

from mcp_car_agent.core.schemas.transmission_schema import Transmission


class TestTransmissionSchema:
    """
    Testes unitários para o schema de Transmissão.
    """

    def test_quando_dados_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto Transmission é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de Transmission com todos os campos.

        Dado que:
            - Dados válidos para `gearbox_type`, `gears_qtde` e `traction`.
        Quando:
            - O objeto Transmission é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - Os atributos do objeto correspondem aos dados de entrada.
        """
        # Dado que
        data = {
            "gearbox_type": "Automático",
            "gears_qtde": 8,
            "traction": "FWD",
        }

        # Quando
        transmission_instance = Transmission(**data)

        # Então
        assert isinstance(transmission_instance, Transmission)
        assert transmission_instance.gearbox_type == "Automático"
        assert transmission_instance.gears_qtde == 8
        assert transmission_instance.traction == "FWD"

    def test_quando_dados_invalidos_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto Transmission falha com dados inválidos.

        Cenário:
            Instanciação de Transmission com campos obrigatórios ausentes ou com tamanho incorreto.

        Dado que:
            - O campo `gearbox_type` está ausente ou tem mais de 20 caracteres.
        Quando:
            - O objeto Transmission é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data_missing = {"gears_qtde": 6}
        invalid_data_long = {"gearbox_type": "a" * 21}

        # Quando e Então
        with pytest.raises(ValidationError):
            Transmission(**invalid_data_missing)

        with pytest.raises(ValidationError):
            Transmission(**invalid_data_long)
