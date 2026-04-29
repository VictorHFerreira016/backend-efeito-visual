from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

class Produto(Base):
    __tablename__ = "produtos"

    id: Mapped[int ]= mapped_column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    categoria = Column(String, nullable=True)
    quantidade = Column(Integer, default=0)
    preco = Column(Float, nullable=False)
    fornecedor = Column(String, nullable=True)