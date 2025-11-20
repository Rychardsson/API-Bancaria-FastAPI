"""
Arquivo de configuração centralizado
"""
import os
from typing import Optional

class Settings:
    """Configurações da aplicação"""
    
    # Segurança
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY",
        "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )
    
    # Servidor
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    
    # Ambiente
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = ENVIRONMENT == "development"
    
    # API
    API_TITLE: str = "API Bancária"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = """
    API RESTful para gerenciamento de operações bancárias com autenticação JWT.
    
    ## Funcionalidades
    
    * **Usuários**: Criar e autenticar usuários
    * **Contas**: Criar e gerenciar contas correntes
    * **Transações**: Realizar depósitos e saques
    * **Extrato**: Visualizar histórico de transações
    
    ## Autenticação
    
    Esta API usa JWT (JSON Web Tokens) para autenticação.
    Para acessar endpoints protegidos:
    
    1. Crie um usuário em `/usuarios/`
    2. Faça login em `/login/` para obter o token
    3. Use o token no header: `Authorization: Bearer {token}`
    """

settings = Settings()
