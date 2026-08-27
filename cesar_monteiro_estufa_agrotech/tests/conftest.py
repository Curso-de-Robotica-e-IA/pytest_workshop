import pytest

#from pkg.banco import ContaBancaria
from src.cesar_monteiro_estufa_agrotech.app import EstufaAgrotech

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
    instancia = EstufaAgrotech()
    return instancia




# @pytest.fixture
# def conta_vazia() -> ContaBancaria:
#     """Retorna uma conta recem-criada, sem saldo."""
#     return ContaBancaria(titular="Fulano de Tal", saldo_inicial=0.0)


# @pytest.fixture
# def conta_com_saldo() -> ContaBancaria:
#     """Retorna uma conta ja com saldo de R$ 100,00."""
#     return ContaBancaria(titular="Ciclana da Silva", saldo_inicial=100.0)


# @pytest.fixture
# def outra_conta_com_saldo() -> ContaBancaria:
#     """Uma segunda conta, util para testar transferencias entre contas."""
#     return ContaBancaria(titular="Beltrano Souza", saldo_inicial=50.0)