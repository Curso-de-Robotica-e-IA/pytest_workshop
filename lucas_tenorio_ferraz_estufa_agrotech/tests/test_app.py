import pytest
import platform


@pytest.mark.parametrize("temp, expected",
                         [(40,"Normal"),(50,"ALERTA: Superaquecimento"),
                          (-10,"ALERTA: Geada"),(0,"Normal"),(20,"Normal")],
                          ids=[f"{i}" for i in [40,50,-10,0,20]])
def test_verificar_status_temperatura(est,temp, expected):
    #case 1
    print(temp)
    est.temperatura_atual = temp
    result = est.verificar_status_temperatura()
    assert expected == result
    
@pytest.mark.parametrize("preço, vip, expected",
                         [(-10,"ValueError",9),(10.879,False,10.88),(9.4949,False,9.49),
                          (20,True,16),(111.1111,True,88.89),(55.5555,True,44.44)]
                          )#,ids=[f"{i}" for i in [40,50,-10,0,20]])
def test_calcular_preco_insumo(est,preço,vip,expected):
    #case 2A,2B?,3A,3B
    if preço<0:
        with pytest.raises(ValueError):
            est.calcular_preco_insumo(preço,vip)
    else: 
        assert expected == est.calcular_preco_insumo(preço,vip)
@pytest.mark.parametrize("val, expected",
                         [(5000.0001,False),
                          (5000,True),
                          (-5555,True),
                          (4444,True),
                          (111.1111,True)]
                          )
def test_processar_carga_insumo(est,val,expected):
    #case 2B?,3B
    if expected:
        assert est.processar_carga_insumo(val) == True
    else:
        with pytest.raises(ValueError):
            est.processar_carga_insumo(val)
    
@pytest.mark.skip(reason="Operação avançada ainda em desenvolvimento")
def test_case_4A(est,temperature):
    est.change_temperature(temperature)

@pytest.mark.skipif(platform.system().lower() != "windows",reason="Operação avançada ainda em desenvolvimento")
def test_case_4B_Windows(est):
    msg = "Test_MSG Windows"
    est.registrar_log(msg)
    with open(est.logger.caminho_arquivo,"r") as f:
        for line in f:
            pass
        last_line = line
    assert last_line == msg+"\n"

@pytest.mark.skipif(platform.system().lower() != "linux",reason="Operação avançada ainda em desenvolvimento")
def test_case_4B_Linux(est):
    msg = "Test_MSG Windows"
    est.registrar_log(msg)
    with open(est.logger.caminho_arquivo,"r") as f:
        for line in f:
            pass
        last_line = line
    assert last_line == msg+"\n"


@pytest.mark.xfail(reason="Strings onde deveria ser numero")
@pytest.mark.parametrize("val, expected",
                         [("A",False)]
                          )
def test_case_4c(est,val,expected):
    assert est.processar_carga_insumo(val) == expected

def test_File_Error(est):
    est.logger.caminho_arquivo = "\\FakeFolder\\estufa_status.log"
    msg = "Test_MSG Windows"
    with pytest.raises(RuntimeError):
        est.registrar_log(msg)

