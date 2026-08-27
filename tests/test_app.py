import pytest
from tests.conftest import *
import sys



@pytest.mark.parametrize(
    "temp_simulada, status_esperado",
    [
        (-1.0, "ALERTA: Geada"),
        (41.0, "ALERTA: Superaquecimento"),
        (25.0, "Normal"),
    ],
)
def test_verificar_status_temperatura(estufa, temp_simulada, status_esperado, monkeypatch):
    monkeypatch.setattr(estufa, "temperatura_atual", temp_simulada)
    assert estufa.verificar_status_temperatura() == status_esperado


@pytest.mark.parametrize(
    "preco_base, eh_vip, preco_esperado",
    [
        (100.0, True, 80.0),
        (100.0, False, 100.0), 
        (49.99, True, 39.99),   
    ],
)
def test_calcular_preco_insumo_sucesso(estufa, preco_base, eh_vip, preco_esperado):
    assert estufa.calcular_preco_insumo(preco_base, eh_vip) == preco_esperado


def test_calcular_preco_insumo_invalido(estufa):
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(-10.0, False)


def test_processar_carga_insumo_limite_excedido(estufa):
    with pytest.raises(ValueError, match="Capacidade máxima excedida"):
        estufa.processar_carga_insumo(5000.1)


def test_processar_carga_insumo_sucesso(estufa):
    assert estufa.processar_carga_insumo(5000.0) is True


def test_registrar_log_sucesso(estufa):
    assert estufa.registrar_log("Log de teste estufa") is True


def test_logar_operacao_exception(logger, monkeypatch):
    monkeypatch.setattr(logger, "caminho_arquivo", "/caminho_invalido/log.txt")
    with pytest.raises(RuntimeError):
        logger.logar_operacao("Teste de erro")


def test_logar_operacao_servico_sucesso(logger):
    assert logger.logar_operacao("Log no ServicoLogger") is True




@pytest.mark.skip(reason="Teste ainda em processo de desenvolvimento")
def test_em_planejamento_e_em_desenvolvimento(estufa):
    pass


@pytest.mark.skipif(
    not sys.platform.startswith("linux"),
    reason="Teste condicionado ao SO linux",
)
def test_leitura_sensor_hardware(estufa):
    pass

@pytest.mark.xfail(reason="Falhas conhecidas")
def test_precisao_extrema_sensor(estufa):
    assert estufa.temperatura_atual == 22.000e01
