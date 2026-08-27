import pytest
from pytest_mock import mocker
from src.thiago_jorge_banco.banco import *
from datetime import datetime

def test_exception_saldo_inicial_negativo():
    """Verifica mensagem passada na exceção ValorInvalidoError, para checar se a conta 
    foi instanciada foi iniciada com saldo negativo"""
    with pytest.raises(ValorInvalidoError, match="Saldo inicial nao pode ser negativo."):
        conta = ContaBancaria("Teste", -200)

def test_exception_sacar_saldo_insuficiente(conta_com_saldo, monkeypatch):
    """Conta com 1000 de saldo, testa exceção ao tentar sacar valor maior que o saldo da conta"""
    with pytest.raises(SaldoInsuficienteError):
        conta_com_saldo.sacar(1001)
    
def test_exception_sacar_saldo_negativo(conta_zerada, monkeypatch):
    """Conta com 0 de saldo, testa exceção ao tentar sacar valor negativo"""
    with pytest.raises(ValorInvalidoError):
        conta_zerada.sacar(-200)
        
def test_exception_depositar_saldo_negativo(conta_zerada, monkeypatch):
    """Conta com 0 de saldo"""
    with pytest.raises(ValorInvalidoError):
        conta_zerada.depositar(-2000)
    
def test_depositar(conta_zerada):
    """Conta com 0 de saldo, verifica se o saldo atual é igual ao saldo depositado"""
    conta_zerada.depositar(2000)
    assert conta_zerada.saldo == 2000
    
def test_sacar(conta_com_saldo):
    """Conta com 1000 de saldo, verifica se o saldo da conta descontou do que foi sacado"""
    conta_com_saldo.sacar(100)
    assert conta_com_saldo.saldo == 900
    
def test_transferencia_bancaria(conta_com_saldo, conta_zerada):
    """Testa metodo transferir e verifica se o saldo da conta zerada é igual ao saldo transferido"""
    conta_com_saldo.transferir(conta_zerada, valor=500)
    assert conta_zerada.saldo == 500

def test_exception_dividir():
    """Testando exceção de divisão por zero"""
    with pytest.raises(ZeroDivisionError):
        dividir(0, 0)

@pytest.mark.parametrize(
    'a, b, resultado',
    [
        (0, 5, 0),
        (10, 5, 2),
        (25, 2, 12.5)
    ]
)
def test_dividir(a, b, resultado):
    """Testa função divir com valores válidos"""
    assert dividir(a, b) == resultado


@pytest.mark.parametrize(
    'percentual',
    [
        (-25),
        (120)
    ]
)
def test_exception_calcular_desconto(percentual):
    """Valor percentual menor que 0 ou maior que 100"""
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(100, percentual)

@pytest.mark.parametrize(
    'valor, percentual, resultado',
    [
        (100, 25, 75),
        (100, 100, 0)
    ]
)
def test_calcular_desconto(valor, percentual, resultado):
    """Testes válidos da função calcular_desconto"""
    assert calcular_desconto(valor, percentual) == resultado

def test_exception_buscar_cotacao_dolar():
    """Teste irá passar pois o endpoint passado não é de uma API válida"""
    with pytest.raises(requests.exceptions.ReadTimeout):
        buscar_cotacao_dolar()

def test_buscar_cotacao_dolar(mock_response_api):
    """Validando cotacao do dolar com API mockada"""
    assert mock_response_api == 5.18
    
def test_converter_reais_para_dolar(mock_response_api):
    """Validando conversão de reais para dolar com API mockada"""
    valor_convertido = converter_reais_para_dolar(1)
    assert valor_convertido == 0.19

@pytest.mark.parametrize(
    "principal, taxa, periodos, resultado",
    [
        (100.0, 2.0, 5, 24300),
        (50.0, 5.0, 2, 1800.0),
    ]
)
def test_juros_compostos(principal, taxa, periodos, resultado):
    """Testar função calcular juros compostos com valores válidos"""
    assert calcular_juros_composto(principal, taxa, periodos) == resultado

def test_exception_calcular_juros_compostos():
    """Testar exceção da função calcular juros compostos"""
    with pytest.raises(ValorInvalidoError):
        calcular_juros_composto(100, 2, -5)

@pytest.mark.parametrize(
    "modo, esperado",
    [
        ("False", False),
        ("True", True)
    ]
)  
def test_esta_em_modo_debug_true(modo, esperado, monkeypatch):
    """Teste para verificar se o modo debug está ativado"""
    monkeypatch.setenv('APP_DEBUG', modo)
    assert esta_em_modo_debug() == esperado

def test_cotacao_dolar_api_real(cotacao_dolar_dia, cotacao_dolar_data_especifica, monkeypatch):
    """Teste para comparar cotação do dolar do dia, com uma data especifica,
        exemplo de variavel `now` 07-23-2026
    """
    now = datetime.now().strftime("%m-%d-%Y") #now = 'mes-dia-ano'
    assert cotacao_dolar_dia['cotacaoCompra'] == cotacao_dolar_data_especifica(now)['cotacaoCompra']
