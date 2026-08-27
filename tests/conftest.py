import pytest
from src.matheus_passos_estufa_agrotech.app import *
from src.matheus_passos_estufa_agrotech.banco import *

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")


@pytest.fixture
def create_agrotech():
    return EstufaAgrotech() #Uses default values


@pytest.fixture
def create_bank_acc():
    #Creates a bank acc using default values.
    bank_acc = ContaBancaria("acc_owner", 50.0)
    return bank_acc
