import pytest
import re

from lucas_correia_estufa_agrotech.banco import ContaBancaria, ValorInvalidoError, SaldoInsuficienteError, dividir, calcular_desconto, converter_reais_para_dolar, esta_em_modo_debug, calcular_juros_composto

@pytest.fixture
def conta_bancaria() -> ContaBancaria:
    return ContaBancaria(titular="Teste", saldo_inicial=1000.0)


@pytest.mark.parametrize(
        "titular, saldo",
        [
            ("Teste", 1000.),
            ("Teste", 1.),
            ("Teste", 0.1),
            ("Teste", 0.01),
            ("Teste", 0.001),
            ("Teste", 0.),
        ]
)
def test_criar_conta_bancaria_ok(titular: str, saldo: float):
    conta = ContaBancaria(titular, saldo)
    assert conta.titular == titular and conta.saldo == saldo
    

@pytest.mark.parametrize(
        "titular, saldo",
        [
            ("Teste", -0.001),
            ("Teste", -0.01),
            ("Teste", -0.1),
            ("Teste", -1.),
            ("Teste", -1000.),
        ]
)
def test_criar_conta_bancaria_raises_valor_invalido(titular: str, saldo: float):
    with pytest.raises(ValorInvalidoError, match=re.escape("Saldo inicial nao pode ser negativo.")) as exc:
        conta = ContaBancaria(titular, saldo)
    assert exc.type is ValorInvalidoError

@pytest.mark.parametrize(
        "valor, expected",
        [
            (1000., 2000.),
            (100., 1100.),
            (10., 1010.),
            (1., 1001.),
            (0.1, 1000.1),
            (0.01, 1000.01),
            (0.001, 1000.001),
        ]
)
def test_conta_bancaria_depositar_ok(conta_bancaria: ContaBancaria, valor: float, expected: float):
    conta_bancaria.depositar(valor)
    assert conta_bancaria.saldo == expected

@pytest.mark.parametrize(
        "valor",
        [
            (-1000.),
            (-100.),
            (-10.),
            (-1.),
            (-0.1),
            (-0.01),
            (-0.001),
            (0),
        ]
)
def test_conta_bancaria_depositar_raises_valor_invalido(conta_bancaria: ContaBancaria, valor: float):
    with pytest.raises(ValorInvalidoError, match=re.escape("O valor do deposito deve ser positivo.")) as exc:
        conta_bancaria.depositar(valor)
    assert exc.type is ValorInvalidoError

@pytest.mark.parametrize(
        "valor, expected",
        [
            (1000., 0.),
            (100., 900.),
            (10., 990.),
            (1., 999.),
            (0.1, 999.9),
            (0.01, 999.99),
            (0.001, 999.999),
        ]
)
def test_conta_bancaria_sacar_ok(conta_bancaria: ContaBancaria, valor: float, expected: float):
    conta_bancaria.sacar(valor)
    assert conta_bancaria.saldo == expected

@pytest.mark.parametrize(
        "valor",
        [
            (-1000.),
            (-100.),
            (-10.),
            (-1.),
            (-0.1),
            (-0.01),
            (-0.001),
            (0),
        ]
)
def test_conta_bancaria_sacar_raises_valor_invalido(conta_bancaria: ContaBancaria, valor: float):
    with pytest.raises(ValorInvalidoError, match=re.escape("O valor do saque deve ser positivo.")) as exc:
        conta_bancaria.sacar(valor)
    assert exc.type is ValorInvalidoError

@pytest.mark.parametrize(
        "valor",
        [
            (2000.),
            (1100.),
            (1010.),
            (1001.),
            (1000.1),
            (1000.01),
            (1000.001),
        ]
)
def test_conta_bancaria_sacar_raises_saldo_insuficiente(conta_bancaria: ContaBancaria, valor: float):
    with pytest.raises(SaldoInsuficienteError, match=re.escape(f"Saldo insuficiente: saldo atual R$ {conta_bancaria.saldo:.2f}, tentativa de saque R$ {valor:.2f}")) as exc:
        conta_bancaria.sacar(valor)
    assert exc.type is SaldoInsuficienteError

@pytest.mark.parametrize(
        "destino, valor",
        [
            (ContaBancaria("Teste"), -1000.),
            (ContaBancaria("Teste"), -100.),
            (ContaBancaria("Teste"), -10.),
            (ContaBancaria("Teste"), -1.),
            (ContaBancaria("Teste"), -0.1),
            (ContaBancaria("Teste"), -0.01),
            (ContaBancaria("Teste"), -0.001),
            (ContaBancaria("Teste"), 0),
        ]
)
def test_conta_bancaria_transferir_raises_valor_invalido(conta_bancaria: ContaBancaria, destino: ContaBancaria, valor: float):
    with pytest.raises(ValorInvalidoError, match=re.escape("O valor do saque deve ser positivo.")) as exc:
        conta_bancaria.transferir(destino, valor)
    assert exc.type is ValorInvalidoError

