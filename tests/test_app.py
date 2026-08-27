from pickle import TRUE
import re

import pytest
from src.lucas_correia_estufa_agrotech.app import EstufaAgrotech, ServicoLogger

import sys

@pytest.fixture
def estufa():
    estufa = EstufaAgrotech()
    return estufa

@pytest.fixture
def logger_raise():
    logger = ServicoLogger()
    logger.caminho_arquivo = None
    return logger


@pytest.mark.xfail(raises=AssertionError, strict=True, reason='Estes valores deveriam causar erro')
@pytest.mark.parametrize(
        "temp, expected",
        [
            (-10., "Normal"),
            (-1., "ALERTA: Superaquecimento"),
            (1., "ALERTA: Superaquecimento"),
            (40., "ALERTA: Geada"),
            (41, "ALERTA: Geada"),
            (60., "Normal"),
        ]
)
def test_verificar_status_temperatura_should_fail(estufa: EstufaAgrotech, temp: float, expected: str) -> None:
    estufa.temperatura_atual = temp
    observed = estufa.verificar_status_temperatura()
    assert observed == expected, f"{observed!r} == {expected!r}"

@pytest.mark.parametrize(
        "temp, expected",
        [
            (-10., "ALERTA: Geada"),
            (-1., "ALERTA: Geada"),
            (-0.1, "ALERTA: Geada"),
            (-0.01, "ALERTA: Geada"),
            (0., "Normal"),
            (0.01, "Normal"),
            (0.1, "Normal"),
            (1., "Normal"),
            (39., "Normal"),
            (39.9, "Normal"),
            (39.99, "Normal"),
            (40., "Normal"),
            (40.01, "ALERTA: Superaquecimento"),
            (40.1, "ALERTA: Superaquecimento"),
            (41., "ALERTA: Superaquecimento"),
        ]
)
def test_verificar_status_temperatura(estufa: EstufaAgrotech, temp: float, expected: str) -> None:
    estufa.temperatura_atual = temp
    observed = estufa.verificar_status_temperatura()
    assert observed == expected, f"{observed!r} == {expected!r}"

@pytest.mark.parametrize(
        "preco_base, eh_vip",
        [
            (-10., True),
            (-1., True),
            (-0.1, True),
            (-0.01, True),
            (-0.001, True),
            (-10., False),
            (-1., False),
            (-0.1, False),
            (-0.01, False),
            (-0.001, False),
        ]
)
def test_calcular_preco_insumo_raises(estufa: EstufaAgrotech, preco_base: float, eh_vip: bool) -> None:
    with pytest.raises(ValueError, match="Preço não pode ser negativo") as exc:
        estufa.calcular_preco_insumo(preco_base, eh_vip)
    assert exc.type is ValueError

@pytest.mark.xfail(strict=True, raises=AssertionError, reason='Estes valores deveriam causar erro')
@pytest.mark.parametrize(
        "preco_base, eh_vip, expected",
        [
            (10., False, 7.),
            (10., True, 10.),
            (5., False, 3.),
            (5., True, 8.),
            (2.5, False, 6),
            (2.5, True, 1.),
            
        ]
)
def test_calcular_preco_insumo_should_fail(estufa: EstufaAgrotech, preco_base: float, eh_vip: bool, expected: float) -> None:
    observed = estufa.calcular_preco_insumo(preco_base, eh_vip)
    assert observed == pytest.approx(expected, 1e-2), f"{observed!r} == {expected!r}"

@pytest.mark.parametrize(
        "preco_base, eh_vip, expected",
        [
            (10., False, 10.),
            (10., True, 8.),
            (5., False, 5.),
            (5., True, 4.),
            (2.5, False, 2.5),
            (2.5, True, 2.),
            (1., False, 1.),
            (1., True, 0.8),
            (0.5, False, 0.5),
            (0.5, True, 0.4),
            (0.25, False, 0.25),
            (0.25, True, 0.2),
            (0.2, False, 0.2),
            (0.2, True, 0.16),
            (0.05, False, 0.05),
            (0.05, True, 0.04),
            (0.03, False, 0.03),
            (0.03, True, 0.02),
            
        ]
)
def test_calcular_preco_insumo_ok(estufa: EstufaAgrotech, preco_base: float, eh_vip: bool, expected: float) -> None:
    observed = estufa.calcular_preco_insumo(preco_base, eh_vip)
    assert observed == pytest.approx(expected, 1e-2), f"{observed!r} == {expected!r}"

@pytest.mark.parametrize(
    "quantidade_kg",
    [
        (6000.),
        (5001.),
        (5000.1),
        (5000.01),
        (5000.001),
        
    ]
)
def test_processar_carga_insumo_up_raises(estufa: EstufaAgrotech,quantidade_kg: float) -> None:
    with pytest.raises(ValueError, match="Capacidade máxima excedida") as exc:
        estufa.processar_carga_insumo(quantidade_kg)
    assert exc.type is ValueError

@pytest.mark.skip(reason='Operação ainda não desenvolvida')
@pytest.mark.parametrize(
    "quantidade_kg",
    [
        (-0.001),
        (-0.01),
        (-0.1),
        (-1),
        (-10),
        (-100),
    ]
)
def test_processar_carga_insumo_bottom_raises(estufa: EstufaAgrotech, quantidade_kg: float) -> None:
    with pytest.raises(ValueError) as exc:
        estufa.processar_carga_insumo(quantidade_kg)
    assert exc.type is ValueError

@pytest.mark.skipif(not sys.platform.startswith('win'), reason='should not work on windows')
@pytest.mark.parametrize(
    "quantidade_kg",
    [
        (5000.),
        (4999.999),
        (4999.99),
        (4999.9),
        (4999.),
        (2500.),
        (1.),
        (0.1),
        (0.01),
        (0.001),
        (0.),
    ]
)
def test_processar_carga_insumo_ok(estufa: EstufaAgrotech, quantidade_kg: float) -> None:
    observed = estufa.processar_carga_insumo(quantidade_kg)
    assert observed,  f"{observed!r} == {True!r}"

@pytest.mark.parametrize(
    "mensagem",
    [
        ("teste"),
        ("..."),
        ("."),
        (""),
    ]
)
def test_registrar_log_ok(estufa: EstufaAgrotech, mensagem: str)-> None:
    observed = estufa.registrar_log(mensagem)
    assert observed

@pytest.mark.parametrize(
    "mensagem",
    [
        ("teste"),
        ("..."),
        ("."),
        (""),
    ]
)
def test_registrar_log_raises(estufa: EstufaAgrotech, logger_raise: ServicoLogger, mensagem: str)-> None:
    estufa.logger = logger_raise
    with pytest.raises(RuntimeError, match="Erro ao gravar log: .*") as exc:
        estufa.registrar_log(mensagem)
    assert exc.type is RuntimeError
