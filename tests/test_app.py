
from sys import exc_info

from hilda_miranda_estufa_agrotech.app import EstufaAgrotech, ServicoLogger
import pytest

def test_logar_operacao_mensagem(tmp_path):

    caminho = tmp_path / "estufa.log"
    logger = ServicoLogger(str(caminho))

    resultado = logger.logar_operacao("temperatura estável")

    assert resultado is True
    assert caminho.read_text(encoding="utf-8") == "temperatura estável\n"

def test_logar_operacao_mensagem_erro(tmp_path):

    caminho = tmp_path / "pasta_inexistente" / "estufa.log"
    logger = ServicoLogger(str(caminho))

    with pytest.raises(RuntimeError, match="Erro ao gravar log"):
        logger.logar_operacao("mensagem")

def test_verificar_status_temperatura_normal():

    estufa = EstufaAgrotech(temperatura_inicial=22.0)

    assert estufa.verificar_status_temperatura() == "Normal"

def test_verificar_status_temperatura_geada():

    estufa = EstufaAgrotech(temperatura_inicial=-10.0)

    assert estufa.verificar_status_temperatura() == "ALERTA: Geada"

def test_verificar_status_temperatura_superaquecimento():

    estufa = EstufaAgrotech(temperatura_inicial=45.0)

    assert estufa.verificar_status_temperatura() == "ALERTA: Superaquecimento"

def test_processar_carga_insumo_validar_quantidade_maxima():

    estufa = EstufaAgrotech()
    resultado = estufa.processar_carga_insumo(5000.0)

    assert resultado is True

def test_calcular_preço_insumo_valido_vip():

    estufa = EstufaAgrotech()
    resultado = estufa.calcular_preco_insumo(544654.474654646, True)

    assert resultado == 435723.58

def test_calcular_preço_insumo_valido():

    estufa = EstufaAgrotech()
    resultado = estufa.calcular_preco_insumo(544654.474654646, False)

    assert resultado == 544654.47

def test_calcular_preço_insumo_invalido():

    estufa = EstufaAgrotech()

    with pytest.raises(ValueError, match="Preço não pode ser negativo"):
        estufa.calcular_preco_insumo(-5001.0, True)

def test_processar_carga_insumo_validar_quantidade_maxima_erro():

    estufa = EstufaAgrotech()

    with pytest.raises(ValueError, match="Capacidade máxima excedida"):
        estufa.processar_carga_insumo(5001.0)

def test_registrar_log_estufa_mensagem(tmp_path):

    caminho = tmp_path / "estufa_status.log"
    logger = ServicoLogger(str(caminho))
    estufa = EstufaAgrotech(logger=logger)

    resultado = estufa.registrar_log("temperatura estável")

    assert resultado is True
    assert caminho.read_text(encoding="utf-8") == "temperatura estável\n"
