from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Date, UUID, Text, DateTime, func
from database import Base
from sqlalchemy.orm import relationship
import uuid

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_categoria = Column(UUID(as_uuid=True), ForeignKey("categorias.id", ondelete="RESTRICT"), nullable=True)
    id_fabricante = Column(UUID(as_uuid=True), ForeignKey("fabricantes.id", ondelete="RESTRICT"), nullable=True)
    id_fornecedor = Column(UUID(as_uuid=True), ForeignKey("fornecedores.id", ondelete="RESTRICT"), nullable=True)

    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Numeric(12, 2), nullable=False)
    quantidade_minima = Column(Integer, default=0, nullable=True)
    data_validade = Column(Date, nullable=True)
    observacoes = Column(Text, nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    categoria = relationship("Categoria", back_populates="produtos")
    fabricante = relationship("Fabricante", back_populates="produtos")
    fornecedor = relationship("Fornecedor", back_populates="produtos")
    estoque = relationship("Estoque", back_populates="produtos")