from sqlalchemy import Column, String, Text, UUID, Time, Numeric, DateTime, func
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Servico(Base):
    __tablename__ = "servicos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    preco = Column(Numeric(12, 2), nullable=False)
    duracao = Column(Time, nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())