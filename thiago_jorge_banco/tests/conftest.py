import pytest
import requests
from datetime import datetime
from src.thiago_jorge_banco.banco import ContaBancaria, buscar_cotacao_dolar

@pytest.fixture
def conta_zerada():
    instancia = ContaBancaria("Teste")
    return instancia

@pytest.fixture
def conta_com_saldo():
    instancia = ContaBancaria("Teste", 1000)
    return instancia

@pytest.fixture
def mock_response_api(mocker):
    mock_api_request = mocker.Mock()
    mock_api_request.json.return_value = {"valor": 5.18}
    mocker.patch("requests.get", return_value=mock_api_request)
    
    result = buscar_cotacao_dolar()
    return result

@pytest.fixture
def cotacao_dolar_dia():
    now = datetime.now().strftime("%m-%d-%Y")
    resposta = requests.get(f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao={now!r}&$top=100&$format=json", timeout=5)
    dados = resposta.json()
    return dados['value'][0]

@pytest.fixture
def cotacao_dolar_data_especifica():
    def _cotacao(data):
        """Retorna cotação do dolar de uma data especifca
        Args:
            data (str): 
        Returns:
            list[dict]: Retorno da API          
        """
        resposta = requests.get(f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoDolarDia(dataCotacao=@dataCotacao)?@dataCotacao={data!r}&$top=100&$format=json", timeout=5)
        dados = resposta.json()
        return dados['value'][0]
    return _cotacao