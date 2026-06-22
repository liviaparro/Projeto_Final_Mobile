import requests

base_url = "http://10.135.232.26:5000"

def post_movimentacao(codigo):
    url = base_url + '/rastreio'
    rastreamento = {"codigo": codigo }
    dados = requests.post(url, json=rastreamento)
    return dados.json()