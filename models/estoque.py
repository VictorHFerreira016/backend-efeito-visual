from sqlalchemy import Column, Integer, DateTime, func, Numeric, UUID, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Estoque(Base):
    __tablename__ = "estoque"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_produto = Column(UUID(as_uuid=True), ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=False)

    quantidade = Column(Integer, default=0, nullable=False)
    preco_pago = Column(Numeric(12, 2), nullable=False)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    produtos = relationship("Produto", back_populates="estoque")