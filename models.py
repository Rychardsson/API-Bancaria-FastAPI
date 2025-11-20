"""
Modelos de dados para a API Bancária
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class TipoTransacao(str, Enum):
    """Tipos de transação bancária"""
    DEPOSITO = "deposito"
    SAQUE = "saque"


class TipoConta(str, Enum):
    """Tipos de conta bancária"""
    CORRENTE = "corrente"
    POUPANCA = "poupanca"


# Schemas de Usuário
class UsuarioBase(BaseModel):
    """Schema base para usuário"""
    nome: str = Field(..., description="Nome completo do usuário", min_length=3)
    cpf: str = Field(..., description="CPF do usuário (apenas números)", min_length=11, max_length=11)
    
    @validator('cpf')
    def validar_cpf(cls, v):
        """Valida se CPF contém apenas números"""
        if not v.isdigit():
            raise ValueError('CPF deve conter apenas números')
        return v


class UsuarioCreate(UsuarioBase):
    """Schema para criação de usuário"""
    senha: str = Field(..., description="Senha do usuário", min_length=6)


class Usuario(UsuarioBase):
    """Schema de resposta de usuário"""
    id: int
    
    class Config:
        from_attributes = True


# Schemas de Conta
class ContaBase(BaseModel):
    """Schema base para conta"""
    tipo_conta: TipoConta = Field(default=TipoConta.CORRENTE, description="Tipo da conta bancária")


class ContaCreate(ContaBase):
    """Schema para criação de conta"""
    pass


class Conta(ContaBase):
    """Schema de resposta de conta"""
    id: int
    numero_conta: str = Field(..., description="Número único da conta")
    saldo: float = Field(default=0.0, description="Saldo atual da conta")
    usuario_id: int
    data_criacao: datetime
    
    class Config:
        from_attributes = True


# Schemas de Transação
class TransacaoBase(BaseModel):
    """Schema base para transação"""
    valor: float = Field(..., description="Valor da transação", gt=0)
    descricao: Optional[str] = Field(None, description="Descrição da transação", max_length=200)
    
    @validator('valor')
    def validar_valor_positivo(cls, v):
        """Valida se o valor é positivo"""
        if v <= 0:
            raise ValueError('O valor da transação deve ser positivo')
        return round(v, 2)


class TransacaoCreate(TransacaoBase):
    """Schema para criação de transação"""
    pass


class Transacao(TransacaoBase):
    """Schema de resposta de transação"""
    id: int
    tipo: TipoTransacao
    conta_id: int
    data_transacao: datetime
    saldo_anterior: float = Field(..., description="Saldo antes da transação")
    saldo_posterior: float = Field(..., description="Saldo após a transação")
    
    class Config:
        from_attributes = True


# Schema de Extrato
class Extrato(BaseModel):
    """Schema para extrato bancário"""
    conta: Conta
    transacoes: List[Transacao]
    total_depositos: float = Field(..., description="Total de depósitos realizados")
    total_saques: float = Field(..., description="Total de saques realizados")
    quantidade_transacoes: int = Field(..., description="Quantidade total de transações")


# Schemas de Autenticação
class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Schema para dados do token"""
    cpf: Optional[str] = None


class LoginRequest(BaseModel):
    """Schema para requisição de login"""
    username: str = Field(..., description="CPF do usuário")
    password: str = Field(..., description="Senha do usuário")
