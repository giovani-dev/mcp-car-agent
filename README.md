# mcp-car-agent


## 🎯 Objetivo do Projeto
O principal objetivo é demonstrar a capacidade de construir uma solução bem pensada, utilizando boas práticas de desenvolvimento, com foco em:
* Modelagem de dados.
* Automatização da inserção de dados.
* Comunicação cliente-servidor assíncrona.
* Construção de uma aplicação interativa no terminal.

## ✨ Funcionalidades e Requisitos

### 1. Modelagem de Dados

### 2. População do Banco de Dados

### 3. Comunicação via Protocolo MCP (Model Context Protocol)

### 4. Aplicação no Terminal com Agente Virtual
O agente virtual interage com o usuário no terminal de forma conversacional e intuitiva. Em vez de um menu rígido, ele faz perguntas fluidas para coletar os critérios de busca. Após coletar as informações, ele envia uma requisição ao servidor e exibe os resultados de maneira clara e amigável, incluindo detalhes como marca, modelo, ano, cor, quilometragem e preço.

## 🚀 Como Executar o Projeto

**Pré-requisitos:**
* Docker e Docker Compose.
* Poetry (para gerenciamento de dependências).

1.  **Clone o repositório:**
    ```bash
    git clone git@github.com:giovani-dev/mcp-car-agent.git
    cd mcp-car-agent
    ```

2.  **Configure o ambiente:**
    Crie um arquivo `.env` na raiz do projeto com as suas configurações de banco de dados, baseando-se no arquivo `.env.example` .

3.  **Inicie a aplicação com Docker Compose:**
    ```bash
    docker-compose up --build
    ```
    Isso irá construir a imagem da aplicação e subir o serviço do banco de dados.

4.  **Execute o agente virtual:**
    ```bash
    poetry run start-agent
    ```
    (Nota: o comando pode variar dependendo da configuração exata, mas este é o passo lógico para iniciar a aplicação do terminal).

## 🧪 Padrões de Nomes para Testes
Para garantir a clareza, consistência e legibilidade de nossos testes, seguimos um conjunto de padrões de nomes que descrevem o cenário, as condições e o resultado esperado de cada teste.

### Convenções Gerais
* **Arquivos de Teste**: Devem **obrigatoriamente** começar com `test_`.
* **Classes de Teste (se aplicável)**: Devem começar com `Test` e usar `CamelCase` (ex: `TestMinhaClasse`, `TestUserAuthentication`).
* **Funções/Métodos de Teste**: Devem começar com `test_` e usar `snake_case`. O nome deve ser descritivo e indicar claramente o que está sendo testado.

### Padrão de Nomes para Arquivos de Teste
O nome do arquivo de teste deve seguir o padrão `test_<nome_do_modulo_ou_funcionalidade>_unit.py` ou `test_<nome_do_modulo_ou_funcionalidade>_integration.py`. Isso ajuda a identificar rapidamente qual parte do sistema está sendo testada e o tipo de teste (unitário ou de integração).

* **Para testes unitários**: `test_<nome_do_modulo_ou_funcionalidade>_unit.py`
    * Exemplo: `test_user_service_unit.py` (testa a unidade `UserService`)
* **Para testes de integração**: `test_<nome_do_modulo_ou_funcionalidade>_integration.py`
    * Exemplo: `test_api_auth_integration.py` (testa a integração da autenticação da API)

### Padrões Descritivos para Nomes de Funções de Teste
Adotamos a seguinte estrutura para os nomes das funções de teste, que visa contar uma "história" clara sobre o comportamento testado: `test_<condição_ou_característica_da_entrada>_<ação_ou_contexto>_<resultado_esperado>`.

* **Exemplos (em Português):**
    * `test_quando_dados_validos_entao_tarefa_e_criada_com_sucesso`
    * `test_quando_descricao_vazia_entao_erro_de_validacao_e_retornado`

### Padrão de Docstring para Casos de Teste
Cada função/método de teste deve incluir uma docstring para fornecer uma descrição mais detalhada e explicitar o propósito do teste. [cite_start]A docstring deve focar no "Porquê" do teste, complementando o "O Quê" do nome da função[cite: 121, 122].

## 📹 Vídeo de Demonstração
[cite_start]Um vídeo mostrando a aplicação em funcionamento, com a interação do agente virtual e a exibição dos resultados para pelo menos alguns casos diferentes, é uma parte crucial da entrega[cite: 149].