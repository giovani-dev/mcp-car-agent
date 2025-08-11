import pytest
from pydantic import ValidationError

from mcp_car_agent.core.schemas.manufacturer_schema import Manufacturer


class TestManufacturerSchema:
    """
    Testes unitários para o schema de Fabricante.
    """

    def test_quando_dados_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto Manufacturer é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de Manufacturer com um nome de fabricante válido.

        Dado que:
            - O nome do fabricante é uma string válida com tamanho entre 1 e 150 caracteres.
        Quando:
            - O objeto Manufacturer é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - O atributo `name` corresponde ao dado de entrada.
        """
        # Dado que
        data = {"name": "Volkswagen"}

        # Quando
        manufacturer_instance = Manufacturer(**data)

        # Então
        assert isinstance(manufacturer_instance, Manufacturer)
        assert manufacturer_instance.name == "Volkswagen"

    def test_quando_nome_vazio_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto Manufacturer falha com um nome vazio.

        Cenário:
            Instanciação de Manufacturer com uma string de nome vazia.

        Dado que:
            - O nome do fabricante é uma string vazia.
        Quando:
            - O objeto Manufacturer é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data = {"name": ""}

        # Quando e Então
        with pytest.raises(ValidationError):
            Manufacturer(**invalid_data)

    def test_quando_nome_muito_longo_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto Manufacturer falha com um nome muito longo.

        Cenário:
            Instanciação de Manufacturer com um nome que excede o limite de 150 caracteres.

        Dado que:
            - O nome do fabricante tem mais de 150 caracteres.
        Quando:
            - O objeto Manufacturer é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data = {"name": "a" * 151}

        # Quando e Então
        with pytest.raises(ValidationError):
            Manufacturer(**invalid_data)
