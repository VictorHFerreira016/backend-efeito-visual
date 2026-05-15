from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Telefone(Base):
    __tablename__ = "telefones"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)

    numero = Column(String(15), nullable=False)
    tipo = Column(String(50), nullable=True)

    cliente = relationship("Cliente", back_populates="telefones")