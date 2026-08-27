import pytest
from src.danilo_monteiro_estufa_agrotech.app import EstufaAgrotech
from src.danilo_monteiro_estufa_agrotech.banco import ContaBancaria, ValorInvalidoError, SaldoInsuficienteError

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
    objeto = EstufaAgrotech()
    return objeto

@pytest.fixture
def banco():
    objeto = ContaBancaria("Danilo")
    return objeto

@pytest.fixture
def valorInvalido():
    objeto = ValorInvalidoError()
    return objeto

