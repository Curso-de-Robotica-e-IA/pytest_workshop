import pytest
from src.lucas_tenorio_ferraz_estufa_agrotech.app import EstufaAgrotech

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def est():
   instancia = EstufaAgrotech()
   return instancia
