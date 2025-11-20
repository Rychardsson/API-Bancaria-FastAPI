"""
Sistema de autenticação JWT
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from models import TokenData

# Configurações de segurança
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  # Em produção, use variável de ambiente
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Contexto para hash de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha fornecida corresponde ao hash
    
    Args:
        senha_plana: Senha em texto plano
        senha_hash: Hash da senha armazenada
        
    Returns:
        bool: True se a senha corresponde, False caso contrário
    """
    return pwd_context.verify(senha_plana, senha_hash)


def obter_hash_senha(senha: str) -> str:
    """
    Gera hash de uma senha
    
    Args:
        senha: Senha em texto plano
        
    Returns:
        str: Hash da senha
    """
    return pwd_context.hash(senha)


def criar_token_acesso(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria um token JWT de acesso
    
    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração do token
        
    Returns:
        str: Token JWT codificado
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def obter_usuario_atual(token: str = Depends(oauth2_scheme)) -> str:
    """
    Obtém o usuário atual a partir do token JWT
    
    Args:
        token: Token JWT do header Authorization
        
    Returns:
        str: CPF do usuário autenticado
        
    Raises:
        HTTPException: Se o token for inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        if cpf is None:
            raise credentials_exception
        token_data = TokenData(cpf=cpf)
    except JWTError:
        raise credentials_exception
    
    return token_data.cpf


def validar_token(token: str) -> Optional[str]:
    """
    Valida um token JWT e retorna o CPF do usuário
    
    Args:
        token: Token JWT
        
    Returns:
        Optional[str]: CPF do usuário se válido, None caso contrário
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        cpf: str = payload.get("sub")
        return cpf
    except JWTError:
        return None
