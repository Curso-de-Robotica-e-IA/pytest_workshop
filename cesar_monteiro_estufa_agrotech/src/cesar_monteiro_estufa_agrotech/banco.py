import os
import requests


class SaldoInsuficienteError(Exception):
    """Levantada quando uma tentativa de saque excede o saldo disponivel."""


class ValorInvalidoError(Exception):
    """Levantada quando um valor de deposito/saque/percentual e invalido."""


class ContaBancaria:
    """Uma conta bancaria simples."""

    def __init__(self, titular: str, saldo_inicial: float = 0.0):
        if saldo_inicial < 0:
            raise ValorInvalidoError("Saldo inicial nao pode ser negativo.")
        self.titular = titular
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        return self._saldo

    def depositar(self, valor: float) -> float:
        if valor <= 0:
            raise ValorInvalidoError("O valor do deposito deve ser positivo.")
        self._saldo += valor
        return self._saldo

    def sacar(self, valor: float) -> float:
        if valor <= 0:
            raise ValorInvalidoError("O valor do saque deve ser positivo.")
        if valor > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente: saldo atual R$ {self._saldo:.2f}, "
                f"tentativa de saque R$ {valor:.2f}."
            )
        self._saldo -= valor
        return self._saldo

    def transferir(self, destino: "ContaBancaria", valor: float) -> None:
        self.sacar(valor)
        destino.depositar(valor)


def dividir(a: float, b: float) -> float:
    """Divide a por b. Levanta ZeroDivisionError se b for 0."""
    return a / b


def calcular_desconto(valor: float, percentual: float) -> float:
    if not 0 <= percentual <= 100:
        raise ValorInvalidoError("Percentual deve estar entre 0 e 100.")
    return valor - (valor * percentual / 100)


def buscar_cotacao_dolar() -> float:
    resposta = requests.get("https://api.exemplo.com/cotacao/usd", timeout=5)
    resposta.raise_for_status()
    dados = resposta.json()
    return dados["valor"]


def converter_reais_para_dolar(valor_em_reais: float) -> float:
    cotacao = buscar_cotacao_dolar()
    return round(valor_em_reais / cotacao, 2)


def esta_em_modo_debug() -> bool:
    """
    Le a variavel de ambiente APP_DEBUG para saber se a aplicacao esta
    rodando em modo debug. 
    """
    return os.environ.get("APP_DEBUG", "false").lower() == "true"


def calcular_juros_composto(principal: float, taxa: float, periodos: int) -> float:
    """Calcula o montante final com juros compostos."""
    if periodos < 0:
        raise ValorInvalidoError("Numero de periodos nao pode ser negativo.")
    return round(principal * ((1 + taxa) ** periodos), 2)