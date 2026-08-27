import pytest
#from src.matheus_passos_estufa_agrotech.app import *
import sys
from src.matheus_passos_estufa_agrotech.banco import SaldoInsuficienteError, ValorInvalidoError


@pytest.mark.parametrize(
        "temperature, expected_output",
        [
            (10.0, "Normal"), #Testing normal value
            (0.0, "Normal"), #Testing min threshold
            (40.0, "Normal"), #Testing max threshold
            (-0.1, "ALERTA: Geada"), #Testing bellow threshold (slightly)
            (-10.0, "ALERTA: Geada"),
            (40.1, "ALERTA: Superaquecimento"), #Testing above threshold
            (60.0, "ALERTA: Superaquecimento")
        ],
        ids =["Normal Value : 10", "Value equals threshold (min)", "Value equals threshold (max)",
              "Bellow min threshold : Slighlty bellow (0.1)", "Bellow min threshold",
              "Above max threshold : Slightly above (0.1)", "Above max threshold"
              ]
        )
def test_temperature_changes_during_runtime(create_agrotech, monkeypatch,temperature, expected_output):
    monkeypatch.setattr(create_agrotech, "temperatura_atual", temperature)
    result = create_agrotech.verificar_status_temperatura()
    assert result == expected_output


@pytest.mark.parametrize(
        "base_price, is_vip, expected_price",
        [
            (100.0 , False, 100), 
            (100.0, True, 80),
            (6.0 , True, 4.8), #Testing the rounding.
            (0.0 , True, 0.0 ), #Testing neutral (0)
            (-10.0, False, None), #Testing value error, since it is negative.
            (-10.0, True, None)
        ],
        )
def test_price_calculation(create_agrotech, base_price, is_vip, expected_price):
    if expected_price != None:
        #Assert values
        assert create_agrotech.calcular_preco_insumo(base_price, is_vip) == expected_price
    else:
        #Test for value error
        with pytest.raises(ValueError):
            create_agrotech.calcular_preco_insumo(base_price, is_vip)



@pytest.mark.parametrize(
        "weight, expected_outcome",
        [
            (0.0 , True),
            #(-1.0, None), #Not included in the code.
            (5000.0, True),
            (5000.1, None) #Value error

        ],
        )
def test_load_processing(create_agrotech, weight, expected_outcome):
    if expected_outcome != None:
        assert create_agrotech.processar_carga_insumo(weight) == expected_outcome
    else:
        with pytest.raises(ValueError):
            create_agrotech.processar_carga_insumo(weight)


def test_register_log(create_agrotech):
    assert create_agrotech.registrar_log("test") == True


def test_register_log_exception(create_agrotech):
    create_agrotech.logger.caminho_arquivo = None
    with pytest.raises(RuntimeError):
        create_agrotech.registrar_log("Failed")


@pytest.mark.skip(reason = "Not implemented yet")
def test_not_implemented():
    pass


@pytest.mark.xfail(reason = "Known error")
def test_known_error():
    assert 1 == 2


@pytest.mark.skipif(not sys.platform.startswith('linux'), reason= "This test is for linux only.")
def test_run_only_on_linux():
    assert True == True


#==========================================================================================#
#TESTS FOR BANK APP. REASON : There was a problem where the conftest was not being recognized.
@pytest.mark.parametrize(
        "deposit_value, expected_outcome,_should_raise_error",
        [
            (100, 150,False),
            (-50.0, 50 ,True),
            (0.0, 50,True)
        ],
        )
def test_deposit_module(create_bank_acc, deposit_value, expected_outcome, _should_raise_error): #Tests the deposit method.
    if _should_raise_error:
        with pytest.raises(ValorInvalidoError):
            create_bank_acc.depositar(deposit_value)
    else:
        assert create_bank_acc.depositar(deposit_value) == expected_outcome


def test_get_bank_balance(create_bank_acc):
    assert create_bank_acc.saldo == create_bank_acc._saldo
