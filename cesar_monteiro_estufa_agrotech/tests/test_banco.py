from cesar_monteiro_estufa_agrotech.banco import calcular_desconto, dividir
import pytest
import sys


def test_saldo(conta_vazia):
    """Testa a função de verificação de saldo"""
    res = conta_vazia.saldo
    assert res == 0.0

def test_saldo_com_saldo_inicial(conta_com_saldo):
    """Testa a função de verificação de saldo"""
    res = conta_com_saldo.saldo
    assert res == 100.0

def test_depositar(conta_vazia):
    """Testa a função de depoósito"""
    res = conta_vazia.depositar(50.0)
    assert res == 50.0
    
def test_sacar_invalido(conta_com_saldo):
    """Testa a função de saque com valor inválido"""
    with pytest.raises(Exception):
        conta_com_saldo.sacar(-10.0)

def test_sacar_saldo_insuficiente(conta_com_saldo):
    """Testa a função de saque com saldo insuficiente"""
    with pytest.raises(Exception):
        conta_com_saldo.sacar(200.0)
        
def test_transferir(conta_com_saldo, conta_vazia):
    """Testa a função de transferência bancária"""
    conta_com_saldo.transferir(conta_vazia, 50.0)
    assert conta_com_saldo.saldo == 50.0
    assert conta_vazia.saldo == 50.0
def test_dividir():
    """Testa a função de divisão"""
    res = dividir(10, 2)
    assert res == 5.0    

def test_dividir_por_zero():
    """Testa a função de divisão por zero"""
    with pytest.raises(ZeroDivisionError):
        dividir(10, 0)
        
def test_calcular_desconto():
    """Testa a função de cálculo de desconto"""
    res = calcular_desconto(100.0, 10.0)
    assert res == 90.0
    
def test_calcular_desconto_percentual_invalido():
    """Testa a função de cálculo de desconto com percentual inválido"""
    with pytest.raises(Exception):
        calcular_desconto(100.0, 110.0)                             