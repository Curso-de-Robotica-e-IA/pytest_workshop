import pytest
from src.renan_vanbasten_estufa_agrotech.app import EstufaAgrotech, ServicoLogger


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