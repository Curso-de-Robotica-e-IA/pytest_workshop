import pytest
import sys

"""
TEST CASE 1:
Alteração dinâmica das respostas de leitura de temperatura em tempo de 
execução para testar cenários de emergência (Geada e Superaquecimento).
"""

@pytest.mark.parametrize(
    "temperatura, resultado_esperado",
    [
        (25.0, "Normal"),
        (-5.0, "ALERTA: Geada"),
        (45.0, "ALERTA: Superaquecimento"),
    ]
)
def test_verificar_status_temperatura(estufa, monkeypatch, temperatura, resultado_esperado):
    monkeypatch.setattr(estufa, 'temperatura_atual', temperatura)
    assert estufa.verificar_status_temperatura() == resultado_esperado

"""
TEST CASE 2:
Teste de múltiplos cenários de regras de negócio de preços e descontos VIP.
Teste em lote com dados e limites inválidos.
"""

@pytest.mark.parametrize(
    "preco_base, eh_vip, resultado_esperado",
    [
        (100.0, True, 80.0),
        (100.0, False, 100.0),
        (50.0, True, 40.0),
    ]
)
def test_calcular_preco_insumo(estufa, monkeypatch, preco_base, eh_vip, resultado_esperado):
    monkeypatch.setattr(estufa, 'preco_base', preco_base)
    monkeypatch.setattr(estufa, 'eh_vip', eh_vip)
    assert estufa.calcular_preco_insumo(estufa.preco_base, estufa.eh_vip) == resultado_esperado

"""
TEST CASE 3: 
Validação do lançamento de `ValueError` para preços incorretos.
Validação do lançamento de exceção ao tentar processar dados fora do limite permitido.
"""

@pytest.mark.parametrize(
    "preco_base, eh_vip",
    [
        (-10.0, True),
        (-5.0, False),
    ]
)
def test_calcular_preco_insumo_excecao(estufa, monkeypatch, preco_base, eh_vip):
    monkeypatch.setattr(estufa, 'preco_base', preco_base)
    monkeypatch.setattr(estufa, 'eh_vip', eh_vip)
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(preco_base, eh_vip)


@pytest.mark.parametrize(
    "quantidade_kg, resultado_esperado",
    [
        (1000.0, True),
        (5000.0, True),
    ]
)
def test_processar_carga_insumo(estufa, monkeypatch, quantidade_kg, resultado_esperado):
    monkeypatch.setattr(estufa, 'quantidade_kg', quantidade_kg)
    assert estufa.processar_carga_insumo(quantidade_kg) == resultado_esperado

@pytest.mark.parametrize(
    "quantidade_kg",
    [
        (6000.0),
    ]
)
def test_processar_carga_insumo_excecao(estufa, monkeypatch, quantidade_kg):
    monkeypatch.setattr(estufa, 'quantidade_kg', quantidade_kg)
    with pytest.raises(ValueError):
        estufa.processar_carga_insumo(quantidade_kg)

"""
TEST CASE 4: 
Ignora recursos em planejamento/desenvolvimento.
Condiciona a execução ao sistema operacional (ex: apenas Linux).
Registra falhas conhecidas tratadas como débitos técnicos.
"""

@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Funcionalidade em planejamento/desenvolvimento")
def test_funcionalidade_em_planejamento_desenvolvimento():
    pass

def test_estufa_registrar_log(estufa, monkeypatch, log_temporario):
    monkeypatch.setattr(estufa.logger, 'caminho_arquivo', log_temporario)
    assert estufa.registrar_log("Mensagem de teste") is True

def test_logar_operacao_excecao(estufa, monkeypatch):
    monkeypatch.setattr(estufa.logger, 'caminho_arquivo', None)
    with pytest.raises(RuntimeError, match="Erro ao gravar log"):
        estufa.logger.logar_operacao("Mensagem de teste")
