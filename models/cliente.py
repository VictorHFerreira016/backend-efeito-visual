from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    cpf = Column(String, nullable=True, unique=True)
    rg = Column(String, nullable=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String, nullable=True)

    telefones = relationship("Telefone", back_populates="cliente", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="cliente", cascade="all, delete-orphan")
    vendas = relationship("Venda", back_populates="cliente")