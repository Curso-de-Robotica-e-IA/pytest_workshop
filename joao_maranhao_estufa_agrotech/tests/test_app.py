import pytest
import sys

MOCK_INPUT_STATUS_TEMPERATURA = [35,60,-5,0]
MOCK_EXPECTED_STATUS_TEMPERATURA = [
    "Normal", "ALERTA: Superaquecimento", 
    "ALERTA: Geada", "Normal"
]
MOCK_BASE_PRECO_NEGATIVO = [-15, -10]

# 1 A
@pytest.mark.parametrize(
    "input, expected",
    [
        (input, expected)
        for input, expected in zip(
            MOCK_INPUT_STATUS_TEMPERATURA, 
            MOCK_EXPECTED_STATUS_TEMPERATURA
        )
    ],
    ids=[f"temp_{i}" for i in MOCK_INPUT_STATUS_TEMPERATURA])
def teste_status_temperatura(mock, input, expected):
    """
        Testagem da alteração dinâmica das respostas de leitura de temperatura 
        em tempo de execução para testar cenários de emergência (Geada 
        e Superaquecimento).

        args: 
            mock - objeto que endereça o método a ser testado
            input - entrada estática
            expected - checagem de saída estática
    """
    mock.temperatura_atual = input
    result = mock.verificar_status_temperatura()
    assert expected == result

# 2 AB
@pytest.mark.parametrize(
    "preco_base, eh_vip, preco_esperado",
    [
        (0, True, 0),
        (5, True, 4),
        (15, True, 12),
        (5, False, 5),
        (15, False, 15),
    ],
)
def teste_calcula_preco_insumo(mock, preco_base, eh_vip, preco_esperado):
    """
        Teste de retorno de preço com base em diferentes clientes, VIPs ou Não.

        args:
            preco_base - preço para base do cálculo de desconto
            vip - flag que indica se é VIP ou NÃO
            preco_esperado - preço no valor exato de saída
    """
    preco_insumo = mock.calcular_preco_insumo(preco_base, eh_vip)
    assert preco_insumo == preco_esperado


# 3 AB
@pytest.mark.parametrize("preco_base", MOCK_BASE_PRECO_NEGATIVO)
def teste_preco_negativo(mock, preco_base, eh_vip=True):
    """
        Teste de rejeição de preço negativo ao calcular preço de insumo.

        args:
            preco_base - preço para base do cálculo de desconto
            vip - flag que indica se é VIP ou NÃO
    """
    with pytest.raises(ValueError, match="Preço não pode ser negativo"):
        mock.calcular_preco_insumo(preco_base, eh_vip)

# 4 A
@pytest.mark.skip(reason="Operação avançada ainda em desenvolvimento")
def teste_estabilizar_temperatura(est,temperatura_alvo):
    est.estabilizar_temperatura(temperatura_alvo)

# 4 B

@pytest.mark.skipif(sys.platform != "linux", reason="Requer sistema Linux")
def teste_apenas_no_linux():
    assert True

# 4 C
@pytest.mark.xfail(reason="String ao invés de número")
def teste_input_processar_carga_insumo(mock):
    assert mock.processar_carga_insumo("12") == 12
