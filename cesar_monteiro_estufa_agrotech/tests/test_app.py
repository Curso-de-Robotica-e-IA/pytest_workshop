from platform import system

from cesar_monteiro_estufa_agrotech.src.cesar_monteiro_estufa_agrotech.app import EstufaAgrotech

import pytest
import sys

def test_temeratura(estufa):
    """Testa a verificação do staus da temperatura quando normal"""
    estufa.temperatura_atual = 25.5
    assert estufa.verificar_status_temperatura() == "Normal"
    
def test_verificar_status_temp_modificada(estufa, monkeypatch):
    """ Testa modificando a temperatura para um valor de alerta, utilizando monkeypatch"""
    monkeypatch.setattr(estufa, "temperatura_atual", 45.0)
    assert estufa.verificar_status_temperatura() == "ALERTA: Superaquecimento"

@pytest.mark.parametrize(
    "temperatura, alerta_esperado",
    [
        (25.0, "Normal"),
        (-5.0, "ALERTA: Geada"),
        (45.0, "ALERTA: Superaquecimento"), 
    ]
)            
def test_verificar_todas_temp(estufa, temperatura, alerta_esperado):
    """ Testa todas as condições de temperatura usando parametrização"""
    estufa.temperatura_atual = temperatura
    assert estufa.verificar_status_temperatura() == alerta_esperado

@pytest.mark.parametrize(
    "preco_base, eh_vip, preco_esperado",
    [
        (100.0, True, 80.0),
        (100.0, False, 100.0),
        (50.0, True, 40.0),
        (50.0, False, 50.0),
        (0.0, True, 0.0)
    ]
)    
def test_preco_insumo(estufa, preco_base, eh_vip, preco_esperado):
    """Testa múltiplos cenarios de calculos com  vários cenários de regras de negocios"""
    estufa.preco_base = preco_base
    estufa.eh_vip = eh_vip
    preco = estufa.calcular_preco_insumo(preco_base, eh_vip)
    assert preco == preco_esperado  
    
def test_preco_insumo_negativo(estufa, monkeypatch):
    """Testa se a função lança ValueError para preço negativo"""
    
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(-15.0, False)       

@pytest.mark.parametrize(
    "preco_base, eh_vip, preco_esperado",
    [
        (100, False, 100),
        (100, True, 80),
        (0, True, 0),       
    ]
)
def test_preco_insumo_limites_invalidos(estufa, preco_base, eh_vip, preco_esperado):
    """Testa cenários com limites inválidos"""
    preco = estufa.calcular_preco_insumo(preco_base, eh_vip)
    assert preco == preco_esperado
    
def test_process_carga_insumo(estufa):
    """Testa a função de processamento de carga 'de insumo"""
    with pytest.raises(ValueError):
        estufa.processar_carga_insumo(10000)  

def test_registrar_log(estufa):
    """Testa a função de registro de log"""
    res = estufa.registrar_log("Teste de log")
    assert res is True    
    
@pytest.mark.skipif(
    
    sys.platform!= "Linux", reason = "System runs linus only."
)
    
def test_sistema_operacional(estufa):
    pass
    

@pytest.mark.skip(reason = "For demonstration purposes this test is skipped.")
def test_skip(estufa):
    pass

@pytest.mark.xfail(reason = "For demonstration purposes this test is expected to fail.")
def test_processar_carga_insumo(estufa):
    """Testa a função de processamento de carga de insumo"""
    with pytest.raises(ValueError):
        estufa.processar_carga_insumo(-10000)
        
        