@pytest.mark.parametrize(
        "destino, valor",
        [
            (ContaBancaria("Teste"), 2000.),
            (ContaBancaria("Teste"), 1100.),
            (ContaBancaria("Teste"), 1010.),
            (ContaBancaria("Teste"), 1001.),
            (ContaBancaria("Teste"), 1000.1),
            (ContaBancaria("Teste"), 1000.01),
            (ContaBancaria("Teste"), 1000.001),
        ]
)
def test_conta_bancaria_transferir_raises_saldo_insuficiente(conta_bancaria: ContaBancaria, destino: ContaBancaria, valor: float):
    with pytest.raises(SaldoInsuficienteError, match=re.escape(f"Saldo insuficiente: saldo atual R$ {conta_bancaria.saldo:.2f}, tentativa de saque R$ {valor:.2f}")) as exc:
        conta_bancaria.transferir(destino, valor)
    assert exc.type is SaldoInsuficienteError


@pytest.mark.parametrize(
        "destino, valor",
        [
            (ContaBancaria("Teste"), 1000.),
            (ContaBancaria("Teste"), 100.),
            (ContaBancaria("Teste"), 1.),
            (ContaBancaria("Teste"), 10.),
            (ContaBancaria("Teste"), 0.1),
            (ContaBancaria("Teste"), 0.01),
            (ContaBancaria("Teste"), 0.001),
        ]
)
def test_conta_bancaria_transferir_ok(conta_bancaria: ContaBancaria, destino: ContaBancaria, valor: float):
    saldo_anterior = conta_bancaria.saldo
    conta_bancaria.transferir(destino, valor)
    assert conta_bancaria.saldo == saldo_anterior - valor and destino.saldo == valor

@pytest.mark.parametrize(
    "a, b",
    [
        (1., 0.),
    ]
)
def test_dividir_raises(a: float, b: float):
    with pytest.raises(ZeroDivisionError):
        dividir(a, b)

@pytest.mark.parametrize(
    "a, b, expected",
    [
        (1., 1., 1.),
        (2., 2., 1.),
        (4., 2., 2.),
        (8., 2., 4.),
        (16., 2., 8.),
        (5., 3., 5/3),
        (7., 5., 7/5),
    ]
)
def test_dividir(a: float, b: float, expected: float):
    observed = dividir(a, b)
    assert observed == expected

@pytest.mark.parametrize(
    "valor, percentual",
    [
        (0., -100.),
        (0., -1.),
        (0., -0.1),
        (0., -0.01),
        (0., -0.001),
        (0., 100.001),
        (0., 100.01),
        (0., 100.1),
        (0., 101.),
        (0., 200.),
    ]
)
def test_calcular_desconto_raises_valor_invalido(valor: float, percentual: float):
    with pytest.raises(ValorInvalidoError):
        calcular_desconto(valor, percentual)

@pytest.mark.parametrize(
    "valor, percentual, expected",
    [
        (200., 0., 200),
        (200., 25., 150),
        (200., 50., 100),
        (200., 75., 50),
        (200., 100., 0),
        (123.45, 0., 123.45),
        (123.45, 23., 95.05),
        (123.45, 43., 70.36),
        (123.45, 73., 33.33),
        (123.45, 91., 11.11),
    ]
)
def test_calcular_desconto_ok(valor: float, percentual: float, expected: float):
    observed = calcular_desconto(valor, percentual)
    assert observed == pytest.approx(expected, rel=1e-2)

@pytest.mark.parametrize(
    "valor, expected",
    [
        (10., 1.94),
        (20., 3.88),
        (37., 7.18),
        (83., 16.12),
    ]
)
def test_converter_reais_para_dolar_ok(monkeypatch: pytest.MonkeyPatch, valor: float, expected: float):
    monkeypatch.setattr("lucas_correia_estufa_agrotech.banco.buscar_cotacao_dolar", lambda: 5.15)
    observed = converter_reais_para_dolar(valor)
    assert observed == pytest.approx(expected, rel=1e-2)

@pytest.mark.parametrize(
    "debug, expected",
    [
        ("true", True),
        ("false", False),
    ]
)
def test_esta_em_modo_debug_ok(monkeypatch: pytest.MonkeyPatch, debug: str, expected: bool):
    monkeypatch.setenv("APP_DEBUG", debug)
    observed = esta_em_modo_debug()
    assert observed == expected

@pytest.mark.parametrize(
    "periodos",
    [
        (-1),
        (-2),
        (-3),
        (-4),
    ]
)
def test_calcular_juros_composto_raises_valor_invalido(periodos: int):
    with pytest.raises(ValorInvalidoError, match=re.escape("Numero de periodos nao pode ser negativo.")):
        calcular_juros_composto(0, 0, periodos)


@pytest.mark.parametrize(
    "principal, taxa, periodos, expected",
    [
        (1., 1., 1, 2.),
        (2., 2., 2, 18.),
        (4., 4., 4, 2500.),
        (8., 13., 7, 843308032.),
    ]
)
def test_calcular_juros_composto_ok(principal: float, taxa: float, periodos: int, expected: float):
    observed = calcular_juros_composto(principal, taxa, periodos)
    assert observed == pytest.approx(expected, rel=1e-2)
