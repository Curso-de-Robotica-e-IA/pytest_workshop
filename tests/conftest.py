import banco
import pytest



@pytest.fixture
def criar_conta_bancaria():
    conta = banco.ContaBancaria("Carlos José", 100.0)
    return conta

@pytest.fixture
def deposito_valor_negativo():
    return banco.ContaBancaria("Guilherme Abil", 100.00)

@pytest.fixture
def desconto_com_sucesso():
    return banco.calcular_desconto(1500.00, 50)

@pytest.fixture
def converter_real_dolar():
    return banco.converter_reais_para_dolar(1000)

@pytest.fixture
def juros_composto():
    return banco.calcular_juros_composto(10,15,2)

@pytest.fixture
def modo_debug():
    return banco.esta_em_modo_debug()

