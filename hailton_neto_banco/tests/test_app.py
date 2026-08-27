import pytest
from src.hailton_neto_banco.app import (
    ContaBancaria,
    dividir, 
    calcular_desconto, 
    buscar_cotacao_dolar, 
    converter_reais_para_dolar, 
    esta_em_modo_debug, 
    calcular_juros_composto
)


@pytest.mark.parametrize("saldo, resultado_esperado", [
    (100.0, 100.0),
    (0.0, 0.0),
    (50.5, 50.5),
])
def test_verificar_saldo_inicial(conta_bancaria, monkeypatch, saldo, resultado_esperado):
    monkeypatch.setattr(conta_bancaria, "_saldo", saldo)
    assert conta_bancaria.saldo == resultado_esperado


@pytest.mark.parametrize("saldo", [
    (-100.0),
    (-50.5),
    (-0.01),
])
def test_verificar_saldo_inicial_negativo(saldo, valor_invalido):
    with pytest.raises(valor_invalido):
        ContaBancaria("Teste", saldo)


@pytest.mark.parametrize("saldo_base, valor, resultado_esperado", [
    (100.0, 100.0, 200.0),
    (100.0, 50.5, 150.5),
    (0.0, 100.0, 100.0),
])
def test_verificar_deposito(conta_bancaria, monkeypatch, saldo_base, valor, resultado_esperado):
    monkeypatch.setattr(conta_bancaria, "_saldo", saldo_base)
    conta_bancaria.depositar(valor)
    assert conta_bancaria.saldo == resultado_esperado


@pytest.mark.parametrize("valor", [
    (0.0),
    (-100.0),
    (-50.5),
    (-0.01),
])
def test_verificar_deposito_excecao(conta_bancaria, valor, valor_invalido):
    with pytest.raises(valor_invalido):
        conta_bancaria.depositar(valor)


@pytest.mark.parametrize("saldo_base, valor, resultado_esperado", [
    (100.0, 50.0, 50.0),
    (100.0, 100.0, 0.0),
    (50.5, 25.5, 25.0),
])
def test_verificar_saque(conta_bancaria, monkeypatch, saldo_base, valor, resultado_esperado):
    monkeypatch.setattr(conta_bancaria, "_saldo", saldo_base)
    conta_bancaria.sacar(valor)
    assert conta_bancaria.saldo == resultado_esperado


@pytest.mark.parametrize("valor", [
    (0.0),
    (-100.0),
    (-50.5),
    (-0.01),
])
def test_verificar_saque_valor_invalido(conta_bancaria, valor, valor_invalido):
    with pytest.raises(valor_invalido):
        conta_bancaria.sacar(valor)


@pytest.mark.parametrize("valor", [
    (150.0),
    (100.0),
    (30.0),
])
def test_verificar_saque_saldo_insuficiente(conta_bancaria, valor, saldo_insuficiente):
    with pytest.raises(saldo_insuficiente):
        conta_bancaria.sacar(valor)


@pytest.mark.parametrize("saldo_origem, saldo_destino, valor_transferencia", [
    (100.0, 50.0, 30.0),
    (200.0, 100.0, 150.0),
    (50.5, 25.5, 25.0),
])
def test_verificar_transferencia(conta_bancaria, monkeypatch, saldo_origem, saldo_destino, valor_transferencia):
    conta_destino = ContaBancaria("Destino", saldo_destino)
    monkeypatch.setattr(conta_bancaria, "_saldo", saldo_origem)
    conta_bancaria.transferir(conta_destino, valor_transferencia)
    assert conta_bancaria.saldo == saldo_origem - valor_transferencia
    assert conta_destino.saldo == saldo_destino + valor_transferencia


@pytest.mark.parametrize("a, b, resultado_esperado", [
    (10, 2, 5),
    (9, 3, 3),
    (5, 2, 2.5),
])
def test_divisao(a, b, resultado_esperado):
    assert dividir(a, b) == resultado_esperado


@pytest.mark.parametrize("a, b", [
    (10, 0),
    (9, 0),
    (5, 0),
])
def test_divisao_por_zero(a, b):
    with pytest.raises(ZeroDivisionError):
        dividir(a, b)


@pytest.mark.parametrize("valor, percentual, resultado_esperado", [
    (100.0, 10.0, 90.0),
    (200.0, 25.0, 150.0),
    (50.0, 50.0, 25.0),
])
def test_calcular_desconto(valor, percentual, resultado_esperado):
    assert calcular_desconto(valor, percentual) == resultado_esperado


@pytest.mark.parametrize("valor, percentual", [
    (100.0, -10.0),
    (200.0, 150.0),
    (50.0, 200.0),
])
def test_calcular_desconto_excecao(valor, percentual, valor_invalido):
    with pytest.raises(valor_invalido):
        calcular_desconto(valor, percentual)


resposta = [
    {
        "moeda": "USD",
        "nome": "Dólar",
        "compra": 5.1515,
        "venda": 5.1523,
        "fechoAnterior": 5.15,
        "dataAtualizacao": "2026-08-26T14:01:00.000Z"
    }
]
cotacao = resposta[0]["compra"]


def test_buscar_cotacao_dolar(mocker):
    mock = mocker.Mock()
    mock.json.return_value = resposta
    mocker.patch("src.hailton_neto_banco.app.requests.get", return_value=mock)
    assert buscar_cotacao_dolar() == cotacao


@pytest.mark.parametrize("valor, resultado_esperado",[
    (5, 5 / cotacao),
    (10, 10 / cotacao),
    (50, 50 / cotacao),
])
def test_converter_reais_para_dolar(mocker, valor, resultado_esperado):
    mocker.patch("src.hailton_neto_banco.app.buscar_cotacao_dolar", return_value=cotacao)
    assert converter_reais_para_dolar(valor) == round(resultado_esperado, 2)


@pytest.mark.parametrize("valor, resultado_esperado", [
    ("true", True),
    ("TRUE", True),
    ("false", False),
    (None, False),
])
def test_esta_em_modo_debug(monkeypatch, valor, resultado_esperado):
    if valor is not None:
        monkeypatch.setenv("APP_DEBUG", valor)
    else:
        monkeypatch.delenv("APP_DEBUG", raising=False)  
    assert esta_em_modo_debug() == resultado_esperado


@pytest.mark.parametrize("principal, taxa_juros, periodo, resultado_esperado", [
    (1000.0, 5.0, 2, 36000.0),
    (2000.0, 3.0, 3, 128000.0),
    (1500.0, 4.0, 1, 7500.0),
])
def test_calcular_juros_composto(principal, taxa_juros, periodo, resultado_esperado):
    assert calcular_juros_composto(principal, taxa_juros, periodo) == round(resultado_esperado, 2)


@pytest.mark.parametrize("principal, taxa_juros, periodo", [
    (-1000.0, 5.0, -2),
    (1000.0, -5.0, -3),
    (-1000.0, -5.0, -1),
])
def test_calcular_juros_composto_excecao(principal, taxa_juros, periodo, valor_invalido):
    with pytest.raises(valor_invalido):
        calcular_juros_composto(principal, taxa_juros, periodo)