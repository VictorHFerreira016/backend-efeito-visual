from sqlalchemy import Column, Integer, Numeric, ForeignKey, UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,index=True)
    id_venda = Column(UUID(as_uuid=True), ForeignKey("vendas.id", ondelete="CASCADE"), nullable=False)
    id_produto = Column(UUID(as_uuid=True), ForeignKey("produtos.id", ondelete="RESTRICT"), nullable=True)
    id_servico = Column(UUID(as_uuid=True), ForeignKey("servicos.id", ondelete="RESTRICT"), nullable=True)

    quantidade = Column(Integer, nullable=True)
    preco_unitario = Column(Numeric(12, 2), nullable=True)
 
    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto")
    servico = relationship("Servico")