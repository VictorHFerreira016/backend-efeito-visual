from sqlalchemy import Column, Numeric, String, DateTime, ForeignKey, Text, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import uuid

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id", ondelete="SET NULL"), nullable=True)

    valor_total = Column(Numeric(12, 2), nullable=False)
    forma_pagamento = Column(String, nullable=True)
    observacao = Column(Text, nullable=True)

    criado_em = Column(DateTime, server_default=func.now(), nullable=False)
    atualizado_em = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    cliente = relationship("Cliente", back_populates="vendas")
    itens = relationship("ItemVenda", back_populates="venda", cascade="all, delete-orphan")