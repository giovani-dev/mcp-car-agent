"""
Módulo de configuração da aplicação.

Este módulo carrega as variádveis de ambiente a partir do arquivo `.env`,
centralizando todas as configurações essenciais para a aplicação.
Isso inclui credenciais de banco de dados, chaves de API e configurações
de serviços externos como Redis.
"""

import os

from dotenv import load_dotenv

load_dotenv()


DB_ENGINE = os.getenv("DB_ENGINE")
"""
Motor do banco de dados a ser utilizado (ex: 'POSTGRESQL').
"""

DB_USER = os.getenv("DB_USER")
"""
Nome de usuário para o banco de dados.
"""
DB_PWD = os.getenv("DB_PWD")
"""
Senha para o banco de dados.
"""
DB_HOST = os.getenv("DB_HOST")
"""
Host do servidor do banco de dados.
"""
DB_PORT = os.getenv("DB_PORT")
"""
Porta do servidor do banco de dados.
"""
DB_NAME = os.getenv("DB_NAME")
"""
Nome do banco de dados.
"""
