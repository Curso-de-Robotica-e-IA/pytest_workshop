import pytest
import banco
import requests
def test_criar_conta(criar_conta_bancaria):
    
    assert criar_conta_bancaria.titular == "Carlos José"
    assert criar_conta_bancaria.saldo == 100.0


@pytest.mark.parametrize(
        "saldo_negativo",
        [(-1.0), (-15.02), (-10000.01)]
)
def test_validar_criacao_conta_saldo_negativo(saldo_negativo):
    with pytest.raises(banco.ValorInvalidoError):
        banco.ContaBancaria("Maria Alice", saldo_inicial=saldo_negativo)

def test_validar_deposito_valor_negativo(deposito_valor_negativo):
    with pytest.raises(banco.ValorInvalidoError):
        deposito_valor_negativo.depositar(-500.00)

@pytest.mark.parametrize(
        "valor, esperado",
        [
            (100.00, 200.00),
            (300.00, 400.00),
            (900.00, 1000.00),
        ]
)
def test_depoisto_com_sucesso(criar_conta_bancaria, valor, esperado):
    criar_conta_bancaria.depositar(valor)
    assert criar_conta_bancaria.saldo == esperado

def test_sacar_valor_negativo(criar_conta_bancaria):
    with pytest.raises(banco.ValorInvalidoError):
        criar_conta_bancaria.sacar(-50.00)

def test_sacar_valor_maior_que_saldo(criar_conta_bancaria):
    with pytest.raises(banco.SaldoInsuficienteError):
        criar_conta_bancaria.sacar(150.00)

@pytest.mark.parametrize(
    "valor, esperado",
    [
        (50.00, 50.00),
        (30.00, 70.00),
        (90.00, 10.00),
    ]
)
def test_sacar_valor_com_sucesso(criar_conta_bancaria, valor, esperado):
    criar_conta_bancaria.sacar(valor)
    assert criar_conta_bancaria.saldo == esperado

@pytest.mark.parametrize(
    "valor, esperado",
    [
        (100.00, 200.00),
        (300.00, 400.00),
        (600.00, 700.00),
    
    ])
def test_transferir_valor(criar_conta_bancaria, valor, esperado):
    conta_outra = banco.ContaBancaria("Maria Alice", 1000.00)
    conta_outra.transferir(criar_conta_bancaria, valor=valor)
    assert criar_conta_bancaria.saldo == esperado

@pytest.mark.parametrize("a, b",[(-100.00, 0),(791.00, 0),(132.50, 0),(1000.00, 0)])
def test_divisao_por_zero(a, b):
    with pytest.raises(ZeroDivisionError):
        result = a/b

@pytest.mark.parametrize("v1, v2, esperado",
        [(100.0, 10.0, 10.0), (25.0, 2.0, 12.50), (180.0, 4.0, 45.0)]
    )
def test_dividir(v1, v2, esperado):
    result = banco.dividir(v1,v2)
    assert result == esperado

def test_desconto_sucesso(desconto_com_sucesso):
    result = desconto_com_sucesso
    assert result == 750.00

def test_desconto_invalido():
    with pytest.raises(banco.ValorInvalidoError):
        banco.calcular_desconto(100.00, 15000)

def test_calcular_juros_composto(juros_composto):
    assert juros_composto == 2560

def test_calcular_juros_composto_periodo_negativo():
    with pytest.raises(banco.ValorInvalidoError):
        banco.calcular_juros_composto(10,30,-6)

def test_modo_debug(modo_debug):
    assert modo_debug == False

def test_cotacao_dolar():
    with pytest.raises(requests.HTTPError):
       banco.buscar_cotacao_dolar()

def test_conversao_real_dolar():
    with pytest.raises(requests.HTTPError):
       banco.converter_reais_para_dolar(1000.0)