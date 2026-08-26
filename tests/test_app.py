from app import EstufaAgrotech
import pytest

@pytest.fixture
def log_temporario(tmp_path):
    """Cria um arquivo temporário isolado para gravar logs de teste."""
    return str(tmp_path / "estufa_status.log")





@pytest.fixture
def estufa():
    e = EstufaAgrotech()
    return e

@pytest.mark.parametrize(
    "atual, esperado",
    [(-1.0,"ALERTA: Geada"),
     (5.0,"Normal"),
     (40.1,"ALERTA: Superaquecimento"),
     (100.0,"ALERTA: Superaquecimento"),
     (-15.0,"ALERTA: Geada"),
     (0.0,"Normal"),
     (-0.5,"ALERTA: Geada"),
     (41.0,"ALERTA: Superaquecimento")
    ],
    ids =["Geada", "Normal", "Superaquecimento","Superaquecimento", "Geada", "Normal", "Geada", "Superaquecimento"],
)

# TEST CASE 1
def test_verificar_temperatura(estufa,atual, esperado):
    estufa.temperatura_atual = atual
    assert estufa.verificar_status_temperatura() == esperado

@pytest.mark.parametrize(
    "atual, esperado",
    [(300, True),
     (900, True),
     (-300, True),
    ],
    ids =["dentro do limite positivo", "dentro do limite positivo","dentro do limite negativo"],
        
)

# TESTE_CASE 3
def test_capacidade_de_carga_estufa(estufa, atual, esperado):
    estufa.processar_carga_insumo(atual) == esperado


@pytest.mark.parametrize(
    "atual, eh_vip, esperado",
    [(150.250, True, round((150.0*0.8),2)),
     (300.230,True,round((300.0*0.8),2)),
     (0.0, True,round((0.0*0.8),2)),
     (150.250, False, round(150.250,2)),
     (300.211,False,round(300.211,2)),
     (0.023, False,round(0.023,2)),
     
    ],
    ids =["preco_vip", "preco_vip","preco_vip", "preco_nao_vip", "preco_nao_vip", "preco_nao_vip"],       
)
# TESTE_CASE 2
def test_precos_incorretos(estufa, atual, eh_vip, esperado):
    estufa.calcular_preco_insumo(atual, eh_vip) == esperado



@pytest.mark.parametrize(
    "preco_invalido, eh_vip",
    [(-300.0, True),
     (-900.0, False),
     (-1.0, False),
    ],
    ids =["preco_invalido", "preco_invalido", "preco_invalido"],
        
)
# TESTE_CASE 2
def test_preco_invalido(estufa, eh_vip, preco_invalido):
    with pytest.raises(ValueError):
        estufa.calcular_preco_insumo(preco_invalido, eh_vip)


@pytest.mark.parametrize(
    "preco_invalido",
    [(7000.0),
     (6000.0),
     (100000.0),
    ],
    ids =["preco_invalido", "preco_invalido", "preco_invalido"],
        
)
# TESTE_CASE 3
def test_carga_maxima_excedida(estufa, preco_invalido):
    with pytest.raises(ValueError):
        estufa.processar_carga_insumo(preco_invalido)