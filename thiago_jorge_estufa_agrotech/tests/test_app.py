import pytest
import sys
@pytest.mark.parametrize(
    "temp, esperado",
    [
        (-20.0, "ALERTA: Geada"),
        (50, "ALERTA: Superaquecimento"),
        (40, "Normal"),
        (0, "Normal")
    ]
)
def test_leituras_temperaturas(estufa, temp, esperado, monkeypatch):
    monkeypatch.setattr(estufa, "temperatura_atual", temp)
    assert estufa.verificar_status_temperatura() == esperado

@pytest.mark.parametrize(
    "preco, vip, esperado",
    [
        (2000.0, False, 2000.0),
        (2000.0, True, 1600.0),
    ]
)
def test_preco_incorreto(estufa, preco, vip, esperado):
    assert estufa.calcular_preco_insumo(preco, vip) == esperado

def test_preco_negativo(estufa):
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(-2000, False)

def test_processar_carga_insumo(estufa):
    assert estufa.processar_carga_insumo(5000) == True 

def test_processar_carga_insumo_exception(estufa):
    with pytest.raises(ValueError):
        assert estufa.processar_carga_insumo(5001) 

def test_registrar_log(estufa, logger, log_temporario, monkeypatch):
    log_temporario = "test_estufa_status.log"
    monkeypatch.setattr(logger, "caminho_arquivo", log_temporario)
    monkeypatch.setattr(estufa, "logger", logger)
    assert estufa.registrar_log("teste") == True

def test_registrar_log_exception(estufa, logger, monkeypatch):
    monkeypatch.setattr(logger, "caminho_arquivo", None)
    monkeypatch.setattr(estufa, "logger", logger)
    with pytest.raises(RuntimeError):
        estufa.registrar_log("teste")

@pytest.mark.skip()
def test_em_desenvolvimento():
    ...

@pytest.mark.xfail()
def test_preco_incorreto_fail(estufa):
    assert estufa.processar_carga_insumo(-2e308) == True

@pytest.mark.skipif(
    sys.platform != "linux",
    reason="Só irá rodar no linux"
)
def test_apenas_linux(estufa):
    assert estufa.processar_carga_insumo(1000) == True