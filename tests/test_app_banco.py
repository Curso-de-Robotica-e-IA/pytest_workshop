import sys
import pytest
import platform
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
import requests
from ygor_matos_estufa_agrotech.app_banco import ContaBancaria, SaldoInsuficienteError, ValorInvalidoError, dividir, calcular_desconto, buscar_cotacao_dolar,converter_reais_para_dolar,esta_em_modo_debug, calcular_juros_composto
import os

def test_criaca_conta_saldo_negativo():
    with pytest.raises(ValorInvalidoError):
        conta = ContaBancaria('joao',-1)

def test_criacao_conta(conta):
    assert isinstance(conta, ContaBancaria)

def test_retorno_saldo(conta):
    assert conta.saldo == 1000000

def test_nome_conta(conta):
    assert conta.titular == 'Ygor'

def test_deposito_conta(conta):
    saldo_inicial = conta.saldo
    conta.depositar(50)
    assert conta.saldo-saldo_inicial == 50

def test_deposito_negativo(conta):
    with pytest.raises(ValorInvalidoError):
        conta.depositar(-1)

def test_sacar_valor_negativo(conta):
    with pytest.raises(ValorInvalidoError):
        conta.sacar(-1)

def test_sacar_valor_maior_que_saldo(conta):
    with pytest.raises(SaldoInsuficienteError):
        conta.sacar(1000001)

def test_saque_valido(conta):
    metade_saldo_inicial = conta.saldo / 2
    conta.sacar(metade_saldo_inicial)
    assert conta.saldo == metade_saldo_inicial

def test_transferir(conta, outra_conta):
    saldo_inicial_conta = conta.saldo
    saldo_inicial_outra_contra = outra_conta.saldo
    transferencia= 50
    conta.transferir(outra_conta,transferencia)
    assert conta.saldo == (saldo_inicial_conta-transferencia)
    assert outra_conta.saldo == (saldo_inicial_outra_contra+transferencia)

def test_transferir_saldo_negativo(conta, outra_conta):
    with pytest.raises(ValorInvalidoError):
        conta.transferir(outra_conta,-50)

def test_divisao_por_zero():
    with pytest.raises(ZeroDivisionError):
        dividir(5,0)

def test_divisao():
    assert dividir(10,5) == 2

def calcular_desconto_percentual_acima_do_limite():
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(200,101)

@pytest.mark.parametrize(
    'valor, desconto',
    [
        (100,101),
        (100,-1)
    ]
)
def test_calcular_desconto_fora_dos_limites(valor,desconto):
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(valor, desconto)


def test_calcular_desconto():
    assert calcular_desconto(10,20)==8

@pytest.mark.xfail
def test_buscar_cotacao_dolar():
    assert buscar_cotacao_dolar == 'xyz'

def test_buscar_cotacao_dolar(mocker):

    mock_get_cotacao=mocker.Mock()
    mock_get_cotacao.json.return_value = {"valor":5.15}
    mocker.patch("requests.get", return_value=mock_get_cotacao)

    cotacao = buscar_cotacao_dolar()

    assert cotacao == 5.15

def test_buscar_cotacao_dolar_timeout(mocker):
    mock_get_cotacao = mocker.patch("requests.get")
    mock_get_cotacao.side_effect = requests.exceptions.Timeout()

    with pytest.raises(requests.exceptions.Timeout):
        buscar_cotacao_dolar()

def test_converter_reais_em_dolar(monkeypatch):
    def cotacao():
        return 5
    
    monkeypatch.setattr("ygor_matos_estufa_agrotech.app_banco.buscar_cotacao_dolar", cotacao)
    dolar = converter_reais_para_dolar(10)

    assert dolar == 2


#no método converter reais em dolar,
# no caso de um valor negativo, deveria haver o lançamento de uma exceção do tipo ValorInvalido
@pytest.mark.xfail
def test_converter_reais_negativos_em_dolar(monkeypatch):
    def cotacao():
        return 5
    monkeypatch.setattr("ygor_matos_estufa_agrotech.app_banco.buscar_cotacao_dolar", cotacao)
    with pytest.raises(ValorInvalidoError):
        converter_reais_para_dolar(-10)

@pytest.mark.skipif(os.environ.get("APP_DEBUG","true").lower ==True, reason="Esse teste só roda se o modo debug não estiver ativo")
def test_modo_debug():
    assert esta_em_modo_debug() == False


def test_calcular_juros_compostos_periodo_invalido():
    with pytest.raises(ValorInvalidoError):
        calcular_juros_composto(1,1,-1)

def test_calcular_juros_compostos():
    juros = calcular_juros_composto(1000, 0.05, 2)

    assert juros == 1102.50