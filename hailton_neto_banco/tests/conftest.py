# conftest.py
import pytest
from src.hailton_neto_banco.app import (
    ContaBancaria, 
    ValorInvalidoError, 
    SaldoInsuficienteError,
)

@pytest.fixture
def conta_bancaria():
    return ContaBancaria()

@pytest.fixture
def valor_invalido():
    return ValorInvalidoError

@pytest.fixture
def saldo_insuficiente():
    return SaldoInsuficienteError