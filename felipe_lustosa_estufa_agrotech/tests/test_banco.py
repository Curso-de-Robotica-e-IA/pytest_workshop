import pytest
import os
from src.felipe_lustosa_estufa_agrotech.banco import ContaBancaria, SaldoInsuficienteError, ValorInvalidoError, dividir, calcular_desconto, esta_em_modo_debug, calcular_juros_composto, buscar_cotacao_dolar, converter_reais_para_dolar


def test_saldo_inicial_invalido():
   with pytest.raises(ValorInvalidoError):
      ContaBancaria("João", -15.0)


@pytest.mark.parametrize(
   "saldo", [-10.0, 0.0], ids=["negativo", "zero"]
)
def test_depositar_invalido(banco, saldo):
   with pytest.raises(ValorInvalidoError):
      banco.depositar(saldo)


@pytest.mark.parametrize(
   "saldo", [10.0], ids=["positivo"]
)
def test_depositar_valido(banco, saldo):
   valor_saldo = banco.depositar(saldo)
   assert valor_saldo == banco.saldo


@pytest.mark.parametrize(
   "valor", [10.0], ids=["positivo"]
)
def test_sacar_valido(banco, valor):
   valor_saldo = banco.depositar(valor)
   assert valor_saldo == banco.saldo


@pytest.mark.parametrize(
   "valor, excessao", 
   [(-10.0, ValorInvalidoError), (100000.0, SaldoInsuficienteError)], 
   ids=["negativo", "saldo_insuficiente"],
)
def test_sacar_invalido(banco, valor, excessao):
   with pytest.raises(excessao):
      banco.sacar(valor)


@pytest.mark.parametrize(
   "valor", [10.0], ids=["positivo"]
)
def test_transferir(banco, valor, monkeypatch):
   destino = ContaBancaria("Luiz")
   monkeypatch.setattr(banco, "_saldo", 100.0)
   destino_saldo_anterior = destino.saldo
   saldo_anterior = banco.saldo
   banco.transferir(destino, valor)
   assert banco.saldo + valor == saldo_anterior
   assert destino.saldo - valor == destino_saldo_anterior


@pytest.mark.parametrize(
   "dividendo, divisor, esperado", 
   [(10.0, 2.0, 5.0), (-10.0, 2.0, -5.0), (0.0, 2.0, 0.0)],
   ids=["positivo", "negativo", "zero"]
)
def test_divisao_valida(dividendo, divisor, esperado):
   assert dividendo / divisor == esperado


@pytest.mark.parametrize(
   "dividendo, divisor, esperado", 
   [(10.0, 2.0, 5.0), (-10.0, 2.0, -5.0), (0.0, 2.0, 0.0)],
   ids=["positivo", "negativo", "zero"]
)
def test_divisao_valida(dividendo, divisor, esperado):
   assert dividir(dividendo, divisor) == esperado


@pytest.mark.parametrize(
   "dividendo, divisor, esperado", 
   [(10.0, 0.0, ZeroDivisionError)],
   ids=["divisao_por_zero"]
)
def test_divisao_invalida(dividendo, divisor, esperado):
   with pytest.raises(esperado):
      dividir(dividendo, divisor)


@pytest.mark.parametrize(
   "valor, percentual, esperado", 
   [(100.0, 80.0, 20.0), (-100.0, 80.0, -20.0), ],
   ids=["positivo", "negativo"]
)
def test_calcular_desconto_valido(valor, percentual, esperado):
   assert calcular_desconto(valor, percentual) == esperado


@pytest.mark.parametrize(
   "valor, percentual, esperado", 
   [(100.0, -80.0, ValorInvalidoError), (100.0, 120.0, ValorInvalidoError)],
   ids=["negativo", "fora_intervalo"]
)
def test_calcular_desconto_invalido(valor, percentual, esperado):
   with pytest.raises(esperado):
      calcular_desconto(valor, percentual)


@pytest.mark.parametrize(
   "valor, percentual, esperado", 
   [(100.0, -80.0, ValorInvalidoError), (100.0, 120.0, ValorInvalidoError)],
   ids=["negativo", "fora_intervalo"]
)
def test_calcular_desconto_invalido(valor, percentual, esperado):
   with pytest.raises(esperado):
      calcular_desconto(valor, percentual)


def test_buscar_cotacao_dolar(mocker):
    mock_resposta = mocker.Mock()
    mock_resposta.json.return_value = {"valor": 5.25}
    
    mocker.patch("src.felipe_lustosa_estufa_agrotech.banco.requests.get", return_value=mock_resposta)

    resultado = buscar_cotacao_dolar()
    
    assert resultado == 5.25


def test_converter_reais_para_dolar_arredondamento(mocker):
    mocker.patch("src.felipe_lustosa_estufa_agrotech.banco.buscar_cotacao_dolar", return_value=3.00)

    resultado = converter_reais_para_dolar(10.00)
    
    assert resultado == 3.33


def test_esta_em_modo_debug():
   is_debug = os.environ.get("APP_DEBUG", "false").lower() == "true"

   assert esta_em_modo_debug() == is_debug


@pytest.mark.parametrize(
   "principal, taxa, periodos, esperado", 
   [(100.0, 1.0, 6, 6400.00)],
   ids=["positivo"]
)
def test_calcular_juros_composto_valido(principal, taxa, periodos, esperado):
   juros = calcular_juros_composto(principal, taxa, periodos)
   assert juros == esperado


@pytest.mark.parametrize(
   "principal, taxa, periodos, esperado", 
   [(100.0, 1.0, -6, ValorInvalidoError)],
   ids=["positivo"]
)
def test_calcular_juros_composto_invalido(principal, taxa, periodos, esperado):
   with pytest.raises(esperado):
      calcular_juros_composto(principal, taxa, periodos)