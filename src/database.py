from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Float, String, Integer, DateTime
from datetime import datetime

Base = declarative_base()

class BitcoinPreco(Base):
    """Define a tabela no banco de dados."""
    __tablename__ = "bitcoin_precos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(Float, nullable=False)
    cripto = Column(String(50), nullable=False)  # Mudando de 'criptomoeda' para 'cripto'
    moeda = Column(String(10), nullable=False)
    time = Column(DateTime, default=datetime.now)  # Mudando de 'timestamp' para 'time'