# Exemplos de Uso da API

Este arquivo contém exemplos práticos de como usar todos os endpoints da API.

## Pré-requisitos

A API deve estar rodando em `http://localhost:8000`:
```bash
uvicorn main:app --reload
```

## 1. Criar Usuário

```bash
curl -X POST "http://localhost:8000/usuarios/" \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "João da Silva",
    "cpf": "12345678900",
    "senha": "senha123"
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "nome": "João da Silva",
  "cpf": "12345678900"
}
```

## 2. Fazer Login

```bash
curl -X POST "http://localhost:8000/login/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=12345678900&password=senha123"
```

**Resposta esperada:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**⚠️ Importante:** Salve o `access_token` para usar nos próximos passos!

## 3. Criar Conta Corrente

```bash
curl -X POST "http://localhost:8000/contas/" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "tipo_conta": "corrente"
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "numero_conta": "0001-000001-5",
  "tipo_conta": "corrente",
  "saldo": 0.0,
  "usuario_id": 1,
  "data_criacao": "2025-11-19T10:30:00"
}
```

## 4. Consultar Minha Conta

```bash
curl -X GET "http://localhost:8000/contas/me" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 5. Fazer Depósito

```bash
curl -X POST "http://localhost:8000/transacoes/deposito" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 1000.00,
    "descricao": "Depósito inicial"
  }'
```

**Resposta esperada:**
```json
{
  "id": 1,
  "tipo": "deposito",
  "conta_id": 1,
  "valor": 1000.0,
  "descricao": "Depósito inicial",
  "saldo_anterior": 0.0,
  "saldo_posterior": 1000.0,
  "data_transacao": "2025-11-19T10:35:00"
}
```

## 6. Fazer Saque

```bash
curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 200.00,
    "descricao": "Saque para compras"
  }'
```

**Resposta esperada:**
```json
{
  "id": 2,
  "tipo": "saque",
  "conta_id": 1,
  "valor": 200.0,
  "descricao": "Saque para compras",
  "saldo_anterior": 1000.0,
  "saldo_posterior": 800.0,
  "data_transacao": "2025-11-19T10:40:00"
}
```

## 7. Ver Extrato

```bash
curl -X GET "http://localhost:8000/transacoes/extrato" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

**Resposta esperada:**
```json
{
  "conta": {
    "id": 1,
    "numero_conta": "0001-000001-5",
    "tipo_conta": "corrente",
    "saldo": 800.0,
    "usuario_id": 1,
    "data_criacao": "2025-11-19T10:30:00"
  },
  "transacoes": [
    {
      "id": 1,
      "tipo": "deposito",
      "valor": 1000.0,
      "descricao": "Depósito inicial",
      "saldo_anterior": 0.0,
      "saldo_posterior": 1000.0,
      "data_transacao": "2025-11-19T10:35:00"
    },
    {
      "id": 2,
      "tipo": "saque",
      "valor": 200.0,
      "descricao": "Saque para compras",
      "saldo_anterior": 1000.0,
      "saldo_posterior": 800.0,
      "data_transacao": "2025-11-19T10:40:00"
    }
  ],
  "total_depositos": 1000.0,
  "total_saques": 200.0,
  "quantidade_transacoes": 2
}
```

## 8. Testando Validações

### Tentativa de saque com valor negativo (ERRO)
```bash
curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": -100.00,
    "descricao": "Teste valor negativo"
  }'
```

**Resposta esperada (400 Bad Request):**
```json
{
  "detail": [
    {
      "loc": ["body", "valor"],
      "msg": "O valor da transação deve ser positivo",
      "type": "value_error"
    }
  ]
}
```

### Tentativa de saque sem saldo (ERRO)
```bash
curl -X POST "http://localhost:8000/transacoes/saque" \
  -H "Authorization: Bearer SEU_TOKEN_AQUI" \
  -H "Content-Type: application/json" \
  -d '{
    "valor": 10000.00,
    "descricao": "Tentativa de saque sem saldo"
  }'
```

**Resposta esperada (400 Bad Request):**
```json
{
  "detail": "Saldo insuficiente para realizar o saque"
}
```

### Tentativa de acesso sem autenticação (ERRO)
```bash
curl -X GET "http://localhost:8000/contas/me"
```

**Resposta esperada (401 Unauthorized):**
```json
{
  "detail": "Not authenticated"
}
```

## 9. Usando PowerShell (Windows)

Se estiver usando PowerShell no Windows, use este formato:

```powershell
# Criar usuário
$body = @{
    nome = "João da Silva"
    cpf = "12345678900"
    senha = "senha123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/usuarios/" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body

# Fazer login
$loginBody = @{
    username = "12345678900"
    password = "senha123"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/login/" `
  -Method POST `
  -ContentType "application/x-www-form-urlencoded" `
  -Body $loginBody

$token = $response.access_token

# Criar conta
$headers = @{
    Authorization = "Bearer $token"
}

$contaBody = @{
    tipo_conta = "corrente"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/contas/" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $contaBody

# Fazer depósito
$depositoBody = @{
    valor = 1000.00
    descricao = "Depósito inicial"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/transacoes/deposito" `
  -Method POST `
  -ContentType "application/json" `
  -Headers $headers `
  -Body $depositoBody

# Ver extrato
Invoke-RestMethod -Uri "http://localhost:8000/transacoes/extrato" `
  -Method GET `
  -Headers $headers
```

## 10. Usando Python (requests)

Você pode usar o script de teste fornecido:

```bash
pip install requests
python test_api.py
```

Ou criar seu próprio script:

```python
import requests

BASE_URL = "http://localhost:8000"

# Criar usuário
usuario = {
    "nome": "João da Silva",
    "cpf": "12345678900",
    "senha": "senha123"
}
response = requests.post(f"{BASE_URL}/usuarios/", json=usuario)
print(response.json())

# Login
login_data = {
    "username": "12345678900",
    "password": "senha123"
}
response = requests.post(f"{BASE_URL}/login/", data=login_data)
token = response.json()["access_token"]

# Headers com autenticação
headers = {"Authorization": f"Bearer {token}"}

# Criar conta
conta = {"tipo_conta": "corrente"}
response = requests.post(f"{BASE_URL}/contas/", json=conta, headers=headers)
print(response.json())

# Depósito
deposito = {"valor": 1000.00, "descricao": "Depósito inicial"}
response = requests.post(f"{BASE_URL}/transacoes/deposito", json=deposito, headers=headers)
print(response.json())

# Ver extrato
response = requests.get(f"{BASE_URL}/transacoes/extrato", headers=headers)
print(response.json())
```

## Documentação Interativa

Acesse a documentação Swagger para testar os endpoints de forma interativa:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
