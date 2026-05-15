from sqlalchemy import Column, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Endereco(Base):
    __tablename__ = "enderecos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    id_cliente = Column(UUID(as_uuid=True), ForeignKey("clientes.id", ondelete="CASCADE"), nullable=False)

    logradouro = Column(String, nullable=False)
    numero = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=False)
    estado = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    pais = Column(String, nullable=True, default="Brasil")

    cliente = relationship("Cliente", back_populates="enderecos")