import pytest
import platform
from src.lucas_tenorio_ferraz_banco.banco import ValorInvalidoError as vException,SaldoInsuficienteError as sException

#@pytest.mark.skip("Not a test, used in another function")

@pytest.mark.parametrize("inter, expected,expected2",
                         [([(500.5,"d1 "),(45.75,"s1 ")],454.75,572.35),
                          ([(40.5,"d1 "),(20.25,"d1 "),(10.5,"d1 ")],71.25,572.35),
                          ([(40.5,"d1 "),(20.25,"d1 "),(10.5,"t1 ")],50.25,582.85),
                          ([(40,"d2 "),(20,"d2 "),(90,"s2 ")],0,542.35),
                          ([(40,"d1 "),(20,"s1 "),(92.35,"t2 ")],112.35,480),
                          ([(-35.5,"d2v"),],0,572.35),
                          ([(-35.5,"s2v"),],0,572.35),
                          ([(-35.5,"t2v"),],0,572.35),
                          ([(35.5,"s1e"),],0,572.35),
                          ([(2.5,"t1e"),],0,572.35)])
def test_saldo(bank,bank2,inter, expected,expected2):
    def selectFun(d,val):#Select  the method to test
        try:
            match(d):
                case "s1": return bank.sacar(val)
                case "t1": return bank.transferir(bank2,val)
                case "d1": return bank.depositar(val)
                case "s2": return bank2.sacar(val)
                case "t2": return bank2.transferir(bank,val)
                case "d2": return bank2.depositar(val)
        except Exception as e:
            raise e

    for v,c in inter:#Test a selection of actions
        if "e" in c:#Test cases with SaldoInsuficienteError
            with pytest.raises(sException):
                selectFun(c[:2],v)
        elif "v" in c:#Test cases with ValorInvalidoError
            with pytest.raises(vException):
                selectFun(c[:2],v)
        else:#Test cases that won't have errors
            selectFun(c[:2],v)

    assert (expected == bank.saldo and expected2 == bank2.saldo)

@pytest.mark.xfail(reason="Valor invalido na hora de criar a conta")
def test_fail_bank(fail_bank):
    x = fail_bank.saldo
    assert x!=0

def test_div(fun_dividir):
    r = fun_dividir(90,3)
    assert 30 == r

@pytest.mark.parametrize("val, d,expected",
                         [(100,3,97),(100,103,-1),(100,-3,-1),(500,55.55,222.25),
                          (100,30,70),(300,3,291),(600,1,594),(1110,30,777)])
def test_desconto(fun_calcular_desconto,val,d,expected):
    if expected<0:#Catch expected errors
        with pytest.raises(vException):
            r = fun_calcular_desconto(val,d)
    else:#Normal execution
        r = fun_calcular_desconto(val,d)
        assert expected == r

@pytest.mark.xfail(reason="Falha de conecção")
def test_dolar(fun_cotarDolar,fun_convert_para_dolar):
    value = 50
    result = fun_convert_para_dolar(value)
    rate = fun_cotarDolar()
    assert result == (round(value/rate),2)

@pytest.mark.parametrize("val, tx,p",
                         [(100,0.01,2),(100,1,-1),(100,-3,-1),
                          (100,0.02,4),(300,0.1,5),(100,-0.02,4)])
def test_juros(fun_juros_comp,val,tx,p):
    
    if p<0:
        with pytest.raises(vException):
            fun_juros_comp(val,tx,p)
    else:
        expected = round(val * ((1 + tx) ** p), 2)
        assert expected == fun_juros_comp(val,tx,p)

def test_debug(fun_debug):
    d = fun_debug()
    assert not d