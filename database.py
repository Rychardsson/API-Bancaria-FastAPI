"""
Simulação de banco de dados em memória
Em produção, substitua por SQLAlchemy com PostgreSQL/MySQL
"""
from typing import Dict, List, Optional
from datetime import datetime
from models import TipoTransacao, TipoConta
import random
import string


class DatabaseSimulator:
    """Simulador de banco de dados em memória"""
    
    def __init__(self):
        # Armazenamento em memória
        self.usuarios: Dict[int, dict] = {}
        self.contas: Dict[int, dict] = {}
        self.transacoes: Dict[int, dict] = {}
        
        # Contadores de IDs
        self.usuario_id_counter = 1
        self.conta_id_counter = 1
        self.transacao_id_counter = 1
        
        # Índices para buscas rápidas
        self.cpf_to_usuario_id: Dict[str, int] = {}
        self.usuario_id_to_conta_id: Dict[int, int] = {}
        self.conta_id_to_transacoes: Dict[int, List[int]] = {}
    
    def gerar_numero_conta(self) -> str:
        """Gera um número de conta único"""
        agencia = "0001"
        numero = str(self.conta_id_counter).zfill(6)
        digito = random.randint(0, 9)
        return f"{agencia}-{numero}-{digito}"
    
    # Operações de Usuário
    def criar_usuario(self, nome: str, cpf: str, senha_hash: str) -> dict:
        """Cria um novo usuário"""
        if cpf in self.cpf_to_usuario_id:
            raise ValueError("CPF já cadastrado")
        
        usuario_id = self.usuario_id_counter
        self.usuario_id_counter += 1
        
        usuario = {
            "id": usuario_id,
            "nome": nome,
            "cpf": cpf,
            "senha_hash": senha_hash,
            "data_criacao": datetime.now()
        }
        
        self.usuarios[usuario_id] = usuario
        self.cpf_to_usuario_id[cpf] = usuario_id
        
        return usuario
    
    def obter_usuario_por_cpf(self, cpf: str) -> Optional[dict]:
        """Obtém usuário por CPF"""
        usuario_id = self.cpf_to_usuario_id.get(cpf)
        if usuario_id:
            return self.usuarios.get(usuario_id)
        return None
    
    def obter_usuario_por_id(self, usuario_id: int) -> Optional[dict]:
        """Obtém usuário por ID"""
        return self.usuarios.get(usuario_id)
    
    # Operações de Conta
    def criar_conta(self, usuario_id: int, tipo_conta: TipoConta) -> dict:
        """Cria uma nova conta para um usuário"""
        if usuario_id not in self.usuarios:
            raise ValueError("Usuário não encontrado")
        
        if usuario_id in self.usuario_id_to_conta_id:
            raise ValueError("Usuário já possui uma conta")
        
        conta_id = self.conta_id_counter
        self.conta_id_counter += 1
        
        conta = {
            "id": conta_id,
            "numero_conta": self.gerar_numero_conta(),
            "tipo_conta": tipo_conta.value,
            "saldo": 0.0,
            "usuario_id": usuario_id,
            "data_criacao": datetime.now()
        }
        
        self.contas[conta_id] = conta
        self.usuario_id_to_conta_id[usuario_id] = conta_id
        self.conta_id_to_transacoes[conta_id] = []
        
        return conta
    
    def obter_conta_por_usuario(self, usuario_id: int) -> Optional[dict]:
        """Obtém a conta de um usuário"""
        conta_id = self.usuario_id_to_conta_id.get(usuario_id)
        if conta_id:
            return self.contas.get(conta_id)
        return None
    
    def obter_conta_por_id(self, conta_id: int) -> Optional[dict]:
        """Obtém conta por ID"""
        return self.contas.get(conta_id)
    
    def atualizar_saldo(self, conta_id: int, novo_saldo: float):
        """Atualiza o saldo de uma conta"""
        if conta_id in self.contas:
            self.contas[conta_id]["saldo"] = round(novo_saldo, 2)
    
    # Operações de Transação
    def criar_transacao(
        self,
        conta_id: int,
        tipo: TipoTransacao,
        valor: float,
        descricao: Optional[str] = None
    ) -> dict:
        """Cria uma nova transação"""
        conta = self.obter_conta_por_id(conta_id)
        if not conta:
            raise ValueError("Conta não encontrada")
        
        saldo_anterior = conta["saldo"]
        
        # Valida e calcula novo saldo
        if tipo == TipoTransacao.SAQUE:
            if saldo_anterior < valor:
                raise ValueError("Saldo insuficiente para realizar o saque")
            saldo_posterior = saldo_anterior - valor
        else:  # DEPOSITO
            saldo_posterior = saldo_anterior + valor
        
        # Cria a transação
        transacao_id = self.transacao_id_counter
        self.transacao_id_counter += 1
        
        transacao = {
            "id": transacao_id,
            "conta_id": conta_id,
            "tipo": tipo.value,
            "valor": round(valor, 2),
            "descricao": descricao,
            "saldo_anterior": round(saldo_anterior, 2),
            "saldo_posterior": round(saldo_posterior, 2),
            "data_transacao": datetime.now()
        }
        
        self.transacoes[transacao_id] = transacao
        self.conta_id_to_transacoes[conta_id].append(transacao_id)
        
        # Atualiza o saldo da conta
        self.atualizar_saldo(conta_id, saldo_posterior)
        
        return transacao
    
    def obter_transacoes_por_conta(self, conta_id: int) -> List[dict]:
        """Obtém todas as transações de uma conta"""
        transacao_ids = self.conta_id_to_transacoes.get(conta_id, [])
        return [self.transacoes[tid] for tid in transacao_ids]
    
    def obter_estatisticas_conta(self, conta_id: int) -> dict:
        """Calcula estatísticas das transações de uma conta"""
        transacoes = self.obter_transacoes_por_conta(conta_id)
        
        total_depositos = sum(
            t["valor"] for t in transacoes if t["tipo"] == TipoTransacao.DEPOSITO.value
        )
        total_saques = sum(
            t["valor"] for t in transacoes if t["tipo"] == TipoTransacao.SAQUE.value
        )
        
        return {
            "total_depositos": round(total_depositos, 2),
            "total_saques": round(total_saques, 2),
            "quantidade_transacoes": len(transacoes)
        }


# Instância global do banco de dados
db = DatabaseSimulator()
