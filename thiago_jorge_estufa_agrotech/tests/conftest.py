import pytest
from src.thiago_jorge_estufa_agrotech.app import EstufaAgrotech, ServicoLogger

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
    instancia = EstufaAgrotech()
    return instancia

@pytest.fixture
def logger():
    instancia = ServicoLogger()
    return instancia