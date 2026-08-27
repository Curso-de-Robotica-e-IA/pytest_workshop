import pytest
from src.renan_vanbasten_estufa_agrotech.app import EstufaAgrotech, ServicoLogger
from src.renan_vanbasten_estufa_agrotech.banco import ContaBancaria, SaldoInsuficienteError, ValorInvalidoError


@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():

    instance = EstufaAgrotech()
    return instance


@pytest.fixture
def logger(log_temporario):

    log = ServicoLogger(log_temporario)
    return log

@pytest.fixture
def conta_banco_com_saldo():
    instancia = ContaBancaria(titular = "Maria", saldo_inicial = 100.00)
    return instancia

@pytest.fixture
def conta_banco_sem_saldo():
    instancia = ContaBancaria(titular = "Renan", saldo_inicial = 0.0)
    return instancia

@pytest.fixture
def conta_banco_destino():
    instancia = ContaBancaria(titular = "Amado", saldo_inicial= 100.0)
    return instancia