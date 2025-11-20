"""
Script de teste e demonstração da API Bancária
Execute este script após iniciar a API para ver todos os endpoints em ação
"""
import requests
import json
from time import sleep

BASE_URL = "http://localhost:8000"

def print_section(title):
    """Imprime uma seção formatada"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def print_response(response):
    """Imprime a resposta formatada"""
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")

def main():
    print_section("TESTANDO API BANCÁRIA")
    
    # 1. Criar usuário
    print_section("1. CRIANDO USUÁRIO")
    usuario_data = {
        "nome": "João da Silva",
        "cpf": "12345678900",
        "senha": "senha123"
    }
    response = requests.post(f"{BASE_URL}/usuarios/", json=usuario_data)
    print_response(response)
    
    sleep(1)
    
    # 2. Fazer login
    print_section("2. FAZENDO LOGIN")
    login_data = {
        "username": "12345678900",
        "password": "senha123"
    }
    response = requests.post(f"{BASE_URL}/login/", data=login_data)
    print_response(response)
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        
        sleep(1)
        
        # 3. Criar conta
        print_section("3. CRIANDO CONTA CORRENTE")
        conta_data = {"tipo_conta": "corrente"}
        response = requests.post(f"{BASE_URL}/contas/", json=conta_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 4. Verificar dados da conta
        print_section("4. VERIFICANDO DADOS DA CONTA")
        response = requests.get(f"{BASE_URL}/contas/me", headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 5. Fazer depósito
        print_section("5. FAZENDO DEPÓSITO DE R$ 1000,00")
        deposito_data = {
            "valor": 1000.00,
            "descricao": "Depósito inicial"
        }
        response = requests.post(f"{BASE_URL}/transacoes/deposito", json=deposito_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 6. Fazer outro depósito
        print_section("6. FAZENDO DEPÓSITO DE R$ 500,00")
        deposito_data = {
            "valor": 500.00,
            "descricao": "Segundo depósito"
        }
        response = requests.post(f"{BASE_URL}/transacoes/deposito", json=deposito_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 7. Fazer saque
        print_section("7. FAZENDO SAQUE DE R$ 200,00")
        saque_data = {
            "valor": 200.00,
            "descricao": "Saque para compras"
        }
        response = requests.post(f"{BASE_URL}/transacoes/saque", json=saque_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 8. Tentar saque com valor negativo
        print_section("8. TENTANDO SAQUE COM VALOR NEGATIVO (DEVE FALHAR)")
        saque_data = {
            "valor": -50.00,
            "descricao": "Teste valor negativo"
        }
        response = requests.post(f"{BASE_URL}/transacoes/saque", json=saque_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 9. Tentar saque sem saldo
        print_section("9. TENTANDO SAQUE SEM SALDO (DEVE FALHAR)")
        saque_data = {
            "valor": 5000.00,
            "descricao": "Teste saldo insuficiente"
        }
        response = requests.post(f"{BASE_URL}/transacoes/saque", json=saque_data, headers=headers)
        print_response(response)
        
        sleep(1)
        
        # 10. Ver extrato completo
        print_section("10. VISUALIZANDO EXTRATO COMPLETO")
        response = requests.get(f"{BASE_URL}/transacoes/extrato", headers=headers)
        print_response(response)
    
    print_section("TESTES CONCLUÍDOS")

if __name__ == "__main__":
    print("\n🚀 Certifique-se de que a API está rodando em http://localhost:8000")
    print("   Execute: uvicorn main:app --reload")
    input("\nPressione ENTER para iniciar os testes...")
    
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERRO: Não foi possível conectar à API.")
        print("   Certifique-se de que a API está rodando!")
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
