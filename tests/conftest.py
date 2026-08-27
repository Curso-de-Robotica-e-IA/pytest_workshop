import pytest
import sys
import platform
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from ygor_matos_estufa_agrotech.app_banco import ContaBancaria
@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")

@pytest.fixture
def conta():
    return ContaBancaria('Ygor',1000000)

@pytest.fixture
def outra_conta():
    return ContaBancaria("Ygor2",500)