import pytest
from src.felipe_lustosa_estufa_agrotech.app import EstufaAgrotech, ServicoLogger

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
# Setup do objeto
   instancia = EstufaAgrotech()
   return instancia