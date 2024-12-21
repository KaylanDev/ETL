import time
import requests
import tinydb
from tinydb import TinyDB
from datetime import datetime


def get_api_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    return dados

def dados_organizados(dados):
    valor = dados["data"]["amount"]
    moeda = dados["data"]["currency"]
    cripto = dados["data"]["base"]
    timestamp = datetime.now().timestamp()
    
    dados_transformados = {
       "valor" : valor,
       "moeda" :  moeda,
       "cripto" : cripto,
       "time" : timestamp
    }
    return dados_transformados

def salvando_banco_bitcoint(dados,name_db = "bitcoin.json"):
    db = TinyDB(name_db)
    db.insert(dados)
    print("Dados salvos com sucesso!")

if __name__ == "__main__":
    while True:
     dados_json = get_api_bitcoin()
     dados_tratados = dados_organizados(dados_json)
     salvando_banco_bitcoint(dados_tratados)
     time.sleep(15)

