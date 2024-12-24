from dotenv import load_dotenv
load_dotenv()  # carrega as variáveis do .env

import time
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from database import BitcoinPreco,Base
import os
import psycopg
import logging
import logfire
from logging import basicConfig, getLogger

logfire.configure()
basicConfig(handlers=[logfire.LogfireLoggingHandler()])
logger = getLogger(__name__)
logger.setLevel(logging.INFO)
logfire.instrument_requests()
logfire.instrument_sqlalchemy()


POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB = os.getenv("POSTGRES_DB")


DATABASE_URL = (
    f"postgresql+psycopg://{POSTGRES_USER}:{POSTGRES_PASSWORD}"  
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)


def criar_tabela():
    """Cria a tabela no banco de dados, se não existir."""
    Base.metadata.create_all(engine)
    logger.info("Tabela criada/verificada com sucesso!")


def get_api_bitcoin():
    url = "https://api.coinbase.com/v2/prices/spot"
    response = requests.get(url)
    dados = response.json()
    return dados

def dados_organizados(dados):
    valor = dados["data"]["amount"]
    moeda = dados["data"]["currency"]
    cripto = dados["data"]["base"]
    time = datetime.now()
    
    dados_transformados = {
       "valor": float(valor),
       "moeda": moeda,
       "cripto": cripto,
       "time": time
    }
    return dados_transformados

def salvar_dados_postgres(dados):
    """Salva os dados no banco PostgreSQL."""
    session = Session()
    novo_registro = BitcoinPreco(**dados)
    session.add(novo_registro)
    session.commit()
    session.close()
    logger.info(f"[{dados['time']}] Dados salvos no PostgreSQL!")



if __name__ == "__main__":
 criar_tabela()
 logger.info("Iniciando ETL com atualização a cada 15 segundos... (CTRL+C para interromper)")
 while True:
        try:
            dados_json = get_api_bitcoin()
            if dados_json:
                dados_tratados = dados_organizados(dados_json)
                logger.info("Dados Tratados:", dados_tratados)
                salvar_dados_postgres(dados_tratados)
            time.sleep(15)
        except KeyboardInterrupt:
            logger.info("\nProcesso interrompido pelo usuário. Finalizando...")
            break
        except Exception as e:
            logger.error(f"Erro durante a execução: {e}")
            time.sleep(15)