import sys

import pytest

#Teste de caso 1
@pytest.mark.parametrize(
    "valor, esperado", 
    [
        (-1, "ALERTA: Geada"),
        (45, "ALERTA: Superaquecimento"),
        (0, "Normal"),
        (40, "Normal"),
        (30, "Normal")
    ],
    ids = ["abaixo do mínimo", "acima do máximo", "limiar mínimo", "limiar máximo", "entre limiares"],)
def test_leitura_temperatura(estufa, valor, esperado, monkeypatch):
    
    monkeypatch.setattr(estufa, "temperatura_atual", valor)
    assert estufa.verificar_status_temperatura() == esperado

#Teste de caso 2

@pytest.mark.parametrize(
    "preco, vip, esperado",
    [
        (10, True, 8.00),
        (100, False, 100.00),
        (0, True, 0.00),
        (0, False, 0.00),
    ],
    ids = ["acima do limiar com vip",
    "acima do limiar sem vip",
    "limiar com vip",
    "limiar sem vip"],
)

def test_calcular_preco_insumo(estufa, preco, vip, esperado):
    assert estufa.calcular_preco_insumo(preco, vip) == esperado


#Teste de caso 3
def test_calcular_preco_insumo_com_exception(estufa):
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(-1, False)

@pytest.mark.xfail(reason=NotImplemented)
def test_processar_carga_insumo_além_do_limite(estufa):
    with pytest.raises(ValueError):
        estufa.processar_carga_insumo(-1)

#Teste de caso 4
pytest.mark.skip
def test_ignora_recursos(estufa):
    pass

@pytest.mark.skipif(sys.platform.startswith("windows"), reason="Não roda no Windows")
def test_ignora_se_windows(estufa):
    pass


