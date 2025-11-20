# API Bancária com FastAPI

API RESTful assíncrona para gerenciamento de operações bancárias (depósitos e saques) com autenticação JWT.

## Funcionalidades

- ✅ Cadastro e autenticação de usuários
- ✅ Criação de contas correntes
- ✅ Depósitos e saques
- ✅ Extrato de transações
- ✅ Autenticação JWT
- ✅ Validações de negócio (valores negativos, saldo insuficiente)
- ✅ Documentação automática OpenAPI/Swagger

## Tecnologias

- **FastAPI**: Framework web assíncrono
- **Pydantic**: Validação de dados
- **JWT**: Autenticação segura
- **Uvicorn**: Servidor ASGI

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/Rychardsson/API-Bancaria-FastAPI.git
cd API-Bancaria-FastAPI
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## Executando a aplicação

```bash
uvicorn main:app --reload
```

A API estará disponível em: `http://localhost:8000`

## Documentação

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Endpoints

### Autenticação

- `POST /usuarios/` - Criar novo usuário
- `POST /login/` - Autenticar e obter token JWT

### Contas

- `POST /contas/` - Criar nova conta corrente (autenticado)
- `GET /contas/me` - Obter dados da conta do usuário autenticado

### Transações

- `POST /transacoes/deposito` - Realizar depósito (autenticado)
- `POST /transacoes/saque` - Realizar saque (autenticado)
- `GET /transacoes/extrato` - Visualizar extrato (autenticado)

## Exemplos de Uso

### 1. Criar usuário
```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{"nome":"João Silva","cpf":"12345678900","senha":"senha123"}'
```

### 2. Fazer login
```bash
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=12345678900&password=senha123"
```

### 3. Criar conta (com token)
```bash
curl -X POST "http://localhost:8000/contas/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"tipo_conta":"corrente"}'
```

### 4. Fazer depósito
```bash
curl -X POST "http://localhost:8000/transacoes/deposito" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"valor":1000.00,"descricao":"Depósito inicial"}'
```

### 5. Fazer saque
```bash
curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{"valor":100.00,"descricao":"Saque ATM"}'
```

### 6. Ver extrato
```bash
curl -X GET "http://localhost:8000/transacoes/extrato" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## Validações Implementadas

- ✅ Valores negativos em depósitos e saques
- ✅ Saque com saldo insuficiente
- ✅ CPF único por usuário
- ✅ Apenas uma conta por usuário
- ✅ Autenticação obrigatória para operações sensíveis

## Estrutura do Projeto

```
API-Bancaria-FastAPI/
├── main.py              # Aplicação principal
├── models.py            # Modelos Pydantic
├── auth.py              # Autenticação JWT
├── database.py          # Simulação de banco de dados
├── requirements.txt     # Dependências
└── README.md           # Documentação
```

## Segurança

- Senhas são hasheadas com bcrypt
- Autenticação via JWT (Bearer Token)
- Tokens expiram em 30 minutos
- Validações rigorosas em todas as operações

## Licença

MIT
