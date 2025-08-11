import pytest
from pydantic import ValidationError

from mcp_car_agent.core.schemas.equipment_schema import Equipment


class TestEquipmentSchema:
    """
    Testes unitários para o schema de Equipamento.
    """

    def test_quando_dados_validos_entao_objeto_e_criado_com_sucesso(self):
        """
        Verifica se a criação de um objeto Equipment é bem-sucedida com dados válidos.

        Cenário:
            Instanciação de Equipment com campos de categoria e descrição.

        Dado que:
            - Dados válidos para `category` e `description`.
            - Os campos booleanos `is_standard` e `is_optional` têm valores padrão.
        Quando:
            - O objeto Equipment é instanciado.
        Então:
            - A criação do objeto é bem-sucedida, sem levantar exceções.
            - Os atributos do objeto correspondem aos dados de entrada.
            - Os valores padrão para `is_standard` e `is_optional` são aplicados corretamente.
        """
        # Dado que
        data = {
            "category": "Seguranca",
            "description": "Airbag Duplo Frontal",
        }

        # Quando
        equipment_instance = Equipment(**data)

        # Então
        assert isinstance(equipment_instance, Equipment)
        assert equipment_instance.category == "Seguranca"
        assert equipment_instance.description == "Airbag Duplo Frontal"
        assert equipment_instance.is_standard is False
        assert equipment_instance.is_optional is False

    def test_quando_dados_validos_com_booleanos_true_entao_objeto_e_criado_com_sucesso(
        self,
    ):
        """
        Verifica se a criação de um objeto Equipment é bem-sucedida com dados válidos e booleanos.

        Cenário:
            Instanciação de Equipment com `is_standard` e `is_optional` definidos como True.

        Dado que:
            - Dados válidos para `category` e `description`.
            - `is_standard` e `is_optional` são definidos como `True`.
        Quando:
            - O objeto Equipment é instanciado.
        Então:
            - A criação do objeto é bem-sucedida.
            - Os atributos booleanos são definidos como `True`.
        """
        # Dado que
        data = {
            "category": "Conforto",
            "description": "Ar-condicionado Digital",
            "is_standard": True,
            "is_optional": True,
        }

        # Quando
        equipment_instance = Equipment(**data)

        # Então
        assert equipment_instance.is_standard is True
        assert equipment_instance.is_optional is True

    def test_quando_dados_invalidos_entao_erro_de_validacao_e_levantado(self):
        """
        Verifica se a criação de um objeto Equipment falha com dados inválidos.

        Cenário:
            Instanciação de Equipment com campos obrigatórios vazios ou excedendo o tamanho.

        Dado que:
            - `category` ou `description` são strings vazias ou muito longas.
        Quando:
            - O objeto Equipment é instanciado.
        Então:
            - Uma exceção `ValidationError` é levantada.
        """
        # Dado que
        invalid_data_empty = {"category": "", "description": "desc"}
        invalid_data_long = {"category": "a" * 51, "description": "b" * 151}

        # Quando e Então
        with pytest.raises(ValidationError):
            Equipment(**invalid_data_empty)

        with pytest.raises(ValidationError):
            Equipment(**invalid_data_long)
