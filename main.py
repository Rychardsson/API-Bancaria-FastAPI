"""
API Bancária com FastAPI
Gerenciamento de contas e transações bancárias com autenticação JWT
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from datetime import timedelta

from models import (
    Usuario, UsuarioCreate,
    Conta, ContaCreate,
    Transacao, TransacaoCreate,
    Extrato, Token, TipoTransacao
)
from auth import (
    verificar_senha, obter_hash_senha, criar_token_acesso,
    obter_usuario_atual
)
from database import db
from config import settings

# Inicialização da aplicação FastAPI
app = FastAPI(
    title=settings.API_TITLE,
    description=settings.API_DESCRIPTION,
    version=settings.API_VERSION,
    contact={
        "name": "Rychardsson",
        "url": "https://github.com/Rychardsson/API-Bancaria-FastAPI",
    },
    license_info={
        "name": "MIT",
    },
)


# ==================== ENDPOINTS DE USUÁRIO ====================

@app.post(
    "/usuarios/",
    response_model=Usuario,
    status_code=status.HTTP_201_CREATED,
    tags=["Usuários"],
    summary="Criar novo usuário",
    description="Cria um novo usuário no sistema. O CPF deve ser único."
)
async def criar_usuario(usuario: UsuarioCreate):
    """
    Cria um novo usuário:
    
    - **nome**: Nome completo do usuário (mínimo 3 caracteres)
    - **cpf**: CPF com 11 dígitos (apenas números)
    - **senha**: Senha do usuário (mínimo 6 caracteres)
    """
    try:
        senha_hash = obter_hash_senha(usuario.senha)
        usuario_criado = db.criar_usuario(
            nome=usuario.nome,
            cpf=usuario.cpf,
            senha_hash=senha_hash
        )
        return Usuario(
            id=usuario_criado["id"],
            nome=usuario_criado["nome"],
            cpf=usuario_criado["cpf"]
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


# ==================== ENDPOINTS DE AUTENTICAÇÃO ====================

@app.post(
    "/login/",
    response_model=Token,
    tags=["Autenticação"],
    summary="Fazer login",
    description="Autentica um usuário e retorna um token JWT"
)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Autentica um usuário e retorna um token JWT:
    
    - **username**: CPF do usuário
    - **password**: Senha do usuário
    
    Retorna um token de acesso que deve ser usado no header Authorization
    como "Bearer {token}" para endpoints protegidos.
    """
    usuario = db.obter_usuario_por_cpf(form_data.username)
    
    if not usuario or not verificar_senha(form_data.password, usuario["senha_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="CPF ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_token_acesso(
        data={"sub": usuario["cpf"]},
        expires_delta=access_token_expires
    )
    
    return Token(access_token=access_token, token_type="bearer")


# ==================== ENDPOINTS DE CONTA ====================

@app.post(
    "/contas/",
    response_model=Conta,
    status_code=status.HTTP_201_CREATED,
    tags=["Contas"],
    summary="Criar nova conta",
    description="Cria uma nova conta corrente para o usuário autenticado"
)
async def criar_conta(
    conta: ContaCreate,
    cpf_atual: str = Depends(obter_usuario_atual)
):
    """
    Cria uma nova conta para o usuário autenticado:
    
    - **tipo_conta**: Tipo da conta (corrente ou poupanca)
    
    Cada usuário pode ter apenas uma conta.
    """
    usuario = db.obter_usuario_por_cpf(cpf_atual)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    try:
        conta_criada = db.criar_conta(
            usuario_id=usuario["id"],
            tipo_conta=conta.tipo_conta
        )
        return Conta(**conta_criada)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get(
    "/contas/me",
    response_model=Conta,
    tags=["Contas"],
    summary="Obter dados da conta",
    description="Retorna os dados da conta do usuário autenticado"
)
async def obter_minha_conta(cpf_atual: str = Depends(obter_usuario_atual)):
    """
    Retorna os dados da conta do usuário autenticado, incluindo:
    
    - Número da conta
    - Saldo atual
    - Tipo de conta
    - Data de criação
    """
    usuario = db.obter_usuario_por_cpf(cpf_atual)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    conta = db.obter_conta_por_usuario(usuario["id"])
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada. Crie uma conta primeiro."
        )
    
    return Conta(**conta)


# ==================== ENDPOINTS DE TRANSAÇÕES ====================

@app.post(
    "/transacoes/deposito",
    response_model=Transacao,
    status_code=status.HTTP_201_CREATED,
    tags=["Transações"],
    summary="Realizar depósito",
    description="Realiza um depósito na conta do usuário autenticado"
)
async def realizar_deposito(
    transacao: TransacaoCreate,
    cpf_atual: str = Depends(obter_usuario_atual)
):
    """
    Realiza um depósito na conta do usuário autenticado:
    
    - **valor**: Valor do depósito (deve ser positivo)
    - **descricao**: Descrição opcional da transação
    
    O valor não pode ser negativo ou zero.
    """
    usuario = db.obter_usuario_por_cpf(cpf_atual)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    conta = db.obter_conta_por_usuario(usuario["id"])
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada. Crie uma conta primeiro."
        )
    
    try:
        transacao_criada = db.criar_transacao(
            conta_id=conta["id"],
            tipo=TipoTransacao.DEPOSITO,
            valor=transacao.valor,
            descricao=transacao.descricao
        )
        return Transacao(**transacao_criada)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.post(
    "/transacoes/saque",
    response_model=Transacao,
    status_code=status.HTTP_201_CREATED,
    tags=["Transações"],
    summary="Realizar saque",
    description="Realiza um saque da conta do usuário autenticado"
)
async def realizar_saque(
    transacao: TransacaoCreate,
    cpf_atual: str = Depends(obter_usuario_atual)
):
    """
    Realiza um saque da conta do usuário autenticado:
    
    - **valor**: Valor do saque (deve ser positivo)
    - **descricao**: Descrição opcional da transação
    
    Validações aplicadas:
    - O valor não pode ser negativo ou zero
    - O saldo da conta deve ser suficiente para o saque
    """
    usuario = db.obter_usuario_por_cpf(cpf_atual)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    conta = db.obter_conta_por_usuario(usuario["id"])
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada. Crie uma conta primeiro."
        )
    
    try:
        transacao_criada = db.criar_transacao(
            conta_id=conta["id"],
            tipo=TipoTransacao.SAQUE,
            valor=transacao.valor,
            descricao=transacao.descricao
        )
        return Transacao(**transacao_criada)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@app.get(
    "/transacoes/extrato",
    response_model=Extrato,
    tags=["Transações"],
    summary="Obter extrato",
    description="Retorna o extrato completo da conta do usuário autenticado"
)
async def obter_extrato(cpf_atual: str = Depends(obter_usuario_atual)):
    """
    Retorna o extrato completo da conta do usuário autenticado:
    
    - Lista de todas as transações (depósitos e saques)
    - Dados da conta (saldo, número, etc)
    - Estatísticas (total de depósitos, saques e quantidade de transações)
    
    As transações são retornadas em ordem cronológica.
    """
    usuario = db.obter_usuario_por_cpf(cpf_atual)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado"
        )
    
    conta = db.obter_conta_por_usuario(usuario["id"])
    if not conta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conta não encontrada. Crie uma conta primeiro."
        )
    
    transacoes = db.obter_transacoes_por_conta(conta["id"])
    estatisticas = db.obter_estatisticas_conta(conta["id"])
    
    return Extrato(
        conta=Conta(**conta),
        transacoes=[Transacao(**t) for t in transacoes],
        total_depositos=estatisticas["total_depositos"],
        total_saques=estatisticas["total_saques"],
        quantidade_transacoes=estatisticas["quantidade_transacoes"]
    )


# ==================== ENDPOINT RAIZ ====================

@app.get(
    "/",
    tags=["Sistema"],
    summary="Informações da API",
    description="Retorna informações básicas sobre a API"
)
async def raiz():
    """
    Endpoint raiz que retorna informações sobre a API e links úteis.
    """
    return {
        "mensagem": "API Bancária - FastAPI",
        "versao": "1.0.0",
        "documentacao": {
            "swagger": "/docs",
            "redoc": "/redoc"
        },
        "endpoints_principais": {
            "criar_usuario": "POST /usuarios/",
            "login": "POST /login/",
            "criar_conta": "POST /contas/",
            "deposito": "POST /transacoes/deposito",
            "saque": "POST /transacoes/saque",
            "extrato": "GET /transacoes/extrato"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
