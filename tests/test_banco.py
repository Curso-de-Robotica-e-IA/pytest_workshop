from contextlib import nullcontext

import pytest
import src.danilo_monteiro_estufa_agrotech.banco as obj

def test_init():
    assert obj.ContaBancaria("Maria", 10)


def test_init_saldo_negativo():
   with pytest.raises(obj.ValorInvalidoError):
       assert obj.ContaBancaria("Danilo", -1.0)

def test_depositar(banco):
    assert banco.depositar(100)

@pytest.mark.parametrize(
    "saque, excecao_esperada",
    [
        (-30, obj.ValorInvalidoError),
        (100000, obj.SaldoInsuficienteError)
    ],
    ids = ["negativo", "saldo_insuficiente"],)
def test_saque_parametrize(banco, saque, excecao_esperada):
    with pytest.raises(excecao_esperada):
        banco.sacar(saque)

def test_divisao():
    with pytest.raises(ZeroDivisionError):
        assert obj.dividir(20,0)

@pytest.mark.parametrize(
        "valor, percentual, excecao_esperada",
        [
            (100, 50, nullcontext()),
            (100, -50, pytest.raises(obj.ValorInvalidoError)),
            pytest.param(-100, 50, nullcontext(), marks=pytest.mark.xfail(reason="Valor negativo não implementado")),
            pytest.param(-100, -50, pytest.raises(obj.ValorInvalidoError), marks=pytest.mark.xfail(reason="Valor negativo não implementado"))
        ],
        ids=["funcional", "percentual_negativo", "valor_negativo", "percentual_valor_negativo"]
)
def test_calcular_desconto(valor, percentual, excecao_esperada):
    with excecao_esperada:
        obj.calcular_desconto(valor, percentual)


@pytest.mark.parametrize("valor", [10.0, 50.0, 100.0], ids=["valor1","valor2","valor3"])
def test_transferir_com_sucesso(valor):
    origem = obj.ContaBancaria("A",100.0)
    destino = obj.ContaBancaria("B",100.0)

    origem_novo = origem.saldo - valor
    destino_novo = destino.saldo + valor
    origem.transferir(destino, valor)


    assert origem.saldo == origem_novo and destino.saldo == destino_novo

def test_transferencia_saldo_insuficiente_nao_altera_saldos():
    origem = obj.ContaBancaria("A",saldo_inicial=20.0)
    destino = obj.ContaBancaria("B",saldo_inicial=50.0)

    with pytest.raises(obj.SaldoInsuficienteError):
        origem.transferir(destino, 100.0)
        
    assert origem.saldo == 20.0
    assert destino.saldo == 50.0

def test_transferencia_valor_negativo_nao_altera_saldos():
    origem = obj.ContaBancaria("A", saldo_inicial=100.0)
    destino = obj.ContaBancaria("B", saldo_inicial=50.0)
    
    with pytest.raises(obj.ValorInvalidoError):
        origem.transferir(destino, -30.0)
        
    assert origem.saldo == 100.0
    assert destino.saldo == 50.0

# @pytest.mark.xfail
def test_buscar_cotacao_dolar_real(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"valor": 5.1}
    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse())
    resultado = obj.buscar_cotacao_dolar()
    
    assert isinstance(resultado, float)
    assert resultado > 0.0


def testar_buscar_cotacao_dolar_real_falha_no_acesso(monkeypatch):
    class MockResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {"valor": 5.1}
    monkeypatch.setattr("requests.get", lambda url, timeout: MockResponse())
    expected = 300 / 5.1
    assert pytest.approx(obj.converter_reais_para_dolar(300), rel=1e-2) == expected

def test_modo_debug():
    assert obj.esta_em_modo_debug() == False

@pytest.mark.parametrize(
    "principal, taxa, periodos, esperado",
    [
        (1000.0, 0.05, 12, 1795.86),  # R$ 1000 a 5% por 12 períodos
        (500.0, 0.02, 6, 563.08),     # R$ 500 a 2% por 6 períodos
        (100.0, 0.0, 5, 100.0),       # Sem juros
        (0.0, 0.10, 10, 0.0),         # Principal zero
    ]
)
def test_calcular_juros_composto_sucesso(principal, taxa, periodos, esperado):
    resultado = obj.calcular_juros_composto(principal, taxa, periodos)
    assert resultado == esperado

@pytest.mark.parametrize(
    "principal, taxa, periodos",
    [
        (1000.0, 0.05, -1),
        (1000.0, 0.05, -10),
    ]
)
def test_calcular_juros_composto_periodo_negativo(principal, taxa, periodos):
    with pytest.raises(obj.ValorInvalidoError) as exc_info:
        obj.calcular_juros_composto(principal, taxa, periodos)
