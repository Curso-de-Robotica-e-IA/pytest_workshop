import pytest

from src.joao_marinho_banco.banco import (
    ContaBancaria,
    SaldoInsuficienteError,
    ValorInvalidoError,
)


MOCK_VALOR_DEPOSITAR = [(10, 10), (20, 20)]


@pytest.mark.parametrize(
    "valor, saldo_esperado",
    MOCK_VALOR_DEPOSITAR,
    ids=[f"deposito_{valor}" for valor, _ in MOCK_VALOR_DEPOSITAR],
)
def teste_depositar(mockContaBancaria, valor, saldo_esperado):
    saldo = mockContaBancaria.depositar(valor)
    assert saldo == saldo_esperado


@pytest.mark.parametrize("valor", [0, -10])
def teste_depositar_valor_negativo(mockContaBancaria, valor):
    with pytest.raises(ValorInvalidoError):
        mockContaBancaria.depositar(valor)


def teste_sacar_reduz_o_saldo(conta_com_saldo):
    saldo = conta_com_saldo.sacar(40)
    assert saldo == 60
    assert conta_com_saldo.saldo == 60


@pytest.mark.parametrize("valor", [0, -10])
def teste_sacar_valor_invalido(conta_com_saldo, valor):
    with pytest.raises(ValorInvalidoError):
        conta_com_saldo.sacar(valor)


def teste_sacar_acima_do_saldo_levanta_erro(conta_com_saldo):
    with pytest.raises(SaldoInsuficienteError):
        conta_com_saldo.sacar(101)

    assert conta_com_saldo.saldo == 100


def teste_transferir_move_valor_entre_contas(conta_com_saldo, outra_conta_com_saldo):
    resultado = conta_com_saldo.transferir(outra_conta_com_saldo, 30)

    assert resultado is None
    assert conta_com_saldo.saldo == 70
    assert outra_conta_com_saldo.saldo == 80


def teste_transferencia_invalida_preserva_saldos(conta_com_saldo, outra_conta_com_saldo):
    with pytest.raises(SaldoInsuficienteError):
        conta_com_saldo.transferir(outra_conta_com_saldo, 101)

    assert conta_com_saldo.saldo == 100
    assert outra_conta_com_saldo.saldo == 50


def teste_saldo_inicial_negativo_levanta_erro():
    with pytest.raises(ValorInvalidoError):
        ContaBancaria(titular="Teste", saldo_inicial=-1)


