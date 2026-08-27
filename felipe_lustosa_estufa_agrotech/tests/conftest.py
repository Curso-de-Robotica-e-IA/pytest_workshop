import pytest
from src.felipe_lustosa_estufa_agrotech.app import EstufaAgrotech
from src.felipe_lustosa_estufa_agrotech.banco import ContaBancaria, ValorInvalidoError

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def estufa():
# Setup do objeto
   instancia = EstufaAgrotech()
   return instancia

@pytest.fixture
def banco():
# Setup do objeto
   instancia = ContaBancaria("João")
   return instancia

@pytest.fixture
def valor_invalido():
# Setup do objeto
   instancia = ValorInvalidoError()
   return instancia