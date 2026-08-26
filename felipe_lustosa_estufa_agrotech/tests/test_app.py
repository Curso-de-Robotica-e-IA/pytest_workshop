import pytest
import platform

# TEST CASE 1
@pytest.mark.parametrize(
   "temp, esperado",
   [
       (-20.0, "ALERTA: Geada"),
       (0.0, "Normal"),
       (20.0, "Normal"),
       (40.0, "Normal"),
       (50.0, "ALERTA: Superaquecimento"),
   ],
   ids=["negativo", "zero", "no intervalo", "igual a 40", "maior que 40"],
)
def test_cenarios_emergencia(estufa, temp, esperado, monkeypatch):
   monkeypatch.setattr(estufa, "temperatura_atual", temp)
   alerta = estufa.verificar_status_temperatura()
   assert alerta == esperado

# TEST CASE 2
@pytest.mark.parametrize(
   "preco_base, eh_vip, esperado",
   [
      (10.0, True, 8.00),
      (10.0, False, 10.00),
      (0.0, True, 0.00),
      (0.0, False, 0.00),
   ],
   ids=["vip", "normal", "zero vip", "zero normal"],
)
def test_preco_insumo(estufa, preco_base, eh_vip, esperado):
   preco = estufa.calcular_preco_insumo(preco_base, eh_vip)
   assert preco == esperado


# TEST CASE 3
# a.
def test_preco_insumo_menor_que_zero(estufa):
   with pytest.raises(ValueError):
      estufa.calcular_preco_insumo(-10.0, True)

# b.
@pytest.mark.xfail(reason="lançamento de exceção ao tentar processar dados fora do limite permitido")
def test_preco_insumo_menor_que_zero(estufa):
   preco = estufa.calcular_preco_insumo(-10.0, True)
   assert preco == 10

    
# TEST CASE 4
# a.
@pytest.mark.skip(reason="Operação de registrar log ainda em desenvolvimento")
def test_registrar_log():
   pass

@pytest.mark.skipif(
   platform.system() == "Linux",
   reason="Sensor de hardware não está acoplado nesta versão do ambiente",
)
def test_logar_operacao():
   pass

def test_carga_maior_que_limite(estufa):
   with pytest.raises(ValueError):
      estufa.processar_carga_insumo(6000.0)

def test_carga_dentro_do_limite(estufa):
   assert estufa.processar_carga_insumo(3000.0) == True

def test_registrar_log(estufa):
   log = estufa.registrar_log("teste")
   assert log == True

def test_registrar_log_exception(estufa):
   with pytest.raises(RuntimeError):
      # monkeypatch.setattr(estufa, "logger.caminho_arquivo", None)
      estufa.logger.caminho_arquivo = None
      estufa.registrar_log("teste")


