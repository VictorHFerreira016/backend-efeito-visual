from sqlalchemy import Column, Integer, String, Float
from database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    quantidade = Column(Integer, default=0)
    preco = Column(Float, nullable=False)
    fornecedor = Column(String, nullable=True)