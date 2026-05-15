from sqlalchemy import Column, String, Date, DateTime, func, Boolean, Text, UUID
from sqlalchemy.orm import relationship
from database import Base
import uuid

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)

    nome = Column(String(150), nullable=False)
    cpf = Column(String(11), nullable=True, unique=True)
    rg = Column(String(11), nullable=True)
    data_nascimento = Column(Date, nullable=True)
    sexo = Column(String(1), nullable=True)
    ativo = Column(Boolean, default=True)
    observacoes = Column(Text, nullable=True)

    criado_em = Column(DateTime(timezone=True), server_default=func.now())
    atualizado_em = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    telefones = relationship("Telefone", back_populates="cliente", cascade="all, delete-orphan")
    enderecos = relationship("Endereco", back_populates="cliente", cascade="all, delete-orphan")
    vendas = relationship("Venda", back_populates="cliente")