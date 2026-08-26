import sys
import pytest
import platform

from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from ygor_matos_estufa_agrotech.app import ServicoLogger, EstufaAgrotech

@pytest.fixture
def instancia_logger():
    #instanciando um logger 
    instancia = ServicoLogger('logs_test.txt')
    return instancia

@pytest.fixture
def instancia_estufa(instancia_logger):
    instancia = EstufaAgrotech(25, instancia_logger)
    return instancia

def test_temperatura_geada(instancia_estufa, monkeypatch):
    monkeypatch.setattr(instancia_estufa,"temperatura_atual", -50)
    assert instancia_estufa.verificar_status_temperatura() == 'ALERTA: Geada'


def test_temperatura_superaquecimento(instancia_estufa, monkeypatch):
    monkeypatch.setattr(instancia_estufa,"temperatura_atual", 50)
    assert instancia_estufa.verificar_status_temperatura() == 'ALERTA: Superaquecimento'

def test_temperatura_normal(instancia_estufa):
    assert instancia_estufa.verificar_status_temperatura() == 'Normal'

def test_calcular_preco_insumo_negativo(instancia_estufa):
    with pytest.raises(ValueError):
        instancia_estufa.calcular_preco_insumo(-1,False)

@pytest.mark.parametrize(
    'preco, vip, resultado',
    [
        #(-1,False,ValueError("Preço não pode ser negativo")),
        (10,False,10),
        (10,True,8)
    ],
)
def test_calcular_preco_insumo(instancia_estufa, preco, vip, resultado):
    preco = instancia_estufa.calcular_preco_insumo(preco,vip)
    assert preco == resultado

def test_carga_insumo_acima_do_limite(instancia_estufa):
    with pytest.raises(ValueError):
        instancia_estufa.processar_carga_insumo(5001)

def test_carga_insumo_abaixo_do_limite(instancia_estufa):
    assert instancia_estufa.processar_carga_insumo(1) == True

@pytest.mark.skip
def test_funcao_incompleta(instancia_estufa):
    assert instancia_estufa.funcao_incompleta() == 'essa funcao nao foi escrita ainda'

@pytest.mark.skipif(
    platform.system()=="Windows" or platform.system()=="Darwin", reason="esse teste só roda em Linux"
)

@pytest.mark.xfail
def test_system(instancia_estufa):
    teste = instancia_estufa.calcular_preco_insumo("vai dar erro", True)
    assert teste == 10
