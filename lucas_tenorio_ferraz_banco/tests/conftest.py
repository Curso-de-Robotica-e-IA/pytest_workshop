import pytest
from src.lucas_tenorio_ferraz_banco.banco import *

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "banco_status.log")

@pytest.fixture
def bank():
   instancia = ContaBancaria("Empty")
   return instancia

@pytest.fixture
def fail_bank():
   instancia = ContaBancaria("Fail",-293.65)
   return instancia

@pytest.fixture
def bank2():
   instancia = ContaBancaria("Account",572.35)
   return instancia

@pytest.fixture
def fun_dividir():
   return dividir

@pytest.fixture
def fun_calcular_desconto():
   return calcular_desconto

@pytest.fixture
def fun_convert_para_dolar():
   return converter_reais_para_dolar

@pytest.fixture
def fun_cotarDolar():
   return buscar_cotacao_dolar

@pytest.fixture
def fun_juros_comp():
   return calcular_juros_composto

@pytest.fixture
def fun_debug():
   return esta_em_modo_debug