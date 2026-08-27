import pytest
from tests.conftest import conta_banco_com_saldo, conta_banco_sem_saldo, conta_banco_destino
from src.renan_vanbasten_estufa_agrotech.banco import (ValorInvalidoError,
                                                       SaldoInsuficienteError,
                                                       dividir,
                                                       calcular_desconto,
                                                       buscar_cotacao_dolar, 
                                                       converter_reais_para_dolar,
                                                       esta_em_modo_debug,
                                                       calcular_juros_composto)
import requests


def test_depositar_exception(conta_banco_com_saldo):
   with pytest.raises(ValorInvalidoError):
        conta_banco_com_saldo.depositar(-10.0)    


@pytest.mark.parametrize(
        "saldo_atual, valor, saldo_atualizado",
        [
            (100, 50, 150),
            (100, 80, 180)
        ]
)
def test_depositar_sucesso(conta_banco_com_saldo, saldo_atual, valor, saldo_atualizado):
    assert conta_banco_com_saldo.depositar(valor) == saldo_atualizado

@pytest.mark.parametrize(
        "saldo_atual, valor, saldo_atualizado",
        [
            (100, 50, 50),
            (100, 80, 20)
        ]
)
def test_sacar_sucesso(conta_banco_com_saldo, saldo_atual, valor, saldo_atualizado):
    assert conta_banco_com_saldo.sacar(valor) == saldo_atualizado

def test_sacar_valor_exception(conta_banco_com_saldo):
    with pytest.raises(ValorInvalidoError):
        conta_banco_com_saldo.sacar(-10.0)

def test_sacar_saldo_exception(conta_banco_sem_saldo):
    with pytest.raises(SaldoInsuficienteError):
        conta_banco_sem_saldo.sacar(200.0)



@pytest.mark.parametrize(
        "saldo_atual, valor", 
        [
            (100, 50), 
            (100, 80)
        ]
)
def test_transferir_sucesso_sacar(conta_banco_com_saldo, conta_banco_destino, saldo_atual, valor):
    conta_banco_com_saldo.transferir(conta_banco_destino, valor)

    assert conta_banco_com_saldo._saldo == saldo_atual - valor
    assert conta_banco_destino._saldo == saldo_atual + valor


def test_divisao_sucesso():
    assert dividir(100, 2) == 50

def test_divisao_exception():
    with pytest.raises(ZeroDivisionError):
        dividir(20, 0)


def test_calcular_desconto_exception_menor_que_zero():
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(20, -10)

def test_calcular_desconto_sucesso_exception_maior_que_cem():
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(20, 200)

def test_calcular_desconto_sucesso():
    assert calcular_desconto(100, 20) == 80

@pytest.mark.parametrize(
    "valor, porcentagem, resultado",
    [
        (50.0, 10.0, 45.0),
        (80.0, 5.0, 76.0),
        (80.0, 100, 0),
        (20, 50, 10)
    ]
)
def test_calular_desconto(valor, porcentagem, resultado):
    assert calcular_desconto(valor, porcentagem) == resultado

def test_esta_em_modo_debug_false(monkeypatch):
    monkeypatch.setenv("APP_DEBUG", "false")
    assert esta_em_modo_debug() is False

def test_esta_em_modo_debug_true(monkeypatch):
    monkeypatch.setenv("APP_DEBUG", "true")
    assert esta_em_modo_debug() is True

@pytest.mark.parametrize(
        "valor, taxa_juros, periodo, esperado",
        [
            (2500.0, 15.0, 5, 2621440000.0),
            (1000.0, 10.0, 7, 19487171000.0)
        ]
)
def test_calcular_juros_composto_sucesso(valor, taxa_juros, periodo, esperado):
    assert calcular_juros_composto(valor, taxa_juros, periodo) == esperado
    with pytest.raises(ValorInvalidoError):
        calcular_juros_composto(valor, taxa_juros, -10)


def test_buscar_cotacao_dolar_sucesso(mocker):
    json_mockado = {
        "moeda": "USD",
        "nome": "Dólar",
        "compra": 5.1515,
        "venda": 5.1523,
        "fechoAnterior": 5.15,
        "dataAtualizacao": "2026-08-26T14:01:00.000Z"
}
    mock_resposta = mocker.Mock()
    mock_resposta.json.return_value = json_mockado
    mocker.patch("requests.get", return_value=mock_resposta)

    resultado = buscar_cotacao_dolar()

    assert resultado == 5.1515
    requests.get.assert_called_once_with("https://br.dolarapi.com/v1/cotacoes/usd")
    mock_resposta.raise_for_status.assert_called_once()


def test_buscar_cotacao_dolar_erro_conexao(mocker):
    mocker.patch("requests.get", side_effect=requests.exceptions.HTTPError("Erro 500"))
    with pytest.raises(requests.exceptions.HTTPError):
        buscar_cotacao_dolar()


@pytest.mark.parametrize(
        "valor, esperado",
        [
            (50.0, 9.71),
            (100.0, 19.41),
            (130.0, 25.24),
            (820.0, 159.18)
        ]
)
def test_converter_reais_para_dolar(valor, esperado):
    #cotacao = buscar_cotacao_dolar()
    assert converter_reais_para_dolar(valor) == esperado