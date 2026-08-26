import pytest
from src.danilo_monteiro_estufa_agrotech.app import EstufaAgrotech

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
    objeto = EstufaAgrotech()
    return objeto

